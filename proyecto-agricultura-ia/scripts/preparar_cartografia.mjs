import './build_babahoyo_display.mjs';
import { writeFile } from 'node:fs/promises';

const portal = 'https://sgrportal.gestionderiesgos.gob.ec/server/rest';
const map = new URL('../frontend/src/components/map/', import.meta.url);

async function download(url) {
  const response = await fetch(url, { signal: AbortSignal.timeout(30000) });
  if (!response.ok) throw new Error(`HTTP ${response.status} al consultar ${url}`);
  return response;
}

async function parishes() {
  const query = new URLSearchParams({
    where: "dpa_parroq LIKE '1201%' AND dpa_anio = '2023'",
    outFields: 'dpa_parroq,dpa_anio,dpa_despar',
    outSR: '4326', geometryPrecision: '6', maxAllowableOffset: '0.0001', f: 'geojson',
  });
  const response = await download(`${portal}/services/Hosted/OT_PARROQUIAL/FeatureServer/0/query?${query}`);
  const data = await response.json();
  const codes = data.features?.map(f => f.properties.dpa_parroq).sort().join(',');
  if (codes !== '120150,120152,120153,120154,120155') {
    throw new Error('El servicio no devolvió las cinco unidades DPA de Babahoyo de 2023.');
  }
  await writeFile(new URL('babahoyo-parroquias-2023.json', map), JSON.stringify(data));
}

async function susceptibility() {
  const query = new URLSearchParams({
    bbox: '-8873276.61,-248305.16,-8819843.26,-178134.34',
    bboxSR: '3857', imageSR: '3857', size: '1024,1344',
    format: 'png32', transparent: 'true', layers: 'show:0', dpi: '24', f: 'json',
  });
  const response = await download(`${portal}/services/Susceptibilidad_de_Inundaciones/MapServer/export?${query}`);
  const { href, extent } = await response.json();
  const expected = { xmin: -8873291.675952379, ymin: -248305.16, xmax: -8819828.194047617, ymax: -178134.34 };
  if (!href || !extent || Object.entries(expected).some(([key, value]) => Math.abs(extent[key] - value) > 1)) {
    throw new Error('La exportación oficial cambió de extensión.');
  }
  const image = Buffer.from(await (await download(href)).arrayBuffer());
  if (image.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a' || image.length < 10000) {
    throw new Error('La exportación no contiene un recorte PNG utilizable.');
  }
  await writeFile(new URL('babahoyo-flood-2024.png', map), image);
}

for (const [label, result] of (await Promise.allSettled([parishes(), susceptibility()])).entries()) {
  const name = ['Límites parroquiales', 'Susceptibilidad a inundaciones'][label];
  if (result.status === 'fulfilled') console.log(`${name}: listo`);
  else {
    console.error(`${name}: ${result.reason.message}`);
    process.exitCode = 1;
  }
}
