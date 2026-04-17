from django.test import TestCase


class AnalysisApiTests(TestCase):
    def test_analysis_endpoints_return_chart_rows(self):
        endpoints = [
            "/api/summary/",
            "/api/analysis/province-sales",
            "/api/analysis/shop-sales",
            "/api/analysis/style-price",
            "/api/analysis/pattern-price",
            "/api/analysis/fabric-price",
            "/api/analysis/fit-price",
        ]

        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                self.assertEqual(response.status_code, 200)
                payload = response.json()
                self.assertEqual(payload["code"], "0")
                self.assertIsInstance(payload["data"], list)
                self.assertGreater(len(payload["data"]), 0)
                self.assertEqual(set(payload["data"][0].keys()), {"name", "value"})
