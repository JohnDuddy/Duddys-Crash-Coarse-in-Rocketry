import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import APP_NAME, REPOSITORY_URL, app  # noqa: E402
from rocket_curriculum import all_modules  # noqa: E402


class RocketAppTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_home_and_public_project_identity(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(APP_NAME.replace("'", "&#39;").encode(), response.data)
        self.assertIn(b"<strong>14</strong> technical modules", response.data)
        self.assertIn(b"<strong>84</strong> research seminars", response.data)
        self.assertIn(REPOSITORY_URL.encode(), response.data)
        self.assertEqual(response.data.count(b'class="module-card reveal"'), 14)

    def test_every_module_and_seminar_route(self):
        for item in all_modules():
            with self.subTest(module=item["slug"]):
                module_response = self.client.get(f"/module/{item['slug']}")
                self.assertEqual(module_response.status_code, 200)
                self.assertEqual(
                    module_response.data.count(b'class="seminar-card reveal"'),
                    6,
                )
                self.assertEqual(
                    module_response.data.count(b'class="equation-card reveal"'),
                    4,
                )
                self.assertIn(b"data-rocket-lab", module_response.data)
                self.assertIn(b"data-lab-canvas", module_response.data)
                self.assertIn(b"data-engineering-model", module_response.data)
                self.assertIn(b"data-model-canvas", module_response.data)
                self.assertIn(b"THEORY / DERIVATION", module_response.data)
                self.assertIn(b"PRACTICAL / WORKED CASE", module_response.data)
                for seminar in item["seminars"]:
                    response = self.client.get(
                        f"/module/{item['slug']}/seminar/{seminar['number']}"
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        response.data.count(b'class="transcript-section reveal"'),
                        7,
                    )
                    self.assertIn(b"data-audio-play", response.data)
                    self.assertIn(b"data-play-from", response.data)

    def test_review_funding_sources_search_and_404(self):
        review = self.client.get("/review")
        self.assertEqual(review.status_code, 200)
        self.assertEqual(review.data.count(b"data-review-criterion"), 10)
        self.assertIn(b'placeholder="Independent reviewer"', review.data)
        self.assertIn(b"data-review-export", review.data)
        self.assertEqual(self.client.get("/funding").status_code, 200)
        sources = self.client.get("/sources")
        self.assertEqual(sources.status_code, 200)
        self.assertEqual(sources.data.count(b'class="reveal"'), 18)
        search = self.client.get("/search?q=cavitation")
        self.assertEqual(search.status_code, 200)
        self.assertIn(b"Cavitation", search.data)
        self.assertEqual(self.client.get("/module/not-real").status_code, 404)

    def test_health_report(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["modules"], 14)
        self.assertEqual(payload["seminars"], 84)
        self.assertGreater(payload["seminar_words"], 43_000)
        self.assertEqual(payload["mathematics_studios"], 14)
        self.assertEqual(payload["interactive_3d_models"], 14)
        self.assertEqual(payload["primary_sources"], 18)
        self.assertEqual(payload["curriculum_errors"], [])


if __name__ == "__main__":
    unittest.main()
