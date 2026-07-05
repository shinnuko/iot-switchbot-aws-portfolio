import os
import boto3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = "noda-iot-switchbot-data-20260705"
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-1")


def upload_to_s3(local_file="data/sample.json"):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    s3_key = f"switchbot-data/sample_{now}.json"

    s3 = boto3.client(
        "s3",
        region_name=REGION_NAME,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    s3.upload_file(
        local_file,
        BUCKET_NAME,
        s3_key
    )

    s3_uri = f"s3://{BUCKET_NAME}/{s3_key}"

    print("S3へのアップロードが完了しました")
    print(s3_uri)

    return s3_uri


if __name__ == "__main__":
    upload_to_s3()