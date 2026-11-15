"""Build the Babahoyo MODIS land surface temperature layer from versioned NetCDF4.

Run with h5py, NumPy and Shapely:
    python proyecto-agricultura-ia/scripts/build_babahoyo_modis.py
"""

import csv
import json
from pathlib import Path

import h5py
import numpy as np
from shapely.geometry import box, shape


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parent
MODIS = ROOT / "04_vegetacion_cultivos_y_monitoreo/MODIS"
BOUNDARY = ROOT / "01_suelos_y_salud_del_suelo/SMAP/geografia/los_rios_cantones_referencia_2019.geojson"
OUTPUT = PROJECT / "backend/app/data/babahoyo_modis_temperature.json"
GROUP = "MODIS_MONTHLY_0_05DEG_CMG_LST"
BANDS = {"day": ("LST_Day_CMG", "QC_Day"), "night": ("LST_Night_CMG", "QC_Night")}
STEP = 0.05
TIMES = tuple(f"{year:04d}-{month:02d}" for year in range(2010, 2027)
              for month in range(1, (11 if year == 2026 else 13)))


def source_files():
    files = {}
    for name in ("consultas_2010_2014.csv", "consultas.csv"):
        with (MODIS / name).open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream, strict=True):
                if row["producto"] != "MOD11C3":
                    continue
                time = row["mes"]
                if time in files:
                    raise ValueError(f"Mes MODIS duplicado: {time}")
                files[time] = MODIS / row["archivo"]
    if tuple(sorted(files)) != TIMES:
        raise ValueError("La cobertura MODIS debe coincidir con enero de 2010–octubre de 2026")
    return files


def axes(group):
    lat_key = "Latitude" if "Latitude" in group else f"YDim_{GROUP}"
    lon_key = "Longitude" if "Longitude" in group else f"XDim_{GROUP}"
    return group[lat_key][:], group[lon_key][:]


def cells_for_canton(latitudes, longitudes):
    collection = json.loads(BOUNDARY.read_text(encoding="utf-8-sig"))
    canton, = [shape(feature["geometry"]) for feature in collection["features"]
               if feature["properties"]["DPA_CANTON"] == "1201"]
    if canton.is_empty or not canton.is_valid:
        raise ValueError("Geometría inválida para Babahoyo")
    left, bottom, right, top = canton.bounds
    half = STEP / 2
    rows = np.flatnonzero((latitudes + half > bottom) & (latitudes - half < top))
    cols = np.flatnonzero((longitudes + half > left) & (longitudes - half < right))
    cells = []
    for row in rows:
        lat = float(latitudes[row])
        for col in cols:
            lon = float(longitudes[col])
            bounds = [round(edge, 6) for edge in (lon - half, lat - half, lon + half, lat + half)]
            if canton.intersection(box(*bounds)).area > 0:
                cells.append((row, col, bounds))
    if len(cells) != 61:
        raise ValueError("Número de celdas inesperado para Babahoyo DPA 2019")
    return cells


def build():
    files = source_files()
    with h5py.File(files[TIMES[0]]) as dataset:
        latitudes, longitudes = axes(dataset[GROUP])
    np.testing.assert_allclose(latitudes, 1.475 - STEP * np.arange(109), atol=1e-6)
    np.testing.assert_allclose(longitudes, -81.025 + STEP * np.arange(53), atol=1e-5)
    cells = cells_for_canton(np.round(latitudes, 3), np.round(longitudes, 3))
    rows = [row for row, _, _ in cells]
    cols = [col for _, col, _ in cells]
    values = {band: [] for band in BANDS}
    for time in TIMES:
        with h5py.File(files[time]) as dataset:
            group = dataset[GROUP]
            current_latitudes, current_longitudes = axes(group)
            np.testing.assert_allclose(current_latitudes, latitudes, atol=1e-6)
            np.testing.assert_allclose(current_longitudes, longitudes, atol=1e-5)
            fields = group["Data_Fields"]
            for band, (field, quality) in BANDS.items():
                raw = fields[field][:][rows, cols]
                qc = fields[quality][:][rows, cols]
                valid = (raw != 0) & ((qc & 3) == 0)
                values[band].append([
                    round(float(pixel) * 0.02 - 273.15, 2) if keep else None
                    for pixel, keep in zip(raw, valid, strict=True)
                ])

    return {
        "metadata": {
            "source": "NASA MODIS Terra MOD11C3.061",
            "source_doi": "10.5067/MODIS/MOD11C3.061",
            "source_url": "https://doi.org/10.5067/MODIS/MOD11C3.061",
            "source_manifests": [
                (MODIS / name).relative_to(ROOT).as_posix()
                for name in ("consultas_2010_2014.csv", "consultas.csv")
            ],
            "boundary": BOUNDARY.relative_to(ROOT).as_posix(),
            "unit": "°C",
            "resolution_degrees": STEP,
            "crs": "EPSG:4326",
            "selection": "Celdas completas con intersección de área positiva con Babahoyo DPA 2019 (1201).",
            "quality": "raw != 0 y bits QC obligatorios iguales a 00 (qc & 3 == 0); el resto es null.",
            "conversion": "raw * 0.02 - 273.15",
        },
        "bounds": [bounds for _, _, bounds in cells],
        "times": TIMES,
        "values": values,
    }


if __name__ == "__main__":
    contents = json.dumps(build(), ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    OUTPUT.write_text(contents + "\n", encoding="utf-8", newline="\n")
