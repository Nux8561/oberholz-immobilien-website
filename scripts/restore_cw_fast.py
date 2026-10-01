#!/usr/bin/env python3
"""Fast remaining contact-widget wiring – only files that still need it."""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STUB_RE = re.compile(
    r"Promise\.resolve\(\{\s*text:\s*function\s*\(\)\s*\{\s*return\s*Promise\.resolve\("
    r"(?:'[^']*'|\"[^\"]*\")"
    r"\)\s*;\s*\}\s*\}\)",
    re.S,
)
REX_FETCH_RE = re.compile(
    r"fetch\(['\"]/index\.php\?rex-api-call=contact_widget['\"]\s*,\s*\{\s*method:\s*'POST'\s*,\s*body:\s*formData\s*\}\)"
)
REAL_FETCH = "fetch('/theme/contact-widget.html')"
CSS = '<link rel="stylesheet" href="/theme/oberholz-contact-widget.css"/>'
JS = '<script src="/theme/oberholz-contact-override.js" defer></script>'


def needs_patch(text: str) -> bool:
    if "cwTriggerClick" not in text and "cw-trigger" not in text:
        return False
    if "contact-widget.html" in text and "Lokale Ansicht" not in text and "cw-local-overlay" not in text:
        # already on real widget – maybe still needs assets
        return ("oberholz-contact-widget.css" not in text) or ("oberholz-contact-override.js" not in text)
    return True


def process(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not needs_patch(text):
        return None
    orig = text
    text, _ = STUB_RE.subn(REAL_FETCH, text)
    text, _ = REX_FETCH_RE.subn(REAL_FETCH, text)
    if "cw-local-overlay" in text and "contact-widget.html" not in text:
        text = re.sub(
            r"Promise\.resolve\(\{[\s\S]{0,8000}?cw-local-(?:overlay|panel)[\s\S]{0,1200}?\}\)",
            REAL_FETCH,
            text,
            count=1,
        )
    if "Lokale Ansicht" in text and "contact-widget.html" not in text:
        text = re.sub(
            r"Promise\.resolve\(\{[\s\S]{0,4000}?Lokale Ansicht[\s\S]{0,800}?\}\)",
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
        return str(path.relative_to(ROOT))
    return None


def main() -> None:
    files = [ROOT / "index.html"]
    files.extend((ROOT / "public").rglob("*.html"))
    files = sorted({p for p in files if p.is_file()})
    print("candidates", len(files))
    changed = 0
    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = {pool.submit(process, p): p for p in files}
        for fut in as_completed(futs):
            rel = fut.result()
            if rel:
                changed += 1
                if changed % 200 == 0:
                    print("changed", changed, "last", rel)
    print("Done. changed=", changed)


if __name__ == "__main__":
    main()
