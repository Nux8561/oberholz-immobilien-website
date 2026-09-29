"""Finish Service-PIN + Ute removal on regionen (byte-filter, city batches)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PIN_RE = re.compile(
    r'\s*<div class="text-center d-block">\s*'
    r'<span class="text-muted">Service-PIN:\s*'
    r'<strong class="text-md"[^>]*>[^<]*</strong>\s*'
    r"</span>\s*</div>",
    re.I,
)
SPAN_RE = re.compile(
    r'<span class="text-muted">\s*Service-PIN:\s*'
    r'<strong class="text-md"[^>]*>[^<]*</strong>\s*</span>',
    re.I,
)


def patch_text(text: str) -> tuple[str, int]:
    pins = 0
    text, n = PIN_RE.subn("", text)
    pins += n
    if "Service-PIN" in text:
        text, n = SPAN_RE.subn("", text)
        pins += n
    if "Ute Schorpp" in text:
        text = text.replace("Ute Schorpp", "Lubka Röger")
        text = text.replace("Teamleiterin Kundenberatung", "Immobilienberaterin")
    if "team_schorpp.jpg" in text:
        text = text.replace(
            "/media/team/team_schorpp.jpg",
            "/media/team/lubka-roeger.jpg",
        )
        text = text.replace(
            r"\/media\/team\/team_schorpp.jpg",
            r"\/media\/team\/lubka-roeger.jpg",
        )
    return text, pins


def patch_file(path: Path) -> tuple[int, int]:
    try:
        raw = path.read_bytes()
    except OSError:
        return 0, 0
    if b"Service-PIN" not in raw and b"Ute Schorpp" not in raw and b"team_schorpp" not in raw:
        return 0, 0
    text = raw.decode("utf-8", errors="replace")
    new_text, pins = patch_text(text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return 1, pins
    return 0, pins


def main() -> None:
    changed = pins = 0
    regionen = ROOT / "public" / "regionen"
    cities = sorted(d for d in regionen.iterdir() if d.is_dir()) if regionen.exists() else []
    print("cities", len(cities), flush=True)
    for i, city in enumerate(cities, 1):
        for path in city.rglob("*.html"):
            c, p = patch_file(path)
            changed += c
            pins += p
        if i % 400 == 0:
            print(f"cities {i}/{len(cities)} changed {changed} pins {pins}", flush=True)

    for path in (ROOT / "public").glob("*.html"):
        c, p = patch_file(path)
        changed += c
        pins += p
    for path in [ROOT / "index.html"]:
        if path.exists():
            c, p = patch_file(path)
            changed += c
            pins += p

    print("done changed", changed, "pins", pins, flush=True)

    # spot check
    sample = ROOT / "public/regionen/felde/immobilienmakler.html"
    if sample.exists():
        t = sample.read_text(encoding="utf-8", errors="replace")
        print("felde PIN", "Service-PIN" in t, "Ute", "Ute Schorpp" in t, flush=True)


if __name__ == "__main__":
    main()
