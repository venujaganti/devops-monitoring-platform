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


def test_list_alerts():
    token = login()

    response = client.get(
        "/api/alerts",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_warning_alert_generation():
    token = login()
    server_id = get_server_id(token)

    response = client.post(
        "/api/metrics",
        json={
            "server_id": server_id,
            "metric_type": "cpu",
            "value": 85,
            "unit": "%",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    alerts = client.get(
        "/api/alerts",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert alerts.status_code == 200

    data = alerts.json()

    assert any(
        alert["severity"] == "warning"
        for alert in data
    )


def test_critical_alert_generation():
    token = login()
    server_id = get_server_id(token)

    response = client.post(
        "/api/metrics",
        json={
            "server_id": server_id,
            "metric_type": "cpu",
            "value": 99,
            "unit": "%",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    alerts = client.get(
        "/api/alerts",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    data = alerts.json()

    assert any(
        alert["severity"] == "critical"
        for alert in data
    )

def test_alert_deduplication():
    token = login()
    server_id = get_server_id(token)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    for value in [96, 97, 98]:
        response = client.post(
            "/api/metrics",
            json={
                "server_id": server_id,
                "metric_type": "cpu",
                "value": value,
                "unit": "%",
            },
            headers=headers,
        )

        assert response.status_code == 201

    response = client.get(
        "/api/alerts",
        params={
            "server_id": server_id,
            "severity": "critical",
            "alert_status": "open",
        },
        headers=headers,
    )

    assert response.status_code == 200

    alerts = response.json()

    assert len(alerts) >= 1

def test_alert_recovery():
    token = login()
    server_id = get_server_id(token)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Generate critical condition.
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

    # Return to healthy state.
    response = client.post(
        "/api/metrics",
        json={
            "server_id": server_id,
            "metric_type": "cpu",
            "value": 30,
            "unit": "%",
        },
        headers=headers,
    )

    assert response.status_code == 201

    response = client.get(
        "/api/alerts",
        params={
            "server_id": server_id,
        },
        headers=headers,
    )

    assert response.status_code == 200

    alerts = response.json()

    assert any(
        alert["status"] == "resolved"
        for alert in alerts
    )