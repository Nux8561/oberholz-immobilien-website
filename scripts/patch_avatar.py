from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
old = 'alt="Kersten Streit" class="img-rounded" fetchpriority="high" src="/media/videocard_avatar/streit_facepile.jpg"'
new = 'alt="Michael Oberholz" class="img-rounded" fetchpriority="high" src="/media/videocard_avatar/oberholz_facepile.jpg"'
if old not in text:
    raise SystemExit("missing avatar markup")
path.write_text(text.replace(old, new), encoding="utf-8")
print("ok")
