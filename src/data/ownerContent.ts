import type { QA, RichBlock } from './oberholz';

export type OwnerKind = 'makler' | 'verkaufen' | 'bewertung' | 'wohnung';
export type OwnerCity = 'essen' | 'bochum';
export type OwnerContent = {
  title: string;
  metaTitle: string;
  description: string;
  intro: string;
  checks: string[];
  blocks: RichBlock[];
  faq: QA[];
};

const h2 = (text: string): RichBlock => ({ t: 'h2', text });
const h3 = (text: string): RichBlock => ({ t: 'h3', text });
const p = (text: string): RichBlock => ({ t: 'p', text });
const ul = (...items: string[]): RichBlock => ({ t: 'ul', items });

// Redaktion auf Basis der Keyword-Planer-Abfragen Juli–September 2026.
// Suchvolumen und Forensik-Hochrechnungen sind keine Aussagen über einzelne Objekte.
const local = {
  essen: {
    city: 'Essen',
    districts: 'Rüttenscheid, Bredeney, Kettwig, Werden, Kupferdreh oder Altenessen',
    market: 'Der Essener Grundstücksmarktbericht unterscheidet unter anderem bebaute Grundstücke, Wohnungseigentum und Immobilienrichtwerte. Für Ihre Entscheidung kommt es darauf an, welches Vergleichssegment zu Ihrem Haus oder Ihrer Wohnung passt. Ein Durchschnitt über die ganze Stadt bildet weder die einzelne Straße noch den Zustand Ihrer Immobilie ab.',
    house: 'Beim Hausverkauf in Essen schauen wir auf das Zusammenspiel von Grundstück, Gebäude und Mikrolage. Ein Reihenhaus in Kupferdreh, ein Einfamilienhaus in Kettwig und ein Altbau in Rüttenscheid lassen sich nicht mit demselben pauschalen Quadratmeterpreis bewerten. Wir besprechen, welche Vergleichsobjekte geeignet sind und welche Besonderheiten Ihrer Immobilie berücksichtigt werden müssen.',
    flat: 'Eine Wohnung in Rüttenscheid spricht je nach Größe, Grundriss und Nutzung andere Käufer an als eine vermietete Wohnung in Altenessen oder eine Maisonette in Werden. Für die Vermarktung Ihrer Essener Eigentumswohnung betrachten wir deshalb die konkrete Wohnlage und den Status der Wohnung gemeinsam mit den Unterlagen der Eigentümergemeinschaft.',
    valuation: 'Was ist mein Haus in Essen wert? Die Antwort beginnt bei der Adresse und dem Zustand, nicht bei einem pauschalen Stadtwert. Wir erfassen Grundstück, Wohnfläche, Modernisierungen und Nutzung. Ob Ihre Immobilie in Bredeney, Kettwig oder einem anderen Essener Stadtteil liegt: Entscheidend bleibt die einzelne Immobilie.',
    source: { title: 'Gutachterausschuss Essen: Grundstücksmarktbericht 2026', href: 'https://gmb.gutachterausschuss-essen.de/' },
  },
  bochum: {
    city: 'Bochum',
    districts: 'Stiepel, Weitmar, Wattenscheid, Langendreer, Linden oder Wiemelhausen',
    market: 'Der Bochumer Gutachterausschuss leitet seine Marktdaten aus ausgewerteten Kaufverträgen ab und veröffentlicht neben dem Grundstücksmarktbericht auch einen Zwischenbericht. Diese Daten helfen, tatsächliche Abschlüsse von bloßen Angebotspreisen zu unterscheiden. Die Übertragung auf Ihre Immobilie erfordert zusätzlich den Blick auf Lage, Zustand und Nutzung.',
    house: 'Für einen Hausverkauf in Bochum prüfen wir zuerst, was genau verkauft werden soll: etwa ein selbst genutztes Haus in Stiepel, ein Reihenhaus in Weitmar oder ein vermietetes Objekt in Langendreer. Neben dem Grundstück und dem Gebäudezustand beeinflussen bestehende Mietverhältnisse, Modernisierungen und die verfügbaren Unterlagen die Verkaufsstrategie.',
    flat: 'Beim Wohnungsverkauf in Bochum zählt nicht nur der Eindruck bei der Besichtigung. Eine Wohnung in Wattenscheid, Weitmar oder Wiemelhausen ist zugleich Teil einer Eigentümergemeinschaft. Käufer müssen deshalb auch Hausgeld, Rücklage und geplante Maßnahmen am Gebäude nachvollziehen können. Diese Informationen bereiten wir gemeinsam mit den Wohnungsunterlagen auf.',
    valuation: 'Wie viel ist Ihre Immobilie in Bochum wert? Wir unterscheiden zwischen dem Wert eines selbst genutzten Hauses, einer Eigentumswohnung und eines vermieteten Objekts. Bei einer Wohnung in Weitmar können beispielsweise die Unterlagen der Gemeinschaft besonders wichtig sein, bei einem Mietshaus in Langendreer die Erträge und der Instandhaltungsbedarf. Die Bewertung richtet sich nach Ihrem Objekt.',
    source: { title: 'Gutachterausschuss Bochum: Grundstücksmarkt- und Zwischenberichte', href: 'https://gars.nrw/bochum/produkte-bochum/grundstuecksmarktberichte-bochum' },
  },
} as const;

