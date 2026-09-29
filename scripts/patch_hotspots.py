"""Replace hotspot services in module-5192 with Oberholz Leistungen."""

from __future__ import annotations

from pathlib import Path

INDEX = Path("index.html")

PLUS_ICON = (
    '<svg fill="none" height="14" viewbox="0 0 14 14" width="14">'
    '<line stroke="currentColor" stroke-linecap="round" stroke-width="2" x1="7" x2="7" y1="1" y2="13"></line>'
    '<line stroke="currentColor" stroke-linecap="round" stroke-width="2" x1="1" x2="13" y1="7" y2="7"></line>'
    "</svg>"
)
CHEVRON = (
    '<svg fill="none" height="16" viewbox="0 0 16 16" width="16">'
    '<path d="M4 6l4 4 4-4" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"></path>'
    "</svg>"
)
CLOSE = (
    '<svg fill="none" height="16" viewbox="0 0 16 16" width="16">'
    '<line stroke="currentColor" stroke-linecap="round" stroke-width="2" x1="1" x2="15" y1="1" y2="15"></line>'
    '<line stroke="currentColor" stroke-linecap="round" stroke-width="2" x1="15" x2="1" y1="1" y2="15"></line>'
    "</svg>"
)

# Positions lined up with the Oberholz house: solar, ridge, right roof, heat pump, patio, sign.
SERVICES = (
    (
        "Verkauf",
        22,
        18,
        (
            "Professionelle Marktwertermittlung",
            "Hochwertiges Exposé",
            "Verkaufsstrategie",
            "Vermarktung auf führenden Immobilienplattformen",
        ),
    ),
    (
        "Immobilienbewertung",
        48,
        10,
        (
            "Ortsbesichtigung der Immobilie",
            "Dokumentation von Zustand &amp; Modernisierungen",
            "Realistische Marktwertermittlung",
            "Bewertung durch zertifizierten Immobiliengutachter",
        ),
    ),
    (
        "Vermietung",
        72,
        18,
        (
            "Mietpreisanalyse",
            "Optimale Präsentation auf Immobilienplattformen",
            "Auswahl geeigneter Mietbewerber",
            "Rechtssicherer Mietvertrag",
            "Begleitung der Wohnungsübergabe",
        ),
    ),
    (
        "Bewertungsverfahren",
        14,
        62,
        (
            "Bodenwert",
            "Ertragswert",
            "Sachwert",
        ),
    ),
    (
        "Rückmietverkauf",
        42,
        75,
        (
            "Verkauf zum Marktwert",
            "Weiter wohnen im eigenen Zuhause",
            "Sofortige Auszahlung des Kaufpreises",
            "Finanzielle Sicherheit &amp; Flexibilität",
        ),
    ),
    (
        "Betreuung &amp; Abwicklung",
        78,
        78,
        (
            "Verhandlung des optimalen Verkaufspreises",
            "Koordination mit Notaren &amp; Ämtern",
            "Transparente Beratung",
            "Begleitung bis zur Schlüsselübergabe",
        ),
    ),
)


def list_html(items: tuple[str, ...]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def hotspot_block(index: int, title: str, x: int, y: int, items: tuple[str, ...]) -> str:
    lists = list_html(items)
    return (
        f'<button aria-controls="sheet-hotspot-{index}" aria-expanded="false" '
        f'aria-label="{title}" class="hotspot" data-hotspot-id="hotspot-{index}" '
        f'style="--hs-x: {x}%; --hs-y: {y}%; top: {y}%; left: {x}%;" type="button"> '
        f'<span aria-hidden="true" class="hotspot-ring"></span> '
        f'<span aria-hidden="true" class="hotspot-inner"> {PLUS_ICON} </span> '
        f"</button> "
        f'<div class="hotspot-popover" data-for="hotspot-{index}" hidden="" '
        f'id="popover-hotspot-{index}" role="tooltip"> '
        f'<div class="hs-card__body"> <p class="hs-card__title">{title}</p> '
        f'<div class="hs-card__text">{lists}</div> </div> '
        f'<button aria-expanded="false" aria-label="Mehr anzeigen" class="hs-card__chevron" type="button"> '
        f"{CHEVRON} </button> </div> "
        f'<div aria-label="{title}" aria-modal="true" class="hotspot-sheet" '
        f'id="sheet-hotspot-{index}" role="dialog"> '
        f'<div class="hotspot-sheet__backdrop"></div> '
        f'<div class="hotspot-sheet__panel rounded-top-4"> '
        f'<button aria-label="Schließen" class="hotspot-sheet__close" type="button"> {CLOSE} </button> '
        f'<div class="hs-sheet-card"> <div class="hs-sheet-card__body"> '
        f'<p class="hs-sheet-card__title">{title}</p> '
        f'<div class="hs-sheet-card__text">{lists}</div> '
        f"</div> </div> </div> </div>"
    )


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    start_marker = '<div class="hotspot-image-wrap position-relative rounded-4">'
    end_marker = "</div> </div> </div> </div></section>"
    start = text.find(start_marker)
    if start < 0:
        raise SystemExit("hotspot wrap not found")
    # End of module-5192 section content after the wrap
    section_start = text.rfind('<section class="hotspots', 0, start)
    section_end = text.find("</section>", start)
    if section_end < 0:
        raise SystemExit("section end not found")

    img_and_svg_end = text.find("</svg>", start)
    if img_and_svg_end < 0:
        raise SystemExit("svg not found")
    img_and_svg_end += len("</svg>")

    # Keep wrap opener + image + svg, replace everything until close of wrap
    # Find closing of hotspot-image-wrap: after last sheet, before row/col closes
    wrap_close = text.find("</div> </div> </div> </div>", img_and_svg_end)
    # More reliable: find from svg end to the first sequence that closes image-wrap
    # Structure: wrap > img, svg, hotspots... then </div> (wrap) </div> (col) </div> (row) </div> (container)
    # Looking at original end: `</div> </div> </div> </div>` after last sheet
    tail_from_svg = text[img_and_svg_end:section_end]
    # Last hotspot sheet ends, then four closing divs
    close_idx = tail_from_svg.rfind("</div> </div> </div> </div>")
    if close_idx < 0:
        raise SystemExit("wrap close not found")
    absolute_close = img_and_svg_end + close_idx

    blocks = " ".join(
        hotspot_block(i, title, x, y, items)
        for i, (title, x, y, items) in enumerate(SERVICES)
    )
    new_text = (
        text[: img_and_svg_end]
        + " "
        + blocks
        + " "
        + text[absolute_close:]
    )
    INDEX.write_text(new_text, encoding="utf-8")
    verify = INDEX.read_text(encoding="utf-8")
    print("Verkauf", verify.count(">Verkauf<"))
    print("Rückmietverkauf", verify.count("Rückmietverkauf"))
    print("Gutachten left", verify.count("aria-label=\"Gutachten\""))
    print("hotspot buttons", verify.count('class="hotspot"'))


if __name__ == "__main__":
    main()
