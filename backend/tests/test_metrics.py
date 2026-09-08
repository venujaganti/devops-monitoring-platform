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

    assert response.status_code == 200

    servers = response.json()

    assert len(servers) > 0

    return servers[0]["id"]


def test_list_metrics():
    token = login()

    response = client.get(
        "/api/metrics",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_metric():
    token = login()
    server_id = get_server_id(token)

    payload = {
        "server_id": server_id,
        "metric_type": "cpu",
        "value": 40,
        "unit": "%",
    }

    response = client.post(
        "/api/metrics",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["metric_type"] == "cpu"
    assert data["value"] == 40