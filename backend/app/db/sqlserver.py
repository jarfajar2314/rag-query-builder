from typing import Any
from app.db.base import DatabaseConnector

class SqlServerConnector(DatabaseConnector):
    def execute_query(self, sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Execute a SELECT query on SQL Server.
        Not fully implemented yet. Replace with pyodbc connection.
        """
        raise NotImplementedError("SQL Server connection not configured yet.")
