import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900}, locale="de-DE")
    leaks = []
    page.on(
        "request",
        lambda req: leaks.append(req.url)
        if ("immobilien-experten" in req.url or "rex-api" in req.url)
        else None,
    )
    page.goto("http://127.0.0.1:5173/", wait_until="domcontentloaded", timeout=60000)
    page.locator("#iwf .iwf-step.is-active .iwf-choice", has_text="Sonstiges").click(force=True)
    page.wait_for_timeout(400)
    page.locator("#iwf .iwf-step.is-active input[type=checkbox]").first.evaluate(
        "el => { el.checked = true; }"
    )
    page.locator("#iwf .iwf-step.is-active .iwf-weiter-plain").click(force=True)
    page.wait_for_timeout(300)
    page.fill("#iwf-name", "Max Beispiel")
    page.fill("#iwf-ort", "70173 Stuttgart")
    page.fill("#iwf-telefon", "0711123456")
    page.fill("#iwf-email", "max@example.com")
    page.locator("#iwf input[name=dsgvo]").evaluate("el => { el.checked = true; }")
    page.locator("#iwf button[type=submit]").click(force=True)
    page.wait_for_timeout(400)
    print(page.locator("#iwf-local-success").inner_text())
    print("url", page.url)
    print("leaks", leaks)
    styles = page.evaluate(
        """() => {
          const keys = ['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','color','backgroundColor','padding','margin','borderRadius','boxShadow','width','height','display'];
          const sel = ['body','h1','header.main-header','section.regio-hero','.iwf-card','footer.footer'];
          const out = {};
          for (const s of sel) {
            const el = document.querySelector(s);
            if (!el) continue;
            const cs = getComputedStyle(el);
            const box = el.getBoundingClientRect();
            out[s] = {};
            for (const k of keys) out[s][k] = cs[k];
            out[s].box = { x: Math.round(box.x), y: Math.round(box.y + scrollY), w: Math.round(box.width), h: Math.round(box.height) };
          }
          const root = getComputedStyle(document.documentElement);
          out.variables = {};
          for (const name of ['--primary-color','--secondary-color','--title-color','--primary-font','--secondary-font','--gray']) {
            out.variables[name] = root.getPropertyValue(name).trim();
          }
          return out;
        }"""
    )
    (ROOT / "analysis" / "styles.json").write_text(json.dumps(styles, ensure_ascii=False, indent=2), encoding="utf-8")
    browser.close()
