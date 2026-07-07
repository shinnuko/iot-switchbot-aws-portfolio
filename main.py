import json
from pathlib import Path

from switchbot import save_switchbot_data
from aws_sender import upload_to_s3


DATA_FILE = Path("data/sample.json")


def show_sensor_data():
    if not DATA_FILE.exists():
        print("data/sample.json が見つかりません。")
        return False

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("現在のセンサーデータ:")
    print(f"時刻: {data.get('timestamp')}")
    print(f"温度: {data.get('temperature')} ℃")
    print(f"湿度: {data.get('humidity')} %")
    print(f"CO2: {data.get('co2')} ppm")
    print(f"電池: {data.get('battery')} %")

    return True


def main():
    print("IoTポートフォリオ処理を開始します")

    print("SwitchBotから最新データを取得します")
    save_switchbot_data()

    print("取得したデータを確認します")
    if not show_sensor_data():
        return

    print("AWS S3へアップロードします")
    upload_to_s3(str(DATA_FILE))

    print("処理が完了しました")


if __name__ == "__main__":
    main()