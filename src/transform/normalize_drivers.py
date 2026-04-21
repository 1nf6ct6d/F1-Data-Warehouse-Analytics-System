import csv
import json
from pathlib import Path

from src.common.config import get_minio_settings
from src.common.paths import STAGING_DIR, RAW_DIR, build_staging_object_key, build_timestamp
from src.ingestion.storage import upload_file_to_minio


def get_latest_drivers_raw_file() -> Path:
    files = sorted(RAW_DIR.glob("drivers_*.json"))
    if not files:
        raise FileNotFoundError("В data/raw не найдено ни одного raw-файла для drivers")
    return files[-1]


def extract_driver_records(raw_data: dict) -> list[dict]:
    drivers = raw_data["MRData"]["DriverTable"]["Drivers"]

    normalized_rows = []

    for driver in drivers:
        row = {
            "driver_id": driver.get("driverId"),
            "permanent_number": driver.get("permanentNumber"),
            "code": driver.get("code"),
            "given_name": driver.get("givenName"),
            "family_name": driver.get("familyName"),
            "date_of_birth": driver.get("dateOfBirth"),
            "nationality": driver.get("nationality"),
            "driver_url": driver.get("url"),
        }
        normalized_rows.append(row)

    return normalized_rows


def save_to_csv(rows: list[dict], output_path: Path) -> None:
    if not rows:
        raise ValueError("Нет данных для записи в staging CSV")

    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    raw_file = get_latest_drivers_raw_file()

    with open(raw_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    rows = extract_driver_records(raw_data)

    output_path = STAGING_DIR / "stg_drivers.csv"
    save_to_csv(rows, output_path)

    _, _, _, _, staging_bucket_name, _ = get_minio_settings()
    timestamp = build_timestamp()

    object_key = build_staging_object_key(
        entity="drivers",
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