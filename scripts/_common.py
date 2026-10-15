"""Gemeinsame Helfer für alle Audit-Scripts (Browser starten, Cookies ablehnen, Lazy-Load triggern)."""
from pathlib import Path

URL = "https://www.engelvoelkers.com/de/de"
LOCAL_URL = "http://localhost:5173/"
ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "reference" / "engelvoelkers"
ANA = ROOT / "analysis" / "engelvoelkers"
SHOTS = ROOT / "screenshots"
for d in (REF, ANA, SHOTS / "original", SHOTS / "local", SHOTS / "diff", SHOTS / "overlay"):
    d.mkdir(parents=True, exist_ok=True)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36")

VIEWPORTS = {
    "desktop-1920": (1920, 1080), "desktop-1600": (1600, 900), "desktop-1440": (1440, 900),
    "desktop-1366": (1366, 768), "tablet-1024": (1024, 1366), "tablet-768": (768, 1024),
    "mobile-430": (430, 932), "mobile-390": (390, 844), "mobile-375": (375, 812), "mobile-360": (360, 800),
}


async def new_page(browser, width, height, mobile=False):
    ctx = await browser.new_context(
        viewport={"width": width, "height": height}, user_agent=UA, locale="de-DE",
        device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
    return await ctx.new_page()


async def dismiss_cookies(page):
    """Datenschutzfreundlichste Option wählen: 'Ablehnen'."""
    for sel in ["button:has-text('Ablehnen')", "#onetrust-reject-all-handler"]:
        try:
            loc = page.locator(sel).first
            if await loc.is_visible(timeout=2500):
                await loc.click()
                await page.wait_for_timeout(600)
                return True
        except Exception:
            pass
    return False


async def settle(page, step=600, pause=120):
    """Einmal komplett scrollen, damit Lazy-Images laden, dann zurück nach oben."""
    h = await page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        await page.evaluate(f"window.scrollTo(0,{y})")
        await page.wait_for_timeout(pause)
        y += step
        h = await page.evaluate("document.documentElement.scrollHeight")
    await page.evaluate("window.scrollTo(0,0)")
    await page.evaluate("document.fonts.ready")
    await page.evaluate("""() => Promise.all([...document.images].filter(i=>!i.complete)
        .map(i=>new Promise(r=>{i.onload=i.onerror=r; setTimeout(r,4000)})))""")
    await page.wait_for_timeout(800)


async def open_original(browser, width, height, mobile=False):
    page = await new_page(browser, width, height, mobile)
    await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(2500)
    await dismiss_cookies(page)
    await settle(page)
    return page
