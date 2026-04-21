from pathlib import Path

import pandas as pd

from src.dwh.oracle_client import get_oracle_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STAGING_DIR = PROJECT_ROOT / "data" / "staging"


def load_dim_race_for_season(season: int) -> None:
    file_path = STAGING_DIR / f"stg_races_{season}.csv"
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        rows.append(
            (
                int(row["season"]),
                int(row["round"]),
                row["race_name"],
                row["race_date"],
                row["race_time"] if pd.notna(row["race_time"]) else None,
                row["race_url"] if pd.notna(row["race_url"]) else None,
                row["circuit_id"] if pd.notna(row["circuit_id"]) else None,
                row["circuit_name"] if pd.notna(row["circuit_name"]) else None,
                row["locality"] if pd.notna(row["locality"]) else None,
                row["country"] if pd.notna(row["country"]) else None,
            )
        )

    connection = get_oracle_connection()
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO dim_race (
            season,
            round_number,
            race_name,
            race_date,
            race_time,
            race_url,
            circuit_id,
            circuit_name,
            locality,
            country
        )
        VALUES (
            :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, :7, :8, :9, :10
        )
        """,
        rows,
    )

    connection.commit()
    cursor.close()
    connection.close()

    print(f"[DWH] Загружено races season={season}: {len(rows)}")