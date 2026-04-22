from src.storage.clickhouse_client import get_clickhouse_client


def fetch_driver_points_from_clickhouse(limit: int = 20) -> list[dict]:
    client = get_clickhouse_client()

    query = f"""
    SELECT
        driver_id,
        given_name,
        family_name,
        nationality,
        total_points
    FROM srv_driver_points
    ORDER BY total_points DESC
    LIMIT {limit}
    """

    rows = client.query(query).result_rows

    return [
        {
            "driver_id": row[0],
            "given_name": row[1],
            "family_name": row[2],
            "nationality": row[3] if row[3] != "" else None,
            "total_points": float(row[4]),
        }
        for row in rows
    ]


def fetch_constructor_points_from_clickhouse(limit: int = 20) -> list[dict]:
    client = get_clickhouse_client()

    query = f"""
    SELECT
        constructor_id,
        constructor_name,
        nationality,
        total_points
    FROM srv_constructor_points
    ORDER BY total_points DESC
    LIMIT {limit}
    """

    rows = client.query(query).result_rows

    return [
        {
            "constructor_id": row[0],
            "constructor_name": row[1],
            "nationality": row[2] if row[2] != "" else None,
            "total_points": float(row[3]),
        }
        for row in rows
    ]