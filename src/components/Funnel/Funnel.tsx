import { useState } from 'react';
import { LineIcon, type LineIconName } from '../../blocks/LineIcons';
import ContactForm from '../ContactForm/ContactForm';
import { IconCheck, IconChevronLeft } from '../Icons';
import './Funnel.css';

// Ablauf wie das Anfrageformular der bisherigen Website (#iwf): Objektart → Details → Absicht → Kontakt.
const ARTEN: { label: string; icon: LineIconName }[] = [
  { label: 'Wohnhaus', icon: 'house' }, { label: 'Wohnung', icon: 'apartment' }, { label: 'Gewerbe', icon: 'multi' },
  { label: 'Grundstück', icon: 'sun' }, { label: 'Sonstiges', icon: 'key' },
];
const WOHNARTEN = ['Einfamilienhaus', 'Reihenhaus', 'Doppelhaus / Hälfte', 'Mehrfamilienhaus', 'Wohn- & Geschäftshaus'];
const GEWERBEARTEN = ['Produktion', 'Lager / Logistik', 'Büro / Praxis', 'Handel', 'Sonstiges'];
const ABSICHTEN = ['Verkaufen', 'Vermieten'];
const ERREICHBAR = ['Vormittags', 'Mittags', 'Nachmittags', 'Abends'];

type State = { art?: string; wohnart?: string; wohnungen: number; wohnflaeche: number; grundstueck: number; gewerbeart?: string; absicht: string[]; ort: string; erreichbar: string[] };

