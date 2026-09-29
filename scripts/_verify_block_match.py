# -*- coding: utf-8 -*-
from pathlib import Path
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, "scripts")
import fix_standorte_safe as m

for root, dirs, files in os.walk("public/regionen"):
    for f in files:
        if not f.endswith(".html"):
            continue
        p = Path(root) / f
        raw = p.read_bytes()
        if b"immobilienmakler-hamburg.html" not in raw:
            continue
        t = raw.decode("utf-8", "ignore")
        print("file", p)
        print("has old desktop sp", m.OLD_DESKTOP_SP in t)
        print("has old mobile", m.OLD_MOBILE in t)
        print("expected head:", m.OLD_DESKTOP_SP[:90])
        i = t.find('href="/kontakt/immobilienmakler-hamburg.html"')
        start = t.rfind("<a ", max(0, i - 60), i + 1)
        print("actual head:", t[start : start + 90])
        # compare first 200 chars of constructed vs actual from start to muenchen end
        end = t.find("Immobilienmakler München</span></a>", start)
        if end > 0:
            end += len("Immobilienmakler München</span></a>")
            actual = t[start:end]
            print("actual len", len(actual), "expected len", len(m.OLD_DESKTOP_SP))
            if actual != m.OLD_DESKTOP_SP:
                for idx, (a, b) in enumerate(zip(actual, m.OLD_DESKTOP_SP)):
                    if a != b:
                        print("mismatch at", idx, repr(actual[max(0, idx - 20) : idx + 20]), "vs", repr(m.OLD_DESKTOP_SP[max(0, idx - 20) : idx + 20]))
                        break
                else:
                    print("prefix equal, length differs", len(actual), len(m.OLD_DESKTOP_SP))
            else:
                print("EXACT MATCH")
        new, n = m.patch_text(t)
        print("ops", n, "changed", new != t)
        raise SystemExit
print("no unpatched file found")
