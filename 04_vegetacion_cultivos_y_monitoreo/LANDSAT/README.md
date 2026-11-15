# Landsat / HLS

La extracción piloto de HLS v2.0 usa Landsat 8/9 (L30) y Sentinel-2 (S30), a 30 m en su cuadrícula UTM nativa. El intervalo solicitado es 2010-01-01 a 2026-11-14. HLS comienza en 2013 para L30 y en 2015 para S30. El manifiesto registra las primeras y últimas escenas que devuelve el catálogo en cada punto.

- [Productos y bandas NASA HLS](https://hls.gsfc.nasa.gov/data-products/)
- [Acceso y condiciones de uso](https://hls.gsfc.nasa.gov/data-access-and-tools/)
- [Guía HLS v2.0](https://lpdaac.usgs.gov/documents/1698/HLS_User_Guide_V2.pdf)

El piloto usa un punto representativo por provincia y una ventana de 33 × 33 píxeles. Los límites administrativos de referencia de 2019 se leen del GeoJSON compartido con SMAP en EPSG:4326. La ventana se lee mediante solicitudes parciales a los GeoTIFF del catálogo STAC de Microsoft Planetary Computer. La descarga histórica y el cálculo por parcela requieren los polígonos de los predios.

Cada GeoTIFF contiene reflectancia unitaria escalada con 0.0001, Fmask e índices NDVI, EVI2 y NDMI. Se enmascaran reflectancias e índices con los bits 0–5 de Fmask y se usa -9999 para valores faltantes. El criterio piloto busca una escena con algún píxel válido entre las 35 más recientes de cada sensor y punto. El manifiesto incluye el conteo válido, tamaño y SHA-256 de cada recorte.

Desde la raíz del repositorio, en PowerShell con uv:

```powershell
uv venv .venv-hls --python 3.13
uv pip install --python .venv-hls/Scripts/python.exe rasterio==1.5.2 shapely==2.2.0 requests==2.34.2 planetary-computer==1.0.0 numpy==2.5.4
$env:VIRTUAL_ENV = (Resolve-Path .venv-hls).Path
uv run --active python 04_vegetacion_cultivos_y_monitoreo/LANDSAT/descargar_piloto_hls.py
```

Los resultados con control de calidad quedan en **piloto_hls_qa**. Para otras regiones, consultar el [instructivo común](../../10_instructivos/ACCESO_A_OTRAS_REGIONES.md).
