# Informe de datos y variables de Field Shift

**Corte del inventario local:** 14 de noviembre de 2026. **Ámbito:** Esmeraldas, Manabí, Santo Domingo de los Tsáchilas, Los Ríos, Guayas, Santa Elena y El Oro. La meta histórica del proyecto es 2010–actualidad. Las fechas de cada producto indican el tramo almacenado o documentado, con los huecos que se señalan.

## Fuentes y cobertura

| Familia | Datos y variables locales | Escala, período y estado |
| --- | --- | --- |
| [SoilGrids 2.0](01_suelos_y_salud_del_suelo/ISRIC/README.md) | pH en agua, arena, limo, arcilla, carbono orgánico y nitrógeno total. Media y cuantiles 0,05, 0,50 y 0,95 por propiedad y profundidad. | 144 capas estáticas a 250 m para 0–5, 5–15, 15–30, 30–60, 60–100 y 100–200 cm. Valores modelados. Consultar el manifiesto y aplicar las escalas de almacenamiento por propiedad. |
| [SMAP SPL4SMGP v008](01_suelos_y_salud_del_suelo/SMAP/datos/README.md) | Humedad volumétrica superficial de 0–5 cm y de zona radicular de 0–100 cm, en m³/m³. Incluye estado de validez y agregados provinciales. | 1.045 celdas de 9 km e intervalos de 3 h. Meses registrados como verificados entre marzo de 2015 y septiembre de 2019 en la lectura del anexo, más prueba del 1 de enero de 2025. Octubre de 2019 tenía insumos temporales. La recopilación avanzó durante la inspección y los conteos reflejan ese corte. Marzo de 2015 comienza el día 31. |
| [NASA POWER](02_clima_temperatura_y_meteorologia/NASA_POWER/REVISION_UTILIDAD.md) | Temperatura del aire a 2 m media, máxima y mínima (°C), precipitación corregida (mm/día), radiación solar de onda corta (MJ/m²/día), viento a 2 m (m/s) y humedad relativa a 2 m (%). | Dos CSV diarios superpuestos para el mismo punto (−2,19°, −79,90°). El largo, guardado bajo ISRIC, va de 1981-10-01 a 2026-01-31. El corto va de 2020-01-31 a 2025-12-31. Conservar la convención LST del archivo y tratar −999 como faltante. Cobertura regional multipunto pendiente. |
| [GPM IMERG Final V07B](02_clima_temperatura_y_meteorologia/GPM/README.md) | Precipitación, índice de calidad y error aleatorio por celda. Agregados con acumulado medio en mm, área y fracción cubierta. | 0,1°, mensual, 2010-01 a 2025-09 en dos tramos. Agregados para las siete provincias y 86 cantones, más subconjunto de Los Ríos. El error medio por celda tiene una interpretación distinta a la incertidumbre del agregado. |
| [ECOSTRESS](03_agua_y_recursos_hidricos/ECOSTRESS/README.md) | Temperatura superficial LST (K), flujo de evapotranspiración instantánea PT-JPL-SM (W/m²), QC L2 y máscaras de nubes L2/L3. CSV con ventanas y píxeles comunes. | Escenas irregulares a 70 m. Los CSV finales registran ocho ventanas con píxeles comunes en las siete provincias, con 2 a 841 píxeles válidos de 1.089 por ventana. La evapotranspiración instantánea requiere conversión y supuestos temporales para expresarla como lámina diaria. |
| [CSR GRACE/GRACE-FO RL06.3](03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO/README.md) | Anomalía del almacenamiento terrestre total en cm equivalentes de agua, fechas de solución, celdas y áreas válidas. | Serie aproximadamente mensual 2010-01 a 2026-09 con huecos. Grilla de 0,25° y soporte efectivo del orden de 300 km. Uso exploratorio macrorregional. |
| [HLS L30 y S30 v2.0](04_vegetacion_cultivos_y_monitoreo/LANDSAT/README.md) | Reflectancia, Fmask, NDVI, EVI2 y NDMI. El anexo indica los nombres y el orden de las bandas. | Pilotos a 30 m en ventanas de 33 × 33 píxeles alrededor de puntos provinciales. La carpeta piloto_hls_qa contiene los recortes con control de calidad. La fecha por escena consta en los manifiestos y nombres. El histórico y los recortes por predio están pendientes. |
| [MODIS Terra](04_vegetacion_cultivos_y_monitoreo/MODIS/README.md) | MOD13C2.061 con NDVI, EVI y VI Quality. MOD11C3.061 con LST diurna y nocturna y sus QC. Los CSV incorporan media, área y fracción válida. | 0,05°, mensual 2010-01 a 2026-10. 202 NetCDF4 por producto y agregados por provincia y cantón. Índices brutos × 0,0001 y temperaturas brutas × 0,02 K, tras filtrar rellenos y QA. |
| [GLAD / NASA Harvest](04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST/README.md) | Máscara histórica de extensión cultivada y documentación metodológica GEOGLAM. | Tres GeoTIFF a 30 m con etiquetas 2011, 2015 y 2019. Representan épocas multianuales. |
| [MapBiomas Ecuador C4](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/README.md) | Clase de cobertura y uso del suelo, jerarquía de clases y superficie en hectáreas. | Tablas anuales 2010–2025 para provincias, cantones y parroquias CONALI 2024. Once GeoTIFF anuales 2015–2025 a ~30 m. La tabla provincial adicional 2015–2025 se superpone con la serie larga. |
| [SRTMGL1 v003](05_topografia_y_modelado_del_terreno/SRTM/README.md) | Elevación (m), pendiente (°) y estadísticas por cantón con mínimo, p10, p50, p90, máximo y cobertura válida. | Dos GeoTIFF de la Costa a ~31 m nominal. Elevación de la misión de febrero de 2000 y pendiente derivada. |
| [ESPAC / INEC](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/README.md) | Producto y condición de cultivo, superficies sembrada/plantada y cosechada (ha), producción y ventas (t), rendimiento derivado (t/ha). En 2025 también uso del suelo, superficie regada por método y labranza de transitorios (ha). | Estimaciones anuales por provincia. Cultivos 2010–2025. Riego, labranza y uso de suelo corresponden a 2025. Se conservan hoja y fila del tabulado y los valores ausentes. |
| [Geografía DPA 2019](01_suelos_y_salud_del_suelo/SMAP/geografia/) | Límites de la Costa, provincias, cantones y Los Ríos. Malla SMAP, intersecciones celda–provincia, áreas y controles de cobertura. | GeoJSON y CSV auxiliares. Los códigos DPA se deben guardar como texto para preservar ceros iniciales. |
| Fichas agronómicas locales ([Libro11.xlsx](07_informacion_agropecuaria_ecuatoriana/Libro11.xlsx), [DATOS_ARROZ_SOYA.xlsx](07_informacion_agropecuaria_ecuatoriana/DATOS_ARROZ_SOYA.xlsx)) | Ciclo, agua, temperatura, suelo, rendimiento, sanidad y rasgos varietales. | Referencias para cultivos de la Costa y la cuenca del Guayas, con menciones territoriales por variedad. Las tablas carecen de fecha de ensayo, identificador de predio y registros anuales. |

