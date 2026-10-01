#!/usr/bin/env python3
from pathlib import Path
import re

html = Path("scripts/_cw_original_widget.html").read_text(encoding="utf-8")
print("len", len(html))

for kw in [
    "cwOpen",
    "cwClose",
    "anrufen",
    "rueckruf",
    "anfrage",
    "whatsapp",
    "kontakt",
    "pane",
    "btn-close",
    "modal",
    "facepile",
    "0800",
    "tel:",
    "mailto",
]:
    print(kw, html.lower().find(kw.lower()))

scripts = re.findall(r"<script[^>]*>([\s\S]*?)</script>", html)
print("scripts", len(scripts), "sizes", [len(s) for s in scripts])
Path("scripts/_cw_orig_head.txt").write_text(html[:5000], encoding="utf-8")

classes = sorted(set(re.findall(r'class="([^"]+)"', html)))
Path("scripts/_cw_orig_classes.txt").write_text("\n".join(classes), encoding="utf-8")
print("classes", len(classes))

ids = sorted(set(re.findall(r'id="([^"]+)"', html)))
print("ids", ids)

# Extract cwOpen/cwClose definitions
for i, s in enumerate(scripts):
    if "cwOpen" in s or "cwClose" in s:
        Path(f"scripts/_cw_orig_script_{i}.js").write_text(s, encoding="utf-8")
        print(f"wrote script {i} with cwOpen/Close, len={len(s)}")

# Find style blocks
styles = re.findall(r"<style[^>]*>([\s\S]*?)</style>", html)
print("styles", len(styles), "sizes", [len(s) for s in styles])
for i, s in enumerate(styles):
    Path(f"scripts/_cw_orig_style_{i}.css").write_text(s, encoding="utf-8")
