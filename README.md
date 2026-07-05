# IoTポートフォリオ  
SwitchBot × Python × MQTT / OPC UA × AWS S3

## 概要

自宅のSwitchBot温湿度・CO2センサーから取得したデータを、PythonでJSON形式に変換し、MQTT送信、OPC UAサーバー公開、AWS S3への保存を行うIoTデータ連携システムです。

製造業における設備データ収集、状態監視、遠隔監視、クラウド保存を想定したポートフォリオとして作成しました。

## システム構成

```text
SwitchBot 温湿度・CO2センサー
        ↓
Pythonでデータ取得
        ↓
JSONファイルに保存
        ↓
MQTTでデータ送信
        ↓
OPC UAサーバーでデータ公開
        ↓
AWS S3へアップロード


取得データ
取得しているデータは以下です。

| 項目          | 内容      |
| ----------- | ------- |
| timestamp   | データ取得日時 |
| temperature | 温度      |
| humidity    | 湿度      |
| co2         | CO2濃度   |
| battery     | バッテリー残量 |


JSONデータ例

{
  "timestamp": "2026-07-04 22:44:34",
  "temperature": 27.9,
  "humidity": 64,
  "co2": 480,
  "battery": 96
}


AWS S3連携
Pythonの boto3 ライブラリを使用し、取得したセンサーデータをAWS S3へアップロードします。
保存先は以下の形式です。
s3://noda-iot-switchbot-data-20260705/switchbot-data/sample_YYYYMMDD_HHMMSS.json
ファイル名に日時を付与することで、時系列データとして保存できるようにしています。


使用技術
| 分類     | 使用技術    |
| ------ | ------- |
| 言語     | Python  |
| データ形式  | JSON    |
| クラウド   | AWS S3  |
| 通信     | MQTT    |
| 産業用通信  | OPC UA  |
| 認証情報管理 | .env    |
| 開発環境   | VS Code |


ファイル構成

IOT ポートフォリオ/
├─ data/
│  └─ sample.json
├─ logs/
├─ .env
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ main.py
├─ switchbot.py
├─ mqtt_sender.py
├─ opcua_server.py
├─ aws_sender.py
└─ config.py

セキュリティ対策
AWSアクセスキーやSwitchBot APIトークンは .env に保存し、GitHubへアップロードしないよう .gitignore に登録しています。

.env
*accessKeys*.csv
資料保管/

実行方法
必要なライブラリをインストールします。
pip install -r requirements.txt

AWS S3へアップロードする場合は以下を実行します。
python aws_sender.py

メイン処理を実行する場合は以下を実行します。
python main.py


