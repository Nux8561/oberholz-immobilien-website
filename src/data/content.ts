// Inhalte der Startseite + globale Daten (Marke, Menüs, Footer).
// Quelle der Firmendaten und Texte: oberholz-immobilien.pages.dev (Impressum, Über uns, Leistungen).
import { ROUTES } from './routes';
import listings from './listings.json';

const OB = '/assets/oberholz';
const M = `${OB}/media`;
const obj = (id: string, n = 0) => `${OB}/objekte/${id}/${String(n).padStart(3, '0')}.jpg`;

export const brand = {
  name: 'Oberholz Immobilien',
  short: 'Oberholz',
  company: 'Oberholz Immobilien',
  owner: 'Michael Oberholz',
  /** Rechtliche Anschrift (Impressum) */
  street: 'Wichernstraße 29',
  city: '48147 Münster, Deutschland',
  /** Kontaktadresse Essen (gleichwertiger Hauptstandort neben Münster) */
  contactStreet: 'Benderstraße 2',
  contactCity: '45257 Essen',
  /** Zentrale Rufnummer (Festnetz Essen) – überall als Hauptnummer */
  phoneDisplay: '0201 61447786',
  phoneHref: 'tel:+4920161447786',
  /** Festnetz Münster – Büro Münster, Michael Oberholz, Impressum */
  phoneMuensterDisplay: '0251 28429090',
  phoneMuensterHref: 'tel:+4925128429090',
  /** WhatsApp überall: Mobilnummer Felix Lesch */
  whatsapp: '491794468850',
  whatsappDisplay: '0179 4468850',
  email: 'mail@oberholz-immobilien.com',
  /** Bestätigt von Felix Lesch (Kundenfeedback Runde 3, 24.10.2026) */
  hours: 'Mo bis Fr 10:00 bis 20:00 Uhr, Sa 10:00 bis 18:00 Uhr',
  rating: 5.0,
  reviews: 28,
  regions: ['Essen', 'Münster'],
  /** Tätigkeitsgebiet rund um die Büros Essen und Münster */
  areas: ['Ruhrgebiet', 'Rheinland', 'Bergisches Land', 'Münsterland'],
  claim: 'Essen · Münster',
  logo: `${M}/oberholz-logo.png`,
  /** Google-Unternehmensprofil Essen (Benderstraße 2, mehr Rezensionen als Münster). reviews = Essen 19 + Münster 9, Stand 10.11.2026 */
  googleUrl: 'https://www.google.com/maps/place/Oberholz+Immobilien/@51.3889613,7.0834661,17z/data=!4m6!3m5!1s0x47b8dda4ad08016f:0xdf634f71dfa92324!8m2!3d51.3889613!4d7.0834661!16s%2Fg%2F11ts3pqm5l',
  /** Google-Unternehmensprofil Münster (Wichernstraße 29) */
  googleUrlMuenster: 'https://www.google.com/maps/place/Oberholz+Immobilien/@51.9735915,7.6248835,17z/data=!4m6!3m5!1s0x47b9bb4567805459:0xa08f5b6274a4201c!8m2!3d51.9735915!4d7.6248835!16s%2Fg%2F11shxgxbpq',
  geo: { lat: 51.4556, lng: 7.0116 },
};

/** WhatsApp-Link mit vorausgefülltem Text (Mobilnummer Felix Lesch) */
export const whatsappUrl = (text = 'Hallo Oberholz Immobilien, ich habe eine Frage:') =>
  `https://wa.me/${brand.whatsapp}?text=${encodeURIComponent(text)}`;

/** Immobilienportale für die Vermarktung. Keine Darstellung von Kooperations- oder Bankpartnern. */
export const partners = {
  portale: [
    { name: 'Kleinanzeigen', logo: `${M}/kleinanzeigen.svg`, url: 'https://www.kleinanzeigen.de/' },
    /** zweizeiliges Logo, daher höher als die einzeiligen (Quelle: Wikimedia Commons, gemeinfrei) */
    { name: 'ImmoScout24', logo: `${M}/immoscout24.svg`, url: 'https://www.immobilienscout24.de/', h: 64 },
  ],
};

