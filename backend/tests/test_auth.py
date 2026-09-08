from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_login_with_invalid_credentials():
    response = client.post(
        "/api/auth/login",
        data={
            "username": "invalid-user",
            "password": "wrong-password",
        },
    )

    assert response.status_code in {401, 400}


def test_protected_endpoint_without_token():
    response = client.get("/api/auth/me")

    assert response.status_code == 401