#!/usr/bin/env python3
from pathlib import Path

t = Path("index.html").read_text(encoding="utf-8")
checks = {
    "css": "oberholz-contact-widget.css" in t,
    "lokale_gone": "Lokale Ansicht" not in t,
    "panel": "cw-local-overlay" in t,
    "anrufen": "Anrufen" in t and "cw-local-actions" in t,
    "mail": "E-Mail schreiben" in t,
    "termin": "Termin / Kontaktformular" in t,
    "cwClose": "window.cwClose" in t,
    "hint_not_preopen": 'class="show" id="cw-trigger-hint"' not in t,
}
for k, v in checks.items():
    print(k, v)
i = t.find("cw-local-overlay")
print(t[i : i + 320])
