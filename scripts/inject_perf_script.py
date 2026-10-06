# -*- coding: utf-8 -*-
"""Inject oberholz-perf.js on pages that already load Oberholz theme helpers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
PERF = '<script src="/theme/oberholz-perf.js" defer></script>'
PERF_TAG = 'src="/theme/oberholz-perf.js"'
OVERRIDE = '<script src="/theme/oberholz-contact-override.js" defer></script>'


def main() -> None:
    changed = 0
    files = [ROOT / "index.html"] + list((ROOT / "public").rglob("*.html"))
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if PERF_TAG in text:
            continue
        if OVERRIDE in text:
            text = text.replace(OVERRIDE, OVERRIDE + "\n" + PERF, 1)
        elif "oberholz-contact-override.js" in text:
            lower = text.lower()
            idx = lower.rfind("</body>")
            if idx < 0:
                continue
            text = text[:idx] + PERF + "\n" + text[idx:]
        else:
            continue
        path.write_text(text, encoding="utf-8")
        changed += 1
    print("injected_perf_files", changed)


if __name__ == "__main__":
    main()
