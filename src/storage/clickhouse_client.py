import clickhouse_connect

from src.common.config import get_clickhouse_settings


def get_clickhouse_client():
    host, port, database, user, password = get_clickhouse_settings()

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        database=database,
        username=user,
        password=password,
    )
    return client