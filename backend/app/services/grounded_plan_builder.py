import json
from openai import OpenAI
from pydantic import ValidationError

from app.config import settings
from app.models.query_plan import QueryPlan
from app.models.user_request import UserRequestUnderstanding
from app.services.metadata_retriever import CatalogContextData

client = OpenAI(api_key=settings.openai_api_key)

QUERY_PLAN_SCHEMA = {
    "name": "query_plan",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "status": {
                "type": "string",
                "enum": ["ready", "needs_clarification", "unsupported"]
            },
            "missing_fields": {
                "type": "array",
                "items": {"type": "string"}
            },
            "clarification_question": {
                "type": ["string", "null"]
            },
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
                "type": ["string", "null"]
            },
            "status_column": {
                "type": ["string", "null"]
            },
            "status_rule_id": {
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
            "status",
            "missing_fields",
            "clarification_question",
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

def build_grounded_query_plan(
    prompt: str,
    understanding: UserRequestUnderstanding,
    catalog_context: CatalogContextData
) -> QueryPlan:
    # Serialize context for prompt
    context_str = json.dumps({
        "catalog_rows": catalog_context.catalog_rows,
        "status_rules": catalog_context.status_rules
    }, indent=2, default=str)
    
    understanding_str = understanding.model_dump_json(indent=2)
    
    system_prompt = """
You are a database query planner. 
Your job is to ground a parsed user request (UserRequestUnderstanding) into the actual database metadata (Catalog Context) to produce a structured JSON QueryPlan.

CRITICAL RULES:
1. ONLY select tables, columns, and rules that exist in the Catalog Context.
3. If the request is understood but some fields (like dates or categories) are missing, YOU MUST STILL output `status: "ready"`. 
   - NEVER use `needs_clarification` for missing `start_time` or `end_time`. Leave them `null`. The backend provides defaults.
   - NEVER use `needs_clarification` for `time_column` or `value_column`. Guess them from `is_time_column` and `is_value_column`.
   - Use `needs_clarification` ONLY if the user's core intent is completely unintelligible.
4. If the user specifies "all" for an entity (e.g. "all machines", "all regions"), DO NOT set a `category_value` filter. Leave it null and treat it as a summary/trend over everything, or group by it if appropriate.
5. If the understanding extracts a specific entity (e.g. "Machine D"), ALWAYS map it exactly to the `category_value` field. DO NOT ask for clarification about entity names or values, as they will be validated against the database in a later step.
6. If intent is downtime, ensure you select the appropriate `status_rule_id` from the status rules context.

Chart rules:
- trend -> line
- compare -> bar
- summary -> kpi
- raw_table -> table
- downtime -> timeline
"""

    user_message = f"""
Original Prompt: {prompt}

Understanding:
{understanding_str}

Catalog Context:
{context_str}
"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": QUERY_PLAN_SCHEMA
        }
    )

    raw_text = response.choices[0].message.content
    parsed = json.loads(raw_text)

    return QueryPlan(**parsed)
