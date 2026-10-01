#!/usr/bin/env python3
"""Clean remaining EE leftovers in contact-widget.html for Oberholz."""

from __future__ import annotations

from pathlib import Path

PATH = Path("public/theme/contact-widget.html")

REPLACEMENTS = [
    ("4.9 / 5 (3.148 Bewertungen)", "4.9 / 5 (9 Bewertungen)"),
    ("3.148 Bewertungen", "9 Bewertungen"),
    ("3148", "9"),
    # Energy topics → immobilien topics
    (
        '<option value="Bestandskunde">Bestandskunde</option>'
        '<option value="Fördermittel">Fördermittel</option>'
        '<option value="Sanierung">Sanierung</option>'
        '<option value="Effizienzhaus">Effizienzhaus</option>'
        '<option value="Energieausweis">Energieausweis</option>'
        '<option value="Energie sparen">Energie sparen</option>'
        '<option value="Thermografie">Thermografie</option>'
        '<option value="Blower Door Test">Blower Door Test</option>'
        '<option value="Sanierungsfahrplan">Sanierungsfahrplan</option>'
        '<option value="Einzelmaßnahme">Einzelmaßnahme</option>'
        '<option value="eWärmeG">eWärmeG</option>'
        '<option value="Steuererstattung">Steuererstattung</option>'
        '<option value="Zählerstand">Zählerstand</option>'
        '<option value="Gas-/Öl-Abrechnung">Gas-/Öl-Abrechnung</option>'
        '<option value="Bewerbung">Bewerbung</option>'
        '<option value="Kooperationsanfrage">Kooperationsanfrage</option>'
        '<option value="Sonstiges">Sonstiges</option>',
        '<option value="Immobilie verkaufen">Immobilie verkaufen</option>'
        '<option value="Immobilie vermieten">Immobilie vermieten</option>'
        '<option value="Immobilienbewertung">Immobilienbewertung</option>'
        '<option value="Rückmietverkauf">Rückmietverkauf</option>'
        '<option value="Kaufberatung">Kaufberatung</option>'
        '<option value="Mehrfamilienhaus">Mehrfamilienhaus</option>'
        '<option value="Wohnung">Wohnung</option>'
        '<option value="Bestandskunde">Bestandskunde</option>'
        '<option value="Kooperationsanfrage">Kooperationsanfrage</option>'
        '<option value="Sonstiges">Sonstiges</option>',
    ),
]


def main() -> None:
    html = PATH.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS:
        if old in html:
            html = html.replace(old, new)
            print("replaced:", old[:60])
        else:
            print("MISSING:", old[:60])
    PATH.write_text(html, encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
