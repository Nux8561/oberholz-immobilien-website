"""Save rendered public HTML and locate where layout CSS lives."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = "https://www.immobilien-experten.de/"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, locale="de-DE")
        page.goto(URL, wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(1500)
        info = page.evaluate(
            """() => {
              const styles = [...document.querySelectorAll('style')].map((s, i) => ({
                i,
                len: (s.textContent || '').length,
                start: (s.textContent || '').slice(0, 120),
              }));
              const links = [...document.querySelectorAll('link')].map(l => ({
                rel: l.rel,
                href: l.href,
                as: l.as || null,
              }));
              const inlineCount = styles.reduce((a, s) => a + s.len, 0);
              return {
                styles,
                links,
                inlineCount,
                htmlLen: document.documentElement.outerHTML.length,
              };
            }"""
        )
        html = page.content()
        (ROOT / "analysis" / "rendered.html").write_text(html, encoding="utf-8")
        (ROOT / "analysis" / "head_meta.json").write_text(
            json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print("html", len(html), "inline", info["inlineCount"], "styles", len(info["styles"]), "links", len(info["links"]))
        browser.close()


if __name__ == "__main__":
    main()
