"""Amplía el recorte MODIS mensual usando las consultas DAP4 del repositorio."""

import csv
import hashlib
import io
import json
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import earthaccess
import h5py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

HERE = Path(__file__).resolve().parent
LOCAL = threading.local()
MONTHS = {f"{year}-{month:02d}" for year in range(2010, 2015) for month in range(1, 13)}


def download(row):
    path = HERE / row["archivo"]
    if path.exists():
        content = path.read_bytes()
    else:
        if not hasattr(LOCAL, "session"):
            LOCAL.session = earthaccess.__auth__.get_session()
            LOCAL.session.mount("https://", HTTPAdapter(max_retries=Retry(
                total=3, backoff_factor=1, status_forcelist=(429, 500, 502, 503, 504))))
        with LOCAL.session.get(row["url"], stream=True, timeout=(20, 90)) as response:
            response.raise_for_status()
            content = response.raw.read(512_001, decode_content=True)
        if len(content) > 512_000:
            raise ValueError(f"Recorte demasiado grande: {path}")
    with h5py.File(io.BytesIO(content)) as dataset:
        group = next(iter(dataset.values()))
        assert all(band.shape == (109, 53) for band in group["Data_Fields"].values())
    if not path.exists():
        stage = path.with_suffix(".part")
        stage.write_bytes(content)
        stage.replace(path)
    return row["archivo"], len(content), hashlib.sha256(content).hexdigest()


def main():
    with (HERE / "consultas.csv").open(encoding="utf-8-sig", newline="") as stream:
        templates = {r["producto"]: r for r in csv.DictReader(stream) if r["mes"] == "2015-01"}
    queries = []
    for product, row in templates.items():
        catalog = row["catalogo"].split("&temporal=")[0] + (
            "&temporal=2010-01-01T00:00:00Z,2014-12-31T23:59:59Z&page_size=100"
        )
        response = requests.get(catalog, timeout=30)
        response.raise_for_status()
        entries = response.json()["feed"]["entry"]
        assert len(entries) == 60 and {e["time_start"][:7] for e in entries} == MONTHS
        suffix = row["url"].split(".dap.nc4", 1)[1]
        for entry in entries:
            month = entry["time_start"][:7]
            url = next(link["href"] for link in entry["links"] if "opendap.earthdata.nasa.gov/collections/" in link["href"])
            queries.append(dict(producto=product, mes=month, archivo=f"{product}/{month}.nc4",
                                url=url + ".dap.nc4" + suffix, catalogo=catalog))
    assert len(queries) == 120
    free = shutil.disk_usage(HERE).free
    estimate = len(queries) * 512_000
    assert free > estimate
    (HERE / "preparacion_2010_2014.json").write_text(json.dumps({
        "consulta": "2026-11-14", "maximo_estimado_bytes": estimate,
        "espacio_libre_bytes": free, "proposito": "Ampliar el histórico de vegetación y temperatura superficial.",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    with (HERE / "consultas_2010_2014.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(queries[0]))
        writer.writeheader()
        writer.writerows(queries)
    earthaccess.login(strategy="netrc")
    with (HERE / "integridad_2010_2014.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["archivo", "bytes", "sha256"])
        with ThreadPoolExecutor(max_workers=4) as pool:
            for record in pool.map(download, queries):
                writer.writerow(record)
                stream.flush()
                print(record[0], flush=True)


if __name__ == "__main__":
    main()
