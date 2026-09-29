"""Rebrand mirrored HTML from Immobilien Experten to Oberholz Immobilien."""

from __future__ import annotations

import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BRAND_NEW = "Oberholz Immobilien"
EMAIL_NEW = "mail@oberholz-immobilien.com"
DOMAIN_NEW = "oberholz-immobilien.com"
PHONE_DISPLAY = "0251 28 42 90 90"
PHONE_TEL = "+4925128429090"
PHONE_TEL_LOCAL = "025128429090"

# Quick binary prefilter – skip already clean pages without full decode.
NEEDLES = (
    b"ie_logo.svg",
    b"Immobilien Experten",
    b"Immobilienexperten",
    b"Immobilienexperte",
    b"Immobilien%20Experten",
    b"info@immobilien-experten.de",
    b"immobilien-experten.de",
    b"0800 - 220 33 30",
    b"0800-220 33 30",
    b"08002203330",
    b"0151 23456789",
    b"0173-2157655",
    b"0173-2149122",
    b"0174-7793694",
    b"07721 - 29 69 240",
    b"0211-54598822",
    b"01522-4595678",
    b"0911 131 327 00",
    b"040 - 741 230 655",
    b"0511-999 889 54",
    b"0711-769 772 70",
    b"069 363 935 920",
    b"089 250 071 200",
    b"tel:+498002203330",
    b"tel://+498002203330",
    b"tel:08002203330",
    b"Logo Immobilien Experten",
)

# Any non-Oberholz tel: link still needs patching
TEL_ANY_RE = re.compile(rb'href="tel:(?://)?\+?[0-9]+"', re.IGNORECASE)
OBERHOLZ_TEL_MARKERS = (b"+4925128429090", b"025128429090")

LOGO_REPLACEMENTS = (
    (
        '<img src="/media/ie_logo.svg" width="200" height="54" alt="Logo Immobilien Experten" class="d-block d-md-none" fetchpriority="high">',
        '<img src="/media/oberholz-logo.png" width="200" height="92" alt="Oberholz Immobilien" class="d-block d-md-none" fetchpriority="high">',
    ),
    (
        '<img src="/media/ie_logo.svg" width="200" height="54" alt="Logo Immobilien Experten" class="d-none d-md-block" fetchpriority="high">',
        '<img src="/media/oberholz-logo.png" width="200" height="92" alt="Oberholz Immobilien" class="d-none d-md-block" fetchpriority="high">',
    ),
    (
        '<img src="/media/ie_logo.svg" alt="Logo Immobilien Experten" class="img-fluid" width="200" loading="lazy">',
        '<img src="/media/oberholz-logo.png" alt="Oberholz Immobilien" class="img-fluid" width="200" loading="lazy">',
    ),
    (
        '<img src="/media/ie_logo.svg" width="300" alt="Logo Immobilien Experten" class="img-fluid">',
        '<img src="/media/oberholz-logo.png" width="300" alt="Oberholz Immobilien" class="img-fluid">',
    ),
    (
        'alt="Logo Immobilien Experten" class="d-block d-md-none" fetchpriority="high" height="54" src="/media/ie_logo.svg" width="200"',
        'alt="Oberholz Immobilien" class="d-block d-md-none" fetchpriority="high" height="92" src="/media/oberholz-logo.png" width="200"',
    ),
    (
        'alt="Logo Immobilien Experten" class="d-none d-md-block" fetchpriority="high" height="54" src="/media/ie_logo.svg" width="200"',
        'alt="Oberholz Immobilien" class="d-none d-md-block" fetchpriority="high" height="92" src="/media/oberholz-logo.png" width="200"',
    ),
    (
        'alt="Logo Immobilien Experten" class="img-fluid" loading="lazy" src="/media/ie_logo.svg" width="200"',
        'alt="Oberholz Immobilien" class="img-fluid" loading="lazy" src="/media/oberholz-logo.png" width="200"',
    ),
    (
        'alt="Logo Immobilien Experten" class="img-fluid" src="/media/ie_logo.svg" width="300"',
        'alt="Oberholz Immobilien" class="img-fluid" src="/media/oberholz-logo.png" width="300"',
    ),
)

PHONE_DISPLAY_OLD = (
    "0800 - 220 33 30",
    "0800-220 33 30",
    "08002203330",
    "0151 23456789",
    "0173-2157655",
    "0173-2149122",
    "0174-7793694",
    "07721 - 29 69 240",
    "0211-54598822",
    "01522-4595678",
    "0911 131 327 00",
    "040 - 741 230 655",
    "0511-999 889 54",
    "0711-769 772 70",
    "069 363 935 920",
    "089 250 071 200",
)

TEL_HREF_RE = re.compile(r'href="tel:(?://)?\+?[0-9]+"', re.IGNORECASE)
COMPACT_BRAND_RE = re.compile(r"Immobilienexperten(?!de)", re.IGNORECASE)
COMPACT_SINGULAR_RE = re.compile(r"Immobilienexperte(?!n)", re.IGNORECASE)


def needs_patch(raw: bytes) -> bool:
    for needle in NEEDLES:
        if needle == b"immobilien-experten.de":
            continue
        if needle in raw:
            return True
    without_guard = raw.replace(b"immobilien-experten\\.de", b"")
    if b"immobilien-experten.de" in without_guard:
        return True
    if TEL_ANY_RE.search(raw) and not any(m in raw for m in OBERHOLZ_TEL_MARKERS):
        return True
    return False


