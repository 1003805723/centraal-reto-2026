"""
Azure Functions (modelo programático v2):
APIs de ingesta, predicción y procesamiento asíncrono.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import azure.functions as func

# =========================================================
# CONFIGURACIÓN IMPORTS
# =========================================================

_root = Path(__file__).resolve().parent

if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# =========================================================
# IMPORTS APP
# =========================================================

from src.ingestion import handle_put_sensor  # noqa: E402

from src.prediction import (  # noqa: E402
    handle_get_all_predictions,
    handle_get_machine_prediction,
)

from src.queue_processor import process_sensor_queue  # noqa: E402

logger = logging.getLogger(__name__)

# =========================================================
# APP
# =========================================================

app = func.FunctionApp()

# =========================================================
# HTTP INGESTA
# =========================================================

@app.route(
    route="sensors",
    methods=["PUT"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def sensors_put(req: func.HttpRequest) -> func.HttpResponse:

    logger.info(
        "Function HTTP disparada: ruta sensors método PUT."
    )

    return handle_put_sensor(req)

# =========================================================
# HTTP PREDICCIÓN POR MÁQUINA
# =========================================================

@app.route(
    route="machines/{machine_id}/prediction",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
def machine_prediction(req: func.HttpRequest) -> func.HttpResponse:

    machine_id = req.route_params.get("machine_id", "")

    logger.info(
        "Function HTTP disparada: predicción máquina=%s",
        machine_id,
    )

    return handle_get_machine_prediction(req, machine_id)

# =========================================================
# HTTP TODAS LAS PREDICCIONES
# =========================================================

@app.route(
    route="predictions",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def all_predictions(req: func.HttpRequest) -> func.HttpResponse:

    logger.info(
        "Function HTTP disparada: listado predictions."
    )

    return handle_get_all_predictions(req)

# =========================================================
# QUEUE TRIGGER DESACTIVADO TEMPORALMENTE
# =========================================================

"""
@app.queue_trigger(
    arg_name="msg",
    queue_name="sensor-events",
    connection="AzureWebJobsStorage"
)
def sensor_queue_trigger(msg):

    logger.info(
        "Queue Trigger disparado: mensaje recibido."
    )

    process_sensor_queue(msg)
"""