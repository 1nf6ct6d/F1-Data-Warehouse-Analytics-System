from pathlib import Path

from src.common.paths import DATA_DIR, build_load_date_from_timestamp


RAW_DIR = DATA_DIR / "raw"


def build_results_raw_file_path(season: int, round_number: int, timestamp: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    file_name = f"results_{season}_{round_number}_{timestamp}.json"
    return RAW_DIR / file_name


def build_results_raw_object_key(
    season: int,
    round_number: int,
    timestamp: str,
    file_name: str,
) -> str:
    load_date = build_load_date_from_timestamp(timestamp)

    return (
        f"jolpica/results/"
        f"season={season}/"
        f"round={round_number}/"
        f"load_date={load_date}/"
        f"{file_name}"
    )