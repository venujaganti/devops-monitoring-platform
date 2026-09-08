from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IncidentBase(BaseModel):
    server_id: int | None = None
    title: str
    description: str
    severity: str = "medium"


class IncidentCreate(IncidentBase):
    assigned_to: int | None = None


class IncidentUpdate(BaseModel):
    status: str | None = None
    severity: str | None = None
    assigned_to: int | None = None
    resolution_notes: str | None = None


class IncidentResponse(IncidentBase):
    id: int
    status: str
    assigned_to: int | None = None
    resolution_notes: str | None = None
    created_at: datetime
    acknowledged_at: datetime | None = None
    resolved_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )