# Oberholz Immobilien – Website

React + Vite + TypeScript. Marke, Texte, Fotos, Objekte und PDFs stammen von Oberholz Immobilien
(Hauptstandorte Essen und Münster). Preview: `https://oberholz-immobilien.pages.dev`.

```bash
npm install
npm run dev              # http://localhost:5173
npm run build
npm test                 # Funktionstests (Dev-Server muss laufen)
npm run check:links      # crawlt alle internen Links, 404/Konsole/Overflow 390px → analysis/link-check.json
npm run build:seo        # Produktions-Build + Prerendering, sitemap.xml, robots.txt → dist/
```

Übergabe, Livegang und Kunden-Checkliste: **ÜBERGABE.md**.

## Seiten (verschlankt, Übersicht: SEITENSTRUKTUR.md)

| Bereich | Routen |
| --- | --- |
| Startseite | `/` |
| Immobilien | `/immobilien/kaufen` · `/immobilien/mieten` (Filter, Kapitalanlage `?anlage=1`, KI-Freitextsuche, Karte, Suche speichern) · `/expose/:id` (aktueller ImmoScout-Bestand) · `/kapitalanlage` · `/finanzierung` |
| Verkaufen | `/verkaufen` · `/bewertung` (Funnel) · `/vermieten` · `/rueckmietverkauf` · `/immotipp` |
| Über uns | `/ueber-uns` (+ `#team`, `#qualifikation`, `#qualitaet`, `#partner`) · `/regionen` (Standorte) · `/regionen/essen` · `/regionen/bochum` (+ je `/verkaufen`, `/immobilienbewertung`, `/wohnung-verkaufen`) · `/kontakt` |
| Ratgeber | `/ratgeber` (+ `#rechner`, `#downloads`) · `/ratgeber/thema/:kategorie` · `/ratgeber/:slug` (23 Artikel) · `/whitepaper/:slug` (6 Leitfäden) · `/service/budgetrechner` · `/service/finanzierungsrechner` · `/service/wert-hebel-rechner` · `/immopedia` · `/immopedia/:slug` (1.999 Begriffe) |
| Sonstiges | `/mein-bereich` (Merkliste, gespeicherte Suchen) · `/impressum` · `/datenschutz` · `/cookie-hinweise` |

Zusammengelegt (17.10.2026, leiten weiter): `/leistungen` und `/vermarktung` → `/verkaufen`, `/wohnung-kaufen` → Suche mit `typ=Wohnung`, `/service` → `/ratgeber#rechner`, `/downloads` → `/ratgeber#downloads`, `/ueber-uns/qualifikation` und `/ueber-uns/iso-9001` → `/ueber-uns`, `/kontakt/:stadt` → `/regionen/:stadt`.
Alte Pfade der ersten Template-Version (`/standorte`, `/stadt/:city`, `/magazin`, `/commercial`, `/makler-werden`) leiten weiter.

## Daten

- `src/data/content.ts` – Marke, Team, Büros, Menüs, Startseite, Footer
- `src/data/routes.ts` – alle Routen
- `src/data/properties.ts` + `listings.json` – Objekte (Fotos: `public/assets/oberholz/objekte/`). Abgleich mit ImmoScout24: `python3 scripts/import_immoscout.py` liest das Homepage-Modul der bisherigen Website (Ergebnisliste 82828525), übernimmt Texte, Eckdaten, bis zu 12 Fotos und den Ansprechpartner und löscht Fotos nicht mehr angebotener Objekte. Danach `npm run build:seo`. Regionen-Zuordnung der Orte: `REGION_GROUPS` in `properties.ts`.
- `src/data/oberholz/content.json` – übernommene Seiteninhalte (Blöcke), FAQs; Zugriff über `src/data/oberholz/index.ts`
- `src/data/ownerContent.ts` – redaktionelle Eigentümertexte für Essen und Bochum: Makler, Hausverkauf, Immobilienbewertung und Wohnungsverkauf. Diese Texte und FAQs werden für die lokalen Seiten anstelle der importierten Regions-Blöcke verwendet.
- `src/pages/oberholz/LocalOwner.tsx` – lokale Bewertung und Wohnungsverkauf sowie gemeinsame Eigentümer- und Ratgeber-Verlinkung. Neue Routen: `/regionen/essen/immobilienbewertung`, `/regionen/bochum/immobilienbewertung`, `/regionen/essen/wohnung-verkaufen`, `/regionen/bochum/wohnung-verkaufen`.
- `src/data/ratgeber/*.ts` – eigene Ratgeber-Artikel der Redaktion (Aufbau wie E&V-Ratgeber: Lesezeit, Inhaltsverzeichnis, „Das Wichtigste in Kürze“, Tabellen, FAQ)
- `public/assets/oberholz/media/team/` – Teamfoto und Gesichtsausschnitte, erzeugt mit `scripts/compose_team.py`
- `public/data/immopedia/` – Glossar (Index + je Begriff eine JSON-Datei, wird bei Bedarf geladen)
- `public/downloads/` – PDFs

