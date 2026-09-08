import pytest

from app.database import init_db
from app.database.connection import SessionLocal
from app.database.seed import seed_admin
from app.models.server import Server


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Create all SQLAlchemy tables.
    init_db()

    # Create the default admin and agent users.
    seed_admin()

    # Tests expect at least one server to exist.
    db = SessionLocal()

    try:
        existing_server = (
            db.query(Server)
            .filter(Server.hostname == "test-server")
            .first()
        )

        if existing_server is None:
            db.add(
                Server(
                    hostname="test-server",
                    ip_address="10.0.0.10",
                    environment="testing",
                    operating_system="Ubuntu",
                    status="online",
                    cpu_cores=2,
                    memory_total_mb=4096,
                    description="CI test server",
                    is_active=True,
                )
            )

            db.commit()
    finally:
        db.close()
