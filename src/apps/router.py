from __future__ import annotations

from fastapi import APIRouter

from src.apps.feature_flag.views import feature_flag_router
from src.apps.health.views import health_check_router


api_router = APIRouter(prefix="/api")

api_router_v1 = APIRouter(prefix="/v1")

api_router_v1.include_router(feature_flag_router, tags=["FeatureFlags"])

api_router.include_router(health_check_router, tags=["Health"])

api_router.include_router(api_router_v1)
