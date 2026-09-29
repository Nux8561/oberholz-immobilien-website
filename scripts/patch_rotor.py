"""Point the homepage hero rotor at the Oberholz portraits."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

PEOPLE = (
    ("michael-oberholz.png", "Michael Oberholz", "Inhaber &amp; Sachverständiger", 768, 1024),
    ("felix-lesch.png", "Felix Lesch", "Immobilienberater", 768, 1024),
    ("michael-penn.png", "Michael Penn", "Immobilienberater", 768, 1024),
    ("pascal-kopp.png", "Pascal Kopp", "Transaktionsberater", 768, 1024),
    ("lubka-roeger.png", "Lubka Röger", "Immobilienberaterin", 768, 1024),
)


def slide(filename: str, name: str, role: str, width: int, height: int, active: bool) -> str:
    state = " is-active" if active else ""
    alt = f"{name} - {role}"
    src = f"/media/oberholz-team/{filename}"
    return (
        f'<div class="regio-rotor-slide{state}">'
        f'<picture><img alt="{alt}" class="img-fluid" decoding="async" '
        f'fetchpriority="{"high" if active else "auto"}" height="{height}" '
        f'loading="{"eager" if active else "lazy"}" src="{src}" width="{width}"/>'
        f"</picture></div>"
    )


def flag(name: str, role: str, active: bool) -> str:
    state = " is-active" if active else ""
    return (
        f'<div class="regio-rotor-flag{state}">'
        f'<span class="h3 text-white fw-semibold">{name}</span>'
        f'<span class="d-block text-white">{role}</span></div>'
    )


def replace_once(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.find(start_marker)
    if start < 0:
        raise SystemExit(f"missing start marker: {start_marker[:40]}")
    end = text.find(end_marker, start)
    if end < 0:
        raise SystemExit(f"missing end marker after {start_marker[:40]}")
    return text[:start] + replacement + text[end:]


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    slides = "".join(
        slide(filename, name, role, width, height, index == 0)
        for index, (filename, name, role, width, height) in enumerate(PEOPLE)
    )
    flags = "".join(
        flag(name, role, index == 0)
        for index, (_filename, name, role, _width, _height) in enumerate(PEOPLE)
    )
    start_marker = '<div class="image-only col-lg-5 position-relative d-flex justify-content-center bannerright align-items-end mt-4 mt-lg-0">'
    end_marker = "</section><style>.regio-rotor{display:grid"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise SystemExit("hero markers are not unique")
    block = (
        start_marker
        + ' <div class="flag-content flag-brush position-absolute ms-5 ms-md-0 mb-5 start-0 bottom-0 z-3 regio-rotor-flags"> '
        + flags
        + ' </div> <div class="image-wrapper regio-rotor"> '
        + slides
        + " </div> </div> </div> </div>"
    )
    text = replace_once(text, start_marker, end_marker, block)
    if "t7a7913" in text or "/media/bannerright-780/" in text[text.find(start_marker) : text.find(end_marker)]:
        raise SystemExit("old rotor images still in the hero")
    INDEX.write_text(text, encoding="utf-8")
    print("patched")


if __name__ == "__main__":
    main()
