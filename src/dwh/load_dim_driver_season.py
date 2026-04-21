from pathlib import Path

import pandas as pd

from src.dwh.oracle_client import get_oracle_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STAGING_DIR = PROJECT_ROOT / "data" / "staging"


def load_dim_driver_for_season(season: int) -> None:
    file_path = STAGING_DIR / f"stg_drivers_{season}.csv"
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        rows.append(
            (
                row["driver_id"],
                row["permanent_number"] if pd.notna(row["permanent_number"]) else None,
                row["code"] if pd.notna(row["code"]) else None,
                row["given_name"],
                row["family_name"],
                row["date_of_birth"],
                row["nationality"] if pd.notna(row["nationality"]) else None,
                row["driver_url"] if pd.notna(row["driver_url"]) else None,
            )
        )

    connection = get_oracle_connection()
    cursor = connection.cursor()

    for row in rows:
        cursor.execute(
            """
            MERGE INTO dim_driver d
            USING (
                SELECT
                    :1 AS driver_id,
                    :2 AS permanent_number,
                    :3 AS code,
                    :4 AS given_name,
                    :5 AS family_name,
                    :6 AS date_of_birth,
                    :7 AS nationality,
                    :8 AS driver_url
                FROM dual
            ) src
            ON (d.driver_id = src.driver_id)
            WHEN NOT MATCHED THEN
                INSERT (
                    driver_id,
                    permanent_number,
                    code,
                    given_name,
                    family_name,
                    date_of_birth,
                    nationality,
                    driver_url
                )
                VALUES (
                    src.driver_id,
                    src.permanent_number,
                    src.code,
                    src.given_name,
                    src.family_name,
                    TO_DATE(src.date_of_birth, 'YYYY-MM-DD'),
                    src.nationality,
                    src.driver_url
                )
            """,
            row,
        )

    connection.commit()
    cursor.close()
    connection.close()

    print(f"[DWH] Загружено/смёржено drivers season={season}: {len(rows)}")