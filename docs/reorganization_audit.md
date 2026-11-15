# Auditoría de reorganización

Corte 2026-11-15. Base `9a0d9b107d9a43806e1da531a0cb28e9fa4d7442`. La copia de entrega estaba limpia. La rama local `biotinder/reorganization-audit` conserva el historial de esa base. El otro árbol de trabajo tiene cambios locales y queda fuera de la intervención.

## Inventario versionado

El inventario contó 1.211 archivos y 25 blobs vacíos con `git ls-tree -rl HEAD`. Las cantidades corresponden al commit base. Los datos sin seguimiento de la carpeta de trabajo no se contabilizan ni se usan como evidencia de reproducibilidad.

| Área | Archivos | Clasificación y estado |
| --- | ---: | --- |
| 01 Suelos | 347 | Muestras SMAP, geometría CONALI, manifiestos y metadatos, scripts Python/PowerShell, tablas derivadas y logs. SoilGrids tiene metadatos y productos según el inventario físico, con cobertura versionada distinta de la copia local. |
| 02 Clima | 17 | Tablas NASA POWER e IMERG, recortes y agregaciones de Babahoyo, documentación, procesadores y resultados. |
| 03 Agua | 264 | Rásteres y tablas de pilotos, documentación, código y manifiestos. Sin ruta activa al motor. |
| 04 Vegetación | 464 | Originales MODIS en NetCDF, TIFF y tablas derivadas, manifiestos, scripts y documentación. Solo el recorte MODIS de temperatura se sirve como capa activa del mapa. |
| 05 Topografía | 3 | Tabla cantonal, script y documentación. El entrenamiento contiene elevaciones anotadas; no lee esta tabla ni un ráster en ejecución. |
| 06 GIS | 4 | Guías de herramientas y consulta. |
| 07 Información agropecuaria | 17 | Libros fuente, extractos CSV, scripts, metadatos y documentación. El motor usa constantes propias. |
| 08 Experiencias | 1 | Guía. No constituye un corpus de observaciones. |
| 09 Cobertura | 1 | Estado y brechas. |
| 10 Acceso | 1 | Instructivo. |

Se encontraron 26 grupos de archivos no vacíos con blobs idénticos, con 176 copias adicionales y menos de 1 MiB total adicional al redondear. La identidad de contenido no identifica la función científica de cada ruta. Permanecen en su lugar. Los mayores blobs de la base incluyen GeoJSON de provincias (~19 MiB), mosaico RGB de Los Ríos (~18 MiB), IMERG Costa CSV (~16 MiB), segundo histórico IMERG (~8 MiB) y GeoJSON cantonal (~7 MiB). Si crecen las series, priorizar almacenamiento externo con manifiestos o Git LFS para nuevas entregas. Una migración retroactiva requeriría acuerdo y afectaría el historial.

## Dependencias y hallazgos

- `backend/app.py` expone las recomendaciones y los aportes; contiene los esquemas, reglas y la inferencia. El artefacto cargaba con una ruta relativa al proceso. La ruta de aportes tenía la misma dependencia. Las observaciones se almacenan como JSON local con estado pendiente. Aún no hay autenticación ni cola transaccional.
- El visor operativo es HTML/CSS/JavaScript bajo `proyecto-agricultura-ia/frontend/`. Su servidor Node enruta `/api/v1/` al backend cartográfico y las dos rutas de IA a FastAPI en la raíz. Archivos JSX vacíos, endpoints vacíos, Dockerfiles vacíos y `services: {}` son plantillas o marcadores.
- El backend cartográfico y los scripts navegan rutas de repositorio por carpeta y/o nivel de directorio. Mover los insumos alteraría validación, lectura de clima, transformaciones e hipervínculos. El README de ejecución documenta la descarga local opcional de archivos cartográficos.
- El entrenamiento escribe el CSV y el Joblib. No se debe ejecutar como comprobación de arranque. La bitácora de entrenamiento y el respaldo sintético necesitan verificación aparte. Consulte [datos y modelo](data_and_model.md).
- La confianza, el margen, el índice de fuerza del suelo, los costos y los resultados agronómicos requieren etiquetas de alcance. La división aleatoria del modelo no representa una prueba temporal, espacial ni de parcelas independientes.
- La demo de Pages y el visor comparten el módulo de tarjetas. Pages está preparado, con activación bloqueada por plan. La demo guardada no invoca el modelo.
- Se revisaron nombres versionados típicos de credenciales y las reglas de exclusión. Esta revisión no certifica todo el historial. No se exponen valores o archivos locales de autenticación.

## Mapa de rutas

| Ruta base | Ruta resultante | Motivo |
| --- | --- | --- |
| `backend/train_nn.py` (entrenamiento) | `backend/ml/train_nn.py` | Separar entrenamiento; el nombre anterior conserva un lanzador compatible. |
| `backend/app.py` | Igual | Punto de entrada `backend.app:app` usado por el equipo. |
| `backend/modelo_ensamble_babahoyo.joblib` | Igual | Artefacto versionado del modelo, sin modificar serialización. |
| `data/dataset_babahoyo_2005_2024.csv` | Igual | Datos derivados del entrenamiento, sin copia ni sobrescritura. |
| `01_*` a `10_*` | Igual | Paquetes por fuente con sus scripts, datos, metadatos y dependencias. |
| `proyecto-agricultura-ia/backend/app/`, `frontend/`, `scripts/`, `backend/tests/` | Igual | Entradas activas; moverlas duplicaría servicios o rompería rutas. |
| `README.md`, inventarios y guías existentes | Igual | Portada internacional y enlaces a guía técnica y evidencia. |
| Auditoría, metodología y verificación | `docs/` | Documentos transversales nuevos, sin duplicar fichas de producto. |

Una división física general en `raw/processed/metadata` se pospone. Los paquetes de datos reproducibles preservan la clasificación mediante sus manifiestos e inventarios. Las pruebas y scripts permanecen cerca de sus servicios.
