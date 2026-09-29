# -*- coding: utf-8 -*-
from pathlib import Path
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, "scripts")
import fix_standorte_safe as m

failed = [
    "public/regionen/spenge/immobilie-verkaufen.html",
    "public/regionen/steinfurt/immobilie-verkaufen.html",
    "public/regionen/steinkirchen/immobilie-verkaufen.html",
    "public/regionen/stockstadt-am-rhein/immobilienmakler.html",
    "public/regionen/stoedtlen/immobilienmakler.html",
]

for rel in failed:
    p = Path(rel)
    if not p.exists():
        print("missing", rel)
        continue
    for attempt in range(5):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
            new, ops = m.patch_text(t)
            if ops and new != t:
                p.write_text(new, encoding="utf-8")
                print("fixed", rel, "ops", ops)
            else:
                print("already ok", rel, "ops", ops, "hamburg", t.count("/kontakt/immobilienmakler-hamburg.html"))
            break
        except OSError as e:
            print("retry", rel, attempt, e)
            time.sleep(1.5)
    else:
        print("FAILED", rel)
