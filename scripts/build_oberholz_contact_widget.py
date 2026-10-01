#!/usr/bin/env python3
"""Restore original contact widget HTML adapted for Oberholz Immobilien."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts" / "_cw_original_widget.html"
OUT = ROOT / "public" / "theme" / "contact-widget.html"

REPLACEMENTS = [
    ("Immobilien Experten", "Oberholz Immobilien"),
    ("Kersten Streit", "Michael Oberholz"),
    ("info@immobilien-experten.de", "mail@oberholz-immobilien.com"),
    ("kundenservice@ee-experten.com", "mail@oberholz-immobilien.com"),
    ("tel:+498002203330", "tel:+4925128429090"),
    ("tel:+4907117697724", "tel:+4925128429090"),
    ("0800 - 220 33 30", "0251 28 42 90 90"),
    ("0800&nbsp;-&nbsp;220&nbsp;33&nbsp;30", "0251&nbsp;28&nbsp;42&nbsp;90&nbsp;90"),
    ("/media/facepile/2_1.jpg", "/media/facepile/oberholz_facepile.jpg"),
    ("/media/facepile/team_holecek.jpg", "/media/oberholz-team/michael-oberholz.png"),
    ("/media/facepile/team_schorpp.jpg", "/media/oberholz-team/felix-lesch.png"),
    ("https://wa.me/49?", "https://wa.me/4925128429090?"),
    ("ee-experten", "oberholz-immobilien"),
]

# Local form submit: show success without remote API
FORM_PATCH = r"""
/* Oberholz local form shim */
(function () {
  var nativeFetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    var url = typeof input === "string" ? input : (input && input.url) || "";
    if (/rex-api-call=send_form_data/.test(url)) {
      return Promise.resolve(new Response(JSON.stringify({ success: true, message: "ok" }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      }));
    }
    return nativeFetch(input, init);
  };
})();
"""


def adapt(html: str) -> str:
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)

    # Ensure absolute media paths
    html = html.replace('src="media/', 'src="/media/')
    html = html.replace("src='media/", "src='/media/")

    # Inject form shim before widget script closes
    if "Oberholz local form shim" not in html:
        html = re.sub(
            r"(<script>)",
            r"\1" + FORM_PATCH,
            html,
            count=1,
        )
    return html


def main() -> None:
    raw = SRC.read_text(encoding="utf-8")
    adapted = adapt(raw)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(adapted, encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), "bytes", len(adapted))
    for needle in [
        "Oberholz Immobilien",
        "0251 28 42 90 90",
        "mail@oberholz-immobilien.com",
        "cwOpen",
        "cw-backdrop",
        "cw-panel",
        "Immobilien Experten",
        "0800",
    ]:
        print(needle, adapted.count(needle))


if __name__ == "__main__":
    main()
