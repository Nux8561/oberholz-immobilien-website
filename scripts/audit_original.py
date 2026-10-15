"""Erster Probe-Lauf: Seite laden, Cookie-Banner (nur notwendige) ablehnen, Status + Screenshot."""
import asyncio, json, sys
from pathlib import Path
from playwright.async_api import async_playwright

URL = "https://www.engelvoelkers.com/de/de"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "reference" / "engelvoelkers"
ANA = ROOT / "analysis" / "engelvoelkers"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36")

async def dismiss_cookies(page):
    # Datenschutzfreundlichste Option: nur notwendige / ablehnen
    for sel in ["#onetrust-reject-all-handler", "button:has-text('Ablehnen')",
                "button:has-text('Nur notwendige')", "button:has-text('Alle ablehnen')",
                "[data-testid='uc-deny-all-button']", "button:has-text('Verweigern')"]:
        try:
            loc = page.locator(sel).first
            if await loc.is_visible(timeout=1500):
                await loc.click()
                await page.wait_for_timeout(800)
                return sel
        except Exception:
            pass
    return None

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1440, "height": 900}, user_agent=UA, locale="de-DE")
        page = await ctx.new_page()
        resp = await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        print("status", resp.status if resp else None)
        await page.wait_for_timeout(4000)
        await page.screenshot(path=str(OUT / "probe_before_cookies.png"))
        # Banner-Infos sammeln
        banner = await page.evaluate("""() => [...document.querySelectorAll('button')].filter(b=>b.offsetParent).map(b=>b.innerText.trim()).filter(Boolean).slice(0,60)""")
        print("buttons:", banner)
        used = await dismiss_cookies(page)
        print("cookie dismiss:", used)
        await page.wait_for_timeout(1500)
        await page.screenshot(path=str(OUT / "probe_after_cookies.png"))
        print("title:", await page.title())
        await b.close()

asyncio.run(main())
