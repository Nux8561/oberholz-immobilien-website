#!/usr/bin/env python3
"""Ensure contact widget CSS/JS links on pages that already have the fetch wiring."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = '<link rel="stylesheet" href="/theme/oberholz-contact-widget.css"/>'
JS = '<script src="/theme/oberholz-contact-override.js" defer></script>'


def main() -> None:
    changed = 0
    # Core pages only (fast) – regionen bulk already long-running
    files = [ROOT / "index.html"]
    for folder in [
        ROOT / "public",
        ROOT / "public" / "leistungen",
        ROOT / "public" / "ueber-uns",
        ROOT / "public" / "service",
        ROOT / "public" / "ratgeber",
        ROOT / "public" / "kontakt",
    ]:
        if folder.is_dir():
            files.extend(folder.glob("*.html"))

    for path in sorted(set(files)):
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        if "cwTriggerClick" not in html and "contact-widget.html" not in html:
            continue
        orig = html
        if "oberholz-contact-widget.css" not in html and "</head>" in html:
            html = html.replace("</head>", CSS + "\n</head>", 1)
        if "oberholz-contact-override.js" not in html and "</body>" in html:
            html = html.replace("</body>", JS + "\n</body>", 1)
        if html != orig:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("assets", path.relative_to(ROOT))
    print("changed", changed)


if __name__ == "__main__":
    main()