## Integración y brechas

- Para análisis territorial, unir por código DPA y período y comprobar la versión de los límites. MapBiomas usa CONALI 2024 y varias fuentes satelitales usan DPA 2019. En GeoJSON y tablas auxiliares se mantienen los identificadores originales para rastrear esas uniones.
- Para análisis temporal, distinguir fechas de escena, meses de agregación y años de referencia. Los extremos impresos en el anexo son rangos observados y pueden contener huecos. Verificar claves, vigencia y fracción válida antes de combinar series.
- Para análisis predial, HLS, SRTM, MapBiomas y ECOSTRESS aportan detalle nominal de decenas de metros con condiciones de calidad y cobertura. POWER, IMERG, SMAP, MODIS, GRACE y ESPAC aportan contexto a escalas regionales o administrativas. Separar temperatura del aire de temperatura superficial y cobertura cartografiada de superficie estimada por encuesta.
- Las fuentes aún tienen brechas de histórico y validación local. Faltan observaciones de finca, geometrías prediales, inventarios operativos de riego y drenaje, calendarios agrícolas y [testimonios de agricultores](08_experiencias_de_agricultores/README.md). Worldview, Giovanni, AppEEARS y VEDA están documentados como herramientas de consulta y procesamiento en [visualización y GIS](06_visualizacion_exploracion_y_gis/).
- La inspección cubre presencia de archivos, encabezados, rangos observados en CSV y metadatos de GeoTIFF. Para NetCDF y variables físicas se usaron las fichas y manifiestos locales. Los controles de exactitud, licencia y procedencia por producto se amplían en la [auditoría de Field Shift](FIELD_SHIFT_AUDITORIA_DATOS.md) y los README de cada fuente.


## Inventario físico

| Formato | Archivos | Tamaño MiB |
| --- | ---: | ---: |
| .csv | 42 | 46.11 |
| .geojson | 4 | 99.25 |
| .gz | 238 | 166.42 |
| .json | 419 | 17.37 |
| .nc4 | 407 | 49.22 |
| .tif | 451 | 500.22 |
| .xml | 1 | 0.24 |
| .xlsx | 2 | 0.09 |

El inventario incluye insumos, resultados, metadatos y archivos temporales de datos. Excluye entornos virtuales, cachés de Python y archivos de configuración ocultos.

### Archivos por carpeta y formato

| Carpeta | Formato | Archivos | Primer y último nombre en orden alfabético |
| --- | --- | ---: | --- |
| `01_suelos_y_salud_del_suelo/ISRIC` | .csv | 1 | [POWER_Point_Daily_19811001_20260131_002d19S_079d90W_LST.csv](01_suelos_y_salud_del_suelo/ISRIC/POWER_Point_Daily_19811001_20260131_002d19S_079d90W_LST.csv) |
| `01_suelos_y_salud_del_suelo/ISRIC/soilgrids_2_costa_dpa2019` | .json | 145 | [clay_0-5cm_Q0.05.json](01_suelos_y_salud_del_suelo/ISRIC/soilgrids_2_costa_dpa2019/clay_0-5cm_Q0.05.json) · [soc_60-100cm_mean.json](01_suelos_y_salud_del_suelo/ISRIC/soilgrids_2_costa_dpa2019/soc_60-100cm_mean.json) |
| `01_suelos_y_salud_del_suelo/ISRIC/soilgrids_2_costa_dpa2019` | .tif | 144 | [clay_0-5cm_Q0.05.tif](01_suelos_y_salud_del_suelo/ISRIC/soilgrids_2_costa_dpa2019/clay_0-5cm_Q0.05.tif) · [soc_60-100cm_mean.tif](01_suelos_y_salud_del_suelo/ISRIC/soilgrids_2_costa_dpa2019/soc_60-100cm_mean.tif) |
| `01_suelos_y_salud_del_suelo/SMAP` | .csv | 1 | [archivos_recopilados.csv](01_suelos_y_salud_del_suelo/SMAP/archivos_recopilados.csv) |
| `01_suelos_y_salud_del_suelo/SMAP/datos/historico` | .csv | 2 | [humedad_mensual_provincial.csv](01_suelos_y_salud_del_suelo/SMAP/datos/historico/humedad_mensual_provincial.csv) · [meses_verificados.csv](01_suelos_y_salud_del_suelo/SMAP/datos/historico/meses_verificados.csv) |
| `01_suelos_y_salud_del_suelo/SMAP/datos/historico` | .gz | 55 | [smap_costa_3horas_2015-03.csv.gz](01_suelos_y_salud_del_suelo/SMAP/datos/historico/smap_costa_3horas_2015-03.csv.gz) · [smap_costa_3horas_2019-09.csv.gz](01_suelos_y_salud_del_suelo/SMAP/datos/historico/smap_costa_3horas_2019-09.csv.gz) |
| `01_suelos_y_salud_del_suelo/SMAP/datos/historico` | .json | 58 | [calidad_2015-03.json](01_suelos_y_salud_del_suelo/SMAP/datos/historico/calidad_2015-03.json) · [proceso.json](01_suelos_y_salud_del_suelo/SMAP/datos/historico/proceso.json) |
| `01_suelos_y_salud_del_suelo/SMAP/datos/prueba_2025_01_01` | .gz | 1 | [smap_costa_3horas_2025-01.csv.gz](01_suelos_y_salud_del_suelo/SMAP/datos/prueba_2025_01_01/smap_costa_3horas_2025-01.csv.gz) |
| `01_suelos_y_salud_del_suelo/SMAP/datos/prueba_2025_01_01` | .json | 5 | [calidad_2025-01.json](01_suelos_y_salud_del_suelo/SMAP/datos/prueba_2025_01_01/calidad_2025-01.json) · [validacion_csv.json](01_suelos_y_salud_del_suelo/SMAP/datos/prueba_2025_01_01/validacion_csv.json) |
| `01_suelos_y_salud_del_suelo/SMAP/geografia` | .csv | 7 | [celda_provincia.csv](01_suelos_y_salud_del_suelo/SMAP/geografia/celda_provincia.csv) · [verificacion_los_rios_cantones.csv](01_suelos_y_salud_del_suelo/SMAP/geografia/verificacion_los_rios_cantones.csv) |
| `01_suelos_y_salud_del_suelo/SMAP/geografia` | .geojson | 4 | [costa_cantones_referencia_2019.geojson](01_suelos_y_salud_del_suelo/SMAP/geografia/costa_cantones_referencia_2019.geojson) · [los_rios_cantones_referencia_2019.geojson](01_suelos_y_salud_del_suelo/SMAP/geografia/los_rios_cantones_referencia_2019.geojson) |
| `01_suelos_y_salud_del_suelo/SMAP/geografia` | .json | 3 | [costa_cantones_referencia_2019.json](01_suelos_y_salud_del_suelo/SMAP/geografia/costa_cantones_referencia_2019.json) · [verificacion_geografica.json](01_suelos_y_salud_del_suelo/SMAP/geografia/verificacion_geografica.json) |
| `01_suelos_y_salud_del_suelo/SMAP/geografia` | .nc4 | 1 | [malla_coordenadas.nc4](01_suelos_y_salud_del_suelo/SMAP/geografia/malla_coordenadas.nc4) |
| `01_suelos_y_salud_del_suelo/SMAP/metadatos` | .csv | 1 | [disponibilidad_anual.csv](01_suelos_y_salud_del_suelo/SMAP/metadatos/disponibilidad_anual.csv) |
| `01_suelos_y_salud_del_suelo/SMAP/metadatos` | .json | 8 | [autenticacion_estado.json](01_suelos_y_salud_del_suelo/SMAP/metadatos/autenticacion_estado.json) · [ultimo_granulo.json](01_suelos_y_salud_del_suelo/SMAP/metadatos/ultimo_granulo.json) |
| `01_suelos_y_salud_del_suelo/SMAP/metadatos` | .xml | 1 | [opendap_dmr.xml](01_suelos_y_salud_del_suelo/SMAP/metadatos/opendap_dmr.xml) |
| `01_suelos_y_salud_del_suelo/SMAP/temporales` | .nc4 | 1 | [grid_coords.nc4](01_suelos_y_salud_del_suelo/SMAP/temporales/grid_coords.nc4) |
| `01_suelos_y_salud_del_suelo/SMAP/temporales/historico/2019-10` | .gz | 182 | [SMAP_L4_SM_gph_20191001T013000_Vv8010_001.h5.csv.gz](01_suelos_y_salud_del_suelo/SMAP/temporales/historico/2019-10/SMAP_L4_SM_gph_20191001T013000_Vv8010_001.h5.csv.gz) · [SMAP_L4_SM_gph_20191023T163000_Vv8010_001.h5.csv.gz](01_suelos_y_salud_del_suelo/SMAP/temporales/historico/2019-10/SMAP_L4_SM_gph_20191023T163000_Vv8010_001.h5.csv.gz) |
| `01_suelos_y_salud_del_suelo/SMAP/temporales/historico/2019-10` | .json | 182 | [SMAP_L4_SM_gph_20191001T013000_Vv8010_001.h5.json](01_suelos_y_salud_del_suelo/SMAP/temporales/historico/2019-10/SMAP_L4_SM_gph_20191001T013000_Vv8010_001.h5.json) · [SMAP_L4_SM_gph_20191023T163000_Vv8010_001.h5.json](01_suelos_y_salud_del_suelo/SMAP/temporales/historico/2019-10/SMAP_L4_SM_gph_20191023T163000_Vv8010_001.h5.json) |
| `01_suelos_y_salud_del_suelo/SMAP/temporales/lote_prueba` | .nc4 | 1 | [subset_00.nc4](01_suelos_y_salud_del_suelo/SMAP/temporales/lote_prueba/subset_00.nc4) |
| `02_clima_temperatura_y_meteorologia/GPM` | .csv | 7 | [IMERG_Costa_2010-01_2014-12.csv](02_clima_temperatura_y_meteorologia/GPM/IMERG_Costa_2010-01_2014-12.csv) · [IMERG_provincias_2015-01_2025-09.csv](02_clima_temperatura_y_meteorologia/GPM/IMERG_provincias_2015-01_2025-09.csv) |
| `02_clima_temperatura_y_meteorologia/GPM` | .json | 1 | [ampliacion_imerg_2010_2014.json](02_clima_temperatura_y_meteorologia/GPM/ampliacion_imerg_2010_2014.json) |
| `02_clima_temperatura_y_meteorologia/NASA_POWER` | .csv | 1 | [POWER_Point_Daily_20200131_20251231_002d19S_079d90W_LST.csv](02_clima_temperatura_y_meteorologia/NASA_POWER/POWER_Point_Daily_20200131_20251231_002d19S_079d90W_LST.csv) |
| `03_agua_y_recursos_hidricos/ECOSTRESS` | .csv | 2 | [pixeles_comunes_ecostress.csv](03_agua_y_recursos_hidricos/ECOSTRESS/pixeles_comunes_ecostress.csv) · [ventanas_validas_ecostress.csv](03_agua_y_recursos_hidricos/ECOSTRESS/ventanas_validas_ecostress.csv) |
| `03_agua_y_recursos_hidricos/ECOSTRESS` | .json | 1 | [cobertura_piloto_2026-11-14.json](03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_piloto_2026-11-14.json) |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | .json | 1 | [manifest.json](03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14/manifest.json) |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | .tif | 140 | [07_20260602T130821_L2_LST.tif](03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14/07_20260602T130821_L2_LST.tif) · [24_20260923T163300_L3_cloud.tif](03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14/24_20260923T163300_L3_cloud.tif) |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | .json | 1 | [manifest.json](03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14/manifest.json) |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | .tif | 75 | [23_20250922T173309_L2_LST.tif](03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14/23_20250922T173309_L2_LST.tif) · [24_20260919T180605_L3_cloud.tif](03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14/24_20260919T180605_L3_cloud.tif) |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | .json | 1 | [manifest.json](03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14/manifest.json) |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | .tif | 35 | [07_20260927T150014_L2_LST.tif](03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14/07_20260927T150014_L2_LST.tif) · [24_20260927T150014_L3_cloud.tif](03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14/24_20260927T150014_L3_cloud.tif) |
| `03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO` | .csv | 2 | [csr_rl063_costa_celdas.csv](03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO/csr_rl063_costa_celdas.csv) · [csr_rl063_costa_mensual.csv](03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO/csr_rl063_costa_mensual.csv) |
| `03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO` | .json | 1 | [metadatos_csr.json](03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO/metadatos_csr.json) |
| `04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls` | .json | 1 | [manifiesto.json](04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls/manifiesto.json) |
| `04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls` | .tif | 27 | [00_HLS.L30.T17MPV.2026303T153233.v2.0.tif](04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls/00_HLS.L30.T17MPV.2026303T153233.v2.0.tif) · [13_HLS.S30.T17MPV.2026305T153629.v2.0.tif](04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls/13_HLS.S30.T17MPV.2026305T153629.v2.0.tif) |
| `04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls_qa` | .json | 1 | [manifiesto.json](04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls_qa/manifiesto.json) |
| `04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls_qa` | .tif | 14 | [00_HLS.L30.T17MPV.2026279T153231.v2.0.tif](04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls_qa/00_HLS.L30.T17MPV.2026279T153231.v2.0.tif) · [13_HLS.S30.T17MPV.2026300T153621.v2.0.tif](04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls_qa/13_HLS.S30.T17MPV.2026300T153621.v2.0.tif) |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | .csv | 4 | [superficie_canton_CONALI2024_2010_2025.csv](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/superficie_canton_CONALI2024_2010_2025.csv) · [superficie_provincial_2015_2025.csv](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/superficie_provincial_2015_2025.csv) |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | .json | 3 | [exportaciones_anuales.json](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/exportaciones_anuales.json) · [manifiesto_geotiff.json](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/manifiesto_geotiff.json) |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | .tif | 11 | [costa_conali2024_col4_2015.tif](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/costa_conali2024_col4_2015.tif) · [costa_conali2024_col4_2025.tif](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/costa_conali2024_col4_2025.tif) |
| `04_vegetacion_cultivos_y_monitoreo/MODIS` | .csv | 6 | [MODIS_mensual_DPA2019_2010-01_2014-12.csv](04_vegetacion_cultivos_y_monitoreo/MODIS/MODIS_mensual_DPA2019_2010-01_2014-12.csv) · [integridad_2010_2014.csv](04_vegetacion_cultivos_y_monitoreo/MODIS/integridad_2010_2014.csv) |
| `04_vegetacion_cultivos_y_monitoreo/MODIS` | .json | 1 | [preparacion_2010_2014.json](04_vegetacion_cultivos_y_monitoreo/MODIS/preparacion_2010_2014.json) |
| `04_vegetacion_cultivos_y_monitoreo/MODIS/MOD11C3` | .nc4 | 202 | [2010-01.nc4](04_vegetacion_cultivos_y_monitoreo/MODIS/MOD11C3/2010-01.nc4) · [2026-10.nc4](04_vegetacion_cultivos_y_monitoreo/MODIS/MOD11C3/2026-10.nc4) |
| `04_vegetacion_cultivos_y_monitoreo/MODIS/MOD13C2` | .nc4 | 202 | [2010-01.nc4](04_vegetacion_cultivos_y_monitoreo/MODIS/MOD13C2/2010-01.nc4) · [2026-10.nc4](04_vegetacion_cultivos_y_monitoreo/MODIS/MOD13C2/2026-10.nc4) |
| `04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST` | .json | 1 | [recortes_glad.json](04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST/recortes_glad.json) |
| `04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST` | .tif | 3 | [glad_costa_dpa2019_2011.tif](04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST/glad_costa_dpa2019_2011.tif) · [glad_costa_dpa2019_2019.tif](04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST/glad_costa_dpa2019_2019.tif) |
| `05_topografia_y_modelado_del_terreno/SRTM` | .csv | 1 | [SRTM_cantones_DPA2019.csv](05_topografia_y_modelado_del_terreno/SRTM/SRTM_cantones_DPA2019.csv) |
| `05_topografia_y_modelado_del_terreno/SRTM/datos_costa` | .json | 1 | [manifiesto.json](05_topografia_y_modelado_del_terreno/SRTM/datos_costa/manifiesto.json) |
| `05_topografia_y_modelado_del_terreno/SRTM/datos_costa` | .tif | 2 | [elevacion_m.tif](05_topografia_y_modelado_del_terreno/SRTM/datos_costa/elevacion_m.tif) · [pendiente_grados.tif](05_topografia_y_modelado_del_terreno/SRTM/datos_costa/pendiente_grados.tif) |
| `07_informacion_agropecuaria_ecuatoriana` | .xlsx | 2 | [DATOS_ARROZ_SOYA.xlsx](07_informacion_agropecuaria_ecuatoriana/DATOS_ARROZ_SOYA.xlsx) · [Libro11.xlsx](07_informacion_agropecuaria_ecuatoriana/Libro11.xlsx) |
| `07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC` | .csv | 7 | [costa_cultivos_2025.csv](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/costa_cultivos_2025.csv) · [costa_uso_suelo_2025.csv](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/costa_uso_suelo_2025.csv) |
| `07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC` | .json | 4 | [origen.json](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/origen.json) · [origen_historico.json](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/origen_historico.json) |

