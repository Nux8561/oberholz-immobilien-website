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

const TYPE_LABEL = {
  bewertung: 'Bewertung', verkauf: 'Verkauf', vermietung: 'Vermietung', rueckmietverkauf: 'Rückmietverkauf',
  immotipp: 'Immotipp (Tippgeber)', finanzierung: 'Finanzierung', expose: 'Exposé-Anfrage', kontakt: 'Kontakt',
  rueckruf: 'Rückruf', 'wert-hebel': 'Wert-Hebel-Rechner', beratung: 'Beratung',
};
const ATTR_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'fbclid', 'msclkid'];

const str = (v, max = 2000) => (typeof v === 'string' ? v.trim().slice(0, max) : v == null ? undefined : String(v).trim().slice(0, max)) || undefined;
const join = (v) => (Array.isArray(v) ? v.map((x) => str(x, 200)).filter(Boolean).join(', ') || undefined : str(v, 200));

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
  };
  const type = str(meta.type, 40) ?? 'kontakt';
  const prop = meta.property && typeof meta.property === 'object' ? meta.property : {};
  const listing = meta.listing && typeof meta.listing === 'object' ? meta.listing : {};
  const attr = ctx.attribution && typeof ctx.attribution === 'object' ? ctx.attribution : {};
  const calculator = meta.calculator && typeof meta.calculator === 'object'
    ? Object.fromEntries(Object.entries(meta.calculator).slice(0, 30).map(([k, v]) => [`rechner_${String(k).replace(/[^a-z0-9_]/gi, '').slice(0, 50)}`, typeof v === 'number' ? v : str(v, 200)]))
    : {};
  const office = (Object.hasOwn(OFFICES, meta.office ?? '') ? OFFICES[meta.office] : undefined) ?? (/Münster/i.test(map['PLZ/Ort'] ?? '') ? OFFICES.muenster : undefined);
  const url = new URL(request.url);
  const now = new Date().toISOString();

  const lead = compact({
    // Technik (im Portal-Mapping auf „ignore“ oder intern)
    event: 'website.lead',
    version: 2,
    id: str(body.id, 80),
    source: 'website',
    website: url.host,
    type: type,
    formular: str(meta.form, 60),
    // Standardfelder – erkennt das Portal automatisch
    first_name: contact.first_name,
    last_name: contact.last_name,
    name: contact.name,
    email: contact.email,
    phone: contact.phone,
    // Anfrage – flache deutsche Schlüssel, passen per Auto-Mapping auf gleichnamige Portal-Felder
    betreff: str(body.subject, 200),
    anfrageart: TYPE_LABEL[type] ?? type,
    anliegen: str(meta.topic, 120),
    vorhaben: join(meta.intent),
    nachricht: str(meta.message, 5000) ?? str(map.Nachricht, 5000),
    objektart: str(prop.kind, 60),
    objekttyp: str(prop.subtype, 80),
    objektdetails: str(prop.detail, 200),
    ort_der_immobilie: str(prop.location, 200) ?? str(map['PLZ/Ort'], 200) ?? str(map.PLZ, 20),
    wohnflaeche_m2: Number(prop.living_area_m2) || undefined,
    grundstueck_m2: Number(prop.plot_area_m2) || undefined,
    wohneinheiten: Number(prop.units) || undefined,
    erreichbarkeit: join(c.reachable),
    rueckruf_zeitraum: str(c.callback_time, 60),
    buero: office?.city,
    ansprechpartner: office?.contact_name,
    expose_nr: str(listing.id, 60),
    expose_titel: str(listing.title, 300),
    expose_ort: str([listing.city, listing.district].filter(Boolean).join('-'), 200),
    expose_link: str(listing.url, 500),
    ...calculator,
    // Einwilligung
    einwilligung_datenschutz: meta.consent?.privacy === true ? 'ja' : undefined,
    einwilligung_text: str(meta.consent?.text, 1000),
    bestaetigung: str(meta.consent?.confirmation, 500),
    einwilligung_zeit: str(ctx.submitted_at, 40) ?? now,
    // Herkunft
    seite: str(ctx.page?.url, 1000) ?? str(body.page, 1000),
    seitentitel: str(ctx.page?.title, 300),
    herkunftsseite: str(ctx.page?.referrer, 1000),
    einstiegsseite: str(attr.landing_url, 1000),
    einstieg_herkunft: str(attr.landing_referrer, 1000),
    ...Object.fromEntries(ATTR_KEYS.map((k) => [k, str(attr[k], 300)])),
    geraet: str(ctx.client?.device, 20),
    bildschirmbreite: Number(ctx.client?.viewport_width) || undefined,
    sprache: str(ctx.client?.language, 20),
    browser: str(request.headers.get('user-agent'), 400),
    land: str(request.cf?.country, 4),
    gesendet_am: str(ctx.submitted_at, 40),
    empfangen_am: now,
  });
  const mailLines = fields.map(([k, v]) => `${k}: ${v}`);
  if (lead.seite) mailLines.push(`Seite: ${lead.seite}`);
  return { lead, mailLines };
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

async function sendMail(env, lead, lines) {
  const to = (env.CONTACT_TO ?? 'mail@oberholz-immobilien.com').trim();
  const from = (env.CONTACT_FROM ?? 'Oberholz Website <onboarding@resend.dev>').trim();
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
      subject: `[Website] ${lead.betreff ?? 'Anfrage'}${lead.name ? ` – ${lead.name}` : ''}`,
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

  const { lead, mailLines } = buildLead(body, request);
  if (!lead.betreff || !mailLines.length) {
    return json({ error: 'missing_fields' }, 400);
  }
  if (lead.email && !EMAIL_RE.test(lead.email)) {
    return json({ error: 'invalid_email' }, 400);
  }

  const [hooked, mailed] = await Promise.all([
    webhook ? sendWebhook(webhook, lead).catch((e) => { console.error('Lead webhook error', e); return false; }) : Promise.resolve(false),
    mail ? sendMail(env, lead, mailLines).catch((e) => { console.error('Resend error', e); return false; }) : Promise.resolve(false),
  ]);

  if (!hooked && !mailed) return json({ error: 'delivery_failed' }, 502);
  return json({ ok: true });
}
