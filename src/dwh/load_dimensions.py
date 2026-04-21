from pathlib import Path

import pandas as pd

from src.dwh.oracle_client import get_oracle_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STAGING_DIR = PROJECT_ROOT / "data" / "staging"


def load_dim_driver(connection) -> None:
    file_path = STAGING_DIR / "stg_drivers.csv"
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

    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO dim_driver (
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
            :1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD'), :7, :8
        )
        """,
        rows,
    )
    connection.commit()
    cursor.close()

    print(f"[DWH] Загружено drivers: {len(rows)}")


def load_dim_constructor(connection) -> None:
    file_path = STAGING_DIR / "stg_constructors.csv"
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

    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO dim_constructor (
            constructor_id,
            constructor_name,
            nationality,
            constructor_url
        )
        VALUES (
            :1, :2, :3, :4
        )
        """,
        rows,
    )
    connection.commit()
    cursor.close()

    print(f"[DWH] Загружено constructors: {len(rows)}")


def load_dim_race(connection) -> None:
    file_path = STAGING_DIR / "stg_races.csv"
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        race_time = row["race_time"] if pd.notna(row["race_time"]) else None

        rows.append(
            (
                int(row["season"]),
                int(row["round"]),
                row["race_name"],
                row["race_date"],
                race_time,
                row["race_url"] if pd.notna(row["race_url"]) else None,
                row["circuit_id"] if pd.notna(row["circuit_id"]) else None,
                row["circuit_name"] if pd.notna(row["circuit_name"]) else None,
                row["locality"] if pd.notna(row["locality"]) else None,
                row["country"] if pd.notna(row["country"]) else None,
            )
        )

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

    print(f"[DWH] Загружено races: {len(rows)}")


def main() -> None:
    connection = get_oracle_connection()

    load_dim_driver(connection)
    load_dim_constructor(connection)
    load_dim_race(connection)

    connection.close()
    print("[DWH] Загрузка dimension tables завершена")


if __name__ == "__main__":
    main()