# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")

idx = t.find("Unsere Standorte")
print("standorte idx", idx)
chunk = t[idx : idx + 12000]
Path("scripts/_tmp_standorte_chunk.html").write_text(chunk, encoding="utf-8")

for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', chunk, re.S):
    plain = re.sub(r"<[^>]+>", " ", m.group(2))
    plain = re.sub(r"\s+", " ", plain).strip()
    href = m.group(1)
    if "makler" in plain.lower() or "immobilienmakler" in href or plain:
        if any(x in href.lower() or x in plain.lower() for x in [
            "stuttgart", "muenchen", "hamburg", "hannover", "frankfurt",
            "duesseldorf", "villingen", "muenster", "essen", "bochum", "standort", "makler"
        ]):
            print("CARD", href[:100], "=>", plain[:120])

idx2 = t.find('title="Kontakt"')
print("\nNAV start", idx2)
nav = t[idx2 : idx2 + 6000]
Path("scripts/_tmp_kontakt_nav.html").write_text(nav, encoding="utf-8")
for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', nav, re.S):
    plain = re.sub(r"<[^>]+>", " ", m.group(2))
    plain = re.sub(r"\s+", " ", plain).strip()
    if plain:
        print("NAV", m.group(1)[:90], "=>", plain[:100])

# also find mobile menu kontakt cities
for label in ["Mobilmakler", "Immobilienmakler Stuttgart", "Immobilienmakler Hamburg"]:
    print(label, "count", t.count(label))
