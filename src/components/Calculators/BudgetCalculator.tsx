import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../data/routes';
import { DEFAULT_LAND, GREST, annuity, balanceAfter, eur, pct, payoffYears } from './calc';
import { IconChevronLeft } from '../Icons';
import './Calculators.css';

const ZINS = 3.6;     // Annahme 10 Jahre Zinsbindung
const TILGUNG = 2;
const QUOTE = 0.35;   // Faustregel: Rate ≤ 35 % des Haushaltsnettoeinkommens
const NOTAR = 2;
const MAKLER = 3.57;

type V = { preis: number; land: string; makler: boolean; ek: number; einkommen: number; miete: number; kredit: number; kreditMonate: number; alter: number };

const STEPS = [
  { q: 'Welche Immobilie schwebt Ihnen vor?', hint: 'Nennen Sie den ungefähren Kaufpreis. Kein Objekt in Sicht? Nehmen Sie einen Wunschwert.' },
  { q: 'In welchem Bundesland kaufen Sie?', hint: 'Die Grunderwerbsteuer ist von Land zu Land verschieden. Notar & Grundbuch (ca. 2 %) rechnen wir automatisch ein.' },
  { q: 'Wie viel Eigenkapital bringen Sie mit?', hint: 'Ersparnisse, Bausparguthaben, Wertpapiere, Schenkungen – alles, was Sie einbringen können.' },
  { q: 'Ihr monatliches Haushaltsnettoeinkommen', hint: 'Gehälter, feste Nebeneinkünfte, Mieteinnahmen, Kindergeld – inklusive Partner:in.' },
  { q: 'Was zahlen Sie aktuell an Kaltmiete?', hint: 'Ihre heutige Miete fällt beim Kauf weg. Wohnen Sie mietfrei, tragen Sie 0 ein.' },
  { q: 'Haben Sie laufende Kredite oder Raten?', hint: 'Bald endende Verpflichtungen bewerten wir milder. Keine Kredite? Einfach 0 lassen.' },
  { q: 'Wie alt sind Sie?', hint: 'Bei mehreren Käufern nehmen Sie die ältere Person – das ist die vorsichtigere Annahme.' },
];

function Money({ value, onChange, label }: { value: number; onChange: (n: number) => void; label: string }) {
  return (
    <label className="calc__money">
      <span className="sr-only">{label}</span>
      <input inputMode="numeric" value={value ? value.toLocaleString('de-DE') : ''} placeholder="0"
        onChange={(e) => onChange(Number(e.target.value.replace(/\D/g, '')) || 0)} />
      <span aria-hidden="true">€</span>
    </label>
  );
}

