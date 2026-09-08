from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def login():
    response = client.post(
        "/api/auth/login",
        data={
            "username": "admin",
            "password": "Admin@123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_list_servers():
    token = login()

    response = client.get(
        "/api/servers",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_server():
    token = login()

    payload = {
        "hostname": "test-server-phase7",
        "ip_address": "10.10.10.10",
        "environment": "testing",
        "operating_system": "Ubuntu",
        "status": "online",
        "cpu_cores": 2,
        "memory_total_mb": 2048,
        "description": "Phase 7 test server",
    }

    response = client.post(
        "/api/servers",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code in {200, 201, 409}