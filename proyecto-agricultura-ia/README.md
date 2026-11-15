# BioTinder

BioTinder, prototipo de AgroRota Ecuador, permite explorar condiciones ambientales y comparar el manejo arrocero actual con dos alternativas de rotación en Babahoyo, Los Ríos. El motor usa clima simulado y reglas agronómicas, y guarda las observaciones por separado para revisión.

- [Instrucciones para agentes](AGENTS.md)
- [Guía de trabajo y alcance previsto](docs/GUIA_AGENTES.md)
- [Auditoría de datos, modelo y límites](../docs/data_and_model.md)
- [Reglas de los datos del repositorio](../REGLAS.md)

El visor local de Babahoyo muestra la precipitación mensual por celda IMERG y abre la ficha del cantón al seleccionar una ubicación.

## Estructura de la aplicación

| Ruta | Responsabilidad |
| --- | --- |
| [backend/app](backend/app/) | API de validación geográfica y capas de clima del visor. |
| [API de recomendaciones](../backend/app.py) | Inferencia de escenarios, reglas de rotación y observaciones locales. |
| [Entrenamiento y auditoría del modelo](../backend/ml/) | Entrenador y relectura del modelo versionado de la API de recomendaciones. |
| [frontend/src](frontend/src/) | Mapa, cuestionario, diagnóstico, comparación y retroalimentación. |
| [docs](docs/) | Guía de implementación y verificación del piloto. |
| [docker-compose.yml](docker-compose.yml) | Plantilla vacía. El arranque actual se realiza con los comandos de esta guía. |

El inventario y los insumos se consultan desde la [sección de datos del repositorio](../README.md#data-in-the-prototype).

## Ejecutar BioTinder localmente

Usa Node.js 22 o posterior y Python 3.11–3.13. Ejecuta los siguientes bloques en tres terminales, cada una desde la raíz del repositorio.

```powershell
python -m pip install -r requirements.txt
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

La segunda terminal inicia la API de parcelas y clima.

```powershell
cd proyecto-agricultura-ia/backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

La tercera terminal prepara las capas para uso local e inicia el visor.

```powershell
node proyecto-agricultura-ia/scripts/preparar_cartografia.mjs
$env:BACKEND_URL = 'http://127.0.0.1:8001'
$env:AI_BACKEND_URL = 'http://127.0.0.1:8000'
cd proyecto-agricultura-ia/frontend
npm start
```

La preparación genera primero el límite cantonal desde los datos del repositorio. La descarga de parroquias e inundaciones requiere Internet y, si falla, las demás capas siguen disponibles al iniciar el visor. Consulta la [fuente de susceptibilidad](docs/SUSCEPTIBILIDAD_INUNDACIONES.md).

### Demostración y GitHub Pages

La portada pública muestra el mapa de Babahoyo con zoom, selección de ubicación y capas de lluvia, humedad y temperatura. Consulta la atribución de los [límites públicos CONALI 2026](frontend/pages/cartography/ATTRIBUTION.md). La serie histórica de lluvia conserva el límite DPA 2019 con el que se calculó. Debajo del mapa aparece el diagnóstico interactivo guardado de Pimocha. Para otras consultas de IA, observaciones o la capa de susceptibilidad a inundaciones, usa la instalación local.

Abre la [demo pública de BioTinder](https://hxnxg.github.io/SCAE_AGROROTA/). Para volver a publicarla, ejecuta el [workflow BioTinder Pages](https://github.com/HxNxG/SCAE_AGROROTA/actions/workflows/pages.yml) sobre `main`.

Para compilar la misma portada desde la raíz en un directorio vacío, ejecuta `python proyecto-agricultura-ia/scripts/build_pages.py _site`. El script incluye solo el código del visor, los límites abiertos, los recortes climáticos y el ejemplo guardado.

Abrir <http://127.0.0.1:5173>. Si ese puerto está ocupado, configura `$env:PORT` antes de iniciar Node.js. Seleccionar un punto en el mapa o ingresar longitud y latitud. Por ejemplo, usar longitud `-79.526` y latitud `-1.802`. Tras aceptar el punto, la ficha muestra la serie IMERG de enero de 2010 a septiembre de 2025. La lluvia se resume a escala cantonal. Una ubicación fuera de Babahoyo deja la ficha sin resultados.

- [Referencia geográfica y validación](docs/MAPA_PARCELAS.md)
- [Serie IMERG de Babahoyo y método](../02_clima_temperatura_y_meteorologia/GPM/README.md)

Usa **Reproducir**, **Pausar**, **Anterior** o **Siguiente** para comparar meses. La leyenda aplica los mismos intervalos en milímetros a todo el período. Al seleccionar un punto válido, la ficha muestra el valor de su celda IMERG de 0,1° para el mes activo. El historial promedio cantonal se puede desplegar por separado.

El fondo de [OpenStreetMap](https://www.openstreetmap.org/copyright) requiere conexión a Internet y muestra ríos, vías y poblados. Usa el control de opacidad o desactiva la lluvia para explorar el fondo. Si las teselas fallan, el visor conserva el límite de referencia y la capa de precipitación. El servicio público de teselas se usa según su [política de uso](https://operations.osmfoundation.org/policies/tiles/).

En el selector de capas, **Humedad superficial** y **Humedad radicular** abren un piloto SMAP del 1 de enero de 2025. Elige uno de los ocho intervalos UTC para ver la humedad volumétrica estimada en la malla de 9 km. Consulta la [ficha de la capa SMAP](docs/CAPA_HUMEDAD.md) para conocer las profundidades, la procedencia y la cobertura.

**Temperatura superficial diurna** y **nocturna** muestran compuestos mensuales Terra/MODIS en °C. Las celdas grises carecen de datos válidos según el filtro de calidad. **Satélite** alterna el fondo con una escena NASA del 7 de septiembre de 2025. La fecha de esa imagen es independiente del período de la capa científica.

Para un despliegue público, verifica primero las condiciones de redistribución de la referencia geográfica.
