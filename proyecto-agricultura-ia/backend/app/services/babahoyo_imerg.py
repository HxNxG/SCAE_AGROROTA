"""Serve the original IMERG cells intersecting the Babahoyo pilot canton."""

import json
import math
from functools import cache
from pathlib import Path

from app.services.babahoyo_climate import EXPECTED_MONTHS


DATA = Path(__file__).resolve().parents[1] / "data" / "babahoyo_imerg_cells.json"


@cache
def read_layer():
    with DATA.open(encoding="utf-8") as stream:
        layer = json.load(stream)

    metadata = layer["metadata"]
    bounds = layer["bounds"]
    months = layer["months"]
    if metadata["unit"] != "mm" or metadata["resolution_degrees"] != 0.1:
        raise ValueError("Unidad o resolución incorrecta en la capa IMERG")
    if tuple(months) != EXPECTED_MONTHS or not bounds or len(set(map(tuple, bounds))) != len(bounds):
        raise ValueError("Meses o celdas repetidos o faltantes en la capa IMERG")
    if any(
        len(row) != len(bounds)
        or any(value is not None and (not math.isfinite(value) or value < 0) for value in row)
        for row in months.values()
    ):
        raise ValueError("Serie por celda inválida en la capa IMERG")
    return metadata["source"], bounds, months


def read_precipitation_cells(month: str):
    source, bounds, months = read_layer()
    values = months.get(month)
    return {
        "month": month,
        "unit": "mm",
        "source": source,
        "cells": [
            {"bounds": extent, "precipitation_mm": value}
            for extent, value in zip(bounds, values, strict=True)
        ] if values is not None else [],
    }
