"""Descarga y verifica capas SoilGrids 2.0 para la Costa ecuatoriana."""

import hashlib
import json
import math
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_geom
from shapely.geometry import shape
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
BOUNDARY = HERE.parent / "SMAP/geografia/costa_provincias_referencia_2019.geojson"
OUTPUT = HERE / "soilgrids_2_costa_dpa2019"
PROJECTION = "+proj=igh +datum=WGS84 +units=m +no_defs"
SERVICE = "https://files.isric.org/soilgrids/latest/data"
DEPTHS = ("0-5", "5-15", "15-30", "30-60", "60-100", "100-200")
STATISTICS = ("mean", "Q0.05", "Q0.5", "Q0.95")
PROPERTIES = {
    "phh2o": ("pH", 10),
    "sand": ("g/kg", 1),
    "silt": ("g/kg", 1),
    "clay": ("g/kg", 1),
    "soc": ("g/kg", 10),
    "nitrogen": ("g/kg", 100),
}


def download(job, geometries):
    variable, depth, statistic = job
    coverage = f"{variable}_{depth}cm_{statistic}"
    target = OUTPUT / f"{coverage}.tif"
    metadata = target.with_suffix(".json")
    if metadata.exists() and target.exists():
        previous = json.loads(metadata.read_text())
        if hashlib.sha256(target.read_bytes()).hexdigest() == previous["sha256"]:
            return coverage
    url = f"{SERVICE}/{variable}/{coverage}.vrt"
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_TIMEOUT="60",
                      GDAL_HTTP_MAX_RETRY="3", GDAL_HTTP_RETRY_DELAY="2"):
        return extract(coverage, variable, url, target, metadata, geometries)


def extract(coverage, variable, url, target, metadata, geometries):
    with rasterio.open(f"/vsicurl/{url}") as source:
        if source.res != (250, 250) or source.count != 1 or source.nodata is None:
            raise ValueError(f"Cuadrícula o nodata inesperado: {coverage}")
        data, transform = mask(source, geometries, filled=False, crop=True)
        valid = data.compressed()
        if not valid.size:
            raise ValueError(f"Sin píxeles válidos: {coverage}")
        temporary = target.with_suffix(".part.tif")
        profile = source.profile | {
            "driver": "GTiff", "compress": "deflate", "height": data.shape[1],
            "width": data.shape[2], "transform": transform,
        }
        with rasterio.open(temporary, "w", **profile) as output:
            output.write(data.filled(source.nodata))
            bounds = list(output.bounds)
        temporary.replace(target)
        unit, divisor = PROPERTIES[variable]
        record = {
            "query": url, "coverage": coverage, "nodata": source.nodata,
            "unit": unit, "divide_stored_value_by": divisor,
            "valid_pixels": int(valid.size), "min": int(valid.min()), "max": int(valid.max()),
            "crs_wkt": source.crs.to_wkt(), "bounds": bounds,
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        }
    metadata.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return coverage


def main():
    features = json.loads(BOUNDARY.read_text(encoding="utf-8"))["features"]
    geometries = [transform_geom("EPSG:4326", PROJECTION, f["geometry"]) for f in features]
    bounds = unary_union([shape(geometry) for geometry in geometries]).bounds
    left, bottom, right, top = [
        rounding(value / 250) * 250
        for value, rounding in zip(bounds, (math.floor, math.floor, math.ceil, math.ceil))
    ]
    bounds = left, bottom, right, top
    jobs = [(v, d, s) for v in PROPERTIES for d in DEPTHS for s in STATISTICS]
    estimate = ((right - left) // 250 + 2) * ((top - bottom) // 250 + 2) * 2 * len(jobs)
    free = shutil.disk_usage(HERE).free
    if free < estimate * 2:
        raise OSError("Espacio insuficiente para los rásteres y archivos temporales")
    OUTPUT.mkdir(exist_ok=True)
    plan = {
        "product": "ISRIC SoilGrids 250 m v2.0", "license": "CC BY 4.0",
        "requested_2026-11-14": len(jobs), "estimated_uncompressed_bytes": estimate,
        "free_bytes_before_download": free, "geographic_reference": str(BOUNDARY.relative_to(HERE.parent)),
        "purpose": "Caracterizar pH, textura, carbono y nitrógeno por profundidad para evaluar aptitud del suelo.",
        "estimated_rectangle": bounds, "resolution_m": 250,
        "temporal_coverage": "Predicción edáfica estática, sin serie anual",
    }
    (OUTPUT / "plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    failures = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        pending = {pool.submit(download, job, geometries): job for job in jobs}
        for future in as_completed(pending):
            try:
                print(future.result(), flush=True)
            except Exception as error:
                failures.append(pending[future])
                print(f"{pending[future]}: {error}", flush=True)
    if failures:
        raise SystemExit(f"Fallaron {len(failures)} de {len(jobs)} capas")


if __name__ == "__main__":
    main()
