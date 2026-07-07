import json
import time
from pathlib import Path

import paho.mqtt.client as mqtt


# =====================================
# MQTT設定
# =====================================
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot_portfolio/switchbot"

# 送信するJSONファイル
DATA_FILE = Path("data/sample.json")


def send_mqtt():
    # -----------------------------
    # JSONファイル存在確認
    # -----------------------------
    if not DATA_FILE.exists():
        print("data/sample.json が見つかりません。")
        return

    # -----------------------------
    # JSONファイル読み込み
    # -----------------------------
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    payload = json.dumps(data, ensure_ascii=False)

    # -----------------------------
    # MQTTクライアント作成
    # -----------------------------
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id=f"switchbot-publisher-{int(time.time())}"
    )

    # -----------------------------
    # MQTTブローカーへ接続
    # -----------------------------
    print("MQTTブローカーへ接続します")
    print(f"Broker: {MQTT_BROKER}")
    print(f"Port: {MQTT_PORT}")
    print(f"Topic: {MQTT_TOPIC}")

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # -----------------------------
    # MQTT送信
    # -----------------------------
    client.loop_start()

    result = client.publish(
        MQTT_TOPIC,
        payload,
        qos=0,
        retain=True
    )

    result.wait_for_publish()

    client.loop_stop()
    client.disconnect()

    print("MQTT送信が完了しました")
    print("送信データ:")
    print(payload)


if __name__ == "__main__":
    send_mqtt()