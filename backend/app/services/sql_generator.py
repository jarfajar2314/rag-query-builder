from typing import Any

from app.models.query_plan import QueryPlan
from app.templates.trend import build_trend_query
from app.templates.summary import build_summary_query
from app.templates.compare import build_compare_query
from app.templates.raw_table import build_raw_table_query
from app.templates.downtime import build_downtime_query
from app.services.downtime_plan_resolver import resolve_downtime_plan


def generate_sql(plan: QueryPlan) -> tuple[str, dict[str, Any]]:
    """
    Generates SQL string based on the provided JSON query plan.
    Only predefined templates are allowed.
    """
    if plan.intent == "trend":
        return build_trend_query(plan)

    if plan.intent == "summary":
        return build_summary_query(plan)

    if plan.intent == "compare":
        return build_compare_query(plan)

    if plan.intent == "raw_table":
        return build_raw_table_query(plan)

    if plan.intent == "downtime":
        resolved_plan = resolve_downtime_plan(plan)
        return build_downtime_query(resolved_plan)
        
    raise ValueError(f"Unsupported intent: {intent}")
