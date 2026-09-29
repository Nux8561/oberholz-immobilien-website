"""Rebuild Oberholz listings with hover secondary images + on-site detail pages."""

from __future__ import annotations

import html as html_lib
import json
import re
import shutil
import time
import unicodedata
import urllib.request
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DATA_PATH = ROOT / "assets" / "oberholz" / "is24-listings.json"
PORTAL = "https://portal.immobilienscout24.de/ergebnisliste/82828525"
TEMPLATE = ROOT / "public" / "immobilien" / "krefeld" / "charmantes-familienhaus-in-krefeld-linn-5835561.html"
MEDIA = ROOT / "public" / "media"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0"}

# Atlas Oberholz: übliche Käuferprovision je Seite in NRW (Münster/Essen/Bochum), inkl. MwSt.
PROVISION_KAUF = "3,57 %"
PROVISION_NOTE = f"zzgl. {PROVISION_KAUF} Käuferprovision"

# Scraped from portal 82828525 (pages 1+2), Anlage-Duplikate weggelassen.
RAW = [
    {
        "id": "170744873",
        "title": "Attraktive Kapitalanlage (Faktor 13,9) - Vermietetes Dreiparteienhaus in Bochum-Langendreer",
        "location": "44892 Bochum, Langendreer",
        "prop": "Haus",
        "deal": "Kauf",
        "price": "499.000 €",
        "price_label": "Kaufpreis",
        "area": "338,5 m²",
        "rooms": "14",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170744873/1/1",
    },
    {
        "id": "170212293",
        "title": "Geräumiges, sanierungsbedürftiges Reihenendhaus in ruhiger Lage in Essen-Kupferdreh",
        "location": "45257 Essen, Kupferdreh",
        "prop": "Haus",
        "deal": "Kauf",
        "price": "425.000 €",
        "price_label": "Kaufpreis",
        "area": "153,8 m²",
        "rooms": "5",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170212293/1/1",
    },
    {
        "id": "170680511",
        "title": "Bezugsfreies Reihenhaus mit Garage und Garten in Duisburg-Walsum",
        "location": "47179 Duisburg, Wehofen",
        "prop": "Haus",
        "deal": "Kauf",
        "price": "350.000 €",
        "price_label": "Kaufpreis",
        "area": "161,3 m²",
        "rooms": "6",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170680511/1/1",
    },
    {
        "id": "170497940",
        "title": "Hohe Rendite möglich. 3 Appartements, Nähe Innenstadt, gut vermietet",
        "location": "48653 Coesfeld",
        "prop": "Wohnung",
        "deal": "Kauf",
        "price": "300.000 €",
        "price_label": "Kaufpreis",
        "area": "165 m²",
        "rooms": "2",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170497940/1/1",
    },
    {
        "id": "170827695",
        "title": "Bezugsfreie Maisonettewohnung mit zwei Balkonen und Tiefgaragenstellplatz in Münster-Mecklenbeck",
        "location": "48163 Münster, Mecklenbeck",
        "prop": "Wohnung",
        "deal": "Kauf",
        "price": "299.000 €",
        "price_label": "Kaufpreis",
        "area": "74 m²",
        "rooms": "3",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170827695/1/1",
    },
    {
        "id": "170022736",
        "title": "Ihr neues Zuhause mit Garten satt – Platz für Kinder, Trampolin und Grillabende",
        "location": "48703 Stadtlohn",
        "prop": "Haus",
        "deal": "Kauf",
        "price": "285.000 €",
        "price_label": "Kaufpreis",
        "area": "149,4 m²",
        "rooms": "7",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170022736/1/1",
    },
    {
        "id": "170710610",
        "title": "Barrierefreie 2-Zi-Wohnung mit Balkon, Schwimmbad und Stellplatz",
        "location": "40470 Düsseldorf, Mörsenbroich",
        "prop": "Wohnung",
        "deal": "Kauf",
        "price": "249.000 €",
        "price_label": "Kaufpreis",
        "area": "68 m²",
        "rooms": "2",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170710610/1/1",
    },
    {
        "id": "170649223",
        "title": "Gepflegtes Reihenhaus mit Garten und Garage in Bergkamen-Oberaden",
        "location": "59192 Bergkamen",
        "prop": "Haus",
        "deal": "Kauf",
        "price": "249.000 €",
        "price_label": "Kaufpreis",
        "area": "98 m²",
        "rooms": "4",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170649223/1/1",
    },
    {
        "id": "170647853",
        "title": "EG-Wohnung mit Terrasse und Garage – barrierefrei und bezugsfrei",
        "location": "45143 Essen, Altendorf",
        "prop": "Wohnung",
        "deal": "Kauf",
        "price": "199.000 €",
        "price_label": "Kaufpreis",
        "area": "74,2 m²",
        "rooms": "3",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170647853/1/1",
    },
    {
        "id": "170934647",
        "title": "Große Eigentumswohnung in Rheine",
        "location": "48429 Rheine",
        "prop": "Wohnung",
        "deal": "Kauf",
        "price": "185.000 €",
        "price_label": "Kaufpreis",
        "area": "93 m²",
        "rooms": "4",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170934647/1/1",
    },
    {
        "id": "170199527",
        "title": "Helle Maisonettewohnung mit Südbalkon und zwei Bädern – bezugsfrei",
        "location": "42553 Velbert, Neviges",
        "prop": "Wohnung",
        "deal": "Kauf",
        "price": "182.000 €",
        "price_label": "Kaufpreis",
        "area": "97,7 m²",
        "rooms": "3,5",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170199527/1/1",
    },
    {
        "id": "170003861",
        "title": "Gepflegte Etagenwohnung mit Südbalkon und Garage – bezugsfrei",
        "location": "45143 Essen, Altendorf",
        "prop": "Wohnung",
        "deal": "Kauf",
        "price": "179.000 €",
        "price_label": "Kaufpreis",
        "area": "75 m²",
        "rooms": "3",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170003861/1/1",
    },
    {
        "id": "170577981",
        "title": "Bezugsfreies Apartment mit saniertem Badezimmer und Böden in Essen-Bochold",
        "location": "45356 Essen, Bochold",
        "prop": "Wohnung",
        "deal": "Kauf",
        "price": "75.000 €",
        "price_label": "Kaufpreis",
        "area": "30 m²",
        "rooms": "1",
        "href": "https://portal.immobilienscout24.de/expose/82828525/170577981/1/1",
    },
    {
        "id": "171202458",
        "title": "3-Zi-Wohnung mit Süd-Balkon und Tiefgarage in Münster-Mauritz",
        "location": "Münster, Herz-Jesu / Mauritz",
        "prop": "Wohnung",
        "deal": "Miete",
        "price": "1.250 €",
        "price_label": "Kaltmiete",
        "area": "85 m²",
        "rooms": "3",
        "href": "https://portal.immobilienscout24.de/expose/82828525/171202458/2/1",
    },
    {
        "id": "171281981",
        "title": "Attraktive 3-Zi-Wohnung mit ruhiger Lage in Steinfurt-Borghorst",
        "location": "Steinfurt, Borghorst",
        "prop": "Wohnung",
        "deal": "Miete",
        "price": "740 €",
        "price_label": "Kaltmiete",
        "area": "86 m²",
        "rooms": "3",
        "href": "https://portal.immobilienscout24.de/expose/82828525/171281981/2/1",
    },
]

