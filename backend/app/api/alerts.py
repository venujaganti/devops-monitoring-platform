from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate
from app.services.incident_service import create_incident_from_alert


router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"],
)


@router.get(
    "",
    response_model=list[AlertResponse],
)
def list_alerts(
    severity: str | None = None,
    alert_status: str | None = None,
    server_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(Alert)

    if severity:
        query = query.filter(
            Alert.severity == severity
        )

    if alert_status:
        query = query.filter(
            Alert.status == alert_status
        )

    if server_id is not None:
        query = query.filter(
            Alert.server_id == server_id
        )

    return (
        query
        .order_by(Alert.created_at.desc())
        .all()
    )


@router.post(
    "",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_alert(
    payload: AlertCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    alert = Alert(
        server_id=payload.server_id,
        title=payload.title,
        message=payload.message,
        severity=payload.severity,
        status="open",
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    if alert.severity == "critical":
        create_incident_from_alert(
            db=db,
            alert=alert,
        )

    return alert


@router.patch(
    "/{alert_id}",
    response_model=AlertResponse,
)
def update_alert(
    alert_id: int,
    payload: AlertUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    allowed_statuses = {
        "open",
        "resolved",
        "acknowledged",
    }

    status_value = payload.status

    if status_value is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alert status is required",
        )

    if status_value not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid alert status",
        )

    alert.status = status_value

    if status_value == "resolved":
        alert.resolved_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(alert)

    return alert