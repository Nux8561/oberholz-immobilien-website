from pathlib import Path
import re

# Shared phrase map for Oberholz SEO/GEO positioning
# Focus: Verkauf, Vermietung, Bewertung, Rueckmietverkauf | Muenster, Essen, Bochum

PHRASES = [
    ("EE-Experten GmbH", "Oberholz Immobilien"),
    ("EE-Experten", "Oberholz Immobilien"),
    ("die EE-Experten", "Oberholz Immobilien"),
    ("Die EE-Experten", "Oberholz Immobilien"),
    ("unserer EE-Experten", "unseres Teams"),
    ("Energieberatung der Oberholz Immobilien", "Leistungsübersicht von Oberholz Immobilien"),
    ("Energieberatung der EE-Experten", "Leistungsübersicht von Oberholz Immobilien"),
    ("zertifizierte Energieberater", "zertifizierte Immobiliengutachter"),
    ("zertifizierter Energieberater", "zertifizierter Immobiliengutachter"),
    ("zertifizierten Energieberater", "zertifizierten Immobiliengutachter"),
    ("als zertifizierte Energieberater", "als zertifizierte Immobiliengutachter"),
    ("Energieberater und Immobilienmakler", "Immobiliengutachter und Immobilienmakler"),
    ("Ihr Energieberater für Sanierung & Förderung", "Ihr Immobilienmakler für Münster, Essen & Bochum"),
    ("Ihr Energieberater für Sanierung &amp; Förderung", "Ihr Immobilienmakler für Münster, Essen &amp; Bochum"),
    ("BAFA-zertifizierte Energieberater | 🇩🇪 Förderexperten des Bundes", "DIN-zertifizierter Immobiliengutachter | Münster · Essen · Bochum"),
    ("BAFA-zertifizierte Energieberater", "DIN-zertifizierte Immobiliengutachter"),
    ("Förderexperten des Bundes", "Immobilienexperten vor Ort"),
    ("einzigartiger Energiekompetenz", "fundierter Markt- und Gutachterkompetenz"),
    ("einzigartige Energiekompetenz", "fundierte Markt- und Gutachterkompetenz"),
    ("energetischen Analyse", "marktgerechten Analyse"),
    ("energetische Einordnung", "marktgerechte Einordnung"),
    ("energetischen Fragen", "fachlichen Fragen zur Immobilie"),
    ("Zwei Kompetenzen, ein Team: Immobilienvermittlung und zertifizierte Energieberatung unter einem Dach",
     "Zwei Kompetenzen, ein Team: Immobilienvermittlung und zertifizierte Wertermittlung unter einem Dach"),
    ("Alle Unterlagen aus einer Hand: Energieausweis, Wohnflächenberechnung, Sanierungsfahrplan und Gutachten",
     "Alle Unterlagen aus einer Hand: Exposé, Marktwertermittlung, Verkaufsstrategie und Gutachten"),
    ("Bessere Argumente für Käufer und Banken: belastbare Energiewerte sichern Finanzierung und Verkaufspreis",
     "Bessere Argumente für Käufer und Banken: belastbare Marktwerte sichern Finanzierung und Verkaufspreis"),
    ("Ein konventioneller Makler inseriert und vermittelt. Wir beurteilen Ihre Immobilie zusätzlich als zertifizierte Energieberater, Gutachter und Planer: von der energetischen Analyse über Fördermöglichkeiten bis zur Vermarktung.",
     "Ein konventioneller Makler inseriert und vermittelt. Wir beurteilen Ihre Immobilie zusätzlich als zertifizierte Immobiliengutachter: von der Ortsbesichtigung über Boden-, Ertrags- und Sachwert bis zur Vermarktung."),
    ("Marktgerechte Einwertung plus energetische Einordnung durch zertifizierte Energieberater, die Basis für Preis und Strategie.",
     "Marktgerechte Einwertung durch unseren DIN-zertifizierten Immobiliengutachter – die Basis für Preis und Verkaufsstrategie."),
    ("Professionelle Fotografie, 3D-Visualisierung, Grundrisse, Wohnflächenberechnung und Energieausweis, alles aus einem Haus.",
     "Professionelles Exposé, aussagekräftige Unterlagen und eine klare Verkaufsstrategie – alles aus einer Hand."),
    ("Eigene Werbeagentur, große Portale und unser Käufernetzwerk. Bei Besichtigungen beantworten wir auch die energetischen Fragen der Interessenten.",
     "Führende Immobilienportale, Suchkunden und Partnernetzwerk. Bei Besichtigungen begleiten wir Sie mit fundierter Marktkenntnis."),
    ("Lernen Sie uns in Ruhe kennen: unser 360°-Immobilien-Service, unsere Energieberatung und unsere Leitfäden für Eigentümer und Erben.",
     "Lernen Sie uns in Ruhe kennen: Verkauf, Vermietung, Rückmietverkauf und Wertermittlung für Eigentümer in Münster, Essen und Bochum."),
    ("Die Oberholz Immobilien GmbH kooperiert mit Wüstenrot", "Oberholz Immobilien – Ihr Partner vor Ort"),
    ("Die EE-Experten GmbH kooperiert mit Wüstenrot", "Oberholz Immobilien – Ihr Partner vor Ort"),
    ("Oberholz Immobilien YouTube-Channel", "Oberholz Immobilien Kontakt"),
    ("EE-Experten YouTube-Channel", "Oberholz Immobilien Kontakt"),
    ("Beratung & Förderungen:", "Beratung & Verkauf:"),
    ("Beratung &amp; Förderungen:", "Beratung &amp; Verkauf:"),
    ("Ihr Partner für den erfolgreichen Immobilienverkauf",
     "Immobilienmakler Münster, Essen, Bochum | Oberholz Immobilien"),
    ("Unsere Leistungen – Alles aus einer Hand",
     "Leistungen: Verkauf, Vermietung, Bewertung | Oberholz Immobilien"),
    ("Unsere Leistungen &ndash; Alles aus einer Hand",
     "Leistungen: Verkauf, Vermietung, Bewertung | Oberholz Immobilien"),
]

