from __future__ import annotations

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def add_prometheus_metrics(app: FastAPI) -> None:
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app, endpoint="/metrics", tags=["Health"])
