"""Exercise local interactions and record console or request leaks."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "interactions.json"
LOCAL = "http://127.0.0.1:5173/"


def main() -> None:
    notes = []
    leaks = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, locale="de-DE")
        page.on(
            "request",
            lambda req: leaks.append(req.url)
            if "immobilien-experten.de" in req.url or "rex-api-call" in req.url or "googletagmanager" in req.url
            else None,
        )
        page.goto(LOCAL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(800)

        leistungen = page.locator("a.nav-link", has_text="Leistungen").first
        leistungen.hover()
        page.wait_for_timeout(400)
        menu_open = page.locator(".dropdown-menu.show").count()
        notes.append({"action": "hover Leistungen", "open_menus": menu_open})
        page.screenshot(path=str(ROOT / "screenshots" / "local" / "menu-leistungen.png"))
        page.mouse.move(10, 10)
        page.wait_for_timeout(200)

        for label in ("Service", "Über uns", "Kontakt"):
            link = page.locator("a.nav-link", has_text=label).first
            link.hover()
            page.wait_for_timeout(300)
            notes.append({"action": f"hover {label}", "open_menus": page.locator(".dropdown-menu.show").count()})

        page.locator("#iwf .iwf-choice", has_text="Wohnhaus").click()
        page.wait_for_timeout(500)
        active = page.locator("#iwf .iwf-step.is-active h3").inner_text()
        notes.append({"action": "form Wohnhaus", "question": active})
        page.locator("#iwf .iwf-step.is-active .iwf-choice", has_text="Einfamilienhaus").click()
        page.wait_for_timeout(500)
        notes.append({"action": "form Einfamilienhaus", "question": page.locator("#iwf .iwf-step.is-active h3").inner_text()})
        back = page.locator("#iwf-globalnav [data-back]")
        notes.append({"action": "back visibility", "visibility": back.evaluate("el => getComputedStyle(el).visibility")})
        back.click()
        page.wait_for_timeout(300)
        notes.append({"action": "form back", "question": page.locator("#iwf .iwf-step.is-active h3").inner_text()})

        faq = page.locator("a[href^='#collapse-3307']").first
        if faq.count():
            faq.click()
            page.wait_for_timeout(300)
            notes.append({"action": "faq first", "expanded": faq.get_attribute("aria-expanded")})

        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(400)
        toggler = page.locator("button.navbar-toggler, .navbar-toggler").first
        if toggler.count():
            toggler.click()
            page.wait_for_timeout(400)
            notes.append({"action": "mobile menu", "visible": page.locator("#mobileMenu.show, .navbar-collapse.show").count()})
            page.screenshot(path=str(ROOT / "screenshots" / "local" / "menu-mobile.png"))

        browser.close()
    OUT.write_text(json.dumps({"notes": notes, "leaks": leaks}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(notes, ensure_ascii=False, indent=2))
    print("leaks", len(leaks))


if __name__ == "__main__":
    main()
