const snapshots = new Map();

async function loadSnapshot(filename, signal) {
  signal?.throwIfAborted();
  if (snapshots.has(filename)) return snapshots.get(filename);
  const response = await fetch(new URL(`../../climate/${filename}`, import.meta.url), { signal });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  signal?.throwIfAborted();
  snapshots.set(filename, data);
  return data;
}

export function loadMonthlyClimate(signal) {
  return loadSnapshot('imerg-monthly.json', signal);
}

export async function loadPrecipitationCells(month, signal) {
  const { source, unit, bounds, months } = await loadSnapshot('imerg-cells.json', signal);
  const values = months[month];
  return {
    source, unit, month,
    cells: Array.isArray(values) ? bounds.map((extent, index) => ({
      bounds: extent, precipitation_mm: values[index],
    })) : [],
  };
}

async function loadGrid(filename, variable, resolutionKey, signal) {
  const grid = await loadSnapshot(filename, signal);
  const frames = grid.times.map((time, frameIndex) => ({
    time,
    cells: grid.bounds.map((bounds, cellIndex) => ({
      bounds, value: grid.values[variable][frameIndex][cellIndex],
    })),
  }));
  return { source: grid.source, unit: grid.unit, [resolutionKey]: grid[resolutionKey], frames };
}

export function loadMoisture(depth, signal) {
  return loadGrid('smap.json', depth, 'resolution_km', signal);
}

export function loadTemperature(band, signal) {
  return loadGrid('modis.json', band, 'resolution_degrees', signal);
}
