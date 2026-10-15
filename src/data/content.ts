// Inhalte der Startseite + globale Daten (Marke, Menüs, Footer).
// Quelle der Firmendaten und Texte: oberholz-immobilien.pages.dev (Impressum, Über uns, Leistungen).
import { ROUTES } from './routes';

const OB = '/assets/oberholz';
const M = `${OB}/media`;
const obj = (id: string, n = 0) => `${OB}/objekte/${id}/${String(n).padStart(3, '0')}.jpg`;

export const brand = {
  name: 'Oberholz Immobilien',
  short: 'Oberholz',
  company: 'Oberholz Immobilien',
  owner: 'Michael Oberholz',
  street: 'Wichernstraße 29',
  city: '48147 Münster, Deutschland',
  phoneDisplay: '0251 28 42 90 90',
  phoneHref: 'tel:+4925128429090',
  /** WhatsApp (Nummer laut bisheriger Website: wa.me/4925128429090) */
  whatsapp: '4925128429090',
  fax: '0251 28 42 90 91',
  email: 'mail@oberholz-immobilien.com',
  hours: 'Mo–Fr 8:00–19:00 Uhr, Sa 8:00–16:00 Uhr',
  rating: 5.0,
  reviews: 28,
  regions: ['Münster', 'Essen', 'Bochum'],
  logo: `${M}/oberholz-logo.png`,
  googleUrl: 'https://www.google.com/maps/place/Oberholz+Immobilien/@51.9735915,7.6248835,17z/data=!4m6!3m5!1s0x47b9bb4567805459:0xa08f5b6274a4201c!8m2!3d51.9735915!4d7.6248835!16s%2Fg%2F11shxgxbpq',
  geo: { lat: 51.9735915, lng: 7.6248835 },
  linkedinUrl: 'https://www.linkedin.com/company/oberholz-immobilien',
};

/** Regionale Zuständigkeiten (Seite „Kontakt“ der bisherigen Website). Postanschrift: Münster. */
/** WhatsApp-Link mit vorausgefülltem Text */
export const whatsappUrl = (text = 'Hallo Oberholz Immobilien, ich habe eine Frage:') =>
  `https://wa.me/${brand.whatsapp}?text=${encodeURIComponent(text)}`;

/** Kooperationen und Partner (wie auf der bisherigen Website) */
export const partners = {
  kooperation: [
    { name: 'DVAG – Deutsche Vermögensberatung', logo: `${M}/dvag-logo.svg`, url: 'https://www.dvag.de/' },
    { name: 'Swiss Life', logo: `${M}/swiss-life-logo.svg`, url: 'https://www.swisslife.de/' },
    { name: 'Interhyp', logo: `${M}/interhyp-logo.svg`, url: 'https://www.interhyp.de/' },
  ],
  finanzierung: [
    { name: 'Postbank', logo: `${M}/postbank-logo.svg` },
    { name: 'Santander', logo: `${M}/santander.svg` },
    { name: 'ING', logo: `${M}/ing-diba-logo-optimized.svg` },
    { name: 'PSD Bank', logo: `${M}/psd_bank_logo.svg` },
    { name: 'DKB', logo: `${M}/deutsche_kreditbank_ag_logo_2016.svg` },
  ],
  portale: [
    { name: 'Kleinanzeigen', logo: `${M}/kleinanzeigen.svg`, url: 'https://www.kleinanzeigen.de/' },
    { name: 'Immowelt', logo: `${M}/immowelt.png`, url: 'https://www.immowelt.de/' },
  ],
};

export const offices = [
  { slug: 'muenster', city: 'Münster', area: 'Münster und Münsterland', image: '/assets/stock/staedte/muenster.jpg' },
  { slug: 'essen', city: 'Essen', area: 'Essen und Ruhrgebiet', image: '/assets/stock/staedte/essen.jpg' },
  { slug: 'bochum', city: 'Bochum', area: 'Bochum und Umgebung', image: '/assets/stock/staedte/bochum.jpg' },
];
export const officeBySlug = (slug: string) => offices.find((o) => o.slug === slug);

