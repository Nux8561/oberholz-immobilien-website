import { useId, useState, type ReactNode } from 'react';
import { IconMinus, IconPlus } from '../Icons';
import './Accordion.css';

export type AccordionItem = { title: ReactNode; content: ReactNode };

/** Akkordeon-Liste – 'faq' (16px, Trennlinien, rotes +) oder 'compact' (12px Versalien, Bundesländer-Liste). */
export default function Accordion({ items, variant = 'faq', columns = 1 }: { items: AccordionItem[]; variant?: 'faq' | 'compact'; columns?: 1 | 2 }) {
  const [open, setOpen] = useState<number | null>(null);
  const id = useId();
  return (
    <ul className={`acc acc--${variant}${columns === 2 ? ' acc--cols' : ''}`}>
      {items.map((it, i) => (
        <li key={i} className={`acc__item${open === i ? ' is-open' : ''}`}>
          <button type="button" className="acc__btn" aria-expanded={open === i} aria-controls={`${id}-${i}`} onClick={() => setOpen(open === i ? null : i)}>
            <span className="acc__title">{it.title}</span>
            {open === i ? <IconMinus /> : <IconPlus />}
          </button>
          <div className="acc__panel" id={`${id}-${i}`} hidden={open !== i}>{it.content}</div>
        </li>
      ))}
    </ul>
  );
}
