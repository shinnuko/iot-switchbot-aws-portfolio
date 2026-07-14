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

import csv
from config import SENSOR_LOG_CSV_PATH


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

    temperature = body.get("temperature")
    humidity = body.get("humidity")

    wbgt = calculate_simple_wbgt(temperature, humidity)
    wbgt_level = judge_wbgt_level(wbgt)

    sensor_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "humidity": humidity,
        "co2": body.get("CO2") or body.get("co2"),
        "battery": body.get("battery"),
        "wbgt": wbgt,
        "wbgt_level": wbgt_level,
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

    # CSVログに追記
    append_sensor_log_csv(sensor_data)    

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

def calculate_simple_wbgt(temperature, humidity):
    """
    温度・湿度から簡易WBGTを算出する
    注意：
    正式なWBGTでは黒球温度なども必要。
    ここではポートフォリオ用の簡易推定値として使用する。
    """

    if temperature is None or humidity is None:
        return None

    # 簡易式：屋内・日射なしの目安として使用
    wbgt = 0.735 * temperature + 0.0374 * humidity + 0.00292 * temperature * humidity + 7.619 * 0 - 4.557 * 0 - 0.0572

    return round(wbgt, 1)


def judge_wbgt_level(wbgt):
    """
    WBGT値から危険度を判定する
    """

    if wbgt is None:
        return "判定不可"

    if wbgt >= 31:
        return "危険"
    elif wbgt >= 28:
        return "厳重警戒"
    elif wbgt >= 25:
        return "警戒"
    elif wbgt >= 21:
        return "注意"
    else:
        return "ほぼ安全"


def append_sensor_log_csv(sensor_data):
    """
    Power BI Desktopで読み込むためのCSVログを追記保存する
    """

    csv_path = Path(SENSOR_LOG_CSV_PATH)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = csv_path.exists()

    fieldnames = [
        "timestamp",
        "temperature",
        "humidity",
        "co2",
        "battery",
        "wbgt",
        "wbgt_level",
    ]

    with open(csv_path, "a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": sensor_data.get("timestamp"),
            "temperature": sensor_data.get("temperature"),
            "humidity": sensor_data.get("humidity"),
            "co2": sensor_data.get("co2"),
            "battery": sensor_data.get("battery"),
            "wbgt": sensor_data.get("wbgt"),
            "wbgt_level": sensor_data.get("wbgt_level"),
        })