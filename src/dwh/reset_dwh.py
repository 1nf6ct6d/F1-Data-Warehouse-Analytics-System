from pathlib import Path

from src.dwh.oracle_client import get_oracle_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = PROJECT_ROOT / "sql" / "oracle"


def main() -> None:
    sql_file = SQL_DIR / "truncate_dwh.sql"

    with open(sql_file, "r", encoding="utf-8") as file:
        sql_text = file.read()

    statements = [stmt.strip() for stmt in sql_text.split(";") if stmt.strip()]

    connection = get_oracle_connection()
    cursor = connection.cursor()

    for statement in statements:
        cursor.execute(statement)

    connection.commit()
    cursor.close()
    connection.close()

    print("[DWH] Таблицы очищены")


if __name__ == "__main__":
    main()