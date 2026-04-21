import json

from src.common.config import get_f1_api_base_url, get_minio_settings
from src.common.paths import build_timestamp
from src.ingestion.storage import upload_file_to_minio
from src.ingestion.client_results import F1ResultsApiClient
from src.common.paths_results import build_results_raw_file_path, build_results_raw_object_key


def main() -> None:
    season = 2023
    round_number = 1

    print(f"[START] Загружаю results: season={season}, round={round_number}")

    api_base_url = get_f1_api_base_url()
    client = F1ResultsApiClient(api_base_url)

    data = client.get_results(season=season, round_number=round_number)
    print("[API] Results успешно получены")

    timestamp = build_timestamp()
    file_path = build_results_raw_file_path(season, round_number, timestamp)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"[LOCAL] Файл сохранен: {file_path}")

    _, _, _, raw_bucket_name, _, _ = get_minio_settings()

    object_key = build_results_raw_object_key(
        season=season,
        round_number=round_number,
        timestamp=timestamp,
        file_name=file_path.name,
    )

    upload_file_to_minio(file_path, raw_bucket_name, object_key)

    print(f"[MINIO] Bucket: {raw_bucket_name}")
    print(f"[MINIO] Object key: {object_key}")
    print("[DONE] Results raw ingestion завершен")
    

if __name__ == "__main__":
    main()