#!/usr/bin/env python3
from pathlib import Path
import re

checks = {
    "index": Path("index.html"),
    "leistungen": Path("public/leistungen.html"),
    "bochum": Path("public/kontakt/immobilienmakler-bochum.html"),
    "mfh": Path("public/leistungen/mehrfamilienhaeuser-kaufen-bochum.html"),
    "wohnung": Path("public/leistungen/wohnungen-kaufen-bochum.html"),
    "energie": Path("public/leistungen/energieberatung.html"),
}

for name, path in checks.items():
    t = path.read_text(encoding="utf-8", errors="replace")
    title = re.search(r"<title>([^<]+)</title>", t)
    print("==", name, "==")
    print("title:", title.group(1) if title else "?")
    print(
        "dvag", "dvag-logo" in t,
        "swiss", "swiss-life" in t,
        "interhyp", "interhyp" in t,
        "wue", "wuestenrot" in t.lower() or "Wüstenrot" in t,
        "flow", "flowfact" in t.lower(),
        "immowelt", "immowelt.png" in t,
        "klein", "kleinanzeigen" in t.lower(),
        "kauf-nav", "wohnungen-kaufen-bochum" in t,
        "trust-link", "sat1.de" in t or "galileo.tv" in t,
    )

# standort order on index
t = Path("index.html").read_text(encoding="utf-8")
m = re.search(
    r'immobilienmakler-bochum\.html.*?immobilienmakler-muenster\.html.*?immobilienmakler-essen\.html',
    t,
    re.S,
)
print("nav order Bochum>Münster>Essen:", bool(m))
