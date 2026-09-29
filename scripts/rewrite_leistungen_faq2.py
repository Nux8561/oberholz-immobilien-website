"""Second pass: regex-based cleanup for Leistung pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sub(text: str, pattern: str, repl: str, flags=0) -> tuple[str, int]:
    return re.subn(pattern, repl, text, flags=flags)


def patch_file(path: Path, ops: list[tuple[str, str, int]]) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    total = 0
    for pattern, repl, flags in ops:
        text, n = sub(text, pattern, repl, flags)
        total += n
        if n == 0:
            print("  miss", pattern[:80])
        else:
            print("  ok", n, pattern[:60])
    path.write_text(text, encoding="utf-8")
    print(path.name, "total", total)


def main() -> None:
    verkauf = ROOT / "public/leistungen/immobilienverkauf.html"
    vermietung = ROOT / "public/leistungen/vermietung-und-verpachtung.html"
    bewertung = ROOT / "public/leistungen/immobilienbewertung.html"
    index = ROOT / "index.html"

    print("== verkauf")
    patch_file(
        verkauf,
        [
            (
                r"<h1[^>]*>\s*Immobilienverkauf mit Energiekompetenz[^<]*</h1>",
                "<h1>Immobilienverkauf in Münster, Essen und Bochum</h1>",
                re.I,
            ),
            (
                r"Immobilienverkauf deutschlandweit\s*[–-]\s*mit Energiekompetenz[^\"<]*",
                "Immobilienverkauf Münster, Essen, Bochum | Oberholz Immobilien",
                re.I,
            ),
            (
                r"Als zertifizierte Energieeffizienz-Experten des Bundes verbinden wir Immobilienvermittlung mit fundiertem Fachwissen rund um Sanierung, Förderung und energetische Optimierung\.",
                "Als DIN-zertifizierter Immobiliengutachter und erfahrenes Maklerteam verbinden wir Vermittlung mit fundierter Wertermittlung nach Boden-, Ertrags- und Sachwert.",
                0,
            ),
            (
                r"setzen Sie auf die Schlagkraft eines bundesweit agierenden Unternehmens mit über 100 festangestellten Mitarbeitern",
                "setzen Sie auf persönliche Betreuung vor Ort und ein starkes Netzwerk in Münster, Essen, Bochum und Umgebung",
                0,
            ),
            (
                r"Mit mattomedia verfügen die Oberholz Immobilien über eine hauseigene Werbeagentur mit über 20 Jahren Erfahrung in der Immobilien- und Unternehmenskommunikation\.",
                "Wir setzen auf hochwertige Exposés, professionelle Objektpräsentation und Vermarktung auf den führenden Immobilienplattformen.",
                0,
            ),
            (
                r"Architekten, Gutachter\s*&amp;\s*Energieberater im eigenen Team",
                "Gutachter und Immobilienberater im eigenen Team",
                0,
            ),
            (
                r"Die Oberholz Immobilien verbinden über 20 Jahre Erfahrung in der Immobilienvermittlung mit einzigartigem Fachwissen in Energieeffizienz\.[^<]{0,200}",
                "Oberholz Immobilien begleitet Ihren Immobilienverkauf persönlich und transparent: von der Marktwertermittlung durch unseren DIN-zertifizierten Immobiliengutachter über Exposé und Vermarktung bis zur Schlüsselübergabe in Münster, Essen und Bochum.",
                0,
            ),
            (r"Energiekompetenz", "Gutachterkompetenz", 0),
            (r"energieeffizien[^\s<]{0,20}", "marktgerecht", 0),
            (r"energetisch(?:en|e|er|es)?", "fachlich", 0),
            (r"deutschlandweit", "in Münster, Essen und Bochum", 0),
            (r"bundesweit", "regional", 0),
            (r"Die EE-Experten GmbH kooperiert mit Wüstenrot", "Oberholz Immobilien – Ihr Partner vor Ort", 0),
            (r"EE-Experten GmbH", "Oberholz Immobilien", 0),
            (r"EE-Experten", "Oberholz Immobilien", 0),
            (r"mattomedia", "unser Vermarktungsteam", 0),
        ],
    )

    print("== vermietung")
    patch_file(
        vermietung,
        [
            (
                r"<h1[^>]*>\s*Vermietung und Verpachtung mit Mehrwert\s*</h1>",
                "<h1>Vermietung in Münster, Essen und Bochum</h1>",
                re.I,
            ),
            (
                r"Mit den Oberholz Immobilien der EE-Experten GmbH sichern Sie sich nicht nur verlässliche Mieter, sondern auch eine nachhaltige Steigerung der Rendite\.[^<]{0,220}",
                "Mit Oberholz Immobilien sichern Sie sich passende, zuverlässige Mieter und eine marktgerechte Vermietung in Münster, Essen und Bochum.",
                0,
            ),
            (
                r"Die Oberholz Immobilien der EE-Experten GmbH sind Ihr zuverlässiger Partner, wenn es um die erfolgreiche Vermietung oder Verpachtung Ihrer Immobilie geht\.[^<]{0,260}",
                "Oberholz Immobilien ist Ihr zuverlässiger Partner für die erfolgreiche Vermietung Ihrer Immobilie. Mit lokaler Marktkenntnis in Münster, Essen und Bochum sorgen wir dafür, dass Ihre Objekte optimal vermietet werden.",
                0,
            ),
            (
                r"Unsere hauseigene Werbeagentur mattomedia ist Marktführer in der Architekturvisualisierung und eine der ersten Anlaufstellen für Immobilienvermarktung von Immobilienmaklern, Banken und Bauträgern in ganz Deutschland\.",
                "Wir vermarkten Ihre Immobilie professionell auf den führenden Immobilienplattformen und bei geeigneten Suchkunden in der Region.",
                0,
            ),
            (r"einzigartiger Energiekompetenz", "fundierter Marktkenntnis", 0),
            (r"Energiekompetenz", "Marktkompetenz", 0),
            (r"Energieeffizienz", "Objektqualität", 0),
            (r"energetische Expertise", "fachliche Expertise", 0),
            (r"energetisch(?:en|e|er|es)?", "fachlich", 0),
            (r"deutschlandweit", "in Münster, Essen und Bochum", 0),
            (r"EE-Experten", "Oberholz Immobilien", 0),
            (r"mattomedia", "unser Vermarktungsteam", 0),
            (r"Fördermöglichkeiten maximiert", "Vermietungschancen maximiert", 0),
        ],
    )

    print("== bewertung")
    patch_file(
        bewertung,
        [
            (
                r"Zertifizierte Gutachter\s*&amp;\s*Energiekompetenz",
                "DIN-zertifizierter Immobiliengutachter Michael Oberholz",
                0,
            ),
            (
                r"Ob Verkauf, Kauf, Erbschaft oder gerichtliche Auseinandersetzungen\s*[–-]\s*unsere zertifizierten Immobiliengutachter erstellen Bewertungen nach anerkannten Verfahren und sorgen für Klarheit, Sicherheit und überzeugende Argumente\.[^<]{0,180}",
                "Ob Verkauf, Kauf, Erbschaft oder gerichtliche Auseinandersetzungen – unser DIN-zertifizierter Immobiliengutachter Michael Oberholz erstellt Bewertungen nach anerkannten Verfahren und sorgt für Klarheit und Sicherheit in Münster, Essen und Bochum.",
                0,
            ),
            (r"Energiekompetenz", "Gutachterkompetenz", 0),
            (r"» Energieeffizienz Experten", "» Oberholz Immobilien Münster", 0),
            (r"Energieeffizienz Experten", "Oberholz Immobilien", 0),
            (r"mattomedia Werbeagentur", "Oberholz Immobilien Bochum", 0),
            (r"mattomedia", "Oberholz Immobilien", 0),
            (r"deutschlandweit", "in Münster, Essen und Bochum", 0),
        ],
    )

    print("== index leftovers")
    patch_file(
        index,
        [
            (
                r"Ihr deutschlandweiter Partner für Immobilien\s*&amp;\s*Energieberatung\. Verkauf, Sanierung\s*&amp;\s*Energieeffizienz[^\"]*",
                "Ihr Immobilienmakler für Münster, Essen und Bochum. Verkauf, Vermietung, Rückmietverkauf und Wertermittlung.",
                0,
            ),
            (
                r"Verkauf, Sanierung\s*&amp;\s*Energieeffizienz – alles aus einer Hand\. Jetzt beraten lassen!",
                "Verkauf, Vermietung und Wertermittlung – persönlich in Münster, Essen und Bochum.",
                0,
            ),
            (
                r"Energieausweis und fachliche Bewertung inklusive",
                "Marktwertermittlung und fundierte Bewertung inklusive",
                0,
            ),
            (
                r"Energieausweis und energetische Bewertung inklusive",
                "Marktwertermittlung und fundierte Bewertung inklusive",
                0,
            ),
            (
                r"von der marktgerechten Analyse über Fördermöglichkeiten bis zur 3D-Visualisierung",
                "von der Marktwertermittlung über Exposé und Strategie bis zur Schlüsselübergabe",
                0,
            ),
            (
                r"Der Austausch einer veralteten Gasheizung gegen eine moderne Wärmepumpe kann nicht nur die Energiebilanz verbessern, sondern den Verkaufswert Ihrer Immobilie erheblich steigern[^\.<]*\.",
                "Eine belastbare Wertermittlung und klare Verkaufsargumente erhöhen die Abschlusschancen deutlich – für Eigentümer und Kaufinteressenten gleichermaßen.",
                0,
            ),
            (r"» \.mattomedia Werbeagentur", "» Oberholz Immobilien Bochum", 0),
            (r"mattomedia Werbeagentur", "Oberholz Immobilien Bochum", 0),
            (r"deutschlandweit", "in Münster, Essen und Bochum", 0),
        ],
    )


if __name__ == "__main__":
    main()
