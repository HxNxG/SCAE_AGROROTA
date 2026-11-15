import csv
import hashlib
from pathlib import Path

import h5py
import numpy as np

root = Path(__file__).resolve().parent
products = {
    "MOD13C2": (
        "MOD_Grid_monthly_CMG_VI",
        {
            "CMG_0_05_Deg_Monthly_NDVI": (-2000, 10000, -3000),
            "CMG_0_05_Deg_Monthly_EVI": (-2000, 10000, -3000),
            "CMG_0_05_Deg_Monthly_VI_Quality": (0, 65534, 65535),
        },
    ),
    "MOD11C3": (
        "MODIS_MONTHLY_0_05DEG_CMG_LST",
        {
            "LST_Day_CMG": (7500, 65535, 0),
            "LST_Night_CMG": (7500, 65535, 0),
            "QC_Day": (0, 255, None),
            "QC_Night": (0, 255, None),
        },
    ),
}

with (root / "consultas.csv").open(encoding="utf-8-sig", newline="") as handle:
    queries = list(csv.DictReader(handle))
months = {f"{year}-{month:02d}" for year in range(2015, 2027)
          for month in range(1, 13) if year < 2026 or month <= 10}
expected = {(product, month) for product in products for month in months}
assert len(queries) == len(expected)
assert {(row["producto"], row["mes"]) for row in queries} == expected
integrity = []
quality = {}
for row in queries:
    product = row["producto"]
    path = root / row["archivo"]
    group, bands = products[product]
    with h5py.File(path) as data:
        grid = data[group]
        np.testing.assert_allclose(grid["Latitude" if "Latitude" in grid else f"YDim_{group}"][:], 1.475 - 0.05 * np.arange(109))
        np.testing.assert_allclose(grid["Longitude" if "Longitude" in grid else f"XDim_{group}"][:], -81.025 + 0.05 * np.arange(53))
        for band, (low, high, fill) in bands.items():
            values = grid["Data_Fields"][band][:]
            assert values.shape == (109, 53), (path, band, values.shape)
            missing = values == fill if fill is not None else np.zeros(values.shape, bool)
            outside = ~missing & ((values < low) | (values > high))
            assert not outside.any(), (path, band, values[outside][:10])
            key = (product, band)
            quality[key] = quality.get(key, 0) + int(missing.sum())
    with path.open("rb") as handle:
        checksum = hashlib.file_digest(handle, "sha256").hexdigest()
    integrity.append({"archivo": row["archivo"], "bytes": path.stat().st_size, "sha256": checksum})

with (root / "integridad.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=("archivo", "bytes", "sha256"))
    writer.writeheader()
    writer.writerows(integrity)

print(len(integrity), "archivos;", sum(row["bytes"] for row in integrity), "bytes")
for (product, band), missing in quality.items():
    print(product, band, missing, "valores de relleno")
