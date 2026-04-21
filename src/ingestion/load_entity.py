import argparse
import json

from src.common.config import get_f1_api_base_url, get_minio_settings
from src.common.paths import (
    build_raw_file_path,
    build_raw_object_key,
    build_timestamp,
)
from src.ingestion.client import F1ApiClient
from src.ingestion.storage import upload_file_to_minio


def load_single_entity(season: int, entity: str) -> None:
    print(f"[START] Начинаю загрузку entity={entity}, season={season}")

    api_base_url = get_f1_api_base_url()
    print(f"[API] Base URL: {api_base_url}")

    client = F1ApiClient(api_base_url)
    data = client.get_data(season, entity)
    print("[API] Данные успешно получены")

    timestamp = build_timestamp()
    file_path = build_raw_file_path(entity, season, timestamp)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"[LOCAL] Файл сохранен локально: {file_path}")

    _, _, _, bucket_name, _ = get_minio_settings()

    object_key = build_raw_object_key(
        entity=entity,
        season=season,
        timestamp=timestamp,
        file_name=file_path.name,
    )

    upload_file_to_minio(file_path, bucket_name, object_key)

    print(f"[MINIO] Bucket: {bucket_name}")
    print(f"[MINIO] Object key: {object_key}")
    print(f"[DONE] Загрузка entity={entity} завершена успешно")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", type=int, required=True)
    parser.add_argument(
        "--entity",
        type=str,
        required=True,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_single_entity(season=args.season, entity=args.entity)


if __name__ == "__main__":
    main()