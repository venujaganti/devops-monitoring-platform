from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.incident import Incident
from app.models.user import User
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
)
from app.services.incident_service import (
    update_incident,
)


router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"],
)


@router.get(
    "",
    response_model=list[IncidentResponse],
)
def list_incidents(
    incident_status: str | None = None,
    severity: str | None = None,
    server_id: int | None = None,
    assigned_to: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Incident)

    if incident_status:
        query = query.filter(
            Incident.status == incident_status
        )

    if severity:
        query = query.filter(
            Incident.severity == severity
        )

    if server_id is not None:
        query = query.filter(
            Incident.server_id == server_id
        )

    if assigned_to is not None:
        query = query.filter(
            Incident.assigned_to == assigned_to
        )

    return (
        query
        .order_by(Incident.created_at.desc())
        .all()
    )


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    return incident


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    payload: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.severity not in {
        "low",
        "medium",
        "high",
        "critical",
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid incident severity",
        )

    if payload.assigned_to is not None:

        user = (
            db.query(User)
            .filter(User.id == payload.assigned_to)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found",
            )

    incident = Incident(
        server_id=payload.server_id,
        title=payload.title,
        description=payload.description,
        severity=payload.severity,
        status="open",
        assigned_to=payload.assigned_to,
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def modify_incident(
    incident_id: int,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    if payload.assigned_to is not None:

        user = (
            db.query(User)
            .filter(User.id == payload.assigned_to)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found",
            )

    try:
        incident = update_incident(
            db=db,
            incident=incident,
            status=payload.status,
            severity=payload.severity,
            assigned_to=payload.assigned_to,
            resolution_notes=payload.resolution_notes,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return incident