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


def get_server_id(token):
    response = client.get(
        "/api/servers",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    servers = response.json()

    assert servers

    return servers[0]["id"]


def test_list_incidents():
    token = login()

    response = client.get(
        "/api/incidents",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_incident():
    token = login()
    server_id = get_server_id(token)

    payload = {
        "server_id": server_id,
        "title": "Phase 7 Test Incident",
        "description": "Testing incident creation",
        "severity": "medium",
    }

    response = client.post(
        "/api/incidents",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Phase 7 Test Incident"
    assert data["status"] == "open"


def test_incident_lifecycle():
    token = login()
    server_id = get_server_id(token)

    create_response = client.post(
        "/api/incidents",
        json={
            "server_id": server_id,
            "title": "Lifecycle Test Incident",
            "description": "Testing lifecycle",
            "severity": "high",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert create_response.status_code == 201

    incident_id = create_response.json()["id"]

    response = client.patch(
        f"/api/incidents/{incident_id}",
        json={
            "status": "acknowledged",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "acknowledged"

    response = client.patch(
        f"/api/incidents/{incident_id}",
        json={
            "status": "in_progress",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

    response = client.patch(
        f"/api/incidents/{incident_id}",
        json={
            "status": "resolved",
            "resolution_notes": "Test completed successfully.",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "resolved"
    assert data["resolution_notes"] == (
        "Test completed successfully."
    )
    assert data["resolved_at"] is not None

def test_critical_metric_creates_incident():
    token = login()
    server_id = get_server_id(token)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = client.post(
        "/api/metrics",
        json={
            "server_id": server_id,
            "metric_type": "cpu",
            "value": 99,
            "unit": "%",
        },
        headers=headers,
    )

    assert response.status_code == 201

    response = client.get(
        "/api/incidents",
        params={
            "server_id": server_id,
        },
        headers=headers,
    )

    assert response.status_code == 200

    incidents = response.json()

    assert any(
        incident["severity"] == "critical"
        for incident in incidents
    )