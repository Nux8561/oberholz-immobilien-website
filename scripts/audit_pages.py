"""Audit der Unterseiten-Templates: Full-Page-Screenshot + gerenderter DOM (Geometrie/Styles) für 1440 und 390 px.
Ergebnis: reference/engelvoelkers/pages/<slug>_<w>.png und analysis/engelvoelkers/pages/<slug>_<w>.json
Aufruf: python3 scripts/audit_pages.py [slug …]"""
import asyncio, json, sys
from playwright.async_api import async_playwright
from _common import REF, ANA, new_page, dismiss_cookies, settle
from inspect_dom import JS

BASE = "https://www.engelvoelkers.com"
PAGES = {
    "suche": "/de/de/immobilien/res/kaufen/immobilien",
    "expose": "/de/de/exposes/fbbe0087-3eb4-54f2-aa84-2c3ce639f79b",
    "verkaufen": "/de/de/verkauf/immobilie-verkaufen",
    "bewertung": "/de/de/verkauf/immobilienbewertung",
    "makler-werden": "/de/de/immobilienmakler-werden",
    "commercial": "/de/de/commercial",
    "ueber-uns": "/de/de/unternehmen/ueber-uns",
    "standorte": "/de/de/shops",
    "stadt": "/de/de/berlin",
    "magazin": "/gg-magazine/de",
}
OUT_IMG = REF / "pages"; OUT_ANA = ANA / "pages"
OUT_IMG.mkdir(exist_ok=True); OUT_ANA.mkdir(exist_ok=True)

async def one(b, slug, path, w, h):
    for attempt in range(3):
        try:
            page = await new_page(b, w, h, mobile=w < 768)
            await page.goto(BASE + path, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(3000)
            await dismiss_cookies(page)
            await settle(page)
            data = await page.evaluate(JS)
            data["finalUrl"] = page.url
            data["title"] = await page.title()
            (OUT_ANA / f"{slug}_{w}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
            await page.screenshot(path=str(OUT_IMG / f"{slug}_{w}.png"), full_page=True)
            await page.context.close()
            print(slug, w, "ok", data["scrollHeight"], data["finalUrl"])
            return
        except Exception as e:
            print(slug, w, "retry", str(e)[:120])

async def main():
    slugs = sys.argv[1:] or list(PAGES)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for s in slugs:
            await one(b, s, PAGES[s], 1440, 900)
            await one(b, s, PAGES[s], 390, 844)
        await b.close()

if __name__ == "__main__":
    asyncio.run(main())
