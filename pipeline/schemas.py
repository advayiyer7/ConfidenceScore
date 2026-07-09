import json
import re
from dataclasses import dataclass

VALID = {"branded": "Branded", "unbranded": "Unbranded"}


class ParseError(ValueError):
    pass


@dataclass
class Cls:
    branding: str
    brandname: str
    reasoning: str

    def to_json(self) -> str:
        return json.dumps({"Branding": self.branding, "Brandname": self.brandname,
                           "Reasoning": self.reasoning}, ensure_ascii=False)


def parse_cls(text: str) -> Cls:
    t = (text or "").strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
        t = re.sub(r"```\s*$", "", t).strip()
    i, j = t.find("{"), t.rfind("}")
    if i < 0 or j <= i:
        raise ParseError(f"no JSON object in {t[:80]!r}")
    try:
        obj = json.loads(t[i:j + 1])
    except json.JSONDecodeError as exc:
        raise ParseError(str(exc)) from exc
    if not isinstance(obj, dict):
        raise ParseError("top-level value is not an object")
    for key in ("Branding", "Brandname", "Reasoning"):
        if key not in obj:
            raise ParseError(f"missing key {key}")
    branding = VALID.get(str(obj["Branding"]).strip().lower())
    if branding is None:
        raise ParseError(f"bad Branding value {obj['Branding']!r}")
    name = str(obj["Brandname"]).strip() or "NA"
    reasoning = str(obj["Reasoning"]).strip()
    if not reasoning:
        raise ParseError("empty Reasoning")
    return Cls(branding, name, reasoning)
