import os
import time
import hmac
import hashlib
import base64
import uuid

import requests
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("SWITCHBOT_TOKEN")
SECRET = os.getenv("SWITCHBOT_SECRET")


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
    return response.json()