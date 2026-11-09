// Rechenkern der Service-Rechner. Alle Werte sind Modellrechnungen ohne Gewähr.
import { page } from '../../data/oberholz';

/** Grunderwerbsteuer je Bundesland – Tabelle der Seite „Finanzierungsrechner“ der bisherigen Website */
export const GREST: [string, number][] = (() => {
  const t = page('service-finanzierungsrechner').blocks.find((b) => b.t === 'table') as { rows: string[][] } | undefined;
  return (t?.rows.slice(1) ?? []).map(([land, rate]) => [land, Number(rate.replace('%', '').replace(',', '.').trim())]);
})();
export const DEFAULT_LAND = 'Nordrhein-Westfalen';

export const eur = (n: number) => `${Math.round(n).toLocaleString('de-DE')} €`;
export const pct = (n: number, d = 2) => `${n.toLocaleString('de-DE', { minimumFractionDigits: d, maximumFractionDigits: d })} %`;

/** Monatsrate einer Annuität (Zins + anfängliche Tilgung p. a.) */
export const annuity = (loan: number, zins: number, tilgung: number) => (loan * (zins + tilgung)) / 100 / 12;

/** Restschuld nach n Monaten bei monatlicher Zahlung */
export function balanceAfter(loan: number, zins: number, rate: number, months: number) {
  const r = zins / 100 / 12;
  if (r === 0) return Math.max(0, loan - rate * months);
  const f = (1 + r) ** months;
  return Math.max(0, loan * f - (rate * (f - 1)) / r);
}

/** Laufzeit bis zur Volltilgung in Jahren */
export function payoffYears(loan: number, zins: number, rate: number) {
  const r = zins / 100 / 12;
  if (rate <= loan * r) return Infinity;
  return -Math.log(1 - (loan * r) / rate) / Math.log(1 + r) / 12;
}

/** Marktzins-Annahme für alle Rechner (Sollzins bei 10 Jahren Zinsbindung).
 *  Wird von Hand gepflegt: bei Zinsänderungen nur diese beiden Werte anpassen.
 *  Stand laut Felix Lesch (Kundenfeedback 09.11.2026): aktuell um die 5 %. */
export const ZINS_BASIS = 5.0;
export const ZINS_STAND = 'November 2026';

/** Sollzins-Annahme aus Zinsbindung und Beleihungsauslauf (Heuristik, keine Bankkondition).
 *  Auf- und Abschläge je Zinsbindung relativ zu ZINS_BASIS (10 Jahre). */
export function estimateZins(bindung: number, ltv: number) {
  const offset: Record<number, number> = { 5: -0.2, 10: 0, 15: 0.2, 20: 0.35, 25: 0.45, 30: 0.55 };
  const b = ZINS_BASIS + (offset[bindung] ?? 0);
  const add = ltv <= 0.6 ? -0.15 : ltv <= 0.8 ? 0 : ltv <= 0.9 ? 0.15 : ltv <= 1 ? 0.35 : 0.6;
  return Math.round((b + add) * 100) / 100;
}