## Diccionario de tablas

Los nombres de columnas se transcriben del encabezado. El número de filas excluye encabezados. En los CSV comprimidos de SMAP se lee un encabezado por grupo.

- [POWER_Point_Daily_19811001_20260131_002d19S_079d90W_LST.csv](01_suelos_y_salud_del_suelo/ISRIC/POWER_Point_Daily_19811001_20260131_002d19S_079d90W_LST.csv) · 16,194 filas · `YEAR` 1981 a 2026.
  - `YEAR`, `DOY`, `T2M`, `T2M_MAX`, `T2M_MIN`, `PRECTOTCORR`, `ALLSKY_SFC_SW_DWN`, `WS2M`, `RH2M`
- [archivos_recopilados.csv](01_suelos_y_salud_del_suelo/SMAP/archivos_recopilados.csv) · 9 filas.
  - `file`, `bytes`, `sha256`
- [humedad_mensual_provincial.csv](01_suelos_y_salud_del_suelo/SMAP/datos/historico/humedad_mensual_provincial.csv) · 770 filas · `mes` 2015-03 a 2019-09 · `variable` radicular, superficial.
  - `mes`, `codigo_dpa`, `provincia`, `variable`, `media_m3_m3`, `fraccion_valida_area_intervalo`, `intervalos`
