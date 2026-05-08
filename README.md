# Predictive Maintenance Platform

## Descripción General

Esta solución implementa una plataforma de mantenimiento predictivo
orientada a equipos industriales, basada en la ingesta de telemetría
operativa y el cálculo de probabilidad de fallo en una ventana de 24
horas.

El sistema está construido bajo un enfoque serverless, utilizando Azure
Functions para la exposición de APIs y Azure Queue Storage para el
procesamiento asíncrono y desacoplamiento de eventos.

## Capacidades

- Ingesta de eventos de sensores en tiempo casi real.
- Persistencia lógica de eventos.
- Procesamiento bajo demanda de datos históricos.
- Cálculo de probabilidad de fallo basada en scoring.
- Exposición de predicciones mediante APIs REST.
- Procesamiento asíncrono mediante Queue Storage.
- Desacoplamiento entre ingesta HTTP y procesamiento backend.

------------------------------------------------------------------------

## Arquitectura

- Azure Functions (HTTP) para APIs.
- Azure Queue Storage para procesamiento asíncrono.
- Queue Trigger para procesamiento desacoplado.
- Arquitectura orientada a eventos.

------------------------------------------------------------------------

## Modelo de Datos

```json
{
  "machine_id": "PUMP-1001",
  "timestamp": "2026-04-06T10:15:00Z",
  "variable": "temperature_c",
  "value": 78.4
}
Data Lake Lógico

raw/machine_id=PUMP-1001/year=2026/month=04/day=06/events.ndjson

Formato: NDJSON (append-only)

Lógica de Predicción

failure_probability_24h = sigmoid(weighted_score)

APIs

PUT /api/sensors

GET /api/machines/{machine_id}/prediction

GET /api/predictions

Async Processing

La solución implementa un flujo desacoplado basado en Azure Queue Storage.

Flujo implementado:

Cliente HTTP -> Azure Function HTTP -> Queue Storage -> Queue Trigger -> Procesamiento Backend

Este enfoque permite:

Mejor escalabilidad.
Mayor resiliencia.
Procesamiento desacoplado.
Reducción de carga en endpoints HTTP.
Ejecución Local

https://learn.microsoft.com/azure/azure-functions/functions-run-local

https://learn.microsoft.com/azure/storage/common/storage-use-azurite

Troubleshooting

Durante el desarrollo se resolvieron incompatibilidades entre:

Azurite
Azure Functions Runtime
Python 3.14
Queue Trigger bindings

También se realizaron pruebas de serialización, validación de payloads y procesamiento asíncrono de eventos.