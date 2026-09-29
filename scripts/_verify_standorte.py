# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

for rel in [
    "index.html",
    "public/kontakt/kontakt-aufnehmen.html",
    "public/kontakt/immobilienmakler-muenster.html",
    "public/ueber-uns.html",
]:
    p = Path(rel)
    if not p.exists():
        print("MISSING", rel)
        continue
    t = p.read_text(encoding="utf-8", errors="ignore")
    print("====", rel, "len", len(t))
    for c in [
        "Hamburg",
        "Stuttgart",
        "München",
        "Düsseldorf",
        "Hannover",
        "Frankfurt",
        "Villingen",
        "Münster",
        "Essen",
        "Bochum",
        "Baden-Württemberg",
        "bundesweit",
        "immobilienmakler-hamburg",
        "immobilienmakler-muenster",
        "immobilienmakler-essen",
        "immobilienmakler-bochum",
    ]:
        n = t.count(c)
        if n:
            print(f"  {c}: {n}")

    # desktop nav after title=Kontakt
    i = t.find('title="Kontakt"')
    if i >= 0:
        chunk = t[i : i + 2800]
        print("  NAV labels:")
        for m in re.finditer(r"Immobilienmakler ([^<]+)</span>", chunk):
            print("   -", m.group(1))

    # table body cities
    if "Unsere Standorte" in t:
        j = t.find("Unsere Standorte")
        chunk = t[j : j + 8000]
        for m in re.finditer(r"Immobilienmakler ([^<]+)</a>", chunk):
            print("  TABLE link:", m.group(1))
        for city in ["Stuttgart", "Hamburg", "Münster", "Essen", "Bochum", "Berlin", "München"]:
            if f"> {city}<" in chunk or f"> {city}</" in chunk or f" {city}</td>" in chunk:
                print("  TABLE city cell:", city)
