from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
old = (
    '<div class="text-center d-block"> '
    '<span class="text-muted">Service-PIN: '
    '<strong class="text-md" style="font-family:\'Courier New\',Courier,monospace;">EE36AKY</strong>'
    "</span> </div>"
)
if old not in text:
    raise SystemExit("Service-PIN block not found")
path.write_text(text.replace(old, "", 1), encoding="utf-8")
print("removed", "Service-PIN" in path.read_text(encoding="utf-8"))
Path("scripts/_pin.txt").unlink(missing_ok=True)
