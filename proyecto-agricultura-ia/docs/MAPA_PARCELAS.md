# Selección de parcelas del piloto

Esta entrega acepta **un punto**, no un polígono predial. GeoJSON usa EPSG:4326 con orden `[longitud, latitud]`. Una ubicación se acepta únicamente si cae dentro o sobre el borde del cantón Babahoyo (código DPA `1201`). El resultado no certifica la ubicación ni el tamaño de una parcela.

## Fuente y transformación

- Original conservado: `../../01_suelos_y_salud_del_suelo/SMAP/geografia/los_rios_cantones_referencia_2019.geojson`, SHA-256 `DDEC0B18BC8A26474E3DA2B12FE7A167FDB2EDE8C47173E3D18CCEA3F7562D4A`.
- Fuente registrada para el original: [servicio cartográfico de EEQ, capa Cantones 30](https://geoportal.eeq.com.ec/arcgis/rest/services/WEBGIS/Visor_cartografia/MapServer/30), campo `DPA_ANIO=2019`. El servicio identifica `Copyright Text: CONALI` y describe límites legales, referenciales y zonas en estudio. La atribución visible debe reconocer a CONALI y citar el servicio EEQ. Al consultar el servicio (2026-11-15) no se encontró una licencia o permiso explícito de redistribución para esta capa; que el servicio y una descarga estén disponibles no demuestra permiso para empaquetar o republicar la geometría. El límite DPA 2019 y el GeoJSON derivado permanecen **provisionales y no autorizados para publicación pública** hasta obtener confirmación escrita sobre las condiciones aplicables.
- Alternativa oficial para actualizar el límite: el Ministerio de Gobierno publica [Organización Territorial Parroquial 2026](https://www.datosabiertos.gob.ec/dataset/organizacion-territorial-parroquial), geoinformación de CONALI con licencia **Creative Commons Attribution (CC BY)**, actualizada el 13-02-2026. Es una fuente candidata para reemplazar el DPA 2019, no una validación de equivalencia geométrica ni legal: antes de adoptarla hay que descargarla, filtrar Babahoyo, revisar metadatos/fecha y validar su geometría frente a la versión actual. El [trámite oficial de límites del Ministerio](https://www.ministeriodegobierno.gob.ec/entrega-del-trazado-de-limites-territoriales-internos-y-organizacion-territorial-del-estado/) diferencia el acceso libre a OTE en Datos Abiertos del trazado de límites entregado por solicitud, cuya publicación digital requiere autorización del Ministerio. Confirmar con el Ministerio si esa condición alcanza al servicio EEQ usado aquí.
- Fondo cartográfico público candidato: el catálogo oficial registra el [Mapa Base Oficial del Ecuador del IGM](https://www.datosabiertos.gob.ec/dataset/mapa-base-oficial-del-ecuador) y el IGM ofrece [WMS regional 1:250.000](https://www.geoportaligm.gob.ec/regional/index.html). Son servicios publicados y técnicamente disponibles para integrarse como fondo; los metadatos consultados no especifican una licencia ni condiciones de atribución/redistribución para el servicio. Por tanto, su uso en una publicación queda **condicionado a confirmar con IGM los términos vigentes y la atribución requerida**. El piloto local puede seguir sin fondo externo mientras se resuelve.
- Cobertura: cantón Babahoyo, Los Ríos. No son datos de cultivo, clima ni mediciones prediales. La verificación geométrica de Los Ríos consta en `../../01_suelos_y_salud_del_suelo/SMAP/geografia/verificacion_geografica.json`.
- `node scripts/build_babahoyo_display.mjs` selecciona el cantón `1201`, simplifica cada anillo con Ramer-Douglas-Peucker (tolerancia `0.0002` grados) y redondea a seis decimales. Genera `frontend/src/components/map/babahoyo-display.json`, 36.446 bytes y 1.592 vértices en esta ejecución. Es solo para visualización. La aceptación se calcula contra el original sin simplificar.

## Integración

- La aplicación FastAPI monta el endpoint `POST /api/v1/parcels/validate`. Recibe `{ "longitude": -79.526, "latitude": -1.802 }` y devuelve `accepted`, el punto en GeoJSON y la referencia oficial usada.
- El selector renderiza la referencia simplificada como SVG y acepta clic o coordenadas. El backend comprueba el punto contra el límite sin simplificar. La ficha de precipitación se muestra tras aceptar la ubicación.
- El historial se obtiene de `GET /api/v1/climate/babahoyo/monthly`. Se presenta como promedio cantonal, con fuente y unidad. El punto seleccionado permite consultar la ficha del área piloto.
- El control temporal obtiene la cobertura del historial y consulta `GET /api/v1/climate/babahoyo/cells?month=AAAA-MM` para dibujar las celdas IMERG originales de 0,1° que intersectan el cantón. Son 22 celdas por mes entre enero de 2010 y septiembre de 2025. La leyenda usa intervalos fijos en milímetros y un color para datos faltantes.
- Para regenerar el recorte desde la raíz del repositorio, ejecuta `python proyecto-agricultura-ia/scripts/build_babahoyo_imerg.py` con Shapely 2. El visor lee el recorte versionado en `backend/app/data/`.
- El servidor de frontend reenvía las solicitudes de la API al backend local. Consulta [los pasos para iniciar la demo](../README.md#ejecutar-la-demo-local).

La API necesita acceso al GeoJSON original y al CSV versionado en la raíz del repositorio. Un paquete que contenga solo `proyecto-agricultura-ia` debe incorporar los insumos conforme a las condiciones de uso.

## Verificación y pendientes

Las pruebas unitarias de geografía comprueban puntos interiores, exteriores, borde y huecos, así como el orden y rango de coordenadas. Verificación documental de M4, consultada el 2026-11-15: capa EEQ ID 30, su atribución `CONALI`, el catálogo oficial de OTE 2026 y el catálogo/servicio de fondo IGM. No se comprobó por descarga ni comparación que la geometría local de 2019 coincida con la capa OTE 2026. Pendiente antes de publicación: resolver por escrito permiso y atribución del DPA 2019/derivado, o migrar y validar la fuente 2026 CC BY; confirmar las condiciones del WMS IGM. Hasta cerrar esos puntos, no presentar el límite 2019 como límite vigente certificado ni publicar una copia derivada.

## Humedad del suelo como capa futura

[Chen y colaboradores (2025)](https://doi.org/10.1016/j.agwat.2025.109353) estimaron la humedad volumétrica de diez estratos hasta 100 cm en el noreste de China, con una malla de salida de 30 m y un intervalo de ocho días. Fusionaron NDVI y temperatura superficial de Landsat y MODIS con ESTARFM y usaron XGBoost con precipitación antecedente, reanálisis, relieve, textura y datos de estaciones. El resultado a 30 m corresponde a un modelo entrenado y evaluado en esa región. La validez de esa resolución y de sus métricas en Babahoyo requiere calibración y evaluación local, incluyendo condiciones de riego y anegamiento.

Para Babahoyo, la capa inicial candidata es [SMAP SPL4SMGP v008](https://nsidc.org/data/spl4smgp/versions/8), con humedad volumétrica superficial (0–5 cm) y de zona radicular (0–100 cm) en su malla nativa de 9 km. Antes de habilitarla, preparar un recorte de meses verificados, publicar fecha, profundidad, unidad y cobertura y conservar los faltantes. Los controles y las leyendas deben distinguir esta variable de la precipitación acumulada IMERG en mm.

Un piloto de estimación a mayor resolución requerirá inventario de mediciones locales, fuentes armonizadas y verificación por sitios y períodos apartados del entrenamiento. Reportar correlación, RMSE, ubRMSE y sesgo por profundidad, además de la cobertura, antes de activar la capa para uso agronómico. La serie regional de SMAP está descrita en su [ficha del repositorio](../../01_suelos_y_salud_del_suelo/SMAP/datos/README.md).

## Capas prioritarias del visor

| Prioridad | Capa | Pregunta que responde |
| --- | --- | --- |
| 1 | Lluvia mensual IMERG | ¿Cuánto llovió en la zona y cómo cambia por mes? |
| 2 | Humedad SMAP superficial y radicular | ¿Qué humedad estima el producto en cada profundidad? El visor cubre el día del piloto. |
| 3 | Temperatura superficial Terra/MODIS diurna y nocturna | ¿Qué temperatura se observó en la superficie? Mantener huecos según el control de calidad. |
| Siguiente | Agua superficial por evento | ¿Dónde hubo agua en una fecha concreta? Verificar un evento con una fuente específica y diferenciarlo de agua habitual y humedad del suelo. |
| Después | Vigor de vegetación HLS | ¿Cómo cambió la cobertura vegetal? Incorporar una escena o serie con control de nubes antes de mostrar índices. |

La [comparación visual de NASA SVS](https://svs.gsfc.nasa.gov/30698) presenta lluvia y humedad en mapas separados. El visor usa una variable activa, con leyenda, fecha y unidad propias. La referencia del [producto IMERG](https://gpm.nasa.gov/data/imerg) distingue tasa de precipitación de acumulación. El visor usa el acumulado mensual.

El botón **Satélite** alterna OpenStreetMap con una escena de reflectancia en color natural del 7 de septiembre de 2025, servida por [NASA EOSDIS GIBS](https://nasa-gibs.github.io/gibs-api-docs/access-basics/) en Web Mercator. Se revisaron cinco fechas en la tesela que contiene el punto de ejemplo y esta escena mostró más terreno visible en esa tesela. La escena puede presentar nubes y tiene su propia fecha, independiente del mes de la capa climática. Se puede [abrir en NASA Worldview](https://worldview.earthdata.nasa.gov/?v=-80,-2.25,-79.1,-1.45&l=MODIS_Terra_CorrectedReflectance_TrueColor&t=2025-09-07).
