import { useState } from 'react';
import { Link } from 'react-router-dom';
import { brand } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { mailtoHref } from '../../lib/mail';
import { IconCheck, IconMail } from '../Icons';
import './ContactForm.css';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
type Key = 'vorname' | 'nachname' | 'email' | 'telefon' | 'dsgvo';
type Errors = Partial<Record<Key, string>>;

type Props = {
  /** Betreff der vorbereiteten E-Mail */
  subject: string;
  message?: string;
  submitLabel?: string;
  /** zusätzliche Angaben aus vorgeschalteten Schritten (Funnel, Rechner, Tippgeber) */
  extra?: [string, string | undefined | false][];
  phoneRequired?: boolean;
  benefits?: string[] | false;
  doneText?: string;
};

/** Anfrageformular: Validierung im Browser, danach Versand über das E-Mail-Programm (mailto) – kein Server. */
export default function ContactForm({
  subject, message = '', submitLabel = 'Details anfragen', extra = [], phoneRequired = false,
  benefits = ['Persönliche Rückmeldung durch unser Team.', 'Unverbindlich und kostenfrei.', 'Ihre Daten nutzen wir nur für diese Anfrage.'],
  doneText,
}: Props) {
  const [v, setV] = useState({ vorname: '', nachname: '', email: '', telefon: '', nachricht: message });
  const [dsgvo, setDsgvo] = useState(false);
  const [errors, setErrors] = useState<Errors>({});
  const [sent, setSent] = useState(false);

  const set = (k: keyof typeof v) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setV({ ...v, [k]: e.target.value });
    if (errors[k as Key]) setErrors({ ...errors, [k]: undefined });
  };
  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const err: Errors = {};
    if (!v.vorname.trim()) err.vorname = 'Bitte geben Sie Ihren Vornamen ein.';
    if (!v.nachname.trim()) err.nachname = 'Bitte geben Sie Ihren Nachnamen ein.';
    if (!EMAIL_RE.test(v.email.trim())) err.email = 'Bitte geben Sie eine gültige E-Mail-Adresse ein.';
    if (phoneRequired && v.telefon.replace(/\D/g, '').length < 6) err.telefon = 'Bitte geben Sie eine Telefonnummer für Rückfragen an.';
    if (!dsgvo) err.dsgvo = 'Bitte bestätigen Sie die Datenschutzhinweise.';
    setErrors(err);
    if (Object.keys(err).length === 0) setSent(true);
  };

  if (sent) {
    const href = mailtoHref(subject, [
      ...extra,
      ['Name', `${v.vorname} ${v.nachname}`], ['E-Mail', v.email], ['Telefon', v.telefon], ['Nachricht', v.nachricht],
    ]);
    return (
      <div className="cform__done" role="status">
        <IconCheck size={32} />
        <p className="head">Fast geschafft, {v.vorname}!</p>
        <p>{doneText ?? 'Ihre Anfrage ist vorbereitet. Senden Sie sie mit einem Klick über Ihr E-Mail-Programm – oder rufen Sie uns direkt an.'}</p>
        <div className="cform__done-btns">
          <a href={href} className="btn btn--accent btn--icon"><IconMail />Anfrage per E-Mail senden</a>
          <a href={brand.phoneHref} className="btn btn--outline">{brand.phoneDisplay}</a>
        </div>
        <button type="button" className="link-underline cform__edit" onClick={() => setSent(false)}>Angaben bearbeiten</button>
      </div>
    );
  }

  const field = (k: 'vorname' | 'nachname' | 'email' | 'telefon', label: string, type = 'text', required = true) => (
    <label className={`cform__field${errors[k] ? ' has-error' : ''}`}>
      <span className="cform__label">{required ? '*' : ''}{label}</span>
      <input type={type} value={v[k]} onChange={set(k)} autoComplete={k === 'email' ? 'email' : k === 'telefon' ? 'tel' : k === 'vorname' ? 'given-name' : 'family-name'}
        aria-invalid={!!errors[k]} />
      {errors[k] && <span className="cform__error" role="alert">{errors[k]}</span>}
    </label>
  );

  return (
    <form className="cform" onSubmit={submit} noValidate>
      <div className="cform__grid">
        {field('vorname', 'Vorname')}
        {field('nachname', 'Nachname')}
        {field('email', 'E-Mail', 'email')}
        {field('telefon', 'Telefon', 'tel', phoneRequired)}
      </div>
      <label className="cform__field cform__field--full">
        <span className="cform__label">Ihre Nachricht</span>
        <textarea rows={3} value={v.nachricht} onChange={set('nachricht')} />
      </label>
      <div className={`cform__consent${errors.dsgvo ? ' has-error' : ''}`}>
        <input id={`dsgvo-${subject.length}`} type="checkbox" checked={dsgvo} onChange={() => { setDsgvo(!dsgvo); setErrors({ ...errors, dsgvo: undefined }); }} />
        <label htmlFor={`dsgvo-${subject.length}`} className="is-open">
          *Ich bin damit einverstanden, dass {brand.company} meine Angaben zur Bearbeitung dieser Anfrage verwendet und mich telefonisch oder per E-Mail kontaktiert.
          Details in der <Link to={ROUTES.datenschutz} className="link-underline">Datenschutzerklärung</Link>.
        </label>
        {errors.dsgvo && <span className="cform__error" role="alert">{errors.dsgvo}</span>}
      </div>
      <div className="cform__submit"><button type="submit" className="btn btn--accent btn--icon"><IconMail />{submitLabel}</button></div>
      {benefits && (
        <ul className="cform__benefits">
          {benefits.map((b) => <li key={b}><span className="cform__tick"><IconCheck size={14} /></span>{b}</li>)}
        </ul>
      )}
    </form>
  );
}
