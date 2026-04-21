from src.serving.api.db import get_connection


def fetch_driver_points(limit: int = 20) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            driver_id,
            given_name,
            family_name,
            nationality,
            total_points
        FROM vw_driver_points
        ORDER BY total_points DESC
        FETCH FIRST :1 ROWS ONLY
        """,
        [limit],
    )

    rows = cursor.fetchall()
    result = [
        {
            "driver_id": row[0],
            "given_name": row[1],
            "family_name": row[2],
            "nationality": row[3],
            "total_points": float(row[4]) if row[4] is not None else 0.0,
        }
        for row in rows
    ]

    cursor.close()
    connection.close()
    return result


def fetch_constructor_points(limit: int = 20) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            constructor_id,
            constructor_name,
            nationality,
            total_points
        FROM vw_constructor_points
        ORDER BY total_points DESC
        FETCH FIRST :1 ROWS ONLY
        """,
        [limit],
    )

    rows = cursor.fetchall()
    result = [
        {
            "constructor_id": row[0],
            "constructor_name": row[1],
            "nationality": row[2],
            "total_points": float(row[3]) if row[3] is not None else 0.0,
        }
        for row in rows
    ]

    cursor.close()
    connection.close()
    return result


def fetch_driver_podiums(limit: int = 20) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            driver_id,
            given_name,
            family_name,
            podiums
        FROM vw_driver_podiums
        ORDER BY podiums DESC
        FETCH FIRST :1 ROWS ONLY
        """,
        [limit],
    )

    rows = cursor.fetchall()
    result = [
        {
            "driver_id": row[0],
            "given_name": row[1],
            "family_name": row[2],
            "podiums": int(row[3]) if row[3] is not None else 0,
        }
        for row in rows
    ]

    cursor.close()
    connection.close()
    return result


def fetch_race_results(season: int, round_number: int) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            season,
            round_number,
            race_name,
            TO_CHAR(race_date, 'YYYY-MM-DD') AS race_date,
            driver_id,
            given_name,
            family_name,
            constructor_name,
            grid_position,
            finish_position,
            position_text,
            points,
            status,
            fastest_lap_time,
            fastest_lap_avg_speed
        FROM vw_race_results
        WHERE season = :1
          AND round_number = :2
        ORDER BY finish_position
        """,
        [season, round_number],
    )

    rows = cursor.fetchall()
    result = [
        {
            "season": int(row[0]),
            "round_number": int(row[1]),
            "race_name": row[2],
            "race_date": row[3],
            "driver_id": row[4],
            "given_name": row[5],
            "family_name": row[6],
            "constructor_name": row[7],
            "grid_position": int(row[8]) if row[8] is not None else None,
            "finish_position": int(row[9]) if row[9] is not None else None,
            "position_text": row[10],
            "points": float(row[11]) if row[11] is not None else None,
            "status": row[12],
            "fastest_lap_time": row[13],
            "fastest_lap_avg_speed": float(row[14]) if row[14] is not None else None,
        }
        for row in rows
    ]

    cursor.close()
    connection.close()
    return result