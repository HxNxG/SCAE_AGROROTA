import { mountParcelSelector } from './components/map/ParcelSelector.js';
import { mountPrecipitation } from './components/map/PrecipitationLayer.js';
import { moistureLayers, mountMoisture } from './components/map/MoistureLayer.js';
import { temperatureLayers, mountTemperature } from './components/map/TemperatureLayer.js';
import { mountCellReading } from './components/map/CellReading.js';
import { mountRecommendations } from './components/recommendations.js';
import { mountFloodSusceptibility } from './components/map/FloodSusceptibility.js';

const app = document.querySelector('#app');
app.innerHTML = `
<main id="visor" class="visor" aria-labelledby="map-title">
  <div id="parcel-map" class="parcel-map">
    <p role="status">Cargando mapa de Babahoyo…</p>
  </div>

  <header class="map-heading">
    <div class="brand">BioTinder</div>
    <h1 id="map-title">Babahoyo</h1>
    <p>Los Ríos, Ecuador</p>
    <label class="poi-selector" hidden>Área de interés
      <select id="poi-selector"><option value="">Todo Babahoyo</option></select>
    </label>
    <a class="recommendations-link" href="#recommendations">Recomendaciones de cultivo</a>
    <label class="layer-chooser" hidden>Capa
      <select id="climate-layer">
        <option value="precipitation">Lluvia mensual</option>
        <option value="surface">${moistureLayers.surface.title}</option>
        <option value="rootzone">${moistureLayers.rootzone.title}</option>
        <option value="day">${temperatureLayers.day.title}</option>
        <option value="night">${temperatureLayers.night.title}</option>
        <option value="flood">Susceptibilidad a inundaciones</option>
      </select>
    </label>
  </header>

  <div class="map-controls" role="group" aria-label="Controles del mapa" hidden>
    <button type="button" data-map-control="zoom-in" aria-label="Acercar" title="Acercar">+</button>
    <button type="button" data-map-control="zoom-out" aria-label="Alejar" title="Alejar">−</button>
    <button type="button" data-map-control="reset" aria-label="Restablecer vista" title="Restablecer vista">⌂</button>
  </div>

  <section id="rain-panel" class="rain-panel" aria-label="Capa de precipitación" hidden>
    <div class="rain-heading">
      <label for="rain-month">Precipitación mensual</label>
      <output id="rain-month-label" for="rain-month"></output>
    </div>
    <div class="rain-layer-controls">
      <label><input id="rain-visible" type="checkbox" checked> Mostrar capa</label>
      <label class="rain-opacity">Opacidad
        <input id="rain-opacity" type="range" min="10" max="100" step="5" value="60">
        <output id="rain-opacity-value" for="rain-opacity">60 %</output>
      </label>
    </div>
    <div class="rain-timeline">
      <div class="rain-transport" role="group" aria-label="Reproducción mensual">
        <button id="rain-previous" type="button" aria-label="Mes anterior" title="Mes anterior" disabled>‹</button>
        <button id="rain-playback" type="button" disabled>Reproducir</button>
        <button id="rain-next" type="button" aria-label="Mes siguiente" title="Mes siguiente" disabled>›</button>
      </div>
      <input id="rain-month" type="range" min="0" max="0" step="1" disabled>
    </div>
    <ul id="rain-legend" class="rain-legend cell-legend" aria-label="Leyenda de lluvia en milímetros"></ul>
    <p id="rain-status" role="status"></p>
    <button id="rain-retry" type="button" hidden>Reintentar</button>
    <p id="rain-source" class="rain-source"></p>
  </section>

  <section id="moisture-panel" class="frame-panel" aria-labelledby="moisture-heading" hidden>
    <h2 id="moisture-heading"></h2>
    <label class="frame-time-control">Inicio del intervalo (UTC)
      <select id="moisture-time" disabled></select>
    </label>
    <ul id="moisture-legend" class="moisture-legend cell-legend" aria-label="Leyenda de humedad en metros cúbicos por metro cúbico"></ul>
    <p class="rain-source">Malla de 9 km · Intervalos de 3 horas</p>
    <p id="moisture-status" role="status"></p>
    <button id="moisture-retry" type="button" hidden>Reintentar</button>
    <p id="moisture-source" class="rain-source"></p>
  </section>

  <section id="temperature-panel" class="frame-panel" aria-labelledby="temperature-heading" hidden>
    <h2 id="temperature-heading"></h2>
    <label class="frame-time-control">Mes
      <select id="temperature-time" disabled></select>
    </label>
    <ul id="temperature-legend" class="temperature-legend cell-legend" aria-label="Leyenda de temperatura superficial en grados Celsius"></ul>
    <p class="rain-source">Malla de 0,05° · Compuesto mensual</p>
    <p id="temperature-status" role="status"></p>
    <button id="temperature-retry" type="button" hidden>Reintentar</button>
    <p id="temperature-source" class="rain-source"></p>
  </section>

  <p class="map-attribution">
    © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap contributors</a>
    <span> · Cantón: CONALI 2019, vía EEQ</span>
    <span> · <a href="https://sgrportal.gestionderiesgos.gob.ec/server/rest/services/Hosted/OT_PARROQUIAL/FeatureServer/0" target="_blank" rel="noopener">Parroquias: CONALI 2023</a></span>
  </p>
  <section id="flood-panel" class="frame-panel" aria-labelledby="flood-heading" hidden>
    <h2 id="flood-heading">Susceptibilidad a inundaciones</h2>
    <ul id="flood-legend" class="cell-legend" aria-label="Niveles de susceptibilidad"></ul>
    <p>Susceptibilidad del terreno. No indica inundación activa ni es un pronóstico.</p>
    <p><a href="https://sgrportal.gestionderiesgos.gob.ec/server/rest/services/Susceptibilidad_de_Inundaciones/MapServer/0" target="_blank" rel="noopener">Fuente: CONAGE 2024 · Geoportal de Gestión de Riesgos</a></p>
    <p id="flood-status" role="status"></p>
  </section>

  <button class="panel-toggle primary" type="button" aria-controls="location-panel" aria-expanded="false">
    Consultar ubicación
  </button>

  <section id="location-panel" class="location-panel" aria-labelledby="location-title" hidden>
    <div class="panel-heading">
      <h2 id="location-title">Consultar ubicación</h2>
      <button class="panel-close" type="button" aria-label="Cerrar ficha" title="Cerrar ficha">×</button>
    </div>
    <p class="map-instructions">Selecciona un punto en el mapa o ingresa sus coordenadas WGS 84.</p>
    <form id="parcel-form">
      <div class="coordinate-fields">
        <label class="field" for="longitude"><span>Longitud</span><input id="longitude" name="longitude" type="number" min="-180" max="180" step="any" placeholder="-79.526" required></label>
        <label class="field" for="latitude"><span>Latitud</span><input id="latitude" name="latitude" type="number" min="-90" max="90" step="any" placeholder="-1.802" required></label>
      </div>
      <button class="primary" type="submit">Validar coordenadas</button>
    </form>
    <p id="parcel-status" class="map-caption" role="status">Selecciona un punto para validar su pertenencia al área piloto.</p>

    <section id="climate-card" class="climate-card" aria-labelledby="climate-title" hidden>
      <h3 id="climate-title">Precipitación en la celda</h3>
      <div class="cell-reading">
        <p id="cell-month"></p>
        <p id="cell-value">Sin fecha disponible</p>
      </div>
      <p class="cell-source">IMERG mensual · Celda de 0,1°</p>
      <details id="climate-history-details" class="climate-history-details">
        <summary>Historial promedio del cantón</summary>
        <p>Promedio cantonal de Babahoyo en milímetros.</p>
        <p id="climate-source" hidden></p>
        <details id="climate-method" hidden>
          <summary>Escala y método del promedio</summary>
          <p id="climate-scale"></p>
        </details>
        <p id="climate-status" role="status"></p>
        <figure id="climate-history-chart" class="climate-history-chart" hidden></figure>
        <section id="climate-rain-outlook" class="climate-rain-outlook" hidden></section>
        <div id="climate-history-container" class="climate-history" tabindex="0" role="region" aria-labelledby="climate-history-caption" hidden>
          <table id="climate-history">
            <caption id="climate-history-caption">Historial de precipitación mensual</caption>
            <thead><tr><th scope="col">Mes (AAAA-MM)</th><th scope="col">Precipitación (mm)</th></tr></thead>
            <tbody></tbody>
          </table>
        </div>
      </details>
    </section>
  </section>
</main>
<section id="recommendations" class="pico" data-theme="light" aria-labelledby="recommendations-title"></section>`;

