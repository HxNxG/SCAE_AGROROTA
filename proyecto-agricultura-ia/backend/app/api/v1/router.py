from fastapi import APIRouter

from app.api.v1.endpoints import climate, parcels


router = APIRouter(prefix="/api/v1")
router.include_router(parcels.router)
router.include_router(climate.router)
