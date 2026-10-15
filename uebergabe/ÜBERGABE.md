# Übergabe – Website Oberholz Immobilien

Stand: 15.10.2026 · Technik: React + Vite + TypeScript, statisch vorgerendert (kein Server, keine Datenbank nötig)

## 1. Ansehen

```bash
npm install
npm run dev          # http://localhost:5173
```

Fertige Website zum Hochladen: Ordner **`dist/`** (bzw. `uebergabe/oberholz-website-dist.zip`).

## 2. Veröffentlichen (Livegang)

1. **Domain prüfen:** `src/data/routes.ts` → `SITE_URL` (aktuell `https://www.oberholz-immobilien.com`). Bei anderer Domain dort ändern, außerdem in `index.html` (Strukturdaten) und `public/llms.txt`.
2. **Bauen:** `npm run build:seo` → erzeugt `dist/` mit 91 vorgerenderten Seiten, `sitemap.xml` (2.088 URLs), `robots.txt`, `llms.txt`.
3. **Hochladen:** Inhalt von `dist/` bei einem statischen Hoster (z. B. Netlify oder Cloudflare Pages – beide lesen die mitgelieferte Datei `_redirects`, damit jede Unterseite direkt aufrufbar ist). Bei einem klassischen Webhoster (Apache) stattdessen eine `.htaccess` mit Fallback auf `/app.html` anlegen.
4. **Google:** Search Console einrichten, `sitemap.xml` einreichen; im Google-Unternehmensprofil die neue Website hinterlegen. Optional Bing Webmaster Tools.
5. **Datenschutzerklärung:** Hoster-Abschnitt (bisher „Timme Hosting“) an den tatsächlichen Hoster anpassen.

## 3. Was die Website kann

- **Alle Seiten** der bisherigen Oberholz-Website im neuen Design (Aufbau nach dem Muster großer Maklerseiten, rote Akzentfarbe, eigene Texte und Bilder) – 71 Routen + Immopedia mit 1.999 Begriffen. Jeder Link führt auf eine echte Seite (Crawler: 131 Seiten, 0 Fehler).
- **Kontakt-Pop-up wie auf der alten Seite:** runder Button mit Michael Oberholz unten rechts (nach dem ersten Scrollen), Hinweis „Kostenlose Erstberatung“, Reiter *Anfrage · Anrufen · Rückruf · WhatsApp · Kontakt*. Auf dem Handy feste Leiste unten: *Anrufen · WhatsApp · Beratung*.
- **WhatsApp** (wa.me/4925128429090) im Pop-up, in der Handy-Leiste, im Footer, auf der Startseite, der Kontaktseite und in jedem Exposé (mit Objektnummer vorausgefüllt).
- **Partner & Kooperationen:** DVAG, Swiss Life, Interhyp (verlinkt) im Footer und auf „Über uns“ (`/ueber-uns#partner`), Finanzierungspartner auf Finanzierung und Finanzierungsrechner, Portale auf Verkaufen/Vermarktung.
- **Google-Bewertungen:** Sterne im Header, auf der Startseite und im Pop-up → Bewertungsübersicht → Google-Profil.
- **Immobiliensuche** mit Filtern, Karte, Merkliste, gespeicherten Suchen und **KI-Suche** (Freitext wie „3-Zimmer-Wohnung in Münster mit Balkon bis 350.000 €“ wird lokal in Filter übersetzt).
- **Funnel** Bewertung/Verkauf/Vermietung, **Rechner** (Budget, Finanzierung, Wert-Hebel), **Ratgeber** (23 Artikel mit Team-Autorenprofilen), Whitepaper, Downloads (11 PDFs).
- **Rechtliches:** Impressum (Daten der bisherigen Seite, § 5 DDG, veralteter EU-Streitschlichtungslink entfernt), Datenschutz (inkl. WhatsApp und externe Links), Cookie-Hinweise (keine Tracking-Cookies), Cookie-Einstellungen.

### SEO & GEO (Münster · Essen · Bochum)

- Pro Seite: eigener Title, Meta-Description, Canonical, Open-Graph-Bild, Breadcrumbs.
- Strukturierte Daten: `RealEstateAgent` mit Adresse, Geo-Koordinaten, Öffnungszeiten, Einsatzgebiet (Münster, Essen, Bochum, Münsterland, Ruhrgebiet), Leistungen, Fachgebieten; auf jeder Stadtseite ein lokaler `Service` mit Stadt und Koordinaten; dazu FAQPage, Article, RealEstateListing, DefinedTerm.
- Vorgerenderte HTML-Seiten (Google und KI-Crawler sehen den Inhalt ohne JavaScript), `sitemap.xml`, `robots.txt`.
- **`llms.txt`**: Kurzprofil für KI-Assistenten (ChatGPT, Perplexity, Gemini) mit Fakten, Leistungen, Regionen und wichtigsten Links.
- Stadtseiten: `/regionen/muenster|essen|bochum`, jeweils `/verkaufen`, dazu `/kontakt/muenster|essen|bochum`.
- Die alte Seite hat Sterne über ein `Product`-Schema mit erfundenem Preis erzwungen – das verstößt gegen die Google-Richtlinien und wurde bewusst **nicht** übernommen.

