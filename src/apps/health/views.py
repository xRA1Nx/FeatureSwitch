from __future__ import annotations

from fastapi import APIRouter, Response
from starlette import status
from starlette.responses import JSONResponse

from src.apps.health.logic.facades import app__is_healthy, app__readiness_result
from src.server.redis import redis_cache


health_check_router = APIRouter()


@health_check_router.get("/health")
@redis_cache(ttl=5)
async def liveness_probe() -> Response:
    is_app_alive = await app__is_healthy()
    if is_app_alive:
        return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_200_OK)
    return JSONResponse(content="undefined_error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@health_check_router.get("/ready")
@redis_cache(ttl=5)
async def readiness_probe() -> JSONResponse:
    readiness_result = await app__readiness_result()
    if readiness_result.is_ok:
        return JSONResponse(content={"status": "ok"}, status_code=200)
    readiness_result_data = readiness_result.model_dump()["errors"]
    return JSONResponse(content=readiness_result_data, status_code=503)