/** Budgetrechner „Kann ich kaufen?“ – 7 Schritte wie auf der bisherigen Website, Auswertung nach Bank-Faustregeln. */
export default function BudgetCalculator() {
  const [step, setStep] = useState(0);
  const [v, setV] = useState<V>({ preis: 350000, land: DEFAULT_LAND, makler: true, ek: 60000, einkommen: 4200, miete: 950, kredit: 0, kreditMonate: 0, alter: 38 });
  const set = (p: Partial<V>) => setV((x) => ({ ...x, ...p }));
  const done = step >= STEPS.length;

  const grest = GREST.find(([l]) => l === v.land)?.[1] ?? 6.5;
  const nkRate = (grest + NOTAR + (v.makler ? MAKLER : 0)) / 100;
  const nk = v.preis * nkRate;
  const loan = Math.max(0, v.preis + nk - v.ek);
  const rate = annuity(loan, ZINS, TILGUNG);
  const kreditLast = v.kredit * (v.kreditMonate > 0 && v.kreditMonate <= 12 ? 0.5 : 1);
  const tragbar = Math.max(0, v.einkommen * QUOTE - kreditLast);
  const maxLoan = (tragbar * 12 * 100) / (ZINS + TILGUNG);
  const maxPreis = (maxLoan + v.ek) / (1 + nkRate);
  const quote = v.einkommen ? (rate + kreditLast) / v.einkommen : 1;
  const verdict = quote <= 0.3 ? { k: 'good', t: 'Gut tragbar', d: 'Ihre Rate bleibt deutlich unter der kritischen Grenze. Gute Ausgangslage für das Bankgespräch.' }
    : quote <= 0.4 ? { k: 'ok', t: 'Grundsätzlich machbar', d: 'Die Rate liegt im üblichen Rahmen. Mehr Eigenkapital oder Fördermittel verschaffen zusätzlichen Spielraum.' }
      : { k: 'warn', t: 'Aktuell ambitioniert', d: 'Die Rate belastet Ihr Einkommen stark. Ein niedrigerer Kaufpreis, mehr Eigenkapital oder eine längere Planung helfen.' };
  const rest10 = balanceAfter(loan, ZINS, rate, 120);
  const years = payoffYears(loan, ZINS, rate);
  const rentenAlter = 67;
  const tooLong = Number.isFinite(years) && v.alter + years > rentenAlter;

  const field = () => {
    switch (step) {
      case 0: return <Money label="Kaufpreis" value={v.preis} onChange={(n) => set({ preis: n })} />;
      case 1: return (
        <>
          <select className="calc__select" value={v.land} onChange={(e) => set({ land: e.target.value })} aria-label="Bundesland">
            {GREST.map(([l, p]) => <option key={l} value={l}>{l} – Grunderwerbsteuer {pct(p, 1)}</option>)}
          </select>
          <label className="calc__check"><input type="checkbox" checked={v.makler} onChange={(e) => set({ makler: e.target.checked })} />Kauf über Makler (Käuferprovision {pct(MAKLER)})</label>
        </>
      );
      case 2: return <Money label="Eigenkapital" value={v.ek} onChange={(n) => set({ ek: n })} />;
      case 3: return <Money label="Haushaltsnettoeinkommen pro Monat" value={v.einkommen} onChange={(n) => set({ einkommen: n })} />;
      case 4: return <Money label="Kaltmiete pro Monat" value={v.miete} onChange={(n) => set({ miete: n })} />;
      case 5: return (
        <div className="calc__row">
          <label className="calc__field"><span>Monatliche Raten (€)</span><input inputMode="numeric" value={v.kredit || ''} placeholder="0" onChange={(e) => set({ kredit: Number(e.target.value.replace(/\D/g, '')) || 0 })} /></label>
          <label className="calc__field"><span>Restlaufzeit (Monate)</span><input inputMode="numeric" value={v.kreditMonate || ''} placeholder="0" onChange={(e) => set({ kreditMonate: Number(e.target.value.replace(/\D/g, '')) || 0 })} /></label>
        </div>
      );
      case 6: return (
        <label className="calc__money"><span className="sr-only">Alter</span>
          <input inputMode="numeric" value={v.alter || ''} onChange={(e) => set({ alter: Number(e.target.value.replace(/\D/g, '')) || 0 })} /><span aria-hidden="true">Jahre</span>
        </label>
      );
      default: return null;
    }
  };

  return (
    <div className="wizard">
      <div className="funnel__progress" aria-hidden="true"><span style={{ width: `${(Math.min(step + 1, STEPS.length) / STEPS.length) * 100}%` }} /></div>
      {!done ? (
        <form className="wizard__step" onSubmit={(e) => { e.preventDefault(); setStep(step + 1); }}>
          <p className="funnel__count">Schritt {step + 1} von {STEPS.length}</p>
          <h3 className="wizard__q head">{STEPS[step].q}</h3>
          <p className="wizard__hint">{STEPS[step].hint}</p>
          {field()}
          <div className="wizard__nav">
            {step > 0 && <button type="button" className="link-underline funnel__back" onClick={() => setStep(step - 1)}><IconChevronLeft size={16} />Zurück</button>}
            <button type="submit" className="btn">{step === STEPS.length - 1 ? 'Ergebnis anzeigen' : 'Weiter'}</button>
          </div>
          <p className="wizard__privacy">100 % kostenlos & anonym · Ihre Angaben verlassen Ihren Browser nicht</p>
        </form>
      ) : (
        <div className="wizard__result" aria-live="polite">
          <p className={`wizard__verdict wizard__verdict--${verdict.k}`}>{verdict.t}</p>
          <p className="wizard__hint">{verdict.d}</p>
          <div className="wizard__kpis">
            <div><p className="eyebrow">Realistischer Kaufpreisrahmen</p><p className="calc__big head">bis {eur(Math.max(0, maxPreis))}</p></div>
            <div><p className="eyebrow">Monatsrate für {eur(v.preis)}</p><p className="calc__big head">{eur(rate)}</p></div>
          </div>
          <dl className="calc__dl">
            <div><dt>Kaufnebenkosten ({pct(nkRate * 100, 2)})</dt><dd>{eur(nk)}</dd></div>
            <div><dt>Benötigtes Darlehen</dt><dd>{eur(loan)}</dd></div>
            <div><dt>Tragbare Rate (35 % abzgl. Kredite)</dt><dd>{eur(tragbar)}</dd></div>
            <div><dt>Rate im Vergleich zur heutigen Miete</dt><dd>{rate >= v.miete ? '+' : '−'}{eur(Math.abs(rate - v.miete))}</dd></div>
            <div><dt>Restschuld nach 10 Jahren</dt><dd>{eur(rest10)}</dd></div>
            <div><dt>Annahmen</dt><dd>{pct(ZINS)} Zins, {pct(TILGUNG, 0)} Tilgung</dd></div>
          </dl>
          {v.ek < nk && <p className="wizard__tip">Ihr Eigenkapital deckt die Kaufnebenkosten noch nicht vollständig – Banken verlangen dafür meist einen Zinsaufschlag.</p>}
          {tooLong && <p className="wizard__tip">Bei {pct(TILGUNG, 0)} Tilgung wäre das Darlehen erst mit etwa {Math.round(v.alter + years)} Jahren getilgt. Eine höhere Tilgung sorgt für Schuldenfreiheit bis zum Ruhestand.</p>}
          <div className="wizard__nav">
            <button type="button" className="btn btn--outline" onClick={() => setStep(0)}>↺ Neu berechnen</button>
            <Link to={`${ROUTES.finanzierung}#anfrage`} className="btn btn--accent">Einschätzung bestätigen lassen</Link>
          </div>
          <p className="calc__note">Orientierung auf Basis marktüblicher Annahmen – keine Finanzierungszusage.</p>
        </div>
      )}
    </div>
  );
}
