import boto3
from django.conf import settings
import uuid

def upload_to_r2(file_obj):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
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

    return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
    