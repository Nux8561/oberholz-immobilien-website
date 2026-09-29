"""Second pass: fix leftover reviewCount/nbsp 3106 patterns sitewide."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"node_modules", "dist", ".git", "analysis", "reference", "screenshots", "theme", "assets", "scripts", "src"}


def main() -> None:
    sys.stdout.reconfigure(line_buffering=True)
    changed = 0
    scanned = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        rel = Path(dirpath).relative_to(ROOT).parts
        if len(rel) >= 2 and rel[0] == "public" and rel[1] == "theme":
            dirnames[:] = []
            continue
        for name in filenames:
            if not name.endswith(".html"):
                continue
            path = Path(dirpath) / name
            scanned += 1
            if scanned % 2000 == 0:
                print(f"progress {scanned} changed={changed}", flush=True)
            raw = path.read_bytes()
            if b"3106" not in raw and b"3.106" not in raw:
                continue
            html = raw.decode("utf-8", errors="replace")
            new = html
            new = new.replace('"reviewCount": 3106', '"reviewCount": 9')
            new = new.replace('"reviewCount":"3106"', '"reviewCount":"9"')
            new = new.replace('"reviewCount": "3106"', '"reviewCount": "9"')
            new = new.replace("3106\u00a0Bewertungen", "9&nbsp;Bewertungen")
            new = new.replace("3.106\u00a0Bewertungen", "9&nbsp;Bewertungen")
            new = new.replace("3106&nbsp;Bewertungen", "9&nbsp;Bewertungen")
            new = new.replace("3.106&nbsp;Bewertungen", "9&nbsp;Bewertungen")
            new = new.replace(">3106</span> Bewertungen", ">9</span> Bewertungen")
            new = new.replace("<strong>3106</strong>", "<strong>9</strong>")
            new = new.replace("<strong>3.106</strong>", "<strong>9</strong>")
            if new != html:
                path.write_text(new, encoding="utf-8", newline="")
                changed += 1
    print(f"DONE scanned={scanned} changed={changed}", flush=True)


if __name__ == "__main__":
    main()
