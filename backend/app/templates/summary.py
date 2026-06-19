from app.models.query_plan import QueryPlan

def build_summary_query(plan: QueryPlan) -> tuple[str, dict]:
    conditions = []
    params = {}

    # Time filter
    if plan.time_column and plan.start_time and plan.end_time:
        conditions.append(f"{plan.time_column} >= %(start_time)s AND {plan.time_column} < %(end_time)s")
        params["start_time"] = plan.start_time
        params["end_time"] = plan.end_time

    # Category filter
    if plan.category_column and plan.category_value:
        conditions.append(f"{plan.category_column} = %(category_value)s")
        params["category_value"] = plan.category_value

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    sql = f"""
        SELECT
            {plan.aggregation.upper()}({plan.value_column}) AS value
        FROM {plan.schema_name}.{plan.table_name}
        {where_clause}
    """

    return sql, params
