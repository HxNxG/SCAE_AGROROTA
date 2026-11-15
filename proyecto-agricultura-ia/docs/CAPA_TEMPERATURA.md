# Capa de temperatura superficial de Babahoyo

## Fuente y cobertura comprobada

La primera capa térmica puede usar [MODIS Terra MOD11C3.061](https://doi.org/10.5067/MODIS/MOD11C3.061), el compuesto mensual de temperatura superficial terrestre de NASA. Los [recortes NetCDF4 de la Costa](../../04_vegetacion_cultivos_y_monitoreo/MODIS/MOD11C3/) conservan la malla CMG de 0,05° (aprox. 5,6 km) y contienen las bandas diurna y nocturna y sus controles de calidad. Los 202 archivos versionados van de enero de 2010 a octubre de 2026. Las 61 celdas que tienen intersección de área positiva con Babahoyo se identificaron con el límite cantonal DPA 2019 (1201).

Con el filtro del [agregador existente](../../04_vegetacion_cultivos_y_monitoreo/MODIS/agregar.py), 20 meses diurnos y 22 nocturnos quedan sin ninguna celda válida en Babahoyo. Enero de 2010 tiene 9 celdas diurnas y 17 nocturnas válidas, y octubre de 2026 tiene 1 y 3, respectivamente. Esto confirma la necesidad de mostrar huecos. Los dos [CSV de medias cantonales](../../04_vegetacion_cultivos_y_monitoreo/MODIS/README.md#archivos-y-validación) registran la fracción de área válida por mes. La fracción máxima observada es 91,2 % en diurno y 52,6 % en nocturno, bajo el filtro existente.

NASA POWER aporta temperatura del **aire a 2 m**. Los [ejemplares puntuales](../../02_clima_temperatura_y_meteorologia/NASA_POWER/REVISION_UTILIDAD.md) consultan `[-79.90, -2.19]`, una coordenada fuera de Babahoyo según DPA 2019. Conservarlos como contexto de su ubicación si se muestran. La serie breve cubre 2020-01-31 a 2025-12-31 y existe un [segundo ejemplar](../../01_suelos_y_salud_del_suelo/ISRIC/POWER_Point_Daily_19811001_20260131_002d19S_079d90W_LST.csv) con cabecera 1981-10-01 a 2026-01-31. Su sigla `LST` denota tiempo solar local. [API diaria de NASA POWER](https://power.larc.nasa.gov/docs/services/api/temporal/daily/)

[ECOSTRESS](../../03_agua_y_recursos_hidricos/ECOSTRESS/README.md) ofrece ventanas de temperatura superficial instantánea a 70 m. Los recortes piloto son escenas parciales por provincia. Evaluarlos en una capa de escenas si se verifica una ventana local que cubra el área y su calidad.

## Representación en el visor

- Usar un selector **Temperatura de superficie** con modos **Diurna** y **Nocturna**, fecha mensual, leyenda continua o por intervalos en °C y opacidad ajustable. Mantener los límites de color constantes entre meses y entre ambos modos cuando se quieran comparar sus valores. Definir los umbrales después de revisar la distribución de valores y los extremos por banda. Los colores indican temperatura, sin categorías de estrés agronómico.
- Reutilizar los rectángulos geográficos del visor, con la malla nativa de 0,05° y celdas descartadas transparentes o explícitamente marcadas **Sin dato**. Ampliar el mapa sin inventar detalle espacial. Mantener las etiquetas, el río y las vías visibles debajo de la capa.
- Al seleccionar un punto válido, mostrar temperatura de su celda, período, banda, resolución y procedencia. La ficha secundaria puede mostrar el historial **promedio cantonal de celdas válidas** y su fracción de área válida por mes, identificando la cobertura parcial. Saltar los meses sin medición en la curva y permitir que la barra temporal los seleccione para mostrar el hueco.
- En el recorte, aplicar `raw != 0 && (qc & 3) == 0` por banda y convertir los píxeles válidos con `raw * 0.02 - 273.15`. Revisar extremos y flags de error antes de publicar la leyenda. Un registro puede resultar válido bajo el filtro básico y seguir sujeto a revisión de calidad.

## Contrato API propuesto

El visor actual usa `GET /api/v1/climate/babahoyo/temperature?band=day|night`. Entrega fuente, unidad, resolución y 202 fotogramas mensuales con huellas y valores. Los contratos de abajo quedan como opción si se necesita paginar la capa o añadir el historial cantonal. El recorte se regenera con `python proyecto-agricultura-ia/scripts/build_babahoyo_modis.py`, con h5py, NumPy y Shapely.

Reutilizar la estructura de rectángulos de IMERG conservando el contrato de ese endpoint. Propuesta para FastAPI:

| Consulta | Respuesta |
| --- | --- |
| `GET /api/v1/climate/babahoyo/temperature/cells?month=YYYY-MM&band=day` | `month`, `band`, `unit: "°C"`, `source: "MODIS Terra MOD11C3.061"`, `source_doi`, `resolution_degrees: 0.05`, `status`, `cells`. Cada celda contiene `bounds: [west, south, east, north]` en EPSG:4326, `value_c: number \| null` y `quality: valid \| masked`. |
| `GET /api/v1/climate/babahoyo/temperature/monthly?band=day` | Mismos metadatos de fuente y unidad, más los meses ordenados con `month`, `mean_c: number \| null` y `valid_area_fraction` entre 0 y 1. Las medias provienen de los dos CSV DPA 2019 y su ponderación por área geodésica de intersección. |

`band` admite `day` o `night`. Parámetros inválidos devuelven 422. Para un mes bien formado fuera de cobertura, responder con `status: "out_of_coverage"` y `cells: []`. Dentro del período, conservar la malla y usar `status: "no_data"` cuando todas las celdas estén enmascaradas, o `status: "ok"` cuando exista algún valor válido. Una falla de lectura se informa como error del servicio.

## Verificación para habilitar la capa

Revisar los 202 meses consecutivos en ambas bandas, las 61 celdas y su orden de extensión, y contrastar enero de 2010 y octubre de 2026 con los NetCDF; el filtro debe reproducir los conteos documentados. Probar un mes totalmente enmascarado, uno fuera del período, un punto sobre el borde de celda con asignación determinista y un cambio de banda durante la reproducción. Verificar las medias y la fracción de cobertura de DPA 1201 contra los CSV existentes.
