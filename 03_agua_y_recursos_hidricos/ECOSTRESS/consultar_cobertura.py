import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from shapely.geometry import shape

HERE = Path(__file__).resolve().parent
BOUNDARY = Path("01_suelos_y_salud_del_suelo/SMAP/geografia/costa_provincias_referencia_2019.geojson")
API = "https://cmr.earthdata.nasa.gov/search/granules.json"
PRODUCTS = ("ECO_L2T_LSTE", "ECO_L3T_JET")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corte", default="2026-11-14")
    args = parser.parse_args()
    temporal = f"2010-01-01T00:00:00Z,{args.corte}T23:59:59Z"
    features = json.loads((HERE.parents[1] / BOUNDARY).read_text(encoding="utf-8-sig"))["features"]

    def query(job):
        feature, product = job
        point = shape(feature["geometry"]).representative_point()
        params = dict(provider="LPCLOUD", short_name=product, version="002",
                      temporal=temporal, point=f"{point.x:.6f},{point.y:.6f}", page_size=1)
        result = dict(provincia=feature["properties"], parametros=params)
        for order, key in (("start_date", "primero"), ("-start_date", "ultimo")):
            response = requests.get(API, params={**params, "sort_key": order}, timeout=45)
            response.raise_for_status()
            entries = response.json()["feed"]["entry"]
            result["granulos"] = int(response.headers["CMR-Hits"])
            result[key] = ({field: entries[0][field] for field in ("producer_granule_id", "time_start")}
                           if entries else None)
        return result

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(query, [(f, p) for f in features for p in PRODUCTS]))
    output = {"catalogo": API, "geometria_epsg_4326": BOUNDARY.as_posix(),
              "metodo": "Un punto interior por provincia; solo huellas de catalogo.",
              "resultados": results}
    target = HERE / f"cobertura_piloto_{args.corte}.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
