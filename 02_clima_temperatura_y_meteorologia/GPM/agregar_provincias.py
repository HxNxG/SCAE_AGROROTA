"""Pondera IMERG por el área geodésica de intersección con cada provincia."""

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

from pyproj import Geod
from shapely import box, orient_polygons
from shapely.geometry import shape

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "IMERG_Costa_2015-01_2025-09.csv"
BOUNDARY = HERE.parents[1] / "01_suelos_y_salud_del_suelo/SMAP/geografia/costa_provincias_referencia_2019.geojson"
OUT = HERE / "IMERG_provincias_2015-01_2025-09.csv"
CANTONS = BOUNDARY.with_name("los_rios_cantones_referencia_2019.geojson")
CANTON_OUT = HERE / "IMERG_cantones_los_rios_2015-01_2025-09.csv"
VARIABLES = ("precipitation", "precipitationQualityIndex", "randomError")


def main(boundary=BOUNDARY, output=OUT, code_field="DPA_PROVIN", name_field="DPA_DESPRO",
         source=SOURCE, expected_months=129):
    provinces = json.loads(boundary.read_text(encoding="utf-8"))["features"]
    data = defaultdict(dict)
    with source.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        next(reader)  # Fila de unidades publicada por ERDDAP.
        for row in reader:
            month = row["time"][:7]
            cell = (round(float(row["longitude"]), 2), round(float(row["latitude"]), 2))
            if cell in data[month]:
                raise ValueError(f"Celda duplicada: {month} {cell}")
            values = tuple(float(row[column]) for column in VARIABLES)
            if not all(math.isfinite(value) and value >= 0 for value in values):
                raise ValueError(f"Valor inválido: {month} {cell}")
            data[month][cell] = values
    grid = set(next(iter(data.values())))
    if len(data) != expected_months or len(grid) != 1458 or any(set(rows) != grid for rows in data.values()):
        raise ValueError("La cobertura mensual de origen no corresponde al recorte documentado")

    geod = Geod(ellps="WGS84")
    records = []
    for feature in provinces:
        code = feature["properties"][code_field]
        name = feature["properties"][name_field]
        province = shape(feature["geometry"])
        area = geod.geometry_area_perimeter(orient_polygons(province))[0]
        weights = {}
        for lon, lat in sorted(grid):
            cell = box(lon - .05, lat - .05, lon + .05, lat + .05)
            if province.intersects(cell):
                overlap = orient_polygons(province.intersection(cell))
                weight = geod.geometry_area_perimeter(overlap)[0]
                if weight > 0:
                    weights[lon, lat] = weight
        covered = sum(weights.values())
        if not 0.99 <= covered / area <= 1.001:
            raise ValueError(f"Cobertura inesperada de {name}: {covered / area:.4%}")
        for month, rows in sorted(data.items()):
            averages = [
                sum(weight * rows[cell][index] for cell, weight in weights.items()) / covered
                for index in range(len(VARIABLES))
            ]
            records.append([month, code, name, len(weights), covered / 1e6, covered / area, *averages])
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        name_column = "canton" if code_field == "DPA_CANTON" else "provincia"
        writer.writerow(["mes", "codigo_dpa", name_column, "celdas", "area_intersectada_km2",
                         "fraccion_cubierta", "precipitacion_media_mm", "indice_calidad_medio",
                         "error_aleatorio_medio_por_celda_mm"])
        writer.writerows(sorted(records))
    for path in (source, boundary, output):
        print(path.name, hashlib.sha256(path.read_bytes()).hexdigest())
    print(len(records), min(row[5] for row in records), max(row[5] for row in records))


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    period = "2010-01_2014-12" if "--2010-2014" in args else "2015-01_2025-09"
    source = HERE / f"IMERG_Costa_{period}.csv"
    options = {"source": source, "expected_months": 60 if "--2010-2014" in args else 129}
    if "--los-rios" in args:
        main(CANTONS, HERE / f"IMERG_cantones_los_rios_{period}.csv", "DPA_CANTON", "DPA_DESCAN", **options)
    elif "--cantones" in args:
        main(BOUNDARY.with_name("costa_cantones_referencia_2019.geojson"),
             HERE / f"IMERG_cantones_costa_{period}.csv", "DPA_CANTON", "DPA_DESCAN", **options)
    else:
        main(output=HERE / f"IMERG_provincias_{period}.csv", **options)
