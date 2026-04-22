import csv
import json
from pathlib import Path

from src.common.config import get_minio_settings
from src.common.paths import STAGING_DIR, RAW_DIR, build_staging_object_key, build_timestamp
from src.ingestion.storage import upload_file_to_minio


def get_latest_results_raw_files_for_season(season: int) -> list[Path]:
    files = sorted(RAW_DIR.glob(f"results_{season}_*.json"))
    if not files:
        return []

    latest_by_round: dict[int, Path] = {}

    for file_path in files:
        parts = file_path.stem.split("_")
        if len(parts) < 4:
            continue

        try:
            round_number = int(parts[2])
        except ValueError:
            continue

        latest_by_round[round_number] = file_path

    return [latest_by_round[round_number] for round_number in sorted(latest_by_round.keys())]


def extract_result_records(raw_data: dict) -> list[dict]:
    races = raw_data["MRData"]["RaceTable"]["Races"]
    if not races:
        return []

    race = races[0]
    results = race.get("Results", [])

    normalized_rows = []

    for result in results:
        driver = result.get("Driver", {})
        constructor = result.get("Constructor", {})
        fastest_lap = result.get("FastestLap", {})
        avg_speed = fastest_lap.get("AverageSpeed", {})
        time_info = result.get("Time", {})

        row = {
            "season": race.get("season"),
            "round_number": race.get("round"),
            "race_name": race.get("raceName"),
            "driver_id": driver.get("driverId"),
            "constructor_id": constructor.get("constructorId"),
            "grid_position": result.get("grid"),
            "finish_position": result.get("position"),
            "position_text": result.get("positionText"),
            "position_order": result.get("positionOrder"),
            "points": result.get("points"),
            "laps": result.get("laps"),
            "status": result.get("status"),
            "time_millis": time_info.get("millis"),
            "time_text": time_info.get("time"),
            "fastest_lap_rank": fastest_lap.get("rank"),
            "fastest_lap_number": fastest_lap.get("lap"),
            "fastest_lap_time": fastest_lap.get("Time", {}).get("time"),
            "fastest_lap_avg_speed": avg_speed.get("speed"),
            "fastest_lap_avg_speed_unit": avg_speed.get("units"),
        }
        normalized_rows.append(row)

    return normalized_rows


def normalize_results_for_season(season: int) -> None:
    raw_files = get_latest_results_raw_files_for_season(season)
    if not raw_files:
        raise FileNotFoundError(f"Не найдены raw results для сезона {season}")

    all_rows = []

    for raw_file in raw_files:
        with open(raw_file, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        all_rows.extend(extract_result_records(raw_data))

    if not all_rows:
        raise ValueError(f"Нет данных results для сезона {season}")

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    output_path = STAGING_DIR / f"stg_race_results_{season}.csv"

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    _, _, _, _, staging_bucket_name, _ = get_minio_settings()
    timestamp = build_timestamp()

    object_key = build_staging_object_key(
        entity=f"race_results/{season}",
        timestamp=timestamp,
        file_name=output_path.name,
    )

    upload_file_to_minio(output_path, staging_bucket_name, object_key)

    print(f"[STAGING] results season={season}, rows={len(all_rows)}")