PAGE_META = {
    "index.html": {
        "title": "Immobilienmakler Münster, Essen, Bochum | Oberholz Immobilien",
        "description": "Oberholz Immobilien: Verkauf, Vermietung, Rückmietverkauf und Marktwertermittlung durch zertifizierten Immobiliengutachter. Standorte in Münster, Essen und Bochum.",
    },
    "public/leistungen.html": {
        "title": "Leistungen: Verkauf, Vermietung, Bewertung | Oberholz Immobilien",
        "description": "Unsere Leistungen: Immobilienverkauf, Vermietung, Rückmietverkauf und Wertermittlung nach Boden-, Ertrags- und Sachwert. Persönlich in Münster, Essen und Bochum.",
    },
    "public/ueber-uns.html": {
        "title": "Über uns | Team & Immobiliengutachter Michael Oberholz",
        "description": "Lernen Sie Oberholz Immobilien kennen: Inhaber und DIN-zertifizierter Immobiliengutachter Michael Oberholz sowie das Team in Münster, Essen und Bochum.",
    },
    "public/kontakt/kontakt-aufnehmen.html": {
        "title": "Kontakt | Oberholz Immobilien Münster, Essen, Bochum",
        "description": "Kontakt zu Oberholz Immobilien: Tel. 0251 28 42 90 90, mail@oberholz-immobilien.com. Standorte in Münster, Essen und Bochum.",
    },
}


def set_title(html: str, title: str) -> str:
    return re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", html, count=1, flags=re.I)


def set_meta_description(html: str, description: str) -> str:
    pattern = re.compile(
        r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=["\'])([^"\']*)(["\'])',
        flags=re.I,
    )
    if pattern.search(html):
        return pattern.sub(rf"\g<1>{description}\g<3>", html, count=1)
    # alternate attribute order
    pattern2 = re.compile(
        r'(<meta\s+[^>]*content=["\'])([^"\']*)(["\'][^>]*name=["\']description["\'])',
        flags=re.I,
    )
    if pattern2.search(html):
        return pattern2.sub(rf"\g<1>{description}\g<3>", html, count=1)
    return html


def patch_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    stats = {"phrases": 0}

    # longer phrases first
    for old, new in sorted(PHRASES, key=lambda x: len(x[0]), reverse=True):
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            stats["phrases"] += n

    rel = path.as_posix()
    if path.name == "index.html" and path.parent.name != "public":
        key = "index.html"
    else:
        key = str(path).replace("\\", "/")
        if key.startswith("./"):
            key = key[2:]

    # normalize key
    for k in PAGE_META:
        if path.match(k) or path.as_posix().endswith(k):
            meta = PAGE_META[k]
            text = set_title(text, meta["title"])
            text = set_meta_description(text, meta["description"])
            stats["meta"] = k
            break

    if text != original:
        path.write_text(text, encoding="utf-8")
        stats["changed"] = True
    else:
        stats["changed"] = False
    return stats


def main() -> None:
    files = [
        Path("index.html"),
        Path("public/leistungen.html"),
        Path("public/ueber-uns.html"),
        Path("public/kontakt/kontakt-aufnehmen.html"),
        Path("public/service.html"),
        Path("public/ratgeber.html"),
        Path("public/impressum.html"),
        Path("public/immobilien.html"),
        Path("public/regionen.html"),
    ]
    for f in files:
        if not f.exists():
            print("missing", f)
            continue
        print(f, patch_file(f))


if __name__ == "__main__":
    main()
