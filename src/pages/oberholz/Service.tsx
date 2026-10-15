// Service-Bereich: Übersicht und Rechner (Inhalte der bisherigen Website + funktionierende Rechner).
import { page, textOf } from '../../data/oberholz';
import { photos } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { usePageMeta } from '../../layout/PageMeta';
import PageHero from '../../components/PageHero/PageHero';
import Rich from '../../components/Rich/Rich';
import Contact from '../../components/Contact/Contact';
import SectionIntro from '../../components/SectionIntro/SectionIntro';
import FinanceCalculator from '../../components/Calculators/FinanceCalculator';
import BudgetCalculator from '../../components/Calculators/BudgetCalculator';
import WertHebel from '../../components/Calculators/WertHebel';
import { BTN_CALL, TeaserBand, TOOL_TEASERS } from './shared';
import Partners from '../../components/Partners/Partners';

const crumbs = (label?: string) => (label ? [{ label: 'Service', to: ROUTES.service }, { label }] : [{ label: 'Service' }]);

export function Service() {
  usePageMeta({ title: 'Service: Rechner & Werkzeuge', crumbs: crumbs(), footer: 'accordion', description: 'Kostenlose Immobilien-Rechner von Oberholz Immobilien: Budgetrechner, Finanzierungsrechner mit Grunderwerbsteuer und Wert-Hebel-Rechner für Modernisierungen.' });
  const b = page('service').blocks;
  return (
    <>
      <PageHero eyebrow="Service" title={textOf(b[0])} text={textOf(b[1])} image={photos.advisorE} cutout
        buttons={[{ label: 'Budget prüfen', to: ROUTES.budgetrechner, variant: 'accent' }, { label: 'Rate berechnen', to: ROUTES.finanzierungsrechner, variant: 'outline' }]} />
      <TeaserBand items={[TOOL_TEASERS.budget, TOOL_TEASERS.finanzierung, TOOL_TEASERS.wertHebel]} />
      <TeaserBand items={[
        { eyebrow: 'Immopedia', title: 'Fachbegriffe von A bis Z', text: 'Rund 2.000 Begriffe rund um Immobilien, Finanzierung und Energie – verständlich erklärt.', to: ROUTES.immopedia, cta: 'Begriff nachschlagen' },
        { eyebrow: 'Dokumente & Downloads', title: 'Formulare, Verträge, Merkblätter', text: 'Erfassungsbogen, Maklerauftrag, Merkblätter zum Energieausweis und mehr als PDF.', to: ROUTES.downloads, cta: 'Zu den Downloads' },
        { eyebrow: 'Ratgeber', title: 'Wissen für Eigentümer', text: 'Fundierte Beiträge zu Verkauf, Erbe, Sanierung und Finanzierung – mit Leitfäden.', to: ROUTES.ratgeber, cta: 'Zum Ratgeber' },
      ]} />
      <Rich blocks={b.slice(2, 4)} />
      <Contact variant="page" />
    </>
  );
}

export function Budgetrechner() {
  const b = page('service-kann-ich-kaufen').blocks;
  usePageMeta({ title: 'Budgetrechner: Kann ich mir eine Immobilie leisten?', crumbs: crumbs('Budgetrechner'), footer: 'accordion', description: textOf(b[1]) });
  const resultsAt = b.findIndex((x) => x.t === 'h2' && /Welche Ergebnisse/.test(textOf(x)));
  return (
    <>
      <PageHero eyebrow="Der ehrliche Budget-Check" title={textOf(b[0])} text={textOf(b[1])} checks={(b[2] as { items: string[] }).items} image={photos.advisorD} cutout
        buttons={[{ label: 'Jetzt berechnen', to: '#rechner', variant: 'accent' }, BTN_CALL]} />
      <section className="wrap" id="rechner">
        <SectionIntro variant="inline" line={false} center eyebrow="Budgetrechner" title={textOf(b[9])} text={textOf(b[10])} />
        <BudgetCalculator />
      </section>
      <Rich blocks={[...b.slice(4, 9), ...b.slice(resultsAt)]} />
      <TeaserBand items={[TOOL_TEASERS.finanzierung, TOOL_TEASERS.wertHebel]} />
      <Contact variant="page" />
    </>
  );
}

export function Finanzierungsrechner() {
  const b = page('service-finanzierungsrechner').blocks;
  usePageMeta({ title: 'Immobilienfinanzierungsrechner: Nebenkosten, Rate & Restschuld', crumbs: crumbs('Finanzierungsrechner'), footer: 'accordion', description: textOf(b[1]) });
  return (
    <>
      <PageHero eyebrow="Finanzierungsrechner" title={textOf(b[0])} text={textOf(b[1])} image={photos.advisorB} cutout rating
        buttons={[{ label: 'Jetzt berechnen', to: '#rechner', variant: 'accent' }, BTN_CALL]} />
      <section className="wrap" id="rechner">
        <SectionIntro variant="inline" line={false} center eyebrow="Rechner" title={textOf(b[3])} text={textOf(b[4])} />
        <FinanceCalculator />
      </section>
      <Partners kinds={['finanzierung']} />
      <Rich blocks={b.slice(6)} />
      <TeaserBand items={[TOOL_TEASERS.budget, TOOL_TEASERS.wertHebel]} />
      <Contact variant="page" />
    </>
  );
}

export function WertHebelRechner() {
  const b = page('service-wert-hebel-rechner').blocks;
  usePageMeta({ title: 'Wert-Hebel-Rechner: Was bringt welche Modernisierung?', crumbs: crumbs('Wert-Hebel-Rechner'), footer: 'accordion', description: textOf(b[1]) });
  return (
    <>
      <PageHero eyebrow="Überschlagsrechner für Eigentümer" title={textOf(b[0])} text={textOf(b[1])} image="/assets/ratgeber/energieausweis-beim-verkauf.jpg" alt="Wärmepumpe an einem modernisierten Einfamilienhaus"
        buttons={[{ label: 'Jetzt starten', to: '#rechner', variant: 'accent' }, BTN_CALL]} />
      <section className="wrap" id="rechner"><WertHebel /></section>
      <TeaserBand items={[TOOL_TEASERS.budget, TOOL_TEASERS.finanzierung]} />
      <Contact variant="page" />
    </>
  );
}
