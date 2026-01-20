from __future__ import annotations

from fastapi import APIRouter

from src.apps.health.views import health_check_router


api_router = APIRouter(prefix="/api")

api_router_v1 = APIRouter(prefix="/v1")

api_router.include_router(health_check_router)
