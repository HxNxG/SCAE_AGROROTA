# BioTinder

Sistema web de apoyo a la rotación agrícola en Babahoyo, Los Ríos. Combina datos ambientales, referencias agronómicas ecuatorianas y observaciones del agricultor para comparar arroz, soya y maíz amarillo duro después de un ciclo de arroz.

- [Instrucciones para agentes](AGENTS.md)
- [Guía de trabajo y alcance](docs/GUIA_AGENTES.md)
- [Reglas de los datos del repositorio](../REGLAS.md)

El visor local de Babahoyo muestra la precipitación mensual por celda IMERG y abre la ficha del cantón al seleccionar una ubicación.

## Estructura de la aplicación

| Ruta | Responsabilidad |
| --- | --- |
| [backend/app](backend/app/) | API, contratos de datos, configuración, persistencia y evaluación agronómica. |
| [backend/models_ml](backend/models_ml/) | Referencias a modelos. Los pesos voluminosos se gestionan fuera de Git. |
| [frontend/src](frontend/src/) | Mapa, cuestionario, diagnóstico, comparación y retroalimentación. |
| [docs](docs/) | Guía de implementación y verificación del piloto. |
| [docker-compose.yml](docker-compose.yml) | Plantilla para la futura ejecución conjunta. |

El inventario y los insumos se consultan desde el [índice del repositorio](../README.md#datos-y-evidencia).

## Ejecutar BioTinder localmente

Usa Node.js 22 o posterior y Python 3.11 o posterior. Ejecuta los siguientes bloques en tres terminales, cada una desde la raíz del repositorio.

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

La demostración estática muestra el diagnóstico interactivo de Pimocha con una respuesta guardada. Usa la instalación local para consultar otros escenarios, explorar las capas del mapa o enviar observaciones.

La publicación está preparada en el workflow **BioTinder Pages**. Cuando GitHub permita activar Pages en este repositorio, elige **Settings → Pages → GitHub Actions** y ejecuta el workflow sobre `main`. La dirección prevista es `https://hxnxg.github.io/SCAE_AGROROTA/`.

Abrir <http://127.0.0.1:5173>. Si ese puerto está ocupado, configura `$env:PORT` antes de iniciar Node.js. Seleccionar un punto en el mapa o ingresar longitud y latitud. Por ejemplo, usar longitud `-79.526` y latitud `-1.802`. Tras aceptar el punto, la ficha muestra la serie IMERG de enero de 2010 a septiembre de 2025. La lluvia se resume a escala cantonal. Una ubicación fuera de Babahoyo deja la ficha sin resultados.

- [Referencia geográfica y validación](docs/MAPA_PARCELAS.md)
- [Serie IMERG de Babahoyo y método](../02_clima_temperatura_y_meteorologia/GPM/README.md)

Usa **Reproducir**, **Pausar**, **Anterior** o **Siguiente** para comparar meses. La leyenda aplica los mismos intervalos en milímetros a todo el período. Al seleccionar un punto válido, la ficha muestra el valor de su celda IMERG de 0,1° para el mes activo. El historial promedio cantonal se puede desplegar por separado.

El fondo de [OpenStreetMap](https://www.openstreetmap.org/copyright) requiere conexión a Internet y muestra ríos, vías y poblados. Usa el control de opacidad o desactiva la lluvia para explorar el fondo. Si las teselas fallan, el visor conserva el límite de referencia y la capa de precipitación. El servicio público de teselas se usa según su [política de uso](https://operations.osmfoundation.org/policies/tiles/).

En el selector de capas, **Humedad superficial** y **Humedad radicular** abren un piloto SMAP del 1 de enero de 2025. Elige uno de los ocho intervalos UTC para ver la humedad volumétrica estimada en la malla de 9 km. Consulta la [ficha de la capa SMAP](docs/CAPA_HUMEDAD.md) para conocer las profundidades, la procedencia y la cobertura.

**Temperatura superficial diurna** y **nocturna** muestran compuestos mensuales Terra/MODIS en °C. Las celdas grises carecen de datos válidos según el filtro de calidad. **Satélite** alterna el fondo con una escena NASA del 7 de septiembre de 2025. La fecha de esa imagen es independiente del período de la capa científica.

Para un despliegue público, verifica primero las condiciones de redistribución de la referencia geográfica.
