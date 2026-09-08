import os

from dotenv import load_dotenv


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000",
).rstrip("/")


AGENT_INTERVAL = int(
    os.getenv(
        "AGENT_INTERVAL",
        "30",
    )
)


AGENT_USERNAME = os.getenv(
    "AGENT_USERNAME",
    "agent",
)


AGENT_PASSWORD = os.getenv(
    "AGENT_PASSWORD",
    "Agent@123",
)


REQUEST_TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        "10",
    )
)


HOSTNAME = os.getenv(
    "HOSTNAME",
    "",
)


def get_config():
    return {
        "backend_url": BACKEND_URL,
        "agent_interval": AGENT_INTERVAL,
        "agent_username": AGENT_USERNAME,
        "agent_password": AGENT_PASSWORD,
        "request_timeout": REQUEST_TIMEOUT,
        "hostname": HOSTNAME,
    }