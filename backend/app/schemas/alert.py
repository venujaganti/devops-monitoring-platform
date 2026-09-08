from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    server_id: int | None = None
    title: str
    message: str
    severity: str = "warning"


class AlertUpdate(BaseModel):
    status: str | None = None


class AlertResponse(AlertCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    created_at: datetime
    resolved_at: datetime | None