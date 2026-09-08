from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.log import Log
from app.models.user import User
from app.schemas.log import LogCreate, LogResponse


router = APIRouter(
    prefix="/api/logs",
    tags=["Logs"],
)


@router.get(
    "",
    response_model=list[LogResponse],
)
def list_logs(
    server_id: int | None = None,
    level: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Log)

    if server_id is not None:
        query = query.filter(
            Log.server_id == server_id
        )

    if level:
        query = query.filter(
            Log.level == level.upper()
        )

    return (
        query.order_by(Log.created_at.desc())
        .limit(min(limit, 1000))
        .all()
    )


@router.post(
    "",
    response_model=LogResponse,
)
def create_log(
    log_data: LogCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    log = Log(**log_data.model_dump())

    db.add(log)
    db.commit()
    db.refresh(log)

    return log