import unittest

from app.services.babahoyo_modis import read_temperature_frames


def values(frame):
    return [cell["value"] for cell in frame["cells"] if cell["value"] is not None]


class BabahoyoModisTests(unittest.TestCase):
    def test_contiguous_months_preserve_native_cells_for_both_bands(self):
        day = read_temperature_frames("day")
        night = read_temperature_frames("night")
        self.assertEqual(day["unit"], "°C")
        self.assertEqual(day["resolution_degrees"], 0.05)
        months = [frame["time"] for frame in day["frames"]]
        self.assertEqual(len(months), 202)
        self.assertEqual(len(set(months)), 202)
        self.assertEqual((months[0], months[-1]), ("2010-01", "2026-10"))
        self.assertEqual(months, [frame["time"] for frame in night["frames"]])
        bounds = [cell["bounds"] for cell in day["frames"][0]["cells"]]
        self.assertEqual(len(bounds), 61)
        for series in (day, night):
            for frame in series["frames"]:
                self.assertEqual([cell["bounds"] for cell in frame["cells"]], bounds)

    def test_masks_and_converts_first_and_last_source_months(self):
        day = read_temperature_frames("day")["frames"]
        night = read_temperature_frames("night")["frames"]
        self.assertEqual((len(values(day[0])), len(values(day[-1]))), (9, 1))
        self.assertEqual((len(values(night[0])), len(values(night[-1]))), (17, 3))
        self.assertEqual(sum(not values(frame) for frame in day), 20)
        self.assertEqual(sum(not values(frame) for frame in night), 22)
        self.assertEqual(day[0]["cells"][3]["value"], 31.45)
        self.assertEqual(night[0]["cells"][3]["value"], 19.73)
        self.assertIsNone(day[0]["cells"][0]["value"])
