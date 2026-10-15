"""Vergleicht Section-Positionen (top/height) der lokalen Version mit der Referenz (dom_<w>.json)."""
import asyncio, json, sys
from playwright.async_api import async_playwright
from _common import LOCAL_URL, ANA, new_page, settle

async def main():
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
    ref = json.loads((ANA / f"dom_{w}.json").read_text())
    rt = [s['r'] for s in ref['sections']] + [ref['footer']['r']]
    async with async_playwright() as p:
        b = await p.chromium.launch(); page = await new_page(b, w, 900, mobile=w < 768)
        await page.goto(LOCAL_URL); await settle(page)
        loc = await page.evaluate("""() => [...document.querySelector('main').children, document.querySelector('footer')].map(e=>{const r=e.getBoundingClientRect(); return {y:Math.round(r.y+scrollY), h:Math.round(r.height), cls:e.className.split(' ')[0]}})""")
        H = await page.evaluate("document.documentElement.scrollHeight")
        await b.close()
    print(f"{'#':>2} {'ref.y':>7} {'loc.y':>7} {'Δy':>5} | {'ref.h':>6} {'loc.h':>6} {'Δh':>5}  class")
    for i, (r, l) in enumerate(zip(rt, loc)):
        print(f"{i:>2} {r['y']:>7} {l['y']:>7} {l['y']-r['y']:>5} | {r['h']:>6} {l['h']:>6} {l['h']-r['h']:>5}  {l['cls']}")
    print("scrollHeight ref", ref['scrollHeight'], "local", H)

asyncio.run(main())
