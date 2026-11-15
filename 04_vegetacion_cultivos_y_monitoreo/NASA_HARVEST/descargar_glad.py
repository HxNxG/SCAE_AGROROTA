"""Recorta los GeoTIFF oficiales de GLAD mediante lecturas HTTP por rango."""
import hashlib
import json
import shutil
from contextlib import ExitStack
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import bounds, geometry_mask
from rasterio.merge import merge

ROOT = Path(__file__).resolve().parent
AOI = ROOT.parents[1] / "01_suelos_y_salud_del_suelo/SMAP/geografia/costa_union_referencia_2019.geojson"
BASE = "https://gladxfer.umd.edu/Potapov/Global_Crop/Data/"
EPOCHS = {2011: "2008-2011", 2015: "2012-2015", 2019: "2016-2019"}
NODATA = 255


def main():
    geometry = json.loads(AOI.read_text(encoding="utf-8-sig"))["features"][0]["geometry"]
    extent = bounds(geometry)
    resolution = 0.00025
    estimated = int(((extent[2] - extent[0]) / resolution + 2)
                    * ((extent[3] - extent[1]) / resolution + 2))
    free = shutil.disk_usage(ROOT).free
    print(f"Estimación por época, sin compresión: {estimated} bytes. Libres: {free}.", flush=True)
    if free < estimated * (len(EPOCHS) + 1):
        raise OSError("Espacio insuficiente para el recorte y su archivo temporal.")

    manifest = []
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_TIMEOUT="30"):
        for year, epoch in EPOCHS.items():
            urls = [f"{BASE}Global_cropland_{side}_{year}.tif" for side in ("SW", "NW")]
            with ExitStack() as stack:
                sources = [stack.enter_context(rasterio.open("/vsicurl/" + url)) for url in urls]
                assert all(src.crs.to_epsg() == 4326 for src in sources)
                pixels, transform = merge(sources, bounds=extent, nodata=NODATA, target_aligned_pixels=True)
            inside = geometry_mask([geometry], pixels.shape[1:], transform, invert=True)
            pixels[0, ~inside] = NODATA
            assert np.isin(pixels[0, inside], [0, 1]).all()
            assert np.any(pixels == 1)
            target = ROOT / f"glad_costa_dpa2019_{year}.tif"
            staged = target.with_suffix(".tmp.tif")
            with rasterio.open(staged, "w", driver="GTiff", width=pixels.shape[2],
                               height=pixels.shape[1], count=1, dtype="uint8",
                               crs="EPSG:4326", transform=transform, nodata=NODATA,
                               compress="lzw", tiled=True) as output:
                output.write(pixels)
                output.update_tags(epoch=epoch, description="0: sin cultivo o sin datos; 1: cultivo; 255: fuera del recorte")
            with rasterio.open(staged) as check:
                assert np.array_equal(check.read(), pixels)
            staged.replace(target)
            record = {
                "archivo": target.name, "epoca": epoch, "fuentes": urls,
                "bytes": target.stat().st_size, "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "pixeles_0": int(np.count_nonzero(pixels == 0)), "pixeles_1": int(np.count_nonzero(pixels == 1)),
            }
            manifest.append(record)
            print(record, flush=True)
    (ROOT / "recortes_glad.json").write_text(json.dumps({
        "fecha_consulta": "2026-11-14", "aoi": AOI.relative_to(ROOT.parents[1]).as_posix(),
        "aoi_sha256": hashlib.sha256(AOI.read_bytes()).hexdigest(), "limites_aoi": extent,
        "crs": "EPSG:4326", "resolucion_grados": resolution,
        "estimacion_sin_compresion_por_epoca_bytes": estimated, "espacio_libre_inicial_bytes": free,
        "archivos": manifest,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
