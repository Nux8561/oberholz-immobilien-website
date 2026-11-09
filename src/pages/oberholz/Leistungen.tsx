// Leistungsseiten: Inhalte der bisherigen Website (content.json) im Seiten-Template-Layout.
import { page, homeFaq, textOf, type RichBlock } from '../../data/oberholz';
import { photos } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { faqLd, usePageMeta } from '../../layout/PageMeta';
import PageHero from '../../components/PageHero/PageHero';
import Rich, { FaqBlock, TeamStrip } from '../../components/Rich/Rich';
import Funnel from '../../components/Funnel/Funnel';
import Contact from '../../components/Contact/Contact';
import SectionIntro from '../../components/SectionIntro/SectionIntro';
import ContactForm from '../../components/ContactForm/ContactForm';
import { LineIcon } from '../../blocks/LineIcons';
import { OwnerGuides, OwnerLinks, SellSteps } from './LocalOwner';
import { documentsAnswer } from '../../data/ownerContent';
import {
  BTN_CALL, BTN_KONTAKT, PropertyStrip, ServiceGrid, TeaserBand, TOOL_TEASERS, short, splitIntro,
} from './shared';

const crumbs = (label: string) => [{ label }];
const teamOf = (blocks: RichBlock[]) => blocks.filter((b): b is Extract<RichBlock, { t: 'img' }> => b.t === 'img' && / - /.test(b.alt) && /bannerright/.test(b.src)).slice(0, 5);

/* ---------- generische Leistungsseite ---------- */

type ServiceOpts = {
  crumb: string; metaTitle: string; exclude: string; heroImage?: string; eyebrow: string;
  intent?: 'Verkaufen' | 'Vermieten'; funnel?: boolean; extra?: React.ReactNode; tools?: (keyof typeof TOOL_TEASERS)[];
  /** Teamleiste unter dem Kopf anzeigen (Finanzierung: nein, Kunde Runde 3) */
  teamStrip?: boolean;
};

