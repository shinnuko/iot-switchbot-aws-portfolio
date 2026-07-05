import json
import paho.mqtt.client as mqtt


# =====================================
# MQTT送信
# センサーデータをMQTTブローカーへ送信する
# =====================================
def send_mqtt(data):
    broker = "localhost"
    port = 1883
    topic = "iot_portfolio/switchbot/room"

    try:
        print("MQTT接続開始")

        client = mqtt.Client()
        client.connect(broker, port, 10)

        payload = json.dumps(data, ensure_ascii=False)

        result = client.publish(topic, payload)
        result.wait_for_publish()

        client.disconnect()

        print("MQTT送信成功")
        print("Topic:", topic)
        print("Payload:", payload)

    except Exception as e:
        print("MQTT送信失敗")
        print("エラー内容:", e)