from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")
text = re.sub(
    r'(fetchpriority="high" height=")\d+(" loading="eager" src="/media/oberholz-team/michael-oberholz\.png" width=")\d+"',
    r'\g<1>1200\g<2>900"',
    text,
    count=1,
)
path.write_text(text, encoding="utf-8")
match = re.search(r"<img[^>]*michael-oberholz[^>]*>", text)
print(match.group(0) if match else "missing")
