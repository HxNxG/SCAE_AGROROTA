"""Export the climate map's committed snapshots for a static Pages build."""

import argparse
import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.babahoyo_climate import read_monthly_precipitation
from app.services.babahoyo_imerg import read_layer
from app.services.babahoyo_modis import TIMES as MODIS_TIMES
from app.services.babahoyo_modis import read_series
from app.services.babahoyo_smap import TIMES as SMAP_TIMES
from app.services.babahoyo_smap import read_sample


def grid_snapshot(reader, times, resolution_key):
    metadata, bounds, values = reader()
    return {
        "source": metadata["source"],
        "unit": metadata["unit"],
        resolution_key: metadata[resolution_key],
        "bounds": bounds,
        "times": times,
        "values": values,
    }


def export_climate(output):
    source, bounds, months = read_layer()
    snapshots = {
        "imerg-monthly.json": read_monthly_precipitation(),
        "imerg-cells.json": {"source": source, "unit": "mm", "bounds": bounds, "months": months},
        "smap.json": grid_snapshot(read_sample, SMAP_TIMES, "resolution_km"),
        "modis.json": grid_snapshot(read_series, MODIS_TIMES, "resolution_degrees"),
    }
    output.mkdir(parents=True, exist_ok=True)
    for filename, snapshot in snapshots.items():
        (output / filename).write_text(
            json.dumps(snapshot, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Destination for the public climate snapshots")
    export_climate(parser.parse_args().output)


if __name__ == "__main__":
    main()
