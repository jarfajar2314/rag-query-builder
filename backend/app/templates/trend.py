from app.models.query_plan import QueryPlan

def build_trend_query(plan: QueryPlan) -> tuple[str, dict]:
    """
    Generate SQL for a trend query.
    Uses parameterized values for start_time and end_time.
    """
    if not plan.time_column:
        raise ValueError("time_column is required for trend queries")
        
    where_clause = ""
    params = {}
    
    if plan.start_time and plan.end_time:
        where_clause = f"WHERE {plan.time_column} >= %(start_time)s AND {plan.time_column} < %(end_time)s"
        params["start_time"] = plan.start_time
        params["end_time"] = plan.end_time

    sql = f"""
        SELECT
            DATE_TRUNC('{plan.group_by}', {plan.time_column}) AS time_bucket,
            {plan.aggregation.upper()}({plan.value_column}) AS value
        FROM {plan.schema_name}.{plan.table_name}
        {where_clause}
        GROUP BY time_bucket
        ORDER BY time_bucket
    """
    return sql, params
