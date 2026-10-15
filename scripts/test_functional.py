"""Funktionale QA der lokalen Startseite (Playwright, Chromium). Aufruf: npm test  (Dev-Server muss laufen)
Prüft alle Homepage-Interaktionen sowie Konsole, 404s, Bild-Ladefehler und horizontales Overflow."""
import asyncio, sys
from playwright.async_api import async_playwright, expect
from _common import LOCAL_URL, new_page

results = []

def ok(name, cond, info=""):
    results.append((name, bool(cond), info))
    print(("PASS " if cond else "FAIL ") + name + (f"  ({info})" if info else ""))

async def desktop(b):
    page = await new_page(b, 1440, 900)
    errors, bad = [], []
    page.on("console", lambda m: m.type == "error" and errors.append(m.text))
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("response", lambda r: r.status >= 400 and bad.append(f"{r.status} {r.url}"))
    await page.goto(LOCAL_URL); await page.wait_for_load_state("networkidle")
    ok("Homepage Load", await page.locator("main > *").count() == 14, "14 Abschnitte (ohne Newsletter)")
    ok("Desktop Layout: Navigation sichtbar", await page.locator(".hdr__nav").is_visible())

    # Mega-Menü öffnen / schließen (Hover + Escape)
    await page.hover(".hdr__link:has-text('Immobilie verkaufen')"); await page.wait_for_timeout(400)
    ok("Mega Menu Open", await page.locator("#flyout-1.is-open").count() == 1)
    ok("Header Navigation: aktiver Link", await page.locator(".hdr__link.is-active").inner_text() == "Immobilie verkaufen")
    await page.keyboard.press("Escape"); await page.wait_for_timeout(300)
    ok("Mega Menu Close (Escape)", await page.locator(".flyout.is-open").count() == 0)
    await page.hover(".hdr__link:has-text('Unternehmen')"); await page.wait_for_timeout(400)
    await page.mouse.move(700, 880); await page.wait_for_timeout(500)
    ok("Mega Menu Close (Mouseleave)", await page.locator(".flyout.is-open").count() == 0)

    # Kaufen / Mieten / KI-Suche
    await page.click(".psearch__mode:has-text('Mieten')")
    ok("Buy/Rent Toggle", await page.locator(".psearch__mode.is-selected").inner_text() == "MIETEN"
       or (await page.locator(".psearch__mode.is-selected").inner_text()).lower() == "mieten")
    await page.click(".psearch__mode:has-text('Kaufen')")

    # Objektarten-Dropdown
    await page.click("button[aria-label='Dropdown-Menü für Objektarten']")
    ok("Property Type Dropdown öffnet", await page.locator(".psearch__types").is_visible())
    await page.click(".psearch__opt:has-text('Wohnung')")
    ok("Property Type Auswahl", await page.locator(".psearch__types").count() == 0)
    await page.click("button[aria-label='Dropdown-Menü für Objektarten']")
    ok("Property Type Auswahl gemerkt", await page.locator(".psearch__opt.is-selected").inner_text() == "Wohnung")
    await page.keyboard.press("Escape"); await page.mouse.click(200, 600)

    # Standort + Autocomplete + Clear
    inp = page.locator(".psearch__input")
    await inp.fill("Ess")
    ok("Location Input Autocomplete", await page.locator(".psearch__suggest li").count() > 0)
    await page.keyboard.press("ArrowDown"); await page.keyboard.press("Enter")
    ok("Autocomplete Auswahl per Tastatur", (await inp.input_value()).startswith("Essen"))
    await page.click(".psearch__clear")
    ok("Clear Action", await inp.input_value() == "")
    await inp.fill("Essen"); await page.click(".psearch__submit"); await page.wait_for_timeout(400)
    ok("Search Action → Ergebnisliste", "/immobilien/kaufen?ort=Essen" in page.url, page.url)
    ok("Ergebnisliste gefiltert", await page.locator(".pcard").count() > 0 and "Essen" in await page.locator(".srch__title").inner_text())
    await page.goto(LOCAL_URL); await page.wait_for_load_state("networkidle")
    await page.click(".psearch__mode:has-text('KI-Suche')")
    await page.locator(".psearch__input").fill("3 Zimmer Wohnung in Essen bis 300.000 €"); await page.click(".psearch__submit"); await page.wait_for_timeout(400)
    ok("KI-Suche → Filter", all(x in page.url for x in ("ort=Essen", "typ=Wohnung", "zimmer=3", "preis_max=300000")), page.url)
    await page.goto(LOCAL_URL); await page.wait_for_load_state("networkidle")

    # Slider
    sel = lambda: page.locator(".hcar__bar[aria-selected='true']").get_attribute("aria-label")
    first = await sel()
    await page.click(".hcar__bar >> nth=2"); await page.wait_for_timeout(800)
    ok("Hero Carousel: Slide-Wahl", (await sel()) != first and "Slide 3" in (await sel()))
    await page.click(".hcar__pause")
    ok("Carousel Pause", await page.locator(".hcar__pause[aria-label='Abspielen']").count() == 1)
    t1 = await page.locator(".hcar__bar[aria-selected='true'] .hcar__fill").get_attribute("style")
    await page.wait_for_timeout(600)
    t2 = await page.locator(".hcar__bar[aria-selected='true'] .hcar__fill").get_attribute("style")
    ok("Carousel bleibt pausiert", t1 == t2)
    await page.click(".hcar__pause")
    await page.focus(".hcar"); await page.keyboard.press("ArrowRight"); await page.wait_for_timeout(300)
    ok("Carousel Tastatur", "Slide 4" in (await sel()))

    # Sticky Header + Hero-Teaser
    await page.evaluate("window.scrollTo(0, 600)"); await page.wait_for_timeout(700)
    top = await page.evaluate("document.querySelector('.hdr').getBoundingClientRect().top")
    ok("Sticky Header (−72px)", abs(top + 72) <= 1, f"top={top}")
    op = await page.evaluate("getComputedStyle(document.querySelector('.hero__teasers')).opacity")
    ok("Hero-Teaser blenden beim Scrollen ein", float(op) > 0.95)

    # City Card Hover
    card = page.locator(".city >> nth=0")
    await card.scroll_into_view_if_needed(); await card.hover(); await page.wait_for_timeout(400)
    tr = await card.evaluate("e => getComputedStyle(e).transform")
    ok("City Card Hover", tr not in ("none", ""), tr)

    # Galerie
    await page.click(".gallery__open"); await page.wait_for_timeout(300)
    ok("Lifestyle Gallery öffnet", await page.locator(".lightbox").is_visible())
    await page.keyboard.press("ArrowRight")
    ok("Galerie Navigation", "2 / 6" in await page.locator(".lightbox__count").inner_text())
    await page.keyboard.press("Escape")
    ok("Galerie schließt", await page.locator(".lightbox").count() == 0)


    # Back to top
    await page.click(".ftr__top")
    for _ in range(40):
        if await page.evaluate("window.scrollY") < 5: break
        await page.wait_for_timeout(100)
    ok("Back to Top", await page.evaluate("window.scrollY") < 5)

    # Overflow, Bilder
    ow = await page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    ok("Kein horizontales Overflow (1440)", ow <= 0, f"{ow}px")
    broken = await page.evaluate("[...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src)")
    ok("Keine defekten Bilder", not broken, ", ".join(broken))
    ok("Keine Konsolenfehler", not errors, " | ".join(errors[:3]))
    ok("Keine 4xx/5xx-Requests", not bad, " | ".join(bad[:3]))
    await page.context.close()

