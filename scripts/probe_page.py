"""First-pass public homepage probe. No tracking replay, no form submit."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis"
URL = "https://www.immobilien-experten.de/"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="de-DE",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()
        requests = []

        def on_request(req):
            requests.append(
                {
                    "url": req.url,
                    "method": req.method,
                    "resource_type": req.resource_type,
                }
            )

        page.on("request", on_request)
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(2500)

        # Dismiss common cookie banners without inventing consent storage.
        for selector in [
            "button:has-text('Alle akzeptieren')",
            "button:has-text('Akzeptieren')",
            "button:has-text('Zustimmen')",
            "button:has-text('Alle Cookies akzeptieren')",
            "#uc-btn-accept-banner",
            ".cmplz-accept",
            "[data-action='accept']",
        ]:
            loc = page.locator(selector)
            if loc.count() > 0:
                try:
                    loc.first.click(timeout=2000)
                    page.wait_for_timeout(500)
                    break
                except Exception:
                    pass

        page.wait_for_timeout(1500)
        try:
            page.evaluate("() => document.fonts.ready")
        except Exception:
            pass

        data = page.evaluate(
            """() => {
              const text = (el) => (el.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 400);
              const box = (el) => {
                const r = el.getBoundingClientRect();
                return { x: Math.round(r.x), y: Math.round(r.y + window.scrollY), w: Math.round(r.width), h: Math.round(r.height) };
              };
              const headings = [...document.querySelectorAll('h1,h2,h3,h4')].slice(0, 80).map(el => ({
                tag: el.tagName,
                className: el.className,
                text: text(el),
                box: box(el),
              }));
              const sections = [...document.querySelectorAll('header, nav, main, section, footer, form')].slice(0, 80).map(el => ({
                tag: el.tagName,
                id: el.id,
                className: String(el.className).slice(0, 200),
                text: text(el).slice(0, 180),
                box: box(el),
              }));
              const links = [...document.querySelectorAll('a')].slice(0, 200).map(a => ({
                text: text(a).slice(0, 80),
                href: a.getAttribute('href'),
              }));
              const buttons = [...document.querySelectorAll('button')].slice(0, 80).map(b => ({
                text: text(b).slice(0, 80),
                className: String(b.className).slice(0, 120),
                type: b.getAttribute('type'),
              }));
              const imgs = [...document.querySelectorAll('img')].map(img => ({
                src: img.currentSrc || img.src,
                alt: img.alt,
                w: img.naturalWidth,
                h: img.naturalHeight,
                className: String(img.className).slice(0, 80),
              }));
              const stylesheets = [...document.querySelectorAll('link[rel="stylesheet"]')].map(l => l.href);
              const scripts = [...document.querySelectorAll('script[src]')].map(s => s.src);
              const vars = {};
              const cs = getComputedStyle(document.documentElement);
              for (const sheet of document.styleSheets) {
                let rules;
                try { rules = sheet.cssRules; } catch (e) { continue; }
                if (!rules) continue;
                for (const rule of rules) {
                  if (rule.selectorText === ':root' || rule.selectorText === 'html') {
                    for (const prop of rule.style) {
                      if (prop.startsWith('--')) vars[prop] = rule.style.getPropertyValue(prop).trim();
                    }
                  }
                }
              }
              const fonts = [];
              for (const sheet of document.styleSheets) {
                let rules;
                try { rules = sheet.cssRules; } catch (e) { continue; }
                if (!rules) continue;
                for (const rule of rules) {
                  if (rule instanceof CSSFontFaceRule) {
                    fonts.push({
                      family: rule.style.getPropertyValue('font-family'),
                      weight: rule.style.getPropertyValue('font-weight'),
                      style: rule.style.getPropertyValue('font-style'),
                      src: rule.style.getPropertyValue('src').slice(0, 500),
                    });
                  }
                }
              }
              const bodyStyle = getComputedStyle(document.body);
              return {
                title: document.title,
                htmlClass: document.documentElement.className,
                bodyClass: document.body.className,
                scrollHeight: document.documentElement.scrollHeight,
                bodyFont: bodyStyle.fontFamily,
                bodySize: bodyStyle.fontSize,
                bodyColor: bodyStyle.color,
                bodyBg: bodyStyle.backgroundColor,
                headings,
                sections,
                links,
                buttons,
                imgs,
                stylesheets,
                scripts,
                vars,
                fonts,
                generator: document.querySelector('meta[name="generator"]')?.content || null,
              };
            }"""
        )
        data["request_count"] = len(requests)
        data["request_types"] = {}
        for req in requests:
            data["request_types"][req["resource_type"]] = data["request_types"].get(req["resource_type"], 0) + 1

        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "probe.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        (OUT / "probe_requests.json").write_text(json.dumps(requests, ensure_ascii=False, indent=2), encoding="utf-8")
        page.screenshot(path=str(ROOT / "reference" / "probe-1440.png"), full_page=True)
        print("title:", data["title"])
        print("scrollHeight:", data["scrollHeight"])
        print("generator:", data["generator"])
        print("stylesheets:", len(data["stylesheets"]))
        print("fonts:", len(data["fonts"]))
        print("vars:", len(data["vars"]))
        print("imgs:", len(data["imgs"]))
        print("sections:", len(data["sections"]))
        print("headings:", len(data["headings"]))
        browser.close()


if __name__ == "__main__":
    main()
