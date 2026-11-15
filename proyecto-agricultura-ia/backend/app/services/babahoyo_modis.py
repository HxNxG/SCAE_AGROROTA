"""Serve the versioned MODIS Terra land surface temperature for Babahoyo."""

import json
import math
from functools import cache
from pathlib import Path


DATA = Path(__file__).resolve().parents[1] / "data" / "babahoyo_modis_temperature.json"
TIMES = tuple(f"{year:04d}-{month:02d}" for year in range(2010, 2027)
              for month in range(1, (11 if year == 2026 else 13)))


@cache
def read_series():
    series = json.loads(DATA.read_text(encoding="utf-8"))
    metadata = series["metadata"]
    bounds = series["bounds"]
    values = series["values"]
    if metadata["unit"] != "°C" or metadata["resolution_degrees"] != 0.05:
        raise ValueError("Unidad o resolución incorrecta en la serie MODIS")
    if tuple(series["times"]) != TIMES or len(bounds) != 61 or len(set(map(tuple, bounds))) != 61:
        raise ValueError("Meses o celdas repetidos o faltantes en la serie MODIS")
    for west, south, east, north in bounds:
        if not math.isclose(east - west, 0.05) or not math.isclose(north - south, 0.05):
            raise ValueError("Tamaño incompatible con la malla MODIS de 0,05°")
    for band in ("day", "night"):
        if len(values[band]) != len(TIMES) or any(
            len(row) != len(bounds) or any(value is not None and not math.isfinite(value) for value in row)
            for row in values[band]
        ):
            raise ValueError(f"Serie inválida en el recorte MODIS: {band}")
    return metadata, bounds, values


def read_temperature_frames(band):
    metadata, bounds, values = read_series()
    return {
        "source": metadata["source"],
        "unit": metadata["unit"],
        "resolution_degrees": metadata["resolution_degrees"],
        "frames": [
            {
                "time": time,
                "cells": [
                    {"bounds": extent, "value": value}
                    for extent, value in zip(bounds, row, strict=True)
                ],
            }
            for time, row in zip(TIMES, values[band], strict=True)
        ],
    }
