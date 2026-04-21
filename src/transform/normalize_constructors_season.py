import csv
import json
from pathlib import Path

from src.common.config import get_minio_settings
from src.common.paths import STAGING_DIR, RAW_DIR, build_staging_object_key, build_timestamp
from src.ingestion.storage import upload_file_to_minio


def get_latest_constructors_raw_file_for_season(season: int) -> Path:
    files = sorted(RAW_DIR.glob(f"constructors_{season}_*.json"))
    if not files:
        raise FileNotFoundError(f"В data/raw не найдено ни одного raw-файла для constructors сезона {season}")
    return files[-1]


def extract_constructor_records(raw_data: dict) -> list[dict]:
    constructors = raw_data["MRData"]["ConstructorTable"]["Constructors"]

    normalized_rows = []

    for constructor in constructors:
        row = {
            "constructor_id": constructor.get("constructorId"),
            "constructor_name": constructor.get("name"),
            "nationality": constructor.get("nationality"),
            "constructor_url": constructor.get("url"),
        }
        normalized_rows.append(row)

    return normalized_rows


def normalize_constructors_for_season(season: int) -> None:
    raw_file = get_latest_constructors_raw_file_for_season(season)

    with open(raw_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    rows = extract_constructor_records(raw_data)
    if not rows:
        raise ValueError(f"Нет данных constructors для сезона {season}")

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    output_path = STAGING_DIR / f"stg_constructors_{season}.csv"

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    _, _, _, _, staging_bucket_name, _ = get_minio_settings()
    timestamp = build_timestamp()

    object_key = build_staging_object_key(
        entity=f"constructors/{season}",
        timestamp=timestamp,
        file_name=output_path.name,
    )

    upload_file_to_minio(output_path, staging_bucket_name, object_key)

    print(f"[STAGING] constructors season={season}, rows={len(rows)}")