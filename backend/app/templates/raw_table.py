from app.models.query_plan import QueryPlan

def build_raw_table_query(plan: QueryPlan) -> tuple[str, dict]:
    where_clause = ""
    params = {"limit": plan.limit or 100}

    if plan.time_column and plan.start_time and plan.end_time:
        where_clause = f"WHERE {plan.time_column} >= %(start_time)s AND {plan.time_column} < %(end_time)s"
        params["start_time"] = plan.start_time
        params["end_time"] = plan.end_time
        
    order_clause = f"ORDER BY {plan.time_column} DESC" if plan.time_column else ""

    sql = f"""
        SELECT *
        FROM {plan.schema_name}.{plan.table_name}
        {where_clause}
        {order_clause}
        LIMIT %(limit)s
    """

    return sql, params
