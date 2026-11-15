import unittest

from app.services.parcel_geography import _in_polygon, validate_point


class ParcelGeographyTests(unittest.TestCase):
    def test_babahoyo_point_and_outside_point(self):
        self.assertTrue(validate_point(-79.526, -1.802)["accepted"])
        self.assertFalse(validate_point(-78.5, -1.8)["accepted"])

    def test_geojson_order_and_invalid_coordinates(self):
        result = validate_point(-79.526, -1.802)
        self.assertEqual(result["point"]["coordinates"], [-79.526, -1.802])
        self.assertEqual(result["location_type"], "point")
        with self.assertRaises(ValueError):
            validate_point(float("nan"), -1.802)
        with self.assertRaises(ValueError):
            validate_point(-79.526, 91)

    def test_hole_and_boundary(self):
        outer = [[0, 0], [4, 0], [4, 4], [0, 4], [0, 0]]
        hole = [[1, 1], [3, 1], [3, 3], [1, 3], [1, 1]]
        self.assertTrue(_in_polygon(0, 2, [outer, hole]))
        self.assertFalse(_in_polygon(2, 2, [outer, hole]))
        self.assertTrue(_in_polygon(1, 2, [outer, hole]))


if __name__ == "__main__":
    unittest.main()
