/**
 * Cloudflare Pages Function: Formularversand an das Anfrage-Portal (Webhook), optional zusätzlich per Resend.
 * Secrets/Variablen im Pages-Projekt:
 *   LEAD_WEBHOOK_URL – Ingest-Adresse des Anfrage-Portals (enthält den Zugangsschlüssel, daher nur als Secret)
 *   RESEND_API_KEY   – optional: zusätzlich E-Mail-Benachrichtigung über resend.com
 *   CONTACT_TO       – optional, Standard: mail@oberholz-immobilien.com
 *   CONTACT_FROM     – optional, Absender (muss in Resend verifiziert sein)
 *
 * Erfolg, sobald der Webhook (bzw. ohne Webhook die E-Mail) die Anfrage angenommen hat.
 * Ohne beides: HTTP 503 mit verständlicher Meldung (kein Schein-Erfolg).
 */

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const OFFICES = {
  essen: { slug: 'essen', city: 'Essen', contact_name: 'Felix Lesch', phone: '0201 61447786' },
  muenster: { slug: 'muenster', city: 'Münster', contact_name: 'Michael Oberholz', phone: '0251 28 42 90 90' },
};
const NOT_CONFIGURED = 'Der Formularversand ist gerade nicht erreichbar. Bitte schreiben Sie uns direkt an mail@oberholz-immobilien.com oder rufen Sie uns an: 0201 61447786.';

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  });
}

const str = (v, max = 2000) => (typeof v === 'string' ? v.trim().slice(0, max) : v == null ? undefined : String(v).trim().slice(0, max)) || undefined;
const list = (v) => (Array.isArray(v) ? v.map((x) => str(x, 200)).filter(Boolean) : undefined);

/** Entfernt leere Werte, damit das Portal nur echte Angaben sieht */
function compact(value) {
  if (Array.isArray(value)) {
    const arr = value.map(compact).filter((x) => x !== undefined);
    return arr.length ? arr : undefined;
  }
  if (value && typeof value === 'object') {
    const entries = Object.entries(value).map(([k, v]) => [k, compact(v)]).filter(([, v]) => v !== undefined);
    return entries.length ? Object.fromEntries(entries) : undefined;
  }
  return value === '' || value === null || Number.isNaN(value) ? undefined : value;
}

function buildLead(body, request) {
  const fields = (Array.isArray(body.fields) ? body.fields : [])
    .filter((f) => Array.isArray(f) && f.length === 2)
    .map(([k, v]) => [str(k, 100), str(v)])
    .filter(([k, v]) => k && v);
  const map = Object.fromEntries(fields);
  const meta = body.meta && typeof body.meta === 'object' ? body.meta : {};
  const ctx = body.context && typeof body.context === 'object' ? body.context : {};
  const c = meta.contact ?? {};

  const name = str(c.name) ?? str(map.Name) ?? str(`${c.first_name ?? ''} ${c.last_name ?? ''}`);
  const [first, ...rest] = (name ?? '').split(/\s+/);
  const contact = {
    first_name: str(c.first_name) ?? (rest.length ? first : undefined),
    last_name: str(c.last_name) ?? (rest.length ? rest.join(' ') : undefined),
    name,
    email: str(c.email, 200) ?? str(map['E-Mail'], 200),
    phone: str(c.phone, 60) ?? str(map.Telefon, 60),
    reachable: list(c.reachable),
    callback_time: str(c.callback_time, 60),
  };
  const office = (Object.hasOwn(OFFICES, meta.office ?? '') ? OFFICES[meta.office] : undefined) ?? (/Münster/i.test(map['PLZ/Ort'] ?? '') ? OFFICES.muenster : undefined);
  const url = new URL(request.url);
  const now = new Date().toISOString();

  return compact({
    event: 'website.lead',
    version: 1,
    id: str(body.id, 80),
    source: 'website',
    site: { name: 'Oberholz Immobilien', host: url.host },
    type: str(meta.type, 40) ?? 'kontakt',
    form: str(meta.form, 60),
    subject: str(body.subject, 200),
    topic: str(meta.topic, 120),
    intent: list(meta.intent),
    // die wichtigsten Angaben flach, damit das Portal sie ohne Verschachtelung findet
    first_name: contact.first_name,
    last_name: contact.last_name,
    name: contact.name,
    email: contact.email,
    phone: contact.phone,
    message: str(meta.message, 5000) ?? str(map.Nachricht, 5000),
    contact,
    property: meta.property && typeof meta.property === 'object' ? {
      kind: str(meta.property.kind, 60),
      subtype: str(meta.property.subtype, 80),
      detail: str(meta.property.detail, 200),
      location: str(meta.property.location, 200),
      units: Number(meta.property.units) || undefined,
      living_area_m2: Number(meta.property.living_area_m2) || undefined,
      plot_area_m2: Number(meta.property.plot_area_m2) || undefined,
    } : undefined,
    listing: meta.listing && typeof meta.listing === 'object' ? {
      id: str(meta.listing.id, 60),
      title: str(meta.listing.title, 300),
      city: str(meta.listing.city, 100),
      district: str(meta.listing.district, 100),
      agent: str(meta.listing.agent, 100),
      url: str(meta.listing.url, 500),
    } : undefined,
    calculator: meta.calculator && typeof meta.calculator === 'object'
      ? Object.fromEntries(Object.entries(meta.calculator).slice(0, 30).map(([k, v]) => [str(k, 60), typeof v === 'number' ? v : str(v, 200)]))
      : undefined,
    office,
    consent: { privacy: meta.consent?.privacy === true, text: str(meta.consent?.text, 1000), at: str(ctx.submitted_at, 40) ?? now },
    page: {
      url: str(ctx.page?.url, 1000) ?? str(body.page, 1000),
      path: str(ctx.page?.path, 300),
      title: str(ctx.page?.title, 300),
      referrer: str(ctx.page?.referrer, 1000),
    },
    attribution: ctx.attribution && typeof ctx.attribution === 'object'
      ? Object.fromEntries(Object.entries(ctx.attribution).slice(0, 20).map(([k, v]) => [str(k, 40), str(v, 1000)]))
      : undefined,
    client: {
      device: str(ctx.client?.device, 20),
      viewport_width: Number(ctx.client?.viewport_width) || undefined,
      language: str(ctx.client?.language, 20),
      user_agent: str(request.headers.get('user-agent'), 400),
      country: str(request.cf?.country, 4),
    },
    fields: Object.fromEntries(fields),
    fields_list: fields,
    submitted_at: str(ctx.submitted_at, 40),
    received_at: now,
  });
}

