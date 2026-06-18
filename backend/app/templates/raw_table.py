def build_raw_table_query(plan: dict) -> str:
    """
    Generate SQL for a raw table query.
    Must include LIMIT to prevent pulling too much data.
    """
    limit = plan.get("limit", 100)
    
    return f"""
        SELECT *
        FROM {plan["schema_name"]}.{plan["table_name"]}
        WHERE {plan.get("time_column", "1=1")} >= %(start_time)s
          AND {plan.get("time_column", "1=1")} < %(end_time)s
        ORDER BY {plan.get("time_column", "id")} DESC
        LIMIT {limit}
    """
