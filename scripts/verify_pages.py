"""Check representative local pages for leaks, console errors and broken images."""
from playwright.sync_api import sync_playwright

PAGES = [
    "/",
    "/leistungen.html",
    "/leistungen/immobilienverkauf.html",
    "/immobilien.html",
    "/immobilien/balzheim/attraktives-reihenmittelhaus-perfekt-fuer-4-familienmitglieder-5273744.html",
    "/immopedia.html",
    "/immopedia/aufstellungsbeschluss-bebauungsplan.html",
    "/regionen.html",
    "/regionen/a.html",
    "/kontakt/kontakt-aufnehmen.html",
    "/ueber-uns.html",
    "/ratgeber.html",
    "/service.html",
    "/impressum.html",
    "/datenschutzerklaerung.html",
    "/whitepaper-generationenwechsel.html",
    "/dokumente-downloads.html",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for path in PAGES:
        errors = []
        leaks = []
        broken = []
        page = browser.new_page(viewport={"width": 1440, "height": 900}, locale="de-DE")
        page.on("pageerror", lambda exc: errors.append(str(exc)[:180]))
        page.on("console", lambda msg: errors.append(msg.text[:180]) if msg.type == "error" else None)
        page.on("request", lambda req: leaks.append(req.url) if "immobilien-experten.de" in req.url else None)
        page.on("response", lambda res: broken.append(f"{res.status} {res.url}") if res.status >= 400 else None)
        response = page.goto("http://127.0.0.1:5173" + path, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(500)
        title = page.title()
        h1 = page.locator("h1").first.inner_text()[:80] if page.locator("h1").count() else ""
        print(f"{response.status if response else '?'} {path}")
        print(" ", title[:80])
        print("  h1:", h1.replace("\n", " "))
        print("  errors", len(errors), "leaks", len(leaks), "broken", len(broken))
        for item in (errors + leaks + broken)[:5]:
            print("   ", item[:160])
        page.close()
    browser.close()
