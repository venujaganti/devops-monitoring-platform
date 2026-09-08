from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ServerCreate(BaseModel):
    hostname: str
    ip_address: str
    environment: str = "development"
    operating_system: str | None = None
    status: str = "unknown"
    cpu_cores: int | None = None
    memory_total_mb: int | None = None
    description: str | None = None


class ServerUpdate(BaseModel):
    hostname: str | None = None
    ip_address: str | None = None
    environment: str | None = None
    operating_system: str | None = None
    status: str | None = None
    cpu_cores: int | None = None
    memory_total_mb: int | None = None
    description: str | None = None
    is_active: bool | None = None


class ServerResponse(ServerCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime