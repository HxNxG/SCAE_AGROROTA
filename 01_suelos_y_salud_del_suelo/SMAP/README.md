## Datos disponibles y recopilación en curso

La autenticación está verificada. Ya hay un [CSV de prueba validado y documentación de uso](datos/README.md); el histórico se está recopilando. La malla nativa selecciona 1.045 celdas, incluidas 134 que intersectan Los Ríos. Revisar [el estado del histórico](datos/historico/estado.json) para distinguir meses completos de pendientes. Estas notas actualizan los pendientes de la planificación inicial que aparece debajo.

# SMAP (Soil Moisture Active Passive)

Recurso oficial: https://smap.jpl.nasa.gov/

Tipo: Fuente o misión. Esta carpeta organiza la fuente; no representa un producto ya seleccionado o descargado.

## Acceso para la Costa ecuatoriana

**Actualización del 14/11/2026:** el equipo definió el período solicitado como 2010–actualidad y autorizó iniciar la recopilación. SMAP L4 está disponible desde 2015-03-31; el período anterior constituye una brecha de la fuente. Consultar el [estado de recopilación y creación de cuenta Earthdata](ESTADO_RECOPILACION.md). Las geometrías y metadatos públicos se recopilan primero; la humedad y la validación de la malla siguen pendientes. Esta actualización sustituye las menciones previas al histórico aún no definido.

1. Abrir el recurso oficial y localizar su catálogo o documentación de acceso a datos.
2. Seleccionar un producto concreto y registrar identificador, versión, variables, unidades, calidad, licencia y resolución.
3. Comprobar la cobertura del área de estudio en la Costa y del período requerido. Usar el polígono documentado del análisis.
4. Revisar requisitos de cuenta, autenticación y formatos en la documentación vigente. No guardar credenciales en este repositorio.
5. Consultar o solicitar un recorte espacial y temporal cuando la fuente lo permita. Estimar el tamaño antes de descargar.
6. Guardar los parámetros reproducibles y metadatos conforme a [REGLAS.md](../../REGLAS.md).

## Otras regiones

Seguir el [instructivo común](../../10_instructivos/ACCESO_A_OTRAS_REGIONES.md), reemplazando el área de estudio y verificando nuevamente cobertura y calidad. No asumir que todos los productos o plataformas admiten las mismas opciones de extracción.

## Información pendiente

Consultar el [plan de recopilación en CSV](PLAN_RECOPILACION_CSV.md): propone SPL4SMGP para humedad superficial y radicular, recorte por las siete provincias y controles explícitos de cobertura de Los Ríos. La revisión documental está realizada; la malla, los límites espaciales y la extracción siguen pendientes. Las siguientes selecciones y verificaciones deben completarse al ejecutar el plan.

- Producto, versión, variables y período: pendientes de selección.
- Cobertura y calidad en la Costa: pendientes de verificar.
- Resolución adecuada para decisiones agrícolas locales: pendiente de evaluar.
- Mecanismo de extracción y condiciones de uso: pendientes de verificar.
- Datos descargados: ninguno.

Actualizar el [registro regional de brechas](../../09_cobertura_y_brechas/ESTADO_POR_REGION.md) con los resultados de la evaluación.
