from sqlalchemy import text
from sqlalchemy.orm import Session


def check_database_health(db: Session) -> bool:
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False