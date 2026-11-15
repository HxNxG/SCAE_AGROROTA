"""Verifica y agrega los meses nuevos publicados por la recopilación SMAP."""

import csv
import gzip
import hashlib
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HIST = ROOT / "datos/historico"
VARIABLES = ("superficial", "radicular")


def read(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def write(path, fields, rows):
    stage = path.with_suffix(".part")
    with stage.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    for attempt in range(10):
        try:
            stage.replace(path)
            return
        except PermissionError:
            if attempt == 9:
                raise
            time.sleep(1)


def main():
    verification_path = HIST / "meses_verificados.csv"
    summary_path = HIST / "humedad_mensual_provincial.csv"
    verification_fields, verified_rows = read(verification_path)
    summary_fields, summary_rows = read(summary_path)
    verified = {r["mes"]: r for r in verified_rows}
    counts = Counter(r["mes"] for r in summary_rows)
    weights = defaultdict(list)
    totals = defaultdict(float)
    for r in read(ROOT / "geografia/celda_provincia.csv")[1]:
        province = r["provincia_id"], r["provincia"]
        area = float(r["intersection_area_m2"])
        weights[r["cell_id"]].append((province, area))
        totals[province] += area
    for marker in sorted(HIST.glob("calidad_????-??.json")):
        month = marker.stem.removeprefix("calidad_")
        meta = json.loads(marker.read_text(encoding="utf-8"))
        if month in verified and verified[month]["sha256"] == meta["sha256"] and counts[month] == len(totals) * 2:
            continue
        path = HIST / f"smap_costa_3horas_{month}.csv.gz"
        with path.open("rb") as stream:
            checksum = hashlib.file_digest(stream, "sha256").hexdigest()
        assert checksum == meta["sha256"], path
        seen = set()
        intervals = Counter()
        missing = Counter()
        summed = defaultdict(float)
        valid_area = defaultdict(float)
        with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream):
                time, cell = row["time_start_utc"], row["cell_id"]
                key = time, cell
                assert key not in seen and time.startswith(month) and cell in weights, key
                seen.add(key)
                intervals[time] += 1
                for variable, field in zip(VARIABLES, ("sm_surface_m3_m3", "sm_rootzone_m3_m3")):
                    raw = row[field]
                    if not raw:
                        missing[variable] += 1
                        continue
                    value = float(raw)
                    assert 0 <= value <= 1, (key, field)
                    for province, area in weights[cell]:
                        summed[province, variable] += value * area
                        valid_area[province, variable] += area
        assert len(seen) == meta["rows"] and len(intervals) == meta["n_intervals"]
        assert set(intervals.values()) == {1045}
        assert missing["superficial"] == meta["missing_surface"]
        assert missing["radicular"] == meta["missing_rootzone"]
        verified[month] = dict(zip(verification_fields, [
            month, len(seen), len(intervals), missing["superficial"], missing["radicular"],
            min(intervals), max(intervals), checksum,
        ]))
        summary_rows = [row for row in summary_rows if row["mes"] != month]
        for province, total in sorted(totals.items()):
            for variable in VARIABLES:
                area = valid_area[province, variable]
                fraction = area / (total * len(intervals))
                assert 0 <= fraction <= 1.000001
                summary_rows.append(dict(zip(summary_fields, [
                    month, *province, variable, summed[province, variable] / area if area else "",
                    min(1, fraction), len(intervals),
                ])))
        print(month, len(seen), flush=True)
    write(verification_path, verification_fields, [verified[m] for m in sorted(verified)])
    write(summary_path, summary_fields, sorted(summary_rows, key=lambda r: (r["mes"], r["codigo_dpa"], r["variable"])))


if __name__ == "__main__":
    main()
