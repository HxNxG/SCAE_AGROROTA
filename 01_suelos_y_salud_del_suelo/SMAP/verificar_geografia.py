"""Valida los limites de referencia y prepara un poligono compacto de consulta."""
import csv
import json
from pathlib import Path

from pyproj import Transformer
from shapely import make_valid
from shapely.geometry import mapping, shape
from shapely.ops import transform, unary_union

ROOT = Path(__file__).parent
GEO = ROOT / 'geografia'


def main():
    provinces = json.loads((GEO / 'costa_provincias_referencia_2019.geojson').read_text(encoding='utf-8-sig'))['features']
    cantons = json.loads((GEO / 'los_rios_cantones_referencia_2019.geojson').read_text(encoding='utf-8-sig'))['features']
    expected = {'07', '08', '09', '12', '13', '23', '24'}
    assert {f['properties']['DPA_PROVIN'] for f in provinces} == expected
    assert len(provinces) == 7 and len(cantons) == 13
    repaired = []
    geoms = {}
    for feature in provinces:
        code = feature['properties']['DPA_PROVIN']
        geom = shape(feature['geometry'])
        if not geom.is_valid:
            repaired.append(code)
            geom = make_valid(geom)
        assert not geom.is_empty and geom.geom_type in ('Polygon', 'MultiPolygon')
        geoms[code] = geom
    coast = unary_union(list(geoms.values()))
    project = Transformer.from_crs('EPSG:4326', 'EPSG:6933', always_xy=True).transform
    los_rios = transform(project, geoms['12'])
    report = []
    canton_geoms = []
    for feature in cantons:
        geom = shape(feature['geometry'])
        originally_valid = geom.is_valid
        geom = transform(project, make_valid(geom))
        canton_geoms.append(geom)
        assert geom.area > 0
        inside = geom.intersection(los_rios).area
        report.append({
            'canton_id': feature['properties']['DPA_CANTON'],
            'canton': feature['properties']['DPA_DESCAN'],
            'original_geometry_valid': originally_valid,
            'area_km2': geom.area / 1e6,
            'area_inside_los_rios_pct': 100 * inside / geom.area,
            'area_outside_los_rios_km2': (geom.area - inside) / 1e6,
        })
    all_cantons = unary_union(canton_geoms)
    summary = {
        'reference_year': 2019,
        'provinces_count': len(provinces), 'los_rios_cantons_count': len(cantons),
        'province_geometries_repaired': repaired,
        'bounding_box_wgs84': list(coast.bounds),
        'los_rios_area_km2': los_rios.area / 1e6,
        'los_rios_area_outside_canton_union_km2': los_rios.difference(all_cantons).area / 1e6,
        'canton_union_outside_los_rios_km2': all_cantons.difference(los_rios).area / 1e6,
        'canton_overlap_area_km2': (sum(g.area for g in canton_geoms) - all_cantons.area) / 1e6,
        'limitations': 'Validacion de referencia DPA 2019; no confirma limites actuales ni cobertura de celdas o humedad SMAP.'
    }
    (GEO / 'costa_union_referencia_2019.geojson').write_text(json.dumps({
        'type': 'FeatureCollection', 'features': [{'type': 'Feature',
        'properties': {'reference_year': 2019, 'purpose': 'consulta_preliminar'},
        'geometry': mapping(coast)}]}, separators=(',', ':')), encoding='utf-8')
    with (GEO / 'verificacion_los_rios_cantones.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(report[0]))
        writer.writeheader()
        writer.writerows(report)
    (GEO / 'verificacion_geografica.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