/** Standorte Essen und Münster (Bochum ist seit Runde 3 kein Standort mehr).
 *  Rufnummer je Büro: Münster hat die Münsteraner Festnetznummer, Essen die zentrale Nummer.
 *  „page“: eigene Regionsseite mit lokalen Eigentümerseiten. */
export const offices = [
  { slug: 'essen', city: 'Essen', area: 'Essen, Ruhrgebiet, Rheinland und Bergisches Land', street: 'Benderstraße 2', zipCity: '45257 Essen', image: '/assets/stock/staedte/essen.jpg', page: true, hub: true,
    phoneDisplay: '0201 61447786', phoneHref: 'tel:+4920161447786', contactName: 'Felix Lesch' },
  { slug: 'muenster', city: 'Münster', area: 'Münster und Münsterland', street: 'Wichernstraße 29', zipCity: '48147 Münster', image: '/assets/stock/staedte/muenster.jpg', page: true, hub: true,
    phoneDisplay: '0251 28429090', phoneHref: 'tel:+4925128429090', contactName: 'Michael Oberholz' },
] as { slug: string; city: string; area: string; street: string; zipCity: string; image: string; page: boolean; hub?: boolean; phoneDisplay: string; phoneHref: string; link?: string; contactName?: string }[];

/** Büros mit persönlichem Ansprechpartner (Essen und Münster) */
export const hubOffices = () => offices.filter((o) => o.hub);
/** Link „Region ansehen“ eines Büros */
export const officeLink = (o: (typeof offices)[number]) => o.link ?? ROUTES.region(o.slug);
/** Nur Büros mit eigener Regionsseite (Essen, Münster) – für Stadtseiten, Routen und lokale Strukturdaten */
export const officeBySlug = (slug: string) => offices.find((o) => o.slug === slug && o.page);

const face = (slug: string) => `${M}/team/face-${slug}.jpg`;

/** Rollen laut Felix Lesch (Kundenfeedback 09.11.2026): alle Immobilienmakler/-in, Standortleitung Essen und Münster ergänzt. */
export const team = [
  { name: 'Michael Oberholz', role: 'Inhaber · Immobilienmakler · Standortleiter Münster', image: `${M}/oberholz-team/michael-oberholz.png`, face: face('michael-oberholz'),
    phoneDisplay: '0251 28429090', phoneHref: 'tel:+4925128429090', office: 'Münster' },
  { name: 'Felix Lesch', role: 'Immobilienmakler · Standortleiter Essen', image: `${M}/oberholz-team/felix-lesch.png`, face: face('felix-lesch'),
    phoneDisplay: '0201 61447786', phoneHref: 'tel:+4920161447786', office: 'Essen' },
  /** eigene Mobilnummer wie im ImmoScout-Exposé – bei seinen Objekten statt der zentralen Nummer */
  { name: 'Michael Penn', role: 'Immobilienmakler', image: `${M}/oberholz-team/michael-penn.png`, face: face('michael-penn'),
    phoneDisplay: '0173 2056491', phoneHref: 'tel:+491732056491' },
  { name: 'Pascal Kopp', role: 'Immobilienmakler', image: `${M}/oberholz-team/pascal-kopp.png`, face: face('pascal-kopp') },
  { name: 'Lubka Röger', role: 'Immobilienmaklerin', image: `${M}/oberholz-team/lubka-roeger.png`, face: face('lubka-roeger') },
  { name: 'Robin Sandkamp', role: 'Auszubildender Immobilienkaufmann', image: `${M}/oberholz-team/robin-sandkamp-studio.png`, face: face('robin-sandkamp') },
];

/** Ansprechpartner je Objekt: kommt aus dem ImmoScout-Exposé („Angeboten von“, Feld `agent` in listings.json).
 *  Abweichend nur bei Bedarf hier überschreiben, z. B. '170827695': 'Michael Penn'. Ohne Angabe: Felix Lesch. */
export const DEFAULT_AGENT = 'Felix Lesch';
export const listingAgents: Record<string, string> = {};
const importedAgent = (id: string) => listings.find((l) => l.id === id)?.agent;
export const agentFor = (id: string) =>
  team.find((m) => m.name === (listingAgents[id] ?? importedAgent(id) ?? DEFAULT_AGENT)) ?? team[1];

