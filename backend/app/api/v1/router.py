from fastapi import APIRouter
from app.api.v1 import roads, incidents, routes, shipments  # health, roads, shipments

api_router = APIRouter()
#api_router.include_router(health.router, tags=["health"])
api_router.include_router(roads.router, prefix="/roads", tags=["roads"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
api_router.include_router(routes.router, prefix="/routes", tags=["routes"])
api_router.include_router(shipments.router, prefix="/shipments", tags=["shipments"])