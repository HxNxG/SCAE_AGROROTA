import { loadMoisture } from '../../services/pilotApi.js';
import { mountTimedCellLayer } from './TimedCellLayer.js';

const classes = [
  { minimum: 0, label: '0–<0,15', color: '#ad552c' },
  { minimum: 0.15, label: '0,15–<0,25', color: '#e4b161' },
  { minimum: 0.25, label: '0,25–<0,35', color: '#eee6ac' },
  { minimum: 0.35, label: '0,35–<0,45', color: '#58b28e' },
  { minimum: 0.45, label: '≥0,45', color: '#00664f' },
];
const timeFormat = new Intl.DateTimeFormat('es-EC', {
  dateStyle: 'medium', timeStyle: 'short', timeZone: 'UTC',
});

export const moistureLayers = {
  surface: { title: 'Humedad superficial (0–5 cm)' },
  rootzone: { title: 'Humedad radicular (0–100 cm)' },
};

export function mountMoisture(panel, view, onFrameChange) {
  return mountTimedCellLayer(panel, view, onFrameChange, {
    id: 'moisture', unit: 'm³/m³', classes, layers: moistureLayers,
    timeName: 'intervalo', dataName: 'la humedad del suelo', loadFrames: loadMoisture,
    formatTime: time => `${timeFormat.format(new Date(time))} UTC`,
  });
}
