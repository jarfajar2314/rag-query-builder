def build_compare_query(plan: dict) -> str:
    """
    Generate SQL for a comparison query (e.g. sales by region).
    """
    return f"""
        SELECT
            {plan["category_column"]} AS category,
            {plan["aggregation"]}({plan["value_column"]}) AS value
        FROM {plan["schema_name"]}.{plan["table_name"]}
        WHERE {plan.get("time_column", "1=1")} >= %(start_time)s
          AND {plan.get("time_column", "1=1")} < %(end_time)s
        GROUP BY {plan["category_column"]}
        ORDER BY value DESC
    """
