from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)


def process_sensor_queue(msg):

    logger.info("=== INICIO PROCESS SENSOR QUEUE ===")

    try:

        logger.info("TIPO MSG: %s", type(msg))

        # =====================================================
        # LEER MENSAJE SEGÚN TIPO
        # =====================================================

        # SI VIENE COMO BYTES
        if isinstance(msg, bytes):

            raw_body = msg.decode("utf-8")

        # SI VIENE COMO STRING
        elif isinstance(msg, str):

            raw_body = msg

        # SI VIENE COMO QueueMessage
        else:

            raw_body = msg.get_body().decode("utf-8")

        logger.info("Mensaje RAW recibido:")
        logger.info(raw_body)

        # =====================================================
        # PARSE JSON
        # =====================================================

        event = json.loads(raw_body)

        logger.info("Evento parseado correctamente")

        # =====================================================
        # EXTRAER DATOS
        # =====================================================

        machine_id = event.get("machine_id")
        variable = event.get("variable")
        value = event.get("value")
        timestamp = event.get("timestamp")

        logger.info(
            "Procesando evento -> machine=%s variable=%s value=%s timestamp=%s",
            machine_id,
            variable,
            value,
            timestamp
        )

        # =====================================================
        # FUTURO:
        # - Blob Storage
        # - Predicción
        # - Persistencia
        # =====================================================

        logger.info("Evento procesado correctamente.")

    except Exception as e:

        logger.exception(
            "ERROR procesando mensaje queue: %s",
            e
        )

        raise