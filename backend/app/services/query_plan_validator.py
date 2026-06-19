from app.models.query_plan import QueryPlan

class QueryPlanValidationError(Exception):
    pass

def validate_plan_against_catalog(
    plan: QueryPlan,
    catalog_rows: list[dict]
) -> None:
    """
    Validate the query plan against retrieved catalog rows.
    """
    if plan.start_time and plan.end_time:
        if plan.start_time >= plan.end_time:
            raise QueryPlanValidationError("start_time must be strictly less than end_time.")
    if plan.intent == "unknown":
        raise QueryPlanValidationError(
            "The request cannot be answered from the available catalog metadata."
        )

    if plan.data_source_id is None:
        raise QueryPlanValidationError("Missing data_source_id.")

    if not plan.schema_name:
        raise QueryPlanValidationError("Missing schema_name.")

    if not plan.table_name:
        raise QueryPlanValidationError("Missing table_name.")

    matching_rows = [
        row for row in catalog_rows
        if row["data_source_id"] == plan.data_source_id
        and row["schema_name"] == plan.schema_name
        and row["table_name"] == plan.table_name
    ]

    if not matching_rows:
        raise QueryPlanValidationError(
            "Selected table is not available in catalog context."
        )

    available_columns = {
        row["column_name"]
        for row in matching_rows
    }

    selected_columns = [
        plan.time_column,
        plan.value_column,
        plan.category_column,
        plan.status_column,
    ]

    for column in selected_columns:
        if column and column not in available_columns:
            raise QueryPlanValidationError(
                f"Column '{column}' is not available in catalog context."
            )

    if plan.intent == "trend":
        if not plan.time_column:
            raise QueryPlanValidationError("Trend intent requires time_column.")
        if not plan.value_column:
            raise QueryPlanValidationError("Trend intent requires value_column.")
        if plan.chart_type != "line":
            raise QueryPlanValidationError("Trend intent requires line chart.")

    if plan.intent == "compare":
        if not plan.value_column:
            raise QueryPlanValidationError("Compare intent requires value_column.")
        if not plan.category_column:
            raise QueryPlanValidationError("Compare intent requires category_column.")
        if plan.chart_type != "bar":
            raise QueryPlanValidationError("Compare intent requires bar chart.")

    if plan.intent == "summary":
        if not plan.value_column:
            raise QueryPlanValidationError("Summary intent requires value_column.")
        if plan.chart_type != "kpi":
            raise QueryPlanValidationError("Summary intent requires kpi chart.")

    if plan.intent == "raw_table":
        if plan.limit is None or plan.limit <= 0:
            raise QueryPlanValidationError("Raw table intent requires positive limit.")
        if plan.chart_type != "table":
            raise QueryPlanValidationError("Raw table intent requires table chart.")

    if plan.intent == "downtime":
        if not plan.time_column:
            raise QueryPlanValidationError("Downtime intent requires time_column.")
        if not plan.status_column:
            raise QueryPlanValidationError("Downtime intent requires status_column.")
        if plan.chart_type != "timeline":
            raise QueryPlanValidationError("Downtime intent requires timeline chart.")
