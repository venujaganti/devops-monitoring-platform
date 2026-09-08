from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    name: str
    server_id: int | None = None
    version: str | None = None
    port: int | None = None
    status: str = "unknown"


class ApplicationResponse(ApplicationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime