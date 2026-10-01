#!/usr/bin/env python3
"""Wire pages to the restored original contact widget (not the stub panel)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Any Promise.resolve stub (Lokale Ansicht OR cw-local-overlay) → real fetch
STUB_RE = re.compile(
    r"Promise\.resolve\(\{\s*text:\s*function\s*\(\)\s*\{\s*return\s*Promise\.resolve\("
    r"(?:'[^']*'|\"[^\"]*\")"
    r"\)\s*;\s*\}\s*\}\)",
    re.S,
)

REAL_FETCH = "fetch('/theme/contact-widget.html')"

# Also catch older fetch to rex-api if still present
REX_FETCH_RE = re.compile(
    r"fetch\(['\"]/index\.php\?rex-api-call=contact_widget['\"]\s*,\s*\{\s*method:\s*'POST'\s*,\s*body:\s*formData\s*\}\)"
)

OVERRIDE_LINK = '<script src="/theme/oberholz-contact-override.js" defer></script>'
CSS_LOCAL = '<link rel="stylesheet" href="/theme/oberholz-contact-widget.css"/>'
CSS_LOCAL_ALT = '<link rel="stylesheet" href="/theme/oberholz-contact-widget.css" />'

# Bootstrap that conflicts with original cwOpen from widget HTML
BOOTSTRAP_RE = re.compile(
    r"window\.cwOpen=function\(pane\)\{var o=document\.getElementById\('cw-local-overlay'\);[\s\S]*?"
    r"document\.addEventListener\('keydown',function\(e\)\{if\(e\.key==='Escape'&&window\.cwClose\)window\.cwClose\(\);\}\);",
)

HINT_IIFE_RE = re.compile(
    r"/\*\s*Trigger-Animation\s*\*/\s*\(function\s*\(\)\s*\{[\s\S]*?\}\(\)\);|"
    r"\(function\s*\(\)\s*\{\s*var trigger = document\.getElementById\('cw-trigger'\);[\s\S]*?"
    r"window\.addEventListener\('scroll',\s*onScroll,\s*\{\s*passive:\s*true\s*\}\);\s*\}\(\)\);",
    re.I,
)

# Original-style hint animation (single pulse ring only while hint visible)
HINT_FIX = (
    "/* Trigger-Animation */(function(){"
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
    "if(hint)hint.classList.remove('show');"
    "trigger.classList.remove('cw-trigger-pulse');"
    "return;"
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


def process(html: str) -> str:
    # Remove broken custom overlay assets
    html = html.replace(OVERRIDE_LINK, "")
    html = html.replace(CSS_LOCAL, "")
    html = html.replace(CSS_LOCAL_ALT, "")

    # Remove conflicting cwOpen bootstrap for local overlay
    html = BOOTSTRAP_RE.sub("", html)

    # Replace stub / rex fetch with real static widget HTML
    html, n1 = STUB_RE.subn(REAL_FETCH, html)
    html, n2 = REX_FETCH_RE.subn(REAL_FETCH, html)
    if n1 + n2 == 0 and "contact-widget.html" not in html and "cwTriggerClick" in html:
        # last-resort: if somehow still Promise.resolve near contact widget
        html = re.sub(
            r"Promise\.resolve\(\{[\s\S]{0,4000}?cw-local-(?:overlay|panel)[\s\S]{0,500}?\}\)",
            REAL_FETCH,
            html,
            count=1,
        )

    # Restore hint dismissal + stop pulse when closed (avoid permanent double rings)
    html, n_hint = HINT_IIFE_RE.subn(HINT_FIX, html)
    if n_hint == 0 and "cw-trigger-hint" in html and "cwDismissHint" not in html:
        # append before closing body if animation block missing
        pass

    html = html.replace('class="show" id="cw-trigger-hint"', 'class="" id="cw-trigger-hint"')
    html = html.replace('id="cw-trigger-hint" class="show"', 'id="cw-trigger-hint" class=""')

    # Ensure trigger uses Oberholz avatar, not foreign pages.dev faces
    html = re.sub(
        r'(id="cw-trigger"[^>]*>\s*<img[^>]*src=")[^"]+(")',
        r'\1/media/videocard_avatar/oberholz_facepile.jpg\2',
        html,
        count=1,
    )
    html = re.sub(
        r'(id="cw-trigger"[^>]*>\s*<img[^>]*alt=")[^"]+(")',
        r'\1Michael Oberholz\2',
        html,
        count=1,
    )

    return html


def collect() -> list[Path]:
    files: list[Path] = [ROOT / "index.html"]
    for folder in [
        ROOT / "public",
        ROOT / "public" / "leistungen",
        ROOT / "public" / "ueber-uns",
        ROOT / "public" / "service",
        ROOT / "public" / "ratgeber",
        ROOT / "public" / "kontakt",
        ROOT / "public" / "immobilien",
    ]:
        if folder.is_dir():
            files.extend(folder.glob("*.html"))
            files.extend(folder.glob("*/*.html"))
    # regionen are many — only those with contact widget
    regio = ROOT / "public" / "regionen"
    if regio.is_dir():
        for p in regio.rglob("*.html"):
            files.append(p)
    return sorted({p for p in files if p.is_file()})


def main() -> None:
    changed = 0
    scanned = 0
    for path in collect():
        original = path.read_text(encoding="utf-8", errors="replace")
        if "cwTriggerClick" not in original and "cw-trigger" not in original:
            continue
        scanned += 1
        html = process(original)
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
    print(f"Done. scanned={scanned} changed={changed}")


if __name__ == "__main__":
    main()
