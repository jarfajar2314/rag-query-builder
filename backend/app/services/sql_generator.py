from app.templates.trend import build_trend_query
from app.templates.summary import build_summary_query
from app.templates.compare import build_compare_query
from app.templates.raw_table import build_raw_table_query
from app.templates.downtime import build_downtime_query

def generate_sql(plan: dict) -> str:
    """
    Generates SQL string based on the provided JSON query plan.
    Only predefined templates are allowed.
    """
    intent = plan.get("intent")
    
    if intent == "trend":
        return build_trend_query(plan)
    elif intent == "summary":
        return build_summary_query(plan)
    elif intent == "compare":
        return build_compare_query(plan)
    elif intent == "raw_table":
        return build_raw_table_query(plan)
    elif intent == "downtime":
        return build_downtime_query(plan)
        
    raise ValueError(f"Unsupported intent: {intent}")
