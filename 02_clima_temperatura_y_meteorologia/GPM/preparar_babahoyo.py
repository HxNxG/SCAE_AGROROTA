"""Construye una serie mensual de precipitación IMERG para Babahoyo.

Usa únicamente los agregados cantonales IMERG ya validados del repositorio.
No descarga ni modifica las fuentes de origen.
"""

import csv
import hashlib
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = (
    HERE / "IMERG_cantones_costa_2010-01_2014-12.csv",
    HERE / "IMERG_cantones_los_rios_2015-01_2025-09.csv",
)
OUTPUT = HERE / "IMERG_Babahoyo_2010-01_2025-09.csv"
MANIFEST = HERE / "babahoyo_2010-01_2025-09.json"
EXPECTED_MONTHS = 189
EXPECTED_CODE = "1201"
EXPECTED_NAME = "BABAHOYO"
FIELDS = (
    "mes", "codigo_dpa", "canton", "celdas", "area_intersectada_km2",
    "fraccion_cubierta", "precipitacion_media_mm", "indice_calidad_medio",
    "error_aleatorio_medio_por_celda_mm",
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_source(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError(f"Encabezado inesperado en {path.name}")
        rows = {}
        for row in reader:
            if row["codigo_dpa"] != EXPECTED_CODE or row["canton"] != EXPECTED_NAME:
                continue
            month = row["mes"]
            if month in rows:
                raise ValueError(f"Mes duplicado en {path.name}: {month}")
            if len(month) != 7 or month[4] != "-":
                raise ValueError(f"Mes inválido: {month}")
            rows[month] = row
    if not rows:
        raise ValueError(f"No se encontraron filas de Babahoyo en {path.name}")
    return rows


def expected_months():
    months = []
    year, month = 2010, 1
    while (year, month) <= (2025, 9):
        months.append(f"{year:04d}-{month:02d}")
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return months


def main():
    rows = {}
    for source in SOURCES:
        source_rows = read_source(source)
        overlap = set(rows) & set(source_rows)
        if overlap:
            raise ValueError(f"Fuentes se traslapan: {sorted(overlap)}")
        rows.update(source_rows)
    months = expected_months()
    if len(months) != EXPECTED_MONTHS or sorted(rows) != months:
        missing = sorted(set(months) - set(rows))
        extra = sorted(set(rows) - set(months))
        raise ValueError(f"Cobertura mensual incompleta; faltan={missing}, sobran={extra}")
    for month, row in rows.items():
        if int(row["celdas"]) < 1 or not 0.99 <= float(row["fraccion_cubierta"]) <= 1.001:
            raise ValueError(f"Cobertura geométrica inválida en {month}")
        if any(float(row[field]) < 0 for field in FIELDS[6:]):
            raise ValueError(f"Valor negativo en {month}")

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows[month] for month in months)

    manifest = {
        "institucion": "NASA Goddard Space Flight Center (GPM)",
        "producto": "IMERG Final Run L3 mensual, GPM_3IMERGM colección 07, V07B",
        "doi": "10.5067/GPM/IMERG/3B-MONTH/07",
        "distribuidor": "University of South Florida ERDDAP, IMERG_monthly_global_precip",
        "url_distribuidor": "https://erddap.marine.usf.edu/erddap/griddap/IMERG_monthly_global_precip.das",
        "condiciones": "El catálogo marca acceso público y licencia de obras del Gobierno de EE. UU.; ver https://www.usa.gov/government-works. Conservar atribución a NASA GPM.",
        "fecha_preparacion": date.today().isoformat(),
        "area": {"pais": "Ecuador", "provincia": "Los Ríos", "canton": "Babahoyo", "codigo_dpa": EXPECTED_CODE,
                 "limite": "DPA 2019 EEQ; límites cantonales, sistema lon/lat WGS84"},
        "periodo_efectivo": {"inicio": months[0], "fin": months[-1], "meses": len(months), "continuo": True},
        "variables": {
            "precipitacion_media_mm": "Acumulado mensual ponderado por área de celda (mm).",
            "indice_calidad_medio": "Índice de calidad de precipitación, adimensional; no se aplicó filtro.",
            "error_aleatorio_medio_por_celda_mm": "Error aleatorio mensual promedio de las celdas; no es incertidumbre del promedio cantonal.",
        },
        "resolucion_origen": "IMERG 0.1°; resumen mensual espacial ponderado por intersección geodésica con DPA 2019.",
        "metodo": "Filtrar codigo_dpa=1201 y canton=BABAHOYO de cada fuente, concatenar los tramos y verificar meses continuos sin duplicados.",
        "fuentes": [
            {"archivo": path.name, "sha256": sha256(path)} for path in SOURCES
        ],
        "salida": {"archivo": OUTPUT.name, "filas": len(months), "sha256": sha256(OUTPUT)},
        "limitaciones": [
            "La resolución de 0.1° y el promedio cantonal no representan lluvia medida en una parcela.",
            "El rectángulo original de descarga podía incluir mar; el agregado cantonal usa intersecciones con el polígono DPA.",
            "La serie disponible termina en septiembre de 2025; octubre de 2025 a la fecha de preparación no está incluido.",
            "No sustituye observaciones locales ni una estación pluviométrica; validar sesgo y latencia antes de uso operativo.",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{OUTPUT.name}: {len(months)} filas, {months[0]} a {months[-1]}")
    print(f"SHA-256 {OUTPUT.name}: {manifest['salida']['sha256']}")
    print(f"Manifiesto: {MANIFEST.name}")


if __name__ == "__main__":
    main()
