import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { brand, team, whatsappUrl } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { mailtoHref } from '../../lib/mail';
import { openRatings } from '../RatingPanel/RatingPanel';
import Stars from '../Stars/Stars';
import { IconClose } from '../Icons';
import './ContactWidget.css';

// Kontakt-Widget wie auf der bisherigen Website: runder Button mit Foto + Hinweis „Kostenlose Erstberatung“,
// Panel mit Anfrage, Anrufen, Rückruf, WhatsApp und Kontaktdaten. Auf dem Handy zusätzlich eine Kontaktleiste unten.

const TOPICS = ['Immobilie verkaufen', 'Immobilie vermieten', 'Immobilienbewertung', 'Rückmietverkauf', 'Kaufberatung', 'Kapitalanlage / Mehrfamilienhaus', 'Finanzierung', 'Bestandskunde', 'Kooperationsanfrage', 'Sonstiges'];
type Tab = 'anfrage' | 'anrufen' | 'rueckruf' | 'whatsapp' | 'kontakt';
const TABS: [Tab, string][] = [['anfrage', 'Anfrage'], ['anrufen', 'Anrufen'], ['rueckruf', 'Rückruf'], ['whatsapp', 'WhatsApp'], ['kontakt', 'Kontakt']];

const EVT = 'oh-contact-open';
export const openContact = (tab: Tab = 'anfrage') => window.dispatchEvent(new CustomEvent(EVT, { detail: tab }));

