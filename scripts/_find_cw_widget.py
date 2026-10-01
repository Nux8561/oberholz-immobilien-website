#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("index.html").read_text(encoding="utf-8")
# extract full contact widget script block
m = re.search(r"function cwTriggerClick[\s\S]{0,8000}?cwDismissHint[\s\S]{0,4000}", t)
Path("scripts/_cw_js.txt").write_text(m.group(0) if m else "NOT FOUND", encoding="utf-8")
print("js len", len(m.group(0)) if m else 0)

# find fetch URL for widget
for m in re.finditer(r".{0,80}cw-widget|/contact[^\"']*|cwOpen|pane.{0,40}", t):
    s = m.group(0)
    if "cw" in s.lower() or "contact" in s.lower():
        if "fetch" in s or "widget" in s or "cwOpen" in s:
            print(s[:200])

# search repo for contact widget html fragments
needles = ["cw-widget", "cwOpen", "Termin vereinbaren", "Direkt anrufen", "Lokale Ansicht"]
for root in [Path("."), Path("public"), Path("analysis"), Path("assets")]:
    if not root.exists():
        continue
    for p in root.rglob("*"):
        if p.suffix.lower() not in {".html", ".js", ".php", ".json", ".txt", ".md"}:
            continue
        if any(x in p.parts for x in ("node_modules", "dist", "dist-regionen", "regionen", "immopedia")):
            continue
        try:
            data = p.read_bytes()
        except Exception:
            continue
        if b"Lokale Ansicht" in data or b"cw-widget-wrapper" in data or b"Direkt anrufen" in data:
            print("HIT", p)
