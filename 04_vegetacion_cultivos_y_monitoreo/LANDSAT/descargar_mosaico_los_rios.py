"""Download a cloud-masked HLS true-color mosaic for Los Ríos."""
import argparse
import json
import math
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import planetary_computer as pc
import rasterio
import requests
from rasterio.enums import ColorInterp
from rasterio.features import geometry_mask
from rasterio.transform import from_origin
from rasterio.vrt import WarpedVRT
from shapely.geometry import shape
from shapely.ops import unary_union

from descargar_piloto_hls import API

ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = ROOT / "01_suelos_y_salud_del_suelo/SMAP/geografia/los_rios_cantones_referencia_2019.geojson"
OUTPUT = Path(__file__).resolve().parent / "mosaico_los_rios_rgb.tif"
PIXEL = 1 / 3600


def read_band(item, name, grid, nodata):
    url = pc.sign(item["assets"][name]["href"])
    with rasterio.open(url) as source:
        with WarpedVRT(source, **grid, nodata=nodata) as vrt:
            return vrt.read(1)


def main(ampliar=False):
    features = json.loads(BOUNDARY.read_text(encoding="utf-8-sig"))["features"]
    province = unary_union([shape(feature["geometry"]).buffer(0) for feature in features])
    west, south, east, north = province.bounds
    grid = dict(
        crs="EPSG:4326", transform=from_origin(west, north, PIXEL, PIXEL),
        width=math.ceil((east - west) / PIXEL), height=math.ceil((north - south) / PIXEL),
    )
    inside = geometry_mask([province], (grid["height"], grid["width"]), grid["transform"], invert=True)
    pending = inside.copy()
    image = np.zeros((4, *inside.shape), dtype=np.uint8)

    today = date.today()
    period = f"{today - timedelta(days=365)}T00:00:00Z/{today}T23:59:59Z"
    search_area = province
    used = []
    if ampliar:
        with rasterio.open(OUTPUT) as previous:
            if previous.transform != grid["transform"] or previous.shape != inside.shape:
                raise ValueError("El mosaico existente usa otra cuadrícula.")
            image = previous.read()
        pending &= image[3] == 0
        used = json.loads(OUTPUT.with_suffix(".json").read_text(encoding="utf-8"))["escenas"]
        search_area = unary_union([
            shape(feature["geometry"]).buffer(0) for feature in features
            if feature["properties"]["DPA_DESCAN"] in {"BUENA FE", "VALENCIA"}
        ])
        period = f"{today - timedelta(days=3 * 365)}T00:00:00Z/{today}T23:59:59Z"
    coverage = 100 * (1 - pending.sum() / inside.sum())
    response = requests.get(API, params={
        "collections": "hls2-s30,hls2-l30", "bbox": ",".join(map(str, search_area.bounds)),
        "datetime": period, "sortby": "+eo:cloud_cover,-datetime", "limit": 32 if ampliar else 100,
    }, timeout=45)
    response.raise_for_status()
    items = response.json()["features"]
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_TIMEOUT="25",
                      GDAL_HTTP_MAX_RETRY="2", CPL_LOG="NUL"):
        for item in items:
            if not item["geometry"] or not search_area.intersects(shape(item["geometry"])):
                continue
            try:
                qa = read_band(item, "Fmask", grid, 255)
                valid = pending & ((qa & 31) == 0)
                if not valid.any():
                    continue
                rgb = np.stack([read_band(item, band, grid, -9999) for band in ("B04", "B03", "B02")])
            except (requests.RequestException, rasterio.errors.RasterioError) as error:
                print(item["id"], type(error).__name__, flush=True)
                continue
            valid &= (rgb != -9999).all(axis=0)
            count = int(valid.sum())
            if not count:
                continue
            image[:3, valid] = np.rint(255 * np.sqrt(np.clip(rgb[:, valid] / 3500, 0, 1)))
            image[3, valid] = 255
            pending[valid] = False
            used.append(dict(escena=item["id"], fecha=item["properties"]["datetime"], pixeles=count))
            coverage = 100 * (1 - pending.sum() / inside.sum())
            print(f'{item["id"]}: {coverage:.2f}% de Los Ríos', flush=True)
            if coverage >= 99.9:
                break

    if not used:
        raise RuntimeError("No se encontraron escenas HLS con píxeles válidos.")
    temporary = OUTPUT.with_suffix(".tmp")
    with rasterio.open(temporary, "w", **grid, driver="GTiff", dtype="uint8", count=4,
                       compress="deflate", tiled=True, photometric="RGB") as destination:
        destination.write(image)
        destination.colorinterp = (ColorInterp.red, ColorInterp.green, ColorInterp.blue, ColorInterp.alpha)
    temporary.replace(OUTPUT)
    OUTPUT.with_suffix(".json").write_text(json.dumps({
        "intervalo": period, "cobertura_porcentaje": coverage, "escenas": used,
    }, indent=2), encoding="utf-8")
    print(f"Mosaico guardado en {OUTPUT}", flush=True)
    return coverage


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ampliar", action="store_true",
                        help="Rellenar huecos del mosaico existente con escenas adicionales del norte.")
    args = parser.parse_args()
    if args.ampliar:
        main(ampliar=True)
    elif main() < 99.9:
        main(ampliar=True)
