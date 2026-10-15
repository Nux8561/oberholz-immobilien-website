"""Erzeugt aus analysis/engelvoelkers/dom_<w>.json eine kompakte, lesbare Geometrie-/Style-Übersicht."""
import json, sys
from pathlib import Path
from _common import ANA

KEYS = ['font-family','font-size','font-weight','line-height','letter-spacing','text-transform','color','background-color',
        'padding','margin','gap','border','border-bottom','border-radius','box-shadow','grid-template-columns','max-width','aspect-ratio','object-fit','transition']

def fmt_s(s):
    out=[]
    for k in KEYS:
        v=s.get(k)
        if v is None: continue
        if k=='font-family': v=v.split(',')[0].replace('"','').replace('Engel Voelkers ','EV ')
        if k=='border' and v.startswith('0px'): continue
        if k=='border-bottom' and v.startswith('0px'): continue
        if k in ('margin','padding') and v in ('0px','0px 0px'): continue
        if k=='transition' and v=='all': continue
        out.append(f"{k}={v}")
    return ' '.join(out)

def walk(n, depth, lines, parent_text_style=None):
    r=n['r']; tag=n['tag']
    interesting = n.get('text') or tag in ('img','input','button','a','h1','h2','h3','h4','p','section','svg','picture','video','ul','li','nav','header','footer','label','span') or depth<3
    s=n.get('s',{})
    if interesting:
        cls=n.get('cls','').split(' ')[0][:40]
        extra=''
        for a in ('text','aria-label','placeholder','alt','href'):
            if n.get(a): extra+=f' {a}="{n[a][:70]}"'
        if tag=='img': extra+=f" natural={n.get('natural')} src={str(n.get('currentSrc'))[-70:]}"
        lines.append(f"{'  '*depth}<{tag}.{cls}> [{r['x']},{r['y']} {r['w']}x{r['h']}]{extra}  {fmt_s(s) if (n.get('text') or tag in ('img','button','input','a','section','h1','h2','h3','p','li','ul','div')) else ''}")
    for c in n.get('c',[]): walk(c, depth+1, lines)

arg = sys.argv[1] if len(sys.argv)>1 else '1440'
src = Path(arg) if arg.endswith('.json') else ANA/f"dom_{arg}.json"   # Breite oder Pfad zu einer Unterseiten-JSON
d=json.load(open(src))
lines=[f"viewport {d['viewport']} scrollHeight {d['scrollHeight']}"]
lines.append("=== HEADER ==="); walk(d['header'],0,lines) if d['header'] else None
for i,s in enumerate(d['sections']):
    lines.append(f"=== SECTION {i} ==="); walk(s,0,lines)
lines.append("=== FOOTER ==="); walk(d['footer'],0,lines) if d['footer'] else None
out = src.with_suffix('.txt') if arg.endswith('.json') else ANA/f"geometry_{arg}.txt"
out.write_text('\n'.join(lines))
print(len(lines), "lines ->", out)
