from typing import Literal

from pydantic import BaseModel, Field

class EntityTerm(BaseModel):
    type: str | None = None
    value: str

class UserRequestUnderstanding(BaseModel):
    intent: Literal[
        "trend",
        "summary",
        "compare",
        "raw_table",
        "downtime",
        "unknown",
    ]

    metric_terms: list[str] = Field(default_factory=list)
    subject_terms: list[str] = Field(default_factory=list)
    entities: list[EntityTerm] = Field(default_factory=list)

    time_expression: str | None = None
    requested_output: str | None = None
    aggregation: str | None = None
    grouping: str | None = None

    explanation: str | None = None
