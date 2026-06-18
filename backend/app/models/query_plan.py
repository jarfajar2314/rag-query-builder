from typing import Literal, Optional
from pydantic import BaseModel, Field

IntentType = Literal[
    "trend",
    "summary",
    "compare",
    "raw_table",
    "downtime",
    "unknown"
]

DatabaseType = Literal[
    "postgresql",
    "sqlserver",
    "tdengine"
]

ChartType = Literal[
    "line",
    "bar",
    "table",
    "kpi",
    "timeline"
]

AggregationType = Literal[
    "sum",
    "avg",
    "min",
    "max",
    "count"
]

GroupByType = Literal[
    "hour",
    "day",
    "week",
    "month",
    "year"
]

class QueryPlan(BaseModel):
    intent: IntentType

    database_type: Optional[DatabaseType] = None
    data_source_id: Optional[int] = None
    schema_name: Optional[str] = None
    table_name: Optional[str] = None

    time_column: Optional[str] = None
    value_column: Optional[str] = None
    category_column: Optional[str] = None
    status_column: Optional[str] = None

    start_time: Optional[str] = None
    end_time: Optional[str] = None

    aggregation: Optional[AggregationType] = "sum"
    group_by: Optional[GroupByType] = "day"
    limit: Optional[int] = 100

    chart_type: Optional[ChartType] = None

    explanation: Optional[str] = Field(
        default=None,
        description="Short explanation of why this query plan was selected."
    )
