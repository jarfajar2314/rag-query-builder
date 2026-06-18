from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.config import settings


def get_postgres_connection():
    """
    Create a PostgreSQL connection.

    For MVP, this uses the configured PostgreSQL user.
    Later, query execution should use a read-only database user.
    """
    return psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        row_factory=dict_row,
    )


from app.db.base import DatabaseConnector

class PostgresConnector(DatabaseConnector):
    def execute_query(self, sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Execute a SELECT query and return rows as dictionaries.
        """
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or {})
                rows = cur.fetchall()
                return list(rows)

def execute_select_query(sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    # Backwards compatibility if needed, or use PostgresConnector directly
    return PostgresConnector().execute_query(sql, params)


def test_postgres_connection() -> bool:
    """
    Test PostgreSQL connection.
    """
    rows = execute_select_query("SELECT 1 AS ok")
    return rows[0]["ok"] == 1