const face = (slug: string) => `${M}/team/face-${slug}.jpg`;

export const team = [
  { name: 'Michael Oberholz', role: 'Inhaber & Sachverständiger', image: `${M}/oberholz-team/michael-oberholz.png`, face: face('michael-oberholz') },
  { name: 'Felix Lesch', role: 'Immobilienberater', image: `${M}/oberholz-team/felix-lesch.png`, face: face('felix-lesch') },
  { name: 'Michael Penn', role: 'Immobilienberater', image: `${M}/oberholz-team/michael-penn.png`, face: face('michael-penn') },
  { name: 'Pascal Kopp', role: 'Transaktionsberater', image: `${M}/oberholz-team/pascal-kopp.png`, face: face('pascal-kopp') },
  { name: 'Lubka Röger', role: 'Immobilienberaterin', image: `${M}/oberholz-team/lubka-roeger.png`, face: face('lubka-roeger') },
];

/** Gesichtsausschnitt (Avatar) zu einem Namen aus Alt-Texten/Autorenangaben */
export const faceOf = (name: string) => team.find((m) => name.startsWith(m.name))?.face;

/** Kundenavatare neben der Google-Bewertung (wie auf der bisherigen Website, ohne Zitate) */
export const reviewFaces = ['ute_kern', 'karsten_pfeiffer', 'alihan_bekc', 'guiseppe_pescatore'].map((n) => `${M}/headbanner-testimonials/${n}.png`);

/** Personenfotos sind freigestellte Hochformate (PNG): Michael Oberholz = A/G, Michael Penn = B, Pascal Kopp = C/F,
 *  Lubka Röger = D, Felix Lesch = E. „team“ ist daraus zusammengesetzt (scripts/compose_team.py). */
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
  columns: MenuColumn[];
  promo: { image: string; eyebrow: string; title: string; to: string; stacked?: boolean };
  mobileCta: MenuLink;
};

