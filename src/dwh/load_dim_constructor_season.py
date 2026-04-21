from pathlib import Path

import pandas as pd

from src.dwh.oracle_client import get_oracle_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STAGING_DIR = PROJECT_ROOT / "data" / "staging"


def load_dim_constructor_for_season(season: int) -> None:
    file_path = STAGING_DIR / f"stg_constructors_{season}.csv"
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        rows.append(
            (
                row["constructor_id"],
                row["constructor_name"],
                row["nationality"] if pd.notna(row["nationality"]) else None,
                row["constructor_url"] if pd.notna(row["constructor_url"]) else None,
            )
        )

    connection = get_oracle_connection()
    cursor = connection.cursor()

    for row in rows:
        cursor.execute(
            """
            MERGE INTO dim_constructor c
            USING (
                SELECT
                    :1 AS constructor_id,
                    :2 AS constructor_name,
                    :3 AS nationality,
                    :4 AS constructor_url
                FROM dual
            ) src
            ON (c.constructor_id = src.constructor_id)
            WHEN NOT MATCHED THEN
                INSERT (
                    constructor_id,
                    constructor_name,
                    nationality,
                    constructor_url
                )
                VALUES (
                    src.constructor_id,
                    src.constructor_name,
                    src.nationality,
                    src.constructor_url
                )
            """,
            row,
        )

    connection.commit()
    cursor.close()
    connection.close()

    print(f"[DWH] Загружено/смёржено constructors season={season}: {len(rows)}")