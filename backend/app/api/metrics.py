from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.metric import Metric
from app.schemas.metric import MetricCreate, MetricResponse
from app.services.alert_engine import evaluate_metric
from app.services.incident_service import create_incident_from_alert


router = APIRouter(
    prefix="/api/metrics",
    tags=["Metrics"],
)


@router.get(
    "",
    response_model=list[MetricResponse],
)
def list_metrics(
    server_id: int | None = None,
    metric_type: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(Metric)

    if server_id is not None:
        query = query.filter(
            Metric.server_id == server_id
        )

    if metric_type:
        query = query.filter(
            Metric.metric_type == metric_type
        )

    limit = min(max(limit, 1), 500)

    return (
        query
        .order_by(Metric.recorded_at.desc())
        .limit(limit)
        .all()
    )


@router.post(
    "",
    response_model=MetricResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_metric(
    payload: MetricCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    metric = Metric(
        server_id=payload.server_id,
        metric_type=payload.metric_type,
        value=payload.value,
        unit=payload.unit,
        recorded_at=payload.recorded_at
        or datetime.now(timezone.utc),
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)

    # Evaluate the metric.
    alert = evaluate_metric(
        db=db,
        metric=metric,
    )

    # Critical alerts automatically become incidents.
    if alert and alert.severity == "critical":
        create_incident_from_alert(
            db=db,
            alert=alert,
        )

    return metric