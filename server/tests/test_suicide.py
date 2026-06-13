import unittest

from suicide import analyze_text


class SuicideAnalysisTests(unittest.TestCase):
    def test_hebrew_benign_content_is_not_high_risk(self):
        result = analyze_text("פוקצ׳ות ללא לישה ! עוד לחם להיט להכין סתם באמצע שבוע לילדים")
        self.assertFalse(result["is_high_risk"])

    def test_explicit_english_warning_is_high_risk(self):
        result = analyze_text("I want to end my life tonight")
        self.assertTrue(result["is_high_risk"])


if __name__ == "__main__":
    unittest.main()
