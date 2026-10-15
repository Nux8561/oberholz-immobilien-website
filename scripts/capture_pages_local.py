"""Screenshots aller Unterseiten-Templates lokal (1440 + 390) inkl. Fehler-/Overflow-Check.
Aufruf: python3 scripts/capture_pages_local.py [slug …]"""
import asyncio, sys
from playwright.async_api import async_playwright
from _common import LOCAL_URL, SHOTS, new_page, settle

ROUTES = {
    "suche": "immobilien/kaufen", "expose": "expose/hamburg-stadtvilla", "verkaufen": "verkaufen", "bewertung": "bewertung",
    "makler-werden": "makler-werden", "commercial": "commercial", "ueber-uns": "ueber-uns", "standorte": "standorte",
    "stadt": "stadt/berlin", "magazin": "magazin",
}

async def main():
    slugs = sys.argv[1:] or list(ROUTES)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for slug in slugs:
            for w, h in ((1440, 900), (390, 844)):
                pg = await new_page(b, w, h, w < 768)
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
                await pg.goto(LOCAL_URL + ROUTES[slug]); await settle(pg)
                ow = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                H = await pg.evaluate("document.documentElement.scrollHeight")
                await pg.screenshot(path=str(SHOTS / "local" / f"page_{slug}_{w}.png"), full_page=True)
                print(f"{slug:14s} {w:4d}  H={H:6d}  overflow={ow}  errors={errs[:2]}")
                await pg.context.close()
        await b.close()

asyncio.run(main())
