import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from dotenv import load_dotenv

load_dotenv()


def send_wbgt_alert(sensor_data):
    """
    WBGT危険区域に入った場合にメールを送信する
    """

    email_from = os.getenv("ALERT_EMAIL_FROM")
    email_to = os.getenv("ALERT_EMAIL_TO")
    email_password = os.getenv("ALERT_EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not email_from or not email_to or not email_password:
        print("メール送信設定が .env に不足しています。")
        return

    subject = "【危険アラート】WBGTが危険区域に入りました"

    body = f"""
WBGT危険アラートです。

以下のセンサーデータが危険区域に入りました。

取得時刻: {sensor_data.get("timestamp")}
温度: {sensor_data.get("temperature")} ℃
湿度: {sensor_data.get("humidity")} %
CO2: {sensor_data.get("co2")} ppm
バッテリー: {sensor_data.get("battery")} %
簡易WBGT: {sensor_data.get("wbgt")} ℃
判定: {sensor_data.get("wbgt_level")}

現場では休憩、水分・塩分補給、作業負荷の見直し、空調・送風の確認を行ってください。

※この値はSwitchBotの温度・湿度から算出した簡易WBGTです。
正式な安全管理ではWBGT計による測定値を使用してください。
"""

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = email_from
    msg["To"] = email_to

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_from, email_password)
            server.send_message(msg)

        print("WBGT危険アラートメールを送信しました")

    except Exception as e:
        print("メール送信に失敗しました")
        print(e)