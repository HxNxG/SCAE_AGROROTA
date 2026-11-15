import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

API = "https://prd.plataforma.mapbiomas.org/api/v1/ecuador/"
QUERY = "?tenantId=mapbiomas"
SUBTHEME = "cobertura-copia-0j43ew_coverage-zbyh4p"
PROVINCES = {
    "07": "1b2c0259-34d4-4757-9501-905b34175b1e",
    "08": "178a7f6c-c7c0-49e3-88fd-8614dda2c6ea",
    "09": "068041c6-dc11-4d31-bf86-23f1aa474270",
    "12": "11021572-3e2d-4cca-b380-2b1d38d96aa0",
    "13": "7fa3e45c-28d0-43de-8993-4d1f90919164",
    "23": "91a238a5-1007-4019-b561-a8bf3f0ee61b",
    "24": "7d65a0dc-4b0f-4088-b254-5d97bb3ed308",
}
YEARS = list(range(2015, 2026))
ROOT = Path(__file__).resolve().parent


def api(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(API + path + QUERY, data, {"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=40) as response:
        return json.load(response)


def submit(item):
    code, territory = item
    exports = api("maps/exports", {
        "territoryId": territory, "subthemeKey": SUBTHEME, "years": YEARS,
        "filters": {}, "exportType": "separate",
    })["exports"]
    print(code, [(row["id"], row["status"]) for row in exports], flush=True)
    return code, exports


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = dict(pool.map(submit, PROVINCES.items()))
    (ROOT / "exportaciones_geotiff.json").write_text(json.dumps(jobs, indent=2), encoding="utf-8")
