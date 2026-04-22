from src.dwh.oracle_client import get_oracle_connection
from src.storage.clickhouse_client import get_clickhouse_client


def fetch_driver_points_from_oracle() -> list[tuple]:
    connection = get_oracle_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            driver_id,
            given_name,
            family_name,
            NVL(nationality, ''),
            total_points
        FROM vw_driver_points
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows


def fetch_constructor_points_from_oracle() -> list[tuple]:
    connection = get_oracle_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            constructor_id,
            constructor_name,
            NVL(nationality, ''),
            total_points
        FROM vw_constructor_points
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows


def load_driver_points_to_clickhouse() -> None:
    client = get_clickhouse_client()
    rows = fetch_driver_points_from_oracle()

    client.command("TRUNCATE TABLE srv_driver_points")

    client.insert(
        "srv_driver_points",
        rows,
        column_names=[
            "driver_id",
            "given_name",
            "family_name",
            "nationality",
            "total_points",
        ],
    )

    print(f"[CLICKHOUSE] Загружено driver_points: {len(rows)}")


def load_constructor_points_to_clickhouse() -> None:
    client = get_clickhouse_client()
    rows = fetch_constructor_points_from_oracle()

    client.command("TRUNCATE TABLE srv_constructor_points")

    client.insert(
        "srv_constructor_points",
        rows,
        column_names=[
            "constructor_id",
            "constructor_name",
            "nationality",
            "total_points",
        ],
    )

    print(f"[CLICKHOUSE] Загружено constructor_points: {len(rows)}")


def main() -> None:
    load_driver_points_to_clickhouse()
    load_constructor_points_to_clickhouse()
    print("[CLICKHOUSE] Serving tables обновлены")


if __name__ == "__main__":
    main()