from typing import Any

from pydantic import BaseModel, Field, model_validator


class StatusRuleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None

    status_column_catalog_id: int
    time_column_catalog_id: int
    category_column_catalog_id: int | None = None

    running_values: list[Any] = Field(default_factory=list)
    downtime_values: list[Any] = Field(min_length=1)

    expected_interval_seconds: int = Field(gt=0)
    gap_tolerance_seconds: int = Field(gt=0)
    minimum_downtime_seconds: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_intervals(self):
        if self.gap_tolerance_seconds < self.expected_interval_seconds:
            raise ValueError(
                "gap_tolerance_seconds must be greater than or equal "
                "to expected_interval_seconds."
            )

        return self


class StatusRuleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    running_values: list[Any] | None = None
    downtime_values: list[Any] | None = None

    expected_interval_seconds: int | None = Field(default=None, gt=0)
    gap_tolerance_seconds: int | None = Field(default=None, gt=0)
    minimum_downtime_seconds: int | None = Field(default=None, ge=0)

    is_active: bool | None = None
