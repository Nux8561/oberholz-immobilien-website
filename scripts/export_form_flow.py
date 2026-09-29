"""Document the public multi-step form from rendered markup. No submission."""
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
soup = BeautifulSoup((ROOT / "index.html").read_text(encoding="utf-8"), "lxml")
steps = []
for section in soup.select("#iwf .iwf-step"):
    options = []
    for button in section.select(".iwf-choice, .iwf-quick__chip"):
        options.append(
            {
                "label": button.get_text(" ", strip=True),
                "value": button.get("data-value") or button.get("data-val"),
                "next": button.get("data-next"),
                "field": button.get("data-field"),
            }
        )
    for box in section.select("input[type='checkbox']"):
        label = box.find_parent("label")
        options.append(
            {
                "label": label.get_text(" ", strip=True) if label else box.get("name"),
                "value": box.get("value"),
                "type": "checkbox",
            }
        )
    weiter = section.select_one(".iwf-weiter, .iwf-weiter-plain, button[type='submit']")
    steps.append(
        {
            "state": section.get("data-step") or "kontakt",
            "question": (section.select_one(".iwf-q").get_text(" ", strip=True) if section.select_one(".iwf-q") else ""),
            "hint": (section.select_one(".iwf-sub").get_text(" ", strip=True) if section.select_one(".iwf-sub") else ""),
            "options": options,
            "next_control": weiter.get_text(" ", strip=True) if weiter else None,
            "next_state": weiter.get("data-next") if weiter else None,
            "back_state": "history",
            "validation": "required value or selection before continue; contact requires name, place, phone, email and privacy checkbox",
        }
    )

flow = {
    "start": "art",
    "submit": "local only, preventDefault, no request to immobilien-experten.de",
    "paths": {
        "Wohnhaus": ["art", "wohnart", "wohnungen", "grundstueck", "absicht", "kontakt"],
        "Wohnung": ["art", "flaeche", "absicht", "kontakt"],
        "Gewerbe": ["art", "gewerbeart", "flaeche", "absicht", "kontakt"],
        "Grundstueck": ["art", "grundstueck", "absicht", "kontakt"],
        "Sonstiges": ["art", "absicht", "kontakt"],
    },
    "steps": steps,
}
(ROOT / "analysis" / "form-flow.json").write_text(json.dumps(flow, ensure_ascii=False, indent=2), encoding="utf-8")
print("steps", len(steps))
