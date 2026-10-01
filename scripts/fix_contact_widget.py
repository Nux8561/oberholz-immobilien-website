#!/usr/bin/env python3
"""Replace broken local contact stub with real multi-option panel."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOCAL_PANEL_HTML = (
    '<div id="cw-local-overlay" onclick="if(event.target===this){window.cwClose&&window.cwClose();}">'
    '<div class="cw-local-panel" role="dialog" aria-modal="true" aria-label="Kontakt">'
    '<button type="button" class="cw-local-close" aria-label="Schließen" '
    'onclick="window.cwClose&&window.cwClose();">&times;</button>'
    "<h3>Kostenlose Erstberatung</h3>"
    "<p>Wie möchten Sie uns erreichen?</p>"
    '<div class="cw-local-actions">'
    '<a href="tel:+4925128429090"><span class="cw-ico"><i class="fa fa-phone"></i></span> Anrufen</a>'
    '<a href="mailto:mail@oberholz-immobilien.com?subject=Kontaktanfrage%20Oberholz%20Immobilien">'
    '<span class="cw-ico"><i class="fa fa-envelope"></i></span> E-Mail schreiben</a>'
    '<a class="cw-secondary" href="/kontakt/kontakt-aufnehmen.html">'
    '<span class="cw-ico"><i class="fa fa-calendar"></i></span> Termin / Kontaktformular</a>'
    "</div></div></div>"
)

OLD_STUB_RE = re.compile(
    r"Promise\.resolve\(\{\s*text:\s*function\s*\(\)\s*\{\s*return\s*Promise\.resolve\("
    r"'[^']*Lokale Ansicht[^']*'\)\s*;\s*\}\s*\}\)",
    re.S,
)

NEW_STUB = (
    "Promise.resolve({ text: function () { return Promise.resolve('"
    + LOCAL_PANEL_HTML.replace("\\", "\\\\").replace("'", "\\'")
    + "'); } })"
)

CW_OPEN_BOOTSTRAP = (
    "window.cwOpen=function(pane){var o=document.getElementById('cw-local-overlay');"
    "if(!o)return;o.classList.add('cw-open');document.documentElement.style.overflow='hidden';"
    "var b=o.querySelector('.cw-local-close');if(b)b.focus();};"
    "window.cwClose=function(){var o=document.getElementById('cw-local-overlay');"
    "if(!o)return;o.classList.remove('cw-open');document.documentElement.style.overflow='';};"
    "document.addEventListener('keydown',function(e){if(e.key==='Escape'&&window.cwClose)window.cwClose();});"
)

HINT_FIX = (
    "(function(){"
    "var trigger=document.getElementById('cw-trigger');"
    "var hint=document.getElementById('cw-trigger-hint');"
    "var hintClose=document.getElementById('cw-trigger-hint-close');"
    "if(!trigger)return;"
    "function cwDismissHint(e){"
    "if(e){e.preventDefault();e.stopPropagation();}"
    "if(hint)hint.classList.remove('show');"
    "trigger.classList.remove('cw-trigger-pulse');"
    "var expires=new Date(Date.now()+7*24*60*60*1000).toUTCString();"
    "document.cookie='cw_hint_closed=1; path=/; expires='+expires+'; SameSite=Lax';"
    "}"
    "if(hintClose){"
    "hintClose.textContent='\u00d7';"
    "hintClose.addEventListener('click',cwDismissHint);"
    "hintClose.addEventListener('touchend',cwDismissHint,{passive:false});"
    "}"
    "if(document.cookie.indexOf('cw_hint_closed=1')!==-1){"
    "if(hint)hint.classList.remove('show');return;"
    "}"
    "trigger.classList.add('cw-trigger-hidden');"
    "var fired=false;"
    "function onScroll(){"
    "if(fired||window.scrollY<80)return;"
    "fired=true;window.removeEventListener('scroll',onScroll);"
    "trigger.classList.remove('cw-trigger-hidden');"
    "trigger.classList.add('cw-trigger-slide-in');"
    "trigger.addEventListener('animationend',function onSlideEnd(){"
    "trigger.removeEventListener('animationend',onSlideEnd);"
    "trigger.classList.remove('cw-trigger-slide-in');"
    "trigger.classList.add('cw-trigger-pulse');"
    "if(hint)hint.classList.add('show');"
    "});"
    "}"
    "window.addEventListener('scroll',onScroll,{passive:true});"
    "}());"
)

HINT_IIFE_RE = re.compile(
    r"\(function\s*\(\)\s*\{\s*var trigger = document\.getElementById\('cw-trigger'\);[\s\S]*?"
    r"window\.addEventListener\('scroll',\s*onScroll,\s*\{\s*passive:\s*true\s*\}\);\s*\}\(\)\);",
    re.I,
)

CSS_LINK = '<link rel="stylesheet" href="/theme/oberholz-contact-widget.css"/>'


def process(html: str) -> str:
    if "oberholz-contact-widget.css" not in html:
        html = html.replace("</head>", CSS_LINK + "\n</head>", 1)

    html, n = OLD_STUB_RE.subn(NEW_STUB, html)
    if not n and "Lokale Ansicht" in html:
        # broader fallback
        html = re.sub(
            r"Promise\.resolve\(\{[^}]*Lokale Ansicht[^}]*\}\)",
            NEW_STUB,
            html,
            count=1,
            flags=re.S,
        )

    if "window.cwClose" not in html:
        html = html.replace(
            "window.cwTriggerClick = cwTriggerClick;",
            CW_OPEN_BOOTSTRAP + "window.cwTriggerClick = cwTriggerClick;",
            1,
        )

    html, n = HINT_IIFE_RE.subn(lambda _m: "/* Trigger-Animation */" + HINT_FIX, html)

    html = html.replace('class="show" id="cw-trigger-hint"', 'class="" id="cw-trigger-hint"')
    html = html.replace('id="cw-trigger-hint" class="show"', 'id="cw-trigger-hint" class=""')
    html = re.sub(
        r'(id="cw-trigger-hint-close"[^>]*>)([^<]*)(</button>)',
        lambda m: m.group(1) + "\u00d7" + m.group(3),
        html,
        count=1,
    )
    return html


def collect() -> list[Path]:
    files = [ROOT / "index.html"]
    for folder in [
        ROOT / "public",
        ROOT / "public" / "leistungen",
        ROOT / "public" / "ueber-uns",
        ROOT / "public" / "service",
        ROOT / "public" / "ratgeber",
        ROOT / "public" / "kontakt",
    ]:
        files.extend(folder.glob("*.html"))
    return sorted({p for p in files if p.is_file()})


def main() -> None:
    changed = 0
    for path in collect():
        original = path.read_text(encoding="utf-8", errors="replace")
        if "cwTriggerClick" not in original and "Lokale Ansicht" not in original:
            continue
        html = process(original)
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
    print(f"Done. Changed {changed}")


if __name__ == "__main__":
    main()
