from typing import Any, Protocol

class DatabaseConnector(Protocol):
    def execute_query(self, sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Execute a query and return a list of dictionaries."""
        ...
