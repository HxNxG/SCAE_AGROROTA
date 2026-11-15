"""Point selection against the documented DPA 2019 Babahoyo boundary."""

from functools import lru_cache
import json
from math import isfinite
from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[4] / "01_suelos_y_salud_del_suelo"
          / "SMAP" / "geografia" / "los_rios_cantones_referencia_2019.geojson")
CANTON_CODE = "1201"


@lru_cache(maxsize=1)
def babahoyo_geometry():
    collection = json.loads(SOURCE.read_text(encoding="utf-8-sig"))
    matches = [feature for feature in collection["features"]
               if feature["properties"].get("DPA_CANTON") == CANTON_CODE]
    if len(matches) != 1:
        raise ValueError("La referencia DPA 2019 no contiene un Babahoyo único")
    return matches[0]["geometry"]


def _on_segment(x, y, ax, ay, bx, by):
    cross = (x - ax) * (by - ay) - (y - ay) * (bx - ax)
    return abs(cross) < 1e-11 and min(ax, bx) <= x <= max(ax, bx) and min(ay, by) <= y <= max(ay, by)


def _in_ring(x, y, ring):
    inside = False
    previous = ring[-1]
    for current in ring:
        ax, ay = previous
        bx, by = current
        if _on_segment(x, y, ax, ay, bx, by):
            return True, True
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
            inside = not inside
        previous = current
    return inside, False


def _in_polygon(x, y, rings):
    inside, boundary = _in_ring(x, y, rings[0])
    if not inside:
        return False
    if boundary:
        return True
    for hole in rings[1:]:
        in_hole, on_hole = _in_ring(x, y, hole)
        if in_hole and not on_hole:
            return False
    return True


def validate_point(longitude, latitude):
    """Return a location result; GeoJSON coordinates are longitude, latitude."""
    if not all(isinstance(value, (int, float)) and isfinite(value)
               for value in (longitude, latitude)):
        raise ValueError("Las coordenadas deben ser números finitos")
    if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
        raise ValueError("Coordenadas fuera del rango WGS84")
    geometry = babahoyo_geometry()
    polygons = ([geometry["coordinates"]] if geometry["type"] == "Polygon"
                else geometry["coordinates"] if geometry["type"] == "MultiPolygon" else None)
    if polygons is None:
        raise ValueError("La referencia geográfica tiene un tipo no compatible")
    accepted = any(_in_polygon(longitude, latitude, polygon) for polygon in polygons)
    return {
        "accepted": accepted,
        "location_type": "point",
        "crs": "EPSG:4326",
        "point": {"type": "Point", "coordinates": [longitude, latitude]},
        "pilot_area": "Babahoyo, Los Ríos, Ecuador",
        "boundary_reference": "DPA 2019, cantón 1201; referencia técnica provisional",
        "message": ("Punto dentro de Babahoyo según DPA 2019" if accepted else
                    "El punto está fuera de Babahoyo según DPA 2019"),
    }
