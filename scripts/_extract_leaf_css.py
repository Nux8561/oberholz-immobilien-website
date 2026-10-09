# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = Path("index.html").read_text(encoding="utf-8", errors="ignore")
idx = t.find("leaf-watermark")
print("idx", idx)
print(t[max(0, idx - 200) : idx + 400])
print("---")
# all style blocks mentioning leaf
for m in re.finditer(r"<style[^>]*>(.*?)</style>", t, re.S):
    if "leaf-watermark" in m.group(1):
        print("STYLE LEN", len(m.group(1)))
        # print relevant part
        i = m.group(1).find("leaf-watermark")
        print(m.group(1)[max(0, i - 250) : i + 500])