- [meses_verificados.csv](01_suelos_y_salud_del_suelo/SMAP/datos/historico/meses_verificados.csv) · 55 filas · `mes` 2015-03 a 2019-09.
  - `mes`, `filas`, `intervalos`, `faltantes_superficie`, `faltantes_raiz`, `primer_inicio_utc`, `ultimo_inicio_utc`, `sha256`
- [celda_provincia.csv](01_suelos_y_salud_del_suelo/SMAP/geografia/celda_provincia.csv) · 1,182 filas.
  - `cell_id`, `provincia_id`, `provincia`, `intersection_area_m2`, `province_area_fraction`, `cell_area_fraction`
- [celdas.csv](01_suelos_y_salud_del_suelo/SMAP/geografia/celdas.csv) · 1,045 filas.
  - `cell_id`, `grid_row`, `grid_col`, `latitude`, `longitude`, `x_m`, `y_m`, `grid_crs`
- [cobertura_malla_los_rios_cantones.csv](01_suelos_y_salud_del_suelo/SMAP/geografia/cobertura_malla_los_rios_cantones.csv) · 13 filas.
  - `canton_id`, `canton`, `n_cells`, `missing_area_m2`, `coverage_pct`
- [cobertura_malla_provincias.csv](01_suelos_y_salud_del_suelo/SMAP/geografia/cobertura_malla_provincias.csv) · 7 filas.
  - `provincia_id`, `provincia`, `n_cells`, `missing_area_m2`, `coverage_pct`
- [limites_por_provincia.csv](01_suelos_y_salud_del_suelo/SMAP/geografia/limites_por_provincia.csv) · 7 filas.
  - `provincia_id`, `provincia`, `anio_referencia`, `west`, `south`, `east`, `north`
- [los_rios_cantones.csv](01_suelos_y_salud_del_suelo/SMAP/geografia/los_rios_cantones.csv) · 13 filas.
  - `DPA_PROVIN`, `DPA_DESPRO`, `DPA_CANTON`, `DPA_DESCAN`, `DPA_ANIO`
- [verificacion_los_rios_cantones.csv](01_suelos_y_salud_del_suelo/SMAP/geografia/verificacion_los_rios_cantones.csv) · 13 filas.
  - `canton_id`, `canton`, `original_geometry_valid`, `area_km2`, `area_inside_los_rios_pct`, `area_outside_los_rios_km2`
- [disponibilidad_anual.csv](01_suelos_y_salud_del_suelo/SMAP/metadatos/disponibilidad_anual.csv) · 17 filas.
  - `year`, `granules_found`, `requested_start_utc`, `requested_end_utc`, `state`
- [IMERG_Costa_2010-01_2014-12.csv](02_clima_temperatura_y_meteorologia/GPM/IMERG_Costa_2010-01_2014-12.csv) · 87,481 filas · `time` 2010-01-01T00:00:00Z a UTC.
  - `time`, `latitude`, `longitude`, `precipitation`, `precipitationQualityIndex`, `randomError`
- [IMERG_Costa_2015-01_2025-09.csv](02_clima_temperatura_y_meteorologia/GPM/IMERG_Costa_2015-01_2025-09.csv) · 188,083 filas · `time` 2015-01-01T00:00:00Z a UTC.
  - `time`, `latitude`, `longitude`, `precipitation`, `precipitationQualityIndex`, `randomError`
- [IMERG_cantones_costa_2010-01_2014-12.csv](02_clima_temperatura_y_meteorologia/GPM/IMERG_cantones_costa_2010-01_2014-12.csv) · 5,160 filas · `mes` 2010-01 a 2014-12.
  - `mes`, `codigo_dpa`, `canton`, `celdas`, `area_intersectada_km2`, `fraccion_cubierta`, `precipitacion_media_mm`, `indice_calidad_medio`, `error_aleatorio_medio_por_celda_mm`
- [IMERG_cantones_costa_2015-01_2025-09.csv](02_clima_temperatura_y_meteorologia/GPM/IMERG_cantones_costa_2015-01_2025-09.csv) · 11,094 filas · `mes` 2015-01 a 2025-09.
  - `mes`, `codigo_dpa`, `canton`, `celdas`, `area_intersectada_km2`, `fraccion_cubierta`, `precipitacion_media_mm`, `indice_calidad_medio`, `error_aleatorio_medio_por_celda_mm`
- [IMERG_cantones_los_rios_2015-01_2025-09.csv](02_clima_temperatura_y_meteorologia/GPM/IMERG_cantones_los_rios_2015-01_2025-09.csv) · 1,677 filas · `mes` 2015-01 a 2025-09.
  - `mes`, `codigo_dpa`, `canton`, `celdas`, `area_intersectada_km2`, `fraccion_cubierta`, `precipitacion_media_mm`, `indice_calidad_medio`, `error_aleatorio_medio_por_celda_mm`