export const megaMenus: MegaMenuData[] = [
  {
    label: 'Kaufen & Mieten', to: ROUTES.kaufen, title: 'Immobilien finden',
    text: 'Aktuelle Häuser, Wohnungen und Kapitalanlagen aus unserer Vermittlung in Münster, Essen, Bochum und Umgebung.',
    columns: [{
      eyebrow: 'Wohnimmobilien', links: [
        { label: 'Immobilien zum Kauf', to: ROUTES.kaufen }, { label: 'Immobilien zur Miete', to: ROUTES.mieten },
        { label: 'Wohnungen kaufen', to: ROUTES.wohnungKaufen }, { label: 'Kapitalanlagen & Mehrfamilienhäuser', to: ROUTES.kapitalanlage },
        { label: 'Immobilienfinanzierung', to: ROUTES.finanzierung }, { label: 'Budgetrechner: Kann ich kaufen?', to: ROUTES.budgetrechner },
        { label: 'Finanzierungsrechner', to: ROUTES.finanzierungsrechner },
      ],
    }],
    promo: { image: photos.team, eyebrow: 'Persönliche Beratung', title: 'Ihre Ansprechpartner in Münster, Essen und Bochum', to: ROUTES.regionen },
    mobileCta: { label: 'Alle Immobilien ansehen', to: ROUTES.kaufen },
  },
  {
    label: 'Immobilie verkaufen', to: ROUTES.verkaufen, title: 'Immobilie verkaufen',
    text: 'Marktwertermittlung, Exposé, Vermarktung und Notartermin – persönlich begleitet von unserem DIN-zertifizierten Team.',
    columns: [{
      eyebrow: 'Verkaufen & vermieten', links: [
        { label: 'Immobilie verkaufen', to: ROUTES.verkaufen }, { label: 'Kostenlose Immobilienbewertung', to: ROUTES.bewertung },
        { label: 'Immobilie vermieten', to: ROUTES.vermieten }, { label: 'Rückmietverkauf', to: ROUTES.rueckmietverkauf },
        { label: 'Immobilienvermarktung', to: ROUTES.vermarktung }, { label: 'Wert-Hebel-Rechner', to: ROUTES.wertHebel },
        { label: 'Immotipp: ab 500 € Prämie', to: ROUTES.immotipp },
      ],
    }],
    promo: { image: photos.bewertung, eyebrow: 'Immobilienbewertung', title: 'Fordern Sie eine kostenfreie und unverbindliche Bewertung an', to: ROUTES.bewertung },
    mobileCta: { label: 'Bewertung anfragen', to: ROUTES.bewertung },
  },
  {
    label: 'Immobilienmakler', to: ROUTES.regionen, title: 'Immobilienmakler vor Ort',
    text: 'Persönliche Ansprechpartner in Münster, Essen und Bochum – mit Gutachter- und Energiekompetenz unter einem Dach.',
    columns: [{
      eyebrow: 'Unsere Regionen', links: [
        { label: 'Immobilienmakler Münster', to: ROUTES.region('muenster') }, { label: 'Immobilienmakler Essen', to: ROUTES.region('essen') },
        { label: 'Immobilienmakler Bochum', to: ROUTES.region('bochum') }, { label: 'Alle Regionen', to: ROUTES.regionen },
        { label: 'Unser Team', to: ROUTES.team }, { label: 'Qualifikationen', to: ROUTES.qualifikation },
      ],
    }],
    promo: { image: photos.schluessel, eyebrow: 'Tippgeber-Programm', title: 'Immobilientipp geben – ab 500 € Prämie erhalten', to: ROUTES.immotipp },
    mobileCta: { label: 'Kontakt aufnehmen', to: ROUTES.kontakt },
  },
  {
    label: 'Kapitalanlage', to: ROUTES.kapitalanlage, title: 'Kapitalanlage',
    text: 'Mehrfamilienhäuser, vermietete Wohnungen und Renditeobjekte – mit Ertragswertanalyse und Finanzierung aus einer Hand.',
    columns: [{
      eyebrow: 'Anlageimmobilien', links: [
        { label: 'Mehrfamilienhäuser kaufen', to: ROUTES.kapitalanlage }, { label: 'Renditeobjekte im Angebot', to: `${ROUTES.kaufen}?anlage=1` },
        { label: 'Wohnungen als Kapitalanlage', to: ROUTES.wohnungKaufen }, { label: 'Mehrfamilienhaus verkaufen', to: ROUTES.verkaufen },
        { label: 'Immobilienbewertung', to: ROUTES.bewertung }, { label: 'Finanzierung', to: ROUTES.finanzierung },
      ],
    }],
    promo: { image: obj('170744873'), eyebrow: 'Aktuell im Angebot', title: 'Vermietetes Dreiparteienhaus in Bochum-Langendreer (Faktor 13,9)', to: ROUTES.expose('170744873') },
    mobileCta: { label: 'Renditeobjekte ansehen', to: `${ROUTES.kaufen}?anlage=1` },
  },
  {
    label: 'Unternehmen', to: ROUTES.ueberUns, title: 'Unternehmen',
    text: 'Seit über 20 Jahren begleiten wir Eigentümer, Käufer und Investoren – mit Immobilien-, Gutachter- und Energiekompetenz.',
    columns: [
      { eyebrow: 'Oberholz Immobilien', links: [
        { label: 'Über uns', to: ROUTES.ueberUns }, { label: 'Unser Team', to: ROUTES.team }, { label: 'Qualifikationen', to: ROUTES.qualifikation },
        { label: 'ISO 9001 Zertifizierung', to: ROUTES.iso }, { label: 'Kontakt', to: ROUTES.kontakt }, { label: 'Leistungen im Überblick', to: ROUTES.leistungen },
      ] },
      { eyebrow: 'Wissen & Service', links: [
        { label: 'Ratgeber', to: ROUTES.ratgeber }, { label: 'Immopedia', to: ROUTES.immopedia }, { label: 'Dokumente & Downloads', to: ROUTES.downloads },
        { label: 'Rechner & Werkzeuge', to: ROUTES.service }, { label: 'Immotipp', to: ROUTES.immotipp }, { label: 'Mein Bereich', to: ROUTES.meinBereich },
      ] },
    ],
    promo: { image: photos.team, eyebrow: 'Über uns', title: 'Immobilienvermittlung mit Gutachter- und Energiekompetenz', to: ROUTES.ueberUns, stacked: true },
    mobileCta: { label: 'Kontakt aufnehmen', to: ROUTES.kontakt },
  },
];

