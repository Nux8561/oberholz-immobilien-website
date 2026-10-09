# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = Path("index.html").read_text(encoding="utf-8", errors="ignore")
m = re.search(r"#navbarmain \.dropdown-menu \{[^}]+\}", t)
print(m.group(0) if m else "not found")
for p in [
    Path("public/media/oberholz-logo.png"),
    Path("public/media/oberholz-logo-header.png"),
]:
    print(p, p.exists(), p.stat().st_size if p.exists() else 0)
