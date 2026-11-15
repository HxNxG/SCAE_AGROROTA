"""Build the Babahoyo SMAP demo layer from the verified 2025-01-01 sample.

Run with Shapely >= 2.1 and pyproj:
    python proyecto-agricultura-ia/scripts/build_babahoyo_smap.py --source PATH.csv.gz
"""

import argparse
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path

from pyproj import Transformer
from shapely import transform
from shapely.geometry import box, shape


PROJECT = Path(__file__).resolve().parents[1]
SMAP = PROJECT.parent / "01_suelos_y_salud_del_suelo/SMAP"
GEOGRAPHY = SMAP / "geografia"
MANIFEST = SMAP / "datos/prueba_2025_01_01/calidad_2025-01.json"
OUTPUT = PROJECT / "backend/app/data/babahoyo_smap_2025-01-01.json"
TIMES = tuple(f"2025-01-01T{hour:02d}:00:00Z" for hour in range(0, 24, 3))
DEPTH_COLUMNS = {"surface": "sm_surface_m3_m3", "rootzone": "sm_rootzone_m3_m3"}


def babahoyo_cells():
    """Select original EASE-Grid cells that intersect Babahoyo with positive area."""
    collection = json.loads((GEOGRAPHY / "los_rios_cantones_referencia_2019.geojson").read_text(encoding="utf-8-sig"))
    canton, = [shape(feature["geometry"]) for feature in collection["features"]
               if feature["properties"]["DPA_CANTON"] == "1201"]
    if canton.is_empty or not canton.is_valid:
        raise ValueError("Geometría inválida para Babahoyo")

    to_grid = Transformer.from_crs("EPSG:4326", "EPSG:6933", always_xy=True)
    to_wgs84 = Transformer.from_crs("EPSG:6933", "EPSG:4326", always_xy=True)
    canton = transform(canton, to_grid.transform, interleaved=False)
    mesh = json.loads((GEOGRAPHY / "malla_resumen.json").read_text(encoding="utf-8-sig"))
    half_width = mesh["dx_m"] / 2
    half_height = mesh["dy_m"] / 2
    selected = {}
    with (GEOGRAPHY / "celdas.csv").open(encoding="utf-8-sig", newline="") as stream:
        for cell in csv.DictReader(stream, strict=True):
            if cell["grid_crs"] != "EPSG:6933":
                raise ValueError("Proyección de la malla incompatible")
            x, y = float(cell["x_m"]), float(cell["y_m"])
            tile = box(x - half_width, y - half_height, x + half_width, y + half_height)
            if canton.intersection(tile).area > 0:
                selected[cell["cell_id"]] = list(to_wgs84.transform_bounds(*tile.bounds))
    if len(selected) != 28:
        raise ValueError("Número de celdas inesperado para el recorte Babahoyo DPA 2019")
    return dict(sorted(selected.items()))


def moisture(value):
    if not value.strip():
        return None
    number = float(value)
    if not math.isfinite(number) or not 0 <= number <= 1:
        raise ValueError(f"Humedad volumétrica inválida: {value}")
    return number


def read_sample(path, cell_ids, manifest):
    if hashlib.sha256(path.read_bytes()).hexdigest() != manifest["sha256"]:
        raise ValueError("El SHA-256 del CSV.GZ difiere del manifiesto verificado")
    granules = set(manifest["source_granules"])
    samples = {time: {} for time in TIMES}
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream, strict=True):
            cell_id = row["cell_id"]
            if cell_id not in cell_ids:
                continue
            time = row["time_start_utc"].replace(".000Z", "Z")
            if time not in samples or row["source_granule"] not in granules:
                raise ValueError("Intervalo u origen inesperado en la muestra verificada")
            if cell_id in samples[time]:
                raise ValueError(f"Celda duplicada: {time} {cell_id}")
            samples[time][cell_id] = {
                depth: moisture(row[column]) for depth, column in DEPTH_COLUMNS.items()
            }
    if any(set(interval) != set(cell_ids) for interval in samples.values()):
        raise ValueError("La muestra verificada debe incluir todas las huellas en los ocho intervalos")
    return {
        depth: [[samples[time][cell_id][depth] for cell_id in cell_ids] for time in TIMES]
        for depth in DEPTH_COLUMNS
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="CSV.GZ de la muestra del 1 de enero de 2025")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    cells = babahoyo_cells()
    dataset = {
        "metadata": {
            "source": "NASA/NSIDC SMAP L4 SPL4SMGP v008",
            "source_doi": "10.5067/T5RUATAQREF8",
            "source_url": "https://nsidc.org/data/spl4smgp/versions/8",
            "source_sha256": manifest["sha256"],
            "source_granules": manifest["source_granules"],
            "source_manifest": MANIFEST.relative_to(PROJECT.parent).as_posix(),
            "unit": "m³/m³",
            "resolution_km": 9,
            "native_crs": "EPSG:6933",
            "interval_hours": 3,
            "depth_cm": {"surface": [0, 5], "rootzone": [0, 100]},
            "selection": "Celdas completas con intersección de área positiva con Babahoyo DPA 2019 (1201).",
        },
        "cell_ids": list(cells),
        "bounds": list(cells.values()),
        "times": TIMES,
        "values": read_sample(args.source, cells, manifest),
    }
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(dataset, stream, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
        stream.write("\n")
    print(f"{len(TIMES)} intervalos, {len(cells)} celdas, {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
