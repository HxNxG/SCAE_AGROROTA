# Cobertura y brechas por región

## Actualización SMAP: recopilación iniciada el 14/11/2026

El equipo definió 2010–actualidad como intervalo solicitado. SMAP L4 v8 comienza el 2015-03-31: la ausencia anterior es temporal y propia de esta fuente en todas las regiones. La recopilación inicial obtiene geometrías provinciales de referencia DPA 2019 y los 13 cantones de Los Ríos, más metadatos públicos del catálogo NASA. Faltan autenticación Earthdata, contraste de límites actuales, malla y descarga de humedad. Consultar el [estado de recopilación](../01_suelos_y_salud_del_suelo/SMAP/ESTADO_RECOPILACION.md). Esta actualización sustituye los pendientes de definición temporal indicados en notas previas.

Actualización: NASA POWER dispone de un CSV provisional recibido y revisado para un punto (-2,19; -79,90), del 2020-01-31 al 2025-12-31. El resto de las fuentes sigue pendiente de verificar. Las brechas de esta tabla son necesidades del proyecto, no afirmaciones de inexistencia de información en los proveedores.

| Región | Información que falta en el repositorio | Impacto | Acción y fuentes potenciales | Estado |
| --- | --- | --- | --- | --- |
| Costa | Series de suelo, clima, agua, vegetación, terreno; estadísticas agropecuarias y experiencias locales | No permite formular recomendaciones locales sustentadas todavía | Evaluar las fuentes de las carpetas 01–06; identificar fuentes oficiales ecuatorianas y recopilar testimonios con consentimiento | Pendiente de verificar; no descargado |
| Sierra | Inventario regional, delimitación, productos adecuados y evidencia agropecuaria local | No permite extrapolar recomendaciones de la Costa | Aplicar el instructivo para otras regiones y evaluar fuentes oficiales y locales | Pendiente de verificar; fuera del almacenamiento prioritario |
| Amazonía | Inventario regional, delimitación, productos adecuados y evidencia agropecuaria local | No permite extrapolar recomendaciones de la Costa | Aplicar el instructivo para otras regiones y evaluar fuentes oficiales y locales | Pendiente de verificar; fuera del almacenamiento prioritario |
| Insular | Inventario regional, delimitación, productos adecuados, evidencia local y condiciones aplicables | No permite extrapolar recomendaciones continentales | Aplicar el instructivo y verificar disponibilidad y restricciones locales | Pendiente de verificar; fuera del almacenamiento prioritario |

## Registro detallado para cada evaluación

Agregar una fila por variable y área evaluada; desglosar la Costa por provincia, cantón o área agrícola cuando se inicie un estudio.

| Región / provincia / cantón | Variable o evidencia faltante | Producto y versión evaluados | Período y resolución necesarios | Evidencia de la limitación y fecha de revisión | Impacto agrícola | Fuente potencial y acción | Responsable | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Los Ríos / Babahoyo | Lluvia local por parcela y meses posteriores a 2025-09 | NASA GPM IMERG Final Run V07B, GPM_3IMERGM 07 | 2010-01 a 2025-09, malla 0,1°, resumen cantonal DPA 2019 | Serie IMERG preparada con 189 meses y cobertura cantonal completa; producto satelital no sustituye pluviómetro ni describe variación dentro del cantón; revisado 2026-11-14 | Contexto mensual útil, insuficiente para inundación o calendario de una parcela sin evidencia local | Validar frente a estación INAMHI y añadir meses posteriores cuando estén publicados; integrar como contexto histórico versionado | Pendiente de asignación | Cobertura parcial |
| Por completar | Por completar | Por completar | Por completar | Sin evaluación todavía | Por evaluar | Por definir | Por asignar | Pendiente de verificar |

Usar `cobertura parcial` cuando existan datos con huecos documentados y `ausencia confirmada` únicamente cuando se haya comprobado la falta de la variable o cobertura requerida. Registrar cuándo una brecha queda resuelta y enlazar los metadatos correspondientes.

## Brecha confirmada de NASA POWER

El archivo recibido cubre un único punto y no toda la Costa; 2020 comienza el 31 de enero. Falta definir el período histórico común, ampliar la cobertura espacial requerida y documentar consulta, versión y fecha de descarga. Acción pendiente: el asistente volverá a descargar los datos cuando el equipo acuerde el intervalo. Ver [revisión de utilidad](../02_clima_temperatura_y_meteorologia/NASA_POWER/REVISION_UTILIDAD.md).

## SMAP: diseño revisado, cobertura espacial pendiente

