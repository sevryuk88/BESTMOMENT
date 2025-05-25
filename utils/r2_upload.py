
import boto3
from django.conf import settings
import uuid

def upload_to_r2(file_obj):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://pub-e9b60722b96746639438295f50602ef5.r2.dev',  # ← ПРАВИЛЬНЫЙ endpoint
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    filename = f"{uuid.uuid4()}.mp4"
    s3.upload_fileobj(
        Fileobj=file_obj,
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=filename,
        ExtraArgs={"ContentType": "video/mp4"}
    )

    return f"https://cdn.bestmoment.org/{filename}"