/** Gesichtsausschnitt (Avatar) zu einem Namen aus Alt-Texten/Autorenangaben */
export const faceOf = (name: string) => team.find((m) => name.startsWith(m.name))?.face;

/** Kundenavatare neben der Google-Bewertung (wie auf der bisherigen Website, ohne Zitate) */
export const reviewFaces = ['ute_kern', 'karsten_pfeiffer', 'alihan_bekc', 'guiseppe_pescatore'].map((n) => `${M}/headbanner-testimonials/${n}.png`);

/** Personenfotos sind freigestellte Hochformate (PNG): Michael Oberholz = A/G, Michael Penn = B, Pascal Kopp = C/F,
 *  Lubka Röger = D, Felix Lesch = E. „team“ ist daraus zusammengesetzt (scripts/compose_team.py).
 *  Robin Sandkamp (Azubi) ist bewusst nicht im Gruppenbild, nur als eigene Karte im Team. */
export const photos = {
  team: `${M}/team/team-gruppe.jpg`,
  beratung: '/assets/szenen/beratung.jpg',
  bewertung: '/assets/szenen/bewertung.jpg',
  buero: '/assets/szenen/buero.jpg',
  finanzierung: '/assets/szenen/finanzierung-banner.jpg',
  schluessel: '/assets/szenen/schluesseluebergabe.jpg',
  verkauf: '/assets/szenen/verkauf-handschlag.jpg',
  senioren: '/assets/szenen/senioren-terrasse.jpg',
  advisorA: `${M}/bannerright-1440/t7a3420.png`,
  advisorB: `${M}/bannerright-1440/t7a7913_1.png`,
  advisorC: `${M}/bannerright-1440/t7a0115_kopie.png`,
  advisorD: `${M}/bannerright-1440/t7a9283_kopie.png`,
  advisorE: `${M}/bannerright-1440/t7a7897.png`,
  advisorF: `${M}/bannerright-1440/t7a9489_copy.png`,
  advisorG: `${M}/bannerright-1440/t7a3373.png`,
  house360: `${M}/focuspoint_media_detail/haus360.png`,
  brochureSale: `${M}/contentimg/brochure_immobilienvermittlung.png`,
  brochureEnergy: `${M}/contentimg/brochure_energieberatung.png`,
};

export type MenuLink = { label: string; to: string };
export type MenuColumn = { eyebrow: string; links: MenuLink[] };
export type MegaMenuData = {
  label: string;
  to: string;
  title: string;
  text: string;
  /** leer = einfacher Link ohne Untermenü */
  columns: MenuColumn[];
  promo?: { image: string; eyebrow: string; title: string; to: string; stacked?: boolean };
  mobileCta?: MenuLink;
};

export const hasFlyout = (m: MegaMenuData) => m.columns.length > 0;

