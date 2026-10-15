import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../data/routes';
import { DEFAULT_LAND, GREST, annuity, balanceAfter, estimateZins, eur, pct, payoffYears } from './calc';
import './Calculators.css';

const num = (s: string) => Number(s.replace(/\./g, '').replace(',', '.')) || 0;

/** Immobilienfinanzierungsrechner: Nebenkosten, Darlehen, Rate und Restschuld (Felder wie auf der bisherigen Website). */
export default function FinanceCalculator() {
  const [land, setLand] = useState(DEFAULT_LAND);
  const [eltern, setEltern] = useState(false);
  const [preis, setPreis] = useState('350000');
  const [ek, setEk] = useState('70000');
  const [makler, setMakler] = useState('3,57');
  const [notar, setNotar] = useState('2,0');
  const [bindung, setBindung] = useState(10);
  const [auto, setAuto] = useState(true);
  const [zinsManual, setZinsManual] = useState('3,6');
  const [tilgung, setTilgung] = useState('2,0');

  const r = useMemo(() => {
    const kp = num(preis); const eigen = num(ek);
    const grest = eltern ? 0 : GREST.find(([l]) => l === land)?.[1] ?? 6.5;
    const nkMakler = kp * num(makler) / 100; const nkNotar = kp * num(notar) / 100; const nkSteuer = kp * grest / 100;
    const nk = nkMakler + nkNotar + nkSteuer;
    const loan = Math.max(0, kp + nk - eigen);
    const ltv = kp ? loan / kp : 0;
    const zins = auto ? estimateZins(bindung, ltv) : num(zinsManual);
    const rate = annuity(loan, zins, num(tilgung));
    const rest = balanceAfter(loan, zins, rate, bindung * 12);
    const years = payoffYears(loan, zins, rate);
    return { kp, grest, nkMakler, nkNotar, nkSteuer, nk, loan, ltv, zins, rate, rest, years, paidInterest: rate * bindung * 12 - (loan - rest) };
  }, [land, eltern, preis, ek, makler, notar, bindung, auto, zinsManual, tilgung]);

  return (
    <div className="calc">
      <form className="calc__form" onSubmit={(e) => e.preventDefault()} aria-label="Finanzierungsrechner">
        <label className="calc__field"><span>Bundesland</span>
          <select value={land} onChange={(e) => setLand(e.target.value)}>{GREST.map(([l, p]) => <option key={l} value={l}>{l} ({pct(p, 1)})</option>)}</select>
        </label>
        <label className="calc__check"><input type="checkbox" checked={eltern} onChange={(e) => setEltern(e.target.checked)} />Kauf von Eltern/Großeltern (GrESt befreit)</label>
        <div className="calc__row">
          <label className="calc__field"><span>Kaufpreis (€)</span><input inputMode="numeric" value={preis} onChange={(e) => setPreis(e.target.value)} /></label>
          <label className="calc__field"><span>Eigenkapital (€)</span><input inputMode="numeric" value={ek} onChange={(e) => setEk(e.target.value)} /></label>
        </div>
        <div className="calc__row">
          <label className="calc__field"><span>Maklerprovision (%)</span><input inputMode="decimal" value={makler} onChange={(e) => setMakler(e.target.value)} /></label>
          <label className="calc__field"><span>Notar & Grundbuch (%)</span><input inputMode="decimal" value={notar} onChange={(e) => setNotar(e.target.value)} /></label>
        </div>
        <div className="calc__row">
          <label className="calc__field"><span>Zinsbindung</span>
            <select value={bindung} onChange={(e) => setBindung(Number(e.target.value))}>{[5, 10, 15, 20, 25, 30].map((j) => <option key={j} value={j}>{j} Jahre</option>)}</select>
          </label>
          <label className="calc__field"><span>Anfängliche Tilgung (%)</span><input inputMode="decimal" value={tilgung} onChange={(e) => setTilgung(e.target.value)} /></label>
        </div>
        <label className="calc__check"><input type="checkbox" checked={auto} onChange={(e) => setAuto(e.target.checked)} />Sollzins automatisch ermitteln (aus Beleihungsauslauf und Zinsbindung)</label>
        {!auto && <label className="calc__field"><span>Sollzins (%)</span><input inputMode="decimal" value={zinsManual} onChange={(e) => setZinsManual(e.target.value)} /></label>}
      </form>

      <div className="calc__result" aria-live="polite">
        <p className="eyebrow">Ihre Monatsrate</p>
        <p className="calc__big head">{eur(r.rate)}</p>
        <p className="calc__sub">bei {pct(r.zins)} Sollzins{auto ? ' (Annahme)' : ''} und {tilgung} % Tilgung</p>
        <dl className="calc__dl">
          <div><dt>Maklerprovision</dt><dd>{eur(r.nkMakler)}</dd></div>
          <div><dt>Notar & Grundbuch</dt><dd>{eur(r.nkNotar)}</dd></div>
          <div><dt>Grunderwerbsteuer ({pct(r.grest, 1)})</dt><dd>{eur(r.nkSteuer)}</dd></div>
          <div className="is-sum"><dt>Nebenkosten gesamt</dt><dd>{eur(r.nk)}</dd></div>
          <div className="is-sum"><dt>Nettodarlehen</dt><dd>{eur(r.loan)}</dd></div>
          <div><dt>Beleihungsauslauf (LTV)</dt><dd>{pct(r.ltv * 100, 1)}</dd></div>
          <div><dt>Restschuld nach {bindung} Jahren</dt><dd>{eur(r.rest)}</dd></div>
          <div><dt>Zinsen in der Zinsbindung</dt><dd>{eur(r.paidInterest)}</dd></div>
          <div><dt>Volltilgung nach ca.</dt><dd>{Number.isFinite(r.years) ? `${Math.ceil(r.years)} Jahren` : '–'}</dd></div>
        </dl>
        <p className="calc__note">Modellrechnung ohne Gewähr. Der automatisch ermittelte Sollzins ist eine Annahme und ersetzt kein Bankangebot.</p>
        <Link to={`${ROUTES.finanzierung}#anfrage`} className="btn btn--accent">Finanzierung anfragen</Link>
      </div>
    </div>
  );
}
