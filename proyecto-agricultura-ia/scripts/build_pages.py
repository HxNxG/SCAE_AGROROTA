"""Assemble the public map and saved diagnosis in an empty directory."""

import argparse
import json
import os
import re
from pathlib import Path
from shutil import copy2

from build_pages_climate import export_climate


FRONTEND = Path(__file__).resolve().parents[1] / "frontend"
HTTPS_ORIGIN = re.compile(
    r"https://(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}/?",
    re.IGNORECASE | re.ASCII,
)


def build(output):
    if output.exists() and any(output.iterdir()):
        raise ValueError("Pages output must be an empty directory")
    api_url = os.environ.get("BIOTINDER_API_URL", "").strip()
    if api_url and not HTTPS_ORIGIN.fullmatch(api_url):
        raise ValueError("BIOTINDER_API_URL must be an HTTPS origin without a path, query or credentials")
    files = [
        "index.html", "pages.css", "pimocha-demo.json",
        "cartography/babahoyo.geojson", "cartography/parroquias.geojson",
        "cartography/ATTRIBUTION.md",
    ]
    for name in files:
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(FRONTEND / "pages" / name, target)

    source_files = [
        "src/main.js", "src/styles.css", "src/components/recommendations.js",
        "src/services/aiApi.js", "src/services/pilotApi.js", "src/services/pagesClimate.js",
        "src/services/pagesGeography.js", "src/vendor/pico.conditional.min.css", "src/vendor/pico.LICENSE.txt",
    ]
    source_files.extend(
        file.relative_to(FRONTEND) for file in (FRONTEND / "src/components/map").glob("*.js")
    )
    for name in source_files:
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(FRONTEND / name, target)
    export_climate(output / "climate")
    (output / "config.json").write_text(
        json.dumps({"apiOrigin": api_url.rstrip("/").lower() or None}) + "\n", encoding="utf-8"
    )
    (output / ".nojekyll").touch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    build(parser.parse_args().output)
