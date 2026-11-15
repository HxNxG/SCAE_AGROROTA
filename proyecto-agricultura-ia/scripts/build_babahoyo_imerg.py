"""Recorta la capa mensual original. Ejecutar con Python y Shapely >= 2.

    python proyecto-agricultura-ia/scripts/build_babahoyo_imerg.py
"""

import csv
import hashlib
import json
import math
from pathlib import Path

from shapely.geometry import box, shape


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
GPM = REPO / "02_clima_temperatura_y_meteorologia/GPM"
BOUNDARY = REPO / "01_suelos_y_salud_del_suelo/SMAP/geografia/los_rios_cantones_referencia_2019.geojson"
OUTPUT = PROJECT / "backend/app/data/babahoyo_imerg_cells.json"
SOURCES = (
    (GPM / "IMERG_Costa_2010-01_2014-12.csv", 0, 60),
    (GPM / "IMERG_Costa_2015-01_2025-09.csv", 60, 189),
)
MONTHS = tuple(f"{2010 + i // 12:04d}-{i % 12 + 1:02d}" for i in range(189))
HEADER = ["time", "latitude", "longitude", "precipitation", "precipitationQualityIndex", "randomError"]
UNITS = ["UTC", "degrees_north", "degrees_east", "mm", "none", "mm"]

# Enteros en centésimas de grado: centros documentados de la malla Costa.
# Evitan artefactos de float del distribuidor y bordes distintos entre vecinos.
GRID = {(lon, lat) for lon in range(-8105, -7844, 10) for lat in range(-385, 146, 10)}


def cell_bounds(lon, lat):
    return [(lon - 5) / 100, (lat - 5) / 100, (lon + 5) / 100, (lat + 5) / 100]


def center(value):
    degrees = float(value)
    hundredths = round(degrees * 100)
    if abs(degrees - hundredths / 100) > 0.00001:
        raise ValueError(f"Centro fuera de la malla nominal: {value}")
    return hundredths


def precipitation(value):
    if value.strip().lower() in {"", "nan", "na", "null"}:
        return None
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"Precipitación inesperada: {value}")
    return number


def read_source(path, months, selected):
    by_time = {f"{month}-01T00:00:00Z": month for month in months}
    seen = {month: set() for month in months}
    values = {month: {} for month in months}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.reader(stream, strict=True)
        if next(rows, None) != HEADER or next(rows, None) != UNITS:
            raise ValueError(f"Encabezados o unidades inesperados en {path.name}")
        for timestamp, lat, lon, rain, _, _ in rows:
            month = by_time.get(timestamp)
            if month is None:
                raise ValueError(f"Fecha inesperada en {path.name}: {timestamp}")
            cell = (center(lon), center(lat))
            if cell not in GRID or cell in seen[month]:
                raise ValueError(f"Celda fuera de malla o duplicada: {month} {cell}")
            seen[month].add(cell)
            if cell in selected:
                values[month][cell] = precipitation(rain)
    if any(not cells for cells in seen.values()):
        raise ValueError(f"Faltan meses completos en {path.name}")
    # Una celda ausente en un mes cubierto queda nula; no se interpola.
    return {month: [data.get(cell) for cell in selected] for month, data in values.items()}


def provenance(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for line in stream:
            digest.update(line[:-2] + b"\n" if line.endswith(b"\r\n") else line)
    return {"path": path.relative_to(REPO).as_posix(), "sha256_lf": digest.hexdigest()}


def compact_json(data):
    return json.dumps(data, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def main():
    features = json.loads(BOUNDARY.read_text(encoding="utf-8"))["features"]
    canton, = [shape(f["geometry"]) for f in features if f["properties"]["DPA_CANTON"] == "1201"]
    if canton.is_empty or not canton.is_valid:
        raise ValueError("Geometría inválida para Babahoyo (DPA 1201)")
    selected = tuple(cell for cell in sorted(GRID) if canton.intersection(box(*cell_bounds(*cell))).area > 0)
    if not selected:
        raise ValueError("La malla no intersecta el cantón")

    monthly = {}
    for source, start, stop in SOURCES:
        monthly.update(read_source(source, MONTHS[start:stop], selected))
    if tuple(monthly) != MONTHS:
        raise ValueError("Los tramos de origen no cubren exactamente el período")

    metadata = {
        "source": "NASA GPM IMERG Final Run L3 mensual (GPM_3IMERGM V07B)",
        "distributor": "University of South Florida ERDDAP (IMERG_monthly_global_precip)",
        "resolution_degrees": 0.1,
        "unit": "mm",
        "crs": "WGS84 (longitud, latitud)",
        "selection": "Intersección de área positiva con DPA 2019 EEQ, cantón 1201. Se conservan las celdas completas.",
        "inputs": [provenance(path) for path, _, _ in SOURCES] + [provenance(BOUNDARY)],
    }
    bounds = [cell_bounds(*cell) for cell in selected]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(f'{{\n"metadata":{compact_json(metadata)},\n"bounds":{compact_json(bounds)},\n"months":{{\n')
        stream.write(",\n".join(f"{compact_json(month)}:{compact_json(values)}" for month, values in monthly.items()))
        stream.write("\n}\n}\n")

    missing = sum(value is None for values in monthly.values() for value in values)
    print(f"{len(monthly)} meses ({MONTHS[0]} a {MONTHS[-1]}), {len(selected)} celdas, "
          f"{missing} valores nulos, {OUTPUT.stat().st_size} bytes: {OUTPUT.name}")


if __name__ == "__main__":
    main()
