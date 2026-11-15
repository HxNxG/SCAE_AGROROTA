import { loadTemperature } from '../../services/pilotApi.js';
import { mountTimedCellLayer } from './TimedCellLayer.js';

const classes = [
  { minimum: -Infinity, label: '<10', color: '#313695' },
  { minimum: 10, label: '10–<15', color: '#4575b4' },
  { minimum: 15, label: '15–<20', color: '#74add1' },
  { minimum: 20, label: '20–<25', color: '#abd9e9' },
  { minimum: 25, label: '25–<30', color: '#f5cf62' },
  { minimum: 30, label: '30–<35', color: '#ed813e' },
  { minimum: 35, label: '≥35', color: '#b2182b' },
];
const monthFormat = new Intl.DateTimeFormat('es-EC', {
  month: 'long', year: 'numeric', timeZone: 'UTC',
});

export const temperatureLayers = {
  day: { title: 'Temperatura superficial diurna' },
  night: { title: 'Temperatura superficial nocturna' },
};

export function mountTemperature(panel, view, onFrameChange) {
  return mountTimedCellLayer(panel, view, onFrameChange, {
    id: 'temperature', unit: '°C', classes, layers: temperatureLayers,
    timeName: 'mes', dataName: 'la temperatura superficial', loadFrames: loadTemperature, defaultLatest: true,
    formatTime: time => monthFormat.format(new Date(`${time}-01T00:00:00Z`)),
  });
}