/** Hauptnavigation: bewusst schlank – jedes Ziel steht im Header nur einmal (Standorte, Merkliste und Kontakt stehen oben rechts). */
export const megaMenus: MegaMenuData[] = [
  {
    label: 'Verkaufen', to: ROUTES.verkaufen, title: 'Immobilie verkaufen oder vermieten',
    text: 'Von der kostenlosen Bewertung bis zur Schlüsselübergabe. Persönlich begleitet von Maklern und Gutachtern aus der Region.',
    columns: [{
      eyebrow: 'Für Eigentümer', links: [
        { label: 'Immobilie vermieten', to: ROUTES.vermieten }, { label: 'Rückmietverkauf', to: ROUTES.rueckmietverkauf },
        { label: 'Immotipp: ab 500 € Prämie', to: ROUTES.immotipp },
      ],
    }],
    promo: { image: photos.bewertung, eyebrow: 'Immobilienbewertung', title: 'Fordern Sie eine kostenfreie und unverbindliche Bewertung an', to: ROUTES.bewertung },
    mobileCta: { label: 'Bewertung anfragen', to: ROUTES.bewertung },
  },
  {
    label: 'Kaufen', to: ROUTES.kaufen, title: 'Immobilie kaufen',
    text: 'Häuser, Wohnungen und Kapitalanlagen aus unserer Vermittlung.',
    columns: [{
      eyebrow: 'Kaufen & Mieten', links: [
        { label: 'Immobilien mieten', to: ROUTES.mieten },
        { label: 'Kapitalanlagen & Mehrfamilienhäuser', to: ROUTES.kapitalanlage }, { label: 'Finanzierung', to: ROUTES.finanzierung },
      ],
    }],
    promo: { image: '/assets/ratgeber/haus-kaufen-ohne-eigenkapital.jpg', eyebrow: 'Budgetrechner', title: 'Wie viel Immobilie können Sie sich leisten?', to: ROUTES.budgetrechner },
    mobileCta: { label: 'Budget berechnen', to: ROUTES.budgetrechner },
  },
  {
    // Team und Qualifikationen stehen auf derselben Seite, Standorte und Kontakt oben rechts – daher ohne Untermenü
    label: 'Über uns', to: ROUTES.ueberUns, title: 'Oberholz Immobilien',
    text: 'Makler und Gutachter unter einem Dach, mit Büros in Essen und Münster.',
    columns: [],
  },
  {
    label: 'Ratgeber', to: ROUTES.ratgeber, title: 'Ratgeber',
    text: 'Verständliche Beiträge, Leitfäden und Rechner für Käufer, Verkäufer und Erben.',
    columns: [{
      eyebrow: 'Wissen & Werkzeuge', links: [
        { label: 'Immobilien-Lexikon', to: ROUTES.immopedia },
        { label: 'Wert-Hebel-Rechner', to: ROUTES.wertHebel }, { label: 'Finanzierungsrechner', to: ROUTES.finanzierungsrechner },
      ],
    }],
    promo: { image: '/assets/ratgeber/immobilie-geerbt-der-erben-kompass-fuer-die-ersten-wochen.jpg', eyebrow: 'Leitfaden', title: 'Der Erben-Kompass: Orientierung für geerbte Immobilien', to: ROUTES.whitepaper('erben-kompass') },
    mobileCta: { label: 'Erben-Kompass herunterladen', to: ROUTES.whitepaper('erben-kompass') },
  },
];

export const hero = {
  title: 'Ihr Immobilienmakler in Essen und Münster',
  /** Tätigkeitsgebiet als Zeile unter der Überschrift (Kunde Runde 3) */
  areas: 'Ruhrgebiet · Rheinland · Bergisches Land · Münsterland',
  modes: ['Kaufen', 'Mieten', 'KI-Suche'] as const,
  placeholder: 'Stadt, Stadtteil, Postleitzahl oder Objekt-Nr.',
  propertyTypes: [
    { group: 'Wohnen', options: ['Haus', 'Wohnung', 'Grundstück'] },
    { group: 'Kapitalanlage', options: [] },
  ],
  /** Slider: Stadtpanoramen aus der Region (keine Objektfotos). Bilder: Unsplash, siehe public/assets/stock/BILDNACHWEISE.json */
  slides: [
    { image: '/assets/stock/staedte/essen.jpg', pos: '70% 40%', title: 'Essen', sub: 'Zeche Zollverein · Büro Essen', to: ROUTES.region('essen') },
    { image: '/assets/stock/staedte/muenster.jpg', pos: '50% 45%', title: 'Münster', sub: 'Prinzipalmarkt · Büro Münster', to: ROUTES.region('muenster') },
    { image: '/assets/stock/staedte/duisburg.jpg', pos: '50% 50%', title: 'Ruhrgebiet', sub: 'Tiger & Turtle, Duisburg', to: `${ROUTES.kaufen}?ort=Ruhrgebiet` },
    { image: '/assets/stock/staedte/duesseldorf.jpg', pos: '50% 50%', title: 'Rheinland', sub: 'Rheinturm & Medienhafen, Düsseldorf', to: ROUTES.kaufen },
    { image: '/assets/stock/staedte/muensterland.jpg', pos: '50% 50%', title: 'Münsterland', sub: 'Zwischen Kanal und Feldern', to: `${ROUTES.kaufen}?ort=M%C3%BCnsterland` },
  ],
  /** Eigentümergewinnung zuerst; Kaufangebote sind nachrangig (eigene Suchseite). */
  teasers: [
    { image: photos.bewertung, title: 'Kostenlose Bewertung', label: 'Marktwert Ihrer Immobilie ermitteln', to: ROUTES.bewertung },
    { image: photos.verkauf, title: 'Immobilie verkaufen', label: 'Persönlich begleitet bis zur Übergabe', to: ROUTES.verkaufen },
    { image: face('michael-penn'), title: 'Immotipp: ab 500 € Prämie', label: 'Tipp geben und Prämie erhalten', to: ROUTES.immotipp },
  ],
};

