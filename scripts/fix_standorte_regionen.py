# -*- coding: utf-8 -*-
"""Nur public/regionen patchen – dort liegen die meisten Alt-Navs."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import fix_standorte_safe as m  # noqa: E402

NEEDLE = b"/kontakt/immobilienmakler-hamburg.html"


def main() -> None:
    start = time.time()
    base = ROOT / "public" / "regionen"
    checked = scanned = changed = errors = ops_total = 0
    print("patching", base, flush=True)

    for root, dirs, files in os.walk(base):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = Path(root) / name
            checked += 1
            try:
                raw = path.read_bytes()
            except OSError:
                errors += 1
                continue
            if NEEDLE not in raw and b"Immobilienmakler Stuttgart" not in raw:
                if checked % 2000 == 0:
                    print(
                        f"... checked {checked} changed {changed} ({time.time()-start:.0f}s)",
                        flush=True,
                    )
                continue
            scanned += 1
            text = raw.decode("utf-8", errors="ignore")
            new_text, ops = m.patch_text(text)
            if ops and new_text != text:
                try:
                    path.write_text(new_text, encoding="utf-8")
                    changed += 1
                    ops_total += ops
                except OSError as e:
                    errors += 1
                    if errors <= 5:
                        print("write err", path, e, flush=True)
            if changed % 200 == 0 and ops:
                print(
                    f"... checked {checked} scanned {scanned} changed {changed} ops {ops_total} ({time.time()-start:.0f}s)",
                    flush=True,
                )

    print(
        "DONE checked",
        checked,
        "scanned",
        scanned,
        "changed",
        changed,
        "ops",
        ops_total,
        "errors",
        errors,
        f"elapsed {time.time()-start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
