"""Misst Elemente der lokalen Version: python3 scripts/probe_local.py <breite> <pfad> <selector> [...]"""
import asyncio, sys
from playwright.async_api import async_playwright
from _common import LOCAL_URL, new_page, settle

async def main():
    w, path, sels = int(sys.argv[1]), sys.argv[2].lstrip('/'), sys.argv[3:]
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await new_page(b, w, 900, w < 768)
        await pg.goto(LOCAL_URL + path); await settle(pg)
        for s in sels:
            r = await pg.evaluate("(s)=>[...document.querySelectorAll(s)].slice(0,8).map(e=>{const r=e.getBoundingClientRect(); return [Math.round(r.x),Math.round(r.y+scrollY),Math.round(r.width),Math.round(r.height)]})", s)
            print(f"{s:22s}", r)
        await b.close()
asyncio.run(main())
