from __future__ import annotations

import json
import logging
import os

from azure.storage.queue import QueueServiceClient

logger = logging.getLogger(__name__)

QUEUE_ENV = "QUEUE_NAME"


def _queue_name() -> str:
    return os.environ.get(QUEUE_ENV, "sensor-events")


def _queue_service_client() -> QueueServiceClient:

    conn = os.environ.get("AzureWebJobsStorage")

    if not conn:
        raise RuntimeError("AzureWebJobsStorage no configurado")

    return QueueServiceClient.from_connection_string(conn)


def ensure_queue_exists():

    service = _queue_service_client()

    queue_client = service.get_queue_client(_queue_name())

    try:
        queue_client.create_queue()
        logger.info("Queue creada")
    except Exception:
        logger.info("Queue ya existe")


def enqueue_sensor_event(event_dict: dict):

    ensure_queue_exists()

    service = _queue_service_client()

    queue_client = service.get_queue_client(_queue_name())

    payload = json.dumps(event_dict, ensure_ascii=False)

    # ENVIAR MENSAJE
    queue_client.send_message(payload)

    logger.info(
        "Evento enviado a queue=%s",
        _queue_name()
    )