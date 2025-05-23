from storages.backends.s3boto3 import S3Boto3Storage
from io import BytesIO


class R2MediaStorage(S3Boto3Storage):
    default_acl = None
    file_overwrite = False
    custom_domain = False

    def _save_content(self, obj, content, parameters):
        # Принудительно читаем весь файл в память (R2 не поддерживает multipart)
        content.open()
        content = content.read()
        obj.upload_fileobj(
            Fileobj=BytesIO(content),
            **parameters,
        )
        