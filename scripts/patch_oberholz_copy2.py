from pathlib import Path
import re

EXTRA = [
    (
        "BAFA-zertifizierte Energieeffizienz-Experten ✓ Individuelle Sanierungsfahrpläne ✓ Maximale Förderung sichern.",
        "DIN-zertifizierter Immobiliengutachter ✓ Verkauf, Vermietung und Wertermittlung ✓ Standorte Münster, Essen, Bochum.",
    ),
    (
        "Regionale Energieberatung: Oberholz Immobilien",
        "Immobilienmakler vor Ort: Oberholz Immobilien",
    ),
    (
        "Energieausweis kostenlos",
        "Marktwertermittlung",
    ),
    (
        "Bei Beauftragung inklusive: Energieausweis vom zertifizierten Energieeffizienz-Experten",
        "Bei Beauftragung: Marktwertermittlung durch zertifizierten Immobiliengutachter",
    ),
    (
        "Bei Beauftragung inklusive: Energieausweis vom zertifizierten Energieeffizienz-Experten ist kostenlos enthalten, inklusive Optimierungs-Check.",
        "Bei Beauftragung erhalten Sie eine marktgerechte Wertermittlung durch unseren DIN-zertifizierten Immobiliengutachter.",
    ),
    (
        "Verkaufen oder vermieten Sie mit uns: Der Energieausweis vom zertifizierten Energieeffizienz-Experten ist kostenlos enthalten, inklusive Optimierungs-Check.",
        "Verkaufen oder vermieten Sie mit uns: Wir ermitteln den Marktwert persönlich und begleiten Sie bis zur Schlüsselübergabe.",
    ),
    (
        "Energieausweis, Förderung und Sanierungsfahrplan",
        "Wertermittlung, Exposé und Verkaufsstrategie",
    ),
    (
        "Energieausweis, Förderung und Sanierungsfahrplan",
        "Wertermittlung, Exposé und Verkaufsstrategie",
    ),
    (
        "🥇 Deutschlandweit einmalig: 360° Immobilien-Service",
        "Ihr Partner vor Ort: Oberholz Immobilien",
    ),
    (
        "360° Immobilien-Service: alle Leistungen rund um Ihre Immobilie",
        "Verkauf, Vermietung und Bewertung rund um Ihre Immobilie",
    ),
    (
        "360° Immobilien-Service",
        "Oberholz Immobilien Service",
    ),
    (
        "Immobilienvermittlung mit Energiekompetenz",
        "Immobilienvermittlung mit Gutachterkompetenz",
    ),
    (
        "Immobilienvermittlung mit Ener",
        "Immobilienvermittlung mit Gutachterkompetenz",
    ),
    (
        "zertifizierte Energieeffizienz-Experten und Immobiliengutachter",
        "zertifizierte Immobiliengutachter und erfahrene Immobilienmakler",
    ),
    (
        "Wir erstellen Sanierungskonzepte, identifizieren Fördermöglichkeiten, berechnen Finanzierungen über unser Bankennetzwerk",
        "Wir erstellen Wertgutachten, entwickeln Verkaufsstrategien und begleiten Verhandlungen bis zum Notartermin",
    ),
    (
        "Alles aus einer Hand: Energieausweise, Grundrisse, Wohnflächenberechnungen, Sanierungsfahrpläne",
        "Alles aus einer Hand: Exposés, Marktanalysen, Wertermittlungen und Verkaufsunterlagen",
    ),
    (
        "Als erfahrene Partner im Bereich der energieeffizienten Sanierung und des Neubaus kennen wir die Anforderungen moderner Immobilien aus technischer",
        "Als erfahrene Partner für Verkauf, Vermietung und Wertermittlung kennen wir die Anforderungen des Marktes aus wirtschaftlicher und technischer",
    ),
    (
        "Mehrwert durch Sanierungsberatung",
        "Mehrwert durch Gutachterkompetenz",
    ),
    (
        "Ihre Immobilienmakler für ganz Deutschland",
        "Ihr Immobilienmakler für Münster, Essen und Bochum",
    ),
    (
        "Wir sind in ganz Deutschland mit Niederlassungen in fast allen Bundesländern vertreten.",
        "Wir sind persönlich für Sie da – mit Standorten in Münster, Essen und Bochum.",
    ),
    (
        "Wir sind in ganz Deutschland mit Niederlassungen in fast allen Bundesländern vertreten. Wählen Sie die Niederlassung in Ihrer Nähe und rufen Sie uns an oder schreiben Sie uns. Seit 20 Jahren sind wir",
        "Wir betreuen Eigentümer in Münster, Essen, Bochum und Umgebung. Rufen Sie uns an oder schreiben Sie uns – wir melden uns persönlich. Seit Jahren sind wir",
    ),
    (
        "Wir sind für Sie da – bundesweit und auch regional vor Ort in Ihrer Nähe.",
        "Wir sind für Sie da – persönlich vor Ort in Münster, Essen und Bochum.",
    ),
    (
        "Unsere Immobilienmakler in ganz Deutschland",
        "Unsere Standorte in Münster, Essen und Bochum",
    ),
    (
        "Leistungen: Verkauf, Vermietung, Bewertung | Oberholz Immobilien</h1>",
        "Verkauf, Vermietung, Bewertung und Rückmietverkauf</h1>",
    ),
    (
        '<h1 class="mb-2">Leistungen: Verkauf, Vermietung, Bewertung | Oberholz Immobilien</h1>',
        '<h1 class="mb-2">Verkauf, Vermietung, Bewertung und Rückmietverkauf</h1>',
    ),
]

# page-specific surgical replacements
PAGE_FIXES = {
    "public/leistungen.html": [
        (
            re.compile(r"<h1[^>]*>.*?Leistungen: Verkauf, Vermietung, Bewertung \| Oberholz Immobilien.*?</h1>", re.I | re.S),
            '<h1 class="mb-2">Verkauf, Vermietung, Bewertung und Rückmietverkauf</h1>',
        ),
    ],
    "public/kontakt/kontakt-aufnehmen.html": [
        (
            re.compile(r"<h1[^>]*>.*?Ihre Immobilienmakler für ganz Deutschland.*?</h1>", re.I | re.S),
            '<h1>Ihr Immobilienmakler für Münster, Essen und Bochum</h1>',
        ),
    ],
}


def apply_phrases(text: str) -> tuple[str, int]:
    n = 0
    for old, new in sorted(EXTRA, key=lambda x: len(x[0]), reverse=True):
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    return text, n


def main() -> None:
    files = list(Path("public").glob("*.html"))
    files += list(Path("public/kontakt").glob("*.html"))
    files += list(Path("public/ueber-uns").glob("*.html"))
    files += list(Path("public/leistungen").glob("*.html"))
    files.append(Path("index.html"))

    for path in files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        text, n = apply_phrases(text)
        key = path.as_posix()
        for k, fixes in PAGE_FIXES.items():
            if key.endswith(k) or path.match(k):
                for pattern, repl in fixes:
                    text, c = pattern.subn(repl, text, count=1)
                    n += c
        if text != original:
            path.write_text(text, encoding="utf-8")
            print("patched", path, "replacements", n)
        elif n:
            print("noop?", path, n)


if __name__ == "__main__":
    main()
