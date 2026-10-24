/**
 * Cloudflare Pages Function: Formularversand per Resend.
 * Benötigte Secrets im Pages-Projekt:
 *   RESEND_API_KEY  – API-Schlüssel von resend.com
 *   CONTACT_TO      – optional, Standard: mail@oberholz-immobilien.com
 *   CONTACT_FROM    – optional, Absender (muss in Resend verifiziert sein)
 *
 * Ohne RESEND_API_KEY: HTTP 503 mit klarer Meldung (kein Schein-Erfolg).
 */

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  });
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
  const key = context.env.RESEND_API_KEY?.trim();
  if (!key) {
    return json({
      error: 'not_configured',
      message: 'Formularversand nicht konfiguriert: RESEND_API_KEY fehlt in den Cloudflare Pages Secrets. Empfänger wäre mail@oberholz-immobilien.com.',
    }, 503);
  }

  let body;
  try {
    body = await context.request.json();
  } catch {
    return json({ error: 'invalid_json' }, 400);
  }

  const subject = (body.subject ?? '').trim().slice(0, 200);
  const fields = Array.isArray(body.fields) ? body.fields : [];
  if (!subject || fields.length === 0) {
    return json({ error: 'missing_fields' }, 400);
  }

  const map = Object.fromEntries(fields.map(([k, v]) => [k, String(v ?? '').trim()]));
  const email = map['E-Mail'] || map.Email || map.email || '';
  const name = map.Name || `${map.Vorname ?? ''} ${map.Nachname ?? ''}`.trim();
  if (email && !EMAIL_RE.test(email)) {
    return json({ error: 'invalid_email' }, 400);
  }

  const to = (context.env.CONTACT_TO ?? 'mail@oberholz-immobilien.com').trim();
  const from = (context.env.CONTACT_FROM ?? 'Oberholz Website <onboarding@resend.dev>').trim();
  const lines = fields
    .filter(([, v]) => String(v ?? '').trim())
    .map(([k, v]) => `${k}: ${String(v).trim()}`);
  if (body.page) lines.push(`Seite: ${body.page}`);
  const text = lines.join('\n');

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${key}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from,
      to: [to],
      reply_to: email || undefined,
      subject: `[Website] ${subject}${name ? ` – ${name}` : ''}`,
      text,
    }),
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => '');
    console.error('Resend error', res.status, detail.slice(0, 500));
    return json({ error: 'delivery_failed' }, 502);
  }

  return json({ ok: true });
}
