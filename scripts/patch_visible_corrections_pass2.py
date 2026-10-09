#!/usr/bin/env python3
"""Second pass: homepage hero/gutachten claims + leistungen overview cleanup."""

from __future__ import annotations

import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    (
        "Wertermittlung durch DIN-zertifizierten Immobiliengutachter",
        "Marktgerechte Preiseinschätzung vor Ort",
    ),
    (
        "Marktgerechte Einwertung durch unseren DIN-zertifizierten Immobiliengutachter – die Basis für Preis und Verkaufsstrategie.",
        "Eine klare Preiseinschätzung als Basis für Ihre Verkaufsstrategie in Essen und Umgebung.",
    ),
    (
        "Als Makler mit integrierter Gutachterkompetenz bewerten wir Ihre Immobilie nachvollziehbar",
        "Als Maklerteam bewerten wir Ihre Immobilie nachvollziehbar",
    ),
    (
        "unser Hybrid-Service aus Immobilienvermittlung und Energieberatung",
        "unser Service aus Immobilienvermittlung und persönlicher Begleitung",
    ),
    (
        "Welche Vorteile habe ich als Verkäufer durch Ihre Gutachterkompetenz?",
        "Welche Vorteile habe ich als Verkäufer mit Oberholz Immobilien?",
    ),
    (
        "Immobilienvermittlung mit Gutachterkompetenzgie-Kompetenz",
        "Immobilienvermittlung mit lokaler Marktkenntnis",
    ),
    (
        "Immobilienvermittlung mit Gutachterkompetenz",
        "Immobilienvermittlung mit lokaler Marktkenntnis",
    ),
    (
        "Die <strong>Oberholz Immobilien</strong> vereinen Immobilienvermittlung, Energieberatung und Marketingkompetenz unter einem Dach. Von der <em>Immobilienbewertung</em>",
        "Die <strong>Oberholz Immobilien</strong> stehen für persönliche Immobilienvermittlung in Essen und Umgebung. Von der <em>Preiseinschätzung</em>",
    ),
    (
        "verbinden Immobilienvermittlung mit einzigartiger Energieberatung für höhere Rendite & sichere Verträge.",
        "begleiten Vermietung und Verkauf persönlich – für passende Mieter und sichere Verträge in Essen und Umgebung.",
    ),
    (
        "in Bochum und Umgebung, professionell & energiekompetent. Durch Banken-Netzwerk, geprüfte Unterlagen & Energieberatung erzielen Sie Top-Preise und schnelle Abschlüsse.",
        "in Essen und Umgebung, professionell und persönlich. Mit geprüften Unterlagen und starker Vermarktung erzielen Sie Top-Preise und schnelle Abschlüsse.",
    ),
    (
        "in Bochum und Umgebung, schnell & sicher. Mit Energieberatung, geprüften Unterlagen & Banken-Netzwerk sorgen wir für Top-Konditionen & verlässliche Abwicklung.",
        "in Essen und Umgebung, schnell und sicher. Mit geprüften Unterlagen und Banken-Netzwerk sorgen wir für Top-Konditionen und verlässliche Abwicklung.",
    ),
    (
        "professionell & energiekompetent",
        "professionell und persönlich",
    ),
    (
        "DIN-zertifizierten Immobiliengutachter",
        "erfahrenen Maklerteam",
    ),
    (
        "zertifizierten Immobiliengutachter",
        "erfahrenen Maklerteam",
    ),
]

FOOTER_ENERGY_NEW = (
    "Die <strong>Oberholz Immobilien</strong> stehen für persönliche Immobilienvermittlung "
    "in Essen und Umgebung. Wir begleiten Verkauf und Vermietung transparent – von der "
    "ersten Einschätzung bis zum erfolgreichen Vertragsabschluss."
)

FOOTER_ENERGY_PREFIX = (
    "Die <strong>Oberholz Immobilien</strong> vereinen Immobilienvermittlung, "
    "Energieberatung und Marketingkompetenz unter einem Dach."
)


def remove_leistungen_energy_card(html: str) -> str:
    """Remove the energyberatung service card without catastrophic backtracking."""
    marker = "Energieberatung mit den Oberholz Immobilien"
    idx = html.find(marker)
    if idx < 0:
        return html
    # Walk back to the nearest opening col/card wrapper
    start = html.rfind('<div class="col', 0, idx)
    if start < 0:
        start = html.rfind("<div class=\"card", 0, idx)
    if start < 0:
        return html
    # Walk forward counting div depth from start
    i = start
    depth = 0
    while i < len(html):
        if html.startswith("<div", i):
            depth += 1
            i = html.find(">", i) + 1
            continue
        if html.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                return html[:start] + html[i:]
            continue
        i += 1
    return html


def patch_core(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="ignore")
    if "Diese Leistung bieten wir nicht an" in original:
        return False
    html = original
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)
    if path.name == "leistungen.html":
        html = remove_leistungen_energy_card(html)
        # Also drop immobilienbewertung card if still present by title marker
        for marker in (
            "Immobilienbewertung durch DIN",
            "href=\"/leistungen/immobilienbewertung.html\"",
            "href=\"/leistungen/energieausweis-kostenlos.html\"",
        ):
            # replace leftover hrefs only; cards already mostly stripped in pass1
            html = html.replace(marker, 'href="/leistungen.html"')
    if html == original:
        return False
    path.write_text(html, encoding="utf-8")
    return True


def patch_global_footers() -> int:
    started = time.time()
    changed = 0
    seen = 0
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
        if "Diese Leistung bieten wir nicht an" in text:
            continue
        if FOOTER_ENERGY_PREFIX not in text and "Energiekompetenz" not in text:
            continue
        updated = text
        if FOOTER_ENERGY_PREFIX in updated:
            # Replace from prefix through end of that sentence/paragraph chunk
            # Find prefix and cut until next closing p or next tag boundary of 400 chars
            pos = updated.find(FOOTER_ENERGY_PREFIX)
            while pos >= 0:
                end = updated.find("</p>", pos)
                if end < 0 or end - pos > 600:
                    end = pos + len(FOOTER_ENERGY_PREFIX)
                    updated = updated[:pos] + FOOTER_ENERGY_NEW + updated[end:]
                else:
                    updated = updated[:pos] + FOOTER_ENERGY_NEW + updated[end:]
                pos = updated.find(FOOTER_ENERGY_PREFIX)
        updated = updated.replace(
            "einzigartiger Energiekompetenz",
            "lokaler Marktkenntnis",
        )
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
        if seen % 2000 == 0:
            print(
                f"footer progress {seen} changed={changed} "
                f"elapsed={time.time()-started:.0f}s",
                flush=True,
            )
    return changed


def main() -> None:
    targets = [
        ROOT / "index.html",
        ROOT / "public" / "leistungen.html",
        ROOT / "public" / "ueber-uns.html",
        ROOT / "public" / "kontakt.html",
    ]
    leist = ROOT / "public" / "leistungen"
    if leist.is_dir():
        targets.extend(sorted(leist.glob("*.html")))

    changed = 0
    for path in targets:
        if path.is_file() and patch_core(path):
            changed += 1
            print("changed", path, flush=True)
    footer_changed = patch_global_footers()
    print("DONE core_changed=", changed, "footer_changed=", footer_changed, flush=True)


if __name__ == "__main__":
    main()
