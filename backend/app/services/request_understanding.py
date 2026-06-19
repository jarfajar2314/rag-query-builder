import json
from openai import OpenAI

from app.config import settings
from app.models.user_request import UserRequestUnderstanding

client = OpenAI(api_key=settings.openai_api_key)

USER_REQUEST_SCHEMA = {
    "name": "user_request_understanding",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "intent": {
                "type": "string",
                "enum": ["trend", "summary", "compare", "raw_table", "downtime", "unknown"]
            },
            "metric_terms": {
                "type": "array",
                "items": {"type": "string"}
            },
            "subject_terms": {
                "type": "array",
                "items": {"type": "string"}
            },
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "type": {"type": ["string", "null"]},
                        "value": {"type": "string"}
                    },
                    "required": ["type", "value"]
                }
            },
            "time_expression": {
                "type": ["string", "null"]
            },
            "requested_output": {
                "type": ["string", "null"]
            },
            "aggregation": {
                "type": ["string", "null"]
            },
            "grouping": {
                "type": ["string", "null"]
            },
            "explanation": {
                "type": ["string", "null"]
            }
        },
        "required": [
            "intent", "metric_terms", "subject_terms", "entities", 
            "time_expression", "requested_output", "aggregation", 
            "grouping", "explanation"
        ]
    },
    "strict": True
}

def understand_user_request(prompt: str) -> UserRequestUnderstanding:
    system_prompt = """
Understand the user request.

Extract:
- intent
- business concepts (metric_terms, subject_terms)
- entity names
- date expressions (time_expression)
- requested output (requested_output e.g. 'intervals', 'chart', 'table')
- aggregation
- grouping

Do not select database tables.
Do not select columns.
Do not generate SQL.

Intent rules:
- downtime: user asks about machine stoppages, downtime, not running, mati, etc.
- trend: user asks for time-series values over time.
- summary: user asks for a total, average, or single aggregate value.
- compare: user asks to compare values by a category.
- raw_table: user asks for latest records, raw logs, or a table.

Extract entities precisely as written by the user. Do not invent entities.
"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": USER_REQUEST_SCHEMA
        }
    )

    raw_text = response.choices[0].message.content
    parsed = json.loads(raw_text)

    return UserRequestUnderstanding(**parsed)
