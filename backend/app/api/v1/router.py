from fastapi import APIRouter, Depends
from app.api.v1 import roads, shipments, incidents, routes, alerts, auth
from app.api.dependencies import get_current_user

api_router = APIRouter()

# Public routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Protected routers (require authentication)
api_router.include_router(
    roads.router,
    prefix="/roads",
    tags=["roads"],
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    shipments.router,
    prefix="/shipments",
    tags=["shipments"],
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    routes.router,
    prefix="/routes",
    tags=["routes"],
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    incidents.router,
    prefix="/incidents",
    tags=["incidents"],
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    alerts.router,
    prefix="/alerts",
    tags=["alerts"],
    dependencies=[Depends(get_current_user)]
)