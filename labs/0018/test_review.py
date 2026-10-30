from datetime import date, timedelta
from pathlib import Path
import importlib.util
import unittest

spec = importlib.util.spec_from_file_location("review", Path(__file__).with_name("review.py"))
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class FreshnessTests(unittest.TestCase):
    def test_current_review(self):
        today = date(2026, 10, 30)
        self.assertEqual(review.check_freshness(today, today), 0)

    def test_boundary(self):
        today = date(2026, 10, 30)
        self.assertEqual(review.check_freshness(today - timedelta(days=30), today), 30)

    def test_expired_review(self):
        today = date(2026, 10, 30)
        with self.assertRaisesRegex(ValueError, "31"):
            review.check_freshness(today - timedelta(days=31), today)

    def test_future_date(self):
        today = date(2026, 10, 30)
        with self.assertRaises(ValueError):
            review.check_freshness(today + timedelta(days=1), today)


if __name__ == "__main__":
    unittest.main(verbosity=2)
