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

/** Sollzins-Annahme aus Zinsbindung und Beleihungsauslauf (Heuristik, keine Bankkondition) */
export function estimateZins(bindung: number, ltv: number) {
  const base: Record<number, number> = { 5: 3.4, 10: 3.6, 15: 3.8, 20: 3.95, 25: 4.05, 30: 4.15 };
  const b = base[bindung] ?? 3.6;
  const add = ltv <= 0.6 ? -0.15 : ltv <= 0.8 ? 0 : ltv <= 0.9 ? 0.15 : ltv <= 1 ? 0.35 : 0.6;
  return Math.round((b + add) * 100) / 100;
}