export default function Funnel({ eyebrow = 'Immobilien-Vermittlung', title = 'Verkaufen oder vermieten?', intent }: { eyebrow?: string; title?: string; intent?: 'Verkaufen' | 'Vermieten' }) {
  const [step, setStep] = useState(0);
  const [s, setS] = useState<State>({ wohnungen: 3, wohnflaeche: 90, grundstueck: 500, absicht: intent ? [intent] : [], ort: '', erreichbar: [] });
  const set = (patch: Partial<State>) => setS((x) => ({ ...x, ...patch }));
  const toggle = (k: 'absicht' | 'erreichbar', v: string) => set({ [k]: s[k].includes(v) ? s[k].filter((x) => x !== v) : [...s[k], v] } as Partial<State>);
  const total = 4;
  const next = () => setStep((n) => Math.min(n + 1, total - 1));
  const needsUnits = s.wohnart === 'Mehrfamilienhaus' || s.wohnart === 'Wohn- & Geschäftshaus';

  const detail = s.art === 'Wohnhaus' ? `${s.wohnart ?? ''}${needsUnits ? `, ${s.wohnungen} Einheiten` : ''}`
    : s.art === 'Wohnung' ? `ca. ${s.wohnflaeche} m² Wohnfläche`
      : s.art === 'Grundstück' ? `ca. ${s.grundstueck} m² Grundstück`
        : s.art === 'Gewerbe' ? s.gewerbeart ?? '' : '';

  const pickArt = (art: string) => { set({ art }); setStep(art === 'Sonstiges' ? 2 : 1); };

  return (
    <section className="funnel" id="anfrage" aria-labelledby="funnel-title">
      <div className="funnel__box">
        <p className="eyebrow funnel__eyebrow">{eyebrow}</p>
        <h2 className="funnel__title head" id="funnel-title">{title}</h2>
        <div className="funnel__progress" aria-hidden="true"><span style={{ width: `${((step + 1) / total) * 100}%` }} /></div>
        <p className="funnel__count">Schritt {step + 1} von {total}</p>

        {step === 0 && (
          <fieldset className="funnel__step">
            <legend className="funnel__q">Welche Art von Immobilie möchten Sie verkaufen oder vermieten?</legend>
            <div className="funnel__tiles">
              {ARTEN.map((a) => (
                <button key={a.label} type="button" className={`funnel__tile${s.art === a.label ? ' is-active' : ''}`} onClick={() => pickArt(a.label)}>
                  <LineIcon name={a.icon} size={40} /><span>{a.label}</span>
                </button>
              ))}
            </div>
          </fieldset>
        )}

        {step === 1 && s.art === 'Wohnhaus' && (
          <fieldset className="funnel__step">
            <legend className="funnel__q">Um welche Art von Wohnhaus handelt es sich?</legend>
            <div className="funnel__chips">
              {WOHNARTEN.map((w) => (
                <button key={w} type="button" className={`chip${s.wohnart === w ? ' is-active' : ''}`}
                  onClick={() => { set({ wohnart: w }); if (w !== 'Mehrfamilienhaus' && w !== 'Wohn- & Geschäftshaus') next(); }}>{w}</button>
              ))}
            </div>
            {needsUnits && (
              <div className="funnel__units">
                <p className="funnel__label">Anzahl der Wohneinheiten</p>
                <div className="funnel__stepper">
                  <button type="button" aria-label="Weniger" onClick={() => set({ wohnungen: Math.max(2, s.wohnungen - 1) })}>−</button>
                  <output aria-live="polite">{s.wohnungen}</output>
                  <button type="button" aria-label="Mehr" onClick={() => set({ wohnungen: s.wohnungen + 1 })}>+</button>
                </div>
                <div className="funnel__chips">{[2, 3, 4, 6, 10].map((n) => <button key={n} type="button" className={`chip${s.wohnungen === n ? ' is-active' : ''}`} onClick={() => set({ wohnungen: n })}>{n}{n === 10 ? '+' : ''}</button>)}</div>
                <button type="button" className="btn funnel__next" onClick={next}>Weiter</button>
              </div>
            )}
          </fieldset>
        )}

        {step === 1 && (s.art === 'Wohnung' || s.art === 'Grundstück') && (() => {
          const flat = s.art === 'Wohnung';
          const val = flat ? s.wohnflaeche : s.grundstueck;
          const [min, max, st] = flat ? [20, 300, 5] : [100, 3000, 50];
          const quick = flat ? [60, 90, 120, 160] : [200, 500, 800, 1200];
          return (
            <fieldset className="funnel__step">
              <legend className="funnel__q">{flat ? 'Wie groß ist die Wohnfläche?' : 'Wie groß ist das Grundstück?'}</legend>
              <p className="funnel__value head">ca. {val.toLocaleString('de-DE')} m²</p>
              <input className="funnel__range" type="range" min={min} max={max} step={st} value={val} aria-label={flat ? 'Wohnfläche in m²' : 'Grundstücksfläche in m²'}
                onChange={(e) => set(flat ? { wohnflaeche: Number(e.target.value) } : { grundstueck: Number(e.target.value) })} />
              <div className="funnel__chips">{quick.map((q) => <button key={q} type="button" className={`chip${val === q ? ' is-active' : ''}`} onClick={() => set(flat ? { wohnflaeche: q } : { grundstueck: q })}>{q} m²</button>)}</div>
              <button type="button" className="btn funnel__next" onClick={next}>Weiter</button>
            </fieldset>
          );
        })()}

        {step === 1 && s.art === 'Gewerbe' && (
          <fieldset className="funnel__step">
            <legend className="funnel__q">Welche Art von Gewerbeimmobilie?</legend>
            <div className="funnel__chips">
              {GEWERBEARTEN.map((g) => <button key={g} type="button" className={`chip${s.gewerbeart === g ? ' is-active' : ''}`} onClick={() => { set({ gewerbeart: g }); next(); }}>{g}</button>)}
            </div>
          </fieldset>
        )}

        {step === 2 && (
          <fieldset className="funnel__step">
            <legend className="funnel__q">Was haben Sie vor?</legend>
            <div className="funnel__tiles funnel__tiles--2">
              {ABSICHTEN.map((a) => (
                <button key={a} type="button" role="checkbox" aria-checked={s.absicht.includes(a)} className={`funnel__tile${s.absicht.includes(a) ? ' is-active' : ''}`} onClick={() => toggle('absicht', a)}>
                  <LineIcon name={a === 'Verkaufen' ? 'handshake' : 'key'} size={40} /><span>{a}</span>
                  {s.absicht.includes(a) && <span className="funnel__tick"><IconCheck size={14} /></span>}
                </button>
              ))}
            </div>
            <p className="funnel__hint">Mehrfachauswahl möglich – wir beraten Sie gern zu beiden Wegen.</p>
            <button type="button" className="btn funnel__next" disabled={!s.absicht.length} onClick={next}>Weiter</button>
          </fieldset>
        )}

        {step === 3 && (
          <div className="funnel__step">
            <p className="funnel__q">Wie erreichen wir Sie?</p>
            <p className="funnel__summary">{[s.art, detail, s.absicht.join(' & ')].filter(Boolean).join(' · ')}</p>
            <label className="cform__field funnel__ort">
              <span className="cform__label">PLZ, Ort der Immobilie</span>
              <input value={s.ort} onChange={(e) => set({ ort: e.target.value })} placeholder="z. B. 48147 Münster" autoComplete="postal-code" />
            </label>
            <p className="funnel__label">Am besten erreichbar</p>
            <div className="funnel__chips">{ERREICHBAR.map((e) => <button key={e} type="button" aria-pressed={s.erreichbar.includes(e)} className={`chip${s.erreichbar.includes(e) ? ' is-active' : ''}`} onClick={() => toggle('erreichbar', e)}>{e}</button>)}</div>
            <ContactForm subject={`Anfrage ${s.absicht.join('/') || 'Vermittlung'}: ${s.art ?? 'Immobilie'}`} submitLabel="Anfrage absenden" phoneRequired
              extra={[['Objektart', s.art], ['Details', detail], ['Vorhaben', s.absicht.join(', ')], ['PLZ/Ort', s.ort], ['Erreichbar', s.erreichbar.join(', ')]]}
              benefits={['Kostenlose und unverbindliche Erstberatung.', 'Persönlicher Ansprechpartner vor Ort.', 'Diskret und vertraulich.']} />
          </div>
        )}

        {step > 0 && (
          <button type="button" className="funnel__back link-underline" onClick={() => setStep(step === 2 && s.art === 'Sonstiges' ? 0 : step - 1)}>
            <IconChevronLeft size={16} />Zurück
          </button>
        )}
      </div>
    </section>
  );
}
