// Formularversand: POST an /api/contact (Cloudflare Pages Function).
// Erfolg erst nach bestätigter Server-Antwort. Ohne RESEND_API_KEY liefert die Function 503.
import { brand } from '../data/content';

export type ContactPayload = {
  subject: string;
  fields: [string, string][];
  page?: string;
};

export function fieldsToBody(fields: [string, string | undefined | false][]) {
  return fields.filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join('\n');
}

/** Legacy-Hilfsfunktion (Tests / Fallback-Hinweise) */
export function mailtoHref(subject: string, fields: [string, string | undefined | false][]) {
  const body = fieldsToBody(fields);
  return `mailto:${brand.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

export type SubmitResult =
  | { ok: true }
  | { ok: false; status: number; message: string };

/** Sendet die Anfrage an den Formular-Endpunkt. Erfolg nur bei HTTP 2xx. */
export async function submitContact(payload: ContactPayload): Promise<SubmitResult> {
  const fields = payload.fields.filter(([, v]) => v.trim()) as [string, string][];
  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        subject: payload.subject,
        fields,
        page: payload.page ?? (typeof window !== 'undefined' ? window.location.href : undefined),
      }),
    });
    const data = (await res.json().catch(() => ({}))) as { error?: string; message?: string };
    if (res.ok) return { ok: true };
    if (res.status === 503) {
      return {
        ok: false,
        status: 503,
        message: data.message
          ?? 'Der Formularversand ist noch nicht freigeschaltet. Bitte schreiben Sie uns direkt an mail@oberholz-immobilien.com oder rufen Sie uns an.',
      };
    }
    return {
      ok: false,
      status: res.status,
      message: data.error ?? 'Die Anfrage konnte nicht gesendet werden. Bitte versuchen Sie es erneut oder kontaktieren Sie uns telefonisch.',
    };
  } catch {
    return {
      ok: false,
      status: 0,
      message: 'Keine Verbindung zum Formularserver. Bitte prüfen Sie Ihre Internetverbindung oder schreiben Sie uns direkt per E-Mail.',
    };
  }
}
