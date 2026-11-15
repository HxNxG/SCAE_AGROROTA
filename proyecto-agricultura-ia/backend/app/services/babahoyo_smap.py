"""Serve the verified three-hour SMAP sample for Babahoyo."""

import json
import math
from functools import cache
from pathlib import Path


DATA = Path(__file__).resolve().parents[1] / "data" / "babahoyo_smap_2025-01-01.json"
TIMES = tuple(f"2025-01-01T{hour:02d}:00:00Z" for hour in range(0, 24, 3))


@cache
def read_sample():
    sample = json.loads(DATA.read_text(encoding="utf-8"))
    metadata = sample["metadata"]
    bounds = sample["bounds"]
    values = sample["values"]
    if metadata["unit"] != "m³/m³" or metadata["resolution_km"] != 9:
        raise ValueError("Unidad o resolución incorrecta en la muestra SMAP")
    if tuple(sample["times"]) != TIMES or len(bounds) != 28 or len(set(map(tuple, bounds))) != 28:
        raise ValueError("Intervalos o celdas repetidos o faltantes en la muestra SMAP")
    for west, south, east, north in bounds:
        if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
            raise ValueError("Límites inválidos en la malla SMAP de Babahoyo")
    for depth in ("surface", "rootzone"):
        if len(values[depth]) != len(TIMES) or any(
            len(row) != len(bounds)
            or any(value is not None and (not math.isfinite(value) or not 0 <= value <= 1) for value in row)
            for row in values[depth]
        ):
            raise ValueError(f"Serie inválida en la muestra SMAP: {depth}")
    return metadata, bounds, values


def read_moisture_frames(depth):
    metadata, bounds, values = read_sample()
    return {
        "source": metadata["source"],
        "unit": metadata["unit"],
        "resolution_km": metadata["resolution_km"],
        "frames": [
            {
                "time": time,
                "cells": [
                    {"bounds": extent, "value": value}
                    for extent, value in zip(bounds, row, strict=True)
                ],
            }
            for time, row in zip(TIMES, values[depth], strict=True)
        ],
    }
