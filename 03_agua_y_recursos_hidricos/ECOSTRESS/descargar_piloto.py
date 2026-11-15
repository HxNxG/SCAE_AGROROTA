import hashlib
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np
import rasterio
import requests
from rasterio.warp import transform
from rasterio.windows import Window

from consultar_cobertura import API, HERE, PRODUCTS

SIDE = 33
LAYERS = (("LST", 0), ("QC", 0), ("cloud", 0), ("PTJPLSMinst", 1), ("cloud", 1))
CAP = 10_000_000


def catalog(session, params):
    response = session.get(API, params=params, timeout=45)
    response.raise_for_status()
    return response.json()["feed"]["entry"]


def clip(session, url, point, destination):
    with session.get(url, headers={"Range": "bytes=0-16383"}, stream=True, timeout=30) as response:
        response.raise_for_status()
        if response.status_code != 206:
            raise RuntimeError("El servidor no admite lectura por rangos")
        signed_url = response.url
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_TIMEOUT="30"):
        with rasterio.open(f"/vsicurl?use_head=no&url={requests.utils.quote(signed_url, safe='')}") as src:
            x, y = transform("EPSG:4326", src.crs, [point[0]], [point[1]])
            row, col = src.index(x[0], y[0])
            window = Window(col - SIDE // 2, row - SIDE // 2, SIDE, SIDE)
            if not (0 <= window.col_off <= src.width - SIDE and 0 <= window.row_off <= src.height - SIDE):
                raise ValueError("Ventana fuera del mosaico")
            data = src.read(1, window=window, masked=True)
            profile = dict(driver="GTiff", dtype=src.dtypes[0], count=1,
                           width=SIDE, height=SIDE, crs=src.crs,
                           transform=src.window_transform(window), nodata=src.nodata,
                           compress="deflate")
            scale, offset, units = src.scales[0], src.offsets[0], src.units[0]
    with rasterio.Env(GDAL_TIFF_INTERNAL_MASK=True):
        with rasterio.open(destination, "w", **profile) as dst:
            dst.write(data.data, 1)
            dst.write_mask((~np.ma.getmaskarray(data)).astype("uint8") * 255)
            dst.scales, dst.offsets = (scale,), (offset,)
            if units:
                dst.set_band_unit(1, units)
    return data, (profile["crs"], profile["transform"]), {
        "archivo": destination.name, "origen": url, "escala": scale, "offset": offset,
        "unidad_geotiff": units, "bytes": destination.stat().st_size,
        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
    }


def download(record, out, after=None, minimum=1):
    code = record["provincia"]["DPA_PROVIN"]
    point = tuple(map(float, record["parametros"]["point"].split(",")))
    params = {**record["parametros"], "page_size": 50, "sort_key": "-start_date"}
    with requests.Session() as session:
        params["short_name"] = PRODUCTS[1]
        candidates = catalog(session, params)
        for et in candidates:
            et_id = et["producer_granule_id"]
            orbit, scene, tile, time = et_id.split("_")[3:7]
            if after and time >= after:
                continue
            pattern = f"ECOv002_L2T_LSTE_{orbit}_{scene}_{tile}_{time}_*"
            if not 12 <= int(time.split("T")[1][:2]) < 22:
                continue
            lst_query = {**params, "short_name": PRODUCTS[0], "producer_granule_id": pattern,
                         "options[producer_granule_id][pattern]": "true", "page_size": 5}
            matches = catalog(session, lst_query)
            if not matches:
                continue
            products = (matches[0], et)
            assets = []
            arrays = []
            grid = None
            for layer, index in LAYERS:
                item = products[index]
                url = next(link["href"] for link in item["links"]
                           if link["href"].startswith("https://data.lpdaac.")
                           and link["href"].endswith(f"_{layer}.tif"))
                target = out / f"{code}_{time}_L{index+2}_{layer}.tif"
                data, current_grid, meta = clip(session, url, point, target)
                if grid is not None and grid != current_grid:
                    raise ValueError("Las capas no coinciden espacialmente")
                grid = current_grid
                arrays.append(data)
                assets.append(meta)
            lst, qc, cloud_lst, et_data, cloud_et = arrays
            clear = ((cloud_lst == 0) & (cloud_et == 0)
                     & ((qc.astype("uint16") & 3) == 0)
                     & np.isfinite(lst) & (lst > 0)
                     & np.isfinite(et_data)).filled(False)
            if after and int(clear.sum()) < minimum:
                continue
            return dict(provincia=record["provincia"], punto=point, adquisicion=time,
                        granulos=[p["producer_granule_id"] for p in products],
                        pixeles_validos=int(clear.sum()), pixeles_totales=SIDE**2,
                        crs=str(grid[0]), archivos=assets)
    raise RuntimeError("Sin par diurno en los primeros 50 gránulos de ET")


def main():
    import sys

    improve = "--mejorar" in sys.argv[1:]
    retry = improve or "--alternativas" in sys.argv[1:]
    historical = HERE / "cobertura_piloto_2026-11-14.json"
    records = json.loads(historical.read_text(encoding="utf-8"))["resultados"][::2]
    free = shutil.disk_usage(HERE).free
    if free < CAP:
        raise RuntimeError("Espacio libre insuficiente")
    out = HERE / "piloto_ecostress_2026-11-14"
    previous = {}
    if retry:
        alternatives = HERE / "alternativas_ecostress_2026-11-14"
        prior = json.loads(((alternatives if improve else out) / "manifest.json").read_text(encoding="utf-8"))
        previous = {r["provincia"]["DPA_PROVIN"]: r["adquisicion"]
                    for r in prior["recortes"] if r["pixeles_validos"] < (100 if improve else 1)}
        records = [r for r in records if r["provincia"]["DPA_PROVIN"] in previous]
        out = HERE / "cobertura_mejorada_ecostress_2026-11-14" if improve else alternatives
    out.mkdir(exist_ok=True)
    manifest = dict(fecha_ejecucion=date.today().isoformat(), catalogo=API,
                    consulta_base=historical.name, bytes_libres_antes=free,
                    bytes_estimados_maximo=CAP, lado_pixeles=SIDE,
                    justificacion="Validar temperatura y ET de una misma adquisición por provincia",
                    recortes=[], errores=[])
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [(r, pool.submit(download, r, out, previous.get(r["provincia"]["DPA_PROVIN"]), 100 if improve else 1))
                for r in records]
        for record, job in jobs:
            try:
                manifest["recortes"].append(job.result())
            except Exception as exc:
                # Evita imprimir enlaces temporales firmados o detalles de autenticación.
                manifest["errores"].append(dict(provincia=record["provincia"],
                                                tipo=type(exc).__name__))
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8")
    print(len(manifest["recortes"]), manifest["errores"])


if __name__ == "__main__":
    main()
