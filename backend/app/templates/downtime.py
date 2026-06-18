def build_downtime_query(plan: dict) -> str:
    """
    Generate SQL for a downtime query.
    """
    return f"""
        SELECT
            {plan["time_column"]} AS timestamp,
            {plan["status_column"]} AS status
        FROM {plan["schema_name"]}.{plan["table_name"]}
        WHERE {plan["time_column"]} >= %(start_time)s
          AND {plan["time_column"]} < %(end_time)s
          AND {plan["status_column"]} <> {plan.get("running_value", 1)}
        ORDER BY {plan["time_column"]}
    """
