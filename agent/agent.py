import logging
import platform
import socket
import time
from datetime import datetime, timezone

import psutil
import requests

from config import (
    AGENT_INTERVAL,
    AGENT_PASSWORD,
    AGENT_USERNAME,
    BACKEND_URL,
    REQUEST_TIMEOUT,
    HOSTNAME,
)


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger(
    "devops-monitoring-agent"
)


class MonitoringAgent:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.interval = AGENT_INTERVAL
        self.timeout = REQUEST_TIMEOUT

        self.hostname = (
            HOSTNAME.strip()
            or socket.gethostname()
        )

        self.server_id = None
        self.token = None

        self.session = requests.Session()

    # -------------------------------------------------
    # Authentication
    # -------------------------------------------------

    def authenticate(self):
        url = (
            f"{self.backend_url}"
            "/api/auth/login"
        )

        payload = {
            "username": AGENT_USERNAME,
            "password": AGENT_PASSWORD,
        }

        try:
            response = self.session.post(
                url,
                data=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

            data = response.json()

            self.token = data.get(
                "access_token"
            )

            if not self.token:
                raise RuntimeError(
                    "Backend did not return access token"
                )

            self.session.headers.update(
                {
                    "Authorization":
                        f"Bearer {self.token}"
                }
            )

            logger.info(
                "Successfully authenticated with backend"
            )

            return True

        except requests.RequestException as exc:
            logger.error(
                "Authentication failed: %s",
                exc,
            )

            return False

        except (ValueError, RuntimeError) as exc:
            logger.error(
                "Invalid authentication response: %s",
                exc,
            )

            return False

    # -------------------------------------------------
    # Server registration
    # -------------------------------------------------

    def register_server(self):
        url = (
            f"{self.backend_url}"
            "/api/servers"
        )

        memory = psutil.virtual_memory()

        payload = {
            "hostname": self.hostname,
            "ip_address": self.get_ip_address(),
            "environment": "monitoring",
            "operating_system": (
                f"{platform.system()} "
                f"{platform.release()}"
            ),
            "status": "online",
            "cpu_cores": psutil.cpu_count(
                logical=True
            ),
            "memory_total_mb": round(
                memory.total / (1024 * 1024)
            ),
            "description": (
                "Registered by monitoring agent"
            ),
        }

        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout,
            )

            if response.status_code == 401:
                logger.warning(
                    "Authentication expired"
                )

                self.token = None

                return False

            if response.status_code == 409:
                logger.info(
                    "Server already exists: %s",
                    self.hostname,
                )

                return self.find_existing_server()

            response.raise_for_status()

            data = response.json()

            self.server_id = data.get("id")

            logger.info(
                "Server registered: %s (ID=%s)",
                self.hostname,
                self.server_id,
            )

            return self.server_id is not None

        except requests.RequestException as exc:
            logger.error(
                "Server registration failed: %s",
                exc,
            )

            return False

    def find_existing_server(self):
        url = (
            f"{self.backend_url}"
            "/api/servers"
        )

        try:
            response = self.session.get(
                url,
                timeout=self.timeout,
            )

            response.raise_for_status()

            servers = response.json()

            for server in servers:
                if (
                    server.get("hostname")
                    == self.hostname
                ):
                    self.server_id = server.get(
                        "id"
                    )

                    logger.info(
                        "Existing server found: ID=%s",
                        self.server_id,
                    )

                    return self.server_id is not None

        except requests.RequestException as exc:
            logger.error(
                "Unable to find existing server: %s",
                exc,
            )

        return False

    # -------------------------------------------------
    # System information
    # -------------------------------------------------

    def get_ip_address(self):
        try:
            hostname = socket.gethostname()

            return socket.gethostbyname(
                hostname
            )

        except socket.gaierror:
            return "127.0.0.1"

    def collect_system_info(self):
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        return {
            "hostname": self.hostname,
            "ip_address": self.get_ip_address(),
            "operating_system": (
                platform.system()
            ),
            "os_release": platform.release(),
            "cpu_count": psutil.cpu_count(
                logical=True
            ),
            "memory_total_mb": round(
                memory.total / (1024 * 1024)
            ),
            "disk_total_gb": round(
                disk.total / (1024 ** 3),
                2,
            ),
        }

    # -------------------------------------------------
    # CPU metric
    # -------------------------------------------------

    def collect_cpu(self):
        return psutil.cpu_percent(
            interval=1
        )

    # -------------------------------------------------
    # Memory metric
    # -------------------------------------------------

    def collect_memory(self):
        memory = psutil.virtual_memory()

        return memory.percent

    # -------------------------------------------------
    # Disk metric
    # -------------------------------------------------

    def collect_disk(self):
        disk = psutil.disk_usage("/")

        return disk.percent

    # -------------------------------------------------
    # Network metric
    # -------------------------------------------------

    def collect_network(self):
        network = psutil.net_io_counters()

        return {
            "bytes_sent": network.bytes_sent,
            "bytes_received": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_received": network.packets_recv,
        }

    # -------------------------------------------------
    # Process information
    # -------------------------------------------------

    def collect_process_count(self):
        try:
            return len(
                psutil.pids()
            )
        except psutil.Error:
            return 0

    # -------------------------------------------------
    # Send metric
    # -------------------------------------------------

    def send_metric(
        self,
        metric_type,
        value,
        unit,
    ):
        if self.server_id is None:
            logger.warning(
                "Cannot send metric: server ID unavailable"
            )

            return False

        url = (
            f"{self.backend_url}"
            "/api/metrics"
        )

        payload = {
            "server_id": self.server_id,
            "metric_type": metric_type,
            "value": float(value),
            "unit": unit,
            "recorded_at": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
        }

        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout,
            )

            if response.status_code == 401:
                logger.warning(
                    "Metric request unauthorized"
                )

                self.token = None

                return False

            response.raise_for_status()

            logger.info(
                "Metric sent: %s = %.2f %s",
                metric_type,
                float(value),
                unit,
            )

            return True

        except requests.RequestException as exc:
            logger.error(
                "Failed to send %s metric: %s",
                metric_type,
                exc,
            )

            return False

    # -------------------------------------------------
    # Collect and send all metrics
    # -------------------------------------------------

    def collect_and_send_metrics(self):
        cpu = self.collect_cpu()

        memory = self.collect_memory()

        disk = self.collect_disk()

        process_count = (
            self.collect_process_count()
        )

        self.send_metric(
            "cpu",
            cpu,
            "percent",
        )

        self.send_metric(
            "memory",
            memory,
            "percent",
        )

        self.send_metric(
            "disk",
            disk,
            "percent",
        )

        self.send_metric(
            "process_count",
            process_count,
            "count",
        )

        network = self.collect_network()

        self.send_metric(
            "network_bytes_sent",
            network["bytes_sent"],
            "bytes",
        )

        self.send_metric(
            "network_bytes_received",
            network["bytes_received"],
            "bytes",
        )

    # -------------------------------------------------
    # Main loop
    # -------------------------------------------------

    def run(self):
        logger.info(
            "Starting DevOps Monitoring Agent"
        )

        logger.info(
            "Hostname: %s",
            self.hostname,
        )

        logger.info(
            "Backend: %s",
            self.backend_url,
        )

        logger.info(
            "Interval: %s seconds",
            self.interval,
        )

        while True:
            try:
                if not self.token:
                    if not self.authenticate():
                        time.sleep(
                            self.interval
                        )
                        continue

                if self.server_id is None:
                    if not self.register_server():
                        time.sleep(
                            self.interval
                        )
                        continue

                self.collect_and_send_metrics()

                time.sleep(
                    self.interval
                )

            except KeyboardInterrupt:
                logger.info(
                    "Monitoring agent stopped"
                )

                break

            except Exception:
                logger.exception(
                    "Unexpected agent error"
                )

                time.sleep(
                    self.interval
                )

        self.session.close()


def main():
    agent = MonitoringAgent()
    agent.run()


if __name__ == "__main__":
    main()