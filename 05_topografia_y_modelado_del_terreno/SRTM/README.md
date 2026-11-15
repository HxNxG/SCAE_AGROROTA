# SRTM en la Costa ecuatoriana

SRTMGL1 v003 de NASA/JPL, distribuido por OpenTopography. Elevación en metros sobre EGM96 y cuadrícula geográfica WGS 84 (EPSG:4326), con paso de 1 segundo de arco (aproximadamente 30 m). La misión adquirió el relieve del 11 al 22 de febrero de 2000. La descarga del 14 de noviembre de 2026 incorpora este relieve como referencia para el período de análisis 2010–2026. El producto v003 incluye rellenos de vacíos con fuentes auxiliares.

- [Guía NASA/USGS del producto](https://lpdaac.usgs.gov/documents/179/SRTM_User_Guide_V3.pdf)
- [Distribución y condiciones de uso](https://portal.opentopography.org/raster?jobId=rt1788193141453)

Los GeoTIFF se recortan a la unión de Esmeraldas, Manabí, Santo Domingo de los Tsáchilas, Los Ríos, Guayas, Santa Elena y El Oro, según el GeoJSON administrativo de referencia de 2019 que comparte SMAP. La elevación conserva la cuadrícula y las alturas de origen. La pendiente en grados se calcula mediante Horn en una ventana de 3 × 3, con distancias horizontales en metros ajustadas por latitud sobre el elipsoide WGS 84. La pendiente requiere nueve alturas válidas y usa vecinos a ambos lados del límite antes de enmascarar. Ambos rásteres usan -32768 como NoData.

Los archivos en datos_costa se acompañan de un manifiesto con fuentes, tamaño, cobertura válida y SHA-256. A escala de parcela, la resolución permite una evaluación preliminar. La estimación de restricciones dentro de cada predio requiere sus polígonos.

Desde la raíz del repositorio, en PowerShell con uv:

El [resumen por cantón](SRTM_cantones_DPA2019.csv) incluye 172 filas para los 86 cantones. Resume elevación en metros y pendiente en grados con mínimo, percentiles 10, 50 y 90, y máximo. Se seleccionaron píxeles por centro dentro de cada límite DPA 2019. Todos los píxeles seleccionados dentro de los rásteres fueron válidos.

~~~
uv venv .venv-srtm --python 3.13
uv pip install --python .venv-srtm/Scripts/python.exe rasterio==1.5.2 shapely==2.2.0 requests==2.34.2 numpy==2.5.4
$env:VIRTUAL_ENV = (Resolve-Path .venv-srtm).Path
uv run --active python 05_topografia_y_modelado_del_terreno/SRTM/descargar_srtm.py
~~~