export const selling = {
  eyebrow: 'Immobilie verkaufen',
  title: 'Verkaufen mit Gutachterkompetenz',
  text: 'Bei uns bewerten Makler und Gutachter Ihre Immobilie gemeinsam. So gehen Sie mit einem Preis an den Markt, der hält. Bis zur Schlüsselübergabe bleiben wir an Ihrer Seite.',
  benefits: [
    { icon: 'pin', title: 'Persönlich vor Ort', text: 'Ein fester Ansprechpartner in Essen oder Münster für Immobilien im Ruhrgebiet, Rheinland, Bergischen Land und Münsterland.' },
    { icon: 'globe', title: 'Gutachterkompetenz', text: 'Den Marktwert ermittelt ein zertifizierter Gutachter aus unserem Team und kein Online-Rechner.' },
    { icon: 'advisor', title: 'Alles aus einer Hand', text: 'Exposé, Grundrisse und alle Unterlagen, die Käufer und Banken sehen wollen.' },
  ],
  card: {
    image: photos.verkauf,
    alt: 'Makler und Eigentümerpaar besiegeln einen Hausverkauf per Handschlag',
    title: 'Geprüfte Käufer, sichere Abwicklung',
    text: 'Wir sprechen bonitätsgeprüfte Käufer aus unserem Netzwerk an, verhandeln in Ihrem Interesse und bleiben bis zur Übergabe an Ihrer Seite.',
    cta: 'Verkauf besprechen',
    to: ROUTES.verkaufen,
  },
};

export const cities = {
  eyebrow: 'Unsere Standorte',
  title: 'Essen und Münster',
  text: 'Mit unseren Standorten in Essen und Münster betreuen wir Ihre Immobilie im Ruhrgebiet, dem Rheinland, dem Bergischen Land und dem Münsterland.',
  items: offices.map((o) => ({ name: o.city, sub: `${o.street} · ${o.zipCity}`, image: o.image, to: officeLink(o) })),
};

export const careers = {
  eyebrow: 'Unser Team',
  title: 'Persönliche Beratung von Experten in Ihrer Region',
  text: 'Seit 2011 begleiten wir Eigentümer, Käufer und Investoren in Essen, Münster und Umgebung.',
  card: {
    image: photos.team,
    alt: 'Das Team von Oberholz Immobilien',
    title: 'Ihr Team von Oberholz Immobilien',
    text: 'Unser Team aus Maklern und Gutachtern berät Sie persönlich. Das erste Gespräch ist kostenlos und unverbindlich.',
    cta: 'Team kennenlernen',
    to: ROUTES.team,
  },
};

export const lifestyle = {
  title: 'Objekte aus unserer Vermittlung',
  galleryButton: 'Zur Galerie',
  more: 'Mehr erfahren',
  items: [
    { image: obj('171838502'), title: 'Reihenendhaus in Essen-Kupferdreh', alt: 'Garten eines Reihenendhauses in Essen-Kupferdreh' },
    { image: obj('170022736', 1), title: 'Einfamilienhaus mit Garten in Stadtlohn', alt: 'Einfamilienhaus in Stadtlohn' },
    { image: obj('170199527', 2), title: 'Maisonettewohnung in Velbert-Neviges', alt: 'Dachterrasse mit Ausblick in Velbert' },
    { image: obj('170649223'), title: 'Reihenhaus in Bergkamen-Oberaden', alt: 'Reihenhaus mit Garten in Bergkamen' },
    { image: obj('170680511'), title: 'Reihenhaus in Duisburg-Walsum', alt: 'Garten eines Reihenhauses in Duisburg' },
    { image: obj('170827695', 5), title: 'Maisonettewohnung in Münster-Mecklenbeck', alt: 'Balkon mit Blick über Münster-Mecklenbeck' },
  ],
};

