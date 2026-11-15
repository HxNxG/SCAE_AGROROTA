import unittest

from app.services.babahoyo_smap import read_moisture_frames


class BabahoyoSmapTests(unittest.TestCase):
    def test_depths_share_dates_and_original_grid_but_keep_distinct_values(self):
        surface = read_moisture_frames("surface")
        rootzone = read_moisture_frames("rootzone")
        frames = surface["frames"]
        self.assertEqual(surface["unit"], "m³/m³")
        self.assertEqual(surface["resolution_km"], 9)
        self.assertEqual([frame["time"] for frame in frames],
                         [f"2025-01-01T{hour:02d}:00:00Z" for hour in range(0, 24, 3)])
        for shallow, deep in zip(frames, rootzone["frames"], strict=True):
            self.assertEqual(shallow["time"], deep["time"])
            shallow_bounds = [tuple(cell["bounds"]) for cell in shallow["cells"]]
            self.assertEqual(len(set(shallow_bounds)), 28)
            self.assertEqual(shallow_bounds, [tuple(cell["bounds"]) for cell in deep["cells"]])
            self.assertNotEqual([cell["value"] for cell in shallow["cells"]],
                                [cell["value"] for cell in deep["cells"]])

        # Values from verified granules for cells EASE2_M09_r0835_c1075 and EASE2_M09_r0842_c1079.
        self.assertEqual(frames[0]["cells"][0]["value"], 0.26800495)
        self.assertEqual(rootzone["frames"][-1]["cells"][-1]["value"], 0.1233742)
