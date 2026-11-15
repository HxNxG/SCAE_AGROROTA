import importlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient


class RecommendationApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = importlib.import_module("backend.app")

    def test_two_scenarios_return_three_strategies_with_eighteen_months(self):
        with TestClient(self.api.app) as client:
            first = client.post("/api/recomendar", json={
                "zona": "Pimocha (Bajial)", "escenario_clima": "sequia",
                "meta": "resistir_sequia", "mes_inicio": 5,
            })
            second = client.post("/api/recomendar", json={
                "zona": "Caracol", "escenario_clima": "normal",
                "meta": "ahorrar_abono", "mes_inicio": 8,
            })
        for response, zone in [(first, "Pimocha (Bajial)"), (second, "Caracol")]:
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["zona"], zone)
            self.assertEqual([len(item["timeline"]) for item in data["estrategias"]], [18, 18, 18])
        self.assertNotEqual(first.json()["estrategias"], second.json()["estrategias"])

    def test_observation_is_written_only_to_temporary_review_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "pending.json"
            with patch.object(self.api, "OBSERVATIONS_PATH", path), TestClient(self.api.app) as client:
                response = client.post("/api/aportar-datos", json={
                    "sector": "Caracol", "categoria": "Prueba", "observacion": "Registro de prueba",
                })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["total_pendientes"], 1)
            entry, = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(entry["estado"], "PENDIENTE_REVISION_TECNICA")
