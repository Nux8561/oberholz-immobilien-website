# Anfragen im Courtage-Portal (Mapping)

Stand: 28.10.2026 · Sender: `functions/api/contact.js` (Pages Function) · Empfänger: Ingest-Webhook des Courtage-Portals (Secret `LEAD_WEBHOOK_URL`)

Jede Website-Anfrage kommt als **flaches JSON** (`event: website.lead`, `version: 2`) mit `Idempotency-Key`. Das Portal ordnet so zu:

- **Automatisch (Standardfelder):** `first_name`, `last_name`, `name`, `email`, `phone`.
- **Automatisch (Auto-Mapping):** jeder Schlüssel, zu dem es in der Kampagne ein eigenes Feld mit gleichem Key **oder** gleichem Label gibt. Verglichen wird ohne Groß-/Kleinschreibung, Umlaute als ae/oe/ue, Sonderzeichen entfallen („Ort der Immobilie“ = `ort_der_immobilie`, „Wohnfläche (m²)“ = `wohnflaeche_m2`).
- **Alles andere** landet unter „nicht zugeordnet“ (es geht nichts verloren) und kann über das Quellen-Mapping zugeordnet oder auf `ignore` gesetzt werden.

## 1. Eigene Felder in der Oberholz-Kampagne anlegen

| Label im Portal | Key | Typ | Beispiel |
|---|---|---|---|
| Anfrageart | `anfrageart` | Text/Auswahl | Bewertung, Verkauf, Vermietung, Rückruf, Exposé-Anfrage, Rückmietverkauf, Immotipp (Tippgeber), Finanzierung, Kontakt, Wert-Hebel-Rechner, Beratung |
| Vorhaben | `vorhaben` | Text | Bewerten, Verkaufen |
| Anliegen | `anliegen` | Text | Immobilie verkaufen (Kontakt-Fenster) |
| Nachricht | `nachricht` | Langtext | |
| Objektart | `objektart` | Text | Wohnhaus, Wohnung, Gewerbe, Grundstück |
| Objekttyp | `objekttyp` | Text | Einfamilienhaus, Reihenhaus … |
| Objektdetails | `objektdetails` | Text | ca. 90 m² Wohnfläche |
| Ort der Immobilie | `ort_der_immobilie` | Text | 48147 Münster |
| Wohnfläche (m²) | `wohnflaeche_m2` | Zahl | 90 |
| Grundstück (m²) | `grundstueck_m2` | Zahl | 500 |
| Wohneinheiten | `wohneinheiten` | Zahl | 6 |
| Erreichbarkeit | `erreichbarkeit` | Text | Vormittags, Abends |
| Rückruf-Zeitraum | `rueckruf_zeitraum` | Text | Nachmittags |
| Büro | `buero` | Text | Essen, Münster |
| Ansprechpartner | `ansprechpartner` | Text | Felix Lesch, Michael Oberholz |
| Exposé-Nr. | `expose_nr` | Text | 171621369 |
| Exposé-Titel | `expose_titel` | Text | |
| Exposé-Ort | `expose_ort` | Text | Essen-Kupferdreh |
| Exposé-Link | `expose_link` | Text/URL | |
| Seite | `seite` | Text/URL | Seite, auf der abgeschickt wurde |
| Einstiegsseite | `einstiegsseite` | Text/URL | erste Seite der Sitzung (mit UTM) |
| Quelle | `utm_source` | Text | google |
| Kampagne | `utm_campaign` | Text | |
| Gerät | `geraet` | Text | mobile, tablet, desktop |
| Einwilligung Datenschutz | `einwilligung_datenschutz` | Text (intern) | ja |
| Einwilligungstext | `einwilligung_text` | Langtext (intern) | Nachweis der Einwilligung |
| Einwilligung am | `einwilligung_zeit` | Datum/Zeit (intern) | |
| Bestätigung | `bestaetigung` | Text (intern) | Immotipp: Einverständnis der Eigentümer |

Optional (Wert-Hebel-Rechner): `rechner_baujahr`, `rechner_vermuteter_wert_eur`, `rechner_heizung`, `rechner_fassade_gedaemmt`, `rechner_dach_gedaemmt`, `rechner_fenster`, `rechner_energieklasse_geschaetzt`, `rechner_werteffekt_von_eur`, `rechner_werteffekt_bis_eur`.

## 2. Quellen-Mapping (für `set_source_mapping` bzw. die Mapping-Maske)

Nur für Schlüssel nötig, die nicht automatisch passen. Technik-Schlüssel auf `ignore`:

```json
{
  "event": "ignore", "version": "ignore", "id": "ignore", "source": "ignore", "website": "ignore",
  "type": "ignore", "formular": "ignore", "betreff": "ignore", "seitentitel": "ignore",
  "herkunftsseite": "ignore", "einstieg_herkunft": "ignore", "utm_medium": "ignore", "utm_term": "ignore",
  "utm_content": "ignore", "gclid": "ignore", "gbraid": "ignore", "wbraid": "ignore", "fbclid": "ignore",
  "msclkid": "ignore", "bildschirmbreite": "ignore", "sprache": "ignore", "browser": "ignore", "land": "ignore",
  "gesendet_am": "ignore", "empfangen_am": "ignore"
}
```

Wer Kampagnen-Auswertung im Portal will, legt für `utm_medium`, `gclid` usw. eigene Felder an, statt sie zu ignorieren.

## 3. Prüfen

In der Mapping-Maske der Quelle die Vorschau mit einem Lead ansehen. Der Test-Lead „TEST Website-Anbindung“ vom 28.10.2026 hatte noch das alte, verschachtelte Format (`version: 1`) und kann gelöscht werden.
