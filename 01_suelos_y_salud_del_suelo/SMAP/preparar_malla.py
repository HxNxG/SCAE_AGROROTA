"""Selecciona huellas nativas SMAP que intersectan las siete provincias."""
import csv
import json
from pathlib import Path

import h5py
import numpy as np
import earthaccess
from pyproj import Transformer
from shapely.geometry import box, shape
from shapely.ops import transform, unary_union
from shapely.prepared import prep

ROOT = Path(__file__).parent
GEO = ROOT / 'geografia'


def write_csv(name, rows):
    with (GEO / name).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    coordinates = GEO / 'malla_coordenadas.nc4'
    if not coordinates.exists():
        auth = earthaccess.login(strategy='netrc')
        assert auth.authenticated
        first = json.loads((ROOT / 'metadatos/primer_granulo.json').read_text(encoding='utf-8'))['feed']['entry'][0]
        url = next(x['href'] for x in first['links'] if 'opendap.earthdata.nasa.gov/collections/' in x['href'])
        response = auth.get_session().get(url+'.dap.nc4', params={'dap4.ce': '/x;/y;/EASE2_global_projection'}, timeout=60)
        response.raise_for_status()
        assert len(response.content) < 1000000 and response.content.startswith(b'\x89HDF')
        coordinates.write_bytes(response.content)
    with h5py.File(coordinates) as h5:
        x, y = h5['x'][:], h5['y'][:]
    dx, dy = float(np.median(np.diff(x))), float(-np.median(np.diff(y)))
    assert np.allclose(np.diff(x), dx) and np.allclose(-np.diff(y), dy)
    forward = Transformer.from_crs(4326, 6933, always_xy=True).transform
    inverse = Transformer.from_crs(6933, 4326, always_xy=True).transform
    features = json.loads((GEO / 'costa_provincias_referencia_2019.geojson').read_text(encoding='utf-8'))['features']
    provinces = [(f['properties'], transform(forward, shape(f['geometry']))) for f in features]
    coast = unary_union([g for _, g in provinces])
    prepared = prep(coast)
    xmin, ymin, xmax, ymax = coast.bounds
    rows = np.where((y + dy/2 > ymin) & (y - dy/2 < ymax))[0]
    cols = np.where((x + dx/2 > xmin) & (x - dx/2 < xmax))[0]
    cells, relations, footprints = [], [], []
    for r in rows:
        for c in cols:
            footprint = box(x[c]-dx/2, y[r]-dy/2, x[c]+dx/2, y[r]+dy/2)
            if not prepared.intersects(footprint):
                continue
            intersections = [(p, g, g.intersection(footprint).area) for p, g in provinces if g.intersects(footprint)]
            intersections = [i for i in intersections if i[2] > 0]
            if not intersections:
                continue
            cell_id = f'EASE2_M09_r{r:04d}_c{c:04d}'
            lon, lat = inverse(x[c], y[r])
            cells.append({'cell_id': cell_id, 'grid_row': int(r), 'grid_col': int(c),
                          'latitude': lat, 'longitude': lon, 'x_m': x[c], 'y_m': y[r],
                          'grid_crs': 'EPSG:6933'})
            footprints.append(footprint)
            for prop, geom, area in intersections:
                relations.append({'cell_id': cell_id, 'provincia_id': prop['DPA_PROVIN'],
                                  'provincia': prop['DPA_DESPRO'], 'intersection_area_m2': area,
                                  'province_area_fraction': area/geom.area,
                                  'cell_area_fraction': area/(dx*dy)})
    assert cells and any(r['provincia_id'] == '12' for r in relations)
    covered = unary_union(footprints)
    checks = []
    for prop, geom in provinces:
        missing = geom.difference(covered).area
        checks.append({'provincia_id': prop['DPA_PROVIN'], 'provincia': prop['DPA_DESPRO'],
                       'n_cells': sum(r['provincia_id'] == prop['DPA_PROVIN'] for r in relations),
                       'missing_area_m2': missing, 'coverage_pct': 100*(1-missing/geom.area)})
        assert missing < 1, f'Hay huecos geometricos en {prop}'
    cantons = json.loads((GEO / 'los_rios_cantones_referencia_2019.geojson').read_text(encoding='utf-8'))['features']
    canton_checks = []
    for feature in cantons:
        geom = transform(forward, shape(feature['geometry']))
        missing = geom.difference(covered).area
        count = sum(geom.intersection(cell).area > 0 for cell in footprints if geom.intersects(cell))
        canton_checks.append({'canton_id': feature['properties']['DPA_CANTON'],
                              'canton': feature['properties']['DPA_DESCAN'], 'n_cells': count,
                              'missing_area_m2': missing, 'coverage_pct': 100*(1-missing/geom.area)})
        assert missing < 1 and count > 0
    write_csv('celdas.csv', cells)
    write_csv('celda_provincia.csv', relations)
    write_csv('cobertura_malla_provincias.csv', checks)
    write_csv('cobertura_malla_los_rios_cantones.csv', canton_checks)
    summary = {'n_cells': len(cells), 'dx_m': dx, 'dy_m': dy,
               'row_min': min(c['grid_row'] for c in cells), 'row_max': max(c['grid_row'] for c in cells),
               'col_min': min(c['grid_col'] for c in cells), 'col_max': max(c['grid_col'] for c in cells),
               'source': 'Coordenadas x/y originales recuperadas mediante OPeNDAP del primer granulo SPL4SMGP v008.',
               'reference_year': 2019, 'coverage': 'Geometrica; no garantiza humedad valida en agua ni en todas las fechas.'}
    (GEO / 'malla_resumen.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
