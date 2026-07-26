import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rocket_curriculum import all_modules, search_curriculum, validate_curriculum  # noqa: E402


class RocketCurriculumTests(unittest.TestCase):
    def test_curriculum_is_structurally_complete(self):
        self.assertEqual(validate_curriculum(), [])
        modules = all_modules()
        self.assertEqual(len(modules), 14)
        self.assertEqual([item["number"] for item in modules], list(range(1, 15)))
        self.assertEqual(sum(len(item["seminars"]) for item in modules), 84)

    def test_every_module_meets_research_standard(self):
        for item in all_modules():
            with self.subTest(module=item["slug"]):
                self.assertEqual(len(item["outcomes"]), 4)
                self.assertEqual(len(item["equations"]), 4)
                self.assertEqual(len(item["seminars"]), 6)
                self.assertEqual(len(item["research_questions"]), 4)
                self.assertGreaterEqual(len(item["sources"]), 3)
                self.assertTrue(item["lab"]["type"])
                for seminar in item["seminars"]:
                    self.assertEqual(len(seminar["sections"]), 7)
                    self.assertGreaterEqual(seminar["word_count"], 500)
                    self.assertTrue(seminar["failure"])

    def test_search_reaches_specialist_content(self):
        cavitation = search_curriculum("cavitation")
        self.assertTrue(
            any(
                result["module"]["slug"]
                == "liquid-engine-cycles-and-turbomachinery"
                for result in cavitation
            )
        )
        assurance = search_curriculum("assurance evidence")
        self.assertTrue(any(result["kind"] == "Research seminar" for result in assurance))


if __name__ == "__main__":
    unittest.main()
