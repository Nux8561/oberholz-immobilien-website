# Stand & offene Punkte

> Für die Übergabe an Oberholz siehe **ÜBERGABE.md** (Livegang, Kunden-Checkliste, Pflege).

## Erledigt (Stand 15.10.2026, Übergabe)
- Kontakt-Pop-up wie auf der alten Seite (Anfrage, Anrufen, Rückruf, WhatsApp, Kontakt) + Handy-Kontaktleiste.
- WhatsApp überall eingebunden (Pop-up, Footer, Kontakt, Exposé mit Objektnummer); Datenschutz um WhatsApp/externe Links ergänzt.
- Partner & Kooperationen (DVAG, Swiss Life, Interhyp, Banken, Portale) im Footer, auf „Über uns“ (#partner), Finanzierung, Verkaufen.
- GEO: lokale `Service`-Strukturdaten je Stadtseite, erweiterte Organisationsdaten (Leistungen, Fachgebiete, Kontaktpunkt), `public/llms.txt`.
- Impressum: veralteter EU-ODR-Link entfernt (Plattform seit 20.07.2025 eingestellt).
- `npm test`: 111/111 · `npm run check:links`: 131 Seiten, 0 Probleme · `npm run build:seo`: 91 Seiten vorgerendert.

## Erledigt (frühere Runden)
- Alle Seiten auf echte Oberholz-Inhalte umgestellt (71 Routen + 1.999 Immopedia-Begriffe), siehe README.
- Link-Prüfung (`npm run check:links`): 111 geprüfte URLs, 0 Fehler (keine 404, keine Konsolenfehler, kein Overflow bei 390 px, alle PDFs und Immopedia-Dateien vorhanden).
- Newsletter entfernt, alle „lokale Demo“-Hinweise entfernt; jeder Link führt auf eine echte Seite.
- Funnel (Bewertung/Verkauf/Vermietung), Budget-, Finanzierungs- und Wert-Hebel-Rechner funktionieren im Browser.
- `npm test`: 81/81 Funktionstests bestanden; Unterseiten werden nachgeladen (Start-Bundle ~325 kB statt ~690 kB).

## Bilder (Stand 15.10.2026, zweite Runde)
- **Ratgeber, Banner, Szenen:** 26 KI-Fotos (GPT Image 2.5 über Higgsfield, ca. 72 Credits) – `public/assets/ratgeber/`, `public/assets/szenen/`, Liste in `public/assets/BILDNACHWEISE-KI.json`. Keine realen Personen.
- **Städte:** echte Fotos von Unsplash (kommerziell frei nutzbar) – `public/assets/stock/staedte/`, Quellen in `BILDNACHWEISE.json`.
- **Team:** echte Fotos der alten Seite; Gesichtsausschnitte und Teamfoto per `scripts/compose_team.py`.
- Hochformat-Objektfotos werden nicht mehr beschnitten (`FitImage`: ganzes Foto auf weichem Hintergrund).
- Später durch eigene Fotos ersetzbar: gleiche Dateinamen verwenden.

## Ratgeber
- 17 Redaktionsartikel + 6 Fachbeiträge, Kategorien Käufer / Verkäufer / Eigentümer & Erben.
- Autoren: Teammitglieder laut `src/data/ratgeber/authors.ts` – **bitte von den jeweiligen Personen gegenlesen und freigeben lassen.**
- E&V-Texte wurden bewusst NICHT übernommen (Urheberrecht) – nur Aufbau und Themenauswahl.

## Google & SEO
- Bewertungs-Panel wie auf der alten Seite (Klick auf Sterne → Übersicht → Google-Profil).
- Strukturierte Daten: RealEstateAgent (global), BreadcrumbList, FAQPage, Article, RealEstateListing, DefinedTerm.
- Meta-Description, Canonical, Open Graph je Seite; `npm run build:seo` erzeugt vorgerenderte HTML-Seiten, `sitemap.xml` und `robots.txt`.
- **Domain** in `src/data/routes.ts` (`SITE_URL`) vor dem Livegang prüfen.
- Die alte Seite nutzte ein `Product`-Schema mit Preis 395 € und Sternen, um Sterne in Google zu erzwingen. Das verstößt gegen die Google-Richtlinien für selbst veröffentlichte Bewertungen und wurde bewusst nicht übernommen.
- Widerspruch der alten Seite: Panel „9 echte Bewertungen“ vs. sonst „28 Bewertungen“ – aktuelle Zahl im Google-Profil prüfen (`brand.reviews`).

## Mit Oberholz zu klären
1. **Öffnungszeiten**: Startseite „Mo–Sa 8–19 Uhr“, Kontakt-Stadtseiten + strukturierte Daten „Mo–Fr 8–19, Sa 8–16 Uhr“ (verwendet).
2. **Telefon in strukturierten Daten** der alten Seite: +49-711-… (Stuttgart) – verwendet wird 0251 28 42 90 90 (Impressum).
3. **Firmierung**: Regionsseiten nennen „Oberholz Immobilien der EE Experten GmbH“, Impressum nur „Oberholz Immobilien“ ohne Inhaber/Rechtsform (Pflichtangabe!).
3a. **WhatsApp**: verlinkt ist die Festnetznummer 0251 28429090 (wie alte Seite) – funktioniert nur mit WhatsApp Business auf dieser Nummer.
4. **Datenschutzerklärung der alten Seite enthielt fremde Daten** (Abschnitt „Widget“: Von-Liebig-Straße 2, 78050, Serhan Sidan, Tel. 07721…; Aufsichtsbehörde Baden-Württemberg; Vimeo). Diese Abschnitte sind entfernt, NRW-Aufsichtsbehörde ergänzt. Hoster-Angabe (Timme Hosting) an den neuen Hoster anpassen. Komplett anwaltlich prüfen lassen.
5. **Impressum**: Agentur-Credits „Platzhirsch Online“ entfernt (betrifft die alte Seite); „§ 5 TMG“ → „§ 5 DDG“ aktualisiert.
6. **Whitepaper-PDFs** (Generationenwechsel, Erben-Kompass usw.) liegen nicht vor → Dateien liefern; aktuell wird die Anfrage per E-Mail vorbereitet.
7. **Textfehler der Quelle** (z. B. „Landkreis Cloppenburg“ auf der Essen-Seite, „Immobilienberaterininin“) werden beim Rendern bereinigt – besser in den Quelltexten korrigieren.
8. **Kapitalanlage-/Wohnungsseiten der alten Website** enthielten nach dem Intro eine Kopie der Verkaufsseite; hier nur Intro + passende Objekte + Finanzierungsteil verwendet.
9. **Vergleichstabelle „Klassischer Makler vs. Oberholz“**: Häkchen-Verteilung aus der alten Seite nicht auslesbar (Icons) – angenommen: klassischer Makler nur Zeile 1.

## Technisch offen
- Formular-Backend anbinden (`src/lib/mail.ts`), z. B. Mail-API oder CRM.
- Optional: Objekte automatisch aus ImmoScout24 o. ä. aktualisieren (bisher statisch aus `listings.json`).