mountRecommendations(app.querySelector('#recommendations'));
app.querySelector('#poi-selector').addEventListener('change', event => {
  if (event.target.value) app.querySelector('#recommendations select[name="zona"]').value = event.target.value;
});

const rainReading = {
  title: 'Precipitación en la celda', source: 'IMERG mensual · Celda de 0,1°',
  unit: 'mm', field: 'precipitation_mm',
};
const cell = mountCellReading(app.querySelector('#climate-card'));
cell.setLayer(rainReading);
const view = await mountParcelSelector(app.querySelector('#visor'), cell.setPoint);
if (view) {
  const chooser = app.querySelector('.layer-chooser');
  const selection = chooser.querySelector('#climate-layer');
  const setRain = mountPrecipitation(app.querySelector('#rain-panel'), {
    project: view.project, layer: view.layer.querySelector('#rain-layer'),
  }, cell.setFrame);
  const setMoisture = mountMoisture(app.querySelector('#moisture-panel'), {
    project: view.project, layer: view.layer.querySelector('#moisture-layer'),
  }, cell.setFrame);
  const setTemperature = mountTemperature(app.querySelector('#temperature-panel'), {
    project: view.project, layer: view.layer.querySelector('#temperature-layer'),
  }, cell.setFrame);
  const setFlood = mountFloodSusceptibility(app.querySelector('#flood-panel'), {
    project: view.project, layer: view.layer.querySelector('#flood-layer'),
  });

  selection.addEventListener('change', () => {
    const mode = selection.value;
    const moisture = moistureLayers[mode];
    const temperature = temperatureLayers[mode];

    if (mode !== 'precipitation') setRain(false);
    if (!moisture) setMoisture(null);
    if (!temperature) setTemperature(null);
    setFlood(mode === 'flood');

    if (mode === 'flood') {
      cell.setLayer({
        title: 'Susceptibilidad a inundaciones', source: 'CONAGE 2024 · Consulta la leyenda del mapa',
        staticMessage: 'Selecciona una parroquia para enfocar la capa.',
      });
    } else if (temperature) {
      cell.setLayer({ ...temperature, source: 'MODIS Terra mensual · Celda de 0,05°', unit: '°C', field: 'value' });
      setTemperature(mode);
    } else if (moisture) {
      cell.setLayer({ ...moisture, source: 'SMAP L4 · Celda de 9 km', unit: 'm³/m³', field: 'value' });
      setMoisture(mode);
    } else {
      cell.setLayer(rainReading);
      setRain(true);
    }
  });
  chooser.hidden = false;
  setRain(true);
}
