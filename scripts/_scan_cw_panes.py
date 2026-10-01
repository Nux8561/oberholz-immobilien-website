#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("public/theme/contact-widget.html").read_text(encoding="utf-8")

# pane-kontakt and pane-support content (without style)
body = re.sub(r"<style[\s\S]*?</style>", "", t, count=1)
for sid in ["pane-kontakt", "pane-support", "pane-anrufen"]:
    m = re.search(rf'id="{sid}"[\s\S]{{0,4500}}', body)
    out = Path(f"scripts/_cw_{sid}.txt")
    out.write_text(m.group(0) if m else "NONE", encoding="utf-8")
    print(sid, "len", len(m.group(0)) if m else 0)

# all unique badge texts
texts = re.findall(r'class="cw-badge[^"]*"[^>]*>[\s\S]*?</span>', t)
for i, x in enumerate(texts):
    plain = re.sub(r"<[^>]+>", "", x)
    plain = re.sub(r"\s+", " ", plain).strip()
    print(i, plain[:120])
