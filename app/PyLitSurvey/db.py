from minio import Minio

from app.PyLitSurvey.config import logger, settings


def file_name_minio(file):
    name = str(file).split('bio_open/')[-1]
    return f'bio_open/{name}'


def save_file(file):
    minio_client = Minio(
        settings.MINIO_ENDPOINT,
        settings.MINIO_ACCESS_KEY,
        settings.MINIO_SECRET_KEY,
        secure=True,
    )
    bucket_name = settings.MINIO_BUCKET_NAME
    file = str(file)
    try:
        minio_client.fput_object(bucket_name, file_name_minio(file), file)
    except Exception as error:
        logger.exception(error)
        return False
    return True
