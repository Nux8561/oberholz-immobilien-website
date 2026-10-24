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
import Partners from '../../components/Partners/Partners';
import { OwnerGuides, OwnerLinks } from './LocalOwner';
import {
  BTN_CALL, BTN_KONTAKT, PropertyStrip, ServiceGrid, TeaserBand, TOOL_TEASERS, short, splitIntro,
} from './shared';

const crumbs = (label: string) => [{ label }];
const teamOf = (blocks: RichBlock[]) => blocks.filter((b): b is Extract<RichBlock, { t: 'img' }> => b.t === 'img' && / - /.test(b.alt) && /bannerright/.test(b.src)).slice(0, 5);

/* ---------- generische Leistungsseite ---------- */

type ServiceOpts = {
  crumb: string; metaTitle: string; exclude: string; heroImage?: string; eyebrow: string;
  intent?: 'Verkaufen' | 'Vermieten'; funnel?: boolean; extra?: React.ReactNode; tools?: (keyof typeof TOOL_TEASERS)[];
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
      {team.length > 1 && <div className="rich"><div className="rich__wide"><TeamStrip imgs={team} /></div></div>}
      <Rich blocks={body} />
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
  { q: 'Welche Unterlagen brauche ich zum Verkauf?', a: 'Zum Start helfen Grundbuchauszug, Grundrisse, Wohnflächenberechnung und Energieausweis. Bei Eigentumswohnungen kommen Unterlagen der Eigentümergemeinschaft hinzu, bei vermieteten Objekten Mietverträge und Ertragsangaben. Wir klären mit Ihnen, was bereits vorliegt und was noch benötigt wird.' },
  { q: 'Was ist meine Immobilie in Essen oder Bochum wert?', a: 'Entscheidend sind die konkrete Lage, Zustand, Fläche, Nutzung und die aktuelle Nachfrage. Ein städtischer Durchschnittspreis ersetzt keine Objektbewertung. Für Essen und Bochum finden Sie auf unseren lokalen Bewertungsseiten die jeweiligen Besonderheiten und offiziellen Marktquellen.' },
  { q: 'Kann ich auch eine vermietete oder geerbte Immobilie verkaufen?', a: 'Ja. Bestehende Mietverhältnisse und die Eigentumssituation müssen dabei früh berücksichtigt werden. Wir ordnen die nächsten Schritte gemeinsam mit Ihnen ein; bei rechtlichen oder steuerlichen Fragen beziehen Sie bitte Ihr Notariat beziehungsweise Ihre Steuerberatung ein.' },
  { q: 'Wie lange dauert der Verkauf und welche Kosten entstehen?', a: 'Die Dauer hängt unter anderem von Lage, Preis, Zustand, Unterlagen und Finanzierung des Käufers ab. Vermarktungsauftrag, Leistungen und vereinbarte Provision besprechen wir vor Beginn transparent mit Ihnen. Eine feste Verkaufsdauer oder einen bestimmten Erlös können wir nicht seriös zusagen.' },
];

