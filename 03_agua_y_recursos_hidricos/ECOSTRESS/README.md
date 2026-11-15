# ECOSTRESS

Prioridad media. ¿Dónde coinciden una superficie más caliente y una evapotranspiración relativamente baja, comparando cultivos y condiciones meteorológicas similares? La coincidencia permite priorizar validación de campo, pero por sí sola no diagnostica déficit hídrico ni prescribe riego.

| Variable | Producto NASA LP DAAC | Resolución nominal |
| --- | --- | --- |
| Temperatura superficial instantánea (K; °C = K − 273,15) | [ECO_L2T_LSTE.002](https://doi.org/10.5067/ECOSTRESS/ECO_L2T_LSTE.002) | 70 m |
| Evapotranspiración estimada, instantánea y diurna (mantener unidades de cada capa según su ficha) | [ECO_L3T_JET.002](https://doi.org/10.5067/ECOSTRESS/ECO_L3T_JET.002) | 70 m |

## Cobertura piloto: 14 de noviembre de 2026

Consulta pública al [catálogo CMR](https://cmr.earthdata.nasa.gov/search/site/collections/directory/LPCLOUD/gov.nasa.eosdis), del 2010-01-01 al 2026-11-14 UTC. Se usó un punto interior por provincia de la [geometría administrativa de referencia DPA 2019](../../01_suelos_y_salud_del_suelo/SMAP/geografia/costa_provincias_referencia_2019.geojson), en EPSG:4326. Los conteos son gránulos cuyas huellas intersectan el punto; no representan días distintos ni garantizan píxeles válidos. El tramo previo a las adquisiciones de la misión queda sin datos ECOSTRESS. No interpolar los vacíos ni llenar con ceros.

| Provincia | LST: gránulos | LST: primera / última fecha UTC | ET: gránulos | ET: primera / última fecha UTC |
| --- | ---: | --- | ---: | --- |
| MANABÍ | 881 | 2018-09-14 / 2026-11-10 | 344 | 2018-09-14 / 2026-10-05 |
| GUAYAS | 660 | 2018-09-14 / 2026-11-09 | 237 | 2018-09-14 / 2026-09-27 |
| SANTA ELENA | 590 | 2018-09-14 / 2026-11-09 | 206 | 2018-09-14 / 2026-09-27 |
| EL ORO | 760 | 2018-09-14 / 2026-11-09 | 268 | 2018-09-14 / 2026-09-27 |
| LOS RÍOS | 523 | 2018-09-14 / 2026-11-05 | 189 | 2018-09-14 / 2026-09-27 |
| ESMERALDAS | 388 | 2018-09-18 / 2026-11-09 | 166 | 2018-09-18 / 2026-10-05 |
| SANTO DOMINGO DE LOS TSÁCHILAS | 1039 | 2018-09-14 / 2026-11-10 | 380 | 2018-09-14 / 2026-10-05 |

Los parámetros, coordenadas e identificadores exactos están en [el resultado JSON](cobertura_piloto_2026-11-14.json). Para repetir desde la raíz, ejecutar el script con Python y las dependencias requests y shapely (disponibles en el entorno del piloto HLS):

~~~powershell
.venv-hls/Scripts/python.exe 03_agua_y_recursos_hidricos/ECOSTRESS/consultar_cobertura.py --corte 2026-11-14
~~~

## Descarga del piloto

Los datos se guardan en [piloto_ecostress_2026-11-14](piloto_ecostress_2026-11-14/). Son 35 GeoTIFF y un manifiesto, 61.286 bytes en total en la primera descarga. Cada ventana mide 33 × 33 píxeles, aproximadamente 2,31 × 2,31 km. Se usaron los puntos interiores de referencia, cuya condición de parcela agrícola no fue comprobada.

Por provincia se guardaron LST (K), ET instantánea PT-JPL-SM (W/m²), QC de LST y una máscara de nubes por producto. La cuenta preliminar de píxeles comunes exige ambas máscaras en cero, los dos bits inferiores de QC en cero, LST positiva y valores finitos presentes para ambas variables. Manabí obtuvo 115 de 1.089 y Los Ríos 272 de 1.089. En las otras cinco ventanas, la adquisición seleccionada obtuvo cero píxeles comunes bajo ese filtro. El [manifiesto](piloto_ecostress_2026-11-14/manifest.json) registra las coordenadas, adquisiciones, CRS, URLs de origen, tamaños y SHA-256.

## Ruta para descargas futuras

Las adquisiciones alternativas completaron el piloto con una ventana con datos válidos en cada una de las siete provincias. El [resumen de ventanas](ventanas_validas_ecostress.csv) registra fechas y cobertura. El [CSV de píxeles](pixeles_comunes_ecostress.csv) reúne 2.218 registros georreferenciados con LST en K y PT-JPL-SM instantánea en W/m². Santa Elena y Santo Domingo de los Tsáchilas aportan tres y dos píxeles, respectivamente. Sigue pendiente ampliar la cobertura espacial y temporal. El [manifiesto de las adquisiciones alternativas](alternativas_ecostress_2026-11-14/manifest.json) registra fuentes y sumas SHA-256.

1. Buscar ECO_L2T_LSTE y ECO_L3T_JET versión 002 en [NASA Earthdata Search](https://search.earthdata.nasa.gov/search). Para repetir el piloto, el script usa CMR y empareja órbita, escena, mosaico y hora UTC, comenzando por candidatos recientes en horario diurno.
2. Configurar el acceso Earthdata Login en el perfil de usuario mediante [el asistente existente](../../01_suelos_y_salud_del_suelo/SMAP/autenticar_earthdata.py). La descarga utiliza la configuración local de requests y las redirecciones de LP DAAC.
3. Ejecutar desde la raíz con el entorno del piloto HLS, o con Python más numpy, rasterio, requests y shapely.

~~~powershell
.venv-hls/Scripts/python.exe 03_agua_y_recursos_hidricos/ECOSTRESS/descargar_piloto.py
~~~

El script usa los parámetros del JSON de cobertura de este piloto y guarda las ventanas en la carpeta indicada arriba. Lee los COG por rangos HTTP. Para otro corte o puntos, generar la consulta de cobertura correspondiente y actualizar la entrada y carpeta de salida en el script. Para obtener observaciones útiles en las cinco ventanas restantes, buscar otras adquisiciones y verificar las mismas máscaras.

[Documentación de productos y calidad de NASA/JPL](https://ecostress.jpl.nasa.gov/data/atbds-summary-table).