ICON_HOME = (
    '<svg class="text-muted" fill="none" height="24" style="width: 1em; height: 1em;" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M2.25 12L11.2045 3.04549C11.6438 2.60615 12.3562 2.60615 12.7955 3.04549L21.75 12M4.5 9.75V19.875C4.5 20.4963 5.00368 21 5.625 21H9.75V16.125C9.75 15.5037 10.2537 15 10.875 15H13.125C13.7463 15 14.25 15.5037 14.25 16.125V21H18.375C18.9963 21 19.5 20.4963 19.5 19.875V9.75M8.25 21H16.5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path></svg>'
)
ICON_TAG = (
    '<svg class="text-muted" fill="none" height="24" style="width: 1em; height: 1em;" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M9.56802 3H5.25C4.00736 3 3 4.00736 3 5.25V9.56802C3 10.1648 3.23705 10.7371 3.65901 11.159L13.2401 20.7401C13.9388 21.4388 15.0199 21.6117 15.8465 21.0705C17.9271 19.7084 19.7084 17.9271 21.0705 15.8465C21.6117 15.0199 21.4388 13.9388 20.7401 13.2401L11.159 3.65901C10.7371 3.23705 10.1648 3 9.56802 3Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path>'
    '<path d="M6 6H6.0075V6.0075H6V6Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path></svg>'
)
ICON_PIN = (
    '<svg class="text-muted" fill="none" height="24" style="width: 1em; height: 1em;" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M15 10.5C15 12.1569 13.6569 13.5 12 13.5C10.3431 13.5 9 12.1569 9 10.5C9 8.84315 10.3431 7.5 12 7.5C13.6569 7.5 15 8.84315 15 10.5Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path>'
    '<path d="M19.5 10.5C19.5 17.6421 12 21.75 12 21.75C12 21.75 4.5 17.6421 4.5 10.5C4.5 6.35786 7.85786 3 12 3C16.1421 3 19.5 6.35786 19.5 10.5Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path></svg>'
)
ICON_AREA = (
    '<svg class="text-muted" fill="none" height="24" style="width: 1em; height: 1em;" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M3.75 3.75V8.25M3.75 3.75H8.25M3.75 3.75L9 9M3.75 20.25V15.75M3.75 20.25H8.25M3.75 20.25L9 15M20.25 3.75L15.75 3.75M20.25 3.75V8.25M20.25 3.75L15 9M20.25 20.25H15.75M20.25 20.25V15.75M20.25 20.25L15 15" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path></svg>'
)
ICON_ROOMS = (
    '<svg class="text-muted" fill="none" height="24" style="width: 1em; height: 1em;" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M3.75 6C3.75 4.75736 4.75736 3.75 6 3.75H8.25C9.49264 3.75 10.5 4.75736 10.5 6V8.25C10.5 9.49264 9.49264 10.5 8.25 10.5H6C4.75736 10.5 3.75 9.49264 3.75 8.25V6Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path>'
    '<path d="M3.75 15.75C3.75 14.5074 4.75736 13.5 6 13.5H8.25C9.49264 13.5 10.5 14.5074 10.5 15.75V18C10.5 19.2426 9.49264 20.25 8.25 20.25H6C4.75736 20.25 3.75 19.2426 3.75 18V15.75Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path>'
    '<path d="M13.5 6C13.5 4.75736 14.5074 3.75 15.75 3.75H18C19.2426 3.75 20.25 4.75736 20.25 6V8.25C20.25 9.49264 19.2426 10.5 18 10.5H15.75C14.5074 10.5 13.5 9.49264 13.5 8.25V6Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path>'
    '<path d="M13.5 15.75C13.5 14.5074 14.5074 13.5 15.75 13.5H18C19.2426 13.5 20.25 14.5074 20.25 15.75V18C20.25 19.2426 19.2426 20.25 18 20.25H15.75C14.5074 20.25 13.5 19.2426 13.5 18V15.75Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></path></svg>'
)

