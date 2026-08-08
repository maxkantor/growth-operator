import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "growth_operator.py"
SPEC = importlib.util.spec_from_file_location("growth_operator", MODULE_PATH)
growth_operator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(growth_operator)


class GrowthOperatorTests(unittest.TestCase):
    def test_first_match_normalizes_markup_text(self):
        source = "<h1>  Daily <span>Workout</span> Plan </h1>"
        value = growth_operator.first_match(r"<h1[^>]*>(.*?)</h1>", source)
        self.assertEqual(value, "Daily <span>Workout</span> Plan")

    def test_unavailable_site_is_first_priority(self):
        action = growth_operator.choose_action({"decision": "focus"}, 0, ["healthy"], 0)
        self.assertIn("availability", action)

    def test_focus_site_gets_offer_experiment(self):
        action = growth_operator.choose_action({"decision": "focus"}, 200, [], 20)
        self.assertIn("offer experiment", action)


if __name__ == "__main__":
    unittest.main()
