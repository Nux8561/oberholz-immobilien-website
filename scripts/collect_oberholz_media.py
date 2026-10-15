"""Lädt Bilder (Team, Banner, Logo, Ratgeber) und öffentliche PDFs der Oberholz-Seite ins Projekt:
public/assets/oberholz/media/<pfad> und public/downloads/<datei>.pdf – und schreibt eine Zuordnung media-map.json."""
import json, re, urllib.request
from pathlib import Path
from _common import ROOT

BASE = "https://oberholz-immobilien.pages.dev"
CONTENT = ROOT / "analysis" / "oberholz-pages" / "content"
PAGES = json.loads((ROOT / "analysis" / "oberholz-pages" / "pages.json").read_text())
MEDIA = ROOT / "public" / "assets" / "oberholz" / "media"
DL = ROOT / "public" / "downloads"
DL.mkdir(parents=True, exist_ok=True)

def get(url, dest, kinds):
    if dest.exists() and dest.stat().st_size > 0: return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (oberholz-site-migration)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            ct = r.headers.get("Content-Type", "")
            if r.status != 200 or not any(ct.startswith(k) for k in kinds): return False
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print("  fehlgeschlagen:", url, str(e)[:60]); return False

urls = set()
for f in CONTENT.glob("*.json"):
    for b in json.loads(f.read_text())["blocks"]:
        if b["t"] == "img" and "/media/" in b["src"] and "/object-" not in b["src"]: urls.add(b["src"].split("?")[0])
for extra in ["/media/oberholz-logo.png", "/media/oberholz-team/michael-oberholz.png", "/media/videocard_avatar/oberholz_facepile.jpg", "/media/brochure_energieberatung.png"]:
    urls.add(BASE + extra)
mapping = {}
for u in sorted(urls):
    rel = u.split("/media/", 1)[1]
    if get(u, MEDIA / rel, ("image/",)): mapping[u] = f"/assets/oberholz/media/{rel}"
print(len(mapping), "Bilder")

pdfs = {l["href"].split("?")[0] for v in PAGES.values() for l in v.get("links", []) if l["href"].lower().endswith(".pdf")}
for u in sorted(pdfs):
    name = u.rsplit("/", 1)[1]
    if get(u, DL / name, ("application/pdf", "application/octet-stream")): mapping[u] = f"/downloads/{name}"
print(len(pdfs), "PDFs")
(ROOT / "analysis" / "oberholz-pages" / "media-map.json").write_text(json.dumps(mapping, indent=1))