HOVER_ASSETS = (
    '<style>.immo-img picture, .immo-img img { position: absolute; inset: 0; }.immo-img-secondary { opacity: 0; transition: opacity .35s ease; }.immo-img-primary { opacity: 1; transition: opacity .35s ease; }.immo-img img { transition: transform .4s ease; }.immo-card { transition: transform .25s ease, box-shadow .25s ease; }'
    "@media (hover: hover) and (pointer: fine) { .immo-card:hover { transform: translateY(-4px); box-shadow: 0 1rem 2rem rgba(0, 0, 0, .12) !important; } .immo-card:hover .immo-img-secondary { opacity: 1; } .immo-card:hover .immo-img-primary { opacity: 0; } .immo-card:hover .immo-img img { transform: scale(1.05); }}</style>"
    "<script>(function () { var geladen = new WeakSet(); function laden(box) { if (!box || geladen.has(box)) { return; } var tpl = box.querySelector('.immo-img-secondary-tpl'); if (!tpl) { return; } geladen.add(box); box.appendChild(tpl.content.cloneNode(true)); } function behandeln(e) { var card = e.target.closest && e.target.closest('.immo-card'); var box = card && card.querySelector('.immo-img'); if (box) { laden(box); } } ['mouseover', 'pointerover', 'touchstart', 'focusin'].forEach(function (ev) { document.addEventListener(ev, behandeln, { passive: true }); });})();</script>"
)

