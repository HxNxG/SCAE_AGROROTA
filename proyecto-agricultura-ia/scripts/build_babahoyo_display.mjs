// Reproducible display-only simplification. Validation uses the full source.
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const project = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.resolve(project, '../01_suelos_y_salud_del_suelo/SMAP/geografia/los_rios_cantones_referencia_2019.geojson');
const target = path.resolve(project, 'frontend/src/components/map/babahoyo-display.json');
const tolerance = 0.0002; // degrees, about 22 m north-south; visualization only
const data = JSON.parse(readFileSync(source, 'utf8'));
const feature = data.features.find(item => item.properties.DPA_CANTON === '1201');
if (!feature || feature.geometry.type !== 'Polygon') throw new Error('Babahoyo DPA 2019 polygon missing');

function distanceSquared(point, first, last) {
  const dx = last[0] - first[0], dy = last[1] - first[1];
  const fraction = dx || dy ? Math.max(0, Math.min(1, ((point[0] - first[0]) * dx + (point[1] - first[1]) * dy) / (dx * dx + dy * dy))) : 0;
  return (point[0] - first[0] - fraction * dx) ** 2 + (point[1] - first[1] - fraction * dy) ** 2;
}

function simplify(line) {
  const keep = new Set([0, line.length - 1]);
  const stack = [[0, line.length - 1]];
  while (stack.length) {
    const [first, last] = stack.pop();
    let index = -1, greatest = tolerance ** 2;
    for (let i = first + 1; i < last; i++) {
      const distance = distanceSquared(line[i], line[first], line[last]);
      if (distance > greatest) { greatest = distance; index = i; }
    }
    if (index >= 0) { keep.add(index); stack.push([first, index], [index, last]); }
  }
  return [...keep].sort((a, b) => a - b).map(index => line[index].map(value => Number(value.toFixed(6))));
}

const coordinates = feature.geometry.coordinates.map(ring => {
  const result = simplify(ring);
  if (result.length < 4) throw new Error('Simplification collapsed a ring');
  return result;
});
const display = {
  type: 'Feature',
  properties: { name: 'Babahoyo', canton_code: '1201', reference_year: 2019, display_only: true },
  geometry: { type: 'Polygon', coordinates },
};
writeFileSync(target, `${JSON.stringify(display)}\n`);
console.log(`Wrote ${target}: ${coordinates.reduce((sum, ring) => sum + ring.length, 0)} vertices`);
