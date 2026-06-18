from pydantic import BaseModel
from typing import Optional

class DataSourceCreate(BaseModel):
    name: str
    database_type: str
    host: str
    port: int
    database_name: str
    username: str
    password: str
    default_schema: Optional[str] = "public"

class DataSourceResponse(BaseModel):
    id: int
    name: str
    database_type: str
    host: str
    port: int
    database_name: str
    username: str
    default_schema: Optional[str]
    is_active: bool
