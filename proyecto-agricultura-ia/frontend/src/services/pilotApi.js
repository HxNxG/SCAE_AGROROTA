import * as pages from './pagesClimate.js';
import { isPublicMap, validatePublicPoint } from './pagesGeography.js';

async function request(path, options) {
  const response = await fetch(`/api/v1/${path}`, options);
  if (!response.ok) {
    const error = new Error(`HTTP ${response.status}`);
    error.status = response.status;
    throw error;
  }
  return response.json();
}

export function validatePoint(point, signal) {
  if (isPublicMap) return validatePublicPoint(point, signal);
  return request('parcels/validate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(point),
    signal,
  });
}

export function loadMonthlyClimate(signal) {
  if (isPublicMap) return pages.loadMonthlyClimate(signal);
  return request('climate/babahoyo/monthly', { signal });
}

export function loadPrecipitationCells(month, signal) {
  if (isPublicMap) return pages.loadPrecipitationCells(month, signal);
  return request(`climate/babahoyo/cells?month=${encodeURIComponent(month)}`, { signal });
}

export function loadMoisture(depth, signal) {
  if (isPublicMap) return pages.loadMoisture(depth, signal);
  return request(`climate/babahoyo/moisture?depth=${encodeURIComponent(depth)}`, { signal });
}

export function loadTemperature(band, signal) {
  if (isPublicMap) return pages.loadTemperature(band, signal);
  return request(`climate/babahoyo/temperature?band=${encodeURIComponent(band)}`, { signal });
}
