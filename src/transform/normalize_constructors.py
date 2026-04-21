import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
STAGING_DIR = PROJECT_ROOT / "data" / "staging"


def get_latest_constructors_raw_file() -> Path:
    files = sorted(RAW_DIR.glob("constructors_*.json"))
    if not files:
        raise FileNotFoundError("В data/raw не найдено ни одного raw-файла для constructors")
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
    raw_file = get_latest_constructors_raw_file()

    with open(raw_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    rows = extract_constructor_records(raw_data)

    output_path = STAGING_DIR / "stg_constructors.csv"
    save_to_csv(rows, output_path)

    print(f"[RAW] Использован raw-файл: {raw_file}")
    print(f"[STAGING] Создан staging-файл: {output_path}")
    print(f"[STAGING] Количество записей: {len(rows)}")


if __name__ == "__main__":
    main()