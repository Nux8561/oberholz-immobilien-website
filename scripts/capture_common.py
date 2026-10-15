"""Gemeinsame Capture-Logik für Original und lokale Version: gleiche Viewports, Positionen, Wartezustände."""
import asyncio
from playwright.async_api import async_playwright
from _common import URL, LOCAL_URL, VIEWPORTS, SHOTS, dismiss_cookies, settle, new_page

POSITIONS = {"top": 0.0, "25": 0.25, "50": 0.5, "75": 0.75, "bottom": 1.0}

async def capture(kind, names=None, positions=True, full=True):
    url = URL if kind == "original" else LOCAL_URL
    out = SHOTS / kind
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, (w, h) in VIEWPORTS.items():
            if names and name not in names: continue
            for attempt in range(3):
                try:
                    page = await new_page(b, w, h, mobile=w < 768)
                    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    await page.wait_for_timeout(2500 if kind == "original" else 800)
                    if kind == "original": await dismiss_cookies(page)
                    await settle(page)
                    # Slider-Autoplay anhalten, damit Slide 1 sichtbar bleibt (beide Seiten gleich behandeln)
                    await page.evaluate("""() => { const b=[...document.querySelectorAll('main button')].find(b=>/^(Pause)$/i.test((b.getAttribute('aria-label')||b.innerText||'').trim())); if(b) b.click(); }""")
                    await page.wait_for_timeout(400)
                    if full:
                        await page.screenshot(path=str(out / f"{name}_full.png"), full_page=True)
                    if positions:
                        H = await page.evaluate("document.documentElement.scrollHeight")
                        for pos, f in POSITIONS.items():
                            await page.evaluate(f"window.scrollTo(0,{int((H - h) * f)})")
                            await page.wait_for_timeout(900)
                            await page.screenshot(path=str(out / f"{name}_{pos}.png"))
                    await page.context.close()
                    print(kind, name, "ok")
                    break
                except Exception as e:
                    print(kind, name, "retry", str(e)[:100])
        await b.close()