## 4. Vom Kunden zu prüfen oder zu liefern

**Vor dem Livegang (rechtlich wichtig)**
1. **Impressum – Inhaber/Rechtsform:** Dort steht nur „Oberholz Immobilien“. Ein Einzelunternehmen muss den vollen Namen des Inhabers nennen; die alten Regionsseiten sprechen aber von „Oberholz Immobilien der **EE Experten GmbH**“. Ist es eine GmbH, braucht das Impressum Rechtsform, Geschäftsführer und Handelsregister. → Bitte klären und ergänzen.
2. **Datenschutzerklärung** anwaltlich prüfen lassen (Hoster ergänzen; fremde Daten der alten Erklärung wurden entfernt).
3. **WhatsApp-Nummer:** Verlinkt ist 0251 28 42 90 90 (Festnetz, wie auf der alten Seite). Das funktioniert nur, wenn diese Nummer bei **WhatsApp Business** registriert ist – sonst andere Nummer nennen (`src/data/content.ts` → `brand.whatsapp`).
4. **Schlichtungsstelle** im Impressum (Ombudsmann Immobilien im IVD, Wolfgang Ball) auf Aktualität prüfen.

**Inhalte**
5. **Öffnungszeiten:** Verwendet wird Mo–Fr 8–19, Sa 8–16 Uhr. Die alte Seite nannte auch Mo–Sa 8–19 Uhr und Mo–Fr 9–18 / Sa 10–17 Uhr → richtige Zeiten bestätigen.
6. **Anzahl Google-Bewertungen:** Verwendet wird 28 Bewertungen, 5,0 Sterne (alte Seite: teils „9 Bewertungen“, Widget 4,9) → aktuellen Stand im Google-Profil prüfen (`brand.reviews`, `brand.rating`).
7. **Ratgeber-Autoren:** Artikel sind Teammitgliedern zugeordnet (`src/data/ratgeber/authors.ts`) → von den Personen gegenlesen und freigeben lassen.
8. **Whitepaper-PDFs** (Generationenwechsel, Erben-Kompass usw.) fehlen → liefern; bis dahin wird die Anfrage per E-Mail vorbereitet.
9. **ISO 9001:** Die Seite sagt korrekt „im Zertifizierungsprozess“. Sobald das TÜV-Zertifikat vorliegt, Text anpassen.
10. **Bilder:** Städte = echte Fotos (Unsplash, frei nutzbar), Szenen/Ratgeber = KI-Bilder ohne reale Personen (Liste: `public/assets/BILDNACHWEISE-KI.json`), Team = echte Fotos. Eigene Fotos können mit gleichem Dateinamen ersetzt werden.

**Technisch (optional, nach dem Livegang)**
11. **Formular-Backend:** Formulare prüfen die Eingaben und öffnen eine vorbereitete E-Mail an mail@oberholz-immobilien.com. Für echte Formular-Übermittlung `src/lib/mail.ts` an einen Maildienst/CRM anbinden.
12. **Objekte:** stammen statisch aus `src/data/listings.json` (21 Objekte). Für automatische Aktualisierung eine Schnittstelle (z. B. ImmoScout24/onOffice) anbinden.

## 5. Häufige Änderungen

| Was | Wo |
| --- | --- |
| Telefon, E-Mail, WhatsApp, Öffnungszeiten, Bewertungen | `src/data/content.ts` → `brand` (zusätzlich `index.html` Strukturdaten, `public/llms.txt`) |
| Team, Partner, Menüs, Startseite, Footer | `src/data/content.ts` |
| Ratgeber-Artikel | `src/data/ratgeber/*.ts` |
| Objekte | `src/data/listings.json`, Fotos in `public/assets/oberholz/objekte/<id>/` |
| Rechtstexte | `src/pages/oberholz/Legal.tsx` |

Danach `npm run build:seo` und `dist/` neu hochladen.

## 6. Qualitätsprüfung

```bash
npm run dev            # in einem Terminal laufen lassen
npm test               # 111 Funktionstests (Menü, Suche, KI-Suche, Funnel, Rechner, Kontakt-Pop-up, WhatsApp, Rechtstexte, Strukturdaten …)
npm run check:links    # crawlt alle Seiten: 404, Konsolenfehler, Überbreite auf dem Handy
```

Stand der Übergabe: 111/111 Tests bestanden, 131 Seiten ohne Fehler, Produktions-Build erfolgreich.
