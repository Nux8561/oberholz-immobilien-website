#!/usr/bin/env python3
from pathlib import Path

p = Path("index.html")
t = p.read_text(encoding="utf-8")
reps = [
    (
        '<h1 class="mb-2"><strong>Ihr Immobilienmakler</strong> in '
        '<span class="text-underline-energy-scale">Bochum und Münster</span></h1>',
        '<h1 class="mb-2"><strong>Ihr Immobilienmakler</strong> in '
        '<span class="text-underline-energy-scale">Essen</span></h1>',
    ),
    ("Bewertung &amp; Energie-Analyse", "Preiseinschätzung &amp; Strategie"),
    ("Bewertung & Energie-Analyse", "Preiseinschätzung & Strategie"),
]
for old, new in reps:
    print(t.count(old), old[:70])
    t = t.replace(old, new)
p.write_text(t, encoding="utf-8")
print("ok")
