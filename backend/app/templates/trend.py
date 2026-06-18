def build_trend_query(plan: dict) -> str:
    """
    Generate SQL for a trend query.
    Uses parameterized values for start_time and end_time.
    """
    return f"""
        SELECT
            DATE_TRUNC('{plan["group_by"]}', {plan["time_column"]}) AS time_bucket,
            {plan["aggregation"]}({plan["value_column"]}) AS value
        FROM {plan["schema_name"]}.{plan["table_name"]}
        WHERE {plan["time_column"]} >= %(start_time)s
          AND {plan["time_column"]} < %(end_time)s
        GROUP BY time_bucket
        ORDER BY time_bucket
    """
