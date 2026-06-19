import json
from datetime import datetime
from openai import OpenAI

from app.config import settings
from app.models.query_plan import QueryPlan

client = OpenAI(api_key=settings.openai_api_key)

QUERY_PLAN_SCHEMA = {
    "name": "query_plan",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "intent": {
                "type": "string",
                "enum": [
                    "trend",
                    "summary",
                    "compare",
                    "raw_table",
                    "downtime",
                    "unknown"
                ]
            },
            "database_type": {
                "type": ["string", "null"],
                "enum": ["postgresql", "sqlserver", "tdengine", None]
            },
            "data_source_id": {
                "type": ["integer", "null"]
            },
            "schema_name": {
                "type": ["string", "null"]
            },
            "table_name": {
                "type": ["string", "null"]
            },
            "time_column": {
                "type": ["string", "null"]
            },
            "value_column": {
                "type": ["string", "null"]
            },
            "category_column": {
                "type": ["string", "null"]
            },
            "category_value": {
                "type": ["string", "number", "boolean", "null"]
            },
            "status_column": {
                "type": ["string", "null"]
            },
            "status_rule_id": {
                "type": ["integer", "null"]
            },
            "minimum_duration_seconds": {
                "type": ["integer", "null"]
            },
            "start_time": {
                "type": ["string", "null"]
            },
            "end_time": {
                "type": ["string", "null"]
            },
            "aggregation": {
                "type": ["string", "null"],
                "enum": ["sum", "avg", "min", "max", "count", None]
            },
            "group_by": {
                "type": ["string", "null"],
                "enum": ["hour", "day", "week", "month", "year", None]
            },
            "limit": {
                "type": ["integer", "null"]
            },
            "chart_type": {
                "type": ["string", "null"],
                "enum": ["line", "bar", "table", "kpi", "timeline", None]
            },
            "explanation": {
                "type": ["string", "null"]
            }
        },
        "required": [
            "intent",
            "database_type",
            "data_source_id",
            "schema_name",
            "table_name",
            "time_column",
            "value_column",
            "category_column",
            "category_value",
            "status_column",
            "status_rule_id",
            "minimum_duration_seconds",
            "start_time",
            "end_time",
            "aggregation",
            "group_by",
            "limit",
            "chart_type",
            "explanation"
        ]
    },
    "strict": True
}

def extract_query_plan_with_openai(
    prompt: str,
    catalog_context: str
) -> QueryPlan:
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    system_prompt = f"""
You are an intent extraction engine for a database query builder.

Your job:
- Convert the user prompt into a JSON query plan.
- Use only the provided catalog context.
- Do not write SQL.
- Do not invent table names.
- Do not invent column names.
- Do not invent data_source_id.
- If the request cannot be answered from the catalog context, return intent "unknown".

Supported intents:
- trend
- summary
- compare
- raw_table
- downtime
- unknown

Intent rules:
- trend: time-series values over time.
- summary: one or more aggregate values.
- compare: compare values by category.
- raw_table: return records in table form.
- downtime: machine stopped / not running / mati / value indicates stopped.

Chart rules:
- trend uses line.
- compare uses bar.
- summary uses kpi.
- raw_table uses table.
- downtime uses timeline.

Aggregation rules:
- total/sales/revenue defaults to sum.
- average/avg uses avg.
- minimum/min uses min.
- maximum/max uses max.
- count uses count.

Date rules:
- Current date context: {current_date}
- If the prompt specifies a relative date (e.g. "today", "last month"), calculate the exact start and end dates based on the current date context.
- If the prompt does NOT mention any date, you MUST provide a default date range covering the last 30 days from the current date context.
- Use format YYYY-MM-DD HH:MM:SS.

For downtime requests:
- Use intent "downtime".
- Select only a status_rule_id included in the provided context.
- Do not invent downtime values.
- Do not create a SQL condition.
- Use chart_type "timeline".
- Select category_value only when the user names a machine or asset.
- Convert duration phrases such as "longer than 30 minutes" into seconds (e.g. minimum_duration_seconds = 1800).
- Return intent "unknown" if no suitable status rule is available.

Return only JSON that matches the schema.
"""

    user_message = f"""
User prompt:
{prompt}

Catalog context:
{catalog_context}
"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": QUERY_PLAN_SCHEMA
        }
    )

    raw_text = response.choices[0].message.content
    parsed = json.loads(raw_text)

    return QueryPlan(**parsed)
