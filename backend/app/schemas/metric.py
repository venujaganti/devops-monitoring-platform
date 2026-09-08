from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MetricBase(BaseModel):
    server_id: int
    metric_type: str
    value: float
    unit: str


class MetricCreate(MetricBase):
    recorded_at: datetime | None = None


class MetricResponse(MetricBase):
    id: int
    recorded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )