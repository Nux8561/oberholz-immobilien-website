# Oberholz Immobilien – Übergabe und Prüfstand

Stand: 16.10.2026. Projekt: `/Users/dominik/Desktop/oberholtz immobilie`.
React, TypeScript und Vite; vollständige statische HTML-Ausgabe für Suchmaschinen.

## Vorschau und Hauptdomain

- Kunden-Vorschau: https://oberholz-immobilien.pages.dev/
- Revu: https://getrevu.app/m/60f2f951-7afd-48e4-8f49-5eb31bdda046
- Vorgesehene Hauptdomain in Canonicals und Strukturdaten: `https://www.oberholz-immobilien.com`.
- Cloudflare-Projektprüfung am 16.10.: am Projekt `oberholz-immobilien` hängt ausschließlich die pages.dev-Adresse. Eine Anbindung der Hauptdomain ist damit noch nicht nachgewiesen.
- Die pages.dev-Vorschau bekommt einen `X-Robots-Tag: noindex`, um nicht mit der späteren Hauptdomain zu konkurrieren. Diese Regel gilt nicht für die Hauptdomain.

## Inhalte und Gestaltung

- Vier neue lokale Seiten: Bewertung und Wohnungsverkauf, jeweils in Essen und Bochum.
- Bestehende Makler- und Verkaufsseiten beider Städte überarbeitet, mit unterschiedlichen lokalen Schwerpunkten, eigenen Fragen und amtlichen Marktquellen.
- Verkaufs- und Bewertungsübersicht gestrafft; wiederholte Leistungsraster und übernommene Konkurrenzvergleiche entfernt.
- Korrekte Bewertungsverfahren: Vergleichswert, Ertragswert und Sachwert. Quelle: § 6 ImmoWertV.
- Kontaktseite auf Essen, Bochum und Münsterland ausgerichtet; lokale Kontaktseiten zeigen die jeweilige Anschrift. Die rechtliche Anschrift wurde nicht verändert.
- Startseite mit genau einer Hauptüberschrift, sechs lokalen Eigentümer-Einstiegen und sichtbaren FAQ passend zu den FAQ-Strukturdaten.
- Hero-Bildspalten folgen auf Desktop der Texthöhe. Mobile Typografie, lange Fachwörter, Buttons und Statistikraster korrigiert. Sprunglink zum Inhalt und reduzierte Bewegung berücksichtigt.
- Sechs echte PDF-Lesefassungen vorhandener Ratgeber unter `public/downloads/leitfaeden/`, jeweils zwei Seiten. Die Downloadseiten nennen den tatsächlichen Umfang und verlinken die Dateien direkt. Frühere Versprechen von 9–13 Seiten beziehungsweise 25 Quellen wurden entfernt. Die PDFs sind Lesefassungen der vorhandenen Artikel, keine neuen Fachgutachten.
- Doppelte Download-Werbung und alte Empfehlungen aus übernommenen Artikeln entfernt; die kuratierten Empfehlungen erscheinen einmal.

## Technische SEO/GEO-Grundlage

- Alle 1.999 Immopedia-Begriffe und die übrigen indexierbaren Inhalte werden vollständig gerendert: 2.089 URLs in der Sitemap.
- Jeder Eintrag in der Sitemap besitzt eine entsprechende HTML-Datei. Der Build prüft Hauptüberschrift, Beschreibung und Canonical und bricht bei fehlendem Inhalt ab.
- Sichtbare Fragen und FAQ-Strukturdaten verwenden dieselben Texte. Lokale Services, Breadcrumbs, Artikel und Begriffe erhalten passende Strukturdaten.
- Gefilterte Suchergebnisse sind im Browser `noindex`; die ungefilterten Suchseiten bleiben indexierbar.
- Echte `404.html` für unbekannte URLs und HTTP-301-Weiterleitungen für bekannte alte Pfade. Kein pauschaler SPA-Rewrite.
- `llms.txt`, `robots.txt` und `sitemap.xml` liegen im Build vor. Sie ersetzen keine Indexierung oder Sichtbarkeitsmessung.
- Für KI-Suchergebnisse werden keine Rankings, Erwähnungen oder Sichtbarkeitsgewinne garantiert.

## Starten, prüfen und bauen

```bash
npm install
npm run dev
npm run lint
npm test
npm run check:links
npm run build:seo
```

`npm test` und die Linkprüfung benötigen den lokalen Server auf Port 5173.
`build:seo` startet und beendet seinen eigenen Preview-Server auf Port 4174.
Die PDF-Dateien sind bereits enthalten; bei Änderungen der Originalartikel können sie mit `python3 scripts/build_guides.py` erneut erstellt werden (ReportLab und pypdf erforderlich).

## Vor dem produktiven Hauptdomain-Livegang offen

1. **Formularzustellung:** Die Formulare validieren Angaben und bereiten eine E-Mail vor. Der Besucher muss sie über sein E-Mail-Programm selbst versenden. Ein automatischer Mail- oder CRM-Eingang ist nicht eingerichtet; ein tatsächlicher Versand wurde nicht behauptet. Der Hinweis ist vor der Formularaktion sichtbar.
2. **Hauptdomain:** Ziel und DNS-Anbindung bestätigen, anschließend auf der tatsächlichen Hauptdomain prüfen und die Sitemap in Search Console einreichen.
3. **Firmierung:** Der Bestand nennt „Oberholz Immobilien“, an anderer Stelle „EE Experten GmbH“. Rechtsform, Vertretungsberechtigung und Pflichtangaben müssen vom Auftraggeber verbindlich geliefert beziehungsweise bestätigt werden.
4. **Öffnungszeiten:** Im Bestand stehen widersprüchliche Zeiten. Aktuell verwendet: Mo–Fr 8–19, Sa 8–16 Uhr. Noch keine Bestätigung des Auftraggebers.
5. **Fachliche Freigabe:** Übernommene Ratgeber, Autorenzuordnung, Qualifikationen, Zertifizierungsstand, Rechtstexte, Google-Bewertungen und Objektangebote vom Auftraggeber abschließend prüfen lassen. Keine neue fachliche oder rechtliche Freigabe durch die technische Überarbeitung.

Zentrale Rufnummer überall: `0201 61447786` (Festnetz Essen). WhatsApp überall: `0179 4468850` (Mobil Felix Lesch). Münster-Festnetz `0251 28 42 90 90` nur beim Büro Münster, bei Objekten in Münster und als Zusatz im Impressum. Ansprechpartner je Objekt: `listingAgents` in `src/data/content.ts` (Standard Felix Lesch). Die Objekte stammen aus statischen Bestandsdaten; eine automatische Objekt-Schnittstelle ist nicht eingerichtet.
