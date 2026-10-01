#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("index.html").read_text(encoding="utf-8")
out = Path("scripts/_contact_widget_snip.txt")

snippets = []
for kw in [
    "Kostenlose Erstberatung",
    "Lokale Ansicht",
    "cw_hint",
    "typeform-rating",
    "footer-contact-bar",
    "contact-fab",
    "erstberatung",
    "Termin buchen",
    "direkt anrufen",
]:
    i = t.lower().find(kw.lower())
    if i >= 0:
        snippets.append(f"\n===== {kw} @{i} =====\n{t[max(0,i-250):i+800]}\n")

# find floating widget markup patterns
for m in re.finditer(r".{0,80}Kostenlose Erstberatung.{0,1200}", t):
    snippets.append("\n===== BLOCK =====\n" + m.group(0) + "\n")
    break

out.write_text("\n".join(snippets), encoding="utf-8")
print("wrote", out, "chars", out.stat().st_size)

# list related scripts/css
for pat in ["contact", "hint", "fab", "sticky", "erstberatung", "calendy", "calendly"]:
    for p in Path("public/theme").rglob(f"*{pat}*"):
        print(p)
