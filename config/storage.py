from storages.backends.s3 import S3Storage


class MediaStorage(S3Storage):
    default_acl = None
    file_overwrite = False