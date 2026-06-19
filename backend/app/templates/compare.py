from app.models.query_plan import QueryPlan

def build_compare_query(plan: QueryPlan) -> tuple[str, dict]:
    where_clause = ""
    params = {}

    if plan.time_column and plan.start_time and plan.end_time:
        where_clause = f"WHERE {plan.time_column} >= %(start_time)s AND {plan.time_column} < %(end_time)s"
        params["start_time"] = plan.start_time
        params["end_time"] = plan.end_time

    sql = f"""
        SELECT
            {plan.category_column} AS category,
            {plan.aggregation.upper()}({plan.value_column}) AS value
        FROM {plan.schema_name}.{plan.table_name}
        {where_clause}
        GROUP BY {plan.category_column}
        ORDER BY value DESC
    """

    return sql, params
