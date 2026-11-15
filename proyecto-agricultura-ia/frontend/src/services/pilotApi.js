async function request(path, options) {
  const response = await fetch(`/api/v1/${path}`, options);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

export function validatePoint(point, signal) {
  return request('parcels/validate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(point),
    signal,
  });
}

export function loadMonthlyClimate(signal) {
  return request('climate/babahoyo/monthly', { signal });
}

export function loadPrecipitationCells(month, signal) {
  return request(`climate/babahoyo/cells?month=${encodeURIComponent(month)}`, { signal });
}

export function loadMoisture(depth, signal) {
  return request(`climate/babahoyo/moisture?depth=${encodeURIComponent(depth)}`, { signal });
}

export function loadTemperature(band, signal) {
  return request(`climate/babahoyo/temperature?band=${encodeURIComponent(band)}`, { signal });
}
