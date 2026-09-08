from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogCreate(BaseModel):
    server_id: int | None = None
    level: str = "INFO"
    source: str | None = None
    message: str


class LogResponse(LogCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime