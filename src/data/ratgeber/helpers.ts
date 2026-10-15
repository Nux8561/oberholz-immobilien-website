// Bausteine für die redaktionellen Ratgeber-Artikel (eigene Texte; Aufbau angelehnt an E&V-Ratgeber:
// Lesezeit, Inhaltsverzeichnis, „Das Wichtigste in Kürze“, Beispielrechnung, FAQ).
import type { QA, RichBlock } from '../oberholz';

import type { Category } from '../oberholz';
export type { Category };

export type EditorialArticle = {
  slug: string;
  category: Category;
  title: string;
  subtitle: string;
  intro: string;
  date: string;
  image: string;
  imageAlt: string;
  facts: string[];
  body: RichBlock[];
  faq: QA[];
  whitepaper?: string;
  tools?: ('budget' | 'finanzierung' | 'wertHebel' | 'bewertung')[];
};

export const h2 = (text: string): RichBlock => ({ t: 'h2', text });
export const h3 = (text: string): RichBlock => ({ t: 'h3', text });
export const p = (text: string): RichBlock => ({ t: 'p', text });
export const ul = (...items: string[]): RichBlock => ({ t: 'ul', items });
export const ol = (...items: string[]): RichBlock => ({ t: 'ol', items });
export const quote = (text: string): RichBlock => ({ t: 'blockquote', text });
export const table = (...rows: string[][]): RichBlock => ({ t: 'table', rows });

const OB = '/assets/oberholz';
export const obj = (id: string, n = 0) => `${OB}/objekte/${id}/${String(n).padStart(3, '0')}.jpg`;
export const media = (path: string) => `${OB}/media/${path}`;
