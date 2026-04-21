from minio import Minio
from src.common.config import get_minio_settings


def get_minio_client():
    endpoint, access_key, secret_key, _, _, secure = get_minio_settings()

    client = Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure,
    )
    return client


def upload_file_to_minio(file_path, bucket_name, object_key) -> None:
    client = get_minio_client()

    client.fput_object(
        bucket_name,
        object_key,
        str(file_path),
    )