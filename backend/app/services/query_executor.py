from typing import Any
from app.db.postgres import PostgresConnector
from app.db.sqlserver import SqlServerConnector
from app.services.sql_validator import validate_sql

def execute_plan_sql(sql: str, params: dict[str, Any], plan: dict[str, Any] = None) -> list[dict[str, Any]]:
    """
    Validates and executes SQL query using parameterized values and the correct DB adapter.
    """
    validate_sql(sql)
    
    db_type = plan.get("database_type", "postgresql") if plan else "postgresql"
    
    if db_type == "postgresql":
        connector = PostgresConnector()
    elif db_type == "sqlserver":
        connector = SqlServerConnector()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
        
    return connector.execute_query(sql, params)
