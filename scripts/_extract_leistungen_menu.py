#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path("index.html").read_text(encoding="utf-8")
i = t.find("Vermietung und Verpachtung")
print("idx", i)
# walk back to dropdown-menu
start = t.rfind('class="dropdown-menu', 0, i)
# find matching end roughly
end = t.find("</div></li>", i)
chunk = t[start : start + 4500]
print(chunk)
print("---IMGS---")
for m in re.finditer(r"<img[^>]+>", chunk):
    print(m.group(0)[:300])
print("---EMPTY COLS---")
for m in re.finditer(r'<div class="col-12 col-md-6"[^>]*>[\s\S]*?</div>', chunk):
    print(repr(m.group(0)[:400]))
