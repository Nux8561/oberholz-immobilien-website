"""Rewrite absolute public site URLs to local root paths."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLES = (
    "https://www.immobilien-experten.de",
    "http://www.immobilien-experten.de",
    "https://immobilien-experten.de",
    "http://immobilien-experten.de",
    "//www.immobilien-experten.de",
)


def rewrite(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    original = text
    for needle in NEEDLES:
        text = text.replace(needle, "")
    if text != original:
        path.write_text(text, encoding="utf-8")
        return 1
    return 0


def main() -> None:
    files = list((ROOT / "public").rglob("*.html"))
    files.append(ROOT / "index.html")
    changed = 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(rewrite, path) for path in files]
        done = 0
        for future in as_completed(futures):
            changed += future.result()
            done += 1
            if done % 2000 == 0:
                print("checked", done, "changed", changed, flush=True)
    print("checked", len(files), "changed", changed, flush=True)


if __name__ == "__main__":
    main()
