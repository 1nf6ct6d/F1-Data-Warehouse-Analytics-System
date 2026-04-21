import json

from src.common.config import get_f1_api_base_url, get_minio_settings
from src.common.paths import build_timestamp
from src.common.paths_results import build_results_raw_file_path, build_results_raw_object_key
from src.ingestion.client_results import F1ResultsApiClient
from src.ingestion.storage import upload_file_to_minio


def load_results_for_round(season: int, round_number: int) -> None:
    api_base_url = get_f1_api_base_url()
    client = F1ResultsApiClient(api_base_url)

    data = client.get_results(season=season, round_number=round_number)

    timestamp = build_timestamp()
    file_path = build_results_raw_file_path(season, round_number, timestamp)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    _, _, _, raw_bucket_name, _, _ = get_minio_settings()

    object_key = build_results_raw_object_key(
        season=season,
        round_number=round_number,
        timestamp=timestamp,
        file_name=file_path.name,
    )

    upload_file_to_minio(file_path, raw_bucket_name, object_key)


def load_results_for_season(season: int) -> None:
    rounds_count = 24

    for round_number in range(1, rounds_count + 1):
        try:
            print(f"[RESULTS] season={season}, round={round_number}")
            load_results_for_round(season, round_number)
        except Exception as exc:
            print(f"[RESULTS] skip season={season}, round={round_number}: {exc}")