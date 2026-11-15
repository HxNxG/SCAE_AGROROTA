## Actualización: acceso verificado y CSV reales disponibles

La autenticación Earthdata fue verificada el 14/11/2026. Se construyó la malla nativa por intersección: 1.045 celdas, 134 de ellas en Los Ríos; cobertura geométrica completa respecto de las siete provincias y los 13 cantones de referencia DPA 2019. Hay un día validado con 8.360 filas y se inició el histórico por OPeNDAP. Consultar [datos/README.md](datos/README.md) y [datos/historico/estado.json](datos/historico/estado.json). Las notas iniciales de este documento que indican ausencia de autenticación, malla o datos quedan sustituidas por esta actualización.

El catálogo histórico contiene 33.944 intervalos únicos tras depurar 33.961 registros. El resultado esperado es 35.471.480 filas; no se declara completo hasta que el estado lo confirme. El extremo efectivo seleccionado es 2026-11-11 00:00 UTC, exclusivo. La descarga utiliza subconjuntos DAP4 y no archivos globales completos.

# Recopilación SMAP: estado y acceso

Inicio: 14 de noviembre de 2026. Período solicitado por el equipo: **2010–actualidad**. Corte de esta ejecución: 2026-11-14; los archivos disponibles pueden terminar antes.

## Lo que se está recopilando

Ejecución terminada: se guardaron nueve archivos de geografía y metadatos, aproximadamente 27,9 MB en total, con inventario de tamaños y SHA-256. No contienen observaciones de humedad.

- `geografia/costa_provincias_referencia_2019.geojson`: siete provincias, incluyendo Los Ríos, en WGS84.
- `geografia/los_rios_cantones_referencia_2019.geojson`: polígonos de los 13 cantones de Los Ríos.
- `geografia/los_rios_cantones.csv`: inventario cantonal.
- `geografia/limites_por_provincia.csv`: cajas envolventes consultadas al servicio.
- `metadatos/`: colección CMR, primeros y últimos granules, disponibilidad anual y manifiesto de consultas.
- `archivos_recopilados.csv`: tamaños y sumas SHA-256 para comprobar integridad.

Reproducción desde PowerShell:

```powershell
& './01_suelos_y_salud_del_suelo/SMAP/recopilar_metadatos.ps1' -Cutoff '2026-11-14T23:59:59Z'
```

El script consulta recursos públicos, valida siete provincias y 13 cantones, y guarda metadatos y geometrías. **No descarga humedad ni genera una malla SMAP.** La caja envolvente es un filtro inicial de catálogo; no es la máscara final del análisis. El conteo de granules globales no demuestra valores válidos sobre cada provincia.

## Alcance geográfico provisional