export const hero = {
  title: 'Finden Sie Ihr neues Zuhause!',
  modes: ['Kaufen', 'Mieten', 'KI-Suche'] as const,
  placeholder: 'Stadt, Stadtteil, Postleitzahl oder Objekt-Nr.',
  propertyTypes: [
    { group: 'Wohnen', options: ['Haus', 'Wohnung', 'Grundstück'] },
    { group: 'Kapitalanlage', options: [] },
  ],
  /** Slider mit echten Objekten (IDs aus src/data/listings.json) */
  slideIds: ['170212293', '170022736', '170680511', '170649223', '170934647'],
  teasers: [
    { image: obj('170212293', 1), title: 'Immobilie kaufen', label: 'Aktuelle Immobilien ansehen', to: ROUTES.kaufen },
    { image: photos.bewertung, title: 'Kostenlose Bewertung', label: 'Marktwert Ihrer Immobilie ermitteln', to: ROUTES.bewertung },
    { image: face('michael-penn'), title: 'Immotipp: ab 500 € Prämie', label: 'Tipp geben und Prämie erhalten', to: ROUTES.immotipp },
  ],
};

export const selling = {
  eyebrow: 'Immobilie verkaufen',
  title: 'Ihr Immobilienmakler in Münster, Essen und Bochum – mehr als ein klassischer Makler',
  text: 'Ein konventioneller Makler inseriert und vermittelt. Wir beurteilen Ihre Immobilie zusätzlich als erfahrenes Team aus Maklern, Gutachtern und Energieberatern: von der Marktwertermittlung über Exposé und Strategie bis zur Schlüsselübergabe.',
  benefits: [
    { icon: 'pin', title: 'Persönlich vor Ort', text: 'Verkauf und Vermietung mit festem Ansprechpartner in Münster, Essen, Bochum und Umgebung.' },
    { icon: 'globe', title: 'Gutachterkompetenz', text: 'DIN-zertifizierte Marktwertermittlung als Basis für eine realistische Preisstrategie.' },
    { icon: 'advisor', title: 'Alles aus einer Hand', text: 'Exposé, Grundrisse, Energieausweis und Finanzierung – von Architekten, Gutachtern und Beratern im eigenen Haus.' },
  ],
  card: {
    image: photos.verkauf,
    alt: 'Makler und Eigentümerpaar besiegeln einen Hausverkauf per Handschlag',
    title: 'Erfolgreich verkaufen – mit Oberholz Immobilien',
    text: 'Über unser Banken-Netzwerk finden wir finanzierungsstarke Käufer, verhandeln in Ihrem Interesse und begleiten Sie bis zur Übergabe.',
    cta: 'Jetzt erfolgreich verkaufen',
    to: ROUTES.verkaufen,
  },
};

export const financeBanner = {
  image: photos.finanzierung,
  alt: 'Finanzierungsberatung mit einem jungen Paar am Laptop',
  wordmark: 'Oberholz',
  sub: 'Finanzierung',
  claim: 'Immobilienfinanzierung mit Energiekompetenz.',
  link: 'Finanzierung anfragen',
  to: ROUTES.finanzierung,
};

