"""Erzeugt sechs lesbare PDF-Fassungen der vorhandenen Original-Ratgeber.
Keine neuen Fachbehauptungen; Umfangsangaben werden aus den PDFs ermittelt.
"""
import json, re
from html import escape
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
import reportlab

ROOT = Path(__file__).resolve().parent.parent
PAGES = json.loads((ROOT/'src/data/oberholz/content.json').read_text())['pages']
FONTS=Path(reportlab.__file__).parent/'fonts'
pdfmetrics.registerFont(TTFont('OberholzText',str(FONTS/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('OberholzBold',str(FONTS/'VeraBd.ttf')))
pdfmetrics.registerFontFamily('OberholzText',normal='OberholzText',bold='OberholzBold')
OUT=ROOT/'public/downloads/leitfaeden';OUT.mkdir(parents=True,exist_ok=True)
GUIDES={
'generationenwechsel': ('whitepaper-generationenwechsel','der-grosse-generationenwechsel-was-der-silver-tsunami-fuer-immobilienverkaeufer-bedeutet'),
'erben-kompass': ('erben-kompass','immobilie-geerbt-der-erben-kompass-fuer-die-ersten-wochen'),
'sanieren-vor-dem-verkauf': ('whitepaper-sanieren-vor-dem-verkauf','erst-sanieren-dann-verkaufen-was-sich-wirklich-rechnet'),
'unterlagen-und-finanzierung': ('whitepaper-unterlagen-und-finanzierung','warum-ihre-unterlagen-ueber-die-finanzierung-ihrer-kaeufer-entscheiden'),
'leerstand-vermietung-oder-verkauf': ('whitepaper-leerstand-vermietung-oder-verkauf','leerstand-vermietung-oder-verkauf-eine-ehrliche-abwaegung'),
'wohnwechsel-im-alter': ('whitepaper-wohnwechsel-im-alter','haus-zu-gross-wie-der-wechsel-in-die-altersgerechte-wohnung-gelingt'),
}
STYLES={
'eyebrow': ParagraphStyle('eyebrow',fontName='OberholzBold',fontSize=9,leading=13,textColor=HexColor('#b3261e'),spaceAfter=16),
'h1': ParagraphStyle('h1',fontName='Times-Bold',fontSize=27,leading=32,textColor=HexColor('#262626'),spaceAfter=18),
'h2': ParagraphStyle('h2',fontName='Times-Bold',fontSize=18,leading=22,spaceBefore=16,spaceAfter=8,keepWithNext=True),
'h3': ParagraphStyle('h3',fontName='OberholzBold',fontSize=11,leading=16,spaceBefore=14,spaceAfter=7,keepWithNext=True),
'p': ParagraphStyle('p',fontName='OberholzText',fontSize=10,leading=15,spaceAfter=8),
'intro': ParagraphStyle('intro',fontName='OberholzText',fontSize=12,leading=19,spaceAfter=18),
'small': ParagraphStyle('small',fontName='OberholzText',fontSize=8,leading=12,spaceAfter=8,textColor=HexColor('#555555')),
}
def para(text,kind='p'):
    text=re.sub(r'[\u2010-\u2015]','-',text)
    return Paragraph(escape(text).replace('\n','<br/>'),STYLES[kind])
def decorate(c,doc):
    w,h=doc.pagesize
    c.setStrokeColor(HexColor('#b3261e'));c.setLineWidth(1.5);c.line(48,h-39,w-48,h-39)
    c.setFillColor(HexColor('#262626'));c.setFont('OberholzBold',9);c.drawString(48,h-29,'OBERHOLZ IMMOBILIEN')
    c.setFillColor(HexColor('#666666'));c.setFont('OberholzText',8)
    c.drawString(48,30,'Ratgeber | Essen - Bochum - Münsterland')
    c.drawRightString(w-48,30,str(doc.page))
manifest={}
for slug,(wp,article) in GUIDES.items():
    b=PAGES[wp]['blocks'];title=next(x['text'] for x in b if x['t']=='h1');intro=next(x['text'] for x in b if x['t']=='p')
    original=PAGES['ratgeber-'+article]['blocks']
    at=next(i for i,x in enumerate(original) if x['t']=='h2' and x['text']=='Inhaltsverzeichnis')
    body=[]
    for x in original[at+2:]:
        if x['t']=='h2' and re.search(r'komplette.*Download|als Download|Weitere Artikel',x['text'],re.I): break
        if x['t']=='ul' and x.get('items',[None])[0]=='Teilen:': break
        body.append(x)
    story=[para('KOSTENLOSER LEITFADEN - PDF-LESEFASSUNG','eyebrow'),para(title,'h1'),para(intro,'intro')]
    for x in body:
        if x['t'] in ('h2','h3','p','blockquote'):
            text=x['text']
            if re.match(r'ZUM .*DOWNLOAD|WHITEPAPER ',text): continue
            story.append(para(text,x['t'] if x['t'] in ('h2','h3') else 'p'))
        elif x['t'] in ('ul','ol'):
            for text in x['items']: story.append(para('- '+text))
        elif x['t']=='table':
            for row in x.get('rows',[]): story.append(para(' | '.join(row)))
    if slug in ('sanieren-vor-dem-verkauf','generationenwechsel'):
        story.extend([para('Zur Markteinordnung: immowelt-Pressemitteilung vom 19. März 2026, Energieeffizienz und Angebotspreise. Die Analyse bezieht sich auf bundesweite Angebote und ersetzt keine Bewertung des einzelnen Objekts.','small')])
    story.extend([para('Zum Weiterdenken','h2'),para('Notieren Sie Ihre offenen Fragen und bringen Sie vorhandene Unterlagen zum persönlichen Gespräch mit. Wir besprechen mit Ihnen, welche nächsten Schritte zu Ihrer Immobilie passen.'),para('Persönlicher Kontakt','h3'),para('Oberholz Immobilien | 0251 28 42 90 90 | mail@oberholz-immobilien.com'),para('PDF-Lesefassung des bestehenden Ratgeberbeitrags. Individuelle Rechts- und Steuerfragen klären Sie bitte mit Ihrer Rechts- beziehungsweise Steuerberatung.','small'),para('Online weiterlesen: www.oberholz-immobilien.com/ratgeber/'+article,'small')])
    path=OUT/(slug+'.pdf')
    doc=SimpleDocTemplate(str(path),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=60,bottomMargin=46,title=title,author='Oberholz Immobilien')
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
    reader=PdfReader(path)
    assert all(len(p.extract_text().strip())>100 for p in reader.pages)
    manifest[slug]={'href':'/downloads/leitfaeden/'+slug+'.pdf','pages':len(reader.pages),'sizeKB':round(path.stat().st_size/1024)}
(ROOT/'src/data/guideFiles.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
