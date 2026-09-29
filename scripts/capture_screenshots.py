"""Capture original and local screenshots at the required viewports."""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = "https://www.immobilien-experten.de/"
LOCAL = "http://127.0.0.1:5173/"

VIEWPORTS = [
    ("1920x1080", 1920, 1080),
    ("1440x900", 1440, 900),
    ("1366x768", 1366, 768),
    ("1024x1366", 1024, 1366),
    ("768x1024", 768, 1024),
    ("430x932", 430, 932),
    ("390x844", 390, 844),
    ("375x812", 375, 812),
]

SECTIONS = {
    "header": "header.main-header",
    "hero": "section.regio-hero",
    "service360": "section.hotspots",
    "form": "#iwf",
    "energy": "section.py-5",
    "comparison": "section.bg-light",
    "process": "section.py-5",
    "properties": "section.bg-light",
    "logos": "section.bg-white.pt-4",
    "downloads": "section.py-5",
    "footer": "footer.footer",
}


def freeze(page: Page) -> None:
    page.evaluate(
        """() => {
          const first = (sel) => {
            const nodes = [...document.querySelectorAll(sel)];
            if (!nodes.length) return;
            nodes.forEach((el) => el.classList.remove('is-active'));
            nodes[0].classList.add('is-active');
          };
          first('.regio-rotor-slide');
          first('.regio-rotor-flag');
          first('.ocv-rotor__item');
          const style = document.createElement('style');
          style.textContent = '*,*::before,*::after{animation:none !important;transition:none !important;}';
          document.head.appendChild(style);
        }"""
    )


def settle(page: Page) -> None:
    page.wait_for_timeout(600)
    page.evaluate(
        """async () => {
          const height = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
          for (let y = 0; y < height; y += 800) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 80));
          }
          window.scrollTo(0, 0);
          if (document.fonts && document.fonts.ready) await document.fonts.ready;
          const images = [...document.images];
          await Promise.race([
            Promise.all(images.map(img => img.complete ? Promise.resolve() : new Promise(res => {
              img.addEventListener('load', res, { once: true });
              img.addEventListener('error', res, { once: true });
            }))),
            new Promise(res => setTimeout(res, 5000))
          ]);
        }"""
    )
    page.wait_for_timeout(250)
    freeze(page)
    page.wait_for_timeout(150)


def dismiss(page: Page) -> None:
    for selector in [
        "button:has-text('Alle akzeptieren')",
        "button:has-text('Akzeptieren')",
        "button:has-text('Zustimmen')",
        "#uc-btn-accept-banner",
    ]:
        loc = page.locator(selector)
        if loc.count():
            try:
                loc.first.click(timeout=1500)
                page.wait_for_timeout(300)
                return
            except Exception:
                pass


def shoot(page: Page, folder: Path, label: str, sections: bool) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(folder / f"{label}-full.png"), full_page=True)
    geometry = page.evaluate(
        """() => {
          const pick = (sel) => {
            const el = document.querySelector(sel);
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return { x: Math.round(r.x), y: Math.round(r.y + window.scrollY), width: Math.round(r.width), height: Math.round(r.height) };
          };
          return {
            scrollHeight: document.documentElement.scrollHeight,
            header: pick('header.main-header'),
            hero: pick('section.regio-hero'),
            service360: pick('section.hotspots'),
            form: pick('#iwf'),
            footer: pick('footer.footer'),
          };
        }"""
    )
    if sections:
        for name, selector in {
            "header": "header.main-header",
            "hero": "section.regio-hero",
            "service360": "section.hotspots",
            "form": "#iwf",
            "footer": "footer.footer",
        }.items():
            loc = page.locator(selector).first
            if loc.count():
                try:
                    loc.screenshot(path=str(folder / f"{label}-{name}.png"))
                except Exception as exc:
                    print("section fail", name, exc)
    return geometry


def run(target: str, out_root: Path) -> None:
    geometries = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for label, width, height in VIEWPORTS:
            page = browser.new_page(viewport={"width": width, "height": height}, locale="de-DE")
            page.goto(target, wait_until="domcontentloaded", timeout=120000)
            dismiss(page)
            settle(page)
            folder = out_root / label
            geometries[label] = shoot(page, folder, label, sections=(label == "1440x900"))
            print(label, geometries[label]["scrollHeight"], flush=True)
            page.close()
        browser.close()
    (out_root / "geometry.json").write_text(json.dumps(geometries, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import sys

    which = sys.argv[1] if len(sys.argv) > 1 else "local"
    if which == "original":
        run(ORIGINAL, ROOT / "reference")
    else:
        run(LOCAL, ROOT / "screenshots" / "local")
