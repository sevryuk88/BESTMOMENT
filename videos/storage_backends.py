from storages.backends.s3boto3 import S3Boto3Storage
from boto3.s3.transfer import TransferConfig
from io import BytesIO

class R2MediaStorage(S3Boto3Storage):
    default_acl = None
    file_overwrite = False
    custom_domain = False

    def get_object_parameters(self, name):
        params = super().get_object_parameters(name)
        params['ContentType'] = 'application/octet-stream'
        return params

    def _save_content(self, obj, content, parameters):
        content.open()
        content = content.read()
        transfer_config = TransferConfig(multipart_threshold=1024 * 1024 * 100,  # 100MB
                                          max_concurrency=1,
                                          multipart_chunksize=1024 * 1024 * 100,  # 100MB
                                          use_threads=False)
        obj.upload_fileobj(Fileobj=BytesIO(content),
                           Config=transfer_config,
                           **parameters)
                           