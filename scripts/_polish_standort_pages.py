# -*- coding: utf-8 -*-
"""Polish Münster/Essen/Bochum standort page titles and H1."""
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAGES = [
    ("muenster", "Münster", "Münster und Münsterland"),
    ("essen", "Essen", "Essen und Ruhrgebiet"),
    ("bochum", "Bochum", "Bochum und Umgebung"),
]

for slug, name, region in PAGES:
    path = Path(f"public/kontakt/immobilienmakler-{slug}.html")
    t = path.read_text(encoding="utf-8", errors="ignore")
    # title
    t2 = re.sub(
        r"<title>.*?</title>",
        f"<title>Immobilienmakler {name} | Oberholz Immobilien</title>",
        t,
        count=1,
        flags=re.S,
    )
    # meta description if present
    t2 = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="Oberholz Immobilien – Ihr Immobilienmakler in {name}. Verkauf, Vermietung und Wertermittlung in {region}.">',
        t2,
        count=1,
    )
    # H1 cleanup – keep structure but ensure city name
    # common patterns from clone
    t2 = t2.replace(
        f"Ihr Immobilienmakler für {name} und ganz {region}",
        f"Ihr Immobilienmakler für {name}",
    )
    t2 = t2.replace(
        f"Ihr Immobilienmakler für {name} und {region}",
        f"Ihr Immobilienmakler für {name}",
    )
    if t2 != t:
        path.write_text(t2, encoding="utf-8")
        print("polished", path.name)
    else:
        print("unchanged", path.name)

    # show title/h1
    title = re.search(r"<title>(.*?)</title>", t2)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t2, re.S)
    print(" title:", title.group(1) if title else None)
    if h1:
        plain = re.sub(r"<[^>]+>", "", h1.group(1))
        plain = re.sub(r"\s+", " ", plain).strip()
        print(" h1:", plain[:120])
