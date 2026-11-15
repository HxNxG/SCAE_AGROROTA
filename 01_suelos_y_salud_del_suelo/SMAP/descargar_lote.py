"""Prueba autenticada de recorte Harmony. Conserva el estado para reanudar."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

import earthaccess
import requests

ROOT = Path(__file__).parent
CID = 'C3480440870-NSIDC_CPRD'
STATE = ROOT / 'metadatos' / 'lote_prueba_harmony.json'


def save(value):
    STATE.write_text(json.dumps(value, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--submit', action='store_true')
    args = parser.parse_args()
    auth = earthaccess.login(strategy='netrc')
    if not auth.authenticated:
        raise SystemExit('Earthdata no autenticado')
    session = auth.get_session()
    if args.submit and not STATE.exists():
        # Solo un intervalo de tres horas, para verificar toda la cadena antes del historico.
        params = [
            ('subset', 'lat(-4.0:1.6)'), ('subset', 'lon(-81.2:-78.3)'),
            ('subset', 'time("2025-01-01T00:00:00Z":"2025-01-01T02:59:59Z")'),
            ('format', 'application/netcdf'), ('forceAsync', 'true'),
            ('maxResults', '1'), ('skipPreview', 'true'), ('ignoreErrors', 'false'),
        ]
        variables = 'V3707348718-NSIDC_CPRD,V3707348437-NSIDC_CPRD'
        url = f'https://harmony.earthdata.nasa.gov/{CID}/ogc-api-coverages/1.0.0/collections/{variables}/coverage/rangeset'
        response = session.get(url, params=params, timeout=45)
        if response.status_code not in (200, 201, 202):
            print('Error Harmony', response.status_code, response.text[:1800])
            raise SystemExit(1)
        data = response.json()
        job_id = data.get('jobID') or data.get('jobId')
        if not job_id:
            print('Respuesta sin identificador:', list(data))
            raise SystemExit(1)
        state = {'job_id': job_id, 'collection': CID, 'params': params,
                 'status': data.get('status'), 'note': 'Caja ampliada para incluir celdas de borde; recorte poligonal local pendiente.'}
        save(state)
    if not STATE.exists():
        raise SystemExit('Usar --submit para iniciar la prueba.')
    state = json.loads(STATE.read_text(encoding='utf-8'))
    response = session.get(f'https://harmony.earthdata.nasa.gov/jobs/{state["job_id"]}', timeout=60)
    response.raise_for_status()
    data = response.json()
    state['status'] = data.get('status')
    state['progress'] = data.get('progress')
    if data.get('message'):
        state['message'] = data['message']
    save(state)
    print(json.dumps({k: state[k] for k in ('job_id', 'status', 'progress') if k in state}))
    if state['status'] not in ('successful', 'complete', 'completed'):
        return
    # Enlaces firmados solo se utilizan en memoria; no guardarlos en manifiestos.
    links = [x for x in data.get('links', []) if x.get('rel') == 'data']
    if not links:
        print('Sin enlaces de datos en respuesta del trabajo; revisar catalogo STAC.')
        return
    folder = ROOT / 'temporales' / 'lote_prueba'
    folder.mkdir(parents=True, exist_ok=True)
    files = []
    for index, link in enumerate(links):
        url = link['href']
        if urlparse(url).scheme != 'https':
            continue
        target = folder / f'subset_{index:02d}.nc4'
        if not target.exists():
            download = requests.get(url, stream=True, timeout=120)
            download.raise_for_status()
            size = 0
            with target.with_suffix('.part').open('wb') as output:
                for chunk in download.iter_content(1024 * 1024):
                    size += len(chunk)
                    if size > 50 * 1024 * 1024:
                        raise RuntimeError('Recorte supera limite de prueba de 50 MiB; revisar antes de continuar.')
                    output.write(chunk)
            target.with_suffix('.part').replace(target)
        files.append({'path': str(target.relative_to(ROOT)), 'bytes': target.stat().st_size})
    state['downloaded_files'] = files
    save(state)
    print(json.dumps(files))


if __name__ == '__main__':
    main()
