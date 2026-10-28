// Formularversand: POST an /api/contact (Cloudflare Pages Function), die Function leitet an das Anfrage-Portal (Webhook) weiter.
// Erfolg erst nach bestätigter Server-Antwort. Ohne LEAD_WEBHOOK_URL (und ohne RESEND_API_KEY) liefert die Function 503.
import { brand } from '../data/content';

/** Art der Anfrage – im Portal als Filter nutzbar */
export type LeadType =
  | 'bewertung' | 'verkauf' | 'vermietung' | 'rueckmietverkauf' | 'immotipp' | 'finanzierung'
  | 'expose' | 'kontakt' | 'rueckruf' | 'wert-hebel' | 'beratung';

/** Strukturierte Zusatzangaben je Formular (Rohfelder stehen zusätzlich in `fields`) */
export type LeadMeta = {
  form?: string;
  type?: LeadType;
  intent?: string[];
  office?: 'essen' | 'muenster';
  topic?: string;
  contact?: { first_name?: string; last_name?: string; name?: string; email?: string; phone?: string; reachable?: string[]; callback_time?: string };
  message?: string;
  property?: { kind?: string; subtype?: string; detail?: string; location?: string; units?: number; living_area_m2?: number; plot_area_m2?: number };
  listing?: { id: string; title?: string; city?: string; district?: string; agent?: string; url?: string };
  calculator?: Record<string, string | number | undefined>;
  consent?: { privacy: boolean; text?: string; confirmation?: string };
  /** Honeypot: von Menschen nie ausgefüllt */
  hp?: string;
};

export type ContactPayload = {
  subject: string;
  fields: [string, string][];
  page?: string;
  meta?: LeadMeta;
};

export function fieldsToBody(fields: [string, string | undefined | false][]) {
  return fields.filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join('\n');
}

/** Legacy-Hilfsfunktion (Tests / Fallback-Hinweise) */
export function mailtoHref(subject: string, fields: [string, string | undefined | false][]) {
  const body = fieldsToBody(fields);
  return `mailto:${brand.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

// Herkunft der Sitzung (Einstiegsseite, Referrer, Kampagnenparameter) – einmal je Sitzung festhalten,
// weil die Website eine Single-Page-App ist und die Parameter nach dem ersten Klick aus der Adresse verschwinden.
const ATTR_KEY = 'oh-attr';
const ATTR_PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'fbclid', 'msclkid'];
type Attribution = { landing_url?: string; landing_referrer?: string; params: Record<string, string> };

function readAttribution(): Attribution | null {
  try { return JSON.parse(sessionStorage.getItem(ATTR_KEY) ?? 'null'); } catch { return null; }
}

export function captureAttribution() {
  if (typeof window === 'undefined') return;
  const current = new URLSearchParams(window.location.search);
  const params = Object.fromEntries(ATTR_PARAMS.filter((k) => current.get(k)).map((k) => [k, current.get(k)!.slice(0, 200)]));
  const stored = readAttribution();
  if (stored && !Object.keys(params).length) return;
  const next: Attribution = {
    landing_url: stored?.landing_url ?? window.location.href,
    landing_referrer: stored?.landing_referrer ?? (document.referrer || undefined),
    params: { ...(stored?.params ?? {}), ...params },
  };
  try { sessionStorage.setItem(ATTR_KEY, JSON.stringify(next)); } catch { /* privater Modus */ }
}
captureAttribution();

function officeFromPath(path: string): LeadMeta['office'] {
  if (path.startsWith('/regionen/essen')) return 'essen';
  if (path.startsWith('/regionen/muenster')) return 'muenster';
  return undefined;
}

function newId() {
  try { return crypto.randomUUID(); } catch { return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`; }
}

export type SubmitResult =
  | { ok: true }
  | { ok: false; status: number; message: string };

/** Sendet die Anfrage an den Formular-Endpunkt. Erfolg nur bei HTTP 2xx. */
export async function submitContact(payload: ContactPayload): Promise<SubmitResult> {
  const fields = payload.fields.filter(([, v]) => v.trim()) as [string, string][];
  const isBrowser = typeof window !== 'undefined';
  const attr = isBrowser ? readAttribution() : null;
  const path = isBrowser ? window.location.pathname : '';
  const context = isBrowser ? {
    submitted_at: new Date().toISOString(),
    page: { url: window.location.href, path, title: document.title, referrer: document.referrer || undefined },
    attribution: attr ? { landing_url: attr.landing_url, landing_referrer: attr.landing_referrer, ...attr.params } : undefined,
    client: {
      device: window.matchMedia('(max-width: 767px)').matches ? 'mobile' : window.matchMedia('(max-width: 1023px)').matches ? 'tablet' : 'desktop',
      viewport_width: window.innerWidth,
      language: navigator.language,
    },
  } : undefined;
  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        id: newId(),
        subject: payload.subject,
        fields,
        page: payload.page ?? (isBrowser ? window.location.href : undefined),
        meta: { office: officeFromPath(path), ...payload.meta },
        context,
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
      message: data.error === 'invalid_email'
        ? 'Bitte prüfen Sie Ihre E-Mail-Adresse.'
        : 'Die Anfrage konnte nicht gesendet werden. Bitte versuchen Sie es erneut oder kontaktieren Sie uns telefonisch.',
    };
  } catch {
    return {
      ok: false,
      status: 0,
      message: 'Keine Verbindung zum Formularserver. Bitte prüfen Sie Ihre Internetverbindung oder schreiben Sie uns direkt per E-Mail.',
    };
  }
}