async def mobile(b):
    page = await new_page(b, 390, 844, mobile=True)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    await page.goto(LOCAL_URL); await page.wait_for_load_state("networkidle")
    ok("Mobile Layout: Burger sichtbar, Nav versteckt", await page.locator(".hdr__burger").is_visible() and not await page.locator(".hdr__nav").is_visible())
    await page.click(".hdr__burger"); await page.wait_for_timeout(400)
    ok("Mobile Menu Open", await page.locator(".mnav.is-open").count() == 1)
    await page.click(".mnav__row >> nth=1"); await page.wait_for_timeout(450)
    ok("Mobile Untermenü", await page.locator(".mnav__track.is-sub").count() == 1)
    await page.click("button[aria-label='Zurück zum Hauptmenü']"); await page.wait_for_timeout(400)
    await page.keyboard.press("Escape"); await page.wait_for_timeout(400)
    ok("Mobile Menu Close", await page.locator(".mnav.is-open").count() == 0)

    # Swipe im Slider
    box = await page.locator(".hcar").bounding_box()
    sel0 = await page.locator(".hcar__bar[aria-selected='true']").get_attribute("aria-label")
    await page.mouse.move(box["x"] + 300, box["y"] + 150); await page.mouse.down()
    await page.mouse.move(box["x"] + 60, box["y"] + 150, steps=8); await page.mouse.up(); await page.wait_for_timeout(800)
    sel1 = await page.locator(".hcar__bar[aria-selected='true']").get_attribute("aria-label")
    ok("Touch Swipe", sel0 != sel1, f"{sel0} -> {sel1}")

    # Weitere Themen Mehr/Weniger
    first = page.locator(".topic >> nth=0")
    await first.scroll_into_view_if_needed()
    vis = lambda: first.locator(".topic__col--mobile li:not([hidden])").count()
    ok("Related Topics eingeklappt (3)", await vis() == 3)
    await first.locator(".topic__toggle").click()
    ok("Related Topics Expand", await vis() == 10)
    await first.locator(".topic__toggle").click()
    ok("Related Topics Collapse", await vis() == 3)

    # Footer-Akkordeon
    await page.click(".ftr__acc >> nth=0")
    ok("Footer Akkordeon", await page.locator(".ftr__col.is-open .ftr__list").is_visible())

    ow = await page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    ok("Kein horizontales Overflow (390)", ow <= 0, f"{ow}px")
    ok("Keine JS-Fehler (Mobile)", not errors, " | ".join(errors[:3]))
    await page.context.close()

