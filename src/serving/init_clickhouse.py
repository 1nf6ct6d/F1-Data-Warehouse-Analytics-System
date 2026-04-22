from pathlib import Path

from src.storage.clickhouse_client import get_clickhouse_client


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_FILE = PROJECT_ROOT / "sql" / "clickhouse" / "serving_tables.sql"


def main() -> None:
    client = get_clickhouse_client()

    with open(SQL_FILE, "r", encoding="utf-8") as file:
        sql_text = file.read()

    statements = [stmt.strip() for stmt in sql_text.split(";") if stmt.strip()]

    for statement in statements:
        client.command(statement)

    print("[CLICKHOUSE] Serving tables initialized")


if __name__ == "__main__":
    main()