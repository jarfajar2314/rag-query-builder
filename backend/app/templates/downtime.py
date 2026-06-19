import re
from typing import Any

from app.services.downtime_plan_resolver import ResolvedDowntimePlan

IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")

def validate_identifier(value: str) -> str:
    if not IDENTIFIER_PATTERN.fullmatch(value):
        raise ValueError(f"Invalid SQL identifier: {value}")
    return value

def build_downtime_query(plan: ResolvedDowntimePlan) -> tuple[str, dict[str, Any]]:
    schema_name = validate_identifier(plan.schema_name)
    table_name = validate_identifier(plan.table_name)
    time_column = validate_identifier(plan.time_column)
    status_column = validate_identifier(plan.status_column)

    category_filter = ""
    if plan.category_column and plan.category_value is not None:
        cat_col = validate_identifier(plan.category_column)
        category_filter = f"AND {cat_col} = %(category_value)s"

    sql = f"""
WITH ordered AS (
    SELECT
        {time_column} AS ts,
        {status_column}::text AS status_value,
        LEAD({time_column}) OVER (
            ORDER BY {time_column}
        ) AS next_ts
    FROM {schema_name}.{table_name}
    WHERE {time_column} >= %(start_time)s
      AND {time_column} < %(end_time)s
      {category_filter}
),
classified AS (
    SELECT
        ts,
        status_value,
        next_ts,

        CASE
            WHEN status_value = ANY(%(downtime_values)s)
            THEN 1
            ELSE 0
        END AS is_down,

        CASE
            WHEN next_ts IS NULL THEN
                LEAST(
                    %(end_time)s::timestamptz,
                    ts + (%(expected_interval_seconds)s * INTERVAL '1 second')
                )

            WHEN EXTRACT(EPOCH FROM next_ts - ts) > %(gap_tolerance_seconds)s THEN
                ts + (%(expected_interval_seconds)s * INTERVAL '1 second')

            ELSE next_ts
        END AS row_end_time
    FROM ordered
),
marked AS (
    SELECT
        *,

        CASE
            WHEN LAG(is_down) OVER (ORDER BY ts) IS DISTINCT FROM is_down
            THEN 1

            WHEN LAG(ts) OVER (ORDER BY ts) IS NULL
            THEN 1

            WHEN EXTRACT(EPOCH FROM ts - LAG(ts) OVER (ORDER BY ts)) > %(gap_tolerance_seconds)s
            THEN 1

            ELSE 0
        END AS new_group
    FROM classified
),
islands AS (
    SELECT
        *,

        SUM(new_group) OVER (
            ORDER BY ts
        ) AS group_id
    FROM marked
),
downtime_intervals AS (
    SELECT
        MIN(ts) AS start_time,
        MAX(row_end_time) AS end_time,

        SUM(EXTRACT(EPOCH FROM row_end_time - ts))::BIGINT AS duration_seconds,

        COUNT(*) AS sample_count
    FROM islands
    WHERE is_down = 1
    GROUP BY group_id
)
SELECT
    start_time,
    end_time,
    duration_seconds,
    ROUND(duration_seconds / 60.0, 2) AS duration_minutes,
    sample_count
FROM downtime_intervals
WHERE duration_seconds >= %(minimum_duration_seconds)s
ORDER BY start_time;
    """

    params = {
        "start_time": plan.start_time,
        "end_time": plan.end_time,
        "downtime_values": plan.downtime_values,
        "expected_interval_seconds": plan.expected_interval_seconds,
        "gap_tolerance_seconds": plan.gap_tolerance_seconds,
        "minimum_duration_seconds": plan.minimum_duration_seconds,
    }

    if plan.category_column and plan.category_value is not None:
        params["category_value"] = plan.category_value

    return sql, params