async function sendWebhook(urlString, lead) {
  const res = await fetch(urlString, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      ...(lead.id ? { 'Idempotency-Key': lead.id } : {}),
    },
    body: JSON.stringify(lead),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => '');
    console.error('Lead webhook error', res.status, detail.slice(0, 500));
    return false;
  }
  return true;
}

async function sendMail(env, lead) {
  const to = (env.CONTACT_TO ?? 'mail@oberholz-immobilien.com').trim();
  const from = (env.CONTACT_FROM ?? 'Oberholz Website <onboarding@resend.dev>').trim();
  const lines = (lead.fields_list ?? []).map(([k, v]) => `${k}: ${v}`);
  if (lead.page?.url) lines.push(`Seite: ${lead.page.url}`);
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY.trim()}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from,
      to: [to],
      reply_to: lead.email || undefined,
      subject: `[Website] ${lead.subject ?? 'Anfrage'}${lead.name ? ` – ${lead.name}` : ''}`,
      text: lines.join('\n'),
    }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => '');
    console.error('Resend error', res.status, detail.slice(0, 500));
    return false;
  }
  return true;
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}

export async function onRequestPost(context) {
  const { env, request } = context;
  const webhook = env.LEAD_WEBHOOK_URL?.trim();
  const mail = Boolean(env.RESEND_API_KEY?.trim());
  if (!webhook && !mail) {
    console.error('Formularversand nicht konfiguriert: LEAD_WEBHOOK_URL bzw. RESEND_API_KEY fehlt in den Pages-Secrets.');
    return json({ error: 'not_configured', message: NOT_CONFIGURED }, 503);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'invalid_json' }, 400);
  }

  // Honeypot ausgefüllt → Bot. Still „ok“ antworten, nichts weiterleiten.
  if (str(body?.meta?.hp)) return json({ ok: true });

  const lead = buildLead(body, request);
  if (!lead.subject || !lead.fields_list?.length) {
    return json({ error: 'missing_fields' }, 400);
  }
  if (lead.email && !EMAIL_RE.test(lead.email)) {
    return json({ error: 'invalid_email' }, 400);
  }

  const [hooked, mailed] = await Promise.all([
    webhook ? sendWebhook(webhook, lead).catch((e) => { console.error('Lead webhook error', e); return false; }) : Promise.resolve(false),
    mail ? sendMail(env, lead).catch((e) => { console.error('Resend error', e); return false; }) : Promise.resolve(false),
  ]);

  if (!hooked && !mailed) return json({ error: 'delivery_failed' }, 502);
  return json({ ok: true });
}
