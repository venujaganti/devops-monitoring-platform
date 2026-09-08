from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.incident import Incident


VALID_STATUSES = {
    "open",
    "acknowledged",
    "in_progress",
    "resolved",
}

VALID_SEVERITIES = {
    "low",
    "medium",
    "high",
    "critical",
}


def find_open_incident(
    db: Session,
    alert: Alert,
) -> Incident | None:
    """
    Find an existing open incident generated from the same alert.
    """

    query = db.query(Incident).filter(
        Incident.status != "resolved",
        Incident.title == alert.title,
    )

    if alert.server_id is not None:
        query = query.filter(
            Incident.server_id == alert.server_id
        )

    return (
        query
        .order_by(Incident.created_at.desc())
        .first()
    )


def create_incident_from_alert(
    db: Session,
    alert: Alert,
) -> Incident | None:
    """
    Automatically create an incident from a critical alert.
    """

    if alert.severity != "critical":
        return None

    existing_incident = find_open_incident(
        db=db,
        alert=alert,
    )

    if existing_incident:
        return existing_incident

    incident = Incident(
        server_id=alert.server_id,
        title=alert.title,
        description=alert.message,
        severity="critical",
        status="open",
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def update_incident(
    db: Session,
    incident: Incident,
    status: str | None = None,
    severity: str | None = None,
    assigned_to: int | None = None,
    resolution_notes: str | None = None,
) -> Incident:

    now = datetime.now(timezone.utc)

    if status is not None:

        if status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid incident status: {status}"
            )

        incident.status = status

        if status == "acknowledged":
            if incident.acknowledged_at is None:
                incident.acknowledged_at = now

        elif status == "in_progress":
            if incident.acknowledged_at is None:
                incident.acknowledged_at = now

        elif status == "resolved":
            if incident.acknowledged_at is None:
                incident.acknowledged_at = now

            incident.resolved_at = now

    if severity is not None:

        if severity not in VALID_SEVERITIES:
            raise ValueError(
                f"Invalid incident severity: {severity}"
            )

        incident.severity = severity

    if assigned_to is not None:
        incident.assigned_to = assigned_to

    if resolution_notes is not None:
        incident.resolution_notes = resolution_notes

    db.commit()
    db.refresh(incident)

    return incident