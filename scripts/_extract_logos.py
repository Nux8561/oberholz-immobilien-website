#!/usr/bin/env python3
from pathlib import Path
import re

for name in ["_swiss.html", "_interhyp.html", "_dvag.html"]:
    p = Path("public/media") / name
    t = p.read_text(encoding="utf-8", errors="replace")
    print("====", name, "len", len(t))
    logos = set()
    for m in re.finditer(
        r"""["']([^"']*(?:logo|Logo|brand)[^"']*\.(?:svg|png|jpg|webp))["']""",
        t,
        re.I,
    ):
        logos.add(m.group(1))
    # also any /assets/ path with svg
    for m in re.finditer(r"""["']([^"']+\.svg)["']""", t, re.I):
        if "logo" in m.group(1).lower() or "brand" in m.group(1).lower():
            logos.add(m.group(1))
    for u in sorted(logos)[:50]:
        print(u)

# inspect downloaded svgs
for p in [
    Path("public/media/dvag-logo.svg"),
    Path("public/media/dvag-dewiki.svg"),
    Path("public/media/swiss-life-logo.svg"),
]:
    data = p.read_text(encoding="utf-8", errors="replace")[:200]
    print("---", p.name, "---")
    print(data)
