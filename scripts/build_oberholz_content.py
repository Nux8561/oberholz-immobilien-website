"""Bereinigt die extrahierten Oberholz-Inhalte und schreibt src/data/oberholz/content.json:
Seiten (Blöcke), FAQs, Startseiten-FAQ (JSON-LD). Bilder/PDFs werden auf lokale Pfade umgestellt."""
import json, re
from _common import ROOT

A = ROOT / "analysis" / "oberholz-pages"
CONTENT = A / "content"
MEDIA = json.loads((A / "media-map.json").read_text())

DROP = re.compile(r"(Gerne helfen wir Ihnen|Ich freue mich auf Ihren Anruf|Ihr Michael Oberholz|Wir helfen Ihnen gerne|Rufen Sie uns an|Kostenfreie Servicenummer|Montag bis Samstag|^UNSERE STANDORTE$|PDF Broschürendownload|Laden Sie hier unsere Broschüren|^Broschüre |Die angezeigten Bewertungen stammen|echte Google-Kundenrezensionen|Alle Google-Bewertungen ansehen|^Jetzt Beratung anfragen|^Verkauf$|^Vermietung$|^Immobilienbewertung$|^Bewertungsverfahren$|^Rückmietverkauf$|^Betreuung & Abwicklung$|^\d[\d.,]*/5$|Bewertungen$)", re.I)
FIX = [
    ("der Oberholz Immobilien der Oberholz Immobilien", "der Oberholz Immobilien"),
    ("Oberholz Immobilien der Oberholz Immobilien", "Oberholz Immobilien"),
    ("Mit unser Vermarktungsansatz", "Mit unserem Vermarktungsansatz"),
    ("mit unser Vermarktungsansatz", "mit unserem Vermarktungsansatz"),
    ("Mit unser Vermarktungsansatz verfügen", "Mit unserem Vermarktungsansatz verfügen"),
    ("durch unseren DIN-erfahrenen Maklerteam", "durch unser DIN-erfahrenes Maklerteam"),
    ("in Bochum und Münsteren Netzwerk", "in Bochum und Münster verankerten Netzwerk"),
    ("Unser Das Team von Oberholz Immobilien", "Das Team von Oberholz Immobilien"),
    ("Familien unternehmen", "Familienunternehmen"),
]

def fix(t):
    for a, b in FIX: t = t.replace(a, b)
    return t.strip()

def clean(blocks):
    out = []
    for b in blocks:
        t = b["t"]
        if t == "img":
            src = MEDIA.get(b["src"].split("?")[0])
            if not src or "logo" in src or src.endswith(".svg"): continue
            b = {"t": "img", "src": src, "alt": b.get("alt", "")}
        elif t == "pdf":
            href = MEDIA.get(b["href"].split("?")[0])
            if not href: continue
            b = {"t": "pdf", "href": href, "text": b.get("text", "")}
        elif "text" in b:
            if DROP.search(b["text"]) or len(b["text"]) < 2: continue
            b = {"t": t, "text": fix(b["text"])}
        elif "items" in b:
            items = [fix(i) for i in b["items"] if not DROP.search(i)]
            if not items: continue
            b = {"t": t, "items": items}
        elif t == "table":
            b = {"t": t, "rows": [[fix(c) for c in r] for r in b["rows"]]}
        elif t == "qa":
            b = {"t": "qa", "q": fix(b["q"]), "a": fix(b["a"])}
        # Dubletten: identisch zu einem der letzten 3 Blöcke, oder Absatz = vorheriges Zitat
        key = json.dumps(b, ensure_ascii=False, sort_keys=True)
        if any(json.dumps(x, ensure_ascii=False, sort_keys=True) == key for x in out[-3:]): continue
        if b.get("t") == "p" and out and out[-1].get("t") == "blockquote" and out[-1].get("text") == b.get("text"): continue
        out.append(b)
    # Abschnitt „Aktuelle Immobilien …“ (Kartenliste) entfernen – wird durch echte Objekt-Komponente ersetzt
    res, skip = [], False
    for b in out:
        if b["t"] in ("h2",) : skip = bool(re.match(r"(Aktuelle Immobilien|Unsere Broschüren|Partner$|Immobilienmakler in .* und Umgebung)", b["text"]))
        if b["t"] == "h3" and re.match(r"Einige unserer Referenzen", b["text"]): skip = True
        if not skip: res.append(b)
    return res

pages = {}
for f in sorted(CONTENT.glob("*.json")):
    if f.stem.startswith(("immobilien-", "immopedia-")) or f.stem == "immopedia": continue
    d = json.loads(f.read_text())
    pages[f.stem] = {"title": d["title"].split(" | ")[0], "blocks": clean(d["blocks"])}

faqs = json.loads((A / "faqs.json").read_text())
faqs = {k: [{"q": fix(x["q"]), "a": fix(x["a"])} for x in v if len(x["a"]) > 30 and not x["q"].startswith("Mehr über")] for k, v in faqs.items()}
ld = json.loads((A / "jsonld.json").read_text())
home_faq = [{"q": fix(q["name"]), "a": fix(q["acceptedAnswer"]["text"])} for x in ld["/"] for y in (x.get("@graph") or [x]) if y.get("@type") == "FAQPage" for q in y["mainEntity"]]
out = {"pages": pages, "faqs": faqs, "homeFaq": home_faq}
(ROOT / "src" / "data" / "oberholz" / "content.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(pages), "Seiten,", sum(len(v) for v in faqs.values()), "FAQs,", len(home_faq), "Startseiten-FAQ")
for k, v in pages.items(): print(f"  {k:70s} {len(v['blocks']):3d} Blöcke  {v['title'][:50]}")
