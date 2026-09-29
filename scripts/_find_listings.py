from pathlib import Path
import re

text = Path("index.html").read_text(encoding="utf-8")
idx = text.find("Aktuelle Immobilien")
if idx < 0:
    idx = text.find("aus unserer Vermittlung")
Path("scripts/_listings_slice.txt").write_text(text[max(0, idx - 200) : idx + 5000], encoding="utf-8")
print("idx", idx)
print("count immobilien cards", text.count("regio-immo") + text.count("immobilie"))
# find section ids around listings
for m in re.finditer(r"(Aktuelle Immobilien|Vermittlung|expose|immoscout|is24)", text, re.I):
    if m.start() > 400000:  # body-ish
        print(m.group(0), m.start())
        if m.start() > 520000:
            break
