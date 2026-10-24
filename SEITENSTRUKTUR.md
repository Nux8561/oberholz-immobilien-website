# Seitenstruktur Oberholz Immobilien (Stand 24.10.2026)

Hauptmenü mit vier Bereichen plus „Jetzt kontaktieren“. Alles andere hängt darunter.

```
Startseite
├── Immobilien
│   ├── Immobilien kaufen            /immobilien/kaufen   (Suche, Filter, Karte)
│   ├── Immobilien mieten            /immobilien/mieten
│   ├── Kapitalanlagen               /kapitalanlage
│   ├── Finanzierung                 /finanzierung
│   └── Exposés                      /expose/<Objekt-Nr.>  (Bestand laut ImmoScout24, Stand 19.10.2026: 13 Objekte)
├── Verkaufen
│   ├── Immobilie verkaufen          /verkaufen
│   ├── Kostenlose Bewertung         /bewertung
│   ├── Immobilie vermieten          /vermieten
│   ├── Rückmietverkauf              /rueckmietverkauf
│   └── Immotipp (Prämie)            /immotipp
├── Über uns                         /ueber-uns  (Team, Qualifikationen, ISO 9001, Partner)
│   ├── Standorte                    /regionen   (Essen · Münster)
│   │   ├── Essen                    /regionen/essen
│   │   └── Münster                  /regionen/muenster
│   └── Kontakt                      /kontakt
└── Ratgeber                         /ratgeber   (Beiträge, Rechner, Leitfäden & Downloads)
    ├── Beiträge                     /ratgeber/<thema>  (23)
    ├── Rechner                      /service/budgetrechner · /service/finanzierungsrechner · /service/wert-hebel-rechner
    ├── Leitfäden                    /whitepaper/<name>  (6)
    └── Immobilien-Lexikon           /immopedia  (rund 2.000 Begriffe)

Rechtliches im Footer: Impressum · Datenschutz · Cookie-Hinweise · Merkliste (/mein-bereich)
```

## Nur für Google (nicht im Menü)

Sechs lokale Seiten bleiben für die Suche bestehen und sind von den Stadtseiten Essen und Münster verlinkt:
`/regionen/<essen|muenster>/verkaufen`, `/immobilienbewertung`, `/wohnung-verkaufen`.

## Zusammengelegt am 17.10.2026

Diese Seiten gibt es nicht mehr einzeln. Alte Links leiten automatisch (301) weiter:

| Alte Seite | Jetzt |
| --- | --- |
| /leistungen, /vermarktung | /verkaufen |
| /wohnung-kaufen | Immobiliensuche mit Filter Wohnung |
| /service | Ratgeber, Abschnitt Rechner |
| /downloads | Ratgeber, Abschnitt Leitfäden & Downloads |
| /ueber-uns/qualifikation, /ueber-uns/iso-9001 | Über uns, Abschnitt Qualifikationen |
| /kontakt/essen, /kontakt/muenster | /regionen/essen, /regionen/muenster |
| /regionen/bochum (+ Unterseiten, bis 24.10.2026) | /regionen, /verkaufen, /bewertung |

Startseite: Finanzierungs-Banner und der Block „Ihr nächster Schritt vor Ort“ entfallen.

## Telefon und WhatsApp

| Wofür | Nummer |
| --- | --- |
| Zentral, überall | 0201 61447786 (Festnetz Essen) |
| WhatsApp, überall | 0179 4468850 (Mobil Felix Lesch) |
| Nur Münster (Büro Münster, Objekte in Münster) | 0251 28 42 90 90 |

Ansprechpartner je Objekt: aus dem ImmoScout-Exposé („Angeboten von“), Überschreiben bei Bedarf über `listingAgents` in `src/data/content.ts`. Bei Objekten von Michael Penn erscheint seine Mobilnummer 0173 2056491 (wie bei ImmoScout).
