from pydantic import BaseModel
from typing import Optional

class CatalogPatch(BaseModel):
    business_name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    aliases: Optional[str] = None
    is_time_column: Optional[bool] = None
    is_value_column: Optional[bool] = None
    is_category_column: Optional[bool] = None
    default_aggregation: Optional[str] = None
    default_chart: Optional[str] = None
    is_queryable: Optional[bool] = None
