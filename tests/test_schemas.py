import pytest

from pipeline.schemas import Cls, ParseError, parse_cls

GOOD = '{"Branding": "Branded", "Brandname": "Maggi (Nestle)", "Reasoning": "FACT: owned by Nestle."}'


def test_plain_json():
    c = parse_cls(GOOD)
    assert c == Cls("Branded", "Maggi (Nestle)", "FACT: owned by Nestle.")


def test_markdown_fenced():
    c = parse_cls(f"```json\n{GOOD}\n```")
    assert c.branding == "Branded"


def test_fence_without_lang_tag():
    c = parse_cls(f"```\n{GOOD}\n```")
    assert c.brandname == "Maggi (Nestle)"


def test_preamble_before_object():
    c = parse_cls(f"Here is the JSON:\n{GOOD}")
    assert c.branding == "Branded"


def test_case_insensitive_branding_normalized():
    c = parse_cls('{"Branding": "UNBRANDED", "Brandname": "NA", "Reasoning": "x"}')
    assert c.branding == "Unbranded"


def test_empty_brandname_becomes_na():
    c = parse_cls('{"Branding": "Unbranded", "Brandname": "", "Reasoning": "x"}')
    assert c.brandname == "NA"


@pytest.mark.parametrize("bad", [
    "",
    "not json at all",
    '{"Branding": "Branded", "Brandname": "X"}',            # missing Reasoning
    '{"Branding": "Maybe", "Brandname": "X", "Reasoning": "y"}',
    '{"Branding": "Branded", "Brandname": "X", "Reasoning": ""}',
    '{"Branding": "Branded", "Brandname": "X", "Reasoning": "y"',  # truncated
    '["Branded", "X", "y"]',
])
def test_malformed_raises(bad):
    with pytest.raises(ParseError):
        parse_cls(bad)
