from pathlib import Path

import pandas as pd

from src.dwh.oracle_client import get_oracle_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STAGING_DIR = PROJECT_ROOT / "data" / "staging"


def load_fact_for_season(season: int) -> None:
    file_path = STAGING_DIR / f"stg_race_results_{season}.csv"
    df = pd.read_csv(file_path)

    connection = get_oracle_connection()
    cursor = connection.cursor()
    rows = []

    def to_int_or_none(value):
        return int(value) if pd.notna(value) else None

    def to_float_or_none(value):
        return float(value) if pd.notna(value) else None

    for _, row in df.iterrows():
        cursor.execute(
            """
            SELECT race_sk
            FROM dim_race
            WHERE season = :1
              AND round_number = :2
            """,
            [int(row["season"]), int(row["round_number"])],
        )
        race_result = cursor.fetchone()
        if race_result is None:
            raise ValueError(
                f"Не найден race_sk для season={row['season']}, round_number={row['round_number']}"
            )
        race_sk = race_result[0]

        cursor.execute(
            "SELECT driver_sk FROM dim_driver WHERE driver_id = :1",
            [row["driver_id"]],
        )
        driver_result = cursor.fetchone()
        if driver_result is None:
            raise ValueError(f"Не найден driver_sk для driver_id={row['driver_id']}")
        driver_sk = driver_result[0]

        cursor.execute(
            "SELECT constructor_sk FROM dim_constructor WHERE constructor_id = :1",
            [row["constructor_id"]],
        )
        constructor_result = cursor.fetchone()
        if constructor_result is None:
            raise ValueError(
                f"Не найден constructor_sk для constructor_id={row['constructor_id']}"
            )
        constructor_sk = constructor_result[0]

        rows.append(
            (
                race_sk,
                driver_sk,
                constructor_sk,
                to_int_or_none(row["grid_position"]),
                to_int_or_none(row["finish_position"]),
                row["position_text"] if pd.notna(row["position_text"]) else None,
                to_int_or_none(row["position_order"]),
                to_float_or_none(row["points"]),
                to_int_or_none(row["laps"]),
                row["status"] if pd.notna(row["status"]) else None,
                to_int_or_none(row["time_millis"]),
                row["time_text"] if pd.notna(row["time_text"]) else None,
                to_int_or_none(row["fastest_lap_rank"]),
                to_int_or_none(row["fastest_lap_number"]),
                row["fastest_lap_time"] if pd.notna(row["fastest_lap_time"]) else None,
                to_float_or_none(row["fastest_lap_avg_speed"]),
                row["fastest_lap_avg_speed_unit"] if pd.notna(row["fastest_lap_avg_speed_unit"]) else None,
            )
        )

    cursor.executemany(
        """
        INSERT INTO fact_race_result (
            race_sk,
            driver_sk,
            constructor_sk,
            grid_position,
            finish_position,
            position_text,
            position_order,
            points,
            laps,
            status,
            time_millis,
            time_text,
            fastest_lap_rank,
            fastest_lap_number,
            fastest_lap_time,
            fastest_lap_avg_speed,
            fastest_lap_avg_speed_unit
        )
        VALUES (
            :1, :2, :3, :4, :5, :6, :7, :8, :9,
            :10, :11, :12, :13, :14, :15, :16, :17
        )
        """,
        rows,
    )

    connection.commit()
    cursor.close()
    connection.close()

    print(f"[DWH] Загружен fact season={season}, rows={len(rows)}")