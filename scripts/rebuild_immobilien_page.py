"""Rebuild public/immobilien.html from existing is24-listings.json (no scrape)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_is24_listings import patch_immobilien_page  # noqa: E402

DATA = ROOT / "assets" / "oberholz" / "is24-listings.json"


def main() -> None:
    items = json.loads(DATA.read_text(encoding="utf-8"))
    for item in items:
        oid = item["id"]
        item.setdefault("thumb0", f"/media/object-thumbnail-780/{oid}_000.jpg")
        item.setdefault("thumb1", f"/media/object-thumbnail-780/{oid}_001.jpg")
        if not item.get("detail_href"):
            raise SystemExit(f"missing detail_href for {oid}")
    patch_immobilien_page(items)


if __name__ == "__main__":
    main()
