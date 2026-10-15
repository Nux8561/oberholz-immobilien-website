import { useState } from 'react';
import ContactForm from '../ContactForm/ContactForm';
import { IconChevronLeft } from '../Icons';
import { eur } from './calc';
import './Calculators.css';

// Überschlägige Modellrechnung: Energieklasse aus Baujahr und Zustand, Werteffekt je gewonnener Klasse
// (Spanne 2,5–4 % des Werts, gedeckelt bei 28 % – größter Preisabstand zwischen den Energieklassen laut Ratgeber),
// Kosten aus typischen Baukosten-Spannen. Keine Immobilienbewertung, kein Angebot.

const HAUSTYPEN = ['Einfamilienhaus', 'Zweifamilienhaus', 'Dreifamilienhaus'];
const BAUJAHRE: [string, number][] = [['vor 1958', 7], ['1958 bis 1978', 6], ['1979 bis 1994', 5], ['1995 bis 2001', 4], ['2002 bis 2015', 3], ['ab 2016', 2]];
const KLASSEN = ['A+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
const HEIZUNG = ['Öl', 'Gas (älter als 20 Jahre)', 'Gas (jünger)', 'Fernwärme / Pellets', 'Wärmepumpe'];
type Tri = 'ja' | 'teilweise' | 'nein';

type S = {
  haustyp: string; baujahr: string; flaeche: number; wert: number; plz: string;
  heizung: string; fassade: Tri; dach: Tri; fenster: 'alt' | 'mittel' | 'neu'; solar: boolean;
  bad: 'modern' | 'alt'; boeden: 'gepflegt' | 'abgenutzt'; elektrik: 'erneuert' | 'alt';
};
type Measure = { title: string; gain: number; cost: [number, number]; valuePct?: [number, number]; funding: string };

function Choice<T extends string>({ label, options, value, onChange }: { label: string; options: readonly T[]; value: T; onChange: (v: T) => void }) {
  return (
    <fieldset className="calc__choice">
      <legend>{label}</legend>
      <div className="funnel__chips">{options.map((o) => <button key={o} type="button" aria-pressed={value === o} className={`chip${value === o ? ' is-active' : ''}`} onClick={() => onChange(o)}>{o}</button>)}</div>
    </fieldset>
  );
}

export default function WertHebel() {
  const [step, setStep] = useState(0);
  const [s, setS] = useState<S>({
    haustyp: 'Einfamilienhaus', baujahr: '1958 bis 1978', flaeche: 140, wert: 400000, plz: '',
    heizung: 'Gas (älter als 20 Jahre)', fassade: 'nein', dach: 'teilweise', fenster: 'mittel', solar: false,
    bad: 'alt', boeden: 'gepflegt', elektrik: 'alt',
  });
  const set = (p: Partial<S>) => setS((x) => ({ ...x, ...p }));

  // Energieklasse heute (Index in KLASSEN)
  let idx = BAUJAHRE.find(([b]) => b === s.baujahr)?.[1] ?? 6;
  idx -= s.fassade === 'ja' ? 1.5 : s.fassade === 'teilweise' ? 0.5 : 0;
  idx -= s.dach === 'ja' ? 1 : s.dach === 'teilweise' ? 0.5 : 0;
  idx -= s.fenster === 'neu' ? 0.5 : 0;
  idx -= s.heizung === 'Wärmepumpe' ? 1.5 : s.heizung === 'Gas (jünger)' || s.heizung === 'Fernwärme / Pellets' ? 0.5 : 0;
  idx -= s.solar ? 0.5 : 0;
  const klasse = Math.max(0, Math.min(8, Math.round(idx)));

  const A = s.flaeche;
  const hull = 'Zuschuss möglich (Bundesförderung, Gebäudehülle)';
  const measures: Measure[] = [
    s.heizung !== 'Wärmepumpe' && { title: 'Heizungstausch auf Wärmepumpe', gain: 1.5, cost: [25000, 40000], funding: 'Zuschuss möglich (Heizungsförderung, Boni für Selbstnutzer)' },
    s.fassade !== 'ja' && { title: 'Fassadendämmung', gain: s.fassade === 'nein' ? 1.5 : 0.75, cost: [A * 1.3 * 130 * (s.fassade === 'nein' ? 1 : 0.5), A * 1.3 * 200 * (s.fassade === 'nein' ? 1 : 0.5)], funding: hull },
    s.dach !== 'ja' && { title: 'Dach / oberste Geschossdecke dämmen', gain: s.dach === 'nein' ? 1 : 0.5, cost: [A * 0.7 * 60, A * 0.7 * 220], funding: hull },
    s.fenster !== 'neu' && { title: 'Fenster mit Wärmeschutzverglasung', gain: s.fenster === 'alt' ? 0.75 : 0.5, cost: [A * 0.18 * 700, A * 0.18 * 1000], funding: hull },
    !s.solar && { title: 'Photovoltaikanlage', gain: 0.5, cost: [12000, 20000], funding: 'Förderkredite möglich' },
    s.bad === 'alt' && { title: 'Badmodernisierung', gain: 0, valuePct: [1, 3], cost: [15000, 30000], funding: 'ggf. Zuschuss für barrierearmen Umbau' },
    s.boeden === 'abgenutzt' && { title: 'Neue Bodenbeläge', gain: 0, valuePct: [0.5, 1.5], cost: [A * 40, A * 80], funding: '–' },
    s.elektrik === 'alt' && { title: 'Elektrik erneuern', gain: 0, valuePct: [0.5, 1.5], cost: [A * 80, A * 120], funding: '–' },
  ].filter(Boolean) as Measure[];

  const effect = (m: Measure): [number, number] => {
    const [lo, hi] = m.valuePct ?? [m.gain * 2.5, m.gain * 4];
    return [s.wert * lo / 100, s.wert * hi / 100];
  };
  const rows = measures.map((m) => ({ m, e: effect(m) })).sort((a, b) => (b.e[1] / b.m.cost[1]) - (a.e[1] / a.m.cost[1]));
  const gainTotal = Math.min(measures.reduce((x, m) => x + m.gain, 0), klasse - 1);
  const capped = (n: number) => Math.min(n, s.wert * 0.28);
  const sumLo = capped(rows.reduce((x, r) => x + r.e[0], 0));
  const sumHi = capped(rows.reduce((x, r) => x + r.e[1], 0));

  const steps = ['Ihre Immobilie', 'Energie und Technik', 'Innenausstattung'];
  return (
    <div className="wizard">
      <div className="funnel__progress" aria-hidden="true"><span style={{ width: `${(Math.min(step + 1, 3) / 3) * 100}%` }} /></div>
      {step < 3 ? (
        <form className="wizard__step wizard__step--left" onSubmit={(e) => { e.preventDefault(); setStep(step + 1); }}>
          <p className="funnel__count">Schritt {step + 1} von 3</p>
          <h3 className="wizard__q head">{steps[step]}</h3>
          {step === 0 && (
            <>
              <Choice label="Haustyp" options={HAUSTYPEN} value={s.haustyp} onChange={(v) => set({ haustyp: v })} />
              <Choice label="Baujahr" options={BAUJAHRE.map(([b]) => b)} value={s.baujahr} onChange={(v) => set({ baujahr: v })} />
              <label className="calc__field"><span>Wohnfläche: {s.flaeche} m²</span>
                <input type="range" min={60} max={400} step={5} value={s.flaeche} onChange={(e) => set({ flaeche: Number(e.target.value) })} className="funnel__range" /></label>
              <div className="calc__row">
                <label className="calc__field"><span>Ihr vermuteter Wert (€)</span><input inputMode="numeric" value={s.wert.toLocaleString('de-DE')} onChange={(e) => set({ wert: Number(e.target.value.replace(/\D/g, '')) || 0 })} /><small>Ihre ehrliche Schätzung genügt.</small></label>
                <label className="calc__field"><span>Postleitzahl</span><input inputMode="numeric" maxLength={5} value={s.plz} onChange={(e) => set({ plz: e.target.value.replace(/\D/g, '') })} /></label>
              </div>
            </>
          )}
          {step === 1 && (
            <>
              <Choice label="Heizung" options={HEIZUNG} value={s.heizung} onChange={(v) => set({ heizung: v })} />
              <Choice label="Fassade gedämmt?" options={['ja', 'teilweise', 'nein'] as const} value={s.fassade} onChange={(v) => set({ fassade: v })} />
              <Choice label="Dach / oberste Geschossdecke gedämmt?" options={['ja', 'teilweise', 'nein'] as const} value={s.dach} onChange={(v) => set({ dach: v })} />
              <Choice label="Fenster" options={['alt', 'mittel', 'neu'] as const} value={s.fenster} onChange={(v) => set({ fenster: v })} />
              <Choice label="Photovoltaik vorhanden?" options={['ja', 'nein'] as const} value={s.solar ? 'ja' : 'nein'} onChange={(v) => set({ solar: v === 'ja' })} />
            </>
          )}
          {step === 2 && (
            <>
              <Choice label="Badezimmer" options={['modern', 'alt'] as const} value={s.bad} onChange={(v) => set({ bad: v })} />
              <Choice label="Bodenbeläge" options={['gepflegt', 'abgenutzt'] as const} value={s.boeden} onChange={(v) => set({ boeden: v })} />
              <Choice label="Elektrik" options={['erneuert', 'alt'] as const} value={s.elektrik} onChange={(v) => set({ elektrik: v })} />
            </>
          )}
          <div className="wizard__nav">
            {step > 0 && <button type="button" className="link-underline funnel__back" onClick={() => setStep(step - 1)}><IconChevronLeft size={16} />Zurück</button>}
            <button type="submit" className="btn">{step === 2 ? 'Ergebnis anzeigen' : 'Weiter'}</button>
          </div>
        </form>
      ) : (
        <div className="wizard__result wizard__step--left" aria-live="polite">
          <div className="wizard__kpis">
            <div><p className="eyebrow">Geschätzte Energieklasse heute</p><p className="calc__big head">{KLASSEN[klasse]}</p></div>
            <div><p className="eyebrow">Möglicher Werteffekt gesamt</p><p className="calc__big head">{eur(sumLo)} – {eur(sumHi)}</p></div>
          </div>
          {gainTotal > 0 && <p className="wizard__hint">Mit allen energetischen Maßnahmen wäre etwa Klasse {KLASSEN[Math.max(0, Math.round(klasse - gainTotal))]} erreichbar.</p>}
          {rows.length === 0 ? <p className="wizard__hint">Ihre Immobilie ist bereits gut aufgestellt – große Wert-Hebel sind nicht erkennbar.</p> : (
            <div className="rich__table-wrap">
              <table className="rich__table calc__table">
                <thead><tr><th>Maßnahme</th><th>Kosten (ca.)</th><th>Werteffekt (ca.)</th><th>Förderung</th></tr></thead>
                <tbody>{rows.map(({ m, e }) => <tr key={m.title}><td>{m.title}</td><td>{eur(m.cost[0])} – {eur(m.cost[1])}</td><td>{eur(e[0])} – {eur(e[1])}</td><td>{m.funding}</td></tr>)}</tbody>
              </table>
            </div>
          )}
          <p className="calc__note">Überschlägige Modellrechnung, keine Immobilienbewertung und kein Angebot. Tatsächliche Effekte hängen stark von Region, Objekt und Ausführung ab. Förderhöhen prüfen wir im persönlichen Gespräch nach aktueller Richtlinie.</p>
          <div className="wizard__nav"><button type="button" className="btn btn--outline" onClick={() => setStep(0)}>↺ Neu berechnen</button></div>
          <div className="wizard__lead">
            <h3 className="head">Ergebnis prüfen lassen: Ihre ehrliche Ersteinschätzung</h3>
            <p className="wizard__hint">Welche Maßnahme sich bei Ihrem Haus wirklich rechnet und welche Förderung Sie konkret bekommen, prüfen wir gern persönlich.</p>
            <ContactForm subject="Wert-Hebel-Rechner: Ersteinschätzung" submitLabel="Ersteinschätzung anfragen"
              extra={[['Haustyp', s.haustyp], ['Baujahr', s.baujahr], ['Wohnfläche', `${s.flaeche} m²`], ['Vermuteter Wert', eur(s.wert)], ['PLZ', s.plz], ['Heizung', s.heizung],
                ['Fassade gedämmt', s.fassade], ['Dach gedämmt', s.dach], ['Fenster', s.fenster], ['Energieklasse (geschätzt)', KLASSEN[klasse]], ['Werteffekt (geschätzt)', `${eur(sumLo)} – ${eur(sumHi)}`]]} />
          </div>
        </div>
      )}
    </div>
  );
}
