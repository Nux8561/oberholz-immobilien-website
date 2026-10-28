import { useId, useState } from 'react';
import { Link } from 'react-router-dom';
import { brand } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { submitContact, type LeadMeta } from '../../lib/mail';
import { IconCheck, IconMail } from '../Icons';
import './ContactForm.css';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
type Key = 'vorname' | 'nachname' | 'email' | 'telefon' | 'dsgvo' | 'confirm';
type Errors = Partial<Record<Key, string>>;

type Props = {
  subject: string;
  message?: string;
  submitLabel?: string;
  /** zusätzliche Angaben aus vorgeschalteten Schritten (Funnel, Rechner, Tippgeber) */
  extra?: [string, string | undefined | false][];
  phoneRequired?: boolean;
  benefits?: string[] | false;
  doneText?: string;
  /** strukturierte Angaben für das Anfrage-Portal (Art der Anfrage, Objekt, Exposé …) */
  meta?: LeadMeta;
  /** zusätzliche Pflichtbestätigung, z. B. Einverständnis der Eigentümer beim Tippgeber-Hinweis */
  confirm?: string;
};

/** Anfrageformular: Client-Validierung, Versand über /api/contact, Erfolg erst nach Server-Bestätigung. */
export default function ContactForm({
  subject, message = '', submitLabel = 'Details anfragen', extra = [], phoneRequired = false,
  benefits = ['Persönliche Rückmeldung durch unser Team.', 'Unverbindlich und kostenfrei.', 'Ihre Daten nutzen wir nur für diese Anfrage.'],
  doneText, meta, confirm,
}: Props) {
  const formId = useId();
  const [v, setV] = useState({ vorname: '', nachname: '', email: '', telefon: '', nachricht: message });
  const [dsgvo, setDsgvo] = useState(false);
  const [confirmed, setConfirmed] = useState(false);
  const [errors, setErrors] = useState<Errors>({});
  const [sent, setSent] = useState(false);
  const [sending, setSending] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [hp, setHp] = useState('');

  const set = (k: keyof typeof v) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setV({ ...v, [k]: e.target.value });
    if (errors[k as Key]) setErrors({ ...errors, [k]: undefined });
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    const err: Errors = {};
    if (!v.vorname.trim()) err.vorname = 'Bitte geben Sie Ihren Vornamen ein.';
    if (!v.nachname.trim()) err.nachname = 'Bitte geben Sie Ihren Nachnamen ein.';
    if (!EMAIL_RE.test(v.email.trim())) err.email = 'Bitte geben Sie eine gültige E-Mail-Adresse ein.';
    if (phoneRequired && v.telefon.replace(/\D/g, '').length < 6) err.telefon = 'Bitte geben Sie eine Telefonnummer für Rückfragen an.';
    if (confirm && !confirmed) err.confirm = 'Bitte bestätigen Sie das Einverständnis.';
    if (!dsgvo) err.dsgvo = 'Bitte bestätigen Sie die Datenschutzhinweise.';
    setErrors(err);
    setSubmitError(null);
    if (Object.keys(err).length > 0) return;

    setSending(true);
    const raw: [string, string | undefined | false][] = [
      ...extra,
      ['Name', `${v.vorname} ${v.nachname}`],
      ['E-Mail', v.email],
      ['Telefon', v.telefon],
      ['Nachricht', v.nachricht],
      [confirm ? 'Bestätigung' : '', confirm && confirmed ? confirm : undefined],
    ];
    const fields = raw.filter(([, val]) => val).map(([k, val]) => [k, String(val)] as [string, string]);
    const result = await submitContact({
      subject,
      fields,
      meta: {
        form: 'kontaktformular',
        ...meta,
        contact: { ...meta?.contact, first_name: v.vorname.trim(), last_name: v.nachname.trim(), email: v.email.trim(), phone: v.telefon.trim() || undefined },
        message: v.nachricht.trim() || undefined,
        consent: { privacy: true, ...(confirm ? { confirmation: confirm } : {}), text: `Ich bin damit einverstanden, dass ${brand.company} meine Angaben zur Bearbeitung dieser Anfrage verwendet und mich telefonisch oder per E-Mail kontaktiert.` },
        hp,
      },
    });
    setSending(false);
    if (result.ok) {
      setSent(true);
      return;
    }
    setSubmitError(result.message);
  };

  if (sent) {
    return (
      <div className="cform__done" role="status">
        <IconCheck size={32} />
        <p className="head">Vielen Dank, {v.vorname}!</p>
        <p>{doneText ?? 'Ihre Anfrage ist bei uns eingegangen. Wir melden uns in Kürze bei Ihnen.'}</p>
        <div className="cform__done-btns">
          <a href={brand.phoneHref} className="btn btn--outline">{brand.phoneDisplay}</a>
        </div>
      </div>
    );
  }

  const field = (k: 'vorname' | 'nachname' | 'email' | 'telefon', label: string, type = 'text', required = true) => (
    <label className={`cform__field${errors[k] ? ' has-error' : ''}`}>
      <span className="cform__label">{required ? '*' : ''}{label}</span>
      <input type={type} value={v[k]} onChange={set(k)} autoComplete={k === 'email' ? 'email' : k === 'telefon' ? 'tel' : k === 'vorname' ? 'given-name' : 'family-name'}
        required={required} id={`${formId}-${k}`} aria-invalid={!!errors[k]} aria-describedby={errors[k] ? `${formId}-${k}-error` : undefined} />
      {errors[k] && <span className="cform__error" id={`${formId}-${k}-error`} role="alert">{errors[k]}</span>}
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
      <label className="cform__hp" aria-hidden="true">
        Website <input tabIndex={-1} autoComplete="off" value={hp} onChange={(e) => setHp(e.target.value)} />
      </label>
      <label className="cform__field cform__field--full">
        <span className="cform__label">Ihre Nachricht</span>
        <textarea rows={3} value={v.nachricht} onChange={set('nachricht')} />
      </label>
      {confirm && (
        <div className={`cform__consent${errors.confirm ? ' has-error' : ''}`}>
          <input id={`${formId}-confirm`} type="checkbox" checked={confirmed} onChange={() => { setConfirmed(!confirmed); setErrors({ ...errors, confirm: undefined }); }} />
          <label htmlFor={`${formId}-confirm`} className="is-open">*{confirm}</label>
          {errors.confirm && <span className="cform__error" role="alert">{errors.confirm}</span>}
        </div>
      )}
      <div className={`cform__consent${errors.dsgvo ? ' has-error' : ''}`}>
        <input id={`${formId}-dsgvo`} type="checkbox" checked={dsgvo} onChange={() => { setDsgvo(!dsgvo); setErrors({ ...errors, dsgvo: undefined }); }} />
        <label htmlFor={`${formId}-dsgvo`} className="is-open">
          *Ich bin damit einverstanden, dass {brand.company} meine Angaben zur Bearbeitung dieser Anfrage verwendet und mich telefonisch oder per E-Mail kontaktiert.
          Details in der <Link to={ROUTES.datenschutz} className="link-underline">Datenschutzerklärung</Link>.
        </label>
        {errors.dsgvo && <span className="cform__error" role="alert">{errors.dsgvo}</span>}
      </div>
      {submitError && <p className="cform__error cform__submit-error" role="alert">{submitError}</p>}
      <div className="cform__submit">
        <button type="submit" className="btn btn--accent btn--icon" disabled={sending}>
          <IconMail />{sending ? 'Wird gesendet …' : submitLabel}
        </button>
      </div>
      {benefits && (
        <ul className="cform__benefits">
          {benefits.map((b) => <li key={b}><span className="cform__tick"><IconCheck size={14} /></span>{b}</li>)}
        </ul>
      )}
    </form>
  );
}
