# IoTポートフォリオ  
SwitchBot × Python × MQTT / OPC UA × AWS S3 × Power BI

## 概要

自宅の SwitchBot 温湿度・CO2センサーから取得した環境データを、Pythonで取得・整形し、JSON / CSV 形式で保存、AWS S3へアップロード、Power BI Desktopでダッシュボード化するIoTデータ連携システムです。

製造現場における設備データ収集、作業環境の見える化、状態監視、熱中症リスク監視、クラウド保存を想定したポートフォリオとして作成しました。

主な実装内容は以下です。

- SwitchBot APIから温度・湿度・CO2濃度を取得
- 取得データをJSON形式で保存
- 履歴データをCSV形式で蓄積
- 温度・湿度から簡易WBGTを算出
- WBGT判定を実施
- 危険区域に入った場合にメール通知
- AWS S3へ時刻付きJSONファイルとしてアップロード
- Power BI Desktopでダッシュボード化
- Windowsタスクスケジューラで30分ごとに自動実行
- MQTT送信処理
- OPC UAサーバー公開処理
- `.env` による秘密情報管理

---

## システム構成

```text
SwitchBot 温湿度・CO2センサー
        ↓
SwitchBot API
        ↓
Python
        ↓
温度・湿度・CO2を取得
        ↓
簡易WBGTを算出
        ↓
data/sample.json に最新データを保存
        ↓
data/sensor_log.csv に履歴データを追記
        ↓
AWS S3へ時刻付きJSONとしてアップロード
        ↓
Power BI Desktopで可視化

追加機能として、以下の連携も実装しています。

Python
↓
MQTTブローカーへデータ送信

Python
↓
OPC UAサーバーとしてデータ公開

WBGT危険判定
↓
対象メールアドレスへ危険アラート送信
取得データ

取得・算出しているデータは以下です。

項目	内容
timestamp	データ取得日時
temperature	温度
humidity	湿度
co2	CO2濃度
battery	SwitchBotセンサーのバッテリー残量
wbgt	温度・湿度から算出した簡易WBGT
wbgt_level	WBGT判定
JSONデータ例
{
  "timestamp": "2026-07-13 22:27:56",
  "temperature": 24.3,
  "humidity": 45,
  "co2": 811,
  "battery": 96,
  "wbgt": 22.7,
  "wbgt_level": "注意"
}
CSVログ例

Power BI Desktopで読み込むため、取得データは data/sensor_log.csv に履歴として追記保存します。

timestamp,temperature,humidity,co2,battery,wbgt,wbgt_level
2026-07-13 22:27:56,24.3,45,811,96,22.7,注意
2026-07-13 22:32:28,24.4,46,877,96,22.9,注意
簡易WBGT算出・判定

SwitchBotで取得できる温度・湿度をもとに、簡易WBGTを算出しています。

判定区分は以下のように設定しています。

簡易WBGT	判定
21未満	ほぼ安全
21以上25未満	注意
25以上28未満	警戒
28以上31未満	厳重警戒
31以上	危険

WBGTが危険区域に入った場合、指定したメールアドレスへ危険アラートを送信する構成にしています。

注意：本ポートフォリオでは、SwitchBotで取得できる温度・湿度から簡易的にWBGT相当値を算出しています。実際の職場安全管理では、黒球温度などを測定できる正式なWBGT計を使用する必要があります。

AWS S3連携

Pythonの boto3 ライブラリを使用し、取得したセンサーデータをAWS S3へアップロードします。

保存先は以下の形式です。

s3://noda-iot-switchbot-data-20260705/switchbot-data/sample_YYYYMMDD_HHMMSS.json

ファイル名に日時を付与することで、時系列データとして保存できるようにしています。

例：

s3://noda-iot-switchbot-data-20260705/switchbot-data/sample_20260713_222756.json
Power BI Desktopによるダッシュボード化

Pythonで作成した data/sensor_log.csv をPower BI Desktopで読み込み、環境データをダッシュボード化しています。

可視化項目
簡易WBGT推移
温度・湿度推移
CO2濃度推移
WBGT判定別件数
最新センサーデータ一覧
ダッシュボード構成
sensor_log.csv
↓
Power BI Desktop
↓
WBGT推移グラフ
温度・湿度推移グラフ
CO2推移グラフ
WBGT判定別件数
最新センサーデータ一覧
目的

製造現場における作業環境の見える化を想定し、温度・湿度・CO2濃度・簡易WBGTをダッシュボード上で確認できるようにしています。

これにより、熱中症リスクの傾向把握、作業環境の確認、現場の安全管理に活用できる構成としています。

メールアラート機能

簡易WBGTが危険区域に入った場合、Pythonから対象メールアドレスへ危険アラートを送信します。

SwitchBotから最新データ取得
↓
簡易WBGTを算出
↓
WBGT判定
↓
危険区域の場合
↓
メールアラート送信

メール送信に必要な情報は .env に保存し、GitHubには公開しないようにしています。

30分ごとの自動実行

Windowsタスクスケジューラを使用し、30分ごとに run_main.bat を実行する構成にしています。

処理の流れは以下です。

30分ごとにタスクスケジューラが起動
↓
run_main.bat を実行
↓
仮想環境 .venv を有効化
↓
python main.py を実行
↓
SwitchBotから最新データ取得
↓
data/sample.json に保存
↓
data/sensor_log.csv に履歴追記
↓
簡易WBGTを算出・判定
↓
必要に応じてメール通知
↓
AWS S3へアップロード
↓
logs/task_log.txt に実行ログ保存
使用技術
分類	使用技術
言語	Python
センサー	SwitchBot 温湿度・CO2センサー
API通信	SwitchBot API
データ形式	JSON / CSV
クラウド保存	AWS S3
AWS連携	boto3
ダッシュボード	Power BI Desktop
メール通知	SMTP / Gmailアプリパスワード
通信	MQTT
産業用通信	OPC UA
認証情報管理	python-dotenv / .env
自動実行	Windowsタスクスケジューラ
バージョン管理	Git / GitHub
開発環境	VS Code
ファイル構成
IOT ポートフォリオ/
├─ data/
│  ├─ sample.json
│  └─ sensor_log.csv
├─ logs/
│  └─ task_log.txt
├─ powerbi/
│  └─ WBGT_dashboard.pbix
├─ .env
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ main.py
├─ switchbot.py
├─ aws_sender.py
├─ mqtt_sender.py
├─ opcua_server.py
├─ alert_sender.py
├─ config.py
└─ run_main.bat
各ファイルの役割
ファイル	役割
main.py	全体処理を実行するメインファイル
switchbot.py	SwitchBot APIから最新データを取得し、JSON / CSVに保存する
aws_sender.py	data/sample.json をAWS S3へアップロードする
mqtt_sender.py	MQTTブローカーへセンサーデータを送信する
opcua_server.py	OPC UAサーバーとしてセンサーデータを公開する
alert_sender.py	WBGT危険判定時にメール通知を送信する
config.py	S3、MQTT、OPC UA、WBGTしきい値など共通設定を管理する
run_main.bat	タスクスケジューラからPython処理を実行するためのバッチファイル
requirements.txt	必要なPythonライブラリ一覧
.env	AWSキー、SwitchBotトークン、メール設定など秘密情報を保存する
.gitignore	GitHubに上げないファイルを指定する
README.md	システム説明書・ポートフォリオ説明
data/sample.json	最新の取得データ保存ファイル
data/sensor_log.csv	Power BI用の履歴データ
logs/task_log.txt	自動実行時のログ保存先
powerbi/WBGT_dashboard.pbix	Power BI Desktopで作成したダッシュボード
セキュリティ対策

AWSアクセスキー、SwitchBot APIトークン、メール送信用パスワードは .env に保存し、GitHubへアップロードしないよう .gitignore に登録しています。

.env に保存する情報の例です。

SWITCHBOT_TOKEN=xxxxx
SWITCHBOT_SECRET=xxxxx
SWITCHBOT_DEVICE_ID=xxxxx

AWS_ACCESS_KEY_ID=xxxxx
AWS_SECRET_ACCESS_KEY=xxxxx
AWS_DEFAULT_REGION=ap-northeast-1

ALERT_EMAIL_FROM=xxxxx
ALERT_EMAIL_TO=xxxxx
ALERT_EMAIL_PASSWORD=xxxxx
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

.gitignore には以下を設定しています。

.venv/
.env
__pycache__/
logs/
資料保管/
*accessKeys*.csv
*.pyc
*.log

これにより、秘密情報や実行ログがGitHubに公開されないようにしています。

実行方法

必要なライブラリをインストールします。

pip install -r requirements.txt

メイン処理を実行する場合は以下を実行します。

python main.py

AWS S3へのアップロード処理だけを確認する場合は以下を実行します。

python aws_sender.py

SwitchBotデータ取得処理だけを確認する場合は以下を実行します。

python switchbot.py

タスクスケジューラから実行する場合は、以下のバッチファイルを使用します。

run_main.bat
Power BI Desktopでの更新方法

Python側で sensor_log.csv が更新された後、Power BI Desktopで以下を実行すると最新データが反映されます。

ホーム
↓
更新

CSVの列名や型を変更した場合は、Power Queryで型を確認したうえで「閉じて適用」を行います。

製造現場での横展開イメージ

本システムは、自宅のSwitchBotセンサーを用いた簡易的なIoTデータ連携システムですが、製造現場では以下のように横展開できます。

1. 設備・工程ごとの状態監視

各製造ラインや設備にセンサーを設置し、温度・湿度・CO2・稼働状態・異常信号などを定期的に取得します。

各設備・各ライン
↓
センサー / PLC / IoT機器
↓
PythonまたはゲートウェイPC
↓
MQTT / OPC UA
↓
クラウド・社内サーバー
↓
Excel / Power BI / 監視画面

これにより、現場の状態を手作業で記録するのではなく、自動でデータ収集・蓄積できるようになります。

2. ライン単位でのデータ収集

本ポートフォリオでは1台のセンサーからデータ取得していますが、製造現場では以下のように複数ラインへ展開できます。

展開先	取得データ例	活用例
成形ライン	温度、湿度、設備稼働状態	品質条件の記録、不良発生時の要因確認
組立ライン	稼働時間、停止時間、異常回数	チョコ停分析、稼働率改善
検査工程	検査結果、不良数、判定データ	品質傾向の見える化
保管エリア	温度、湿度、CO2	保管環境の監視、品質維持
設備保全	電流値、振動、異常信号	予防保全、異常兆候の早期発見
3. OPC UA / MQTTを使った標準化

製造現場では、設備メーカーやPLCの種類が異なる場合があります。
そのため、データ取得方法を設備ごとに個別対応すると、管理が複雑になります。

そこで、OPC UAやMQTTを活用することで、以下のような標準化が可能になります。

設備ごとのデータ形式を統一する
取得項目名を標準化する
データ送信先を統一する
ライン追加時の展開手順を共通化する
現場・保全・品質・生産管理で同じデータを活用する

例：

{
  "line": "Line_A",
  "equipment": "Machine_01",
  "timestamp": "2026-07-13 22:27:56",
  "temperature": 24.3,
  "humidity": 45,
  "co2": 811,
  "wbgt": 22.7,
  "wbgt_level": "注意",
  "status": "running"
}

このようにデータ形式を統一することで、別ラインや別設備にも同じ仕組みを展開しやすくなります。

4. AWS S3を使ったデータ蓄積

本システムでは、取得したデータをAWS S3へJSON形式で保存しています。
製造現場で活用する場合、S3をデータ保管場所として利用することで、以下のような活用ができます。

日時ごとの設備データ履歴を保存
不良発生時の環境データ確認
ライン別・設備別のデータ保管
Power BIによる可視化
将来的なAI分析や予兆保全への活用

保存先の例：

s3://factory-iot-data/line-a/machine-01/2026/07/13/data_222756.json
s3://factory-iot-data/line-b/machine-03/2026/07/13/data_223000.json

ライン名・設備名・日付でフォルダを分けることで、後からデータを検索・分析しやすくなります。

5. 横展開時のメリット

この仕組みを製造現場へ横展開することで、以下の効果が期待できます。

項目	期待できる効果
手書き記録の削減	現場作業者の記録負担を軽減
データの見える化	設備状態や環境変化を把握しやすくする
異常時の原因調査	不良や停止が発生した時のデータ確認が可能
熱中症対策	WBGT傾向を把握し、作業環境改善につなげる
保全活動への活用	異常傾向を早期に把握し、予防保全につなげる
標準化	他ライン・他拠点へ同じ仕組みを展開しやすい
今後の拡張イメージ

今後は以下のような機能を追加することで、より実際の製造IoTに近い構成へ拡張できます。

複数センサー対応
ライン名・設備名の自動付与
S3保存先の日付別フォルダ化
Power BIダッシュボードのレイアウト改善
WBGT危険区域の条件付き書式
異常値検知の精度向上
PLCデータとの連携
AWS Lambdaとの連携
Amazon QuickSightでのクラウドダッシュボード化
社内ネットワーク上のMQTTブローカーとの連携


このポートフォリオは、製造現場の環境データ収集と見える化を想定して作成しました。
SwitchBotセンサーから温度・湿度・CO2濃度をPythonで取得し、簡易WBGTを算出しています。
取得したデータはJSONとしてローカル保存し、AWS S3へ時刻付きファイルとしてアップロードしています。
また、CSVログとして履歴保存し、Power BI DesktopでWBGT推移、温度・湿度推移、CO2推移、WBGT判定別件数を可視化しています。
さらに、Windowsタスクスケジューラを使い、30分ごとに自動でデータ取得・保存できる構成にしています。
製造現場では、作業環境の見える化、熱中症リスク監視、品質条件の記録、保全活動への活用に展開できると考えています。