export function Verkaufen() {
  usePageMeta({ title: 'Immobilie verkaufen in Essen, Bochum & Münsterland', description: 'Haus oder Wohnung verkaufen: persönliche Bewertung, vollständige Unterlagen und begleitete Vermarktung mit Oberholz Immobilien in Essen, Bochum und im Münsterland.', crumbs: crumbs('Immobilie verkaufen'), footer: 'accordion', image: photos.advisorA, jsonLd: [faqLd(sellFaq)] });
  return <>
    <PageHero eyebrow="Immobilie verkaufen" title="Ihr Immobilienverkauf. Persönlich begleitet." text="Ob Haus, Eigentumswohnung oder Mehrfamilienhaus: Wir begleiten Ihren Verkauf in Essen, Bochum und im Münsterland – von der ersten Wertermittlung bis zur Schlüsselübergabe." checks={['Ein fester Ansprechpartner', 'Bewertung und Vermarktung aus einer Hand', 'Ein klarer Plan für Ihre Immobilie']} image={photos.advisorA} alt="Michael Oberholz" cutout rating buttons={[{ label: 'Verkauf besprechen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
    <section className="wrap">
      <SectionIntro variant="inline" line={false} eyebrow="Vom ersten Gespräch bis zur Übergabe" title="Drei Schritte. Ein gemeinsames Ziel." />
      <div className="svc-grid svc-grid--3">
        {[['01', 'Wert und Ausgangslage klären', 'Wir sehen uns Ihre Immobilie und die Unterlagen an. Gemeinsam besprechen wir Zeitplan, Zielgruppe und einen nachvollziehbaren Angebotspreis.'], ['02', 'Gezielt an den Markt gehen', 'Wir bereiten Exposé und Präsentation vor, koordinieren Anfragen und Besichtigungen und besprechen die Rückmeldungen mit Ihnen.'], ['03', 'Den Verkauf sicher abschließen', 'Wir begleiten die Verhandlung und die Abstimmung mit dem Notariat. Auch die Vorbereitung der Übergabe gehört zu unserem gemeinsamen Fahrplan.']].map(([n, title, text]) => <article className="svc" key={n}><p className="eyebrow">Schritt {n}</p><h3 className="svc__title head">{title}</h3><p className="svc__text">{text}</p></article>)}
      </div>
    </section>
    <Rich blocks={[{ t: 'h2', text: 'Ihr Objekt bestimmt die Strategie' }, { t: 'p', text: 'Beim Hausverkauf zählen Grundstück, Bausubstanz und energetischer Zustand. Bei der Eigentumswohnung kommen Hausgeld, Rücklagen und Beschlüsse der Eigentümergemeinschaft hinzu. Eine vermietete Immobilie wird zudem anhand ihrer Erträge und Mietverhältnisse eingeordnet.' }, { t: 'p', text: 'Wir erklären Ihnen, welche Faktoren den Preis Ihres Objekts beeinflussen und welche Unterlagen für Kaufinteressenten wichtig sind. So schaffen wir eine belastbare Grundlage für Ihre Entscheidung.' }]} />
    <OwnerLinks exclude="makler" />
    <Funnel intent="Verkaufen" title="Lassen Sie uns über Ihren Verkauf sprechen" />
    <div className="rich"><div className="rich__text"><FaqBlock title="Häufige Fragen zum Immobilienverkauf" items={sellFaq} /></div></div>
    <OwnerGuides />
    <Contact variant="page" />
  </>;
}
export function Vermieten() {
  usePageMeta({ title: 'Immobilie vermieten und verpachten', crumbs: crumbs('Vermietung'), footer: 'accordion', description: 'Vermietung und Verpachtung mit Oberholz Immobilien: marktgerechte Miete, geprüfte Interessenten und persönliche Begleitung in Essen, Münster und der Region.' });
  return (
    <>
      <PageHero eyebrow="Vermietung & Verpachtung" title="Ihre Immobilie vermieten – persönlich begleitet"
        text="Wir unterstützen Sie bei der Vermietung in Essen, Münster und der Region: von der Mietpreis-Einschätzung über die Suche nach geeigneten Interessenten bis zum Mietvertrag."
        checks={['Marktgerechte Mieteinschätzung', 'Geprüfte Interessenten', 'Persönlicher Ansprechpartner']}
        image={photos.advisorD} alt="Lubka Röger" cutout rating
        buttons={[{ label: 'Vermietung anfragen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      <Rich blocks={[
        { t: 'h2', text: 'Vermietung mit klarem Ablauf' },
        { t: 'p', text: 'Zuerst besprechen wir Objekt, Zielmiete und Ihre Anforderungen an künftige Mieter. Anschließend bereiten wir die Vermarktung vor, koordinieren Besichtigungen und unterstützen Sie bei der Auswahl.' },
        { t: 'p', text: 'Für die Vermietung sind vollständige Unterlagen hilfreich – etwa Grundrisse, Wohnflächenangaben und ein vorhandener Energieausweis. Die Ausstellung von Energieausweisen gehört nicht zu unseren Leistungen; wir helfen Ihnen, die erforderlichen Dokumente zusammenzustellen.' },
        { t: 'h2', text: 'Was wir für Vermieter übernehmen' },
        { t: 'ul', items: ['Einschätzung einer marktgerechten Miete', 'Exposé und gezielte Vermarktung', 'Koordination von Anfragen und Besichtigungen', 'Abstimmung der nächsten Schritte bis zum Vertragsabschluss'] },
      ]} />
      <Funnel intent="Vermieten" title="Lassen Sie uns über Ihre Vermietung sprechen" />
      <ServiceGrid exclude="vermietung" title="Weitere Leistungen" eyebrow="Das könnte Sie auch interessieren" />
      <Contact variant="page" />
    </>
  );
}
export const Finanzierung = () => (
  <ServicePage k="leistungen-immobilienfinanzierung" crumb="Finanzierung" metaTitle="Immobilienfinanzierung"
    exclude="finanzierung" eyebrow="Immobilienfinanzierung" funnel={false} tools={['budget', 'finanzierung']}
    extra={<><FinanceRequest /><Partners kinds={['kooperation', 'finanzierung']} /></>} />
);
function FinanceRequest() {
  return (
    <section className="wrap" id="anfrage">
      <div className="lead">
        <div>
          <SectionIntro variant="inline" line={false} eyebrow="Finanzierung anfragen" title="Wir prüfen Ihre Finanzierung – unverbindlich und kostenfrei"
            text="Nennen Sie uns kurz Ihr Vorhaben. Wir melden uns mit einer ersten Einschätzung und den nächsten Schritten." />
        </div>
        <div className="lead__box"><ContactForm subject="Finanzierungsanfrage" submitLabel="Finanzierung anfragen" message="Ich interessiere mich für eine Immobilienfinanzierung. Kaufpreis ca.: … / Eigenkapital ca.: …" /></div>
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
  const fin = page('leistungen-immobilienfinanzierung').blocks;
  const finCols = fin.slice(fin.findIndex((x) => x.t === 'h2'), fin.findIndex((x) => x.t === 'h2' && /Ihre Vorteile/.test(textOf(x))));
  return (
    <>
      <PageHero eyebrow={eyebrow} title={textOf(h1)} text={textOf(intro)} image={photos.advisorE} cutout rating
        buttons={[{ label: 'Aktuelle Objekte ansehen', to: search, variant: 'accent' }, { label: 'Budget prüfen', to: ROUTES.budgetrechner, variant: 'outline' }]} />
      <PropertyStrip title="Passende Angebote aus unserer Vermittlung" filter={filter} cta={{ label: 'Alle passenden Objekte', to: search }} />
      <Rich blocks={[{ t: 'h2', text: 'Kaufen mit Finanzierungssicherheit' }, { t: 'p', text: 'Wir begleiten Sie nicht nur bei der Objektauswahl, sondern auch bei der Finanzierung – mit bankengerechten Unterlagen und unserem Banken-Netzwerk.' }, ...finCols]} />
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
  usePageMeta({ title: 'Rückmietverkauf: verkaufen und wohnen bleiben', crumbs: crumbs('Rückmietverkauf'), footer: 'accordion', description: 'Rückmietverkauf mit Oberholz Immobilien: Immobilie zum Marktwert verkaufen, Kaufpreis erhalten und weiter im eigenen Zuhause wohnen – persönlich beraten in Essen, Münster und Bochum.', image: photos.senioren });
  const checks = page('home').blocks.filter((x) => x.t === 'ul')[5] as { items: string[] };
  return (
    <>
      <PageHero eyebrow="Rückmietverkauf" title="Verkaufen und im eigenen Zuhause wohnen bleiben" image={photos.senioren} alt="Älteres Paar auf der Terrasse seines Hauses" rating
        text="Beim Rückmietverkauf verkaufen Sie Ihre Immobilie zum Marktwert und mieten sie direkt zurück. So erhalten Sie den Kaufpreis und bleiben in Ihrem vertrauten Umfeld."
        checks={checks.items} buttons={[{ label: 'Beratung anfragen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      <Rich blocks={[
        { t: 'h2', text: 'So funktioniert der Rückmietverkauf' },
        { t: 'h3', text: 'Marktwert ermitteln' }, { t: 'p', text: 'Wir bewerten Ihre Immobilie persönlich vor Ort – als Grundlage für einen fairen Kaufpreis.' },
        { t: 'h3', text: 'Käufer & Mietvertrag' }, { t: 'p', text: 'Wir suchen einen passenden Käufer und vereinbaren mit ihm einen langfristigen Mietvertrag für Sie.' },
        { t: 'h3', text: 'Notar & Auszahlung' }, { t: 'p', text: 'Nach dem Notartermin erhalten Sie den Kaufpreis – Sie wohnen als Mieter:in weiter in Ihrem Zuhause.' },
        { t: 'h2', text: 'Für wen eignet sich der Rückmietverkauf?' },
        { t: 'p', text: 'Für Eigentümer:innen, die Kapital aus ihrer Immobilie freisetzen möchten – etwa für den Ruhestand, die Familie oder eine Pflegesituation –, ohne umzuziehen. Ob die Lösung zu Ihnen passt, klären wir in einem unverbindlichen Gespräch, gern gemeinsam mit Ihren Angehörigen.' },
        { t: 'blockquote', text: 'Wir nehmen uns Zeit für Ihre Fragen und zeigen Ihnen auch die Alternativen – vom klassischen Verkauf bis zur Vermietung.' },
      ]} />
      <section className="wrap" id="anfrage">
        <div className="lead">
          <SectionIntro variant="inline" line={false} eyebrow="Persönliche Beratung" title="Rückmietverkauf unverbindlich prüfen lassen" text="Wir melden uns persönlich bei Ihnen und besprechen Ihre Situation vertraulich." />
          <div className="lead__box"><ContactForm subject="Anfrage Rückmietverkauf" submitLabel="Beratung anfragen" phoneRequired message="Ich interessiere mich für einen Rückmietverkauf meiner Immobilie." /></div>
        </div>
      </section>
      <ServiceGrid exclude="rueckmiet" title="Weitere Leistungen" />
      <Contact variant="page" />
    </>
  );
}

/* ---------- Immobilienbewertung ---------- */

const METHODS = [
  { title: 'Vergleichswertverfahren', icon: 'house' as const, text: 'Vergleichbare Verkäufe und geeignete Vergleichsfaktoren bilden die Grundlage – zum Beispiel bei Eigentumswohnungen und vergleichbaren Wohnhäusern.' },
  { title: 'Ertragswertverfahren', icon: 'money' as const, text: 'Bei vermieteten Immobilien stehen die marktüblichen Erträge, die Bewirtschaftungskosten und das Grundstück im Mittelpunkt.' },
  { title: 'Sachwertverfahren', icon: 'document' as const, text: 'Bodenwert und Gebäudesachwert werden zusammen betrachtet und an die Marktsituation angepasst. Das kann etwa bei individuell geprägten Häusern sinnvoll sein.' },
];
const valuationFaq = [
  { q: 'Was kostet die erste Immobilienbewertung?', a: 'Die erste Marktwerteinschätzung durch Oberholz Immobilien ist kostenlos und unverbindlich. Falls Sie ein förmliches Gutachten für einen bestimmten Zweck benötigen, klären wir Umfang und mögliche Kosten separat vor einer Beauftragung.' },
  { q: 'Ist eine Online-Schätzung so genau wie eine Bewertung vor Ort?', a: 'Eine Online-Schätzung kann eine erste Orientierung geben. Eine Besichtigung berücksichtigt zusätzlich den tatsächlichen Zustand, Modernisierungen, Besonderheiten der Lage und die Unterlagen. Dadurch lässt sich die Einschätzung nachvollziehbar auf Ihr Objekt beziehen.' },
  { q: 'Welche Unterlagen helfen bei der Wertermittlung?', a: 'Hilfreich sind Grundrisse, Wohn- und Grundstücksfläche, Baujahr, Modernisierungsangaben, Energieausweis und Grundbuchauszug. Für Wohnungen sind WEG-Unterlagen, für vermietete Objekte die Mietverträge und Ertragsangaben wichtig. Fehlende Unterlagen besprechen wir gemeinsam.' },
  { q: 'Ist die Marktwerteinschätzung ein Verkehrswertgutachten?', a: 'Unsere erste Einschätzung unterstützt die Preisfindung und Verkaufsentscheidung. Sie ist kein förmliches Verkehrswertgutachten. Ob Sie für Gericht, Finanzamt, Erbauseinandersetzung oder Finanzierung ein Gutachten benötigen, hängt vom konkreten Zweck und den Anforderungen des Empfängers ab.' },
  { q: 'In welchen Orten bewerten Sie Immobilien?', a: 'Wir begleiten Eigentümer in Essen, Bochum und im Münsterland. Für Essen und Bochum erläutern unsere lokalen Bewertungsseiten, welche Lage- und Objektmerkmale relevant sind, und verlinken die amtlichen Grundstücksmarktberichte.' },
];

export function Bewertung() {
  usePageMeta({ title: 'Kostenlose Immobilienbewertung in Essen & Bochum', crumbs: crumbs('Immobilienbewertung'), footer: 'accordion', description: 'Was ist Ihr Haus oder Ihre Wohnung wert? Persönliche, kostenlose Marktwerteinschätzung in Essen, Bochum und im Münsterland. Jetzt Bewertung anfragen.', image: photos.bewertung, jsonLd: [faqLd(valuationFaq)] });
  return <>
    <PageHero eyebrow="Immobilienbewertung" title="Der Wert Ihrer Immobilie. Verständlich erklärt." image={photos.bewertung} alt="Besprechung von Immobilienunterlagen" rating text="Sie möchten wissen, was Ihr Haus oder Ihre Wohnung wert ist? Wir betrachten Lage, Zustand und Unterlagen persönlich – als Grundlage für Ihre nächsten Schritte." checks={['Kostenlose erste Marktwerteinschätzung', 'Persönlicher Blick auf Ihr Objekt', 'Für Essen, Bochum und das Münsterland']} buttons={[{ label: 'Bewertung anfragen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
    <section className="wrap">
      <SectionIntro variant="inline" line={false} eyebrow="Bewertungsverfahren" title="Die passende Methode für Ihre Immobilie" text="Die Auswahl richtet sich nach Objektart, Nutzung und verfügbarer Datengrundlage. Je nach Immobilie werden auch mehrere Verfahren herangezogen." />
      <div className="svc-grid svc-grid--3">{METHODS.map(m => <article key={m.title} className="svc"><LineIcon name={m.icon} size={36} /><h3 className="svc__title head">{m.title}</h3><p className="svc__text">{m.text}</p></article>)}</div>
      <p className="owner-method-source">Grundlage: <a className="link-underline" href="https://www.gesetze-im-internet.de/immowertv_2022/__6.html" target="_blank" rel="noopener noreferrer">§ 6 Immobilienwertermittlungsverordnung</a></p>
    </section>
    <OwnerLinks exclude="makler" />
    <Funnel intent="Bewerten" eyebrow="Kostenlose erste Einschätzung" title="Erzählen Sie uns von Ihrer Immobilie" />
    <div className="rich"><div className="rich__text"><FaqBlock title="Häufige Fragen zur Immobilienbewertung" items={valuationFaq} /></div></div>
    <Contact variant="page" />
  </>;
}

/* ---------- Immotipp ---------- */

export function Immotipp() {
  usePageMeta({ title: 'Immotipp: ab 500 € Tippgeber-Prämie', crumbs: [{ label: 'Immotipp' }], footer: 'accordion', description: 'Sie kennen jemanden, der seine Immobilie verkaufen möchte? Geben Sie Oberholz Immobilien einen Tipp und erhalten Sie mindestens 500 € Prämie – diskret und unkompliziert.' });
  const b = page('immotipp').blocks;
  return (
    <>
      <PageHero eyebrow="Immotipp" title={textOf(b[0])} text={textOf(b[1])} checks={(b[2] as { items: string[] }).items} image={photos.advisorB} cutout rating
        buttons={[{ label: 'Tipp jetzt abgeben', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      <Rich blocks={[
        { t: 'h2', text: 'So funktioniert das Tippgeber-Programm' },
        { t: 'h3', text: 'Tipp abgeben' }, { t: 'p', text: 'Sie nennen uns eine Immobilie, deren Eigentümer verkaufen möchte – über das Formular oder telefonisch.' },
        { t: 'h3', text: 'Wir übernehmen' }, { t: 'p', text: 'Wir sprechen die Eigentümer diskret an und begleiten den Verkauf persönlich.' },
        { t: 'h3', text: 'Prämie erhalten' }, { t: 'p', text: 'Kommt durch Ihren Tipp ein Verkauf zustande, erhalten Sie eine Prämie von mindestens 500 €.' },
      ]} />
      <section className="wrap" id="anfrage">
        <div className="lead">
          <SectionIntro variant="inline" line={false} eyebrow="Tippgeber-Formular" title={textOf(b[3])} text={textOf(b[4])} />
          <div className="lead__box">
            <ContactForm subject="Immotipp – Tippgeber-Hinweis" submitLabel="Tipp jetzt absenden"
              message="Art der Immobilie: … | Ort/PLZ: … | Ansprechpartner & Telefonnummer der Eigentümer (falls bekannt): …"
              benefits={['Kein Aufwand – Formular ausfüllen genügt.', 'Gilt für Häuser, Wohnungen und Grundstücke.', 'Diskret & vertraulich.']} />
          </div>
        </div>
      </section>
      <Contact variant="page" />
    </>
  );
}
