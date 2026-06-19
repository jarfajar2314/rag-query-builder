import re

BLOCKED_KEYWORDS = [
    "insert", "update", "delete", "drop", "alter", "truncate",
    "create", "grant", "revoke", "exec", "execute", "call"
]

def validate_sql(sql: str) -> bool:
    """
    Validates SQL string to ensure it is safe to run.
    Blocks any DML, DDL, or multiple statements.
    """
    sql_lower = sql.lower()
    sql_strip = sql_lower.strip()
    
    if not (sql_strip.startswith("select") or sql_strip.startswith("with")):
        raise ValueError("Only SELECT or WITH queries are allowed")
        
    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_lower):
            raise ValueError(f"Blocked SQL keyword detected: {keyword}")
            
    if ";" in sql_strip.rstrip(";"):
        raise ValueError("Multiple statements not allowed")
        
    # Later add table/column metadata checks and date range checks here
    
    return True