export const magazine = {
  eyebrow: 'Ratgeber & Leitfäden',
  title: 'Wissen für Eigentümer, Käufer und Erben',
  text: 'Verständliche Beiträge zu Markt, Verkauf, Bewertung und Energie, jeweils mit Quellen. Dazu Leitfäden zum Download, vom Erben-Kompass bis zum Generationenwechsel.',
  card: {
    image: '/assets/ratgeber/immobilie-geerbt-der-erben-kompass-fuer-die-ersten-wochen.jpg',
    alt: 'Hände sortieren Familienfotos, Briefe und Hausschlüssel',
    title: 'Der Erben-Kompass',
    text: 'Orientierung für geerbte Immobilien: erste Schritte, Erbengemeinschaft, Bewertung und offene Fragen. Als kompakte PDF-Lesefassung kostenlos herunterladen.',
    cta: 'Zum kostenlosen Download',
    to: ROUTES.whitepaper('erben-kompass'),
  },
};

const groupLinks = (places: string[]) => ({
  haus: places.map((p) => `Haus kaufen in ${p}`),
  wohnung: places.map((p) => `Wohnung kaufen in ${p}`),
});

export const relatedTopics = {
  eyebrow: 'Weitere Themen',
  title: 'Passende Themen für Ihre Region',
  groups: [
    { icon: 'house', title: 'Immobilien im Ruhrgebiet', text: 'Häuser, Wohnungen und Kapitalanlagen im Ruhrgebiet.', ...groupLinks(['Essen', 'Duisburg', 'Gelsenkirchen', 'Bergkamen']) },
    { icon: 'apartment', title: 'Immobilien im Münsterland', text: 'Häuser und Wohnungen in Münster, Coesfeld, Stadtlohn und Umgebung.', ...groupLinks(['Münster', 'Coesfeld', 'Stadtlohn']) },
    { icon: 'townhouse', title: 'Immobilien im Bergischen Land', text: 'Angebote in Velbert und Umgebung.', ...groupLinks(['Velbert']) },
  ],
};

export const contact = {
  eyebrow: 'Kontakt',
  title: 'Sprechen Sie mit uns. Persönlich und unverbindlich.',
  avatars: [team[1].face, team[0].face],
  office: 'Oberholz Immobilien',
  cta: 'Jetzt kontaktieren',
};

export const footer = {
  claim: 'Ihr Immobilienpartner in Essen, Münster und Umgebung',
  socials: ['google', 'whatsapp'] as const,
  columns: [
    { title: 'Leistungen', links: [
      { label: 'Immobilien kaufen', to: ROUTES.kaufen }, { label: 'Immobilie verkaufen', to: ROUTES.verkaufen },
      { label: 'Kostenlose Bewertung', to: ROUTES.bewertung }, { label: 'Vermietung', to: ROUTES.vermieten },
      { label: 'Rückmietverkauf', to: ROUTES.rueckmietverkauf }, { label: 'Finanzierung', to: ROUTES.finanzierung },
    ] },
    { title: 'Unternehmen', links: [
      { label: 'Über uns', to: ROUTES.ueberUns },
      { label: 'Standorte', to: ROUTES.regionen }, { label: 'Ratgeber', to: ROUTES.ratgeber },
      { label: 'Kontakt', to: ROUTES.kontakt }, { label: 'Immotipp', to: ROUTES.immotipp },
    ] },
  ],
  legalLeft: [{ label: 'Cookie-Einstellungen', to: '#cookies' }, { label: 'Cookie-Hinweise', to: ROUTES.cookieHinweise }],
  legalRight: [{ label: 'Datenschutz', to: ROUTES.datenschutz }, { label: 'Impressum', to: ROUTES.impressum }],
};