async def subpages(b):
    page = await new_page(b, 1440, 900)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: m.type == "error" and errors.append(m.text))
    go = lambda path: page.goto(LOCAL_URL + path.lstrip("/"))

    # Navigation über Header und Mega-Menü
    await go("/"); await page.wait_for_load_state("networkidle")
    await page.click(".hdr__link:has-text('Immobilie verkaufen')"); await page.wait_for_timeout(400)
    ok("Navigation → Verkaufen", page.url.endswith("/verkaufen"), page.url)
    await page.mouse.move(700, 600); await page.wait_for_timeout(300)
    await page.hover(".hdr__link:has-text('Immobilie verkaufen')"); await page.wait_for_timeout(400)
    await page.click("#flyout-1 .flyout__link:has-text('Kostenlose Immobilienbewertung')"); await page.wait_for_timeout(400)
    ok("Mega-Menü-Link → Bewertung", page.url.endswith("/bewertung"), page.url)
    ok("Unterseite: Breadcrumb", await page.locator(".crumbs").count() == 1)
    ok("Unterseite: Footer-Akkordeon (Desktop)", await page.locator(".ftr--accordion .ftr__acc").first.is_visible())

    # Bewertungs-Funnel
    await page.click(".funnel__tile:has-text('Wohnung')")
    ok("Funnel: Schritt 2 (Wohnfläche)", await page.locator(".funnel__value").is_visible())
    await page.click(".funnel .chip:has-text('120 m²')"); await page.click(".funnel__next")
    await page.click(".funnel__tile:has-text('Verkaufen')"); await page.click(".funnel__next")
    ok("Funnel: Zusammenfassung", "Wohnung · ca. 120 m² Wohnfläche · Verkaufen" in await page.locator(".funnel__summary").inner_text())
    await page.click(".funnel .cform__submit button")
    ok("Funnel: Pflichtfelder", await page.locator(".funnel .cform__error").count() == 5)

    # Suche
    await go("/immobilien/kaufen"); await page.wait_for_load_state("networkidle")
    total = await page.locator(".pcard").count()
    ok("Suche: Ergebnisse", total >= 15, f"{total} Karten")
    await page.click(".fbtn:has-text('Objektart')"); await page.click(".fcheck:has-text('Wohnung') input"); await page.wait_for_timeout(300)
    flats = await page.locator(".pcard").count()
    ok("Suche: Filter Objektart", 0 < flats < total and "typ=Wohnung" in page.url, f"{flats} Wohnungen")
    await go("/immobilien/kaufen?anlage=1"); await page.wait_for_load_state("networkidle")
    badges = await page.locator(".pcard").evaluate_all("cs => cs.map(c => c.innerText.includes('KAPITALANLAGE') || c.innerText.includes('Kapitalanlage'))")
    ok("Suche: Filter Kapitalanlage", badges and all(badges), f"{len(badges)} Objekte")
    await go("/immobilien/kaufen?sort=preis_auf"); await page.wait_for_load_state("networkidle")
    prices = [p for p in await page.locator(".pcard__price").all_inner_texts() if "€" in p]
    nums = [int("".join(ch for ch in p if ch.isdigit())) for p in prices[:5]]
    ok("Suche: Sortierung Preis aufsteigend", nums == sorted(nums), str(nums))
    await page.click(".srch__map"); await page.wait_for_timeout(200)
    ok("Suche: Kartenansicht", await page.locator(".srch__mapview .srch__pin").count() > 3)
    await page.click(".fbar .btn--accent"); await page.wait_for_timeout(200)
    await page.select_option(".fsel select >> nth=0", "mieten"); await page.wait_for_timeout(400)
    ok("Suche: Wechsel Mieten", page.url.split("?")[0].endswith("/immobilien/mieten") and "mieten" in (await page.locator(".srch__title").inner_text()))

    # Exposé
    await go("/immobilien/kaufen"); await page.wait_for_load_state("networkidle")
    await page.locator(".pcard__link").first.click(); await page.wait_for_timeout(500)
    ok("Karte → Exposé", "/expose/" in page.url and await page.locator(".expo__title").count() == 1, page.url)
    ok("Exposé: echte Objektbeschreibung", len(await page.locator(".expo__copy").inner_text()) > 100)
    await page.click(".expo__img >> nth=0"); await page.wait_for_timeout(200)
    ok("Exposé: Galerie öffnet", await page.locator(".lightbox").is_visible())
    await page.keyboard.press("Escape")
    await page.click(".expo__action:has-text('Merken')")
    ok("Exposé: Merkliste", await page.locator(".expo__action[aria-pressed='true']").count() == 1)
    await page.locator("#anfrage .cform").scroll_into_view_if_needed()
    await page.click("#anfrage .cform__submit button")
    ok("Exposé: Formular-Validierung", await page.locator("#anfrage .cform__error").count() == 4)
    inputs = page.locator("#anfrage .cform__field input")
    await inputs.nth(0).fill("Max"); await inputs.nth(1).fill("Muster"); await inputs.nth(2).fill("max@example.com")
    await page.check("#anfrage .cform__consent input")
    await page.click("#anfrage .cform__submit button")
    href = await page.locator(".cform__done a[href^='mailto:']").get_attribute("href")
    ok("Exposé: Anfrage als E-Mail vorbereitet", bool(href) and "subject=Expos" in href and "max%40example.com" in href, (href or "")[:80])
    await go("/mein-bereich"); await page.wait_for_load_state("networkidle")
    ok("Mein Bereich: Merkliste + gespeicherte Suche", await page.locator(".pcard").count() == 1 and await page.locator(".saved li").count() == 1)

    # Rechner
    await go("/service/finanzierungsrechner"); await page.wait_for_load_state("networkidle")
    rate = await page.locator(".calc__result .calc__big").inner_text()
    ok("Finanzierungsrechner: Rate", "€" in rate, rate)
    await page.fill(".calc__field:has-text('Kaufpreis') input", "500000"); await page.wait_for_timeout(100)
    ok("Finanzierungsrechner: reagiert", await page.locator(".calc__result .calc__big").inner_text() != rate)
    await go("/service/budgetrechner"); await page.wait_for_load_state("networkidle")
    for _ in range(7):
        await page.click(".wizard form button[type=submit]")
    ok("Budgetrechner: Ergebnis", "kaufpreisrahmen" in (await page.locator(".wizard__result").inner_text()).lower())
    await go("/service/wert-hebel-rechner"); await page.wait_for_load_state("networkidle")
    for _ in range(3):
        await page.click(".wizard form button[type=submit]")
    ok("Wert-Hebel-Rechner: Maßnahmen", await page.locator(".calc__table tbody tr").count() >= 3)

    # Ratgeber, Immopedia, Regionen, Weiterleitungen
    await go("/ratgeber"); await page.wait_for_load_state("networkidle")
    await page.locator(".post").first.click(); await page.wait_for_timeout(400)
    ok("Ratgeber → Artikel", "/ratgeber/" in page.url and await page.locator(".toc li").count() >= 4, page.url)
    await go("/immopedia"); await page.wait_for_load_state("networkidle")
    await page.fill(".ipedia__search input", "Grundschuld"); await page.wait_for_timeout(200)
    ok("Immopedia: Suche", await page.locator(".ipedia__list li").count() > 0)
    await page.locator(".ipedia__list a").first.click(); await page.wait_for_load_state("networkidle")
    ok("Immopedia: Begriff", "/immopedia/" in page.url and len(await page.locator(".rich").first.inner_text()) > 200, page.url)
    await go("/regionen/muenster"); await page.wait_for_load_state("networkidle")
    await page.locator(".rich__faq .acc__btn").first.click()
    ok("Region: FAQ mit Antwort", len(await page.locator(".rich__faq .acc__item.is-open .acc__panel").inner_text()) > 40)
    for old, new in (("/standorte", "/regionen"), ("/stadt/essen", "/regionen/essen"), ("/magazin", "/ratgeber"), ("/commercial", "/kapitalanlage"), ("/makler-werden", "/ueber-uns")):
        await go(old); await page.wait_for_timeout(300)
        ok(f"Weiterleitung {old}", page.url.rstrip("/").endswith(new), page.url)
    await go("/datenschutz"); await page.wait_for_load_state("networkidle")
    txt = await page.locator("main").inner_text()
    ok("Datenschutz ohne fremde Daten", "Serhan" not in txt and "78050" not in txt and "Vimeo" not in txt)
    await page.click(".ftr__link:has-text('Cookie-Einstellungen')"); await page.wait_for_timeout(200)
    ok("Cookie-Einstellungen öffnen", await page.locator(".cookies").is_visible())
    await page.keyboard.press("Escape")
    await go("/gibt-es-nicht"); await page.wait_for_load_state("networkidle")
    ok("404-Seite", "gibt es nicht" in await page.locator("main").inner_text())
    ok("Unterseiten: keine JS-/Konsolenfehler", not errors, " | ".join(errors[:3]))
    await page.context.close()

    # Overflow ausgewählter Seiten (Mobile + Tablet); vollständige Prüfung: scripts/check_links.py
    worst = []
    for path in ("immobilien/kaufen", "expose/170744873", "verkaufen", "bewertung", "leistungen", "service/finanzierungsrechner", "ratgeber", "immopedia", "regionen/bochum", "kontakt"):
        for w in (360, 768):
            pg = await new_page(b, w, 900, mobile=w < 768)
            await pg.goto(LOCAL_URL + path); await pg.wait_for_load_state("networkidle")
            ow = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if ow > 0: worst.append(f"{path}@{w}:+{ow}")
            await pg.context.close()
    ok("Unterseiten: kein Overflow (360/768)", not worst, ", ".join(worst))

