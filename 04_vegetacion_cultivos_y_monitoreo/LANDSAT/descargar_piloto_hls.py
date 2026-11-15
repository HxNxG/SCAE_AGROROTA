import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
import planetary_computer as pc
import rasterio
import requests
from rasterio.windows import Window
from rasterio.warp import transform
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = Path("01_suelos_y_salud_del_suelo/SMAP/geografia/costa_provincias_referencia_2019.geojson")
OUT = Path(__file__).resolve().parent / "piloto_hls_qa"
PERIOD = "2010-01-01T00:00:00Z/2026-11-14T23:59:59Z"
API = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
SIDE = 33
NAMES = ["azul", "verde", "rojo", "nir", "swir1", "swir2", "Fmask", "NDVI", "EVI2", "NDMI"]


def search(collection, geometry, order, limit=1):
    response = requests.get(API, params={
        "collections": collection, "datetime": PERIOD,
        "intersects": json.dumps(geometry.__geo_interface__),
        "sortby": order, "limit": limit,
    }, timeout=45)
    response.raise_for_status()
    return response.json()["features"]


def clip(item, point, bands, destination):
    arrays = []
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_TIMEOUT="30", GDAL_HTTP_MAX_RETRY="2"):
        for band in ["Fmask", *bands[:-1]]:
            with rasterio.open(pc.sign(item["assets"][band]["href"])) as src:
                x, y = transform("EPSG:4326", src.crs, [point.x], [point.y])
                row, col = src.index(x[0], y[0])
                window = Window(col - SIDE//2, row - SIDE//2, SIDE, SIDE)
                arrays.append(src.read(1, window=window, boundless=True,
                                       fill_value=255 if band == "Fmask" else -9999))
                if band == "Fmask" and not np.any((arrays[0] & 63) == 0):
                    return 0
                profile = dict(driver="GTiff", crs=src.crs, transform=src.window_transform(window),
                               height=SIDE, width=SIDE, count=len(NAMES), dtype="float32",
                               nodata=-9999, compress="deflate")

    qa = arrays[0]
    valid = ((qa & 63) == 0) & np.all(np.asarray(arrays[1:]) != -9999, axis=0)
    if not valid.any():
        return 0
    values = np.where(valid, np.asarray(arrays[1:], dtype="float32") * 0.0001, -9999)

    def ratio(numerator, denominator):
        result = np.full(valid.shape, -9999, dtype="float32")
        return np.divide(numerator, denominator, out=result, where=valid & (denominator != 0))

    _, _, red, nir, swir, _ = values
    output = [*values, qa, ratio(nir-red, nir+red),
              ratio(2.5*(nir-red), nir+2.4*red+1), ratio(nir-swir, nir+swir)]
    temporary = destination.with_suffix(".tmp")
    with rasterio.open(temporary, "w", **profile) as dst:
        for index, (name, data) in enumerate(zip(NAMES, output), 1):
            dst.write(data.astype("float32"), index)
            dst.set_band_description(index, name)
    temporary.replace(destination)
    return int(valid.sum())


def main():
    provinces = json.loads((ROOT / BOUNDARY).read_text(encoding="utf-8-sig"))["features"]
    free = shutil.disk_usage(ROOT).free
    estimated = len(provinces) * 2 * (SIDE**2 * len(NAMES) * 4 + 16384)
    if free < estimated:
        raise RuntimeError("Espacio insuficiente")
    OUT.mkdir(exist_ok=True)
    manifest = {
        "fecha_ejecucion": "2026-11-14", "intervalo_solicitado": PERIOD,
        "catalogo": API, "limites_EPSG_4326": str(BOUNDARY),
        "justificacion": "Verificar bandas, calidad e indices con un recorte interior por provincia y sensor.",
        "bytes_libres_antes": free, "bytes_estimados": estimated, "recortes": [], "errores": [],
    }
    for province in provinces:
        geometry = shape(province["geometry"])
        point = geometry.representative_point()
        for sensor, nir in (("l30", "B05"), ("s30", "B8A")):
            record = {"provincia": province["properties"], "lon": point.x, "lat": point.y, "sensor": sensor}
            try:
                items = search(f"hls2-{sensor}", point, "-datetime", limit=35)
                oldest = search(f"hls2-{sensor}", point, "+datetime")
                if not items or not oldest:
                    raise RuntimeError("Sin escenas en el punto")
                record["ultima_escena_catalogo"] = items[0]["properties"]["datetime"]
                for item in items:
                    destination = OUT / f"{len(manifest['recortes']):02d}_{item['id']}.tif"
                    try:
                        count = clip(item, point, ["B02", "B03", "B04", nir, "B06" if sensor == "l30" else "B11",
                                                   "B07" if sensor == "l30" else "B12", "Fmask"], destination)
                    except rasterio.errors.RasterioIOError:
                        continue
                    if count:
                        break
                else:
                    raise RuntimeError("Sin pixeles validos en escenas accesibles")
                 
                record.update(primera_escena=oldest[0]["properties"]["datetime"],
                              escena=item["id"], fecha=item["properties"]["datetime"],
                              archivo=destination.name, pixeles_validos=count,
                              bytes=destination.stat().st_size,
                              sha256=hashlib.sha256(destination.read_bytes()).hexdigest())
                manifest["recortes"].append(record)
                print(destination.name, count, flush=True)
            except (requests.RequestException, rasterio.errors.RasterioError, RuntimeError) as error:
                # Exception messages from remote readers may contain signed asset URLs.
                record["error"] = str(error) if isinstance(error, RuntimeError) else type(error).__name__
                manifest["errores"].append(record)
                print(sensor, record["error"], flush=True)
            (OUT / "manifiesto.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
