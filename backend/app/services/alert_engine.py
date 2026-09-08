from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.metric import Metric
from app.models.server import Server


WARNING_THRESHOLDS = {
    "cpu": 80.0,
    "memory": 80.0,
    "disk": 80.0,
}

CRITICAL_THRESHOLDS = {
    "cpu": 95.0,
    "memory": 90.0,
    "disk": 90.0,
}


def get_severity(metric_type: str, value: float) -> str | None:
    """
    Determine alert severity based on metric type and value.

    Returns:
        None       -> healthy
        warning    -> warning threshold exceeded
        critical   -> critical threshold exceeded
    """

    metric_type = metric_type.lower()

    critical_threshold = CRITICAL_THRESHOLDS.get(metric_type)
    warning_threshold = WARNING_THRESHOLDS.get(metric_type)

    if critical_threshold is not None and value > critical_threshold:
        return "critical"

    if warning_threshold is not None and value > warning_threshold:
        return "warning"

    return None


def build_alert_title(
    server: Server,
    metric_type: str,
    severity: str,
) -> str:
    return (
        f"{severity.upper()} {metric_type.upper()} alert "
        f"on {server.hostname}"
    )


def build_alert_message(
    server: Server,
    metric_type: str,
    value: float,
    severity: str,
) -> str:
    if metric_type == "cpu":
        unit = "%"
    elif metric_type == "memory":
        unit = "%"
    elif metric_type == "disk":
        unit = "%"
    else:
        unit = ""

    return (
        f"{server.hostname} reported {metric_type.upper()} usage "
        f"of {value:.2f}{unit}. "
        f"Alert severity: {severity.upper()}."
    )


def find_active_alert(
    db: Session,
    server_id: int,
    metric_type: str,
) -> Alert | None:
    """
    Find an existing unresolved alert for the same server and metric.

    This prevents the agent from creating thousands of duplicate alerts
    while a metric remains above its threshold.
    """

    return (
        db.query(Alert)
        .filter(
            Alert.server_id == server_id,
            Alert.status == "open",
            Alert.title.ilike(f"%{metric_type.upper()}%"),
        )
        .order_by(Alert.created_at.desc())
        .first()
    )


def resolve_active_alerts(
    db: Session,
    server_id: int,
    metric_type: str,
) -> None:
    """
    Resolve active alerts when the metric returns to a healthy value.
    """

    alerts = (
        db.query(Alert)
        .filter(
            Alert.server_id == server_id,
            Alert.status == "open",
            Alert.title.ilike(f"%{metric_type.upper()}%"),
        )
        .all()
    )

    now = datetime.now(timezone.utc)

    for alert in alerts:
        alert.status = "resolved"
        alert.resolved_at = now

    db.commit()


def evaluate_metric(
    db: Session,
    metric: Metric,
) -> Alert | None:
    """
    Evaluate one metric and create/update/resolve an alert.
    """

    server = (
        db.query(Server)
        .filter(Server.id == metric.server_id)
        .first()
    )

    if server is None:
        return None

    metric_type = metric.metric_type.lower()
    value = float(metric.value)

    severity = get_severity(metric_type, value)

    # Healthy metric.
    if severity is None:
        resolve_active_alerts(
            db=db,
            server_id=server.id,
            metric_type=metric_type,
        )
        return None

    existing_alert = find_active_alert(
        db=db,
        server_id=server.id,
        metric_type=metric_type,
    )

    # Existing alert found.
    if existing_alert:
        # Upgrade warning → critical.
        if (
            existing_alert.severity != severity
            and severity == "critical"
        ):
            existing_alert.severity = "critical"
            existing_alert.message = build_alert_message(
                server,
                metric_type,
                value,
                severity,
            )

            db.commit()
            db.refresh(existing_alert)

        return existing_alert

    # Create a new alert.
    alert = Alert(
        server_id=server.id,
        title=build_alert_title(
            server,
            metric_type,
            severity,
        ),
        message=build_alert_message(
            server,
            metric_type,
            value,
            severity,
        ),
        severity=severity,
        status="open",
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert