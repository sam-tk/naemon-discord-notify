## NaemonのDiscord通知コマンド

NaemonのDiscord向け通知コマンドです

discord_notify.pyを/usr/local/binに配置し、実効権限を付与します。

セットアップ手順は前回と同じですが、以下の点に注意してください:

1. スクリプトの実行権限を忘れずに付与
2. WEBHOOK_URLを実際のものに置き換え
3. 必要に応じてrequestsパッケージをインストール


ホストやサービスの定義で、action_urlを設定すると、通知メッセージのリンクからステータスページに飛ぶことができます。例えば：

```
define service {
    service_description    HTTP
    host_name             webserver01
    check_command         check_http
    action_url            https://your-naemon.example.com/naemon/cgi-bin/extinfo.cgi?type=2&host=$HOSTNAME$&service=$SERVICEDESC$
    # ... その他の設定 ...
}
```

hostの時のaction_urlは https://your-naemon.example.com/naemon/cgi-bin/extinfo.cgi?type=1&host=$HOSTNAME$ となります。

これにより、Discordの通知メッセージのタイトルをクリックすると、対応するNaemonのサービス詳細ページに遷移できるようになります。


