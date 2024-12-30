#!/usr/bin/env python3
import sys
import json
import requests
from datetime import datetime
from argparse import ArgumentParser

# Discord Webhook URL - 実際のWebhook URLに置き換えてください
WEBHOOK_URL = "https://discord.com/api/webhooks/"

# 通知タイプに応じた絵文字とカラーの設定
STATUS_CONFIG = {
    'DOWN': {'emoji': '🔴', 'color': 16711680},  # 赤
    'UP': {'emoji': '🟢', 'color': 65280},      # 緑
    'CRITICAL': {'emoji': '🚫', 'color': 16711680},
    'WARNING': {'emoji': '⚠️', 'color': 16776960},
    'OK': {'emoji': '🟢', 'color': 65280},
    'UNKNOWN': {'emoji': '⚪', 'color': 8421504}
}

def send_host_notification(notification_type, hostname, state, output, url):
    status_info = STATUS_CONFIG.get(state, {'emoji': '❓', 'color': 8421504})
    title = f"{status_info['emoji']} Host Alert: {hostname} is {state}"
    
    embed = {
        "title": title,
        "color": status_info['color'],
        "fields": [
            {
                "name": "Status",
                "value": state,
                "inline": True
            },
            {
                "name": "Host",
                "value": hostname,
                "inline": True
            },
            {
                "name": "Notification Type",
                "value": notification_type,
                "inline": True
            }
        ],
        "timestamp": datetime.utcnow().isoformat(),
        "url": url
    }
    
    if output:
        embed["fields"].append({
            "name": "Details",
            "value": output,
            "inline": False
        })
    
    send_to_discord(embed)

def send_service_notification(notification_type, hostname, service_desc, state, output, url):
    status_info = STATUS_CONFIG.get(state, {'emoji': '❓', 'color': 8421504})
    title = f"{status_info['emoji']} Service Alert: {hostname}/{service_desc} is {state}"
    
    embed = {
        "title": title,
        "color": status_info['color'],
        "fields": [
            {
                "name": "Status",
                "value": state,
                "inline": True
            },
            {
                "name": "Host",
                "value": hostname,
                "inline": True
            },
            {
                "name": "Service",
                "value": service_desc,
                "inline": True
            },
            {
                "name": "Notification Type",
                "value": notification_type,
                "inline": True
            }
        ],
        "timestamp": datetime.utcnow().isoformat(),
        "url": url
    }
    
    if output:
        embed["fields"].append({
            "name": "Details",
            "value": output,
            "inline": False
        })
    
    send_to_discord(embed)

def send_to_discord(embed):
    payload = {"embeds": [embed]}
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print(f"Successfully sent notification to Discord: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification to Discord: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = ArgumentParser(description='Send Naemon notifications to Discord')
    
    # ホスト通知用のサブコマンド
    subparsers = parser.add_subparsers(dest='command', help='Notification type')
    
    host_parser = subparsers.add_parser('host', help='Host notification')
    host_parser.add_argument('notification_type', help='Notification type')
    host_parser.add_argument('hostname', help='Host name')
    host_parser.add_argument('state', help='Host state')
    host_parser.add_argument('output', help='Host check output')
    host_parser.add_argument('url', help='Action URL for the host')
    
    # サービス通知用のサブコマンド
    service_parser = subparsers.add_parser('service', help='Service notification')
    service_parser.add_argument('notification_type', help='Notification type')
    service_parser.add_argument('hostname', help='Host name')
    service_parser.add_argument('service_desc', help='Service description')
    service_parser.add_argument('state', help='Service state')
    service_parser.add_argument('output', help='Service check output')
    service_parser.add_argument('url', help='Action URL for the service')
    
    args = parser.parse_args()
    
    if args.command == 'host':
        send_host_notification(
            args.notification_type,
            args.hostname,
            args.state,
            args.output,
            args.url
        )
    elif args.command == 'service':
        send_service_notification(
            args.notification_type,
            args.hostname,
            args.service_desc,
            args.state,
            args.output,
            args.url
        )
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
