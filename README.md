# Immobilien Experten Local Reconstruction

Lokale Reproduktion aller öffentlichen Seiten von https://www.immobilien-experten.de/. Die Liste kommt aus der öffentlichen Sitemap.

Die Seite besteht aus dem gemessenen öffentlichen DOM, den originalen Stylesheets, Schriften und Bildern. Tracking und echte Formularanfragen sind entfernt. Eine Neuinterpretation in eigenen Komponenten würde die gemessenen Abstände verändern, deshalb bleibt das Markup erhalten und wird lokal ausgeliefert.

## Installation

```bash
npm install
pip install playwright beautifulsoup4 requests pillow lxml
python -m playwright install chromium
```

## Development

```bash
npm run dev
```

Lokal: http://127.0.0.1:5173/

## Build

```bash
npm run build
npm run preview
```

## Analyse

```bash
python scripts/mirror_frontend.py
python scripts/export_form_flow.py
python scripts/inspect_interactions.py
```

Ergebnisse liegen in `analysis/`:

- `network.json`
- `assets.json`
- `styles.json`
- `geometry.json`
- `form-flow.json`
- `interactions.json`

## Screenshot Tests

```bash
python scripts/capture_reference.py
python scripts/capture_local.py
python scripts/compare_screenshots.py
```

Ordner:

- `reference/` und `screenshots/original/`
- `screenshots/local/`
- `screenshots/diff/`

## Projektstruktur

```text
index.html          gemessene Homepage, Tracking entfernt
public/             Schriften, Bilder, CSS, JS, PDFs
src/guards.ts       zusätzliche lokale Request-Sperre
scripts/            Audit, Spiegel, Screenshots, Diff
analysis/           Messwerte
reference/          Original-Screenshots
screenshots/        Lokal, Originalkopie, Diff
```

## Assets

Öffentliche Same-Origin-Dateien liegen unter `public/` und werden über dieselben Root-Pfade geladen (`/media`, `/theme`, `/assets`, `/images`). Mapping: `analysis/assets.json`.

Schriften: Lato und Roboto als lokale WOFF2, plus Icon-Font.

## Externe Funktionen

Diese Funktionen rufen das Originalsystem nicht auf:

- Formular: `preventDefault`, Anzeige `Demo submission successful`
- Kontakt-Widget: lokale Hinweiskarte, kein POST
- Service-PIN-Polling: deaktiviert
- Google Tag Manager, Analytics und ähnliche Tracker: entfernt

Navigation bleibt auf den lokalen Seiten. Formulare auf allen Seiten werden lokal abgefangen und nicht versendet.

## Seiten

21.795 HTML-Seiten aus der Sitemap liegen unter `public/`, die Startseite zusätzlich als `index.html`.

```text
19640 regionen
 2000 immopedia
   64 kontakt
   55 immobilien
    8 leistungen
    6 ratgeber
    3 service
    2 ueber-uns
 plus Impressum, Datenschutz, Whitepaper, Downloads, Service, Ratgeber
```

Neue Seiten erneut holen:

```bash
python scripts/list_sitemap.py
python scripts/mirror_pages.py
python scripts/rewrite_local_urls.py
```

## Bekannte Abweichungen

- Seitenhöhen stimmen in allen geprüften Viewports überein.
- Pixelabweichung der Full-Page-Screenshots liegt zwischen 0,037 % und 0,443 %. Der Rest ist vor allem Schriftrasterung und der Zeitpunkt des Personen-Rotors.
- Vier Theme-Hintergrundbilder antworten auch auf der Originalseite mit 404 und fehlen lokal ebenfalls.
- Das schwebende Kontaktfenster ist nur die lokale Ansicht, nicht das serverseitig nachgeladene Widget.
- Kartenkacheln auf Exposés können weiterhin vom Kartenanbieter geladen werden.
- Seiten, die nicht in der öffentlichen Sitemap stehen, sind nicht enthalten.