function ServicePage(o: ServiceOpts & { k: string }) {
  const { title, text, checks, rest } = splitIntro(page(o.k).blocks);
  usePageMeta({ title: o.metaTitle, crumbs: crumbs(o.crumb), footer: 'accordion', description: text });
  const team = teamOf(rest.slice(0, 6));
  const body = rest.slice(team.length);
  return (
    <>
      <PageHero eyebrow={o.eyebrow} title={title} text={text} checks={checks?.map(short).slice(0, 4)} image={o.heroImage ?? team[0]?.src ?? photos.advisorA}
        alt="" cutout rating buttons={[o.funnel === false ? BTN_KONTAKT : { label: 'Jetzt anfragen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      {o.teamStrip !== false && team.length > 1 && <div className="rich"><div className="rich__wide"><TeamStrip imgs={team} /></div></div>}
      <Rich collapse blocks={body} />
      {o.extra}
      {o.funnel !== false && <Funnel intent={o.intent} />}
      {o.tools && <TeaserBand items={o.tools.map((t) => TOOL_TEASERS[t])} />}
      <ServiceGrid exclude={o.exclude} title="Weitere Leistungen" eyebrow="Das könnte Sie auch interessieren" />
      <Contact variant="page" />
    </>
  );
}

const sellFaq = [
  { q: 'Wie läuft ein Immobilienverkauf ab?', a: 'Zuerst besprechen wir Ihr Ziel, prüfen die Unterlagen und bewerten die Immobilie. Danach stimmen wir Angebotspreis und Vermarktung ab, koordinieren Besichtigungen und begleiten die Abstimmung mit Käufer und Notariat bis zur Übergabe.' },
  { q: 'Welche Unterlagen brauche ich zum Verkauf?', a: documentsAnswer },
  { q: 'Was ist meine Immobilie wert?', a: 'Entscheidend sind die konkrete Lage, Zustand, Fläche, Nutzung und die aktuelle Nachfrage. Ein städtischer Durchschnittspreis ersetzt keine Objektbewertung. Für Essen und Münster finden Sie auf unseren lokalen Bewertungsseiten die jeweiligen Besonderheiten und offiziellen Marktquellen.' },
  { q: 'Kann ich auch eine vermietete oder geerbte Immobilie verkaufen?', a: 'Ja. Bestehende Mietverhältnisse und die Eigentumssituation müssen dabei früh berücksichtigt werden. Wir ordnen die nächsten Schritte gemeinsam mit Ihnen ein; bei rechtlichen oder steuerlichen Fragen beziehen Sie bitte Ihr Notariat beziehungsweise Ihre Steuerberatung ein.' },
  { q: 'Lohnt sich ein Makler, wenn ich auch privat verkaufen könnte?', a: 'Privat zu verkaufen ist möglich. Aufwendig sind vor allem eine realistische Preisfindung, vollständige Unterlagen, die Prüfung der Kaufinteressenten auf ihre Finanzierung, die Besichtigungen und die Verhandlung bis zum Notartermin. Diese Schritte übernehmen wir für Sie, mit Gutachterkompetenz im Team. Ob sich das für Ihre Immobilie lohnt, besprechen wir offen im kostenlosen Erstgespräch.' },
  { q: 'Was, wenn meine Immobilie aus meiner Sicht mehr wert ist?', a: 'Wir begründen unsere Einschätzung mit Vergleichsdaten und den Besonderheiten Ihrer Immobilie und gehen Ihre Sicht gemeinsam mit Ihnen durch. Ein zu hoch angesetzter Angebotspreis verlängert häufig die Vermarktung und führt später zu Preisnachlässen. Die Entscheidung über den Angebotspreis treffen Sie.' },
  { q: 'Muss ich mich nach der Bewertung für einen Verkauf entscheiden?', a: 'Nein. Die erste Marktwerteinschätzung ist kostenlos und unverbindlich. Sie können sie auch nutzen, um Verkauf, Vermietung oder Abwarten in Ruhe abzuwägen.' },
  { q: 'Was kostet mich der Makler?', a: 'Das erste Gespräch und die Marktwerteinschätzung sind kostenlos. Beim Verkauf einer Wohnung oder eines Einfamilienhauses teilen sich Verkäufer und Käufer die Maklerprovision in der Regel zu gleichen Teilen. Höhe und Leistungen vereinbaren wir vor Beginn schriftlich mit Ihnen.' },
  { q: 'Wie lange dauert der Verkauf?', a: 'Die Dauer hängt unter anderem von Lage, Preis, Zustand, Unterlagen und der Finanzierung des Käufers ab. Einen festen Verkaufstermin können wir ohne Prüfung nicht zusagen, streben jedoch einen erfolgreichen Verkauf in den ersten sechs Monaten an.' },
];

export function Verkaufen() {
  usePageMeta({ title: 'Immobilie verkaufen in Essen, Münster & Umgebung', description: 'Haus oder Wohnung verkaufen: persönliche Bewertung, vollständige Unterlagen und begleitete Vermarktung mit Oberholz Immobilien in Essen, Münster und Umgebung.', crumbs: crumbs('Immobilie verkaufen'), footer: 'accordion', image: photos.advisorA, jsonLd: [faqLd(sellFaq)] });
  return <>
    <PageHero eyebrow="Immobilie verkaufen" title="Immobilie verkaufen in Essen und Münster" text="Erst der fundierte Marktwert, dann der passende Käufer. Ob Haus, Eigentumswohnung oder Mehrfamilienhaus: Wir begleiten Ihren Verkauf in Essen, Münster und Umgebung von der ersten Wertermittlung bis zur Schlüsselübergabe." checks={['Marktwert durch einen zertifizierten Immobiliengutachter', 'Bonitätsgeprüfte Käufer aus unserem Netzwerk', 'Ein fester Ansprechpartner in Essen oder Münster']} image={photos.advisorA} alt="Michael Oberholz" cutout rating buttons={[{ label: 'Verkauf besprechen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
    <SellSteps />
    <Funnel intent="Verkaufen" title="Lassen Sie uns über Ihren Verkauf sprechen" />
    <Rich collapse blocks={[{ t: 'h2', text: 'Ihr Objekt bestimmt die Strategie' }, { t: 'p', text: 'Beim Hausverkauf spielen das Grundstück, die Bausubstanz und der energetische Zustand eine wichtige Rolle. Bei der Eigentumswohnung kommen Hausgeld, Rücklagen und Beschlüsse der Eigentümergemeinschaft hinzu. Eine vermietete Immobilie wird zudem anhand ihrer Erträge und Mietverhältnisse eingeordnet.' }, { t: 'p', text: 'Wir erklären Ihnen, welche Faktoren den Preis Ihres Objekts beeinflussen, welche Unterlagen für Kaufinteressenten benötigt werden und welche weiteren Faktoren für Ihre Zielgruppe relevant sind. So schaffen wir eine belastbare Grundlage für Ihre Entscheidung.' }]} />
    <OwnerLinks exclude="makler" />
    <div className="rich"><div className="rich__text"><FaqBlock title="Häufige Fragen zum Immobilienverkauf" items={sellFaq} /></div></div>
    <OwnerGuides />
    <Contact variant="page" />
  </>;
}
export function Vermieten() {
  usePageMeta({ title: 'Immobilie vermieten und verpachten', crumbs: crumbs('Vermietung'), footer: 'accordion', description: 'Vermietung und Verpachtung mit Oberholz Immobilien: marktgerechte Miete, geprüfte Interessenten und persönliche Begleitung in Essen, Münster und der Umgebung.' });
  return (
    <>
      <PageHero eyebrow="Vermietung & Verpachtung" title="Immobilie vermieten in Essen und Münster"
        text="Wir unterstützen Sie bei der Vermietung in Essen, Münster und der Umgebung: von der Mietpreis-Einschätzung über die Suche nach geeigneten Interessenten bis zum Mietvertrag."
        checks={['Marktgerechte Mieteinschätzung', 'Geprüfte Interessenten', 'Persönlicher Ansprechpartner']}
        image={photos.advisorD} alt="Lubka Röger" cutout rating
        buttons={[{ label: 'Vermietung anfragen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      <Rich collapse blocks={[
        { t: 'h2', text: 'Vermietung mit klarem Ablauf' },
        { t: 'p', text: 'Zuerst besprechen wir Objekt, Zielmiete und Ihre Anforderungen an künftige Mieter. Anschließend bereiten wir die Vermarktung vor, koordinieren Besichtigungen und unterstützen Sie bei der Auswahl des geeigneten Mieters.' },
        { t: 'p', text: 'Für die Vermietung brauchen Sie vollständige Unterlagen, etwa Grundrisse, Wohnflächenangaben und einen Energieausweis. Wir helfen Ihnen, alles zusammenzustellen.' },
        { t: 'h2', text: 'Was wir für Vermieter übernehmen' },
        { t: 'ul', items: ['Einschätzung einer marktgerechten Miete', 'Exposé und gezielte Vermarktung', 'Koordination von Anfragen und Besichtigungen', 'Abschluss des Mietvertrags'] },
      ]} />
      <Funnel intent="Vermieten" title="Lassen Sie uns über Ihre Vermietung sprechen" />
      <ServiceGrid exclude="vermietung" title="Weitere Leistungen" eyebrow="Das könnte Sie auch interessieren" />
      <Contact variant="page" />
    </>
  );
}
export const Finanzierung = () => (
  <ServicePage k="leistungen-immobilienfinanzierung" crumb="Finanzierung" metaTitle="Immobilienfinanzierung"
    exclude="finanzierung" eyebrow="Immobilienfinanzierung" funnel={false} tools={['budget', 'finanzierung']} teamStrip={false}
    extra={<FinanceRequest />} />
);
function FinanceRequest() {
  return (
    <section className="wrap" id="anfrage">
      <div className="lead">
        <div>
          <SectionIntro variant="inline" line={false} eyebrow="Finanzierung anfragen" title="Wir prüfen Ihre Finanzierung, kostenfrei und unverbindlich"
            text="Nennen Sie uns kurz Ihr Vorhaben. Wir melden uns mit einer ersten Einschätzung und den nächsten Schritten." />
        </div>
        <div className="lead__box"><ContactForm subject="Finanzierungsanfrage" submitLabel="Finanzierung anfragen" meta={{ form: 'finanzierung', type: 'finanzierung' }} message="Ich interessiere mich für eine Immobilienfinanzierung. Kaufpreis ca.: … / Eigenkapital ca.: …" /></div>
      </div>
    </section>
  );
}

/* ---------- Kauf-Landingpage (Kapitalanlage) ---------- */

function BuyLanding({ k, crumb, metaTitle, eyebrow, filter, search }: { k: string; crumb: string; metaTitle: string; eyebrow: string; filter: (p: import('../../data/properties').Property) => boolean; search: string }) {
  const b = page(k).blocks;
  const h1 = b.find((x) => x.t === 'h1');
  const intro = b.find((x, i) => x.t === 'p' && i > b.indexOf(h1!) );
  usePageMeta({ title: metaTitle, crumbs: crumbs(crumb), footer: 'accordion', description: textOf(intro), jsonLd: [faqLd(homeFaq.slice(0, 4))] });
  return (
    <>
      <PageHero eyebrow={eyebrow} title={textOf(h1)} text={textOf(intro)} image={photos.advisorE} cutout rating
        buttons={[{ label: 'Aktuelle Objekte ansehen', to: search, variant: 'accent' }, { label: 'Budget prüfen', to: ROUTES.budgetrechner, variant: 'outline' }]} />
      <PropertyStrip title="Passende Angebote aus unserer Vermittlung" filter={filter} cta={{ label: 'Alle passenden Objekte', to: search }} />
      <TeaserBand items={[TOOL_TEASERS.budget, TOOL_TEASERS.finanzierung]} />
      <ServiceGrid exclude="kapitalanlage" title="Weitere Leistungen" eyebrow="Alles aus einer Hand" />
      <div className="rich"><div className="rich__text"><FaqBlock title="Häufige Fragen" items={homeFaq.slice(0, 4)} /></div></div>
      <Contact variant="page" />
    </>
  );
}

export const Kapitalanlage = () => (
  <BuyLanding k="leistungen-mehrfamilienhaeuser-kaufen-bochum" crumb="Kapitalanlage" metaTitle="Mehrfamilienhäuser & Kapitalanlagen kaufen" eyebrow="Kapitalanlage"
    filter={(p) => p.mode === 'kaufen' && p.investment} search={`${ROUTES.kaufen}?anlage=1`} />
);

/* ---------- Rückmietverkauf ---------- */

export function Rueckmietverkauf() {
  usePageMeta({ title: 'Rückmietverkauf: verkaufen und wohnen bleiben', crumbs: crumbs('Rückmietverkauf'), footer: 'accordion', description: 'Rückmietverkauf mit Oberholz Immobilien: Immobilie zum Marktwert verkaufen, Kaufpreis erhalten und weiter im eigenen Zuhause wohnen. Persönliche Beratung in Essen, Münster und Umgebung.', image: photos.senioren });
  const checks = page('home').blocks.filter((x) => x.t === 'ul')[5] as { items: string[] };
  return (
    <>
      <PageHero eyebrow="Rückmietverkauf" title="Verkaufen und im eigenen Zuhause wohnen bleiben" image={photos.senioren} alt="Älteres Paar auf der Terrasse seines Hauses" rating
        text="Beim Rückmietverkauf verkaufen Sie Ihre Immobilie zum Marktwert und mieten sie direkt zurück. So erhalten Sie den Kaufpreis und bleiben in Ihrem vertrauten Umfeld wohnen."
        checks={checks.items} buttons={[{ label: 'Beratung anfragen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      <Rich collapse blocks={[
        { t: 'h2', text: 'So funktioniert der Rückmietverkauf' },
        { t: 'h3', text: 'Marktwert ermitteln' }, { t: 'p', text: 'Wir bewerten Ihre Immobilie persönlich vor Ort. Das ist die Grundlage für einen fairen Kaufpreis.' },
        { t: 'h3', text: 'Käufer & Mietvertrag' }, { t: 'p', text: 'Wir suchen einen passenden Käufer und vereinbaren mit ihm einen langfristigen Mietvertrag für Sie.' },
        { t: 'h3', text: 'Notar & Auszahlung' }, { t: 'p', text: 'Nach dem Notartermin erhalten Sie den Kaufpreis und wohnen als Mieter weiter in Ihrem Zuhause.' },
        { t: 'h2', text: 'Für wen eignet sich der Rückmietverkauf?' },
        { t: 'p', text: 'Für Eigentümer, die Kapital aus ihrer Immobilie freisetzen möchten, ohne umzuziehen. Zum Beispiel für den Ruhestand, die Familie oder eine Pflegesituation. Ob die Lösung zu Ihnen passt, klären wir in einem unverbindlichen Gespräch, gern gemeinsam mit Ihren Angehörigen.' },
      ]} />
      <section className="wrap" id="anfrage">
        <div className="lead">
          <SectionIntro variant="inline" line={false} eyebrow="Persönliche Beratung" title="Rückmietverkauf unverbindlich prüfen lassen" text="Wir melden uns persönlich bei Ihnen und besprechen Ihre Situation vertraulich." />
          <div className="lead__box"><ContactForm subject="Anfrage Rückmietverkauf" submitLabel="Beratung anfragen" phoneRequired meta={{ form: 'rueckmietverkauf', type: 'rueckmietverkauf', intent: ['Verkaufen', 'Zurückmieten'] }} message="Ich interessiere mich für einen Rückmietverkauf meiner Immobilie." /></div>
        </div>
      </section>
      <ServiceGrid exclude="rueckmiet" title="Weitere Leistungen" />
      <Contact variant="page" />
    </>
  );
}

/* ---------- Immobilienbewertung ---------- */

const METHODS = [
  { title: 'Vergleichswertverfahren', icon: 'house' as const, text: 'Grundlage sind vergleichbare Verkäufe und geeignete Vergleichsfaktoren, zum Beispiel bei selbstgenutzten Eigentumswohnungen und Einfamilienhäusern.' },
  { title: 'Ertragswertverfahren', icon: 'money' as const, text: 'Bei vermieteten Immobilien stehen die marktüblichen Erträge und die Bewirtschaftungskosten im Mittelpunkt.' },
  { title: 'Sachwertverfahren', icon: 'document' as const, text: 'Bei eigengenutzten Immobilien ergeben der Bodenwert und der Zeitwert des Gebäudes addiert den Sachwert der Immobilie. Dieser wird an die Marktsituation angepasst.' },
];
const valuationFaq = [
  { q: 'Was kostet die erste Immobilienbewertung?', a: 'Die erste Marktwerteinschätzung durch Oberholz Immobilien ist kostenlos und unverbindlich. Falls Sie ein förmliches Gutachten für einen bestimmten Zweck benötigen, klären wir Umfang und mögliche Kosten separat vor einer Beauftragung.' },
  { q: 'Ist eine Online-Schätzung so genau wie eine Bewertung vor Ort?', a: 'Eine Online-Schätzung kann eine erste Orientierung geben. Eine Begehung berücksichtigt zusätzlich den tatsächlichen Zustand, erfolgte Modernisierungen und Besonderheiten der Lage.' },
  { q: 'Welche Unterlagen helfen bei der Wertermittlung?', a: documentsAnswer },
  { q: 'Ist die Marktwerteinschätzung ein Verkehrswertgutachten?', a: 'Unsere Marktwerteinschätzung unterstützt die Preisfindung und die damit verbundene Verkaufsentscheidung. Sie ist kein förmliches Verkehrswertgutachten. Sollten Sie für Gericht, das Finanzamt, Erbauseinandersetzungen oder eine Finanzierung ein Verkehrswertgutachten benötigen, sprechen Sie uns ebenfalls gern an.' },
  { q: 'In welchen Orten bewerten Sie Immobilien?', a: 'Wir unterstützen Eigentümer mit ihren Immobilien in Essen, dem umliegenden Ruhrgebiet, dem Rheinland, dem Bergischen Land sowie Münster und dem Münsterland.' },
];

export function Bewertung() {
  usePageMeta({ title: 'Kostenlose Immobilienbewertung in Essen & Münster', crumbs: crumbs('Immobilienbewertung'), footer: 'accordion', description: 'Was ist Ihr Haus oder Ihre Wohnung wert? Persönliche, kostenlose Marktwerteinschätzung in Essen, Münster und Umgebung. Jetzt Bewertung anfragen.', image: photos.bewertung, jsonLd: [faqLd(valuationFaq)] });
  return <>
    <PageHero eyebrow="Immobilienbewertung" title="Was ist Ihre Immobilie wert?" image={photos.bewertung} alt="Besprechung von Immobilienunterlagen" rating text="Makler und Gutachter bewerten Ihr Haus oder Ihre Wohnung gemeinsam: persönlich vor Ort und nachvollziehbar begründet. Auch wenn Sie noch nicht wissen, ob Sie verkaufen möchten." checks={['Kostenlose erste Marktwerteinschätzung', 'Besichtigung statt Online-Schätzung', 'Für Essen, Münster und Umgebung']} buttons={[{ label: 'Wert ermitteln lassen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
    <Funnel intent="Bewerten" eyebrow="Kostenlose erste Einschätzung" title="Erzählen Sie uns von Ihrer Immobilie" />
    <section className="wrap">
      <SectionIntro variant="inline" line={false} eyebrow="Bewertungsverfahren" title="Die passende Methode für Ihre Immobilie" text="Die Auswahl des Bewertungsverfahrens richtet sich nach der Objektart und der tatsächlichen Nutzung. Je nach Immobilie werden auch mehrere Verfahren herangezogen." />
      <div className="svc-grid svc-grid--3">{METHODS.map(m => <article key={m.title} className="svc"><LineIcon name={m.icon} size={36} /><h3 className="svc__title head">{m.title}</h3><p className="svc__text">{m.text}</p></article>)}</div>
      <p className="owner-method-source">Grundlage: <a className="link-underline" href="https://www.gesetze-im-internet.de/immowertv_2022/__6.html" target="_blank" rel="noopener noreferrer">§ 6 Immobilienwertermittlungsverordnung</a></p>
    </section>
    <OwnerLinks exclude="makler" />
    <div className="rich"><div className="rich__text"><FaqBlock title="Häufige Fragen zur Immobilienbewertung" items={valuationFaq} /></div></div>
    <Contact variant="page" />
  </>;
}

/* ---------- Immotipp ---------- */

export function Immotipp() {
  usePageMeta({ title: 'Immotipp: ab 500 € Tippgeber-Prämie', crumbs: [{ label: 'Immotipp' }], footer: 'accordion', description: 'Sie kennen jemanden, der seine Immobilie verkaufen möchte? Geben Sie Oberholz Immobilien einen Tipp und erhalten Sie mindestens 500 € Prämie. Diskret und unkompliziert.' });
  const b = page('immotipp').blocks;
  return (
    <>
      <PageHero eyebrow="Immotipp" title={textOf(b[0])} text={textOf(b[1])} checks={(b[2] as { items: string[] }).items} image={photos.advisorB} cutout rating
        buttons={[{ label: 'Tipp jetzt abgeben', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      <Rich collapse blocks={[
        { t: 'h2', text: 'So funktioniert das Tippgeber-Programm' },
        { t: 'h3', text: 'Tipp abgeben' }, { t: 'p', text: 'Sie nennen uns per Formular oder Telefon eine Immobilie, deren Eigentümer verkaufen möchte.' },
        { t: 'h3', text: 'Wir übernehmen' }, { t: 'p', text: 'Mit dem Einverständnis der Eigentümer nehmen wir diskret Kontakt auf und begleiten den Verkauf persönlich.' },
        { t: 'h3', text: 'Prämie erhalten' }, { t: 'p', text: 'Kommt durch Ihren Tipp ein Verkauf zustande, erhalten Sie eine Prämie von mindestens 500 €.' },
      ]} />
      <section className="wrap" id="anfrage">
        <div className="lead">
          <SectionIntro variant="inline" line={false} eyebrow="Tippgeber-Formular" title={textOf(b[3])} text={textOf(b[4])} />
          <div className="lead__box">
            <ContactForm subject="Immotipp: Tippgeber-Hinweis" submitLabel="Tipp jetzt absenden" meta={{ form: 'immotipp', type: 'immotipp' }}
              confirm="Die Eigentümer wissen von meinem Tipp und sind damit einverstanden, dass Oberholz Immobilien sie kontaktiert."
              message="Art der Immobilie: … | Ort/PLZ: … | Ansprechpartner & Telefonnummer der Eigentümer (falls bekannt): …"
              benefits={['Kein Aufwand: Das Formular genügt.', 'Gilt für Häuser, Wohnungen und Grundstücke.', 'Diskret & vertraulich.']} />
          </div>
        </div>
      </section>
      <Contact variant="page" />
    </>
  );
}
