"""Recopila CSV SMAP por mes mediante subconjuntos nativos OPeNDAP.

Reanudable: los fragmentos validados se reutilizan y un mes solo se publica
cuando todos sus granulos catalogados se han procesado. No descarga HDF globales.
"""
import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path

import earthaccess
import h5py
import numpy as np
import requests

ROOT = Path(__file__).parent
CID = 'C3480440870-NSIDC_CPRD'
FIELDS = ['time_start_utc', 'time_end_utc', 'cell_id', 'sm_surface_m3_m3',
          'sm_rootzone_m3_m3', 'quality_status', 'source_granule']
LOCAL = threading.local()


def dt(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.json.part')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')
    temporary.replace(path)


def catalog(start, end, folder):
    target = folder / 'catalogo_seleccionado.json'
    if target.exists():
        saved = json.loads(target.read_text(encoding='utf-8'))
        if saved['start'] == start and saved['end'] == end:
            return saved['granules']
    selected = {}
    count = 0
    page = 1
    while True:
        response = requests.get('https://cmr.earthdata.nasa.gov/search/granules.json', params={
            'collection_concept_id': CID, 'temporal': start + ',' + end,
            'page_size': 2000, 'page_num': page, 'sort_key[]': ['start_date', 'producer_granule_id']
        }, timeout=90)
        response.raise_for_status()
        entries = response.json()['feed']['entry']
        for entry in entries:
            count += 1
            begin = dt(entry['time_start'])
            if not dt(start) <= begin < dt(end):
                continue
            url = next((x['href'] for x in entry['links'] if 'opendap.earthdata.nasa.gov/collections/' in x['href']), None)
            if not url:
                raise RuntimeError('Falta enlace OPeNDAP: ' + entry['id'])
            name_match = re.search(r'SMAP_L4_SM_gph_\d{8}T\d{6}_Vv\d+_\d+\.h5', entry['title'])
            if not name_match:
                raise RuntimeError('Nombre de granulo desconocido: ' + entry['id'])
            name = name_match.group()
            version, revision = map(int, re.search(r'_Vv(\d+)_(\d+)\.h5', name).groups())
            rank = (version, revision, entry.get('updated', ''), entry['id'])
            key = begin.isoformat()
            record = {'id': entry['id'], 'name': name, 'time_start': entry['time_start'],
                      'time_end': entry['time_end'], 'url': url, 'rank': rank}
            if key not in selected or rank > tuple(selected[key]['rank']):
                selected[key] = record
        if len(entries) < 2000:
            break
        page += 1
    granules = sorted(selected.values(), key=lambda e: e['time_start'])
    atomic_json(target, {'start': start, 'end': end, 'raw_catalog_records': count,
                        'deduplication': 'Por inicio UTC; mayor revision Vv y revision de archivo; updated e ID como desempate.',
                        'granules': granules})
    print('Catalogo:', len(granules), 'intervalos unicos;', count, 'registros', flush=True)
    return granules


def session():
    if not hasattr(LOCAL, 'session'):
        LOCAL.session = earthaccess.__auth__.get_session()
    return LOCAL.session


