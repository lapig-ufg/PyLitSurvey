from minio import Minio
from PyLitSurvey.config import settings, logger

def file_name_minio(file):
    return file.split('bio_open/')[-1]

def save_file(file):
    minio_client = Minio(
        settings.MINIO_ENDPOINT,
        settings.MINIO_ACCESS_KEY,
        settings.MINIO_SECRET_KEY,
        secure=True,
    )
    bucket_name = settings.MINIO_BUCKET_NAME
    file = str(file)
    file_name = file_name_minio(file)
    try:
        minio_client.fput_object(bucket_name, f'bio_open/{file_name}', file)
    except Exception as error:
        logger.exception(error)
        return False
    return True