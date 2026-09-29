"""Inject oberholz-nav-fix.css into all HTML pages."""

from __future__ import annotations

import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = '<link href="/theme/oberholz-nav-fix.css" rel="stylesheet"/>'
NEEDLE = "oberholz-nav-fix.css"


def iter_html():
    index = ROOT / "index.html"
    if index.is_file():
        yield index
    for dirpath, _d, files in os.walk(ROOT / "public"):
        for name in files:
            if name.lower().endswith(".html"):
                yield Path(dirpath) / name


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if NEEDLE in text:
        return False
    lower = text.lower()
    idx = lower.find("</head>")
    if idx < 0:
        return False
    # preserve original casing of </head>
    end = text[idx : idx + 7]
    updated = text[:idx] + LINK + end + text[idx + 7 :]
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    started = time.time()
    seen = changed = skipped = 0
    for path in iter_html():
        seen += 1
        try:
            if patch(path):
                changed += 1
            else:
                skipped += 1
        except OSError as exc:
            print("fail", path, exc, flush=True)
        if seen % 2000 == 0:
            print(
                f"progress {seen} changed={changed} skipped={skipped} "
                f"elapsed={time.time()-started:.0f}s",
                flush=True,
            )
    print(
        "DONE",
        {"seen": seen, "changed": changed, "skipped": skipped},
        f"elapsed={time.time()-started:.0f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
