from app.database.connection import Base, engine

# Import models so SQLAlchemy registers all tables.
from app.models import (
    Alert,
    Application,
    Incident,
    Log,
    Metric,
    Server,
    User,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)