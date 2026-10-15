"""Alle Exposés der Oberholz-Seite → src/data/listings.json + Fotos nach public/assets/oberholz/objekte/<id>/"""
import asyncio, json, re
import urllib.request
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from _common import ROOT

BASE = "https://oberholz-immobilien.pages.dev"
PAGES = ROOT / "analysis" / "oberholz-pages"
IMG_DIR = ROOT / "public" / "assets" / "oberholz" / "objekte"
MAX_IMAGES = 12

JS = r"""() => {
  const T = e => (e ? e.innerText.replace(/\s+/g, ' ').trim() : '');
  const hero = document.querySelector('.immo-detail-hero-content');
  const badges = [...document.querySelectorAll('.immo-detail-hero-content .badge')].map(T);
  const loc = T(hero?.querySelector('.lead span'));
  const priceLabel = T(hero?.querySelector('.text-uppercase'));
  const price = T(hero?.querySelector('.fw-bold[style*="1.75rem"]'));
  const provision = T(document.querySelector('.immo-provision'));
  const count = T(document.querySelector('.immo-detail-hero .badge.position-absolute'));
  const all = document.body.innerText;
  const area = (all.match(/([\d.,]+)\s*m²\s*\n?\s*[\d.,]+\s*Zi/) || [])[1] || (all.match(/([\d.,]+)\s*m²/) || [])[1] || '';
  const rooms = (all.match(/([\d.,]+)\s*Zi\./) || [])[1] || '';
  const sections = {};
  document.querySelectorAll('main h2, .container h2').forEach(h => {
    const title = T(h); if (!title || /Interesse|^Attraktive|^$/.test(title) || sections[title]) return;
    const paras = []; let e = h.nextElementSibling;
    while (e && e.tagName !== 'H2') { e.querySelectorAll ? (e.matches('p,li') ? paras.push(T(e)) : e.querySelectorAll('p,li').forEach(x => paras.push(T(x)))) : 0; e = e.nextElementSibling; }
    if (paras.length) sections[title] = paras.filter(Boolean);
  });
  const facts = [...document.querySelectorAll('table tr, dl > div, .immo-facts li, .immo-detail-facts li')].map(T).filter(Boolean).slice(0, 40);
  return { title: T(document.querySelector('h1')), badges, loc, priceLabel, price, provision, count, area, rooms, sections, facts };
}"""

def num(s):
    s = (s or '').replace('.', '').replace(',', '.')
    try: return float(s)
    except ValueError: return None

def fetch(url, dest):
    if dest.exists(): return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (oberholz-site-migration)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            if r.status != 200 or not r.headers.get('Content-Type', '').startswith('image/'): return False
            dest.write_bytes(r.read())
        return True
    except Exception:
        return False

async def one(ctx, url, out):
    pg = await ctx.new_page()
    try:
        await pg.goto(url, wait_until="networkidle", timeout=45000)
        d = await pg.evaluate(JS)
    except Exception as e:
        print("ERR", url, str(e)[:80]); await pg.close(); return
    await pg.close()
    if not d["title"] or "nicht gefunden" in d["title"]: return
    lid = re.search(r"(\d{6,})(?:\.html)?$", url).group(1)
    city_slug = urlparse(url).path.split('/')[2]
    m = re.match(r"(\d{5})\s+([^,]+)(?:,\s*(.+))?", d["loc"] or "")
    total = int((re.search(r"/\s*(\d+)", d["count"] or "") or [0, 1])[1])
    folder = IMG_DIR / lid; folder.mkdir(parents=True, exist_ok=True)
    images = []
    for i in range(min(total, MAX_IMAGES)):
        name = f"{i:03d}.jpg"
        if fetch(f"{BASE}/media/object-zoom-780/{lid}_{i:03d}.jpg", folder / name) or fetch(f"{BASE}/media/object-hero-780/{lid}_{i:03d}.jpg", folder / name):
            images.append(f"/assets/oberholz/objekte/{lid}/{name}")
    out.append({
        "id": lid, "url": url, "title": d["title"], "type": d["badges"][0] if d["badges"] else "", "mode": d["badges"][1] if len(d["badges"]) > 1 else "Kauf",
        "zip": m.group(1) if m else "", "city": (m.group(2).strip() if m else d["loc"]), "district": (m.group(3) or "").strip() if m else "",
        "citySlug": city_slug, "priceLabel": d["priceLabel"], "priceText": d["price"], "price": num(re.sub(r"[^\d.,]", "", d["price"] or "")),
        "provision": d["provision"], "area": num(d["area"]), "rooms": num(d["rooms"]), "imageTotal": total, "images": images,
        "sections": d["sections"], "facts": d["facts"],
    })
    print(len(out), lid, d["title"][:60], len(images), "Bilder")

async def main():
    pages = json.loads((PAGES / "pages.json").read_text())
    urls = {u.replace(".html", "") for u in pages if re.search(r"/immobilien/[^/]+/.+\d{6,}", u)}
    urls |= {u.replace(".html", "") for u in json.loads((PAGES / "uncrawled.json").read_text()) if "/immobilien/" in u}
    urls = sorted(urls)
    print(len(urls), "Exposé-URLs")
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); ctx = await b.new_context(viewport={"width": 1440, "height": 900})
        for i in range(0, len(urls), 6):
            await asyncio.gather(*[one(ctx, u, out) for u in urls[i:i + 6]])
        await b.close()
    out.sort(key=lambda x: x["id"], reverse=True)
    (ROOT / "src" / "data" / "listings.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("gespeichert:", len(out))

asyncio.run(main())
