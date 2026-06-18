def build_summary_query(plan: dict) -> str:
    """
    Generate SQL for a summary query (e.g. total sales).
    """
    return f"""
        SELECT
            {plan["aggregation"]}({plan["value_column"]}) AS value
        FROM {plan["schema_name"]}.{plan["table_name"]}
        WHERE {plan.get("time_column", "1=1")} >= %(start_time)s
          AND {plan.get("time_column", "1=1")} < %(end_time)s
    """
