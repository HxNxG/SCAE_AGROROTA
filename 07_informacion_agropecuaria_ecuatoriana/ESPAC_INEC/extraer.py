"""Extrae estimaciones provinciales de los tabulados oficiales ESPAC 2025."""

import csv
import hashlib
import io
import json
import re
import shutil
import unicodedata
from pathlib import Path
from urllib.request import Request, urlopen

import openpyxl

OUT = Path(__file__).resolve().parent
BASE = "https://www.ecuadorencifras.gob.ec/documentos/web-inec/"
AGRO = BASE + "Estadisticas_agropecuarias/espac/2025/Tabulados_excel_2025.xlsx"
AMBIENTAL = BASE + "Encuestas_Ambientales/Modulo_Ambiental_ESPAC/2025/TABULADOS_MOD_AMB_ESPAC.xlsx"
PROVINCES = {
    "EL ORO": "07", "ESMERALDAS": "08", "GUAYAS": "09", "LOS RIOS": "12",
    "MANABI": "13", "SANTO DOMINGO DE LOS TSACHILAS": "23", "SANTA ELENA": "24",
}


def normalize(value):
    text = unicodedata.normalize("NFKD", str(value))
    return " ".join("".join(c for c in text if not unicodedata.combining(c)).upper().split())


def fetch(url, inputs, manifest):
    with urlopen(Request(url, method="HEAD"), timeout=30) as response:
        size = int(response.headers.get("Content-Length") or 20_000_000)
    free = shutil.disk_usage(OUT).free
    if size > 20_000_000 or free < size * 2:
        raise ValueError(f"Tamaño inesperado o espacio insuficiente: {url}")
    inputs[url] = {"estimated_bytes": size, "free_bytes": free}
    manifest.write_text(json.dumps(inputs, indent=2), encoding="utf-8")
    with urlopen(url, timeout=60) as response:
        data = response.read(20_000_001)
    if len(data) > 20_000_000:
        raise ValueError(f"Descarga demasiado grande: {url}")
    inputs[url].update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    return openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)


def write(name, columns, records):
    target = OUT / name
    with target.with_suffix(".part").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(records)
    target.with_suffix(".part").replace(target)


def province_rows(sheet, column):
    for index, row in enumerate(sheet.values, 1):
        province = normalize(row[column])
        if province in PROVINCES:
            yield [2025, PROVINCES[province], row[column].strip(), sheet.title, index], row


def crop_rows(book, year):
    titles = {}
    for row in book.worksheets[0].values:
        cells = [value.strip() for value in row if isinstance(value, str) and value.strip()]
        if len(cells) >= 2 and cells[0].startswith("T"):
            key = cells[0].rstrip(".").replace(" ", "")
            parts = re.split(r"según región y provincia", cells[1], maxsplit=1, flags=re.I)
            if len(parts) == 2 and normalize(parts[1]):
                titles[key] = parts[1].strip()
    crops = []
    for number in range(11 if year <= 2015 else 12, 50 if year <= 2017 else 49):
        if year <= 2015 and "(" not in titles.get(f"T{number}", ""):
            continue
        key = f"T{number}"
        sheet = book[key if key in book.sheetnames else f"T {number}"]
        province = None
        start = len(crops)
        product = titles[key]
        for index, original in enumerate(sheet.values, 1):
            row = (None,) + original if year <= 2016 else original
            if row[1] is not None:
                label = normalize(row[1])
                if year == 2019 and number == 13 and label.startswith("TABLA 13."):
                    product = "banano (fruta fresca) - " + (
                        "exportación en monocultivo" if label.startswith("TABLA 13.1")
                        else "otras provincias y condiciones"
                    )
                province_name = "EL ORO" if label == "ELORO" else str(row[1]).strip()
                province = PROVINCES.get(normalize(province_name))
            if province and normalize(row[2]) in {"SOLO", "ASOCIADO"}:
                values = [None if v in (".", "..", "*") else v for v in row[3:7]]
                planted, harvested, production, sales = values
                assert all(v is None or isinstance(v, (int, float)) for v in values)
                yield_t_ha = production / harvested if harvested and production is not None else None
                crops.append([year, province, province_name, sheet.title, index,
                              product, row[2].strip(), planted, harvested,
                              production, sales, yield_t_ha])
        assert len(crops) > start, sheet.title
        if year == 2025:
            assert len(crops) - start == 14, sheet.title
    return crops


def main():
    inputs = {}
    with_agro = fetch(AGRO, inputs, OUT / "origen.json")
    ambient = fetch(AMBIENTAL, inputs, OUT / "origen.json")
    common = ["anio", "codigo_dpa", "provincia", "hoja", "fila_fuente"]
    land = [(key + list(row[2:11])) for key, row in province_rows(with_agro["T1"], 1)]
    assert len(land) == 7
    write("costa_uso_suelo_2025.csv", common + [
        "total_ha", "permanentes_ha", "transitorios_barbecho_ha", "descanso_ha",
        "pastos_cultivados_ha", "pastos_naturales_ha", "paramos_ha",
        "montes_bosques_ha", "otros_usos_ha",
    ], land)

    crops = crop_rows(with_agro, 2025)
    write("costa_cultivos_2025.csv", common + [
        "producto", "condicion", "plantada_o_sembrada_ha", "cosechada_ha",
        "produccion_t", "ventas_t", "rendimiento_derivado_t_ha",
    ], crops)

    irrigation = [key + list(row[2:9]) for key, row in province_rows(ambient["T14"], 1)]
    tillage = [key + list(row[3:7]) for key, row in province_rows(ambient["IND_1"], 2)]
    assert len(irrigation) == len(tillage) == 7
    write("costa_riego_transitorios_2025.csv", common + [
        "surcos_ha", "aspersion_ha", "microaspersion_ha", "goteo_ha",
        "nebulizacion_ha", "otro_ha", "total_ha",
    ], irrigation)
    write("costa_labranza_transitorios_2025.csv", common + [
        "convencional_ha", "reducida_ha", "cero_labranza_ha", "total_ha",
    ], tillage)
    (OUT / "origen.json").write_text(json.dumps(inputs, indent=2), encoding="utf-8")
    print(len(crops), len(land), len(irrigation), len(tillage))


if __name__ == "__main__":
    main()
