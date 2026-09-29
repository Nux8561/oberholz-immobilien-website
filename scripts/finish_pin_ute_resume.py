"""Resume PIN/Ute cleanup from city index offset (previous abort ~4000)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = 4000  # resume after abort

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
    regionen = ROOT / "public" / "regionen"
    cities = sorted(d for d in regionen.iterdir() if d.is_dir())
    subset = cities[START:]
    print(f"resume from {START}, remaining cities {len(subset)}", flush=True)
    changed = pins = 0
    for i, city in enumerate(subset, 1):
        for path in city.rglob("*.html"):
            c, p = patch_file(path)
            changed += c
            pins += p
        if i % 300 == 0:
            print(
                f"progress {START + i}/{len(cities)} changed {changed} pins {pins}",
                flush=True,
            )
    print("done changed", changed, "pins", pins, flush=True)


if __name__ == "__main__":
    main()
