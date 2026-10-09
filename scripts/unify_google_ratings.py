#!/usr/bin/env python3
"""Unify Google ratings from Essen + Münster into one sitewide score.

Sources (Google Maps, 2026-10-09):
- Essen, Benderstraße 2: 5.0 / 19 reviews
- Münster, Wichernstraße 29: 5.0 / 9 reviews
Combined: 5.0 / 28 reviews
"""

from __future__ import annotations

import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RATING = "5.0"
COUNT = "28"

REPLACEMENTS = [
    # HTML entity form used in many headers
    (
        "4.9/5&nbsp;Sehr&nbsp;gut",
        f"{RATING}/5&nbsp;Sehr&nbsp;gut",
    ),
    (
        "4.9/5\xa0Sehr\xa0gut",
        f"{RATING}/5\xa0Sehr\xa0gut",
    ),
    (
        "4.9/5 Sehr gut",
        f"{RATING}/5 Sehr gut",
    ),
    (
        '<span class="fw-bold">4.9</span><span class="opacity-75">/5</span>',
        f'<span class="fw-bold">{RATING}</span><span class="opacity-75">/5</span>',
    ),
    (
        'class="ratingValue d-inline">4.9</div>',
        f'class="ratingValue d-inline">{RATING}</div>',
    ),
    (
        '<strong class="d-inline me-3">5.0/5</strong> <span class="opacity-75">9 Bewertungen</span>',
        f'<strong class="d-inline me-3">{RATING}/5</strong> <span class="opacity-75">{COUNT} Bewertungen</span>',
    ),
    (
        '<strong class="d-inline me-3">4.9/5</strong> <span class="opacity-75">9 Bewertungen</span>',
        f'<strong class="d-inline me-3">{RATING}/5</strong> <span class="opacity-75">{COUNT} Bewertungen</span>',
    ),
    (
        '<strong class="d-inline me-3">5.0/5</strong> <span class="opacity-75">28 Bewertungen</span>',
        f'<strong class="d-inline me-3">{RATING}/5</strong> <span class="opacity-75">{COUNT} Bewertungen</span>',
    ),
    (
        '<strong>5.0/5</strong> <span class="opacity-75">9 Bewertungen</span>',
        f'<strong>{RATING}/5</strong> <span class="opacity-75">{COUNT} Bewertungen</span>',
    ),
    (
        '<strong>4.9/5</strong> <span class="opacity-75">9 Bewertungen</span>',
        f'<strong>{RATING}/5</strong> <span class="opacity-75">{COUNT} Bewertungen</span>',
    ),
    ("<span>9</span> Bewertungen", f"<span>{COUNT}</span> Bewertungen"),
    (">9 Bewertungen<", f">{COUNT} Bewertungen<"),
    (">9&nbsp;Bewertungen<", f">{COUNT}&nbsp;Bewertungen<"),
    ("9&nbsp;Bewertungen", f"{COUNT}&nbsp;Bewertungen"),
    ("9\xa0Bewertungen", f"{COUNT}\xa0Bewertungen"),
    ("9 Bewertungen", f"{COUNT} Bewertungen"),
    (
        '<span class="fs-3 fw-bold">4.9</span>',
        f'<span class="fs-3 fw-bold">{RATING}</span>',
    ),
    (
        '"ratingValue": 5.0, "reviewCount": 9',
        f'"ratingValue": {RATING}, "reviewCount": {COUNT}',
    ),
    (
        '"ratingValue": 4.9, "reviewCount": 9',
        f'"ratingValue": {RATING}, "reviewCount": {COUNT}',
    ),
    (
        '"ratingValue":"5.0","reviewCount":9',
        f'"ratingValue":"{RATING}","reviewCount":{COUNT}',
    ),
    (
        '"ratingValue":"4.9","reviewCount":9',
        f'"ratingValue":"{RATING}","reviewCount":{COUNT}',
    ),
    ('"reviewCount": 9', f'"reviewCount": {COUNT}'),
    ('"reviewCount":9', f'"reviewCount":{COUNT}'),
    ("Sehr gut4.9/5", f"Sehr gut{RATING}/5"),
    ("Sehr gut4.9/5", f"Sehr gut{RATING}/5"),
    (">4.9</span>", f">{RATING}</span>"),
    (">4.9</div>", f">{RATING}</div>"),
    (">4.9</strong>", f">{RATING}</strong>"),
    # catch remaining bare 4.9/5 in rating UI
    ("4.9/5", f"{RATING}/5"),
]


def main() -> None:
    started = time.time()
    changed = seen = 0
    paths = [ROOT / "index.html"]
    for dirpath, _d, files in os.walk(ROOT / "public"):
        for name in files:
            if name.lower().endswith(".html"):
                paths.append(Path(dirpath) / name)

    for path in paths:
        seen += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if (
            "4.9" not in text
            and "9 Bewertungen" not in text
            and "9&nbsp;Bewertungen" not in text
            and "9\xa0Bewertungen" not in text
        ):
            continue
        updated = text
        for old, new in REPLACEMENTS:
            if old in updated:
                updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
        if seen % 500 == 0:
            print(f"progress {seen} changed={changed}", flush=True)

    print(
        "DONE",
        {"seen": seen, "changed": changed},
        f"rating={RATING} count={COUNT}",
        f"elapsed={time.time()-started:.0f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