Se documentó el [plan de recopilación CSV](../01_suelos_y_salud_del_suelo/SMAP/PLAN_RECOPILACION_CSV.md). Se propone SPL4SMGP para humedad superficial y radicular, seleccionando celdas que intersecten las siete provincias e incluyendo explícitamente Los Ríos. Falta obtener límites provinciales y cantonales, comprobar cobertura geométrica y disponibilidad válida por fecha, definir el histórico y probar acceso autenticado y conversión. No se han descargado series ni construido una malla.

## NASA GPM IMERG en la Costa

La serie mensual de enero de 2010 a septiembre de 2025 incluye recortes por celda y agregados para siete provincias y 86 cantones. Septiembre de 2025 es el último mes confirmado en el catálogo CMR de IMERG Final V07 y en el servidor ERDDAP consultado. [Datos y metodología](../02_clima_temperatura_y_meteorologia/GPM/README.md).

## Landsat / HLS v2.0 en la Costa

Cobertura parcial. El piloto del 2026-11-14 verifica bandas e índices a 30 m en ventanas de referencia de las siete provincias. HLS L30 empieza en 2013 y HLS S30 en 2015; la fecha inicial efectiva del catálogo puede ser posterior en cada punto. Para construir la serie de vegetación faltan los polígonos de parcela, la consulta de todas las escenas dentro del período y el cálculo de cobertura válida por fecha. Ver [procedimiento y resultados](../04_vegetacion_cultivos_y_monitoreo/LANDSAT/README.md).

## NASA Harvest y GEOGLAM en la Costa

| Área | Brecha | Impacto | Acción | Estado |
| --- | --- | --- | --- | --- |
| Siete provincias de la Costa | Cobertura de informes y máscaras por cultivo y provincia; disponibilidad de calendarios y observaciones de campo | Limita la interpretación de anomalías de vegetación y la validación de sus causas | Revisar el archivo GEOGLAM y el selector GLAM para el cultivo piloto; contrastar con registros oficiales ecuatorianos y observaciones consentidas | Tres recortes GLAD descargados (2008–2019); cobertura de informes y validación de campo pendientes |

Ver el [protocolo de evaluación](../04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST/README.md).

## ECOSTRESS en la Costa

Cobertura parcial verificada por huellas de catálogo en un punto de cada una de las siete provincias, incluido Los Ríos. Primeros gránulos en septiembre de 2018; últimos gránulos piloto en noviembre de 2026 para temperatura superficial y octubre de 2026 para evapotranspiración. Se descargaron siete ventanas piloto. Manabí y Los Ríos tienen píxeles comunes que pasan el filtro aplicado. Falta verificar cobertura por polígono y buscar otras adquisiciones para las cinco ventanas restantes. Ver [consulta y resultados](../03_agua_y_recursos_hidricos/ECOSTRESS/README.md).

## SRTM en la Costa

Elevacion y pendiente verificadas para las siete provincias de referencia. SRTM corresponde a febrero de 2000 y se usa como base de relieve para el periodo 2010-2026. Sigue pendiente la delimitacion de predios para evaluar restricciones por parcela y la verificacion local de cambios posteriores a la adquisicion. Ver [datos y procedimiento](../05_topografia_y_modelado_del_terreno/SRTM/README.md).

## MODIS Terra en la Costa

La serie mensual de enero de 2010 a octubre de 2026 cubre NDVI, EVI y temperatura superficial diurna y nocturna. Los agregados por provincia y cantón incluyen el área válida con filtro de calidad. [Datos y metodología](../04_vegetacion_cultivos_y_monitoreo/MODIS/README.md).

## GRACE/GRACE-FO en la Costa

El recorte de CSR RL06.3 conserva 171 intervalos de enero de 2010 a septiembre de 2026, con anomalías de almacenamiento de agua por celda terrestre y un promedio regional. Hay 32 meses sin fecha central. La resolución efectiva limita su uso a contexto regional. [Datos y metodología](../03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO/README.md).

## Cobertura anual provincial desde 2015

El [recorte ESPAC 2025 del INEC](../07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/README.md) aporta superficie, producción y ventas de 37 productos, uso del suelo y superficies por método de riego y labranza. Cubre las siete provincias. Quedan pendientes las series provinciales anteriores, los calendarios y el detalle cantonal y de parcela.

[MapBiomas Ecuador, Colección 4](../04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/README.md) aporta estadísticas de cobertura por clase para las siete provincias, 2015–2025. La colección aún no cubre 2026. Se descargaron y verificaron 11 mosaicos GeoTIFF de 2015 a 2025 con cobertura de las siete provincias.
