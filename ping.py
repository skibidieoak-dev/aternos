import logging
import os
import sys

import requests

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger("aternos-ping")


def ping_server() -> int:
    base_url = os.getenv("SERVICE_URL", "").strip().rstrip("/")
    if not base_url:
        logger.error("SERVICE_URL não configurada no Cron Job")
        return 1

    url = f"{base_url}/health"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        logger.info("Ping bem-sucedido em %s: HTTP %s", url, response.status_code)
        return 0
    except requests.RequestException as exc:
        logger.error("Falha ao fazer ping em %s: %s", url, exc)
        return 1


if __name__ == "__main__":
    sys.exit(ping_server())
