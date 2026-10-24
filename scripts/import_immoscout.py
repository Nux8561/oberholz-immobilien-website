"""Aktueller Objektbestand aus dem ImmoScout24-Homepage-Modul → src/data/listings.json + Fotos.

Quelle ist dieselbe Ergebnisliste, die auf der bisherigen Website eingebunden ist. Was dort nicht mehr steht
(verkauft, offline), fällt hier heraus; Ansprechpartner und Telefon kommen aus dem Exposé („Angeboten von“).
Ausführen: python3 scripts/import_immoscout.py  – danach `npm run build:seo`.
Bis ein API-Zugang vorliegt, ist das der Abgleich von Hand."""
import json, re, shutil, sys, urllib.request
from bs4 import BeautifulSoup
from _common import ROOT, UA

PORTAL = "https://portal.immobilienscout24.de"
LIST_ID = "82828525"
IMG_DIR = ROOT / "public" / "assets" / "oberholz" / "objekte"
OUT = ROOT / "src" / "data" / "listings.json"
MAX_IMAGES = 12


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "de-DE"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def num(s):
    m = re.search(r"[\d.]+(?:,\d+)?", s or "")
    return float(m.group(0).replace(".", "").replace(",", ".")) if m else None


def slug(s):
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def block(soup, title):
    h = soup.find("h4", string=lambda t: t and t.strip() == title)
    return h.parent if h else None


def criteria(soup):
    out = {}
    for title in ("Hauptkriterien", "Weitere Daten", "Kosten"):
        b = block(soup, title)
        for li in (b.select("li") if b else []):
            ps = li.find_all("p")
            if len(ps) >= 2:
                key = re.sub("[\u00ad\u200b]", "", ps[0].get_text(" ", strip=True)).rstrip(":").strip()
                out[key] = ps[1].get_text(" ", strip=True)
    return out


def lines(b):
    """Absätze eines Textblocks; Zeilenumbrüche (<br>) trennen die Einträge wie im bisherigen Datenbestand."""
    out = []
    for p in b.find_all("p"):
        for br in p.find_all("br"):
            br.replace_with("\n")
        out += [re.sub(r"\s+", " ", x).strip() for x in p.get_text().split("\n")]
    return [x for x in out if x]


def location(soup):
    """„Deutschland, 45257 Essen, Kupferdreh,“ oder „Nordsternstraße 37, Gelsenkirchen, Horst, Deutschland“"""
    b = soup.select_one(".expose--text__address")
    text = (b.get_text(" ", strip=True) if b else "").split("Die vollständige Adresse")[0]
    parts = [x.strip() for x in text.split(",") if x.strip() and x.strip() != "Deutschland"]
    for i, x in enumerate(parts):
        m = re.match(r"(\d{5})\s+(.+)", x)
        if m:
            return m.group(1), m.group(2), (parts[i + 1] if i + 1 < len(parts) else "")
    parts = [x for x in parts if not re.search(r"\d", x)]  # Straße mit Hausnummer überspringen
    return "", (parts[0] if parts else ""), (parts[1] if len(parts) > 1 else "")


def provider(soup):
    b = block(soup, "Angeboten von")
    text = [x for x in (b.get_text("\n", strip=True).split("\n") if b else []) if x.strip()]
    name = next((re.sub(r"^(Herr|Frau)\s+", "", x) for x in text if re.match(r"^(Herr|Frau)\s", x)), "")
    phone = next((re.sub(r"^\w+:\s*", "", x) for x in text if re.match(r"^(Telefon|Mobil):", x)), "")
    return name, phone


def provision(c, mode):
    if mode == "Miete":
        return ""
    t = c.get("Provision", "")
    m = re.match(r"\s*([\d.]+(?:,\d+)?)\s*(%|€|EUR)?", t)
    if not m:
        return t
    if m.group(2) in ("€", "EUR"):
        return f"zzgl. {m.group(1)} € Käuferprovision (pauschal)"
    return f"zzgl. {m.group(1)} % Käuferprovision"  # „3,57%“, „4%“, auch „3,57 Die Maklerprovision …“


