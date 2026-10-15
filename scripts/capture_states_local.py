"""Interaktionszustände der lokalen Version (gleich wie Referenz-Captures in inspect_interactions.py)."""
import asyncio
from playwright.async_api import async_playwright
from _common import LOCAL_URL, SHOTS, new_page, settle

async def main():
    out = SHOTS / "local"
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await new_page(b, 1440, 900); await page.goto(LOCAL_URL); await settle(page)
        for i, lab in enumerate(["Kaufen & Mieten", "Immobilie verkaufen", "Immobilienmakler", "Commercial", "Unternehmen"]):
            await page.hover(f".hdr__link:has-text('{lab}')"); await page.wait_for_timeout(700)
            await page.screenshot(path=str(out / f"megamenu_{i}_1440.png"))
            await page.mouse.move(700, 880); await page.wait_for_timeout(500)
        await page.click("button[aria-label='Dropdown-Menü für Objektarten']"); await page.wait_for_timeout(400)
        await page.screenshot(path=str(out / "dropdown_open_1440.png"), clip={"x": 600, "y": 150, "width": 840, "height": 600})
        await page.context.close()
        m = await new_page(b, 390, 844, mobile=True); await m.goto(LOCAL_URL); await settle(m)
        await m.click(".hdr__burger"); await m.wait_for_timeout(600)
        await m.screenshot(path=str(out / "mobile_menu_open_390.png"))
        await m.click(".mnav__row >> nth=0"); await m.wait_for_timeout(600)
        await m.screenshot(path=str(out / "mobile_menu_sub_390.png"))
        await b.close()
    print("states ok")
asyncio.run(main())
