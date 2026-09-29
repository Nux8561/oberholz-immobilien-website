from pathlib import Path

samples = [
    Path("index.html"),
    Path("public/regionen.html"),
    Path("public/immobilien.html"),
    Path("public/leistungen.html"),
    Path("public/immobilien/balzheim/attraktives-reihenmittelhaus-perfekt-fuer-4-familienmitglieder-5273744.html"),
]
for path in samples:
    text = path.read_text(encoding="utf-8", errors="ignore")
    print(path.name, "abs", text.count("https://www.immobilien-experten.de"), "proto", text.count("//www.immobilien-experten.de"))