export const cities = {
  eyebrow: 'Immobilie kaufen',
  title: 'Finden Sie Immobilien in Ihrer Region',
  text: 'Aktuelle Häuser, Wohnungen und Kapitalanlagen aus unserer Vermittlung – mit persönlichem Ansprechpartner vor Ort in Münster, Essen, Bochum und Umgebung.',
  items: [
    { name: 'Münster', image: '/assets/stock/staedte/muenster.jpg', to: ROUTES.region('muenster') },
    { name: 'Essen', image: '/assets/stock/staedte/essen.jpg', to: ROUTES.region('essen') },
    { name: 'Bochum', image: '/assets/stock/staedte/bochum.jpg', to: ROUTES.region('bochum') },
    { name: 'Düsseldorf', image: '/assets/stock/staedte/duesseldorf.jpg', to: `${ROUTES.kaufen}?ort=D%C3%BCsseldorf` },
    { name: 'Duisburg', image: '/assets/stock/staedte/duisburg.jpg', to: `${ROUTES.kaufen}?ort=Duisburg` },
    { name: 'Münsterland', image: '/assets/stock/staedte/muensterland.jpg', to: `${ROUTES.kaufen}?ort=M%C3%BCnsterland` },
  ],
  subtitle: 'Immobilien in der Umgebung',
};

export const careers = {
  eyebrow: 'Unser Team',
  title: 'Persönliche Beratung von Menschen, die Ihre Region kennen',
  text: 'Makler, Gutachter, Energieberater und Architekten unter einem Dach – seit über 20 Jahren begleiten wir Eigentümer, Käufer und Investoren.',
  card: {
    image: photos.team,
    alt: 'Das Team von Oberholz Immobilien',
    title: 'Ihr Team in Münster, Essen und Bochum',
    text: 'Michael Oberholz und sein Team beraten Sie persönlich – unsere Erstberatungsgespräche sind unverbindlich und kostenlos.',
    cta: 'Team kennenlernen',
    to: ROUTES.team,
  },
};

export const lifestyle = {
  title: 'Aus unserer Vermittlung',
  text: 'Einblicke in Häuser und Wohnungen aus unserer Vermittlung in Münster, im Münsterland und im Ruhrgebiet – persönlich begleitet von der ersten Einschätzung bis zum erfolgreichen Vertragsabschluss.',
  galleryButton: 'Zur Galerie',
  more: 'Mehr erfahren',
  items: [
    { image: obj('170022736', 1), title: 'Einfamilienhaus mit Garten in Stadtlohn', alt: 'Einfamilienhaus in Stadtlohn' },
    { image: obj('170212293', 3), title: 'Reihenendhaus in Essen-Kupferdreh', alt: 'Garten eines Reihenendhauses in Essen-Kupferdreh' },
    { image: obj('170199527', 2), title: 'Maisonettewohnung in Velbert-Neviges', alt: 'Dachterrasse mit Ausblick in Velbert' },
    { image: obj('170649223'), title: 'Reihenhaus in Bergkamen-Oberaden', alt: 'Reihenhaus mit Garten in Bergkamen' },
    { image: obj('170680511', 1), title: 'Reihenhaus in Duisburg-Walsum', alt: 'Garten eines Reihenhauses in Duisburg' },
    { image: obj('170827695', 5), title: 'Maisonettewohnung in Münster-Mecklenbeck', alt: 'Balkon mit Blick über Münster-Mecklenbeck' },
  ],
};

export const magazine = {
  eyebrow: 'Ratgeber & Leitfäden',
  title: 'Wissen für Eigentümer, Käufer und Erben',
  text: 'Fundierte Beiträge zu Marktentwicklung, Verkauf, Bewertung und Energie – mit Quellen belegt. Dazu unsere Leitfäden zum Download, vom Erben-Kompass bis zum Whitepaper zum Generationenwechsel.',
  card: {
    image: '/assets/ratgeber/immobilie-geerbt-der-erben-kompass-fuer-die-ersten-wochen.jpg',
    alt: 'Hände sortieren Familienfotos, Briefe und Hausschlüssel',
    title: 'Der Erben-Kompass',
    text: 'Der Praxisleitfaden für Immobilienerben: erste Schritte, Erbengemeinschaft, Steuern und Fristen, Notar-Ablauf. 12 Seiten mit Checkliste.',
    cta: 'Leitfaden anfordern',
    to: ROUTES.whitepaper('erben-kompass'),
  },
};

