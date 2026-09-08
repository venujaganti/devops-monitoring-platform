from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.database.connection import SessionLocal
from app.models.user import User


DEFAULT_USERNAME = "admin"
DEFAULT_EMAIL = "admin@example.com"
DEFAULT_PASSWORD = "Admin@123"


def seed_admin() -> None:
    db: Session = SessionLocal()

    try:
        existing_admin = (
            db.query(User)
            .filter(User.username == DEFAULT_USERNAME)
            .first()
        )

        if existing_admin is None:
            db.add(
                User(
                    username=DEFAULT_USERNAME,
                    email=DEFAULT_EMAIL,
                    password_hash=hash_password(DEFAULT_PASSWORD),
                    full_name="System Administrator",
                    role="admin",
                    is_active=True,
                )
            )

        # The monitoring agent uses a separate least-privileged account.
        agent_username = settings.AGENT_USERNAME.strip()
        if agent_username and agent_username != DEFAULT_USERNAME:
            existing_agent = (
                db.query(User)
                .filter(User.username == agent_username)
                .first()
            )

            if existing_agent is None:
                db.add(
                    User(
                        username=agent_username,
                        email=f"{agent_username}@example.com",
                        password_hash=hash_password(settings.AGENT_PASSWORD),
                        full_name="Monitoring Agent",
                        role="viewer",
                        is_active=True,
                    )
                )

        db.commit()

    finally:
        db.close()
