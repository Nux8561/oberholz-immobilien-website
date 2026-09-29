# -*- coding: utf-8 -*-
"""Clean Stuttgart leftovers from Münster/Essen/Bochum standort pages."""
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPLACEMENTS = [
    ("streit@oberholz-immobilien.com", "mail@oberholz-immobilien.com"),
    ("Königstraße 22", "Münster · Essen · Bochum"),
    ("70173 Münster", "Standorte in Münster, Essen und Bochum"),
    ("70173", ""),
    ("Landeshauptstadt Münster", "Universitätsstadt Münster"),
    ("Landeshauptstadt", "Stadt"),
    ("im Südwesten", "in der Region"),
    ("für den Südwesten", "vor Ort"),
    ("des Südwestens", "der Region"),
    ("Metropolregion Münster", "Region Münster"),
    ("schwäbischer Gründlichkeit", "fundierter Marktkenntnis"),
    ("schwäbischer", "persönlicher"),
    ("Killesberg & Degerloch (S)", "Kreuzviertel & Schlossviertel"),
    ("Münster-West & Süd (S)", "Hiltrup & Mecklenbeck"),
    ("Bad Cannstatt & Frauenkopf (S)", "Gievenbeck & Handorf"),
    ("Esslingen & Ludwigsburg (Region)", "Greven & Telgte (Münsterland)"),
    ("Böblingen & Sindelfingen (Region)", "Steinfurt & Coesfeld (Münsterland)"),
    ("Waiblingen & das Remstal (Region)", "Warendorf & Ahlen (Münsterland)"),
    ("im Kessel", "in Münster"),
    ("über den Kessel", "über die Stadt"),
    ("Kessel-Immobilien", "Wohnimmobilien"),
    ("Kessel, Hang oder Ebene", "Innenstadt, Wohngebiet oder Umland"),
    ("Halbhöhenlage", "gute Wohnlage"),
    ("Hanglage", "Wohnlage"),
    ("Top-Hanglagen", "begehrten Wohnlagen"),
    ("exklusive Halbhöhenlagen", "begehrte Wohnlagen"),
    ("Energieeffizienz-Experte", "Immobiliengutachter"),
    ("Energiekompetenz", "Gutachterkompetenz"),
    ("EE-Experten YouTube-Channel", "Oberholz Immobilien Kontakt"),
]

CITY_EXTRA = {
    "muenster": [
        ("Ihr Partner für Häuser, Wohnungen und Anlageimmobilien im Südwesten",
         "Ihr Partner für Häuser, Wohnungen und Anlageimmobilien in Münster"),
    ],
    "essen": [
        ("Kreuzviertel & Schlossviertel", "Rüttenscheid & Südviertel"),
        ("Hiltrup & Mecklenbeck", "Kupferdreh & Werden"),
        ("Gievenbeck & Handorf", "Altendorf & Steele"),
        ("Greven & Telgte (Münsterland)", "Mülheim & Oberhausen (Ruhrgebiet)"),
        ("Steinfurt & Coesfeld (Münsterland)", "Bottrop & Gladbeck (Ruhrgebiet)"),
        ("Warendorf & Ahlen (Münsterland)", "Gelsenkirchen & Hattingen"),
        ("Universitätsstadt Münster", "Ruhrgebietsstadt Essen"),
        ("Münster und Münsterland", "Essen und das Ruhrgebiet"),
        ("Münsterland", "Ruhrgebiet"),
        ("in Münster", "in Essen"),
        ("für Münster", "für Essen"),
        ("Region Münster", "Region Essen"),
    ],
    "bochum": [
        ("Kreuzviertel & Schlossviertel", "Ehrenfeld & Querenburg"),
        ("Hiltrup & Mecklenbeck", "Langendreer & Wattenscheid"),
        ("Gievenbeck & Handorf", "Weitmar & Linden"),
        ("Greven & Telgte (Münsterland)", "Dortmund & Witten"),
        ("Steinfurt & Coesfeld (Münsterland)", "Herne & Castrop-Rauxel"),
        ("Warendorf & Ahlen (Münsterland)", "Hattingen & Sprockhövel"),
        ("Universitätsstadt Münster", "Universitätsstadt Bochum"),
        ("Münster und Münsterland", "Bochum und Umgebung"),
        ("Münsterland", "Umgebung"),
        ("in Münster", "in Bochum"),
        ("für Münster", "für Bochum"),
        ("Region Münster", "Region Bochum"),
    ],
}

for slug in ("muenster", "essen", "bochum"):
    path = Path(f"public/kontakt/immobilienmakler-{slug}.html")
    t = path.read_text(encoding="utf-8", errors="ignore")
    orig = t
    for a, b in REPLACEMENTS:
        t = t.replace(a, b)
    for a, b in CITY_EXTRA.get(slug, []):
        t = t.replace(a, b)
    # broken empty address remnants
    t = re.sub(r"\n\s*\n\s*\n", "\n\n", t)
    if t != orig:
        path.write_text(t, encoding="utf-8")
        print("cleaned", path.name)
    else:
        print("no change", path.name)

    # leftover checks
    for bad in ["Killesberg", "Degerloch", "Königstraße", "streit@", "schwäb", "Südwesten", "70173", "Cannstatt"]:
        if bad in t:
            print("  leftover", bad, t.count(bad))