export const ownerMarketSource = (city: OwnerCity) => local[city].source;

export function ownerContent(slug: OwnerCity, kind: OwnerKind): OwnerContent {
  const l = local[slug];
  const city = l.city;
  const valuationFaq: QA[] = [
    { q: `Was ist mein Haus in ${city} wert?`, a: 'Der Marktwert hängt unter anderem von der konkreten Lage, Grundstück und Wohnfläche, Zustand, Modernisierungen und Nutzung ab. Für eine persönliche Einschätzung sehen wir uns Ihre Angaben und Unterlagen an und besprechen einen Vor-Ort-Termin. Einen pauschalen Wert ohne diese Prüfung nennen wir nicht.' },
    { q: `Ist die Immobilienbewertung in ${city} kostenlos?`, a: 'Unsere erste Marktwerteinschätzung im Rahmen eines Verkaufs- oder Vermietungsgesprächs ist kostenlos und unverbindlich. Wenn Sie ein förmliches Gutachten benötigen, klären wir Zweck, Umfang und mögliche Kosten vor einer Beauftragung.' },
    { q: 'Ist ein Bodenrichtwert der Wert meines Hauses?', a: 'Nein. Der Bodenrichtwert bezieht sich auf den Boden einer Richtwertzone. Für den Wert einer bebauten Immobilie müssen zusätzlich das Gebäude und die konkreten Eigenschaften von Grundstück und Nutzung berücksichtigt werden.' },
    { q: 'Welche Unterlagen helfen bei der Wertermittlung?', a: 'Hilfreich sind Adresse, Baujahr, Wohn- und Grundstücksfläche, Grundrisse, Angaben zu Modernisierungen und ein vorhandener Energieausweis. Bei Wohnungen kommen Unterlagen der Eigentümergemeinschaft hinzu, bei vermieteten Objekten Mietverträge und eine Übersicht der Erträge.' },
    { q: 'Kann ich vor einer Verkaufsentscheidung eine Bewertung anfragen?', a: 'Ja. Eine Einschätzung kann helfen, Verkauf, Vermietung oder eine spätere Entscheidung abzuwägen. Beschreiben Sie uns Ihren Anlass und den Stand Ihrer Überlegungen.' },
  ];

  if (kind === 'bewertung') return {
    title: `Immobilienbewertung in ${city}`,
    metaTitle: `Immobilienbewertung ${city} – persönlich vor Ort`,
    description: `Immobilienbewertung in ${city}: Haus oder Wohnung persönlich einschätzen lassen. Lage, Zustand und Unterlagen prüfen. Kostenloses Erstgespräch anfragen.`,
    intro: `Was ist Ihr Haus oder Ihre Wohnung in ${city} wert? Wir betrachten Lage, Zustand und Unterlagen persönlich mit Ihnen – als nachvollziehbare Grundlage für Ihre nächste Entscheidung.`,
    checks: ['Persönliche Einschätzung statt pauschalem Onlinepreis', 'Haus, Eigentumswohnung oder vermietete Immobilie', 'Kostenloses und unverbindliches Erstgespräch'],
    blocks: [
      h2(`Immobilienwert in ${city} ermitteln: von den Daten zur Entscheidung`),
      p(l.valuation),
      p('Ein Angebotspreis im Immobilienportal zeigt, welchen Preis ein Verkäufer anstrebt. Er belegt noch keinen tatsächlich gezahlten Kaufpreis. Wir betrachten deshalb geeignete Vergleichsdaten und prüfen, wie gut sie zu Ihrer Immobilie passen. Das Ergebnis dient als Grundlage für eine Preisstrategie, nicht als Garantie eines späteren Verkaufserlöses.'),
      h2('Was den Wert Ihres Hauses oder Ihrer Wohnung beeinflusst'),
      ul('Mikrolage: Straße, Umfeld, Erreichbarkeit und konkrete Grundstückssituation.', 'Objekt: Baujahr, Wohnfläche, Grundriss, Ausstattung und baulicher Zustand.', 'Energie und Modernisierung: vorhandene Nachweise, bekannte Maßnahmen und erkennbarer Handlungsbedarf.', 'Nutzung: selbst genutzt, leer stehend oder vermietet sowie bestehende Besonderheiten.'),
      h2(`Welche Marktdaten sind für ${city} sinnvoll?`), p(l.market),
      p('Bodenrichtwerte und Immobilienrichtwerte sind Orientierungshilfen. Sie müssen auf das konkrete Objekt bezogen werden. Der Marktwert einer bebauten Immobilie ergibt sich daher nicht allein aus Grundstücksfläche mal Bodenrichtwert.'),
      h2('So läuft die persönliche Bewertung ab'),
      h3('Ihr Objekt und Ihren Anlass kennenlernen'), p('Sie nennen uns die Adresse, die Objektart und Ihr Anliegen. Geht es um einen geplanten Verkauf, eine geerbte Immobilie oder die Frage, ob Sie zunächst vermieten möchten? Wir klären, welche Einschätzung Sie dafür benötigen.'),
      h3('Unterlagen und Zustand einordnen'), p('Wir sichten die verfügbaren Angaben und besprechen die Besichtigung. Fehlende Pläne oder Nachweise halten wir fest, damit die Bewertung nachvollziehbar bleibt.'),
      h3('Einschätzung und nächste Schritte besprechen'), p('Wir erläutern die wertbestimmenden Faktoren und leiten daraus eine passende Verkaufs- oder Entscheidungsgrundlage ab. Sie können anschließend entscheiden, ob und wann Sie weitergehen möchten.'),
      h2('Marktwerteinschätzung oder förmliches Gutachten?'),
      p('Für die Vorbereitung eines Verkaufs ist eine persönliche Marktwerteinschätzung ein sinnvoller Einstieg. Soll die Bewertung in einem gerichtlichen, steuerlichen oder anderen förmlichen Verfahren verwendet werden, muss vorher geklärt werden, welche Art von Gutachten und welcher Nachweis dort benötigt werden. Beides ist nicht automatisch dieselbe Leistung.'),
    ], faq: valuationFaq,
  };

  if (kind === 'wohnung') return {
    title: `Wohnung verkaufen in ${city}`,
    metaTitle: `Wohnung verkaufen ${city} – Eigentümerberatung`,
    description: `Eigentumswohnung in ${city} verkaufen: Marktwert, WEG-Unterlagen, Hausgeld und Vermietung einordnen. Persönliche Begleitung durch Oberholz Immobilien.`,
    intro: `Sie möchten Ihre Eigentumswohnung in ${city} verkaufen? Wir klären mit Ihnen den Marktwert, die Unterlagen der Eigentümergemeinschaft und die passende Vermarktung – für freie und vermietete Wohnungen.`,
    checks: ['Bewertung von Wohnung und Gemeinschaft zusammen denken', 'Freie oder vermietete Eigentumswohnung', 'Unterlagen, Vermarktung und Übergabe persönlich begleiten'],
    blocks: [
      h2(`Eigentumswohnung in ${city}: den Verkauf vom Käufer her vorbereiten`),
      p(l.flat),
      p('Käufer interessieren sich für den Grundriss und die Lage, aber auch für die laufenden Kosten und den Zustand des gesamten Hauses. Wir bereiten Ihre Wohnung so auf, dass diese Fragen früh beantwortet werden. Das erleichtert eine sachliche Kaufentscheidung und hilft, vermeidbare Rückfragen vor dem Notartermin zu reduzieren.'),
      h2('Welche Unterlagen sind für den Wohnungsverkauf wichtig?'),
      ul('Grundriss, Wohnflächenangaben, Grundbuchauszug und vorhandener Energieausweis.', 'Teilungserklärung und Gemeinschaftsordnung sowie gegebenenfalls Nachträge.', 'Aktueller Wirtschaftsplan, Hausgeldabrechnungen und Stand der Erhaltungsrücklage.', 'Beschlusssammlung beziehungsweise relevante Versammlungsprotokolle und Informationen zu beschlossenen Maßnahmen.', 'Bei Vermietung: Mietvertrag, aktuelle Miethöhe und Angaben zu bestehenden Vereinbarungen.'),
      p('Welche Unterlagen im Einzelfall benötigt werden, hängt von der Wohnung und der Gemeinschaft ab. Fehlende Dokumente besprechen wir frühzeitig mit Ihnen und stimmen ab, was bei der Verwaltung angefragt werden sollte.'),
      h2('Freie und vermietete Wohnung brauchen unterschiedliche Strategien'),
      p('Eine freie Wohnung kann für Selbstnutzer und Kapitalanleger interessant sein. Bei einer vermieteten Wohnung stehen zusätzlich die Mietunterlagen, laufenden Erträge und die langfristige Nutzung im Vordergrund. Der bestehende Mietvertrag wird durch den Verkauf grundsätzlich nicht beendet; der Erwerber tritt nach § 566 BGB in das Mietverhältnis ein. Eine spätere freie Übergabe darf deshalb nicht ungeprüft zugesagt werden.'),
      h2('Hausgeld und geplante Maßnahmen offen darstellen'),
      p('Hausgeld, Rücklage und mögliche Sonderumlagen können die Entscheidung von Interessenten beeinflussen. Wir unterscheiden deshalb Kosten der einzelnen Wohnung von Themen des Gemeinschaftseigentums. Wenn etwa Arbeiten an Dach, Fassade oder Heizung diskutiert oder beschlossen sind, gehören die verfügbaren Informationen in die Verkaufsvorbereitung.'),
      h2(`Wie finden wir den Angebotspreis Ihrer Wohnung in ${city}?`),
      p(`${l.market} Hinzu kommen bei einer Eigentumswohnung zum Beispiel Etage, Aufzug, Balkon, Grundriss, Vermietungsstatus und der Zustand des Gemeinschaftseigentums. Der Preis einer benachbarten Wohnung ist deshalb ein Vergleichspunkt, aber kein automatisch übertragbarer Wert.`),
      h2('Vom ersten Gespräch bis zur Übergabe'),
      p('Zuerst besprechen wir Ihre Ziele und den gewünschten Zeitrahmen. Anschließend folgen Bewertung und Unterlagenprüfung, die Vorbereitung des Exposés und die Vermarktung. Wir koordinieren Besichtigungen und Rückfragen, begleiten die Verhandlungen und stimmen die nächsten Schritte bis zum Notartermin und zur Übergabe mit Ihnen ab.'),
    ],
    faq: [
      { q: `Wie verkaufe ich meine Eigentumswohnung in ${city}?`, a: 'Beginnen Sie mit einer realistischen Bewertung und den Unterlagen der Wohnung und Eigentümergemeinschaft. Darauf folgen Preisstrategie, Exposé, Besichtigungen und Verhandlung. Erst nach der Einigung werden die Schritte zum notariellen Kaufvertrag und zur Übergabe abgestimmt.' },
      { q: 'Kann ich eine vermietete Wohnung verkaufen?', a: 'Ja. Die Wohnung kann mit bestehendem Mietverhältnis verkauft werden. Der Verkauf beendet den Mietvertrag grundsätzlich nicht. Wir bereiten die Mietunterlagen und die Informationen zur Gemeinschaft für die Vermarktung auf.' },
      { q: 'Warum sind Rücklage und Hausgeld für Käufer wichtig?', a: 'Sie helfen, die laufenden Kosten und die finanzielle Situation der Gemeinschaft einzuordnen. Zusammen mit den Beschlüssen und dem Gebäudezustand geben sie Hinweise auf mögliche künftige Aufwendungen. Eine Rücklage allein garantiert nicht, dass alle geplanten Arbeiten finanziert sind.' },
      { q: `Wie lange dauert ein Wohnungsverkauf in ${city}?`, a: 'Eine feste Dauer lässt sich ohne Objektprüfung nicht seriös nennen. Preis, Lage, Zustand, Vermietung und Vollständigkeit der Unterlagen beeinflussen den Ablauf. Im Erstgespräch besprechen wir Ihre zeitlichen Ziele und mögliche Abhängigkeiten.' },
      { q: 'Muss ich meine Wohnung vor dem Verkauf renovieren?', a: 'Nicht jede Maßnahme zahlt sich im Verkauf aus. Vor größeren Ausgaben sollten Kosten, möglicher Mehrerlös und Zeitbedarf gegenübergestellt werden. Ein aufgeräumter und nachvollziehbar dokumentierter Zustand ist oft der sinnvollere erste Schritt.' },
    ],
  };

  const selling = kind === 'verkaufen';
  return {
    title: selling ? `Haus oder Immobilie verkaufen in ${city}` : `Ihr Immobilienmakler in ${city} – persönlich an Ihrer Seite`,
    metaTitle: selling ? `Hausverkauf ${city} – Immobilie verkaufen` : `Immobilienmakler ${city} – Verkauf & Bewertung`,
    description: selling
      ? `Haus oder Immobilie in ${city} verkaufen: Bewertung, Unterlagen und Vermarktung mit klarer Strategie. Oberholz Immobilien begleitet Sie persönlich.`
      : `Immobilienmakler in ${city}: Oberholz Immobilien begleitet Eigentümer bei Bewertung, Hausverkauf, Wohnungsverkauf und Vermietung. Persönlich vor Ort.`,
    intro: selling ? `Sie möchten Ihr Haus oder Ihre Immobilie in ${city} verkaufen? Wir begleiten Sie von der ersten Bewertung über Unterlagen und Vermarktung bis zur Übergabe – mit einer Strategie, die zu Ihrem Objekt und Ihren Zielen passt.` : `Sie möchten Ihre Immobilie in ${city} verkaufen, vermieten oder zunächst ihren Wert kennen? Wir begleiten Sie mit persönlicher Beratung, einer nachvollziehbaren Bewertung und einer Vermarktung, die zu Ihrem Objekt passt.`,
    checks: ['Ein fester Ansprechpartner für Ihr Vorhaben', 'Bewertung und Unterlagen gemeinsam betrachten', 'Verkaufsstrategie passend zu Ihrer Immobilie'],
    blocks: [
      h2(selling ? `Hausverkauf in ${city}: zuerst den Ausgangspunkt klären` : `Wobei wir Eigentümer in ${city} unterstützen`),
      p(selling ? 'Bevor ein Exposé entsteht, klären wir Ihre Ziele: Soll ein selbst genutztes Haus verkauft werden, geht es um ein Erbe oder möchten Sie eine Kapitalanlage veräußern? Auch der Zeitrahmen, bestehende Mietverhältnisse und bekannte Arbeiten am Gebäude gehören in dieses erste Gespräch.' : 'Eine gute Maklerbegleitung beginnt mit Ihrer Situation. Bei einem geplanten Hausverkauf stehen Preis und Ablauf im Mittelpunkt. Bei einer Eigentumswohnung kommt die Gemeinschaft hinzu, bei einer vermieteten Immobilie die laufende Nutzung. Wenn Sie noch zwischen Verkauf und Vermietung abwägen, schaffen wir zunächst eine Grundlage für diese Entscheidung.'),
      h2(`Lage und Objekt in ${city} einzeln betrachten`),
      p(l.house),
      ...(selling ? [p(l.market)] : []),
      p(`Wir besprechen Immobilien unter anderem in ${l.districts}. Die Nennung eines Stadtteils ersetzt keine Objektprüfung: Straße, Gebäudezustand, Grundstück und Nutzung bleiben entscheidend. Deshalb beginnen wir mit Ihren konkreten Angaben statt mit einem pauschalen Preisversprechen.`),
      h2(selling ? 'So bereiten wir Ihren Immobilienverkauf vor' : 'So arbeiten wir mit Ihnen zusammen'),
      h3('Bewertung und Preisstrategie'), p('Wir ordnen Lage, Zustand und Unterlagen ein und besprechen einen nachvollziehbaren Angebotspreis. Dabei unterscheiden wir den angestrebten Verkaufspreis von einem bereits belegten Marktwert.'),
      h3('Unterlagen und Präsentation'), p('Wir sichten die vorhandenen Dokumente und halten fest, was ergänzt werden muss. Auf dieser Grundlage entstehen die Objektpräsentation und die Informationen für Interessenten und finanzierende Banken.'),
      h3('Vermarktung und Abschluss'), p('Wir stimmen die Käuferansprache mit Ihnen ab, koordinieren Besichtigungen und begleiten Rückfragen und Verhandlungen. Nach einer Einigung unterstützen wir bei der Abstimmung bis zum Notartermin und zur Übergabe.'),
      h2('Wenn sich Ihre Lebenssituation verändert'),
      p('Eine geerbte Immobilie, eine Trennung oder der Wunsch nach einem kleineren Zuhause können sehr unterschiedliche Entscheidungen erfordern. Zunächst sollten Ziel, Nutzung und finanzielle Möglichkeiten geklärt werden. Eine Bewertung hilft bei der Orientierung; rechtliche oder steuerliche Einzelheiten werden bei Bedarf mit den zuständigen Fachleuten abgestimmt.'),
      h2('Unsaniertes Haus, vermietete Wohnung oder Mehrfamilienhaus?'),
      p('Bei älteren Häusern stellt sich oft die Frage, ob vor dem Verkauf noch modernisiert werden sollte. Bei vermieteten Wohnungen und Mehrfamilienhäusern gehören Mietunterlagen und Instandhaltung in die Vorbereitung. Wir betrachten diese Themen zusammen mit der Bewertung, bevor Sie größere Ausgaben oder einen Verkaufstermin festlegen.'),
    ],
    faq: [
      { q: `Wie finde ich einen passenden Immobilienmakler in ${city}?`, a: 'Fragen Sie, wie die Bewertung begründet wird, welche Leistungen der Auftrag umfasst und wer Sie persönlich betreut. Lassen Sie sich die geplante Vermarktung und die Konditionen erklären. Ein konkreter Ablauf ist aussagekräftiger als ein pauschales Versprechen zum höchsten Preis.' },
      { q: `Was kostet die Begleitung beim Hausverkauf in ${city}?`, a: 'Die Kosten richten sich nach dem vereinbarten Auftrag und den anwendbaren rechtlichen Vorgaben. Wir besprechen die Leistungen und Konditionen vor der Beauftragung mit Ihnen. Eine erste Beratung ist kostenlos und unverbindlich.' },
      { q: `Wie lange dauert es, ein Haus in ${city} zu verkaufen?`, a: 'Das hängt unter anderem von Lage, Zustand, Preisstrategie und der Vollständigkeit der Unterlagen ab. Auch die Finanzierung des Käufers und die Abwicklung des Kaufvertrags benötigen Zeit. Einen festen Verkaufstermin können wir ohne Prüfung nicht zusagen.' },
      { q: 'Welche Unterlagen sollte ich zum ersten Gespräch bereithalten?', a: 'Adresse, Grundrisse, Baujahr, Wohnfläche und Angaben zu Modernisierungen sind ein guter Anfang. Hilfreich sind außerdem ein vorhandener Energieausweis und Grundbuchunterlagen. Bei vermieteten Objekten und Eigentumswohnungen sehen wir uns zusätzlich Miet- beziehungsweise Gemeinschaftsunterlagen an.' },
      { q: 'Kann ich auch eine geerbte oder sanierungsbedürftige Immobilie anfragen?', a: 'Ja. Beschreiben Sie uns den Zustand, die aktuelle Nutzung und Ihre Überlegungen. Wir klären zunächst, welche Unterlagen und Einschätzungen für Ihre Entscheidung gebraucht werden. Ein sofortiger Verkaufsentschluss ist dafür nicht erforderlich.' },
    ],
  };
}
