# -*- coding: utf-8 -*-
"""Debug first files that match needles but don't patch."""
from pathlib import Path
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, "scripts")
import fix_standorte_safe as m

NEEDLES = m.NEEDLES
checked = scanned = 0
for root, dirs, files in os.walk("public"):
    dirs[:] = [d for d in dirs if d not in m.SKIP_DIRS]
    for name in files:
        if not name.endswith(".html"):
            continue
        path = Path(root) / name
        checked += 1
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if not any(n in raw for n in NEEDLES):
            continue
        scanned += 1
        text = raw.decode("utf-8", errors="ignore")
        new, n = m.patch_text(text)
        which = [n.decode("utf-8", "ignore") for n in NEEDLES if n in raw]
        print(f"{path} ops={n} changed={new!=text} needles={which[:3]}")
        if scanned >= 20:
            raise SystemExit
print("done scanned", scanned)
