"""Geographic validation for a pilot parcel represented by one point."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.parcel_geography import validate_point


router = APIRouter(prefix="/parcels", tags=["parcels"])


class ParcelPoint(BaseModel):
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)


@router.post("/validate")
def validate_parcel_point(point: ParcelPoint):
    try:
        return validate_point(point.longitude, point.latitude)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
