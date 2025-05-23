
import boto3
from django.conf import settings
from uuid import uuid4

def upload_to_r2(file):
    session = boto3.session.Session()
    client = session.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    filename = f"videos/{uuid4()}.mp4"
    client.upload_fileobj(
        file,
        settings.AWS_STORAGE_BUCKET_NAME,
        filename,
        ExtraArgs={'ContentType': 'video/mp4'}
    )

    return filename  # возвращаем путь, а не URL
            