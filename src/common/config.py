import os
from dotenv import load_dotenv

load_dotenv()

def get_f1_api_base_url():
    base_url=os.getenv('F1_API_BASE_URL')
    if base_url is None:
        raise ValueError("Base url пустой")
    return base_url

def get_minio_settings():
    
    minio_endpoint=os.getenv('MINIO_ENDPOINT')
    minio_acces_key=os.getenv('MINIO_ACCESS_KEY')
    minio_secret_key=os.getenv('MINIO_SECRET_KEY')
    minio_bucket_raw=os.getenv('MINIO_BUCKET_RAW')
    secure_raw = os.getenv("MINIO_SECURE", "false")
    minio_secure = secure_raw.lower() == "true"
    
    if minio_endpoint is None:
        raise ValueError("minio_endpoint пустой")
    if minio_acces_key is None:
        raise ValueError("minio_acces_key пустой")
    if minio_secret_key is None:
        raise ValueError("minio_secret_key пустой")
    if minio_bucket_raw is None:
        raise ValueError("minio_bucket_raw пустой")
    
    return minio_endpoint, minio_acces_key, minio_secret_key , minio_bucket_raw, minio_secure