SIZES = ("780", "1024", "1440", "2400")
MAX_GALLERY = 16
FEATURED = 6


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", "replace")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1000:
        return
    req = urllib.request.Request(url, headers={**UA, "Accept": "image/*"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        dest.write_bytes(resp.read())


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    repl = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
    for a, b in repl.items():
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:80] or "objekt"


def city_slug(location: str) -> str:
    # "44892 Bochum, Langendreer" -> bochum; "Münster, Herz-Jesu" -> muenster
    part = location.split(",")[0]
    part = re.sub(r"^\d+\s*", "", part).strip()
    return slugify(part) or "region"


def clean_text(raw: str) -> str:
    raw = unescape(raw)
    raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
    raw = re.sub(r"</p\s*>", "\n\n", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw.strip()


def extract_section(html: str, label: str) -> str:
    m = re.search(
        rf">{re.escape(label)}</h[1-6]>\s*(?:<div[^>]*>\s*)?(?:<p[^>]*>)?(.*?)(?:</p>|<h[1-6]\b)",
        html,
        re.S | re.I,
    )
    if not m:
        return ""
    return clean_text(m.group(1))


def scrape_expose(item: dict) -> dict:
    html = fetch(item["href"])
    bare = list(dict.fromkeys(re.findall(r"/listings/[a-f0-9\-]+-\d+\.(?:jpg|jpeg|png)", html, re.I)))
    imgs = [
        f"https://pictures.immobilienscout24.de{path}/ORIG/resize/1106x830%3E/format/jpg/quality/80"
        for path in bare[:MAX_GALLERY]
    ]
    if not imgs:
        # fallback: any resized listing url
        resized = list(
            dict.fromkeys(
                re.findall(
                    r"//pictures\.immobilienscout24\.de(/listings/[a-f0-9\-]+-\d+\.(?:jpg|jpeg|png)/ORIG/resize/[^\"'\s]+)",
                    html,
                    re.I,
                )
            )
        )
        imgs = [f"https://pictures.immobilienscout24.de{p}" for p in resized[:MAX_GALLERY]]

    item["images"] = imgs
    item["desc"] = extract_section(html, "Objektbeschreibung")
    item["ausstattung"] = extract_section(html, "Ausstattung")
    item["lage"] = extract_section(html, "Lage")
    item["sonstiges"] = extract_section(html, "Sonstiges")
    print(f"scrape {item['id']}: {len(imgs)} imgs, desc={len(item['desc'])}")
    time.sleep(0.35)
    return item


def place_images(item: dict) -> None:
    oid = item["id"]
    images = item.get("images") or []
    if not images:
        raise RuntimeError(f"no images for {oid}")

    # Ensure at least 2 images for hover (duplicate first if needed).
    if len(images) == 1:
        images = [images[0], images[0]]
        item["images"] = images

    local_paths: list[str] = []
    for idx, url in enumerate(images):
        suffix = f"{idx:03d}"
        # canonical store in object-zoom-780
        dest = MEDIA / "object-zoom-780" / f"{oid}_{suffix}.jpg"
        download(url, dest)
        local_paths.append(f"/media/object-zoom-780/{oid}_{suffix}.jpg")

        # mirror into responsive folders used by cards/detail
        for size in SIZES:
            for folder_prefix, start_from in (
                ("object-zoom", 0),
                ("object-hero", 0),
                ("object-thumb", 1),
                ("object-thumbnail", 0),
            ):
                if folder_prefix == "object-hero" and idx != 0:
                    continue
                if folder_prefix == "object-thumb" and idx < start_from:
                    continue
                target = MEDIA / f"{folder_prefix}-{size}" / f"{oid}_{suffix}.jpg"
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists() or target.stat().st_size < 1000:
                    shutil.copyfile(dest, target)

        # also keep flat oberholz-listings for debugging
        flat = MEDIA / "oberholz-listings" / f"{oid}_{suffix}.jpg"
        flat.parent.mkdir(parents=True, exist_ok=True)
        if not flat.exists():
            shutil.copyfile(dest, flat)

    item["local_images"] = local_paths
    item["thumb0"] = f"/media/object-thumbnail-780/{oid}_000.jpg"
    item["thumb1"] = f"/media/object-thumbnail-780/{oid}_001.jpg"
    print("images placed", oid, len(local_paths))


def badge(label: str, icon: str) -> str:
    return (
        f'<span class="badge bg-white text-dark border d-inline-flex align-items-center gap-1 fw-normal" style="font-size:.75rem"> '
        f"{icon} {escape(label)} </span>"
    )


def picture_tag(src: str, alt: str, cls: str) -> str:
    # Keep structure close to original; all size variants point to same file if missing.
    oid_match = re.search(r"/(\d+)_(\d{3})\.jpg$", src)
    if oid_match:
        oid, suf = oid_match.group(1), oid_match.group(2)
        sources = []
        for media, size, folder in (
            ("(min-width: 2400px)", "2400", "object-thumbnail-2400"),
            ("(min-width: 1440px)", "1440", "object-thumbnail-1440"),
            ("(min-width: 1024px)", "1024", "object-thumbnail-1024"),
            ("(min-width: 780px)", "780", "object-thumbnail-780"),
        ):
            sources.append(
                f'<source media="{media}" srcset="/media/{folder}/{oid}_{suf}.jpg" width="800" height="600">'
            )
        body = "".join(sources) + (
            f'<img alt="{escape(alt)}" class="img-fluid w-100 h-100 object-fit-cover {cls}" decoding="async" '
            f'fetchpriority="low" height="520" loading="lazy" src="/media/object-thumbnail-780/{oid}_{suf}.jpg" '
            f'sizes="(max-width: 992px) 50vw, (max-width: 1320px) 33vw, 440px" width="700"/>'
        )
        return f"<picture>{body}</picture>"
    return (
        f'<img alt="{escape(alt)}" class="img-fluid w-100 h-100 object-fit-cover {cls}" decoding="async" '
        f'fetchpriority="low" height="520" loading="lazy" src="{escape(src, quote=True)}" width="700"/>'
    )


def card(item: dict) -> str:
    title = escape(item["title"])
    loc = escape(item["location"])
    href = escape(item["detail_href"], quote=True)
    area = escape(item["area"])
    rooms = escape(item["rooms"])
    price = escape(item["price"])
    price_label = escape(item["price_label"])
    primary = picture_tag(item["thumb0"], item["title"], "immo-img-primary")
    secondary = picture_tag(item["thumb1"], item["title"], "immo-img-secondary")
    return (
        f'<div class="col-12 col-md-6 col-lg-4" data-object-id="{escape(item["id"])}"> '
        f'<article class="card immo-card h-100 border-0 shadow-sm overflow-hidden"> '
        f'<div class="position-relative overflow-hidden"> '
        f'<div class="ratio ratio-4x3 immo-img bg-light"> '
        f"{primary} "
        f'<template class="immo-img-secondary-tpl">{secondary}</template> '
        f"</div> "
        f'<div class="position-absolute bottom-0 start-0 m-3 d-flex gap-2"> '
        f'{badge(item["prop"], ICON_HOME)} {badge(item["deal"], ICON_TAG)} '
        f"</div> </div> "
        f'<div class="card-body d-flex flex-column p-4"> '
        f'<div class="text-muted small d-flex align-items-start gap-2 mb-2"> '
        f'<span class="flex-shrink-0" style="font-size:1.05rem;line-height:1.25;"> {ICON_PIN} </span> '
        f"<span> {loc} </span> </div> "
        f'<h3 class="h5 fw-bold lh-base title-2lines mb-3 title-color"> '
        f'<a class="stretched-link text-decoration-none title-color" href="{href}"> {title} </a> '
        f"</h3> "
        f'<div class="d-flex flex-wrap gap-3 text-muted small mb-3"> '
        f'<span class="d-inline-flex align-items-center gap-1"> {ICON_AREA} <strong class="text-body">{area}</strong> </span> '
        f'<span class="d-inline-flex align-items-center gap-1"> {ICON_ROOMS} <strong class="text-body">{rooms} Zi.</strong> </span> '
        f"</div> "
        f'<div class="mt-auto pt-3 border-top"> '
        f'<div class="d-flex align-items-baseline justify-content-between gap-2"> '
        f'<span class="text-muted small"> {price_label} </span> '
        f'<span class="h5 mb-0 fw-bold" style="color:var(--secondary-color,#0d6efd)"> {price} </span> '
        f"</div> "
        f'{provision_html(item)}'
        f"</div> </div> </article></div>"
    )


def provision_html(item: dict) -> str:
    if item.get("deal") != "Kauf":
        return ""
    return (
        '<div class="text-muted text-end mt-1" style="font-size:.72rem;line-height:1.3;opacity:.85"> '
        f"{escape(PROVISION_NOTE)} </div>"
    )


def build_section(items: list[dict]) -> str:
    featured = items[:FEATURED]
    cards = "".join(card(item) for item in featured)
    return (
        '<section class="py-5 bg-light" id="angebote"> <div class="container"> '
        '<h2 class="pb-1">Aktuelle Immobilien aus unserer Vermittlung</h2> '
        '<p class="pb-3">Ein Auszug aus unseren aktuellen Objekten über Immobilienscout24 – Münster, Essen, Bochum und Umgebung.</p> '
        f'<div class="row g-4"> {cards} {HOVER_ASSETS} </div> '
        f'<div class="pt-4"> <a class="btn btn-solid-border btn-round-full" href="{PORTAL}" rel="noopener" target="_blank" title="Alle Immobilien auf Immobilienscout24">Alle aktuellen Immobilien ansehen</a> </div> '
        "</div> </section>"
    )


def paragraphs(text: str) -> str:
    if not text:
        return "<p class=\"text-muted\">Details auf Anfrage.</p>"
    chunks = [c.strip() for c in re.split(r"\n\s*\n", text) if c.strip()]
    if not chunks:
        chunks = [text]
    return "".join(f"<p>{escape(c)}</p>" for c in chunks)


def gallery_main(item: dict) -> str:
    oid = item["id"]
    imgs = item["local_images"]
    n = len(imgs)
    title = escape(item["title"])
    loc = escape(item["location"])
    price = escape(item["price"])
    price_label = escape(item["price_label"])
    area = escape(item["area"])
    rooms = escape(item["rooms"])
    prop = escape(item["prop"])
    deal = escape(item["deal"])

    thumbs = ""
    for i in range(1, min(5, n)):
        thumbs += (
            f'<div class="immo-detail-thumbcell"> '
            f'<a class="gallery-trigger d-block h-100 w-100" data-bs-target="#galleryModal" data-bs-toggle="modal" data-index="{i}" href="#"> '
            f'<picture><img alt="{title}" class="img-fluid w-100 h-100 object-fit-cover" loading="lazy" '
            f'src="/media/object-thumb-780/{oid}_{i:03d}.jpg"/></picture></a></div> '
        )

    slides = ""
    for i in range(n):
        active = " active" if i == 0 else ""
        slides += (
            f'<div class="carousel-item{active}"> '
            f'<img alt="{title}" class="d-block w-100" src="/media/object-zoom-780/{oid}_{i:03d}.jpg"/> '
            f"</div> "
        )

    indicators = "".join(
        f'<button aria-label="Slide {i+1}" class="{"active" if i == 0 else ""}" data-bs-slide-to="{i}" '
        f'data-bs-target="#galleryCarousel" type="button"></button> '
        for i in range(n)
    )

    sections = []
    for label, key in (
        ("Objektbeschreibung", "desc"),
        ("Ausstattung", "ausstattung"),
        ("Lage", "lage"),
        ("Sonstiges", "sonstiges"),
    ):
        val = item.get(key) or ""
        if val:
            sections.append(f'<div class="mb-4"><h2 class="h4 title-color mb-3">{label}</h2>{paragraphs(val)}</div>')

    return f"""
<main>
  <section class="py-4 bg-light">
    <div class="container">
      <nav aria-label="breadcrumb" class="mb-3">
        <ol class="breadcrumb mb-0">
          <li class="breadcrumb-item"><a href="/">Start</a></li>
          <li class="breadcrumb-item"><a href="/#angebote">Immobilien</a></li>
          <li class="breadcrumb-item active" aria-current="page">{title}</li>
        </ol>
      </nav>
      <div class="row g-3 align-items-stretch">
        <div class="col-12 col-md-8">
          <div class="position-relative rounded overflow-hidden bg-dark" style="min-height:320px">
            <a class="gallery-trigger d-block" data-bs-toggle="modal" data-bs-target="#galleryModal" data-index="0" href="#">
              <div class="ratio ratio-16x9">
                <img alt="{title}" class="img-fluid w-100 h-100 object-fit-cover" src="/media/object-hero-780/{oid}_000.jpg"/>
              </div>
            </a>
            <span class="badge bg-dark bg-opacity-75 text-white position-absolute" style="top:1rem;right:1rem;font-size:.75rem">1 / {n}</span>
          </div>
        </div>
        <div class="col-12 col-md-4 immo-detail-thumbcol">
          <div class="immo-detail-thumbgrid immo-detail-thumbgrid--4" style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem;height:100%">
            {thumbs}
          </div>
        </div>
      </div>

      <div class="row g-4 mt-1">
        <div class="col-12 col-lg-8">
          <div class="bg-white p-4 rounded shadow-sm">
            <div class="d-flex flex-wrap gap-2 mb-3">
              <span class="badge bg-white text-dark border">{prop}</span>
              <span class="badge bg-white text-dark border">{deal}</span>
            </div>
            <h1 class="mb-2 fw-bold title-color" style="font-size:clamp(1.6rem,2.5vw,2.25rem);line-height:1.25">{title}</h1>
            <div class="text-muted mb-3 d-flex align-items-center gap-2">{ICON_PIN}<span>{loc}</span></div>
            <div class="d-flex align-items-baseline gap-2 mb-4">
              <span class="text-uppercase small" style="letter-spacing:.5px;opacity:.75">{price_label}</span>
              <span class="fw-bold title-color" style="font-size:1.75rem;line-height:1">{price}</span>
            </div>
            <div class="d-flex flex-wrap gap-4 text-muted mb-4 pb-3 border-bottom">
              <span class="d-inline-flex align-items-center gap-2">{ICON_AREA}<strong class="text-body">{area}</strong></span>
              <span class="d-inline-flex align-items-center gap-2">{ICON_ROOMS}<strong class="text-body">{rooms} Zi.</strong></span>
            </div>
            {''.join(sections)}
          </div>
        </div>
        <div class="col-12 col-lg-4">
          <div class="bg-white p-4 rounded shadow-sm sticky-top" style="top:1rem">
            <h2 class="h5 title-color mb-3">Interesse an diesem Objekt?</h2>
            <p class="text-muted">Wir beraten Sie persönlich zu Besichtigung, Unterlagen und nächsten Schritten.</p>
            <a class="btn btn-primary w-100 mb-2" href="tel:+4925128429090">0251 28 42 90 90</a>
            <a class="btn btn-outline-secondary w-100 mb-3" href="mailto:mail@oberholz-immobilien.com?subject={escape(item['title'], quote=True)}">E-Mail senden</a>
            <a class="btn btn-link px-0" href="/#angebote">Zurück zu den Angeboten</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="modal fade" id="galleryModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-xl">
      <div class="modal-content bg-dark border-0">
        <div class="modal-header border-0">
          <h2 class="modal-title h6 text-white mb-0">{title}</h2>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Schließen"></button>
        </div>
        <div class="modal-body p-0">
          <div id="galleryCarousel" class="carousel slide" data-bs-ride="false">
            <div class="carousel-indicators">{indicators}</div>
            <div class="carousel-inner">{slides}</div>
            <button class="carousel-control-prev" type="button" data-bs-target="#galleryCarousel" data-bs-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Zurück</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#galleryCarousel" data-bs-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Weiter</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <script>
  (function(){{
    var modal = document.getElementById('galleryModal');
    if (!modal) return;
    modal.addEventListener('show.bs.modal', function (event) {{
      var trigger = event.relatedTarget;
      var idx = trigger && trigger.getAttribute('data-index');
      if (idx == null) return;
      var carousel = bootstrap.Carousel.getOrCreateInstance(document.getElementById('galleryCarousel'));
      carousel.to(Number(idx));
    }});
  }})();
  </script>
</main>
"""


def write_detail_page(item: dict, shell_before: str, shell_after: str) -> str:
    city = city_slug(item["location"])
    slug = f"{slugify(item['title'])}-{item['id']}"
    rel = f"/immobilien/{city}/{slug}.html"
    out = ROOT / "public" / "immobilien" / city / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)

    title = item["title"]
    page = shell_before + gallery_main(item) + shell_after

    # Replace template title/meta leftovers carefully on the chrome only.
    page = page.replace("Charmantes Familienhaus in Krefeld-Linn", title)
    page = page.replace(
        "/immobilien/krefeld/charmantes-familienhaus-in-krefeld-linn-5835561.html",
        rel,
    )
    page = page.replace("5835561", item["id"])
    # Remove preload hero of old object if still present
    page = re.sub(
        r'<link rel="preload" as="image" href="/media/object-hero-780/[^"]+"[^>]*>',
        f'<link rel="preload" as="image" href="/media/object-hero-780/{item["id"]}_000.jpg" fetchpriority="high">',
        page,
        count=1,
    )

    out.write_text(page, encoding="utf-8")
    item["detail_href"] = rel
    item["detail_path"] = str(out.relative_to(ROOT)).replace("\\", "/")
    print("detail", rel)
    return rel


def load_shell() -> tuple[str, str]:
    tpl = TEMPLATE.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"(.*)<main\b[^>]*>.*</main>(.*)", tpl, re.S | re.I)
    if not m:
        raise SystemExit("detail template main not found")
    return m.group(1), m.group(2)


def patch_index(items: list[dict]) -> None:
    text = INDEX.read_text(encoding="utf-8")
    marker = "Aktuelle Immobilien aus unserer Vermittlung"
    start = text.rfind("<section", 0, text.find(marker))
    end = text.find("</section>", text.find(marker))
    if start < 0 or end < 0:
        raise SystemExit("listings section not found")
    end += len("</section>")
    new_text = text[:start] + build_section(items) + text[end:]
    INDEX.write_text(new_text, encoding="utf-8")
    print("index patched, featured", FEATURED)


def main() -> None:
    shell_before, shell_after = load_shell()
    items: list[dict] = []
    for raw in RAW:
        item = dict(raw)
        scrape_expose(item)
        place_images(item)
        write_detail_page(item, shell_before, shell_after)
        items.append(item)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    patch_index(items)
    print("done", len(items), "objects")


if __name__ == "__main__":
    main()
