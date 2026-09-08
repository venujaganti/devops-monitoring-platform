import os

import requests


BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://localhost:8000",
)


def login():
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={
            "username": "admin",
            "password": "Admin@123",
        },
        timeout=10,
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_health():
    response = requests.get(
        f"{BASE_URL}/health",
        timeout=10,
    )

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


def test_authenticated_api():
    token = login()

    response = requests.get(
        f"{BASE_URL}/api/servers",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=10,
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )