import hashlib
import json
import shutil
import time
import urllib.request
from contextlib import ExitStack
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from tempfile import TemporaryDirectory

import numpy as np
import rasterio
from rasterio.merge import merge

from solicitar_geotiffs import API, QUERY, ROOT, YEARS, PROVINCES, submit, api
from urllib.error import HTTPError
from pathlib import Path


def fetch(item, folder):
    for attempt in range(5):
        try:
            return fetch_once(item, folder)
        except (HTTPError, TimeoutError) as error:
            if attempt == 4 or isinstance(error, HTTPError) and error.code not in {429, 500, 502, 503, 504}:
                raise
            time.sleep(5 * (attempt + 1))


def fetch_once(item, folder):
    code, export = item
    identifier = export["id"]
    url = API + f"maps/exports/{identifier}/download" + QUERY
    target = folder / f"{code}_{export['years'][0]}.tif"
    if target.exists():
        with rasterio.open(target) as source:
            assert source.count == 1 and source.crs is not None
            for _, window in source.block_windows(1):
                source.read(1, window=window)
        return target, dict(code=code, url=url, years=export["years"], bytes=target.stat().st_size)
    stage = target.with_suffix(".part")
    deadline = time.monotonic() + 3600
    while time.monotonic() < deadline:
        status = api(f"maps/exports/{identifier}")["status"]
        print(code, export["years"][0], status, flush=True)
        if status == "READY":
            with urllib.request.urlopen(url, timeout=120) as response:
                expected = int(response.headers["Content-Length"])
                free = shutil.disk_usage(folder).free
                print(code, expected, free, flush=True)
                if free < expected * 10:
                    raise OSError("Espacio insuficiente")
                with stage.open("wb") as file:
                    shutil.copyfileobj(response, file)
            if stage.stat().st_size != expected:
                raise OSError(f"Descarga incompleta: {code}")
            stage.replace(target)
            return target, dict(code=code, url=url, years=export["years"], bytes=expected)
        if status in {"FAILED", "ERROR", "CANCELLED", "EXPIRED"}:
            raise RuntimeError(f"{code}: {status}")
        time.sleep(30)
    raise TimeoutError(f"Exportación pendiente: {code}")


def mosaic(files, year):
    records = []
    with ExitStack() as stack:
        sources = [stack.enter_context(rasterio.open(file)) for file in files]
        reference = sources[0]
        for source in sources:
            assert source.count == 1
            assert source.crs == reference.crs and source.res == reference.res
            for axis, step in ((2, reference.res[0]), (5, reference.res[1])):
                offset = (source.transform[axis] - reference.transform[axis]) / step
                assert abs(offset - round(offset)) < 1e-4
        for band in (1,):
            target = ROOT / f"costa_conali2024_col4_{year}.tif"
            staged = target.with_suffix(".tmp.tif")
            merge(sources, indexes=[band], nodata=0, dtype="uint8", target_aligned_pixels=False,
                  mem_limit=64, dst_path=staged, dst_kwds=dict(compress="lzw", tiled=True, BIGTIFF="IF_SAFER"))
            with rasterio.open(staged, "r+") as result:
                result.set_band_description(1, f"classification_{year}")
                result.update_tags(year=year, collection="MapBiomas Ecuador 4.0", territory="CONALI 2024")
                counts = np.zeros(256, dtype=np.int64)
                for _, window in result.block_windows(1):
                    counts += np.bincount(result.read(1, window=window).ravel(), minlength=256)
                assert np.count_nonzero(counts[1:]) > 2 and counts[0] > 0
                for source in sources:
                    sample = source.read(band, masked=True)
                    for row, col in zip(*np.where((~np.ma.getmaskarray(sample))[::100, ::100] & (sample.data[::100, ::100] > 0))):
                        point = source.xy(row * 100, col * 100)
                        assert next(result.sample([point]))[0] == sample.data[row * 100, col * 100]
                        break
                    else:
                        raise ValueError(f"Sin píxeles verificables: {source.name}, {year}")
                metadata = dict(year=year, file=target.name, crs=str(result.crs), resolution=result.res,
                                bounds=list(result.bounds), dimensions=[result.width, result.height],
                                nodata=result.nodata, class_counts={i: int(v) for i, v in enumerate(counts) if v})
            staged.replace(target)
            with target.open("rb") as file:
                metadata["sha256"] = hashlib.file_digest(file, "sha256").hexdigest()
            metadata["bytes"] = target.stat().st_size
            records.append(metadata)
            print(year, metadata["bytes"], flush=True)
    return records


def wait_for_exports(code, territory):
    deadline = time.monotonic() + 3600
    while time.monotonic() < deadline:
        try:
            return submit((code, territory))[1]
        except HTTPError as error:
            if error.code != 422 or b"simultaneous map exports" not in error.read():
                raise
            time.sleep(45)
    raise TimeoutError(f"Cupo de exportación pendiente: {code}")


if __name__ == "__main__":
    jobs_file = ROOT / "exportaciones_anuales.json"
    exports = json.loads(jobs_file.read_text(encoding="utf-8")) if jobs_file.exists() else {}
    folder = ROOT / "temporales_provinciales"
    folder.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = []
        for code, territory in PROVINCES.items():
            if code not in exports:
                exports[code] = wait_for_exports(code, territory)
                jobs_file.write_text(json.dumps(exports, indent=2), encoding="utf-8")
            assert sorted(row["years"][0] for row in exports[code]) == YEARS
            futures.extend(pool.submit(fetch, (code, row), folder) for row in exports[code])
        inputs = [future.result() for future in futures]
    outputs = []
    for year in YEARS:
        outputs.extend(mosaic([path for path, record in inputs if record["years"] == [year]], year))
    manifest = dict(download_date=datetime.now().date().isoformat(), area="CONALI 2024, categoría 115",
                    collection="MapBiomas Ecuador 4.0", license="CC BY 4.0",
                    exports=[record for _, record in inputs], files=outputs)
    (ROOT / "manifiesto_geotiff.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    for path, _ in inputs:
        path.unlink()
    folder.rmdir()