"""Historical climate for the Babahoyo pilot area."""

import csv
import logging
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.babahoyo_climate import read_monthly_precipitation
from app.services.babahoyo_imerg import read_precipitation_cells
from app.services.babahoyo_modis import read_temperature_frames
from app.services.babahoyo_smap import read_moisture_frames


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/climate", tags=["climate"])


class PrecipitationCell(BaseModel):
    """Celda IMERG de 0,1° × 0,1° en WGS84."""

    bounds: tuple[float, float, float, float]  # oeste, sur, este, norte
    precipitation_mm: float | None


class PrecipitationCells(BaseModel):
    month: str
    unit: Literal["mm"]
    source: str
    cells: list[PrecipitationCell]


class ClimateGridCell(BaseModel):
    bounds: tuple[float, float, float, float]  # oeste, sur, este, norte
    value: float | None


class ClimateGridFrame(BaseModel):
    time: str
    cells: list[ClimateGridCell]


class MoistureSample(BaseModel):
    source: str
    unit: Literal["m³/m³"]
    resolution_km: Literal[9]
    frames: list[ClimateGridFrame]


class SurfaceTemperatureSeries(BaseModel):
    source: str
    unit: Literal["°C"]
    resolution_degrees: Literal[0.05]
    frames: list[ClimateGridFrame]


@router.get("/babahoyo/moisture", response_model=MoistureSample)
def get_babahoyo_moisture(depth: Literal["surface", "rootzone"]):
    """Entrega la muestra piloto del 1 de enero de 2025, con inicio UTC por fotograma."""
    try:
        return read_moisture_frames(depth)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        logger.exception("No se pudo leer la muestra de humedad de Babahoyo")
        raise HTTPException(status_code=503, detail="La muestra de humedad de Babahoyo no está disponible") from exc


@router.get("/babahoyo/cells", response_model=PrecipitationCells)
def get_babahoyo_precipitation_cells(
    month: Annotated[str, Query(pattern=r"^[0-9]{4}-(0[1-9]|1[0-2])$", description="Mes YYYY-MM")],
):
    """Entrega las celdas completas que intersectan Babahoyo para el mes solicitado."""
    if month.startswith("0000-"):
        raise HTTPException(status_code=422, detail="Año inválido")
    try:
        return read_precipitation_cells(month)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        logger.exception("No se pudo leer la capa de precipitación de Babahoyo")
        raise HTTPException(
            status_code=503,
            detail="La capa de precipitación de Babahoyo no está disponible",
        ) from exc


@router.get("/babahoyo/temperature", response_model=SurfaceTemperatureSeries)
def get_babahoyo_temperature(band: Literal["day", "night"]):
    """Entrega los 202 compuestos mensuales de temperatura superficial MODIS."""
    try:
        return read_temperature_frames(band)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        logger.exception("No se pudo leer la temperatura superficial de Babahoyo")
        raise HTTPException(
            status_code=503, detail="La serie MODIS de temperatura superficial no está disponible",
        ) from exc


@router.get("/babahoyo/monthly")
def get_babahoyo_monthly_precipitation():
    try:
        return read_monthly_precipitation()
    except (OSError, ValueError, csv.Error) as exc:
        logger.exception("No se pudo leer la serie de precipitación de Babahoyo")
        raise HTTPException(
            status_code=503,
            detail="La serie histórica de precipitación de Babahoyo no está disponible",
        ) from exc
