"""Resume MODIS mensual por provincia y cantón con ponderación geodésica."""

import csv
import json
from pathlib import Path

import h5py
import numpy as np
from pyproj import Geod
from shapely import box, orient_polygons
from shapely.geometry import shape

HERE = Path(__file__).resolve().parent
GEO = HERE.parents[1] / "01_suelos_y_salud_del_suelo/SMAP/geografia"
GROUPS = {"MOD13C2": "MOD_Grid_monthly_CMG_VI", "MOD11C3": "MODIS_MONTHLY_0_05DEG_CMG_LST"}
BANDS = {
    "MOD13C2": [
        ("ndvi", "CMG_0_05_Deg_Monthly_NDVI", "CMG_0_05_Deg_Monthly_VI_Quality", -3000, .0001, 0),
        ("evi", "CMG_0_05_Deg_Monthly_EVI", "CMG_0_05_Deg_Monthly_VI_Quality", -3000, .0001, 0),
    ],
    "MOD11C3": [
        ("lst_diurna_c", "LST_Day_CMG", "QC_Day", 0, .02, -273.15),
        ("lst_nocturna_c", "LST_Night_CMG", "QC_Night", 0, .02, -273.15),
    ],
}


def areas(features):
    geod = Geod(ellps="WGS84")
    lat = np.round(1.475 - .05 * np.arange(109), 3)
    lon = np.round(-81.025 + .05 * np.arange(53), 3)
    weights = np.zeros((len(features), 109, 53))
    for index, feature in enumerate(features):
        geometry = shape(feature["geometry"])
        west, south, east, north = geometry.bounds
        ys = np.flatnonzero((lat + .025 > south) & (lat - .025 < north))
        xs = np.flatnonzero((lon + .025 > west) & (lon - .025 < east))
        for y in ys:
            for x in xs:
                cell = box(lon[x] - .025, lat[y] - .025, lon[x] + .025, lat[y] + .025)
                overlap = geometry.intersection(cell)
                if not overlap.is_empty:
                    weights[index, y, x] = geod.geometry_area_perimeter(orient_polygons(overlap))[0]
        expected, _ = geod.geometry_area_perimeter(orient_polygons(geometry))
        assert .999 <= weights[index].sum() / expected <= 1.001, feature["properties"]
    return weights.reshape(len(features), -1)


def main(early=False):
    provinces = json.loads((GEO / "costa_provincias_referencia_2019.geojson").read_text(encoding="utf-8"))["features"]
    cantons = json.loads((GEO / "costa_cantones_referencia_2019.geojson").read_text(encoding="utf-8"))["features"]
    features = provinces + cantons
    assert len(provinces) == 7 and len(cantons) == 86
    weights = areas(features)
    total = weights.sum(axis=1)
    manifest = "consultas_2010_2014.csv" if early else "consultas.csv"
    with (HERE / manifest).open(encoding="utf-8-sig", newline="") as stream:
        queries = list(csv.DictReader(stream))
    assert len({(q["producto"], q["mes"]) for q in queries}) == len(queries) == (120 if early else 284)
    period = "2010-01_2014-12" if early else "2015-01_2026-10"
    target = HERE / f"MODIS_mensual_DPA2019_{period}.csv"
    stage = target.with_suffix(".part")
    with stage.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["mes", "codigo_dpa", "territorio", "variable", "media",
                         "area_valida_km2", "fraccion_valida"])
        for query in sorted(queries, key=lambda row: (row["mes"], row["producto"])):
            product = query["producto"]
            with h5py.File(HERE / query["archivo"]) as dataset:
                group = dataset[GROUPS[product]]
                lat_key = "Latitude" if "Latitude" in group else f"YDim_{GROUPS[product]}"
                lon_key = "Longitude" if "Longitude" in group else f"XDim_{GROUPS[product]}"
                np.testing.assert_allclose(group[lat_key][:], 1.475 - .05 * np.arange(109))
                np.testing.assert_allclose(group[lon_key][:], -81.025 + .05 * np.arange(53))
                fields = group["Data_Fields"]
                for name, band, quality_band, fill, scale, offset in BANDS[product]:
                    raw = fields[band][:].ravel()
                    qc = fields[quality_band][:].ravel()
                    valid = (raw != fill) & ((qc & 3) == 0)
                    valid_area = weights @ valid
                    weighted = weights @ np.where(valid, raw * scale + offset, 0)
                    for i, feature in enumerate(features):
                        prop = feature["properties"]
                        writer.writerow([
                            query["mes"], prop.get("DPA_CANTON", prop["DPA_PROVIN"]),
                            prop.get("DPA_DESCAN", prop["DPA_DESPRO"]), name,
                            weighted[i] / valid_area[i] if valid_area[i] else "",
                            valid_area[i] / 1e6, min(1.0, valid_area[i] / total[i]),
                        ])
    stage.replace(target)


if __name__ == "__main__":
    import sys

    main(early="--2010-2014" in sys.argv[1:])