- [IMERG_provincias_2010-01_2014-12.csv](02_clima_temperatura_y_meteorologia/GPM/IMERG_provincias_2010-01_2014-12.csv) · 420 filas · `mes` 2010-01 a 2014-12.
  - `mes`, `codigo_dpa`, `provincia`, `celdas`, `area_intersectada_km2`, `fraccion_cubierta`, `precipitacion_media_mm`, `indice_calidad_medio`, `error_aleatorio_medio_por_celda_mm`
- [IMERG_provincias_2015-01_2025-09.csv](02_clima_temperatura_y_meteorologia/GPM/IMERG_provincias_2015-01_2025-09.csv) · 903 filas · `mes` 2015-01 a 2025-09.
  - `mes`, `codigo_dpa`, `provincia`, `celdas`, `area_intersectada_km2`, `fraccion_cubierta`, `precipitacion_media_mm`, `indice_calidad_medio`, `error_aleatorio_medio_por_celda_mm`
- [POWER_Point_Daily_20200131_20251231_002d19S_079d90W_LST.csv](02_clima_temperatura_y_meteorologia/NASA_POWER/POWER_Point_Daily_20200131_20251231_002d19S_079d90W_LST.csv) · 2,162 filas · `YEAR` 2020 a 2025.
  - `YEAR`, `DOY`, `T2M`, `T2M_MAX`, `T2M_MIN`, `PRECTOTCORR`, `ALLSKY_SFC_SW_DWN`, `WS2M`, `RH2M`
- [pixeles_comunes_ecostress.csv](03_agua_y_recursos_hidricos/ECOSTRESS/pixeles_comunes_ecostress.csv) · 2,801 filas · `adquisicion_utc` 20260318T192156 a 20260927T150014.
  - `provincia_dpa`, `adquisicion_utc`, `fila`, `columna`, `longitud`, `latitud`, `lst_k`, `ptjplsminst_w_m2`
- [ventanas_validas_ecostress.csv](03_agua_y_recursos_hidricos/ECOSTRESS/ventanas_validas_ecostress.csv) · 8 filas · `adquisicion_utc` 20260318T192156 a 20260927T150014.
  - `provincia_dpa`, `adquisicion_utc`, `pixeles_comunes_validos`, `pixeles_totales`, `carpeta`
- [csr_rl063_costa_celdas.csv](03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO/csr_rl063_costa_celdas.csv) · 22,401 filas · `mes` 2010-01 a 2026-09.
  - `mes`, `fecha_central_utc`, `inicio_utc`, `fin_utc`, `latitud`, `longitud`, `interseccion_km2`, `anomalia_cm`
- [csr_rl063_costa_mensual.csv](03_agua_y_recursos_hidricos/GRACE_Y_GRACE_FO/csr_rl063_costa_mensual.csv) · 171 filas · `mes` 2010-01 a 2026-09.
  - `mes`, `fecha_central_utc`, `inicio_utc`, `fin_utc`, `anomalia_cm`, `area_valida_km2`, `area_malla_km2`, `celdas_validas`
- [superficie_canton_CONALI2024_2010_2025.csv](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/superficie_canton_CONALI2024_2010_2025.csv) · 14,832 filas · `anio` 2010 a 2025.
  - `codigo_dpa`, `canton`, `anio`, `clase_id`, `clase_nivel_0`, `clase_nivel_1`, `clase_nivel_2`, `clase_nivel_3`, `clase_nivel_4`, `superficie_ha`, `parroquias_con_fila`
- [superficie_parroquia_CONALI2024_2010_2025.csv](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/superficie_parroquia_CONALI2024_2010_2025.csv) · 44,720 filas · `anio` 2010 a 2025.
  - `codigo_dpa`, `territorio`, `canton_fuente`, `anio`, `clase_id`, `clase_nivel_0`, `clase_nivel_1`, `clase_nivel_2`, `clase_nivel_3`, `clase_nivel_4`, `superficie_ha`
- [superficie_provincia_CONALI2024_2010_2025.csv](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/superficie_provincia_CONALI2024_2010_2025.csv) · 1,792 filas · `anio` 2010 a 2025.
  - `codigo_dpa`, `territorio`, `canton_fuente`, `anio`, `clase_id`, `clase_nivel_0`, `clase_nivel_1`, `clase_nivel_2`, `clase_nivel_3`, `clase_nivel_4`, `superficie_ha`
- [superficie_provincial_2015_2025.csv](04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR/superficie_provincial_2015_2025.csv) · 1,232 filas · `anio` 2015 a 2025.
  - `codigo_provincia`, `provincia`, `anio`, `clase_id`, `clase_nivel_0`, `clase_nivel_1`, `clase_nivel_2`, `clase_nivel_3`, `clase_nivel_4`, `superficie_ha`
- [MODIS_mensual_DPA2019_2010-01_2014-12.csv](04_vegetacion_cultivos_y_monitoreo/MODIS/MODIS_mensual_DPA2019_2010-01_2014-12.csv) · 22,320 filas · `mes` 2010-01 a 2014-12 · `variable` evi, lst_diurna_c, lst_nocturna_c, ndvi.
  - `mes`, `codigo_dpa`, `territorio`, `variable`, `media`, `area_valida_km2`, `fraccion_valida`
- [MODIS_mensual_DPA2019_2015-01_2026-10.csv](04_vegetacion_cultivos_y_monitoreo/MODIS/MODIS_mensual_DPA2019_2015-01_2026-10.csv) · 52,824 filas · `mes` 2015-01 a 2026-10 · `variable` evi, lst_diurna_c, lst_nocturna_c, ndvi.
  - `mes`, `codigo_dpa`, `territorio`, `variable`, `media`, `area_valida_km2`, `fraccion_valida`
- [consultas.csv](04_vegetacion_cultivos_y_monitoreo/MODIS/consultas.csv) · 284 filas · `mes` 2015-01 a 2026-10.
  - `producto`, `mes`, `archivo`, `url`, `catalogo`