async def contact_widget(b):
    """Kontakt-Pop-up (Desktop), Kontaktleiste (Handy), WhatsApp, Partner, Rechtstexte, lokale Strukturdaten"""
    page = await new_page(b, 1440, 900)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    await page.goto(LOCAL_URL); await page.wait_for_load_state("networkidle")
    ok("Widget: oben ausgeblendet", await page.locator(".cw-trigger.is-visible").count() == 0)
    await page.mouse.wheel(0, 1500); await page.wait_for_timeout(600)
    ok("Widget: erscheint nach Scrollen", await page.locator(".cw-trigger.is-visible").count() == 1)
    ok("Widget: Hinweis „Kostenlose Erstberatung“", await page.locator(".cw-trigger__hint").is_visible())
    await page.click(".cw-trigger__x"); await page.wait_for_timeout(200)
    ok("Widget: Hinweis schließbar", await page.locator(".cw-trigger__hint").count() == 0)
    await page.click(".cw-trigger__btn"); await page.wait_for_timeout(400)
    ok("Widget: Panel öffnet", await page.locator(".cw.is-open").count() == 1)
    await page.click(".cw__submit"); await page.wait_for_timeout(150)
    ok("Widget: Pflichtfelder geprüft", await page.locator(".cw__field.has-error").count() >= 2)
    await page.fill(".cw__body input[autocomplete=name]", "Erika Muster")
    await page.fill(".cw__body input[type=email]", "erika@example.org")
    await page.select_option(".cw__body select", "Immobilie verkaufen")
    await page.click(".cw__submit"); await page.wait_for_timeout(150)
    href = await page.get_attribute(".cw__done a.btn--accent", "href") or ""
    ok("Widget: Anfrage → vorbereitete E-Mail", href.startswith("mailto:") and "Immobilie%20verkaufen" in href)
    await page.click(".cw__tabs button:has-text('Rückruf')"); await page.wait_for_timeout(150)
    await page.click(".cw__submit"); await page.wait_for_timeout(150)
    ok("Widget: Rückruf verlangt Telefonnummer", await page.locator(".cw__field.has-error input[type=tel]").count() == 1)
    await page.click(".cw__tabs button:has-text('Anrufen')"); await page.wait_for_timeout(150)
    ok("Widget: Anrufen-Link", await page.locator(".cw__call a[href='tel:+4925128429090']").count() == 1)
    await page.click(".cw__tabs button:has-text('WhatsApp')"); await page.wait_for_timeout(150)
    ok("Widget: WhatsApp-Formular", await page.locator(".cw__wa").is_visible())
    await page.keyboard.press("Escape"); await page.wait_for_timeout(350)
    ok("Widget: Escape schließt", await page.locator(".cw.is-open").count() == 0)
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)"); await page.wait_for_timeout(500)
    ok("Widget: am Seitenende ausgeblendet (Footer-Links frei)", await page.locator(".cw-trigger.is-visible").count() == 0)
    ok("Footer: WhatsApp-Icon", await page.locator(".ftr a[href*='wa.me/4925128429090']").count() >= 1)
    ok("Footer: 3 Kooperationspartner verlinkt", await page.locator(".ftr__partners a[target=_blank]").count() == 3)
    ok("Desktop: keine Kontaktleiste", not await page.locator(".cw-bar").is_visible())
    ok("Widget: keine JS-Fehler", not errors, " | ".join(errors[:3]))
    await page.context.close()

    page = await new_page(b, 390, 844, mobile=True)
    await page.goto(LOCAL_URL); await page.wait_for_load_state("networkidle")
    bar = page.locator(".cw-bar")
    ok("Mobile: Kontaktleiste sichtbar", await bar.is_visible())
    ok("Mobile: Anrufen + WhatsApp", await bar.locator("a[href='tel:+4925128429090']").count() == 1 and await bar.locator("a[href*='wa.me/4925128429090']").count() == 1)
    pad = await page.evaluate("parseFloat(getComputedStyle(document.body).paddingBottom)")
    ok("Mobile: Footer wird nicht verdeckt", pad >= 56, f"{pad}px")
    await bar.locator("button").click(); await page.wait_for_timeout(400)
    ok("Mobile: Beratung öffnet Pop-up", await page.locator(".cw.is-open").count() == 1)
    ow = await page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    ok("Mobile: Pop-up ohne Overflow", ow <= 0, f"+{ow}")
    await page.context.close()

    page = await new_page(b, 1440, 900)
    async def go(path):
        await page.goto(LOCAL_URL + path); await page.wait_for_load_state("networkidle")
    await go("expose/170744873")
    ok("Exposé: WhatsApp mit Objektnummer", await page.locator(".expo__agent-wa[href*='170744873']").count() == 1)
    await go("kontakt")
    ok("Kontakt: WhatsApp", await page.locator("main a[href*='wa.me/']").count() >= 1)
    await go("ueber-uns")
    ok("Über uns: Partner & Kooperationen", await page.locator("#partner .partners__logo, #partner img").count() >= 8)
    await go("datenschutz")
    ok("Datenschutz: WhatsApp-Abschnitt", "Kontakt per WhatsApp" in await page.locator("main").inner_text())
    await go("impressum")
    txt = await page.locator("main").inner_text()
    ok("Impressum: kein veralteter ODR-Hinweis, Schlichtungsstelle vorhanden", "consumers/odr" not in txt and "Schlichtungsstelle" in txt)
    for city in ("muenster", "essen", "bochum"):
        await go(f"regionen/{city}")
        ld = await page.evaluate("document.getElementById('ld-page')?.textContent || ''")
        ok(f"GEO: Service-Strukturdaten {city}", '"@type":"Service"' in ld and '"areaServed"' in ld)
    r = await page.request.get(LOCAL_URL + "llms.txt")
    ok("GEO: llms.txt erreichbar", r.ok and "Oberholz Immobilien" in await r.text())
    await page.context.close()

async def overflow_sweep(b):
    widths = [320, 360, 375, 430, 480, 600, 768, 900, 1024, 1200, 1366, 1600, 1920]
    worst = []
    for w in widths:
        page = await new_page(b, w, 900, mobile=w < 768)
        await page.goto(LOCAL_URL); await page.wait_for_load_state("networkidle")
        ow = await page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        if ow > 0: worst.append(f"{w}px:+{ow}")
        await page.context.close()
    ok("Kein Overflow 320–1920px", not worst, ", ".join(worst))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        await desktop(b); await mobile(b); await overflow_sweep(b); await subpages(b); await contact_widget(b)
        await b.close()
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} Tests bestanden")
    sys.exit(1 if failed else 0)

asyncio.run(main())
