# =====================================
# config.py
# IoTポートフォリオ 共通設定ファイル
# =====================================
# このファイルでは、各Pythonファイルで共通して使う設定値を管理します。
#
# 注意：
# AWSアクセスキー、SwitchBotトークン、Secretなどの秘密情報は
# このファイルには書かず、.env に保存します。
# =====================================


# =====================================
# プロジェクト基本設定
# =====================================

# プロジェクト名
PROJECT_NAME = "IoT Portfolio - SwitchBot Sensor Data Collection"

# 取得対象のセンサー名
SENSOR_NAME = "SwitchBot 温湿度・CO2センサー"


# =====================================
# ローカルファイル設定
# =====================================

# SwitchBotから取得した最新データを保存するJSONファイル
SAMPLE_JSON_PATH = "data/sample.json"

# ログファイル保存先フォルダ
LOG_DIR = "logs"

# タスクスケジューラ等で実行した場合のログ保存先
TASK_LOG_PATH = "logs/task_log.txt"


# =====================================
# AWS S3 設定
# =====================================
# AWS認証情報は .env に保存する
# 例：
# AWS_ACCESS_KEY_ID=xxxxx
# AWS_SECRET_ACCESS_KEY=xxxxx
# AWS_DEFAULT_REGION=ap-northeast-1

# AWSリージョン
AWS_REGION = "ap-northeast-1"

# S3バケット名
S3_BUCKET_NAME = "noda-iot-switchbot-data-20260705"

# S3上の保存先フォルダ
S3_FOLDER = "switchbot-data"


# =====================================
# MQTT 設定
# =====================================
# MQTTは、センサーデータを軽量な通信で送信するために使用します。

# 無料で利用できる公開MQTTブローカー
MQTT_BROKER = "broker.hivemq.com"

# MQTT標準ポート
MQTT_PORT = 1883

# センサーデータ送信用トピック
MQTT_TOPIC = "iot/switchbot/sensor"


# =====================================
# OPC UA 設定
# =====================================
# OPC UAは、製造現場の設備データを標準的に公開する用途を想定しています。

# OPC UAサーバーのエンドポイント
OPCUA_ENDPOINT = "opc.tcp://0.0.0.0:4840/freeopcua/server/"

# OPC UAサーバー名
OPCUA_SERVER_NAME = "IoT Portfolio OPC UA Server"

# OPC UA名前空間
OPCUA_NAMESPACE = "https://iot-portfolio.local"

# OPC UA上で表示するオブジェクト名
OPCUA_OBJECT_NAME = "SwitchBot"


# =====================================
# SwitchBot API 設定
# =====================================
# SWITCHBOT_TOKEN と SWITCHBOT_SECRET は .env に保存する
# 例：
# SWITCHBOT_TOKEN=xxxxx
# SWITCHBOT_SECRET=xxxxx

# SwitchBot APIのベースURL
SWITCHBOT_API_BASE_URL = "https://api.switch-bot.com/v1.1"


# =====================================
# データ項目設定
# =====================================
# JSONデータで扱うセンサー項目

DATA_FIELDS = [
    "timestamp",
    "temperature",
    "humidity",
    "co2",
    "battery",
]


# =====================================
# 製造現場への横展開を想定した設定
# =====================================
# 面接・README説明用として、現場展開時に付与する想定項目

FACTORY_NAME = "Sample Factory"
LINE_NAME = "Line_A"
EQUIPMENT_NAME = "SwitchBot_Sensor_01"

# 製造現場でデータを管理する場合の想定ステータス
DEFAULT_STATUS = "running"

# =====================================
# WBGT / 熱中症アラート設定
# =====================================

# 簡易WBGTの危険判定しきい値
# 環境省の目安では WBGT 31以上が「運動は原則中止」相当
WBGT_DANGER_THRESHOLD = 31.0

# 厳重警戒のしきい値
WBGT_SEVERE_WARNING_THRESHOLD = 28.0

# 警戒のしきい値
WBGT_WARNING_THRESHOLD = 25.0

# CSVログ保存先
SENSOR_LOG_CSV_PATH = "data/sensor_log.csv"