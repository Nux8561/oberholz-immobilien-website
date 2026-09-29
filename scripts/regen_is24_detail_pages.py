"""Regenerate detail pages + homepage cards: fixed hero + Atlas provision."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "oberholz" / "is24-listings.json"
INDEX = ROOT / "index.html"

import sys

sys.path.insert(0, str(ROOT / "scripts"))
from build_is24_listings import (  # noqa: E402
    FEATURED,
    ICON_AREA,
    ICON_PIN,
    ICON_ROOMS,
    PROVISION_NOTE,
    build_section,
    city_slug,
    load_shell,
    paragraphs,
    slugify,
)

HERO_CSS = """
<style id="oberholz-immo-detail-css">
.immo-detail-hero{
  position:relative;
  background:#1a1a1a;
  border-radius:.75rem;
  overflow:hidden;
  min-height:280px;
}
.immo-detail-hero-link{display:block;line-height:0;}
.immo-detail-hero-img{
  width:100%;
  height:auto;
  aspect-ratio:16/9;
  max-height:560px;
  min-height:280px;
  object-fit:cover;
  display:block;
  background:#222;
}
.immo-detail-hero-overlay{
  position:absolute;inset:0;
  background:linear-gradient(to top, rgba(0,0,0,.78) 0%, rgba(0,0,0,.28) 42%, rgba(0,0,0,0) 68%);
  pointer-events:none;
}
.immo-detail-hero-content{
  position:absolute;bottom:0;left:0;right:0;
  padding:1.75rem 2rem;
  color:#fff;
  z-index:2;
}
.immo-detail-hero-content h1,
.immo-detail-hero-content .lead{color:#fff;}
.immo-detail-thumbcol{position:relative;min-height:280px;}
.immo-detail-thumbgrid{display:grid;gap:.5rem;height:100%;}
.immo-detail-thumbgrid--4{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;}
.immo-detail-thumbcell{position:relative;overflow:hidden;border-radius:.5rem;min-height:120px;background:#e9eef3;}
.immo-detail-thumbcell > a,
.immo-detail-thumbcell picture{display:block;width:100%;height:100%;}
.immo-detail-thumb{width:100%;height:100%;object-fit:cover;display:block;cursor:pointer;}
@media (min-width:768px){
  .immo-detail-thumbgrid{position:absolute;inset:0;}
  .immo-detail-thumbcell{min-height:0;}
}
@media (max-width:767.98px){
  .immo-detail-thumbgrid{aspect-ratio:16/9;}
  .immo-detail-hero{background:transparent;min-height:0;}
  .immo-detail-hero-img{border-radius:.75rem;min-height:200px;}
  .immo-detail-hero-overlay{display:none;}
  .immo-detail-hero-content{
    position:static;padding:1.25rem 0 0;color:inherit;z-index:auto;
  }
  .immo-detail-hero-content h1,
  .immo-detail-hero-content .lead{color:var(--title-color,#1a1a1a);}
}
#galleryModal .modal-content{background:#000;}
#galleryModal .carousel-item{text-align:center;}
#galleryModal .carousel-item img{
  display:block;width:100%;height:auto;max-height:80vh;object-fit:contain;margin:0 auto;
}
.immo-breadcrumb{font-size:.85rem;color:var(--base-color,#5a6270);}
.immo-breadcrumb-list{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:center;gap:.35rem .5rem;}
.immo-breadcrumb-item{display:inline-flex;align-items:center;gap:.5rem;}
.immo-breadcrumb-item + .immo-breadcrumb-item::before{
  content:"";display:inline-block;width:.45rem;height:.45rem;
  border-top:1.5px solid currentColor;border-right:1.5px solid currentColor;
  transform:rotate(45deg);opacity:.45;
}
.immo-breadcrumb-item a{color:inherit;text-decoration:none;}
.immo-breadcrumb-item a:hover{color:var(--secondary-color,#0d6efd);text-decoration:underline;}
.immo-breadcrumb-item.is-current span{
  color:var(--title-color,#1a1a1a);font-weight:500;
  max-width:42ch;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
}
.immo-provision{font-size:.85rem;opacity:.85;}
</style>
"""


def provision_block(item: dict, *, light: bool = False) -> str:
    if item.get("deal") != "Kauf":
        return ""
    cls = "text-white-50" if light else "text-muted"
    return f'<div class="immo-provision {cls} mt-1">{escape(PROVISION_NOTE)}</div>'


def gallery_main(item: dict) -> str:
    oid = item["id"]
    imgs = item.get("local_images") or []
    if not imgs:
        imgs = [
            f"/media/object-zoom-780/{oid}_{i:03d}.jpg"
            for i in range(16)
            if (ROOT / "public" / "media" / "object-zoom-780" / f"{oid}_{i:03d}.jpg").exists()
        ]
    n = max(len(imgs), 1)
    title = escape(item["title"])
    loc = escape(item["location"])
    price = escape(item["price"])
    price_label = escape(item["price_label"])
    area = escape(item["area"])
    rooms = escape(item["rooms"])
    prop = escape(item["prop"])
    deal = escape(item["deal"])
    hero = f"/media/object-hero-780/{oid}_000.jpg"
    # fallback if hero missing
    if not (ROOT / "public" / "media" / "object-hero-780" / f"{oid}_000.jpg").exists():
        hero = f"/media/object-zoom-780/{oid}_000.jpg"

    thumbs = ""
    for i in range(1, min(5, n)):
        thumbs += (
            f'<div class="immo-detail-thumbcell">'
            f'<a href="#" class="gallery-trigger d-block h-100 w-100" data-index="{i}" '
            f'data-bs-toggle="modal" data-bs-target="#galleryModal">'
            f'<img src="/media/object-thumb-780/{oid}_{i:03d}.jpg" width="400" height="300" '
            f'class="immo-detail-thumb" alt="{title} – Bild {i+1}" loading="lazy" decoding="async">'
            f"</a></div>"
        )

    slides = ""
    for i in range(n):
        active = " active" if i == 0 else ""
        slides += (
            f'<div class="carousel-item{active}">'
            f'<img alt="{title}" class="d-block w-100" src="/media/object-zoom-780/{oid}_{i:03d}.jpg">'
            f"</div>"
        )
    indicators = "".join(
        f'<button type="button" data-bs-target="#galleryCarousel" data-bs-slide-to="{i}" '
        f'class="{"active" if i == 0 else ""}" aria-label="Slide {i+1}"></button>'
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
            sections.append(
                f'<div class="mb-4"><h2 class="h4 title-color mb-3">{label}</h2>{paragraphs(val)}</div>'
            )

    return f"""
<main>
{HERO_CSS}
<div class="container-wide pt-4">
  <nav aria-label="Breadcrumb" class="immo-breadcrumb">
    <ol class="immo-breadcrumb-list">
      <li class="immo-breadcrumb-item"><a href="/">Start</a></li>
      <li class="immo-breadcrumb-item"><a href="/#angebote">Immobilien</a></li>
      <li class="immo-breadcrumb-item is-current" aria-current="page"><span>{title}</span></li>
    </ol>
  </nav>
</div>
<div class="container-wide my-4">
  <div class="row g-3 align-items-stretch">
    <div class="col-12 col-md-8">
      <div class="immo-detail-hero" style="background-image:url('{hero}');background-size:cover;background-position:center;">
        <a href="#" class="gallery-trigger immo-detail-hero-link" data-index="0" data-bs-toggle="modal" data-bs-target="#galleryModal" aria-label="Galerie öffnen">
          <img src="{hero}" width="975" height="548" class="immo-detail-hero-img" alt="{title}" fetchpriority="high" decoding="async">
        </a>
        <div class="immo-detail-hero-overlay"></div>
        <div class="immo-detail-hero-content">
          <div class="d-flex flex-column gap-2">
            <div class="d-flex flex-wrap gap-2">
              <span class="badge bg-white text-dark border">{prop}</span>
              <span class="badge bg-white text-dark border">{deal}</span>
            </div>
            <h1 class="mb-0 fw-bold" style="font-size:clamp(1.35rem,2.2vw,2.1rem);line-height:1.25">{title}</h1>
            <div class="d-flex align-items-center gap-2 lead mb-0" style="font-size:1rem">{ICON_PIN}<span>{loc}</span></div>
            <div class="d-flex align-items-baseline gap-2 mt-1 flex-wrap">
              <span class="text-uppercase small" style="letter-spacing:.5px;opacity:.75">{price_label}</span>
              <span class="fw-bold" style="font-size:1.75rem;line-height:1">{price}</span>
            </div>
            {provision_block(item, light=True)}
          </div>
        </div>
        <span class="badge bg-dark bg-opacity-75 text-white position-absolute" style="top:1rem;right:1rem;font-size:.75rem;z-index:3">1 / {n}</span>
      </div>
    </div>
    <div class="col-12 col-md-4 immo-detail-thumbcol">
      <div class="immo-detail-thumbgrid immo-detail-thumbgrid--4">{thumbs}</div>
    </div>
  </div>
</div>

<section class="pb-5">
  <div class="container-wide">
    <div class="row g-4">
      <div class="col-12 col-lg-8">
        <div class="bg-white p-4 rounded shadow-sm">
          <div class="d-flex flex-wrap gap-4 text-muted mb-3 pb-3 border-bottom">
            <span class="d-inline-flex align-items-center gap-2">{ICON_AREA}<strong class="text-body">{area}</strong></span>
            <span class="d-inline-flex align-items-center gap-2">{ICON_ROOMS}<strong class="text-body">{rooms} Zi.</strong></span>
          </div>
          <div class="d-flex align-items-baseline justify-content-between gap-2 mb-4">
            <div>
              <div class="text-uppercase small text-muted" style="letter-spacing:.5px">{price_label}</div>
              <div class="fw-bold title-color" style="font-size:1.6rem;line-height:1.2">{price}</div>
              {provision_block(item)}
            </div>
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
    <div class="modal-content border-0">
      <div class="modal-header border-0">
        <h2 class="modal-title h6 text-white mb-0">{title}</h2>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Schließen"></button>
      </div>
      <div class="modal-body p-0">
        <div id="galleryCarousel" class="carousel slide" data-bs-ride="false">
          <div class="carousel-indicators">{indicators}</div>
          <div class="carousel-inner">{slides}</div>
          <button class="carousel-control-prev" type="button" data-bs-target="#galleryCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span><span class="visually-hidden">Zurück</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#galleryCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span><span class="visually-hidden">Weiter</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
(function(){{
  var modal = document.getElementById('galleryModal');
  if (!modal || !window.bootstrap) return;
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


def write_detail(item: dict, before: str, after: str) -> str:
    city = city_slug(item["location"])
    slug = f"{slugify(item['title'])}-{item['id']}"
    rel = f"/immobilien/{city}/{slug}.html"
    out = ROOT / "public" / "immobilien" / city / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    page = before + gallery_main(item) + after
    page = page.replace("Charmantes Familienhaus in Krefeld-Linn", item["title"])
    page = page.replace(
        "/immobilien/krefeld/charmantes-familienhaus-in-krefeld-linn-5835561.html",
        rel,
    )
    page = page.replace("5835561", item["id"])
    page = re.sub(
        r'<link rel="preload" as="image" href="/media/object-hero-780/[^"]+"[^>]*>',
        f'<link rel="preload" as="image" href="/media/object-hero-780/{item["id"]}_000.jpg" fetchpriority="high">',
        page,
        count=1,
    )
    out.write_text(page, encoding="utf-8")
    item["detail_href"] = rel
    print("detail", rel)
    return rel


def main() -> None:
    items = json.loads(DATA.read_text(encoding="utf-8"))
    before, after = load_shell()
    for item in items:
        oid = item["id"]
        if not item.get("local_images"):
            item["local_images"] = []
            for i in range(16):
                p = ROOT / "public" / "media" / "object-zoom-780" / f"{oid}_{i:03d}.jpg"
                if p.exists():
                    item["local_images"].append(f"/media/object-zoom-780/{oid}_{i:03d}.jpg")
        item["thumb0"] = f"/media/object-thumbnail-780/{oid}_000.jpg"
        item["thumb1"] = f"/media/object-thumbnail-780/{oid}_001.jpg"
        write_detail(item, before, after)

    DATA.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    text = INDEX.read_text(encoding="utf-8")
    marker = "Aktuelle Immobilien aus unserer Vermittlung"
    start = text.rfind("<section", 0, text.find(marker))
    end = text.find("</section>", text.find(marker)) + len("</section>")
    INDEX.write_text(text[:start] + build_section(items) + text[end:], encoding="utf-8")
    print("index refreshed, featured", FEATURED, "provision", PROVISION_NOTE)


if __name__ == "__main__":
    main()
