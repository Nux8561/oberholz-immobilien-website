// Formulare ohne Server: Die Anfrage wird als E-Mail vorbereitet und über das E-Mail-Programm
// der Besucher:innen versendet (mailto). Für den Livebetrieb kann hier ein Formular-Backend angebunden werden.
import { brand } from '../data/content';

export function mailtoHref(subject: string, fields: [string, string | undefined | false][]) {
  const body = fields.filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join('\n');
  return `mailto:${brand.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
