import json
from typing import Any
from pydantic import BaseModel

from app.models.query_plan import QueryPlan
from app.db.postgres import get_postgres_connection
from app.services.status_rule_service import get_status_rule

class ResolvedDowntimePlan(BaseModel):
    data_source_id: int
    database_type: str

    schema_name: str
    table_name: str

    time_column: str
    status_column: str

    category_column: str | None = None
    category_value: Any | None = None

    downtime_values: list[str]

    expected_interval_seconds: int
    gap_tolerance_seconds: int
    minimum_duration_seconds: int

    start_time: str
    end_time: str

def resolve_downtime_plan(plan: QueryPlan) -> ResolvedDowntimePlan:
    if not plan.status_rule_id:
        raise ValueError("downtime intent requires status_rule_id")

    rule = get_status_rule(plan.status_rule_id)
    if not rule["is_active"]:
        raise ValueError("Status rule is not active")

    # Load column info from data_catalog
    col_ids = [rule["status_column_catalog_id"], rule["time_column_catalog_id"]]
    if rule["category_column_catalog_id"] is not None:
        col_ids.append(rule["category_column_catalog_id"])

    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            format_strings = ','.join(['%s'] * len(col_ids))
            cur.execute(f"""
                SELECT id, data_source_id, schema_name, table_name, column_name
                FROM data_catalog
                WHERE id IN ({format_strings})
            """, tuple(col_ids))
            cols = {row["id"]: row for row in cur.fetchall()}

    if len(cols) != len(col_ids):
        raise ValueError("One or more rule columns are missing from data_catalog")

    status_col_info = cols[rule["status_column_catalog_id"]]
    time_col_info = cols[rule["time_column_catalog_id"]]
    
    # Confirm they belong to the same table
    if (status_col_info["data_source_id"] != time_col_info["data_source_id"] or
        status_col_info["schema_name"] != time_col_info["schema_name"] or
        status_col_info["table_name"] != time_col_info["table_name"]):
        raise ValueError("Rule columns span multiple tables")

    category_column_name = None
    if rule["category_column_catalog_id"]:
        cat_col_info = cols[rule["category_column_catalog_id"]]
        if (cat_col_info["data_source_id"] != status_col_info["data_source_id"] or
            cat_col_info["table_name"] != status_col_info["table_name"]):
            raise ValueError("Category column spans multiple tables")
        category_column_name = cat_col_info["column_name"]

    # Minimum duration (override from user if provided)
    min_duration = rule["minimum_downtime_seconds"]
    if plan.minimum_duration_seconds is not None:
        min_duration = plan.minimum_duration_seconds

    # Stringify downtime values for SQL comparison
    downtime_vals = json.loads(rule["downtime_values"]) if isinstance(rule["downtime_values"], str) else rule["downtime_values"]
    downtime_vals_str = [str(v) for v in downtime_vals]

    return ResolvedDowntimePlan(
        data_source_id=status_col_info["data_source_id"],
        database_type="postgresql", # Default for MVP
        schema_name=status_col_info["schema_name"],
        table_name=status_col_info["table_name"],
        time_column=time_col_info["column_name"],
        status_column=status_col_info["column_name"],
        category_column=category_column_name,
        category_value=plan.category_value,
        downtime_values=downtime_vals_str,
        expected_interval_seconds=rule["expected_interval_seconds"],
        gap_tolerance_seconds=rule["gap_tolerance_seconds"],
        minimum_duration_seconds=min_duration,
        start_time=plan.start_time,
        end_time=plan.end_time
    )
