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
import {
  BTN_BEWERTUNG, BTN_CALL, BTN_KONTAKT, PropertyStrip, ServiceGrid, TeaserBand, TOOL_TEASERS, short, splitIntro, valuationMethods,
} from './shared';

const crumbs = (label: string) => [{ label: 'Leistungen', to: ROUTES.leistungen }, { label }];
const teamOf = (blocks: RichBlock[]) => blocks.filter((b): b is Extract<RichBlock, { t: 'img' }> => b.t === 'img' && / - /.test(b.alt) && /bannerright/.test(b.src)).slice(0, 5);
const compareTable = page('home').blocks.filter((b) => b.t === 'h2' || b.t === 'p' || b.t === 'table').slice(0, 3);
const howWeSell = (() => { const b = page('home').blocks; const i = b.findIndex((x) => x.t === 'h2' && /So verkaufen wir/.test(x.text)); return b.slice(i, i + 9); })();

/* ---------- Übersicht ---------- */

export function Leistungen() {
  usePageMeta({ title: 'Leistungen: Verkauf, Vermietung, Bewertung', crumbs: [{ label: 'Leistungen' }], footer: 'accordion', description: textOf(page('leistungen').blocks[1]), jsonLd: [faqLd(homeFaq)] });
  const b = page('leistungen').blocks;
  return (
    <>
      <PageHero eyebrow="Leistungen" title={textOf(b[0])} text={textOf(b[1])} image={photos.advisorG} alt="Michael Oberholz" cutout rating
        buttons={[BTN_BEWERTUNG, BTN_KONTAKT]} />
      <ServiceGrid title="Persönlich vor Ort – von der Bewertung bis zur Schlüsselübergabe" />
      <Rich blocks={[{ t: 'blockquote', text: textOf(b[2]) }, ...compareTable, ...howWeSell]} />
      <Funnel />
      <TeaserBand items={[TOOL_TEASERS.budget, TOOL_TEASERS.finanzierung, TOOL_TEASERS.wertHebel]} />
      <div className="rich"><div className="rich__text"><FaqBlock title="Häufige Fragen zu unseren Leistungen" items={homeFaq} /></div></div>
      <Contact variant="page" />
    </>
  );
}

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

export const Verkaufen = () => (
  <ServicePage k="leistungen-immobilienverkauf" crumb="Immobilie verkaufen" metaTitle="Immobilie verkaufen in Münster, Essen und Bochum"
    exclude="verkauf" eyebrow="Immobilie verkaufen" intent="Verkaufen" tools={['wertHebel', 'immotipp']} extra={<Partners kinds={['portale']} />} />
);
export const Vermieten = () => (
  <ServicePage k="leistungen-vermietung-und-verpachtung" crumb="Vermietung" metaTitle="Immobilie vermieten und verpachten"
    exclude="vermietung" eyebrow="Vermietung & Verpachtung" intent="Vermieten" heroImage={photos.advisorD} />
);
export const Finanzierung = () => (
  <ServicePage k="leistungen-immobilienfinanzierung" crumb="Finanzierung" metaTitle="Immobilienfinanzierung mit Energiekompetenz"
    exclude="finanzierung" eyebrow="Immobilienfinanzierung" funnel={false} tools={['budget', 'finanzierung']}
    extra={<><FinanceRequest /><Partners kinds={['kooperation', 'finanzierung']} /></>} />
);
export const Vermarktung = () => (
  <ServicePage k="leistungen-immobilienvermarktung" crumb="Vermarktung" metaTitle="Immobilienvermarktung mit eigener Werbeagentur"
    exclude="vermarktung" eyebrow="Immobilienvermarktung" intent="Verkaufen" heroImage={photos.advisorF} extra={<Partners kinds={['portale']} />} />
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

/* ---------- Kauf-Landingpages (Kapitalanlage, Wohnung kaufen) ---------- */

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
export const WohnungKaufen = () => (
  <BuyLanding k="leistungen-wohnungen-kaufen-bochum" crumb="Wohnung kaufen" metaTitle="Wohnungen kaufen in Bochum und Umgebung" eyebrow="Wohnung kaufen"
    filter={(p) => p.mode === 'kaufen' && p.type === 'Wohnung'} search={`${ROUTES.kaufen}?typ=Wohnung`} />
);

/* ---------- Rückmietverkauf ---------- */

export function Rueckmietverkauf() {
  usePageMeta({ title: 'Rückmietverkauf: verkaufen und wohnen bleiben', crumbs: crumbs('Rückmietverkauf'), footer: 'accordion', description: 'Rückmietverkauf mit Oberholz Immobilien: Immobilie zum Marktwert verkaufen, Kaufpreis erhalten und weiter im eigenen Zuhause wohnen – persönlich beraten in Münster, Essen und Bochum.', image: photos.senioren });
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

const METHODS: Record<string, string> = {
  Bodenwert: 'Wert des Grundstücks ohne Bebauung – ermittelt aus Bodenrichtwerten und Lagemerkmalen.',
  Ertragswert: 'Für vermietete Objekte: Wert aus den nachhaltig erzielbaren Mieterträgen.',
  Sachwert: 'Für selbst genutzte Häuser: Wert aus Bodenwert und Herstellungswert der Gebäude abzüglich Alterung.',
};

export function Bewertung() {
  usePageMeta({ title: 'Kostenlose Immobilienbewertung', crumbs: crumbs('Immobilienbewertung'), footer: 'accordion', description: 'Was ist Ihre Immobilie wert? Kostenlose, persönliche Immobilienbewertung vor Ort in Münster, Essen, Bochum und Umgebung – nachvollziehbar und unverbindlich.', image: photos.bewertung, jsonLd: [faqLd(homeFaq)] });
  const lists = page('home').blocks.filter((x) => x.t === 'ul') as { items: string[] }[];
  const mw = page('kontakt-immobilienmakler-bochum').blocks;
  const mwText = textOf(mw[mw.findIndex((x) => x.t === 'h2' && textOf(x) === 'Marktwertermittlung') + 1]);
  return (
    <>
      <PageHero eyebrow="Immobilienbewertung" title="Was ist Ihre Immobilie wert? Kostenlose Bewertung vor Ort" image={photos.bewertung} alt="Immobilienbewertung vor Ort" rating
        text="Wir ermitteln den Marktwert Ihrer Immobilie persönlich und nachvollziehbar – als Grundlage für Verkauf, Vermietung, Erbe oder Finanzierung."
        checks={lists[2].items.slice(0, 3)} buttons={[{ label: 'Bewertung anfragen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      <Funnel eyebrow="Kostenlose Immobilienbewertung" title="In vier Schritten zur Bewertung" />
      <section className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow="Bewertungsverfahren" title="Drei Verfahren – ein belastbarer Marktwert" />
        <div className="svc-grid svc-grid--3">
          {valuationMethods.map((m) => (
            <div key={m} className="svc"><LineIcon name={m === 'Bodenwert' ? 'sun' : m === 'Ertragswert' ? 'money' : 'house'} size={40} /><h3 className="svc__title head">{m}</h3><p className="svc__text">{METHODS[m]}</p></div>
          ))}
        </div>
      </section>
      <Rich blocks={[{ t: 'h2', text: 'Marktwertermittlung durch unser Team' }, { t: 'p', text: mwText }, ...compareTable, ...howWeSell]} />
      <TeaserBand items={[TOOL_TEASERS.wertHebel, TOOL_TEASERS.immotipp]} />
      <div className="rich"><div className="rich__text"><FaqBlock title="Häufige Fragen zur Bewertung" items={homeFaq} /></div></div>
      <Contact variant="page" />
    </>
  );
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