- [consultas_2010_2014.csv](04_vegetacion_cultivos_y_monitoreo/MODIS/consultas_2010_2014.csv) · 120 filas · `mes` 2010-01 a 2014-12.
  - `producto`, `mes`, `archivo`, `url`, `catalogo`
- [integridad.csv](04_vegetacion_cultivos_y_monitoreo/MODIS/integridad.csv) · 284 filas.
  - `archivo`, `bytes`, `sha256`
- [integridad_2010_2014.csv](04_vegetacion_cultivos_y_monitoreo/MODIS/integridad_2010_2014.csv) · 120 filas.
  - `archivo`, `bytes`, `sha256`
- [SRTM_cantones_DPA2019.csv](05_topografia_y_modelado_del_terreno/SRTM/SRTM_cantones_DPA2019.csv) · 172 filas · `variable` elevacion_m, pendiente_grados.
  - `provincia_dpa`, `canton_dpa`, `canton`, `variable`, `unidad`, `pixeles_en_raster`, `pixeles_validos`, `fraccion_valida_en_raster`, `min`, `p10`, `p50`, `p90`, `max`
- [costa_cultivos_2025.csv](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/costa_cultivos_2025.csv) · 518 filas · `anio` 2025 a 2025.
  - `anio`, `codigo_dpa`, `provincia`, `hoja`, `fila_fuente`, `producto`, `condicion`, `plantada_o_sembrada_ha`, `cosechada_ha`, `produccion_t`, `ventas_t`, `rendimiento_derivado_t_ha`
- [costa_cultivos_ediciones_2010_2013.csv](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/costa_cultivos_ediciones_2010_2013.csv) · 1,456 filas · `anio` 2010 a 2013.
  - `anio`, `codigo_dpa`, `provincia`, `hoja`, `fila_fuente`, `producto`, `condicion`, `plantada_o_sembrada_ha`, `cosechada_ha`, `produccion_t`, `ventas_t`, `rendimiento_derivado_t_ha`
- [costa_cultivos_ediciones_2014_2017.csv](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/costa_cultivos_ediciones_2014_2017.csv) · 1,918 filas · `anio` 2014 a 2017.
  - `anio`, `codigo_dpa`, `provincia`, `hoja`, `fila_fuente`, `producto`, `condicion`, `plantada_o_sembrada_ha`, `cosechada_ha`, `produccion_t`, `ventas_t`, `rendimiento_derivado_t_ha`
- [costa_cultivos_ediciones_2018_2024.csv](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/costa_cultivos_ediciones_2018_2024.csv) · 3,625 filas · `anio` 2018 a 2024.
  - `anio`, `codigo_dpa`, `provincia`, `hoja`, `fila_fuente`, `producto`, `condicion`, `plantada_o_sembrada_ha`, `cosechada_ha`, `produccion_t`, `ventas_t`, `rendimiento_derivado_t_ha`
- [costa_labranza_transitorios_2025.csv](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/costa_labranza_transitorios_2025.csv) · 7 filas · `anio` 2025 a 2025.
  - `anio`, `codigo_dpa`, `provincia`, `hoja`, `fila_fuente`, `convencional_ha`, `reducida_ha`, `cero_labranza_ha`, `total_ha`
- [costa_riego_transitorios_2025.csv](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/costa_riego_transitorios_2025.csv) · 7 filas · `anio` 2025 a 2025.
  - `anio`, `codigo_dpa`, `provincia`, `hoja`, `fila_fuente`, `surcos_ha`, `aspersion_ha`, `microaspersion_ha`, `goteo_ha`, `nebulizacion_ha`, `otro_ha`, `total_ha`
- [costa_uso_suelo_2025.csv](07_informacion_agropecuaria_ecuatoriana/ESPAC_INEC/costa_uso_suelo_2025.csv) · 7 filas · `anio` 2025 a 2025.
  - `anio`, `codigo_dpa`, `provincia`, `hoja`, `fila_fuente`, `total_ha`, `permanentes_ha`, `transitorios_barbecho_ha`, `descanso_ha`, `pastos_cultivados_ha`, `pastos_naturales_ha`, `paramos_ha`, `montes_bosques_ha`, `otros_usos_ha`
- `01_suelos_y_salud_del_suelo/SMAP/datos/historico` · 55 CSV comprimidos · [smap_costa_3horas_2015-03.csv.gz](01_suelos_y_salud_del_suelo/SMAP/datos/historico/smap_costa_3horas_2015-03.csv.gz).
  - `time_start_utc`, `time_end_utc`, `cell_id`, `sm_surface_m3_m3`, `sm_rootzone_m3_m3`, `quality_status`, `source_granule`
- `01_suelos_y_salud_del_suelo/SMAP/datos/prueba_2025_01_01` · 1 CSV comprimidos · [smap_costa_3horas_2025-01.csv.gz](01_suelos_y_salud_del_suelo/SMAP/datos/prueba_2025_01_01/smap_costa_3horas_2025-01.csv.gz).
  - `time_start_utc`, `time_end_utc`, `cell_id`, `sm_surface_m3_m3`, `sm_rootzone_m3_m3`, `quality_status`, `source_granule`
- `01_suelos_y_salud_del_suelo/SMAP/temporales/historico/2019-10` · 182 CSV comprimidos · [SMAP_L4_SM_gph_20191001T013000_Vv8010_001.h5.csv.gz](01_suelos_y_salud_del_suelo/SMAP/temporales/historico/2019-10/SMAP_L4_SM_gph_20191001T013000_Vv8010_001.h5.csv.gz).
  - `time_start_utc`, `time_end_utc`, `cell_id`, `sm_surface_m3_m3`, `sm_rootzone_m3_m3`, `quality_status`, `source_granule`

## Fichas agronómicas de la carpeta 07

