from sqlalchemy.orm import Session

from app.models.metric import Metric


def record_metric(
    db: Session,
    server_id: int,
    metric_type: str,
    value: float,
    unit: str | None = None,
) -> Metric:

    metric = Metric(
        server_id=server_id,
        metric_type=metric_type,
        value=value,
        unit=unit,
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)

    return metric