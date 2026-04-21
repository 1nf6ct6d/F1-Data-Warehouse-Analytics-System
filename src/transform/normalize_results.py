import csv
import json
from pathlib import Path

from src.common.config import get_minio_settings
from src.common.paths import STAGING_DIR, RAW_DIR, build_staging_object_key, build_timestamp
from src.ingestion.storage import upload_file_to_minio


def get_latest_results_raw_file() -> Path:
    files = sorted(RAW_DIR.glob("results_*.json"))
    if not files:
        raise FileNotFoundError("В data/raw не найдено ни одного raw-файла для results")
    return files[-1]


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


def save_to_csv(rows: list[dict], output_path: Path) -> None:
    if not rows:
        raise ValueError("Нет данных для записи в stg_race_results.csv")

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    raw_file = get_latest_results_raw_file()

    with open(raw_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    rows = extract_result_records(raw_data)

    output_path = STAGING_DIR / "stg_race_results.csv"
    save_to_csv(rows, output_path)

    _, _, _, _, staging_bucket_name, _ = get_minio_settings()
    timestamp = build_timestamp()

    object_key = build_staging_object_key(
        entity="race_results",
        timestamp=timestamp,
        file_name=output_path.name,
    )

    upload_file_to_minio(output_path, staging_bucket_name, object_key)

    print(f"[RAW] Использован raw-файл: {raw_file}")
    print(f"[STAGING] Создан staging-файл: {output_path}")
    print(f"[STAGING] Количество записей: {len(rows)}")
    print(f"[MINIO] Bucket: {staging_bucket_name}")
    print(f"[MINIO] Object key: {object_key}")


if __name__ == "__main__":
    main()