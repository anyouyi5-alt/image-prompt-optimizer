"""Check explicit, literal constraints in an image prompt result."""

import json
import sys
import unicodedata
from pathlib import Path


def normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def string_list(value: object, field: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        errors.append(f"{field} must be an array of non-empty strings")
        return []
    return value


def validate(brief: object, result: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(brief, dict) or not isinstance(result, dict):
        return ["brief and result must both be JSON objects"]

    mode = brief.get("mode", "standalone")
    if mode not in ("standalone", "video_first_frame"):
        errors.append("mode must be standalone or video_first_frame")

    expected_ratio = brief.get("aspect_ratio")
    if expected_ratio is not None and (
        not isinstance(expected_ratio, str) or not expected_ratio.strip()
    ):
        errors.append("aspect_ratio must be a non-empty string when supplied")

    positive = result.get("positive_prompt")
    if not isinstance(positive, str) or not positive.strip():
        errors.append("positive_prompt must be a non-empty string")
        positive = ""

    negative = result.get("negative_prompt")
    if not isinstance(negative, str):
        errors.append("negative_prompt must be a string")
        negative = ""

    if not isinstance(result.get("aspect_ratio"), str):
        errors.append("result.aspect_ratio must be a string")
    elif expected_ratio is not None and result["aspect_ratio"] != expected_ratio:
        errors.append("result.aspect_ratio differs from brief.aspect_ratio")

    first_frame_notes = result.get("first_frame_notes")
    if not isinstance(first_frame_notes, str):
        errors.append("first_frame_notes must be a string")
    elif mode == "video_first_frame" and not first_frame_notes.strip():
        errors.append("video_first_frame requires first_frame_notes")

    string_list(result.get("assumptions"), "assumptions", errors)
    required = string_list(brief.get("required_details", []), "required_details", errors)
    excluded = string_list(
        brief.get("exclude_from_positive", []), "exclude_from_positive", errors
    )

    positive_key = normalized(positive)
    negative_key = normalized(negative)
    for phrase in required:
        if normalized(phrase) not in positive_key:
            errors.append(f"required detail missing from positive_prompt: {phrase}")
    for phrase in excluded:
        key = normalized(phrase)
        if key in positive_key:
            errors.append(f"excluded detail appears in positive_prompt: {phrase}")
        if key not in negative_key:
            errors.append(f"excluded detail missing from negative_prompt: {phrase}")
    return errors


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: python3 scripts/check_output.py <brief.json> <result.json>", file=sys.stderr)
        return 2
    try:
        brief = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"cannot read input: {exc}", file=sys.stderr)
        return 2
    errors = validate(brief, result)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: explicit image prompt constraints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
