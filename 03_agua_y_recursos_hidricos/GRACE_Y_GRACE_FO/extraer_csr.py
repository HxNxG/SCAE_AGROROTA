"""Recorta la serie GRACE/GRACE-FO de CSR a la Costa DPA 2019."""

import csv
import hashlib
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path

import fsspec
import h5py
import numpy as np
from pyproj import Geod
from shapely import box, orient_polygons, union_all
from shapely.geometry import shape

HERE = Path(__file__).resolve().parent
BOUNDARY = HERE.parents[1] / "01_suelos_y_salud_del_suelo/SMAP/geografia/costa_provincias_referencia_2019.geojson"
BASE = "https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/"
DATA = BASE + "CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc"
LAND = BASE + "CSR_GRACE_GRACE-FO_RL06_Mascons_v02_LandMask.nc"
EPOCH = datetime(2002, 1, 1)


def open_remote(url):
    return fsspec.open(url, block_size=262144, cache_type="blockcache")


def write_csv(name, header, rows):
    path = HERE / name
    temporary = path.with_suffix(".part")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)
    temporary.replace(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    reference = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    coast = union_all([shape(feature["geometry"]) for feature in reference["features"]])
    left, bottom, right, top = coast.bounds
    free = shutil.disk_usage(HERE).free
    estimate = 5_000_000
    if free < estimate * 2:
        raise OSError("Espacio insuficiente para el recorte y los archivos temporales")
    record = {
        "urls": [DATA, LAND], "estimated_output_bytes": estimate, "free_bytes": free,
        "boundary": BOUNDARY.name, "boundary_sha256": hashlib.sha256(BOUNDARY.read_bytes()).hexdigest(),
        "purpose": "Contexto regional de anomalías de almacenamiento de agua y sequía.",
    }
    metadata = HERE / "metadatos_csr.json"
    metadata.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    with open_remote(DATA) as raw, h5py.File(raw, "r") as dataset:
        lat = dataset["lat"][:]
        lon = (dataset["lon"][:] + 180) % 360 - 180
        y = np.flatnonzero((lat + .125 > bottom) & (lat - .125 < top))
        x = np.flatnonzero((lon + .125 > left) & (lon - .125 < right))
        ys, xs = slice(y[0], y[-1] + 1), slice(x[0], x[-1] + 1)
        dates = [EPOCH + timedelta(days=float(t)) for t in dataset["time"][:]]
        times = [i for i, day in enumerate(dates) if day >= datetime(2010, 1, 1)]
        bounds = dataset["time_bounds"][times[0]:]
        values = dataset["lwe_thickness"][times[0]:, ys, xs]
        record["source_bytes"] = raw.size
        record["source_attributes"] = {
            k: dataset.attrs[k].decode() for k in (
                "time_coverage_start", "time_coverage_end", "time_mean_removed", "license",
                "geospatial_lat_resolution", "label", "date_created", "user_note_1", "user_note_2",
            )
        }
        assert dataset["lwe_thickness"].attrs["Units"] == b"cm"
    with open_remote(LAND) as raw, h5py.File(raw, "r") as mask:
        assert np.array_equal(mask["lat"][ys], lat[ys])
        assert np.allclose((mask["lon"][xs] + 180) % 360 - 180, lon[xs])
        land = mask["LO_val"][ys, xs]
    assert set(np.unique(land)) <= {0, 1}
    geod = Geod(ellps="WGS84")
    cells = []
    detailed = []
    summaries = []
    for j, latitude in enumerate(lat[ys]):
        for i, longitude in enumerate(lon[xs]):
            if not land[j, i]:
                continue
            overlap = coast.intersection(box(longitude - .125, latitude - .125,
                                             longitude + .125, latitude + .125))
            area, _ = geod.geometry_area_perimeter(orient_polygons(overlap))
            if area > 0:
                cells.append((j, i, latitude, longitude, area / 1_000_000))
    assert cells
    total_area = sum(c[4] for c in cells)
    months = set()
    intervals = set()
    for index, time in enumerate(times):
        month = dates[time].strftime("%Y-%m")
        months.add(month)
        interval = tuple(bounds[index])
        assert interval not in intervals
        intervals.add(interval)
        date_fields = [month, dates[time].isoformat()] + [
            (EPOCH + timedelta(days=float(t))).isoformat() for t in bounds[index]
        ]
        total, valid_area, valid_count = 0.0, 0.0, 0
        for j, i, latitude, longitude, area in cells:
            value = float(values[index, j, i])
            if np.isfinite(value):
                total += value * area
                valid_area += area
                valid_count += 1
            else:
                value = None
            detailed.append(date_fields + [latitude, longitude, area, value])
        assert valid_count
        summaries.append(date_fields + [total / valid_area, valid_area, total_area, valid_count])

    columns = ["mes", "fecha_central_utc", "inicio_utc", "fin_utc"]
    for name, more, rows in (
        ("csr_rl063_costa_celdas.csv", ["latitud", "longitud", "interseccion_km2", "anomalia_cm"], detailed),
        ("csr_rl063_costa_mensual.csv", ["anomalia_cm", "area_valida_km2", "area_malla_km2", "celdas_validas"], summaries),
    ):
        record[name] = {"sha256": write_csv(name, columns + more, rows), "rows": len(rows)}
    expected = {f"{year}-{month:02d}" for year in range(2010, dates[-1].year + 1) for month in range(1, 13)
                if f"{year}-{month:02d}" <= max(months)}
    record.update(first_month=min(months), last_month=max(months), missing_months=sorted(expected - months))
    metadata.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(intervals)} intervalos en {len(months)} meses, {len(cells)} celdas, {len(detailed)} registros")


if __name__ == "__main__":
    main()
