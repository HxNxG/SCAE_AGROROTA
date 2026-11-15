# GRACE y GRACE-FO

Recurso oficial: https://grace.jpl.nasa.gov/

Producto incorporado: [CSR GRACE/GRACE-FO RL06.3 Mascon, con correcciones aplicadas](https://www2.csr.utexas.edu/grace/RL0603_mascons.html), de la Universidad de Texas en Austin. Citar al CSR y el [DOI 10.15781/cgq9-nh24](https://doi.org/10.15781/cgq9-nh24). Consultar la política de datos en los metadatos.

## Acceso para la Costa ecuatoriana

1. Abrir el recurso oficial y localizar su catálogo o documentación de acceso a datos.
2. Seleccionar un producto concreto y registrar identificador, versión, variables, unidades, calidad, licencia y resolución.
3. Comprobar la cobertura del área de estudio en la Costa y del período requerido. Usar el polígono documentado del análisis.
4. Revisar requisitos de cuenta, autenticación y formatos en la documentación vigente. No guardar credenciales en este repositorio.
5. Consultar o solicitar un recorte espacial y temporal cuando la fuente lo permita. Estimar el tamaño antes de descargar.
6. Guardar los parámetros reproducibles y metadatos conforme a [REGLAS.md](../../REGLAS.md).

## Otras regiones

Seguir el [instructivo común](../../10_instructivos/ACCESO_A_OTRAS_REGIONES.md), reemplazando el área de estudio y verificando nuevamente cobertura y calidad. No asumir que todos los productos o plataformas admiten las mismas opciones de extracción.

## Datos incorporados para la Costa

La extracción del 14 de noviembre de 2026 contiene 171 intervalos publicados en 169 meses con fecha central entre enero de 2010 y septiembre de 2026. Se conservan los dos intervalos de octubre de 2011 y los dos de abril de 2015. Usar inicio y fin como clave temporal. Los 32 meses sin fecha central se listan en `metadatos_csr.json`.

- `csr_rl063_costa_celdas.csv` contiene 22.401 registros en 131 celdas terrestres de 0,25°, con coordenadas geográficas, área intersectada y anomalía en centímetros de agua equivalente respecto de 2004–2009.
- `csr_rl063_costa_mensual.csv` contiene el promedio regional por intervalo, ponderado por el área geodésica de intersección con las siete provincias DPA 2019. Se aplicó la máscara terrestre de CSR. El área de malla retenida es de aproximadamente 71.061 km².
- `metadatos_csr.json` registra la fuente, la delimitación, las advertencias de calidad instrumental del producto y los SHA-256 de ambas salidas. El producto no suministra incertidumbre por celda en este archivo.

La resolución gravitacional efectiva es de aproximadamente 300 km. El área retenida está por debajo de los 200.000 km² para los que el proveedor recomienda precaución. Usar este agregado como contexto regional exploratorio de sequía y almacenamiento total. La resolución de 0,25° es la cuadrícula de representación.

Para reproducir, ejecutar `extraer_csr.py` con el entorno `.venv-smap`. Lee ventanas remotas por HTTP Range y guarda el recorte tabular.

Actualizar el [registro regional de brechas](../../09_cobertura_y_brechas/ESTADO_POR_REGION.md) con los resultados de la evaluación.