def fetch(entry, cells, mesh, folder):
    marker = folder / (entry['name'] + '.json')
    fragment = folder / (entry['name'] + '.csv.gz')
    if marker.exists() and fragment.exists():
        result = json.loads(marker.read_text(encoding='utf-8'))
        if result['sha256'] == hashlib.sha256(fragment.read_bytes()).hexdigest():
            return result
    row0, row1, col0, col1 = (mesh[k] for k in ('row_min','row_max','col_min','col_max'))
    section = f'[{row0}:{row1}][{col0}:{col1}]'
    constraint = ';'.join([
        '/Geophysical_Data/sm_surface' + section,
        '/Geophysical_Data/sm_rootzone' + section,
        f'/x[{col0}:{col1}]', f'/y[{row0}:{row1}]', '/EASE2_global_projection'])
    content = None
    for attempt in range(3):
        try:
            response = session().get(entry['url'] + '.dap.nc4', params={'dap4.ce': constraint},
                                     stream=True, timeout=(20, 90))
            response.raise_for_status()
            buffer = io.BytesIO()
            for chunk in response.iter_content(65536):
                buffer.write(chunk)
                if buffer.tell() > 2 * 1024 * 1024:
                    raise RuntimeError('Respuesta supera 2 MiB: no aceptar posible archivo global.')
            response.close()
            content = buffer.getvalue()
            break
        except (requests.RequestException, OSError):
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    with h5py.File(io.BytesIO(content), 'r') as h5:
        source = str(h5.attrs.get('Filename', ''))
        if entry['name'] not in source:
            raise RuntimeError('Granulo recibido no coincide con el catalogo.')
        x, y = h5['x'][:], h5['y'][:]
        indices = [(c['grid_row']-row0, c['grid_col']-col0) for c in cells]
        assert len(x) == col1-col0+1 and len(y) == row1-row0+1
        surface, rootzone = [], []
        masks = []
        for name, output in [('sm_surface', surface), ('sm_rootzone', rootzone)]:
            dataset = h5['Geophysical_Data/' + name]
            unit = dataset.attrs['units']
            if isinstance(unit, bytes):
                unit = unit.decode()
            assert str(unit) == 'm3 m-3'
            array = dataset[:]
            assert array.shape == (len(y), len(x))
            values = np.array([array[r, c] for r, c in indices])
            fill = dataset.attrs['_FillValue']
            invalid = ~np.isfinite(values) | (values == fill)
            outside = ~invalid & ((values < dataset.attrs['valid_min']) | (values > dataset.attrs['valid_max']))
            if np.any(outside):
                raise RuntimeError('Humedad fuera del rango declarado por el producto.')
            output.extend([None if bad else float(v) for v, bad in zip(values, invalid)])
            masks.append(invalid)
        for cell, (r,c) in zip(cells, indices):
            assert abs(x[c] - cell['x_m']) < .01 and abs(y[r] - cell['y_m']) < .01
    temporary = fragment.with_suffix('.part')
    with gzip.open(temporary, 'wt', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS)
        for cell, a, b in zip(cells, surface, rootzone):
            quality = 'valid' if a is not None and b is not None else 'missing_surface_and_rootzone' if a is None and b is None else 'missing_surface' if a is None else 'missing_rootzone'
            if dt('2026-05-14T00:00:00Z') <= dt(entry['time_start']) < dt('2026-07-29T00:00:00Z'):
                quality += ';geolocation_2026_notice_review_required'
            writer.writerow([entry['time_start'], entry['time_end'], cell['cell_id'],
                             '' if a is None else format(a, '.8g'), '' if b is None else format(b, '.8g'), quality, entry['name']])
    temporary.replace(fragment)
    result = {'name': entry['name'], 'time_start': entry['time_start'], 'rows': len(cells),
              'missing_surface': int(masks[0].sum()), 'missing_rootzone': int(masks[1].sum()),
              'bytes_received': len(content), 'bytes_csv_gz': fragment.stat().st_size,
              'sha256': hashlib.sha256(fragment.read_bytes()).hexdigest()}
    atomic_json(marker, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', required=True, help='Fecha UTC inclusiva YYYY-MM-DD')
    parser.add_argument('--end', required=True, help='Fecha UTC exclusiva YYYY-MM-DD')
    parser.add_argument('--workers', type=int, choices=range(1,5), default=4)
    parser.add_argument('--name', default='historico')
    args = parser.parse_args()
    auth = earthaccess.login(strategy='netrc')
    assert auth.authenticated
    start, end = args.start+'T00:00:00Z', args.end+'T00:00:00Z'
    assert dt(start) < dt(end)
    output = ROOT / 'datos' / args.name
    output.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(output).free < 2 * 1024**3:
        raise RuntimeError('Se requieren al menos 2 GiB libres para la recopilacion.')
    mesh = json.loads((ROOT/'geografia/malla_resumen.json').read_text(encoding='utf-8'))
    with (ROOT/'geografia/celdas.csv').open(encoding='utf-8', newline='') as f:
        cells = list(csv.DictReader(f))
    for cell in cells:
        for k in ('grid_row', 'grid_col'):
            cell[k] = int(cell[k])
        for k in ('x_m','y_m'):
            cell[k] = float(cell[k])
    granules = catalog(start, end, output)
    monthly = {}
    for entry in granules:
        monthly.setdefault(entry['time_start'][:7], []).append(entry)
    state = {'requested_start': start, 'requested_end_exclusive': end, 'product': 'SPL4SMGP', 'version': '008',
             'n_cells': len(cells), 'expected_catalog_intervals': len(granules), 'estimated_rows': len(cells)*len(granules),
             'method': 'Subconjuntos nativos DAP4 NetCDF; sin interpolacion; CSV mensual gzip.',
             'geography_reference_year': 2019, 'months': {}, 'status': 'running'}
    status_path = output / 'estado.json'
    atomic_json(status_path, state)
    for month, entries in monthly.items():
        final = output / f'smap_costa_3horas_{month}.csv.gz'
        month_report = output / f'calidad_{month}.json'
        if final.exists() and month_report.exists():
            report = json.loads(month_report.read_text(encoding='utf-8'))
            if report['source_granules'] == [e['name'] for e in entries] and report['sha256'] == hashlib.sha256(final.read_bytes()).hexdigest():
                state['months'][month] = report
                atomic_json(status_path, state)
                continue
        folder = ROOT / 'temporales' / args.name / month
        folder.mkdir(parents=True, exist_ok=True)
        results, failures = [], []
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            pending = {pool.submit(fetch, e, cells, mesh, folder): e for e in entries}
            for future in as_completed(pending):
                entry = pending[future]
                try:
                    results.append(future.result())
                except Exception as exc:
                    # No registrar URL de redireccion, cabeceras ni objetos de sesion.
                    failures.append({'granule': entry['name'], 'error_type': type(exc).__name__})
                if (len(results)+len(failures)) % 8 == 0 or len(results)+len(failures) == len(entries):
                    state['current_month'] = month
                    state['current_month_done'] = len(results)
                    state['current_month_total'] = len(entries)
                    state['current_month_failures'] = failures
                    atomic_json(status_path, state)
                    print(month, len(results), '/', len(entries), 'fallos', len(failures), flush=True)
        if failures:
            state['status'] = 'partial_requires_retry'
            atomic_json(status_path, state)
            raise SystemExit('Mes incompleto; fragmentos conservados para reanudar.')
        results.sort(key=lambda r:r['time_start'])
        temporary = final.with_suffix('.part')
        with gzip.open(temporary, 'wt', newline='', encoding='utf-8') as dest:
            for index, result in enumerate(results):
                with gzip.open(folder / (result['name']+'.csv.gz'), 'rt', newline='', encoding='utf-8') as src:
                    header = src.readline()
                    if index == 0:
                        dest.write(header)
                    shutil.copyfileobj(src, dest)
        temporary.replace(final)
        report = {'source_granules': [e['name'] for e in entries], 'n_intervals': len(results),
                  'rows': sum(r['rows'] for r in results), 'missing_surface': sum(r['missing_surface'] for r in results),
                  'missing_rootzone': sum(r['missing_rootzone'] for r in results),
                  'bytes_received': sum(r['bytes_received'] for r in results), 'bytes_csv_gz': final.stat().st_size,
                  'sha256': hashlib.sha256(final.read_bytes()).hexdigest()}
        atomic_json(month_report, report)
        state['months'][month] = report
        atomic_json(status_path, state)
        # Solo fragmentos generados y regenerables del mes validado, dentro de temporales.
        for result in results:
            for suffix in ('.csv.gz', '.json'):
                (folder / (result['name']+suffix)).unlink()
    actual = {dt(e['time_start']) for e in granules}
    expected = int((dt(end)-dt(start)).total_seconds()/10800)
    missing = []
    point = max(dt(start), dt('2015-03-31T00:00:00Z'))
    while point < dt(end):
        if point not in actual:
            missing.append(point.isoformat())
        point += timedelta(hours=3)
    atomic_json(output/'intervalos_ausentes.json', {'missing_intervals': missing,
                'pre_smap_gap': '2010-01-01 a 2015-03-30 sin SMAP L4', 'requested_3hour_intervals': expected})
    state['status'] = 'completed_catalog_intervals' if not missing else 'completed_with_catalog_gaps'
    state['missing_catalog_intervals'] = len(missing)
    atomic_json(status_path, state)
    print('Finalizado:', state['status'], flush=True)


if __name__ == '__main__':
    main()
