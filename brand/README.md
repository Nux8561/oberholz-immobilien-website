# Oberholz Markenpaket – Schriften & Icons

Übersicht mit allen Schriften und Icons: `brand/index.html` im Browser öffnen.

## Schriften

| Schrift | Einsatz | Schnitte | Grundlage |
|---|---|---|---|
| **Oberholz Antiqua** | Überschriften | 600 | Spectral, © 2017 The Spectral Project Authors |
| **Oberholz Grotesk** | Text, Navigation, Buttons | 400, 500, 600, 700 | Inter Tight, © 2022 The Inter Project Authors |

Eigene Anpassungen im Hausschnitt:

- **Rautenpunkte**: i- und j-Punkte, Umlaute, Punkt, Doppelpunkt, Ausrufe- und Fragezeichen sowie das Aufzählungszeichen sind flächengleiche Rauten statt runder Punkte.
- Eigene Schriftnamen, Herstellerkennung `OBHZ` und eigene Metadaten. Statische Schnitte, ohne Hinting, auf Latein und Latein erweitert reduziert.

**Lizenz:** Beide Hausschriften sind abgeleitete Werke unter der SIL Open Font License 1.1 (`fonts/OFL.txt`). Die Grundschriften haben keine „Reserved Font Names“. Die Lizenz erlaubt Nutzung, Änderung und Einbettung, auch gewerblich. Nur der Verkauf der Schriftdateien allein ist nicht erlaubt. Die Hausschnitte müssen unter der OFL bleiben, deshalb kann Oberholz sie nicht exklusiv beanspruchen. Mit Engel & Völkers oder deren Schriften „EV Head“ und „EV Text“ haben sie nichts zu tun.

Neu bauen (z. B. nach einer Änderung an der Raute):

```bash
python3 scripts/build_brand_fonts.py
```

Das Skript liest `fonts/source/` und schreibt `fonts/*.woff2` sowie `src/styles/fonts.css`.

## Icons – „Oberholz Icons“

60 Motive: 56 Icons im 24er-Raster und 4 Illustrationen. Alle sind eigene Gestaltung, © 2026 Oberholz Immobilien.

Formensprache **„Fuge & Raute“**:

- Raster 24 × 24 (Illustrationen 48 × 48), 2 Einheiten Schutzzone
- Linie 1,5 px, stumpfe Enden, spitze Ecken, keine abgerundeten Rechtecke
- **Fuge**: Bauteile berühren sich nicht. Zwischen Dach und Wand, Lupenglas und Griff usw. bleibt Luft.
- **Raute**: Punkte und Akzente sind Rauten, wie die Punkte der Hausschriften. In Inhaltsbereichen (Klasse `oi-accent`) sind sie rot, in Bedienelementen haben sie die Textfarbe.
- Eigene Motive statt Standardsymbolen: Standort-Pin in Hausform, Verkaufsschild statt Handschlag, Grundstück mit Grenzsteinen, Schlüssel mit Rautenbart, Giebelhäuser nach Vorbild des Prinzipalmarkts.

Dateien:

- `icons/svg/<name>.svg` – Einzeldateien (Farbe über `currentColor`)
- `icons/sprite.svg` – alle Icons als `<symbol id="oi-<name>">`
- Quelle im Code: `src/icons/pack.ts`, Darstellung: `src/icons/Icon.tsx` (`<Icon name="pin" size={24} />`)

Nach einer Änderung in `pack.ts` den Export neu erzeugen (Node ≥ 22.18):

```bash
node scripts/export_icons.ts
```

Fremdmarken wie die Logos von WhatsApp, Instagram, Facebook, LinkedIn, YouTube und Google gehören nicht zum Set. Sie bleiben in ihrer Originalform (`SocialIcon`, Kontakt-Widget, Bewertungs-Panel).
