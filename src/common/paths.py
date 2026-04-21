from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"


def build_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def build_raw_file_path(entity: str, season: int, timestamp: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    file_name = f"{entity}_{season}_{timestamp}.json"
    return RAW_DIR / file_name


def build_raw_object_key(entity: str, season: int, timestamp: str, file_name: str) -> str:
    load_date_raw = timestamp[:8]
    load_date = f"{load_date_raw[:4]}-{load_date_raw[4:6]}-{load_date_raw[6:8]}"

    return (
        f"jolpica/{entity}/"
        f"season={season}/"
        f"load_date={load_date}/"
        f"{file_name}"
    )