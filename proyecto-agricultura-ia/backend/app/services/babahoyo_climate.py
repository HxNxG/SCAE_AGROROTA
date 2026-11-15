"""Read the versioned monthly GPM IMERG series for the pilot canton."""

import csv
import math
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[4]
    / "02_clima_temperatura_y_meteorologia"
    / "GPM"
    / "IMERG_Babahoyo_2010-01_2025-09.csv"
)
EXPECTED_MONTHS = tuple(
    f"{2010 + offset // 12:04d}-{offset % 12 + 1:02d}"
    for offset in range(189)
)


def read_monthly_precipitation():
    months = []
    with SOURCE.open(encoding="utf-8-sig", newline="") as source:
        rows = csv.DictReader(source, strict=True)
        required_fields = {"mes", "codigo_dpa", "precipitacion_media_mm"}
        if not required_fields.issubset(rows.fieldnames or []):
            raise ValueError("Faltan columnas de precipitación en el CSV de Babahoyo")

        for row in rows:
            if row["codigo_dpa"] != "1201" or row["precipitacion_media_mm"] is None:
                raise ValueError("Fila incompleta o cantón incorrecto en el CSV de Babahoyo")
            precipitation = float(row["precipitacion_media_mm"])
            if not math.isfinite(precipitation) or precipitation < 0:
                raise ValueError("Precipitación inválida en el CSV de Babahoyo")
            months.append({"month": row["mes"], "precipitation_mm": precipitation})

    if tuple(row["month"] for row in months) != EXPECTED_MONTHS:
        raise ValueError("Período incompleto o desordenado en el CSV de Babahoyo")

    return {
        "source": "NASA GPM IMERG Final Run L3 mensual (GPM_3IMERGM V07B)",
        "spatial_scale": "Promedio del cantón Babahoyo (DPA 2019, código 1201), "
        "ponderado por área de intersección con celdas de 0,1°",
        "unit": "mm",
        "months": months,
    }
