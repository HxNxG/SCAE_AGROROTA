import json
from pathlib import Path

import earthaccess
import h5py

ROOT = Path(__file__).parent
auth = earthaccess.login(strategy='netrc')
entry = json.loads((ROOT / 'metadatos' / 'primer_granulo.json').read_text())['feed']['entry'][0]
url = next(x['href'] for x in entry['links'] if x.get('rel', '').endswith('/data#') and x['href'].endswith('.h5'))
print('Abriendo HDF5 remoto mediante rangos HTTPS...', flush=True)
files = earthaccess.open([url], provider='NSIDC_CPRD', show_progress=False,
                        open_kwargs={'block_size': 262144, 'cache_type': 'blockcache'})
with files[0].f as remote:
    with h5py.File(remote, 'r') as h5:
        report = {}
        def inspect(name, value):
            if isinstance(value, h5py.Dataset):
                report[name] = {'shape': value.shape, 'dtype': str(value.dtype),
                                'chunks': value.chunks,
                                'attrs': {k: str(v) for k, v in value.attrs.items()}}
        h5.visititems(inspect)
        (ROOT / 'metadatos' / 'estructura_hdf5.json').write_text(json.dumps(report, indent=2), encoding='utf8')
        print(json.dumps({k:v for k,v in report.items() if k in ('x','y','cell_lat','cell_lon','cell_row','cell_column','EASE2_global_projection','Geophysical_Data/sm_surface','Geophysical_Data/sm_rootzone')}, indent=2), flush=True)
        for name in ('x', 'y', 'cell_lat', 'cell_lon', 'cell_row', 'cell_column'):
            ds = h5[name]
            print(name, ds[0:2] if ds.ndim == 1 else ds[0:2, 0:2], flush=True)
