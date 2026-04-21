import oracledb

from src.common.config import get_oracle_settings


def get_connection():
    host, port, service_name, user, password = get_oracle_settings()
    dsn = f"{host}:{port}/{service_name}"

    connection = oracledb.connect(
        user=user,
        password=password,
        dsn=dsn,
    )
    return connection