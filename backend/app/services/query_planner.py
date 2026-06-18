from datetime import datetime, timezone
from app.models.query_plan import QueryPlan

def detect_intent(prompt: str) -> str:
    text = prompt.lower()
    if any(word in text for word in ["trend", "over time", "per day", "daily", "monthly"]):
        return "trend"
    if any(word in text for word in ["compare", "by region", "by machine", "per machine", "per region"]):
        return "compare"
    if any(word in text for word in ["total", "average", "avg", "sum", "minimum", "maximum", "count"]):
        return "summary"
    if any(word in text for word in ["latest", "raw", "records", "table", "top"]):
        return "raw_table"
    if any(word in text for word in ["downtime", "not running", "stop", "stopped", "mati"]):
        return "downtime"
    return "trend"

def detect_aggregation(prompt: str) -> str:
    text = prompt.lower()
    if "average" in text or "avg" in text:
        return "avg"
    if "minimum" in text or "min" in text:
        return "min"
    if "maximum" in text or "max" in text:
        return "max"
    if "count" in text:
        return "count"
    return "sum"

def detect_group_by(prompt: str) -> str:
    text = prompt.lower()
    if "hour" in text or "hourly" in text:
        return "hour"
    if "month" in text or "monthly" in text:
        return "month"
    if "week" in text or "weekly" in text:
        return "week"
    if "year" in text or "yearly" in text:
        return "year"
    return "day"

def default_date_range() -> tuple[str, str]:
    """
    MVP default date range.
    For now, use June 2026 because the demo data is in June 2026.
    Later, replace this with real natural-language date parsing.
    """
    return "2026-06-01", "2026-07-01"

def choose_column(catalog_rows: list[dict], column_flag: str) -> str | None:
    for row in catalog_rows:
        if row.get(column_flag):
            return row["column_name"]
    return None

def choose_table_context(catalog_rows: list[dict]) -> dict:
    """
    For MVP, choose the first matched table context.
    Later, improve scoring.
    """
    if not catalog_rows:
        raise ValueError("No matching catalog metadata found.")
    first = catalog_rows[0]
    return {
        "data_source_id": first["data_source_id"],
        "database_type": first["database_type"],
        "schema_name": first["schema_name"],
        "table_name": first["table_name"],
    }

def build_query_plan_from_catalog(prompt: str, catalog_rows: list[dict]) -> QueryPlan:
    intent = detect_intent(prompt)
    aggregation = detect_aggregation(prompt)
    group_by = detect_group_by(prompt)
    start_time, end_time = default_date_range()

    table_context = choose_table_context(catalog_rows)
    time_column = choose_column(catalog_rows, "is_time_column")
    value_column = choose_column(catalog_rows, "is_value_column")
    category_column = choose_column(catalog_rows, "is_category_column")

    if intent == "trend":
        chart_type = "line"
    elif intent == "compare":
        chart_type = "bar"
    elif intent == "summary":
        chart_type = "kpi"
    elif intent == "raw_table":
        chart_type = "table"
    else:
        chart_type = "timeline"

    return QueryPlan(
        intent=intent,
        database_type=table_context["database_type"],
        data_source_id=table_context["data_source_id"],
        schema_name=table_context["schema_name"],
        table_name=table_context["table_name"],
        time_column=time_column,
        value_column=value_column,
        category_column=category_column,
        start_time=start_time,
        end_time=end_time,
        aggregation=aggregation,
        group_by=group_by,
        limit=100,
        chart_type=chart_type,
    )
