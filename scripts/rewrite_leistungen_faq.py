"""Rewrite core Leistung pages + homepage FAQ for Oberholz SEO/GEO."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERKAUF = ROOT / "public" / "leistungen" / "immobilienverkauf.html"
VERMIETUNG = ROOT / "public" / "leistungen" / "vermietung-und-verpachtung.html"
BEWERTUNG = ROOT / "public" / "leistungen" / "immobilienbewertung.html"
INDEX = ROOT / "index.html"


def replace_all(text: str, pairs: list[tuple[str, str]]) -> tuple[str, int]:
    n = 0
    for old, new in pairs:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
        else:
            print("  MISSING:", old[:90])
    return text, n


def patch_verkauf() -> None:
    print("== immobilienverkauf")
    text = VERKAUF.read_text(encoding="utf-8", errors="ignore")
    pairs = [
        (
            "Immobilienverkauf mit Energiekompetenz – deutschlandweit erfolgreich",
            "Immobilienverkauf in Münster, Essen und Bochum",
        ),
        (
            "Die Oberholz Immobilien verbinden über 20 Jahre Erfahrung in der Immobilienvermittlung mit einzigartigem Fachwissen in Energieeffizienz. So erzielen Sie nicht nur den besten Verkaufspreis, sondern profitieren auch von einer professionellen Rundum-Betreuung.",
            "Oberholz Immobilien begleitet Ihren Immobilienverkauf persönlich und transparent: von der Marktwertermittlung durch unseren DIN-zertifizierten Immobiliengutachter über Exposé und Vermarktung bis zur Schlüsselübergabe in Münster, Essen und Bochum.",
        ),
        ("Maximaler Verkaufserfolg", "Ihr Vorteil beim Verkauf"),
        (
            "Höhere Verkaufspreise durch Banken-Netzwerk",
            "Marktgerechte Preisstrategie durch Gutachterkompetenz",
        ),
        (
            "Finanzierte Käufer statt unverbindlicher Anfragen",
            "Qualifizierte Interessenten statt unverbindlicher Anfragen",
        ),
        (
            "Energieausweise &amp; Sanierungsfahrpläne direkt im Haus",
            "Wertermittlung &amp; Exposé direkt aus einer Hand",
        ),
        (
            "Architekten, Gutachter &amp; Energieberater im eigenen Team",
            "Gutachter und Immobilienberater im eigenen Team",
        ),
        ("Deutschlandweite Stärke", "Starke Präsenz vor Ort"),
        (
            "Über 100 festangestellte Fachkräfte",
            "Erfahrenes Team aus Maklern und Gutachtern",
        ),
        (
            "Niederlassungen in ganz Deutschland",
            "Standorte in Münster, Essen und Bochum",
        ),
        (
            "Regionale Marktkenntnis + zentrale Expertise",
            "Regionale Marktkenntnis mit Gutachter-Expertise",
        ),
        (
            "Seit über 20 Jahren erfolgreich am Markt",
            "Langjährige Erfahrung in der Immobilienwirtschaft",
        ),
        (
            "Ihr starker Partner für den erfolgreichen Immobilienverkauf",
            "Ihr Partner für den erfolgreichen Immobilienverkauf",
        ),
        (
            "Ein Immobilienverkauf ist weit mehr als die reine Vermittlung zwischen Käufer",
            "Ein Immobilienverkauf ist weit mehr als die reine Vermittlung zwischen Eigentümer",
        ),
        (
            "Eigene Inhouse-Werbeagentur für maximale Sichtbarkeit",
            "Professionelle Vermarktung für maximale Sichtbarkeit",
        ),
        (
            "Mit mattomedia verfügen die Oberholz Immobilien über eine hauseigene Werbeagentur mit über 20 Jahren Erfahrung in der Immobilien- und Unternehmenskommunikation.",
            "Wir setzen auf hochwertige Exposés, professionelle Objektpräsentation und Vermarktung auf den führenden Immobilienplattformen.",
        ),
        (
            "Synergien durch unsere Energieeffizienz-Expertise",
            "Synergien durch unsere Gutachterkompetenz",
        ),
        (
            "Als zertifizierte Energieeffizienz-Experten des Bundes verbinden wir Immobilienvermittlung mit fundiertem Fachwissen rund um Sanierung, Förderung und energetische Optimierung.",
            "Als DIN-zertifizierter Immobiliengutachter und erfahrenes Maklerteam verbinden wir Vermittlung mit fundierter Wertermittlung nach Boden-, Ertrags- und Sachwert.",
        ),
        (
            "Dieses Zusammenspiel schafft für Verkäufer und Käufer klare Vorteile – und macht die Oberholz",
            "Dieses Zusammenspiel schafft für Verkäufer und Käufer klare Vorteile – und macht Oberholz",
        ),
        (
            "Erfolg durch unser deutschlandweites Netzwerk",
            "Erfolg durch lokales Know-how und starkes Netzwerk",
        ),
        (
            "Mit den Oberholz Immobilien setzen Sie auf die Schlagkraft eines bundesweit agierenden Unternehmens mit über 100 festangestellten Mitarbeitern",
            "Mit Oberholz Immobilien setzen Sie auf persönliche Betreuung vor Ort und ein starkes Netzwerk in Münster, Essen, Bochum und Umgebung",
        ),
        (
            "ohne die passenden Unterlagen, transparente Energiewerte und eine realistische Sanierungskosteneinschätzung",
            "ohne belastbare Unterlagen, eine realistische Marktwertermittlung und eine klare Verkaufsstrategie",
        ),
        (
            "mattomedia",
            "unser Vermarktungsansatz",
        ),
    ]
    text, n = replace_all(text, pairs)
    VERKAUF.write_text(text, encoding="utf-8")
    print(" replacements", n)


def patch_vermietung() -> None:
    print("== vermietung")
    text = VERMIETUNG.read_text(encoding="utf-8", errors="ignore")
    pairs = [
        (
            "Vermietung und Verpachtung mit Mehrwert",
            "Vermietung in Münster, Essen und Bochum",
        ),
        (
            "Mit den Oberholz Immobilien der EE-Experten GmbH sichern Sie sich nicht nur verlässliche Mieter, sondern auch eine nachhaltige Steigerung der Rendite. Profitieren Sie von unserem bundesweiten Netzwerk, langjähriger Erfahrung und einzigartiger Energiekompetenz.",
            "Mit Oberholz Immobilien sichern Sie sich passende, zuverlässige Mieter und eine marktgerechte Vermietung. Profitieren Sie von lokaler Marktkenntnis in Münster, Essen und Bochum sowie einer klaren, transparenten Abwicklung.",
        ),
        (
            "Vermietung und Verpachtung mit den Oberholz Immobilien",
            "Vermietung und Verpachtung mit Oberholz Immobilien",
        ),
        (
            "Die Oberholz Immobilien der EE-Experten GmbH sind Ihr zuverlässiger Partner, wenn es um die erfolgreiche Vermietung oder Verpachtung Ihrer Immobilie geht. Mit über 20 Jahren Erfahrung in Immobilien- und Energieberatung sowie einem bundesweiten Netzwerk sorgen wir dafür, dass Ihre Objekte optima",
            "Oberholz Immobilien ist Ihr zuverlässiger Partner für die erfolgreiche Vermietung Ihrer Immobilie. Mit Erfahrung in der Immobilienwirtschaft und starker Präsenz in Münster, Essen und Bochum sorgen wir dafür, dass Ihre Objekte optima",
        ),
        (
            "Energie- &amp; Sanierungskompetenz: Unsere Experten erstellen bei Bedarf Energieausweise, Wohnflächenberechnungen und Sanierungsfahrpläne – für ma",
            "Markt- &amp; Prozesskompetenz: Wir übernehmen Mietpreisanalyse, Objektpräsentation, Mieterauswahl und Übergabe – für ma",
        ),
        (
            "Unsere hauseigene Werbeagentur mattomedia ist Marktführer in der Architekturvisualisierung und eine der ersten Anlaufstellen für Immobilienvermarktung von Immobilienmaklern, Banken und Bauträgern in ganz Deutschland.",
            "Wir vermarkten Ihre Immobilie professionell auf den führenden Immobilienplattformen und bei geeigneten Suchkunden in der Region.",
        ),
        (
            "Nebenkosten optimieren – Mehrwert schaffen",
            "Marktgerecht vermieten – Mehrwert schaffen",
        ),
        (
            "Als zertifizierte Energieberater analysieren wir Ihre Immobilie ganzheitlich und zeigen konkrete Möglichkeiten auf, die Nebenkosten für Ihre Mieter spürbar zu senken. Diese Kompetenz macht uns einzigartig auf dem Immobilienmarkt und bietet Vorteile für alle Beteiligten:",
            "Wir analysieren den lokalen Mietmarkt und positionieren Ihre Immobilie so, dass Sie zuverlässige Mieter und eine stabile Rendite erzielen. Das bietet Vorteile für alle Beteiligten:",
        ),
        (
            "Warum profitiere ich als Vermieter, wenn die Nebenkosten sinken?",
            "Warum profitieren Sie von einer professionellen Vermietung?",
        ),
        (
            "Aber die Optimierung der Nebenkosten kostet doch sicher viel Geld?",
            "Was kostet eine professionelle Vermietung?",
        ),
        (
            "Warum es riskant ist, bei den Nebenkosten nichts zu tun",
            "Warum es riskant ist, die Vermietung allein zu organisieren",
        ),
        (
            "Die Energiekosten steigen seit Jahren kontinuierlich – und Experten rechnen auch in Zukunft mit deutlichen Erhöhungen. Für Vermieter bedeutet das: Wer heute nicht handelt, riskiert morgen noch höhere Nebenkosten und damit sinkende Attraktivität seiner Immobilie.",
            "Der Mietmarkt ist anspruchsvoll: falsche Mietpreise, ungeeignete Bewerber oder lückenhaftte Verträge kosten Zeit und Geld. Wer heute unstrukturiert vermietet, riskiert Leerstand, Streit und Ertragsausfälle.",
        ),
        ("EE-Experten GmbH", "Oberholz Immobilien"),
        ("bundesweiten Netzwerk", "regionalen Netzwerk"),
        ("bundesweite Netzwerk", "regionale Netzwerk"),
        ("mattomedia", "unser Vermarktungsansatz"),
    ]
    text, n = replace_all(text, pairs)
    VERMIETUNG.write_text(text, encoding="utf-8")
    print(" replacements", n)


def patch_bewertung() -> None:
    print("== immobilienbewertung")
    text = BEWERTUNG.read_text(encoding="utf-8", errors="ignore")
    pairs = [
        (
            "Immobilienbewertung & Gutachten – präzise, unabhängig, deutschlandweit",
            "Immobilienbewertung & Gutachten – präzise, unabhängig, vor Ort",
        ),
        (
            "Ob Verkauf, Kauf, Erbschaft oder gerichtliche Auseinandersetzungen – unsere zertifizierten Immobiliengutachter erstellen Bewertungen nach anerkannten Verfahren und sorgen für Klarheit, Sicherheit und überzeugende Argumente. Mit über 20 Jahren Erfahrung und ca. 100 festangestellt",
            "Ob Verkauf, Kauf, Erbschaft oder gerichtliche Auseinandersetzungen – unser DIN-zertifizierter Immobiliengutachter Michael Oberholz erstellt Bewertungen nach anerkannten Verfahren und sorgt für Klarheit, Sicherheit und überzeugende Argumente. Mit langjähriger Erfahrung und persönlicher Betreuung vor Ort in Münster, Essen und Bochum arbeiten wir strukturiert",
        ),
        (
            "Energieberater-Kompetenz: Die EE-Experten sind ebenfalls im Bereich der Energi",
            "Gutachter-Kompetenz: Oberholz Immobilien bewertet Immobilien fundiert nach Boden-, Ertrags- und Sachwert sowie anhand von Markt",
        ),
        (
            "Immobiliengutachten als Fundament für Ihren Verkaufserfolg",
            "Immobiliengutachten als Fundament für Ihren Verkaufserfolg",
        ),
        (
            "Ein erfolgreicher Immobilienverkauf benötigt mehr als nur ein gutes Exposé – er braucht eine verlässliche und nachv",
            "Ein erfolgreicher Immobilienverkauf braucht mehr als ein gutes Exposé – er braucht eine verlässliche und nachv",
        ),
        ("EE-Experten", "Oberholz Immobilien"),
        ("deutschlandweit", "in Münster, Essen und Bochum"),
    ]
    text, n = replace_all(text, pairs)
    BEWERTUNG.write_text(text, encoding="utf-8")
    print(" replacements", n)


def patch_faq() -> None:
    print("== faq index")
    text = INDEX.read_text(encoding="utf-8", errors="ignore")
    pairs = [
        (
            "Ja. Wir beraten Käufer und Mieter umfassend – auch zu Fördermöglichkeiten, energetischem Zustand und Sanierungsoptionen. So treffen Sie eine informierte und zukunftssichere Entscheidung.",
            "Ja. Wir beraten Käufer und Mieter praxisnah zu Lage, Marktwert, Objektzustand und realistischer Preisfindung. So treffen Sie eine informierte Entscheidung – transparent und ohne Verkaufsdruck.",
        ),
        (
            "Nein. Wir vermitteln Immobilien jeder Art – unsere Stärke liegt jedoch darin, energetisches Verbesserungspotenzial zu erkennen und gezielt darzustellen. Das erhöht die Chancen auf dem Markt erheblich.",
            "Ja. Wir bewerten und vermitteln Wohn- und Gewerbeimmobilien jeder Art – vom Einfamilienhaus über Eigentumswohnungen bis zum Mehrfamilienhaus. Unsere Stärke ist die belastbare Marktwertermittlung.",
        ),
        (
            "Weil wir den Immobilienmarkt mit einem ganzheitlichen Blick betrachten: Unsere langjährige Expertise im Bereich Energieeffizienz ergänzt die klassische Immobilienvermittlung perfekt. So schaffen wir echten Mehrwert für Verkäufer, Käufer, Mieter und Vermieter.",
            "Weil wir Vermittlung und Wertermittlung verbinden: Unser DIN-zertifizierter Immobiliengutachter Michael Oberholz ermittelt belastbare Marktwerte – als Basis für Verkauf, Vermietung und strategische Entscheidungen in Münster, Essen und Bochum.",
        ),
        (
            "Wir gehen weit über die reine Vermittlung hinaus – denn wir verstehen Immobilien nicht nur als Objekte, sondern als energetische Systeme mit Potenzial.Als zertifizierte Immobiliengutachter analysieren wir nicht nur den Ist-Zustand Ihrer Immobilie, sondern zeigen auf, wie Sie durch gezielte Maßnahmen – oft staatlich gefördert – eine deutliche Wertsteigerung erzielen können.Beispiel: Der Austausch einer veralteten Gasheizung gegen eine moderne Wärmepumpe kann nicht nur die Energiebilanz verbessern, sondern den Verkaufswert Ihrer Immobilie erheblich steigern – besonders, wenn Käufer Fördervorteile erkennen oder bereits eine zukunftssichere Lösung vorfinden.",
            "Wir gehen über die reine Inseratsvermittlung hinaus: Als Makler mit integrierter Gutachterkompetenz bewerten wir Ihre Immobilie nachvollziehbar, entwickeln eine klare Verkaufs- oder Vermietungsstrategie und begleiten Sie bis zum Abschluss. So entstehen realistische Preise, bessere Verhandlungen und weniger Streuverluste.",
        ),
        (
            "Wir analysieren den energetischen Zustand Ihrer Immobilie und zeigen Optimierungspotenziale auf. So steigern wir nicht nur die Attraktivität, sondern auch den Marktwert – fundiert, transparent und nachweisbar.",
            "Wir ermitteln den realistischen Marktwert, bereiten ein aussagekräftiges Exposé vor und führen Verhandlungen mit fundierten Argumenten. So sichern Sie Preis, Tempo und Sicherheit im Verkaufsprozess.",
        ),
        (
            "Nach einem Erstgespräch analysieren wir Ihre Immobilie umfassend – sowohl marktseitig als auch energetisch. Anschließend erstellen wir ein professionelles Vermarktungskonzept und begleiten Sie bis zum erfolgreichen Abschluss.",
            "Nach dem Erstgespräch folgt die Ortsbesichtigung und Marktwertermittlung. Danach entwickeln wir die Verkaufs- oder Vermietungsstrategie, vermarkten das Objekt und begleiten Sie bis zum Notar bzw. zur Übergabe.",
        ),
        # data-search-term leftovers (lowercase)
        (
            "vermitteln sie nur energieeffiziente immobilien?nein. wir vermitteln immobilien jeder art – unsere stärke liegt jedoch darin, energetisches verbesserungspotenzial zu erkennen und gezielt darzustellen. das erhöht die chancen auf dem markt erheblich.",
            "bewerten und vermitteln sie alle arten von immobilien?ja. wir bewerten und vermitteln wohn- und gewerbeimmobilien jeder art – vom einfamilienhaus über eigentumswohnungen bis zum mehrfamilienhaus. unsere stärke ist die belastbare marktwertermittlung.",
        ),
        (
            "welche vorteile habe ich als verkäufer durch ihre energiekompetenz?wir analysieren den energetischen zustand ihrer immobilie und zeigen optimierungspotenziale auf. so steigern wir nicht nur die attraktivität, sondern auch den marktwert – fundiert, transparent und nachweisbar.",
            "welche vorteile habe ich als verkäufer durch ihre gutachterkompetenz?wir ermitteln den realistischen marktwert, bereiten ein aussagekräftiges exposé vor und führen verhandlungen mit fundierten argumenten. so sichern sie preis, tempo und sicherheit im verkaufsprozess.",
        ),
    ]
    text, n = replace_all(text, pairs)

    leftovers = [
        ("energetisches Verbesserungspotenzial", "marktgerechtes Preis- und Vermarktungspotenzial"),
        ("sowohl marktseitig als auch energetisch", "marktseitig und objektbezogen"),
        ("als energetische Systeme mit Potenzial", "als werthaltige Vermögenswerte mit Marktpotenzial"),
        ("Fördermöglichkeiten, energetischem Zustand und Sanierungsoptionen", "Lage, Marktwert, Objektzustand und Preisfindung"),
        ("Expertise im Bereich Energieeffizienz", "Expertise in Wertermittlung und Transaktionsbegleitung"),
    ]
    for old, new in leftovers:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
            print("  leftover", old[:55], c)

    # JSON-LD FAQ block: rewrite acceptedAnswer texts if still old
    json_pairs = [
        (
            "Ja. Wir beraten Käufer und Mieter umfassend – auch zu Fördermöglichkeiten, energetischem Zustand und Sanierungsoptionen. So treffen Sie eine informierte und zukunftssichere Entscheidung.",
            "Ja. Wir beraten Käufer und Mieter praxisnah zu Lage, Marktwert, Objektzustand und realistischer Preisfindung. So treffen Sie eine informierte Entscheidung – transparent und ohne Verkaufsdruck.",
        ),
    ]
    for old, new in json_pairs:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c

    INDEX.write_text(text, encoding="utf-8")
    print(" replacements", n)


def main() -> None:
    patch_verkauf()
    patch_vermietung()
    patch_bewertung()
    patch_faq()


if __name__ == "__main__":
    main()
