# NASA Harvest

**Prioridad complementaria · Referencia metodológica para Field Shift**  
Consulta documental del 14 de noviembre de 2026. Alcance: Esmeraldas, Manabí, Santo Domingo de los Tsáchilas, Los Ríos, Guayas, Santa Elena y El Oro.

[Sitio oficial de NASA Harvest](https://www.nasaharvest.org/)

## Recursos evaluados

| Recurso | Cobertura y acceso | Aplicación en la Costa |
| --- | --- | --- |
| [GEOGLAM Crop Monitor](https://www.cropmonitor.org/methodology) | Metodología pública de evaluación de cultivos que combina observación de la Tierra y revisión por especialistas. GEOGLAM inició el Crop Monitor en 2013 y publica evaluaciones mensuales a escala regional y global. [Cobertura general](https://geoglam.org/ag-monitoring/) | Adoptar el proceso de contraste de fuentes y revisión de la condición y sus posibles causas. La cobertura de informes por cultivo y provincia queda pendiente de verificar. |
| [GIMMS GLAM](https://www.climatehubs.usda.gov/hubs/international/tools/gimms-global-agricultural-monitoring) | Herramienta de consulta de curvas NDVI MODIS de ocho días por área administrativa y máscara de cultivo. | Consultar como referencia regional si el selector ofrece la zona y máscara requeridas. Queda pendiente confirmar el nivel administrativo, la máscara y la fecha efectiva para Ecuador. |
| [HarvestStat Africa](https://doi.org/10.1038/s41597-025-05001-z) | Estadísticas agrícolas subnacionales armonizadas para África subsahariana. [Consorcio HarvestStat](https://www.harveststat.org/) | Referencia para documentar unidades, cambios de límites y calidad al integrar estadísticas ecuatorianas. El alcance del conjunto Africa excluye Ecuador. |
| [Global Cropland Extent and Change, GLAD/UMD](https://glad.umd.edu/dataset/croplands) | Máscara global de cultivos de 30 m derivada de Landsat, disponible en cinco épocas de cuatro años. Las épocas 2008–2011, 2012–2015 y 2016–2019 intersectan el intervalo del repositorio. | Candidata para contextualizar la extensión histórica. Verificar localmente la clase 0, que agrupa ausencia de cultivos y ausencia de datos. Registrar cada época completa y contrastar el mapa con evidencia local, en especial para cultivos perennes. |

## Protocolo para interpretar alertas

1. Elegir un cultivo y un área piloto con registros locales de siembra y cosecha. Registrar provincia, cantón, polígono, CRS, fuente y versión de la delimitación.
2. Para cada período y fase fenológica, resumir el NDVI de [Landsat/HLS](../LANDSAT/README.md) en píxeles válidos de la parcela y registrar la fracción observada. Comparar con la mediana histórica de la misma fase, indicando los años usados. Usar [MODIS](../MODIS/README.md) como contexto regional. Si faltan observaciones válidas o fechas de siembra, marcar la evaluación como insuficiente.
3. Contrastar las anomalías con lluvia de [GPM](../../02_clima_temperatura_y_meteorologia/GPM/README.md), humedad de [SMAP](../../01_suelos_y_salud_del_suelo/SMAP/README.md) y registros de riego y manejo. Considerar la resolución de cada señal y registrar si las fuentes coinciden o discrepan. La condición observada puede tener varias causas.
4. Validar cultivo, fase y posibles causas con registros ecuatorianos y observaciones consentidas de agricultores. Guardar por evaluación la fecha, fase, indicador, referencia histórica, calidad, condición observada, causa probable y evidencia de validación. Para orientar rotaciones o asociaciones, incorporar evidencia agronómica local de los cultivos y sus efectos sobre el suelo.

## Cobertura y almacenamiento

El intervalo de referencia del repositorio es 2010-01-01 a 2026-11-14. La cobertura efectiva se registra por recurso y por producto. Se descargaron tres recortes GLAD para las épocas 2008–2011, 2012–2015 y 2016–2019. La primera época incluye años previos a 2010 y se conserva completa. Esta edición termina en 2019. Ver [REGLAS.md](../../REGLAS.md) y el [registro regional de brechas](../../09_cobertura_y_brechas/ESTADO_POR_REGION.md).

Para otras regiones, sustituir el polígono y validar de nuevo calendarios, máscaras y fuentes locales según el [instructivo común](../../10_instructivos/ACCESO_A_OTRAS_REGIONES.md).

## Recortes GLAD descargados el 14 de noviembre de 2026

- GeoTIFF de 8 bits, compresión LZW, WGS84 (EPSG:4326), paso de 0,00025° (aprox. 30 m en el ecuador). Se leyeron ventanas de los mosaicos NW y SW mediante HTTP, sin remuestrear, y se aplicó la unión de las siete provincias [DPA 2019 de referencia](../../01_suelos_y_salud_del_suelo/SMAP/ESTADO_RECOPILACION.md).
- Clases: 1 indica cultivo según GLAD, 0 agrupa ausencia de cultivo y ausencia de datos en el original, y 255 indica píxeles fuera del polígono. La definición de GLAD excluye cultivos leñosos perennes, pastos permanentes y agricultura itinerante. Falta validar la clasificación con datos de campo.
- Acceso público según la [ficha oficial](https://glad.umd.edu/dataset/croplands) y el [artículo de Potapov et al.](https://doi.org/10.1038/s43016-021-00429-z). La ficha consultada no especifica una licencia independiente para los GeoTIFF.
- El [manifiesto](recortes_glad.json) registra URL, tamaño, SHA-256, conteos por clase, polígono y espacio disponible. Se comprobó la lectura de los tres recortes y la presencia de ambas clases.

Desde la raíz del repositorio:

```powershell
uv run --no-project --python 3.13 --with rasterio python 04_vegetacion_cultivos_y_monitoreo/NASA_HARVEST/descargar_glad.py
```
## Alcance vigente desde 2015

La serie anual de referencia para la Costa es [MapBiomas Ecuador 2015–2025](../MAPBIOMAS_ECUADOR/README.md), última colección publicada al corte del 14 de noviembre de 2026. Los tres GeoTIFF GLAD de arriba se conservan como referencia histórica separada. Cada archivo GLAD representa una época indivisible y su cobertura termina en 2019.
