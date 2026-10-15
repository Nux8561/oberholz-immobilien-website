# Oberholz Immobilien – Website

React + Vite + TypeScript. Aufbau, Abstände, Breakpoints und Interaktionen folgen dem per Playwright vermessenen
Seitenmuster von `engelvoelkers.com/de/de` (rote Akzentfarbe). Marke, Texte, Fotos, Objekte und PDFs stammen von der
bisherigen Oberholz-Website (`oberholz-immobilien.pages.dev`); von Engel & Völkers sind keine Inhalte, Bilder oder Fonts übernommen.

```bash
npm install
npm run dev              # http://localhost:5173
npm run build
npm test                 # Funktionstests (Dev-Server muss laufen)
npm run check:links      # crawlt alle internen Links, 404/Konsole/Overflow 390px → analysis/link-check.json
npm run build:seo        # Produktions-Build + Prerendering, sitemap.xml, robots.txt → dist/
```

Übergabe, Livegang und Kunden-Checkliste: **ÜBERGABE.md**.

## Seiten (71 Routen + Immopedia)

| Bereich | Routen |
| --- | --- |
| Startseite | `/` |
| Immobilien | `/immobilien/kaufen` · `/immobilien/mieten` (Filter, Kapitalanlage `?anlage=1`, KI-Freitextsuche, Karte, Suche speichern) · `/expose/:id` (21 echte Objekte) |
| Leistungen | `/leistungen` · `/verkaufen` · `/bewertung` (Funnel) · `/vermieten` · `/rueckmietverkauf` · `/finanzierung` · `/vermarktung` · `/kapitalanlage` · `/wohnung-kaufen` · `/immotipp` |
| Service | `/service` · `/service/budgetrechner` · `/service/finanzierungsrechner` · `/service/wert-hebel-rechner` |
| Wissen | `/ratgeber` · `/ratgeber/thema/:kategorie` (Käufer, Verkäufer, Eigentümer & Erben) · `/ratgeber/:slug` (23 Artikel) · `/whitepaper/:slug` (6 Leitfäden) · `/downloads` (11 PDFs) · `/immopedia` · `/immopedia/:slug` (1.999 Begriffe) |
| Unternehmen | `/ueber-uns` (+ `#team`) · `/ueber-uns/qualifikation` · `/ueber-uns/iso-9001` · `/kontakt` · `/kontakt/:stadt` · `/regionen` · `/regionen/:stadt` · `/regionen/:stadt/verkaufen` (Münster, Essen, Bochum) |
| Sonstiges | `/mein-bereich` (Merkliste, gespeicherte Suchen) · `/impressum` · `/datenschutz` · `/cookie-hinweise` |

Alte Pfade der ersten Template-Version (`/standorte`, `/stadt/:city`, `/magazin`, `/commercial`, `/makler-werden`) leiten weiter.

## Daten

- `src/data/content.ts` – Marke, Team, Büros, Menüs, Startseite, Footer
- `src/data/routes.ts` – alle Routen
- `src/data/properties.ts` + `listings.json` – Objekte (Fotos: `public/assets/oberholz/objekte/`)
- `src/data/oberholz/content.json` – übernommene Seiteninhalte (Blöcke), FAQs; Zugriff über `src/data/oberholz/index.ts`
- `src/data/ratgeber/*.ts` – eigene Ratgeber-Artikel der Redaktion (Aufbau wie E&V-Ratgeber: Lesezeit, Inhaltsverzeichnis, „Das Wichtigste in Kürze“, Tabellen, FAQ)
- `public/assets/oberholz/media/team/` – Teamfoto und Gesichtsausschnitte, erzeugt mit `scripts/compose_team.py`
- `public/data/immopedia/` – Glossar (Index + je Begriff eine JSON-Datei, wird bei Bedarf geladen)
- `public/downloads/` – PDFs

Neu erzeugen: `scripts/crawl_oberholz.py` → `extract_*.py` → `build_oberholz_content.py`.

## Kontakt-Widget, WhatsApp, Partner

- `src/components/ContactWidget/` – Pop-up unten rechts (Anfrage, Anrufen, Rückruf, WhatsApp, Kontakt) und Handy-Kontaktleiste; `openContact(tab)` öffnet es von überall.
- WhatsApp-Links über `whatsappUrl(text)` aus `src/data/content.ts` (`brand.whatsapp`).
- `src/components/Partners/` – Logo-Raster aus `partners` (Kooperation, Finanzierung, Portale).

## Formulare

Es gibt keinen Server: Formulare (Kontakt, Funnel, Exposé-Anfrage, Immotipp, Whitepaper, Wert-Hebel) prüfen die
Eingaben und bereiten danach eine E-Mail an `mail@oberholz-immobilien.com` vor (`src/lib/mail.ts`, mailto).
Für den Livebetrieb dort ein Formular-Backend anbinden. Merkliste/Suchen liegen nur im `localStorage`.

## Design-Tokens

`src/styles/tokens.css`: Akzent Rot `#e60000`, Button `#c80000`, Spectral 600 / Inter Tight, Breakpoints 600 / 960 / 1240 px.

## Audit & Vergleich

`scripts/` enthält Audit-, Extraktions- und Prüfskripte (Python + Playwright + Pillow), u. a. `capture_reference.py`,
`visual_diff.py`, `test_functional.py`, `check_links.py`. Messdaten/Screenshots liegen in `reference/` und `analysis/`.