| Libro y rango | Contenido | Variables |
| --- | --- | --- |
| [Libro11.xlsx](07_informacion_agropecuaria_ecuatoriana/Libro11.xlsx), Hoja1 A1:G8 | Siete filas de fichas. Arroz SFL-11, arroz INIAP-15, maíz duro (referencia a INIAP H-603), soya INIAP-307, cacao, banano/plátano y una fila agrupada para café, mango, pitahaya, piña, maracuyá y caña. | Cultivo o variedad, ciclo o duración, precipitación o agua, temperatura óptima, suelo y textura, rendimiento estimado, plagas, enfermedades y observaciones. |
| [DATOS_ARROZ_SOYA.xlsx](07_informacion_agropecuaria_ecuatoriana/DATOS_ARROZ_SOYA.xlsx), Hoja1 B5:E14 y Hoja2 B5:E14 | Dos versiones de la misma matriz comparativa de nueve características para arroz SFL-11, arroz INIAP-15 y soya INIAP 307. | Especie, rendimiento, ciclo, altura de planta, características y peso de grano o semilla, calidad industrial o composición, resistencia al acame y tolerancia a plagas y enfermedades. |
| DATOS_ARROZ_SOYA.xlsx, Hoja2 G5:J14 | Matriz adicional de nueve parámetros para las mismas tres variedades. | Duración y floración, rendimiento, sanidad, suelo (textura, pH, profundidad y otras condiciones), riego, precipitación, temperatura, altitud y pendiente o topografía. |

Valores reportados en la matriz de Hoja2, pendientes de cotejo con sus fuentes primarias.

| Variedad | Ciclo (días) | Rendimiento indicado (t/ha) | Temperatura (°C) | pH |
| --- | --- | --- | --- | --- |
| Arroz SFL-11 | 120–131 | 6,0–8,0 en riego y 6,0 en secano | 25–35 | 5,5–6,5 |
| Arroz INIAP-15 | 110–128, con rangos por estación | 5,1–9,0 en riego, con promedio declarado de 5,9. En secano, 4,0–7,0 | 25–35 | 5,5–7,0 |
| Soya INIAP 307 | 105–120, con floración a los 43–48 días | 4,47 en promedio | 22–25 | 6,0–6,5 |

- Las dos fichas comparten las tres variedades. Sus rendimientos de referencia y descripciones de manejo tienen un uso distinto al rendimiento anual provincial derivado de ESPAC.
- Para soya, Libro11 indica profundidad mayor de 25 cm y Hoja2 de DATOS_ARROZ_SOYA indica profundidad efectiva de al menos 1,5 m. Confirmar si se refieren a medidas distintas antes de aplicar un umbral. El rendimiento de SFL-11 aparece como 6,0–8,0 t/ha en riego y otra celda del mismo libro menciona un máximo de 7,0 t/ha.
- Las celdas mezclan texto, rangos y unidades. Distinguir precipitación anual, necesidad hídrica por ciclo y lámina de riego. Para peso, el arroz se expresa por 1.000 granos y la soya por 100 semillas. Hoja1 de DATOS_ARROZ_SOYA conserva marcas de cita y texto residual como `more_horiz`, sin bibliografía trazable dentro de las tablas revisadas.

## Esquemas geográficos y ráster

### GeoJSON

- [costa_cantones_referencia_2019.geojson](01_suelos_y_salud_del_suelo/SMAP/geografia/costa_cantones_referencia_2019.geojson) · 86 entidades · MultiPolygon, Polygon · `DPA_ANIO`, `DPA_CANTON`, `DPA_DESCAN`, `DPA_DESPRO`, `DPA_PROVIN`.
- [costa_provincias_referencia_2019.geojson](01_suelos_y_salud_del_suelo/SMAP/geografia/costa_provincias_referencia_2019.geojson) · 7 entidades · MultiPolygon, Polygon · `DPA_ANIO`, `DPA_DESPRO`, `DPA_PROVIN`.
- [costa_union_referencia_2019.geojson](01_suelos_y_salud_del_suelo/SMAP/geografia/costa_union_referencia_2019.geojson) · 1 entidades · MultiPolygon · `purpose`, `reference_year`.
- [los_rios_cantones_referencia_2019.geojson](01_suelos_y_salud_del_suelo/SMAP/geografia/los_rios_cantones_referencia_2019.geojson) · 13 entidades · Polygon · `DPA_ANIO`, `DPA_CANTON`, `DPA_DESCAN`, `DPA_DESPRO`, `DPA_PROVIN`.

### GeoTIFF

Se leyeron los metadatos de cada GeoTIFF. Las filas agrupan archivos con igual esquema dentro de cada carpeta. Para las capas monobanda sin descripción, el nombre del archivo identifica la variable o la máscara.

| Carpeta | Archivos | Bandas en orden | Tipo por banda | NoData |
| --- | ---: | --- | --- | --- |
| `01_suelos_y_salud_del_suelo/ISRIC/soilgrids_2_costa_dpa2019` | 144 | sin descripción | int16 | -32768.0 |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 28 | sin descripción | uint16 | None |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 56 | sin descripción | uint8 | None |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/alternativas_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 15 | sin descripción | uint16 | None |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 30 | sin descripción | uint8 | None |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/cobertura_mejorada_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 7 | sin descripción | uint16 | None |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 14 | sin descripción | uint8 | None |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `03_agua_y_recursos_hidricos/ECOSTRESS/piloto_ecostress_2026-11-14` | 1 | sin descripción | float32 | nan |
| `04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls` | 27 | azul, verde, rojo, nir, swir1, swir2, Fmask, NDVI, EVI2, NDMI | float32, float32, float32, float32, float32, float32, float32, float32, float32, float32 | -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0 |
| `04_vegetacion_cultivos_y_monitoreo/LANDSAT/piloto_hls_qa` | 14 | azul, verde, rojo, nir, swir1, swir2, Fmask, NDVI, EVI2, NDMI | float32, float32, float32, float32, float32, float32, float32, float32, float32, float32 | -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2015 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2016 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2017 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2018 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2019 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2020 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2021 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2022 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2023 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2024 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/MAPBIOMAS_ECUADOR` | 1 | classification_2025 | uint8 | 0.0 |
| `04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST` | 3 | sin descripción | uint8 | 255.0 |
| `05_topografia_y_modelado_del_terreno/SRTM/datos_costa` | 1 | Elevacion SRTMGL1 v003 (m EGM96) | int16 | -32768.0 |
| `05_topografia_y_modelado_del_terreno/SRTM/datos_costa` | 1 | Pendiente Horn (grados) | float32 | -32768.0 |

