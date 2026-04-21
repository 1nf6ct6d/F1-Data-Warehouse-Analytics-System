import os
from dotenv import load_dotenv

load_dotenv()


def get_f1_api_base_url() -> str:
    base_url = os.getenv("F1_API_BASE_URL")
    if base_url is None:
        raise ValueError("F1_API_BASE_URL пустой")
    return base_url


def get_minio_settings() -> tuple[str, str, str, str, str, bool]:
    minio_endpoint = os.getenv("MINIO_ENDPOINT")
    minio_access_key = os.getenv("MINIO_ACCESS_KEY")
    minio_secret_key = os.getenv("MINIO_SECRET_KEY")
    minio_bucket_raw = os.getenv("MINIO_BUCKET_RAW")
    minio_bucket_staging = os.getenv("MINIO_BUCKET_STAGING")
    secure_raw = os.getenv("MINIO_SECURE", "false")
    minio_secure = secure_raw.lower() == "true"

    if minio_endpoint is None:
        raise ValueError("MINIO_ENDPOINT пустой")
    if minio_access_key is None:
        raise ValueError("MINIO_ACCESS_KEY пустой")
    if minio_secret_key is None:
        raise ValueError("MINIO_SECRET_KEY пустой")
    if minio_bucket_raw is None:
        raise ValueError("MINIO_BUCKET_RAW пустой")
    if minio_bucket_staging is None:
        raise ValueError("MINIO_BUCKET_STAGING пустой")

    return (
        minio_endpoint,
        minio_access_key,
        minio_secret_key,
        minio_bucket_raw,
        minio_bucket_staging,
        minio_secure,
    )

def get_oracle_settings() -> tuple[str, str, str, str, str]:
    host = os.getenv("ORACLE_HOST")
    port = os.getenv("ORACLE_PORT")
    service_name = os.getenv("ORACLE_SERVICE_NAME")
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")

    if host is None:
        raise ValueError("ORACLE_HOST пустой")
    if port is None:
        raise ValueError("ORACLE_PORT пустой")
    if service_name is None:
        raise ValueError("ORACLE_SERVICE_NAME пустой")
    if user is None:
        raise ValueError("ORACLE_USER пустой")
    if password is None:
        raise ValueError("ORACLE_PASSWORD пустой")

    return host, port, service_name, user, password