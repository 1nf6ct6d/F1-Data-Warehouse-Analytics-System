import csv
import json
from pathlib import Path

from src.common.config import get_minio_settings
from src.common.paths import STAGING_DIR, RAW_DIR, build_staging_object_key, build_timestamp
from src.ingestion.storage import upload_file_to_minio


def get_latest_races_raw_file_for_season(season: int) -> Path:
    files = sorted(RAW_DIR.glob(f"races_{season}_*.json"))
    if not files:
        raise FileNotFoundError(f"В data/raw не найдено ни одного raw-файла для races сезона {season}")
    return files[-1]


def extract_race_records(raw_data: dict) -> list[dict]:
    races = raw_data["MRData"]["RaceTable"]["Races"]

    normalized_rows = []

    for race in races:
        circuit = race.get("Circuit", {})
        location = circuit.get("Location", {})

        row = {
            "season": race.get("season"),
            "round": race.get("round"),
            "race_name": race.get("raceName"),
            "race_date": race.get("date"),
            "race_time": race.get("time"),
            "race_url": race.get("url"),
            "circuit_id": circuit.get("circuitId"),
            "circuit_name": circuit.get("circuitName"),
            "locality": location.get("locality"),
            "country": location.get("country"),
        }

        normalized_rows.append(row)

    return normalized_rows


def normalize_races_for_season(season: int) -> None:
    raw_file = get_latest_races_raw_file_for_season(season)

    with open(raw_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    rows = extract_race_records(raw_data)
    if not rows:
        raise ValueError(f"Нет данных races для сезона {season}")

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    output_path = STAGING_DIR / f"stg_races_{season}.csv"

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    _, _, _, _, staging_bucket_name, _ = get_minio_settings()
    timestamp = build_timestamp()

    object_key = build_staging_object_key(
        entity=f"races/{season}",
        timestamp=timestamp,
        file_name=output_path.name,
    )

    upload_file_to_minio(output_path, staging_bucket_name, object_key)

    print(f"[STAGING] races season={season}, rows={len(rows)}")
    print(f"[MINIO] Bucket: {staging_bucket_name}")
    print(f"[MINIO] Object key: {object_key}")