const groupLinks = (places: string[]) => ({
  haus: places.map((p) => `Haus kaufen in ${p}`),
  wohnung: places.map((p) => `Wohnung kaufen in ${p}`),
});

export const relatedTopics = {
  eyebrow: 'Weitere Themen',
  title: 'Das könnte Sie auch interessieren',
  groups: [
    { icon: 'apartment', title: 'Immobilien im Münsterland', text: 'Häuser und Wohnungen in Münster und den umliegenden Kreisen.', ...groupLinks(['Münster', 'Steinfurt', 'Coesfeld', 'Rheine', 'Stadtlohn']) },
    { icon: 'house', title: 'Immobilien im Ruhrgebiet', text: 'Häuser, Wohnungen und Kapitalanlagen zwischen Essen, Bochum und Duisburg.', ...groupLinks(['Essen', 'Bochum', 'Duisburg', 'Bergkamen', 'Bottrop']) },
    { icon: 'townhouse', title: 'Immobilien in NRW', text: 'Weitere Angebote aus unserer Vermittlung in Nordrhein-Westfalen.', ...groupLinks(['Düsseldorf', 'Velbert', 'Krefeld', 'Kamp-Lintfort']) },
  ],
};

export const contact = {
  eyebrow: 'Kontakt',
  title: 'Kontaktieren Sie uns jetzt – persönlich',
  avatars: [team[0].face, team[1].face],
  office: 'Oberholz Immobilien',
  cta: 'Jetzt kontaktieren',
};

export const footer = {
  title: 'Kontaktieren Sie uns',
  socials: ['linkedin', 'google', 'whatsapp'] as const,
  columns: [
    { title: 'Immobilienangebote', links: [
      { label: 'Haus kaufen', to: `${ROUTES.kaufen}?typ=Haus` }, { label: 'Wohnung kaufen', to: `${ROUTES.kaufen}?typ=Wohnung` },
      { label: 'Grundstück kaufen', to: `${ROUTES.kaufen}?typ=Grundst%C3%BCck` }, { label: 'Wohnung mieten', to: ROUTES.mieten },
      { label: 'Kapitalanlagen', to: ROUTES.kapitalanlage },
    ] },
    { title: 'Immobilien verkaufen', links: [
      { label: 'Immobilie bewerten', to: ROUTES.bewertung }, { label: 'Immobilie verkaufen', to: ROUTES.verkaufen },
      { label: 'Immobilie vermieten', to: ROUTES.vermieten }, { label: 'Rückmietverkauf', to: ROUTES.rueckmietverkauf }, { label: 'Immotipp', to: ROUTES.immotipp },
    ] },
    { title: 'Immobilienmakler finden', links: [
      { label: 'Immobilienmakler Münster', to: ROUTES.region('muenster') }, { label: 'Immobilienmakler Essen', to: ROUTES.region('essen') },
      { label: 'Immobilienmakler Bochum', to: ROUTES.region('bochum') }, { label: 'Unsere Regionen', to: ROUTES.regionen },
      { label: 'Google-Bewertungen', to: '#bewertungen' },
    ] },
    { title: 'Unternehmen', links: [
      { label: 'Über uns', to: ROUTES.ueberUns }, { label: 'Unser Team', to: ROUTES.team }, { label: 'Qualifikationen', to: ROUTES.qualifikation },
      { label: 'Partner & Kooperationen', to: `${ROUTES.ueberUns}#partner` }, { label: 'Ratgeber', to: ROUTES.ratgeber }, { label: 'Immopedia', to: ROUTES.immopedia },
      { label: 'Dokumente & Downloads', to: ROUTES.downloads }, { label: 'Rechner & Werkzeuge', to: ROUTES.service }, { label: 'Kontakt', to: ROUTES.kontakt },
    ] },
  ],
  legalLeft: [{ label: 'Cookie-Einstellungen verwalten', to: '#cookies' }, { label: 'Cookie-Hinweise', to: ROUTES.cookieHinweise }],
  legalRight: [{ label: 'Datenschutzhinweise', to: ROUTES.datenschutz }, { label: 'Impressum', to: ROUTES.impressum }],
};
