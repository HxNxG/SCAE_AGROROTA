"""Reúne tabulados provinciales de ediciones ESPAC anteriores."""

import json

from extraer import BASE, OUT, crop_rows, fetch, write

ROOT = BASE + "Estadisticas_agropecuarias/espac/"
SOURCES = {
    year: ROOT + f"espac-{year}/Tabulados%20ESPAC%20{year}.xlsx"
    for year in (2018, 2019, 2020, 2021)
}
SOURCES[2022] = ROOT + "espac_2022/Tabulados%20ESPAC%202022.xlsx"
SOURCES.update({
    year: ROOT + f"{year}/Tabulados_ESPAC_{year}.xlsx"
    for year in (2023, 2024)
})
EARLY = {
    2014: ROOT + "espac_2014-2015/2014/Indice%20de%20publicacion%20ESPAC-2014.xlsx",
    2015: ROOT + "espac_2014-2015/2015/Indice%20de%20publicacion%20ESPAC%202015.xlsx",
    2016: ROOT + "espac-2016/Indice%20de%20publicacion%20ESPAC%202016.xlsx",
    2017: ROOT + "espac_2017/Indice_de%20publicacion_ESPAC_2017.xlsx",
}
ARCHIVE = {
    year: ROOT + f"Publicaciones-espac/INDICE_PUBLICACION%20ESPAC%20{year}.xlsx"
    for year in range(2010, 2014)
}


def extract(sources, period):
    manifest = OUT / f"origen_{period}.json"
    inputs = {}
    records = []
    for year, url in sources.items():
        with_book = fetch(url, inputs, manifest)
        try:
            rows = crop_rows(with_book, year)
        finally:
            with_book.close()
        records.extend(rows)
        print(year, len(rows), flush=True)
    write(f"costa_cultivos_ediciones_{period}.csv", [
        "anio", "codigo_dpa", "provincia", "hoja", "fila_fuente", "producto",
        "condicion", "plantada_o_sembrada_ha", "cosechada_ha", "produccion_t",
        "ventas_t", "rendimiento_derivado_t_ha",
    ], records)
    manifest.write_text(json.dumps(inputs, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import sys

    periods = {"2010_2013": ARCHIVE, "2014_2017": EARLY, "2018_2024": SOURCES}
    period = sys.argv[1] if len(sys.argv) > 1 else "2018_2024"
    extract(periods[period], period)
