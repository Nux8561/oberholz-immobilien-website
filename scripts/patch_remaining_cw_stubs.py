#!/usr/bin/env python3
"""Patch only HTML files that still contain the local contact stub."""

from __future__ import annotations

import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REAL_FETCH = "fetch('/theme/contact-widget.html')"
CSS = '<link rel="stylesheet" href="/theme/oberholz-contact-widget.css"/>'
JS = '<script src="/theme/oberholz-contact-override.js" defer></script>'

STUB_RE = re.compile(
    r"Promise\.resolve\(\{\s*text:\s*function\s*\(\)\s*\{\s*return\s*Promise\.resolve\("
    r"(?:'[^']*'|\"[^\"]*\")"
    r"\)\s*;\s*\}\s*\}\)",
    re.S,
)


def list_stub_files() -> list[Path]:
    out = subprocess.check_output(
        ["git", "grep", "-l", "-E", "Lokale Ansicht|cw-local-overlay", "--", "*.html"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return [ROOT / line.strip() for line in out.splitlines() if line.strip()]


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    orig = text
    text, n = STUB_RE.subn(REAL_FETCH, text)
    if n == 0 and ("Lokale Ansicht" in text or "cw-local-overlay" in text):
        text = re.sub(
            r"Promise\.resolve\(\{[\s\S]{0,12000}?(?:Lokale Ansicht|cw-local-(?:overlay|panel))[\s\S]{0,2000}?\}\)",
            REAL_FETCH,
            text,
            count=1,
        )
    if "oberholz-contact-widget.css" not in text and "</head>" in text:
        text = text.replace("</head>", CSS + "\n</head>", 1)
    if "oberholz-contact-override.js" not in text and "</body>" in text:
        text = text.replace("</body>", JS + "\n</body>", 1)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    files = list_stub_files()
    print("stub files", len(files), flush=True)
    changed = 0
    with ThreadPoolExecutor(max_workers=16) as pool:
        futs = [pool.submit(process, p) for p in files]
        for i, fut in enumerate(as_completed(futs), 1):
            if fut.result():
                changed += 1
            if i % 250 == 0:
                print(f"progress {i}/{len(files)} changed={changed}", flush=True)
    print("Done changed=", changed, flush=True)


if __name__ == "__main__":
    main()