const IconPhone = () => (<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true"><path d="M7.5 3.5h-3a1 1 0 0 0-1 1C3.5 13 11 20.5 19.5 20.5a1 1 0 0 0 1-1v-3l-4-1.5-2 2c-2.5-1-5-3.5-6-6l2-2Z" /></svg>);
const IconWa = () => (<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2a9.8 9.8 0 0 0-8.4 14.8L2.3 21.8l4.9-1.3A9.8 9.8 0 1 0 12 2.2Zm0 17.8a8 8 0 0 1-4.1-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1 1 12 20Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8.9c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.7-1.7c-.2-.4-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3c-.2.3-.9.9-.9 2.2s.9 2.5 1.1 2.7c.1.2 1.8 2.8 4.4 3.9 1.7.7 2.3.8 3.2.7.5-.1 1.4-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.4-.3Z" /></svg>);

export default function ContactWidget() {
  const [open, setOpen] = useState(false);
  const [tab, setTab] = useState<Tab>('anfrage');
  const [visible, setVisible] = useState(false);
  const [hint, setHint] = useState(() => { try { return sessionStorage.getItem('oh-hint') !== '0'; } catch { return true; } });
  const [f, setF] = useState({ name: '', email: '', tel: '', topic: '', msg: '', zeit: 'Vormittags' });
  const [err, setErr] = useState<Record<string, string>>({});
  const [done, setDone] = useState<string | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  const face = team[0].face;

  useEffect(() => {
    // erscheint nach dem ersten Scrollen, verschwindet am Seitenende (Footer-Links bleiben frei)
    const onScroll = () => setVisible(window.scrollY > 300 && window.innerHeight + window.scrollY < document.documentElement.scrollHeight - 160);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    const onOpen = (e: Event) => { setTab((e as CustomEvent<Tab>).detail ?? 'anfrage'); setOpen(true); };
    window.addEventListener(EVT, onOpen);
    return () => { window.removeEventListener('scroll', onScroll); window.removeEventListener(EVT, onOpen); };
  }, []);
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('keydown', onKey);
    ref.current?.querySelector<HTMLElement>('.cw__tabs button[aria-selected="true"]')?.focus();
    return () => document.removeEventListener('keydown', onKey);
  }, [open]);

  const closeHint = (e: React.MouseEvent) => { e.stopPropagation(); setHint(false); try { sessionStorage.setItem('oh-hint', '0'); } catch { /* */ } };
  const set = (k: keyof typeof f) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => { setF({ ...f, [k]: e.target.value }); setErr({ ...err, [k]: '' }); };

  const submit = (kind: 'anfrage' | 'rueckruf') => (e: React.FormEvent) => {
    e.preventDefault();
    const er: Record<string, string> = {};
    if (!f.name.trim()) er.name = 'Bitte geben Sie Ihren Namen an.';
    if (!f.topic) er.topic = 'Bitte wählen Sie Ihr Anliegen.';
    if (kind === 'rueckruf' && f.tel.replace(/\D/g, '').length < 6) er.tel = 'Bitte geben Sie Ihre Telefonnummer an.';
    if (kind === 'anfrage' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.email.trim()) && f.tel.replace(/\D/g, '').length < 6) er.email = 'Bitte E-Mail-Adresse oder Telefonnummer angeben.';
    setErr(er);
    if (Object.keys(er).length) return;
    const href = mailtoHref(kind === 'rueckruf' ? `Rückrufbitte: ${f.topic}` : `Anfrage: ${f.topic}`, [
      ['Name', f.name], ['E-Mail', f.email], ['Telefon', f.tel], ['Anliegen', f.topic],
      ['Rückruf gewünscht', kind === 'rueckruf' && f.zeit], ['Nachricht', f.msg], ['Seite', window.location.href],
    ]);
    setDone(href);
  };

  const field = (k: 'name' | 'email' | 'tel', label: string, type = 'text', required = false) => (
    <label className={`cw__field${err[k] ? ' has-error' : ''}`}>
      <span>{label}{required ? ' *' : ''}</span>
      <input type={type} value={f[k]} onChange={set(k)} autoComplete={k === 'name' ? 'name' : k === 'email' ? 'email' : 'tel'} />
      {err[k] && <small role="alert">{err[k]}</small>}
    </label>
  );
  const topicSelect = (
    <label className={`cw__field${err.topic ? ' has-error' : ''}`}>
      <span>Ihr Anliegen *</span>
      <select value={f.topic} onChange={set('topic')}><option value="">Bitte wählen …</option>{TOPICS.map((t) => <option key={t}>{t}</option>)}</select>
      {err.topic && <small role="alert">{err.topic}</small>}
    </label>
  );

  return (
    <>
      {/* runder Button mit Hinweis */}
      <div className={`cw-trigger${visible && !open ? ' is-visible' : ''}`}>
        {hint && (
          <button type="button" className="cw-trigger__hint" onClick={() => openContact('anfrage')}>
            Kostenlose Erstberatung
            <span role="button" tabIndex={0} aria-label="Hinweis schließen" className="cw-trigger__x" onClick={closeHint} onKeyDown={(e) => { if (e.key === 'Enter') closeHint(e as unknown as React.MouseEvent); }}>×</span>
          </button>
        )}
        <button type="button" className="cw-trigger__btn" aria-label="Kontakt öffnen" onClick={() => openContact('anfrage')}>
          <img src={face} alt="" />
          <span className="cw-trigger__dot" aria-hidden="true" />
        </button>
      </div>

      {/* Kontaktleiste unten (Handy) */}
      <nav className="cw-bar" aria-label="Schnellkontakt">
        <a href={brand.phoneHref}><IconPhone /><span>Anrufen</span></a>
        <a href={whatsappUrl()} target="_blank" rel="noopener noreferrer"><IconWa /><span>WhatsApp</span></a>
        <button type="button" onClick={() => openContact('anfrage')}><img src={face} alt="" /><span>Beratung</span></button>
      </nav>

      <div className={`cw${open ? ' is-open' : ''}`} aria-hidden={!open}>
        <button type="button" className="cw__backdrop" tabIndex={-1} aria-label="Schließen" onClick={() => setOpen(false)} />
        <div className="cw__panel" role="dialog" aria-modal="true" aria-labelledby="cw-title" ref={ref}>
          <div className="cw__head">
            <img src={face} alt="Michael Oberholz" />
            <div>
              <p className="cw__title head" id="cw-title">Ihr Team von {brand.name}</p>
              <p className="cw__sub">Kostenlose Erstberatung · <a href={brand.phoneHref}>{brand.phoneDisplay}</a></p>
              <button type="button" className="cw__rating rating-trigger" onClick={() => { setOpen(false); openRatings(); }}><Stars value={brand.rating} /> <strong>{brand.rating.toFixed(1).replace('.', ',')}/5</strong> ({brand.reviews} Google-Bewertungen)</button>
            </div>
            <button type="button" className="cw__close" aria-label="Schließen" onClick={() => setOpen(false)}><IconClose /></button>
          </div>
          <ul className="cw__usp"><li>Unverbindlich</li><li>Makler nach § 34c GewO</li><li>Regional: Münster · Essen · Bochum</li></ul>
          <div className="cw__tabs" role="tablist">
            {TABS.map(([k, l]) => <button key={k} type="button" role="tab" aria-selected={tab === k} className={tab === k ? 'is-active' : ''} onClick={() => { setTab(k); setDone(null); }}>{l}</button>)}
          </div>

          <div className="cw__body" role="tabpanel">
            {done ? (
              <div className="cw__done">
                <p className="head">Fast geschafft!</p>
                <p>Ihre Nachricht ist vorbereitet. Senden Sie sie mit einem Klick über Ihr E-Mail-Programm – wir melden uns schnellstmöglich.</p>
                <a className="btn btn--accent" href={done}>Per E-Mail senden</a>
                <a className="btn cw__submit cw__wa" href={whatsappUrl(`Hallo, ich bin ${f.name}. Mein Anliegen: ${f.topic}. ${f.msg}`.trim())} target="_blank" rel="noopener noreferrer"><IconWa /> Lieber per WhatsApp</a>
                <button type="button" className="link-underline" onClick={() => setDone(null)}>Angaben bearbeiten</button>
              </div>
            ) : tab === 'anfrage' ? (
              <form onSubmit={submit('anfrage')} noValidate>
                <p className="cw__lead">Unverbindliche Anfrage</p>
                {field('name', 'Vor- und Nachname', 'text', true)}
                {field('email', 'E-Mail-Adresse', 'email')}
                {field('tel', 'Telefonnummer', 'tel')}
                {topicSelect}
                <label className="cw__field"><span>Nachricht (optional)</span><textarea rows={3} value={f.msg} onChange={set('msg')} /></label>
                <button type="submit" className="btn btn--accent cw__submit">Jetzt kostenlos anfragen</button>
                <p className="cw__legal">Ihre Daten werden nur zur Bearbeitung Ihrer Anfrage genutzt. <Link to={ROUTES.datenschutz} onClick={() => setOpen(false)}>Datenschutz</Link></p>
              </form>
            ) : tab === 'anrufen' ? (
              <div className="cw__call">
                <p className="cw__lead">Rufen Sie uns an – unverbindlich und kostenlos</p>
                <a className="btn btn--accent cw__submit" href={brand.phoneHref}><IconPhone /> {brand.phoneDisplay}</a>
                <p className="cw__hours">{brand.hours}</p>
              </div>
            ) : tab === 'rueckruf' ? (
              <form onSubmit={submit('rueckruf')} noValidate>
                <p className="cw__lead">Kostenlosen Rückruf anfordern</p>
                {field('name', 'Ihr Name', 'text', true)}
                {topicSelect}
                {field('tel', 'Telefonnummer', 'tel', true)}
                <div className="cw__field"><span>Gewünschter Zeitraum</span>
                  <div className="cw__chips">{['Vormittags', 'Mittags', 'Nachmittags', 'Abends'].map((z) => <button key={z} type="button" aria-pressed={f.zeit === z} className={f.zeit === z ? 'is-active' : ''} onClick={() => setF({ ...f, zeit: z })}>{z}</button>)}</div>
                </div>
                <button type="submit" className="btn btn--accent cw__submit">Rückruf anfordern</button>
              </form>
            ) : tab === 'whatsapp' ? (
              <form onSubmit={(e) => { e.preventDefault(); window.open(whatsappUrl(`${f.msg || 'Hallo Oberholz Immobilien, ich habe eine Frage.'}${f.name ? `\n\n– ${f.name}` : ''}`), '_blank', 'noopener'); }}>
                <p className="cw__lead">WhatsApp-Chat</p>
                <p className="cw__hours">Wir antworten in der Regel innerhalb weniger Stunden ({brand.hours}).</p>
                {field('name', 'Ihr Name (optional)')}
                <label className="cw__field"><span>Ihre Nachricht</span><textarea rows={3} value={f.msg} onChange={set('msg')} placeholder="z. B. Ich möchte meine Wohnung in Münster bewerten lassen." /></label>
                <button type="submit" className="btn cw__submit cw__wa"><IconWa /> Auf WhatsApp öffnen</button>
                <p className="cw__legal">Beim Öffnen von WhatsApp gelten die Datenschutzbestimmungen von WhatsApp. <Link to={ROUTES.datenschutz} onClick={() => setOpen(false)}>Mehr erfahren</Link></p>
              </form>
            ) : (
              <div className="cw__contact">
                <p className="cw__lead">Kontaktdaten</p>
                <dl>
                  <div><dt>Telefon</dt><dd><a href={brand.phoneHref}>{brand.phoneDisplay}</a></dd></div>
                  <div><dt>WhatsApp</dt><dd><a href={whatsappUrl()} target="_blank" rel="noopener noreferrer">{brand.phoneDisplay}</a></dd></div>
                  <div><dt>E-Mail</dt><dd><a href={`mailto:${brand.email}`}>{brand.email}</a></dd></div>
                  <div><dt>Adresse</dt><dd>{brand.street}, {brand.city.replace(', Deutschland', '')}</dd></div>
                  <div><dt>Öffnungszeiten</dt><dd className="cw__pre">{brand.hours.replace(', ', '\n')}</dd></div>
                </dl>
                <a className="link-underline" href={brand.googleUrl} target="_blank" rel="noopener noreferrer">Route in Google Maps</a>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
