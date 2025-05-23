
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
    client.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, filename, ExtraArgs={'ACL': 'public-read'})

    return f"{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
    


'''

import requests

def upload_to_r2(file_path, file_name):
    url = f"https://pub-e9b60722b96746639438295f50602ef5.r2.dev/videos/{file_name}"

    headers = {
        "Content-Type": "video/mp4",
    }

    with open(file_path, 'rb') as f:
        response = requests.put(url, headers=headers, data=f)

    if response.status_code in [200, 201]:
        return url  # Ссылка на видео
    else:
        raise Exception(f"Upload failed: {response.status_code} {response.text}")
        
'''
        