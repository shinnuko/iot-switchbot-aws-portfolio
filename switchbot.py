import os
import time
import hmac
import hashlib
import base64
import uuid
import json
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


# =====================================
# .env 読み込み
# =====================================
load_dotenv()

TOKEN = os.getenv("SWITCHBOT_TOKEN")
SECRET = os.getenv("SWITCHBOT_SECRET")
DEVICE_ID = os.getenv("SWITCHBOT_DEVICE_ID")


# =====================================
# 保存先ファイル
# =====================================
SAMPLE_JSON_PATH = Path("data/sample.json")


# =====================================
# SwitchBot API認証ヘッダー作成
# =====================================
def make_headers():
    nonce = str(uuid.uuid4())
    timestamp = str(int(round(time.time() * 1000)))

    string_to_sign = f"{TOKEN}{timestamp}{nonce}"

    sign = base64.b64encode(
        hmac.new(
            SECRET.encode("utf-8"),
            msg=string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()
    ).decode("utf-8")

    return {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
        "charset": "utf8",
        "t": timestamp,
        "sign": sign,
        "nonce": nonce,
    }


# =====================================
# SwitchBotデバイス状態取得
# =====================================
def get_device_status(device_id):
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/status"
    response = requests.get(url, headers=make_headers())
    response.raise_for_status()
    return response.json()


# =====================================
# SwitchBotデータを整形する
# =====================================
def format_sensor_data(api_response):
    body = api_response.get("body", {})

    sensor_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": body.get("temperature"),
        "humidity": body.get("humidity"),
        "co2": body.get("CO2") or body.get("co2"),
        "battery": body.get("battery"),
    }

    return sensor_data


# =====================================
# SwitchBotデータを data/sample.json に保存する
# main.py から呼び出す関数
# =====================================
def save_switchbot_data():
    if not TOKEN:
        raise ValueError("SWITCHBOT_TOKEN が .env に設定されていません。")

    if not SECRET:
        raise ValueError("SWITCHBOT_SECRET が .env に設定されていません。")

    if not DEVICE_ID:
        raise ValueError("SWITCHBOT_DEVICE_ID が .env に設定されていません。")

    # SwitchBot APIから最新データを取得
    api_response = get_device_status(DEVICE_ID)

    # 必要なデータだけに整形
    sensor_data = format_sensor_data(api_response)

    # dataフォルダがなければ作成
    SAMPLE_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)

    # JSONとして保存
    with open(SAMPLE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(sensor_data, f, ensure_ascii=False, indent=4)

    print("SwitchBotから最新データを取得しました")
    print(f"保存先: {SAMPLE_JSON_PATH}")
    print(sensor_data)

    return sensor_data


# =====================================
# 単体実行用
# python switchbot.py で動作確認できる
# =====================================
if __name__ == "__main__":
    save_switchbot_data()