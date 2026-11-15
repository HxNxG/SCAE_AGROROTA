import hashlib
import json
import math
import shutil
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from pathlib import Path

import numpy as np
import rasterio
import requests
from rasterio.features import geometry_mask
from rasterio.merge import merge
from rasterio.windows import Window
from shapely.geometry import box, shape
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOUNDARY = Path("01_suelos_y_salud_del_suelo/SMAP/geografia/costa_provincias_referencia_2019.geojson")
SOURCE = "https://opentopography.s3.sdsc.edu/raster/SRTM_GL1/SRTM_GL1_srtm/"
NODATA = -32768
STEP = 1 / 3600


def tile_url(cell):
    x, y = cell
    return f"{SOURCE}{'N' if y >= 0 else 'S'}{abs(y):02d}{'E' if x >= 0 else 'W'}{abs(x):03d}.tif"


def inspect_tile(url):
    response = requests.head(url, timeout=25)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return (url, int(response.headers["Content-Length"]))


def main():
    provinces = json.loads((ROOT / BOUNDARY).read_text(encoding="utf-8-sig"))["features"]
    coast = unary_union([shape(feature["geometry"]) for feature in provinces])
    padded = coast.buffer(2 * STEP)
    left, bottom, right, top = padded.bounds
    urls = [tile_url((x, y)) for x in range(math.floor(left), math.ceil(right))
            for y in range(math.floor(bottom), math.ceil(top))
            if padded.intersects(box(x, y, x + 1, y + 1))]
    with ThreadPoolExecutor(max_workers=8) as pool:
        inventory = list(pool.map(inspect_tile, urls))
    sources = [tile for tile in inventory if tile is not None]
    estimate = math.ceil((right-left)/STEP) * math.ceil((top-bottom)/STEP) * 10
    free = shutil.disk_usage(ROOT).free
    if free < estimate:
        raise RuntimeError("Espacio insuficiente")
    print(f"{len(sources)} teselas remotas; estimado local {estimate:,} B; libres {free:,} B", flush=True)
    result = HERE / "datos_costa"
    result.mkdir(exist_ok=True)
    manifest = dict(producto="SRTMGL1 v003", distribuidor="OpenTopography",
                    adquisicion="2000-02-11/2000-02-22", fecha_descarga="2026-11-14",
                    periodo_proyecto="2010-01-01/2026-11-14",
                    limites=str(BOUNDARY), datum_vertical="EGM96", crs="EPSG:4326",
                    resolucion_grados=STEP, nodata=NODATA, fuentes=sources,
                    teselas_sin_archivo=[url for url, item in zip(urls, inventory) if item is None],
                    bytes_libres=free, bytes_estimados=estimate,
                    justificacion="Un mosaico regional por variable para evaluar restricciones del terreno.")
    temp = result / "mosaico.tmp.tif"
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_TIMEOUT="35",
                      GDAL_HTTP_MAX_RETRY="3", GDAL_HTTP_RETRY_DELAY="2"), ExitStack() as stack:
        readers = [stack.enter_context(rasterio.open(url)) for url, _ in sources]
        for src in readers:
            assert src.crs.to_epsg() == 4326 and np.allclose(src.res, (STEP, STEP))
        origin = readers[0].transform
        bounds = (
            origin.c + math.floor((left-origin.c)/STEP)*STEP,
            origin.f - math.ceil((origin.f-bottom)/STEP)*STEP,
            origin.c + math.ceil((right-origin.c)/STEP)*STEP,
            origin.f - math.floor((origin.f-top)/STEP)*STEP,
        )
        merge(readers, bounds=bounds, nodata=NODATA, mem_limit=48, dst_path=temp,
              dst_kwds=dict(tiled=True, compress="deflate", predictor=2))
    print("Mosaico recortado a la envolvente; calculando pendiente y mascara.", flush=True)
    with rasterio.open(temp) as src, ExitStack() as stack:
        profile = src.profile
        profile.update(tiled=True, compress="deflate")
        paths = [result / "elevacion_m.tif", result / "pendiente_grados.tif"]
        partials = [path.with_suffix(".tmp.tif") for path in paths]
        elevation = stack.enter_context(rasterio.open(partials[0], "w", **profile))
        profile.update(dtype="float32", predictor=3)
        slope = stack.enter_context(rasterio.open(partials[1], "w", **profile))
        elevation.set_band_description(1, "Elevacion SRTMGL1 v003 (m EGM96)")
        slope.set_band_description(1, "Pendiente Horn (grados)")
        elevation.set_band_unit(1, "m")
        slope.set_band_unit(1, "degree")
        counts = [0, 0, 0]
        for row in range(0, src.height, 256):
            height = min(256, src.height-row)
            window = Window(0, row, src.width, height)
            z = src.read(1, window=Window(-1, row-1, src.width+2, height+2),
                         boundless=True, fill_value=NODATA).astype("float32")
            inside = geometry_mask([coast], out_shape=(height, src.width),
                                   transform=src.window_transform(window), invert=True)
            center = z[1:-1, 1:-1]
            neighborhood = [z[i:i+height, j:j+src.width] for i in range(3) for j in range(3)]
            valid = inside & np.logical_and.reduce([cell != NODATA for cell in neighborhood])
            a,b,c,d,_,f,g,h,i = neighborhood
            latitude = np.deg2rad(src.transform.f - (np.arange(row, row+height)+0.5)*STEP)
            eccentricity2 = 0.00669437999014
            w = np.sqrt(1 - eccentricity2*np.sin(latitude)**2)
            dx = (6378137*np.cos(latitude)/w*np.deg2rad(STEP))[:, None]
            dy = (6378137*(1-eccentricity2)/w**3*np.deg2rad(STEP))[:, None]
            angle = np.rad2deg(np.arctan(np.hypot((c+2*f+i-a-2*d-g)/(8*dx),
                                                (g+2*h+i-a-2*b-c)/(8*dy))))
            elevation.write(np.where(inside, center, NODATA).astype("int16"), 1, window=window)
            slope.write(np.where(valid, angle, NODATA).astype("float32"), 1, window=window)
            counts[0] += int(inside.sum())
            counts[1] += int((inside & (center != NODATA)).sum())
            counts[2] += int(valid.sum())
    manifest["pixeles_costa_elevacion_pendiente"] = counts
    manifest["archivos"] = []
    for partial, path in zip(partials, paths):
        partial.replace(path)
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        manifest["archivos"].append(dict(nombre=path.name, bytes=path.stat().st_size, sha256=digest))
    (result / "manifiesto.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    temp.unlink()
    print(counts, flush=True)


if __name__ == "__main__":
    main()
