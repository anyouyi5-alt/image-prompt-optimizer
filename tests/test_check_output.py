"""Meaningful checks for the image prompt constraint validator."""

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_output import validate  # noqa: E402


class ImagePromptChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.brief = json.loads((ROOT / "examples/brief.json").read_text(encoding="utf-8"))
        cls.result = json.loads((ROOT / "examples/result.json").read_text(encoding="utf-8"))

    def test_example_satisfies_explicit_constraints(self) -> None:
        self.assertEqual(validate(self.brief, self.result), [])

    def test_standalone_example_satisfies_explicit_constraints(self) -> None:
        brief = json.loads(
            (ROOT / "examples/standalone-brief.json").read_text(encoding="utf-8")
        )
        result = json.loads(
            (ROOT / "examples/standalone-result.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate(brief, result), [])

    def test_missing_required_detail_is_reported(self) -> None:
        result = copy.deepcopy(self.result)
        result["positive_prompt"] = result["positive_prompt"].replace("红色气球", "气球")
        self.assertTrue(any("红色气球" in error for error in validate(self.brief, result)))

    def test_forbidden_phrase_in_positive_prompt_is_reported(self) -> None:
        result = copy.deepcopy(self.result)
        result["positive_prompt"] += " 画面有水印。"
        self.assertTrue(any("水印" in error for error in validate(self.brief, result)))

    def test_first_frame_notes_are_required(self) -> None:
        result = copy.deepcopy(self.result)
        result["first_frame_notes"] = ""
        self.assertTrue(any("first_frame_notes" in error for error in validate(self.brief, result)))

    def test_aspect_ratio_must_match(self) -> None:
        result = copy.deepcopy(self.result)
        result["aspect_ratio"] = "16:9"
        self.assertTrue(any("aspect_ratio" in error for error in validate(self.brief, result)))


if __name__ == "__main__":
    unittest.main()
