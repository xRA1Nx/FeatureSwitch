from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.apps.router import api_router
from src.server.db import get_async_engine
from src.server.prometheus import add_prometheus_metrics
from src.server.settings import get_cors_origins


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:  # noqa: ARG001
    logging.basicConfig(level=logging.INFO)
    yield
    await get_async_engine().dispose()


def get_application() -> FastAPI:
    """
    Базовая настройка приложения.
    """
    app = FastAPI(title="TV-Program", lifespan=lifespan)
    app.include_router(api_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_prometheus_metrics(app=app)
    return app


application = get_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(application, host="localhost", port=8000)