Neu erzeugen: `scripts/crawl_oberholz.py` → `extract_*.py` → `build_oberholz_content.py`.

## Kontakt-Widget, WhatsApp, Partner

- `src/components/ContactWidget/` – Pop-up unten rechts (Anfrage, Anrufen, Rückruf, WhatsApp, Kontakt) und Handy-Kontaktleiste; `openContact(tab)` öffnet es von überall.
- WhatsApp-Links über `whatsappUrl(text)` aus `src/data/content.ts` (`brand.whatsapp` = Mobilnummer Felix Lesch 0179 4468850).
- Rufnummern: zentral `brand.phoneDisplay` (Essen 0201 61447786); `brand.phoneMuensterDisplay` (0251 28 42 90 90) nur für reine Münster-Inhalte (Büro Münster, Münster-Objekte, Impressum als Zusatz).
- Ansprechpartner je Objekt: Feld `agent` aus dem ImmoScout-Exposé, überschreibbar über `listingAgents` in `src/data/content.ts` (ohne Angabe: Felix Lesch). Hat das Teammitglied eine eigene Nummer (`phoneDisplay` in `team`, derzeit Michael Penn), zeigt das Exposé diese statt der zentralen Nummer.
- `src/components/Partners/` – Logo-Raster aus `partners` (Kooperation, Finanzierung, Portale).

## Formulare

Formulare posten an `/api/contact` (`functions/api/contact.js`, Cloudflare Pages Function + Resend).
Erfolg wird erst nach HTTP-2xx angezeigt. Zur Aktivierung in den Pages-Secrets setzen:
`RESEND_API_KEY` (Pflicht), optional `CONTACT_TO` (Standard `mail@oberholz-immobilien.com`) und `CONTACT_FROM`
(verifizierte Absenderadresse in Resend). Ohne Key antwortet die Function mit 503 und verständlicher Fehlermeldung.
Merkliste/Suchen liegen nur im `localStorage`.

## Design-Tokens

`src/styles/tokens.css`: Akzent Dunkelblau `#1f3a5f`, Button `#1a3253`, Hausschriften Oberholz Antiqua 600 / Oberholz Grotesk 400–700 (siehe `brand/`), Breakpoints 600 / 960 / 1240 px.

## Audit & Vergleich

`scripts/` enthält Audit-, Extraktions- und Prüfskripte (Python + Playwright + Pillow), u. a. `capture_reference.py`,
`visual_diff.py`, `test_functional.py`, `check_links.py`. Messdaten/Screenshots liegen in `reference/` und `analysis/`.

## Abnahmeüberarbeitung 16.10.2026

- Startseite, lokale Einstiege, Verkauf, Bewertung und Kontakt gestrafft und überarbeitet.
- Sichtbare FAQ und Strukturdaten stimmen überein; gefilterte Suchseiten sind im Browser noindex.
- `npm run build:seo` rendert alle 1.999 Lexikon-Einträge mit und erstellt 2.089 Sitemap-Ziele sowie echte 404-/301-Ausgaben.
- `scripts/build_guides.py` erstellt sechs PDF-Lesefassungen vorhandener Ratgeber; die fertigen Dateien liegen in `public/downloads/leitfaeden/`. `src/data/guideFiles.json` enthält die tatsächlichen Seitenzahlen.
- Die pages.dev-Vorschau ist per HTTP-Header noindex. Die vorgesehene Hauptdomain ist noch nicht am Cloudflare-Projekt nachgewiesen.
- Verbindlicher Überblick über Funktionen und offene Livegang-Punkte: `ÜBERGABE.md`. Formularzustellung, Firmierung und Öffnungszeiten werden dort ausdrücklich nicht als erledigt dargestellt.
