# -*- coding: utf-8 -*-
"""Copy Oberholz brochure PNGs from Downloads as-is (true RemoveBG RGBA)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DOWNLOADS = Path(r"C:\Users\lsper\Downloads")
OUT_DIR = Path(__file__).resolve().parents[1] / "public" / "media" / "contentimg"
DIST_DIR = Path(__file__).resolve().parents[1] / "dist" / "media" / "contentimg"

MAP = {
    "360° Immobilien-Service Broschüre.png": "brochure_immobilienvermittlung.png",
    "Energiekosten sparen_ Immobilienbroschüre.png": "brochure_energieberatung.png",
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for src_name, dst_name in MAP.items():
        src = DOWNLOADS / src_name
        if not src.exists():
            print("MISSING", src, flush=True)
            continue
        data = src.read_bytes()
        (OUT_DIR / dst_name).write_bytes(data)
        print("copied as-is", src.name, "->", dst_name, len(data), "bytes", flush=True)
        if DIST_DIR.exists():
            (DIST_DIR / dst_name).write_bytes(data)


if __name__ == "__main__":
    main()
