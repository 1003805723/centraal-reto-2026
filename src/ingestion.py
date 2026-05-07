from __future__ import annotations

import json
import logging

import azure.functions as func

from .queue_processor import process_sensor_queue
from .queue_storage import enqueue_sensor_event
from .validation import parse_sensor_payload

logger = logging.getLogger(__name__)


def handle_put_sensor(req: func.HttpRequest) -> func.HttpResponse:

    logger.info("--- Ingesta async: recibida petición PUT /api/sensors ---")

    try:
        body = req.get_json()

    except ValueError:

        logger.info("Ingesta: rechazo — cuerpo no es JSON válido.")

        return func.HttpResponse(
            json.dumps({"error": "Cuerpo debe ser JSON"}),
            status_code=400,
            mimetype="application/json",
        )

    if not isinstance(body, dict):

        logger.info("Ingesta: rechazo — JSON raíz debe ser objeto.")

        return func.HttpResponse(
            json.dumps({"error": "JSON debe ser un objeto"}),
            status_code=400,
            mimetype="application/json",
        )

    try:

        event = parse_sensor_payload(body)

    except ValueError as e:

        logger.info("Ingesta: validación fallida — %s", e)

        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json",
        )

    try:

        # =====================================================
        # ENVÍO A QUEUE
        # =====================================================

        enqueue_sensor_event(event.to_ndjson_dict())

        logger.info(
            "Evento enviado correctamente a queue."
        )

        # =====================================================
        # TEST PROCESAMIENTO DIRECTO
        # =====================================================

        logger.info(
            "TEST PROCESAMIENTO DIRECTO"
        )

        process_sensor_queue(
            json.dumps(event.to_ndjson_dict())
        )

    except Exception as e:

        logger.info(
            "Ingesta: error enviando/procesando evento — %s",
            e,
            exc_info=True
        )

        return func.HttpResponse(
            json.dumps({
                "error": "Error procesando evento",
                "detail": str(e)
            }),
            status_code=500,
            mimetype="application/json",
        )

    logger.info(
        "Ingesta async: evento procesado correctamente."
    )

    return func.HttpResponse(
        json.dumps(
            {
                "status": "accepted",
                "machine_id": event.machine_id,
                "message": "Evento enviado y procesado correctamente"
            },
            ensure_ascii=False,
        ),
        status_code=202,
        mimetype="application/json",
    )