def list_types(html):
    """Objektart je Scout-ID aus der Ergebnisliste („Wohnung zum Kauf“, „Haus zum Kauf“, „Anlageobjekte“ …)"""
    out = {}
    for m in re.finditer(rf"/expose/{LIST_ID}/(\d+)/", html):
        rest = BeautifulSoup(html[m.end():m.end() + 4000], "html.parser").get_text(" ", strip=True)
        t = re.search(r"\b(Haus|Wohnung|Grundstück)\s+zu[mr]\s+(Kauf|Miete)|Anlageobjekte", rest)
        out.setdefault(m.group(1), t.group(1) or "Haus" if t else "Haus")
    return out


def one(sid, ptype):
    url = f"{PORTAL}/expose/{LIST_ID}/{sid}/1/1"
    soup = BeautifulSoup(get(url), "html.parser")
    title = soup.select_one(".expose--text h4").get_text(" ", strip=True)
    c = criteria(soup)
    zip_, city, district = location(soup)
    mode = "Miete" if "Kaltmiete" in c else "Kauf"
    price_key = "Kaltmiete" if mode == "Miete" else "Kaufpreis"
    sections = {}
    for k in ("Objektbeschreibung", "Ausstattung", "Lage", "Sonstiges"):
        b = block(soup, k)
        if b and lines(b):
            sections[k] = lines(b)
    agent, phone = provider(soup)

    srcs = [i.get("data-src") for i in soup.select("img.sp-image") if i.get("data-src")]
    srcs = list(dict.fromkeys(srcs))
    folder = IMG_DIR / sid
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    images = []
    for n, src in enumerate(srcs[:MAX_IMAGES]):
        big = "https:" + src.replace("/resize/540x540%3E/format/jpg", "/resize/1106x830%3E/format/jpg/quality/80")
        (folder / f"{n:03d}.jpg").write_bytes(get(big))
        images.append(f"/assets/oberholz/objekte/{sid}/{n:03d}.jpg")

    price = num(c.get(price_key))
    return {
        "id": sid, "url": url, "title": title, "type": ptype, "mode": mode,
        "zip": zip_, "city": city, "district": district, "citySlug": slug(city),
        "priceLabel": price_key.upper(), "priceText": f"{price:,.0f} €".replace(",", ".") if price else "Preis auf Anfrage", "price": price,
        "provision": provision(c, mode),
        "area": num(c.get("Wohnfläche ca.") or c.get("Vermietbare Fläche ca.") or c.get("Nutzfläche ca.")),
        "plot": num(c.get("Grundstücksfläche ca.")), "rooms": num(c.get("Zimmer")),
        "energyClass": c.get("Energieeffizienzklasse", ""),
        "agent": agent, "agentPhone": phone,
        "imageTotal": len(srcs), "images": images, "sections": sections,
        "facts": [f"{k}: {v}" for k, v in c.items()],
    }


def main():
    html = get(f"{PORTAL}/ergebnisliste/{LIST_ID}").decode("utf-8", "replace")
    ids = list(dict.fromkeys(re.findall(rf"/expose/{LIST_ID}/(\d+)/", html)))
    if re.search(rf"/ergebnisliste/{LIST_ID}/2\b", html):
        sys.exit("Ergebnisliste hat eine zweite Seite – Blättern im Skript ergänzen.")
    print(len(ids), "Objekte in der ImmoScout-Ergebnisliste")
    out = []
    types = list_types(html)
    for sid in ids:
        x = one(sid, types[sid])
        out.append(x)
        print(sid, x["mode"], x["type"], x["zip"], x["city"], x["district"], x["priceText"], "|", x["agent"], x["agentPhone"], "|", len(x["images"]), "Bilder")
    out.sort(key=lambda x: x["id"], reverse=True)

    # Fotos nicht mehr angebotener Objekte entfernen
    keep = {x["id"] for x in out}
    for d in IMG_DIR.iterdir():
        if d.is_dir() and d.name not in keep:
            shutil.rmtree(d)
            print("entfernt:", d.name)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print("gespeichert:", len(out), "→", OUT.relative_to(ROOT))


main()
