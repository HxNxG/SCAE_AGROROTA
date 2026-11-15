# ISRIC World Soil Data

Recurso oficial: https://www.isric.org/

Producto seleccionado: [ISRIC SoilGrids 250 m v2.0](https://docs.isric.org/globaldata/soilgrids/), licencia CC BY 4.0. Las capas son predicciones estáticas por profundidad.

## Acceso para la Costa ecuatoriana

1. Abrir el recurso oficial y localizar su catálogo o documentación de acceso a datos.
2. Seleccionar un producto concreto y registrar identificador, versión, variables, unidades, calidad, licencia y resolución.
3. Comprobar la cobertura del área de estudio en la Costa y del período requerido. Usar el polígono documentado del análisis.
4. Revisar requisitos de cuenta, autenticación y formatos en la documentación vigente. No guardar credenciales en este repositorio.
5. Consultar o solicitar un recorte espacial y temporal cuando la fuente lo permita. Estimar el tamaño antes de descargar.
6. Guardar los parámetros reproducibles y metadatos conforme a [REGLAS.md](../../REGLAS.md).

## Otras regiones

Seguir el [instructivo común](../../10_instructivos/ACCESO_A_OTRAS_REGIONES.md), reemplazando el área de estudio y verificando nuevamente cobertura y calidad. No asumir que todos los productos o plataformas admiten las mismas opciones de extracción.

## Recorte de las siete provincias

Descarga completa. Se verificaron los 144 GeoTIFF y sus SHA-256, con una malla común de 2.388 × 1.144 celdas de 250 m y nodata -32768. Cada capa tiene de 995.617 a 1.087.623 píxeles válidos. Los GeoTIFF ocupan 135.364.189 bytes.

La descarga selecciona pH en agua, arena, limo, arcilla, carbono orgánico y nitrógeno total en seis profundidades hasta 200 cm. Para cada combinación conserva la media y los cuantiles 0,05, 0,50 y 0,95. El script lee ventanas de los VRT de ISRIC y aplica la máscara de las siete provincias, incluido Los Ríos, con límites DPA 2019. Preserva la proyección y cuadrícula nativas y el código de ausencia del VRT.

Desde la raíz, con el entorno local que incluye Rasterio y Shapely:

```powershell
& .\.venv-hls\Scripts\python.exe -u .\01_suelos_y_salud_del_suelo\ISRIC\descargar_soilgrids.py
```

En `soilgrids_2_costa_dpa2019/`, cada TIFF validado tiene un JSON con la fuente, las unidades, el divisor, el rango observado, el conteo de píxeles válidos y SHA-256. La descarga se puede reanudar con el mismo comando. El CSV provisional de esta carpeta pertenece a NASA POWER.

Actualizar el [registro regional de brechas](../../09_cobertura_y_brechas/ESTADO_POR_REGION.md) con los resultados de la evaluación.