Fuente: [servicio cartográfico institucional de EEQ, provincias](https://geoportal.eeq.com.ec/arcgis/rest/services/WEBGIS/Visor_cartografia/MapServer/31) y [cantones](https://geoportal.eeq.com.ec/arcgis/rest/services/WEBGIS/Visor_cartografia/MapServer/30). Los atributos declaran DPA 2019. Se conserva ese año en nombres y metadatos para no presentarlo como un límite actualizado a 2026.

La cartografía se utiliza como referencia técnica provisional. Falta contrastar cambios territoriales con una fuente actual, validar topología y calcular cobertura por intersección con celdas SMAP. Que los 13 polígonos estén descargados no significa que ya se haya validado cobertura de humedad en los 13 cantones.

## Disponibilidad temporal

La colección `SPL4SMGP` v008 identificada en [CMR](https://cmr.earthdata.nasa.gov/search/collections.json?short_name=SPL4SMGP&version=008&page_size=10) es `C3480440870-NSIDC_CPRD` y comienza el 2015-03-31.

La consulta ejecutada encontró 33.961 registros de granules. El primer intervalo empieza el 2015-03-31 a las 00:00 UTC y el último encontrado empieza el 2026-11-10 a las 21:00 UTC y termina el 2026-11-11 a las 00:00 UTC. Es una instantánea del catálogo, no una garantía de continuidad ni un inventario de instantes únicos: las consultas temporales pueden incluir intervalos que tocan el límite anual y archivos reprocesados. Antes de extraer, deduplicar por intervalo y versión científica conforme a la documentación y revisar huecos.

La caja envolvente calculada por el servicio es aproximadamente: oeste -81,011346; sur -3,889949; este -78,426389; norte 1,469581 grados WGS84. Incluye las siete provincias de referencia. No debe utilizarse como sustituto del recorte poligonal: también contiene territorio exterior al área de estudio y zonas marinas.

Registrar 2010-01-01 a 2015-03-30 como período sin datos SMAP L4. No rellenarlo con cero ni presentar otra fuente como SMAP. Las fechas exactas observadas y la última disponibilidad consultada quedan en `metadatos/manifiesto_recopilacion.json` al terminar el script. La última fecha publicada no asegura que todos los intervalos anteriores estén completos.

## Paso pendiente del usuario: autenticar la cuenta localmente

1. Crear una cuenta gratuita en [NASA Earthdata Login](https://urs.earthdata.nasa.gov/users/new).
2. Verificar el correo y comprobar que se puede iniciar sesión en [Earthdata Search, colección SMAP L4 v8](https://search.earthdata.nasa.gov/search/granules?p=C3480440870-NSIDC_CPRD).
3. Avisar que la cuenta está lista. No enviar contraseña, tokens ni códigos privados al chat. La autenticación se realizará localmente cuando se configure la extracción.

El usuario confirmó que ya creó la cuenta. Se preparó un entorno Python aislado y un formulario de terminal mediante earthaccess. Falta que el usuario complete la autenticación local; no se han realizado solicitudes autenticadas ni descargado humedad. No se ha probado todavía qué transformación de Harmony está disponible para la selección concreta.

## Continuación tras disponer del acceso

1. Validar límites y construir la selección de celdas nativas por intersección; comprobar cobertura de Los Ríos y sus cantones.
2. Probar un lote pequeño recortado con `sm_surface`, `sm_rootzone`, geolocalización y atributos auxiliares, antes de solicitar el histórico.
3. Verificar relleno, unidades, tiempos, máscaras y trazabilidad; exportar CSV y medir el tamaño real por mes.
4. Recopilar el intervalo efectivo disponible por lotes acotados, conservando CSV comprimidos y evitando descargar todo el archivo global.
5. Revisar los avisos de geolocalización y reprocesamiento de 2026 en la [ficha oficial](https://nsidc.org/data/spl4smgp/versions/8) antes de aceptar esos meses.

La conversión y descarga científica no se dan por realizadas con estos metadatos. Véase el [plan técnico](PLAN_RECOPILACION_CSV.md) para esquema CSV, calidad y limitaciones agronómicas.

## Autenticación desde la terminal de VS Code

Validación geométrica ejecutada: las siete geometrías provinciales de referencia son válidas y la unión de los 13 cantones coincide con Los Ríos (sin área faltante ni excedente calculada; solapamiento residual numérico despreciable). Los resultados están en `geografia/verificacion_geografica.json` y `geografia/verificacion_los_rios_cantones.csv`. Esto no sustituye la comprobación de límites actuales ni la cobertura de celdas SMAP.

Desde la raíz del repositorio, ejecutar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\01_suelos_y_salud_del_suelo\SMAP\autenticar_earthdata.ps1
```

El script solicita usuario y contraseña en la terminal, utilizando la [autenticación interactiva de earthaccess](https://earthaccess.readthedocs.io/en/stable/user/howto/authenticate/). La contraseña no se muestra al escribir. `persist=True` guarda credenciales en el archivo de autenticación del perfil de Windows, fuera del repositorio; no subir ese archivo ni compartirlo. Solo se escribe un indicador de éxito sin secretos en `metadatos/autenticacion_estado.json`. La cuenta creada no equivale a una sesión ya autenticada.

El entorno `.venv-smap` está excluido de Git. Las dependencias se declaran en `requirements.txt`. El script `verificar_geografia.py` valida las geometrías de referencia, prepara su unión y compara áreas cantonales con Los Ríos, sin afirmar que ya exista cobertura SMAP validada.
