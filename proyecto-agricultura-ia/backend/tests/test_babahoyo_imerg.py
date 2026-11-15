import csv
import unittest
from pathlib import Path

from app.services.babahoyo_imerg import read_precipitation_cells


GPM = Path(__file__).resolve().parents[3] / "02_clima_temperatura_y_meteorologia" / "GPM"


class BabahoyoImergTests(unittest.TestCase):
    def test_cells_match_original_csv_in_both_segments(self):
        for month, segment in (
            ("2010-01", "2010-01_2014-12"),
            ("2025-09", "2015-01_2025-09"),
        ):
            with self.subTest(month=month):
                layer = read_precipitation_cells(month)
                self.assertEqual(layer["month"], month)
                self.assertEqual(layer["unit"], "mm")
                self.assertIn("GPM_3IMERGM V07B", layer["source"])
                self.assertEqual(len(layer["cells"]), 22)

                actual = {}
                for cell in layer["cells"]:
                    west, south, east, north = cell["bounds"]
                    self.assertAlmostEqual(east - west, 0.1)
                    self.assertAlmostEqual(north - south, 0.1)
                    center = (round((west + east) / 2, 2), round((south + north) / 2, 2))
                    self.assertNotIn(center, actual)
                    actual[center] = cell["precipitation_mm"]

                expected = {}
                with (GPM / f"IMERG_Costa_{segment}.csv").open(encoding="utf-8", newline="") as stream:
                    timestamp = f"{month}-01T00:00:00Z"
                    for row in csv.DictReader(stream):
                        if row["time"] == timestamp:
                            center = (round(float(row["longitude"]), 2), round(float(row["latitude"]), 2))
                            if center in actual:
                                expected[center] = float(row["precipitation"])
                self.assertEqual(actual, expected)

    def test_valid_month_outside_coverage_has_no_cells(self):
        for month in ("2009-12", "2025-10"):
            with self.subTest(month=month):
                layer = read_precipitation_cells(month)
                self.assertEqual(layer["month"], month)
                self.assertEqual(layer["cells"], [])
