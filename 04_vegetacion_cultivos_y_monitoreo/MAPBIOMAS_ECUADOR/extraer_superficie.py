import csv
import hashlib
import os
from pathlib import Path

from openpyxl import load_workbook

source = Path(os.environ["MB_TEMP"])
root = Path(os.environ["MB_OUT"])
names = {"07": "El Oro", "08": "Esmeraldas", "09": "Guayas", "12": "Los Ríos", "13": "Manabí", "23": "Santo Domingo de los Tsáchilas", "24": "Santa Elena"}
years = range(2015, 2026)
with source.open("rb") as handle:
    book = load_workbook(handle, read_only=True, data_only=True)
    rows = book["pivot_ha"].values
    columns = next(rows)
    records = []
    for cells in rows:
        row = dict(zip(columns, cells))
        code = str(row["geocode"]).zfill(2)
        if code in names:
            for year in years:
                records.append((code, names[code], year, row["class"],
                                *(row[f"class_level_{level}"] for level in range(5)),
                                row[f"y{year}"]))
    book.close()
assert {(r[0], r[2]) for r in records} == {(c, y) for c in names for y in years}
assert len({(r[0], r[2], r[3]) for r in records}) == len(records)
assert all(isinstance(r[-1], (int, float)) and r[-1] >= 0 for r in records)
output = root / "superficie_provincial_2015_2025.csv"
with output.open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["codigo_provincia", "provincia", "anio", "clase_id",
                     *(f"clase_nivel_{n}" for n in range(5)), "superficie_ha"])
    writer.writerows(sorted(records))
print(len(records))
for file in (source, output):
    print(file.name, file.stat().st_size, hashlib.sha256(file.read_bytes()).hexdigest())