def patch_text(text: str) -> tuple[str, dict[str, int]]:
    stats = {
        "logo": 0,
        "brand": 0,
        "email": 0,
        "domain": 0,
        "phone_display": 0,
        "tel_href": 0,
        "compact": 0,
    }

    for old, new in LOGO_REPLACEMENTS:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            stats["logo"] += n

    if "ie_logo.svg" in text:
        n = text.count("ie_logo.svg")
        text = text.replace("ie_logo.svg", "oberholz-logo.png")
        stats["logo"] += n
    if 'alt="Logo Immobilien Experten"' in text:
        n = text.count('alt="Logo Immobilien Experten"')
        text = text.replace(
            'alt="Logo Immobilien Experten"', 'alt="Oberholz Immobilien"'
        )
        stats["logo"] += n

    n = text.count("Immobilien Experten")
    if n:
        text = text.replace("Immobilien Experten", BRAND_NEW)
        stats["brand"] += n

    n = text.count("Immobilien%20Experten")
    if n:
        text = text.replace("Immobilien%20Experten", "Oberholz%20Immobilien")
        stats["brand"] += n

    n = text.count("info@immobilien-experten.de")
    if n:
        text = text.replace("info@immobilien-experten.de", EMAIL_NEW)
        stats["email"] += n

    # Domain contact strings, but preserve the JS guard pattern immobilien-experten\.de
    if "immobilien-experten.de" in text:
        parts = text.split("immobilien-experten\\.de")
        rebuilt = []
        for i, part in enumerate(parts):
            c = part.count("immobilien-experten.de")
            if c:
                part = part.replace("immobilien-experten.de", DOMAIN_NEW)
                stats["domain"] += c
            rebuilt.append(part)
            if i < len(parts) - 1:
                rebuilt.append("immobilien-experten\\.de")
        text = "".join(rebuilt)

    for old in PHONE_DISPLAY_OLD:
        n = text.count(old)
        if n:
            text = text.replace(old, PHONE_DISPLAY)
            stats["phone_display"] += n

    def _tel_sub(match: re.Match[str]) -> str:
        raw = match.group(0)
        stats["tel_href"] += 1
        if "://" in raw:
            return f'href="tel://{PHONE_TEL}"'
        if raw.lower().startswith('href="tel:0') or raw.lower().startswith(
            'href="tel:0800'
        ):
            return f'href="tel:{PHONE_TEL_LOCAL}"'
        return f'href="tel:{PHONE_TEL}"'

    text = TEL_HREF_RE.sub(_tel_sub, text)

    def _compact(match: re.Match[str]) -> str:
        stats["compact"] += 1
        word = match.group(0)
        if word.isupper():
            return "OBERHOLZ IMMOBILIEN"
        return BRAND_NEW

    text = COMPACT_BRAND_RE.sub(_compact, text)
    text = COMPACT_SINGULAR_RE.sub(_compact, text)

    return text, stats


def iter_html_files():
    index = ROOT / "index.html"
    if index.is_file():
        yield index
    public = ROOT / "public"
    for dirpath, _dirnames, filenames in os.walk(public):
        for name in filenames:
            if name.lower().endswith(".html"):
                yield Path(dirpath) / name


def main() -> None:
    started = time.time()
    totals = {
        "seen": 0,
        "skipped": 0,
        "changed": 0,
        "logo": 0,
        "brand": 0,
        "email": 0,
        "domain": 0,
        "phone_display": 0,
        "tel_href": 0,
        "compact": 0,
    }

    for path in iter_html_files():
        totals["seen"] += 1
        try:
            raw = path.read_bytes()
        except OSError as exc:
            print("read-fail", path, exc, flush=True)
            continue

        if not needs_patch(raw):
            totals["skipped"] += 1
        else:
            text = raw.decode("utf-8", errors="ignore")
            updated, stats = patch_text(text)
            if updated != text:
                path.write_text(updated, encoding="utf-8")
                totals["changed"] += 1
                for key in (
                    "logo",
                    "brand",
                    "email",
                    "domain",
                    "phone_display",
                    "tel_href",
                    "compact",
                ):
                    totals[key] += stats[key]
            else:
                totals["skipped"] += 1

        if totals["seen"] % 1000 == 0:
            print(
                f"progress seen={totals['seen']} changed={totals['changed']} "
                f"skipped={totals['skipped']} elapsed={time.time()-started:.0f}s",
                flush=True,
            )

    print("DONE", totals, f"elapsed={time.time()-started:.0f}s", flush=True)

    samples = [
        ROOT / "index.html",
        ROOT / "public" / "impressum.html",
        ROOT / "public" / "regionen" / "aachen" / "immobilienmakler.html",
        ROOT / "public" / "regionen" / "muenster" / "immobilienmakler.html",
        ROOT / "public" / "ueber-uns.html",
    ]
    for p in samples:
        if not p.exists():
            print("missing", p, flush=True)
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        print(
            p.as_posix(),
            "ie_logo=",
            t.count("ie_logo.svg"),
            "IE=",
            t.count("Immobilien Experten"),
            "OH=",
            t.count("Oberholz Immobilien"),
            "old_mail=",
            t.count("info@immobilien-experten.de"),
            "new_mail=",
            t.count(EMAIL_NEW),
            "0800=",
            t.count("0800 - 220 33 30"),
            "phone=",
            t.count(PHONE_DISPLAY),
            flush=True,
        )


if __name__ == "__main__":
    main()
