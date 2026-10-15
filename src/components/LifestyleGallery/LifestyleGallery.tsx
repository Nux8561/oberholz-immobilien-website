import { useCallback, useEffect, useRef, useState } from 'react';
import { lifestyle } from '../../data/content';
import { IconArrowRight, IconChevronLeft, IconChevronRight, IconClose, IconExpand } from '../Icons';
import './LifestyleGallery.css';

/** Galerie – Referenz 1440: zwei Reihen à 445px, Gap 16: [groß 789×444 | 2× klein 322×214] und gespiegelt.
 *  Kacheln sind Buttons; „Zur Galerie“ öffnet eine Vollbild-Ansicht. */
type Item = { image: string; title: string; alt: string };

export default function LifestyleGallery() {
  return <LifestyleGrid items={lifestyle.items} />;
}

/** Asymmetrisches 6er-Raster (groß + 2 klein, gespiegelt) mit Vollbildansicht – auch für Unterseiten */
export function LifestyleGrid({ items }: { items: Item[] }) {
  const [open, setOpen] = useState<number | null>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const lastFocus = useRef<HTMLElement | null>(null);

  const show = (i: number) => { lastFocus.current = document.activeElement as HTMLElement; setOpen(i); };
  const close = useCallback(() => { setOpen(null); lastFocus.current?.focus(); }, []);
  const step = useCallback((d: number) => setOpen((o) => (o === null ? o : (o + d + items.length) % items.length)), [items.length]);

  useEffect(() => {
    if (open === null) return;
    document.body.classList.add('no-scroll');
    closeRef.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') step(1);
      if (e.key === 'ArrowLeft') step(-1);
    };
    document.addEventListener('keydown', onKey);
    return () => { document.removeEventListener('keydown', onKey); document.body.classList.remove('no-scroll'); };
  }, [open, close, step]);

  const tile = (i: number, big: boolean) => (
    <button key={i} type="button" className={`gtile${big ? ' gtile--big' : ''}`} onClick={() => show(i)} aria-label={`${items[i].title} – Bild vergrößern`}>
      <img src={items[i].image} alt={items[i].alt} loading="lazy" />
      <span className="gtile__overlay">
        <span className="gtile__title head">{items[i].title}</span>
        <span className="gtile__more">{lifestyle.more}<IconArrowRight /></span>
      </span>
    </button>
  );

  return (
    <section className="wrap gallery-wrap" aria-label="Bildergalerie">
      <div className="gallery">
        <div className="gallery__row">
          {tile(0, true)}
          <div className="gallery__stack">{tile(1, false)}{tile(2, false)}</div>
        </div>
        {items.length > 3 && <div className="gallery__row gallery__row--rev">
          {tile(5, true)}
          <div className="gallery__stack">{tile(3, false)}{tile(4, false)}</div>
        </div>}
        <button type="button" className="btn btn--light btn--icon gallery__open" onClick={() => show(0)}>
          <IconExpand /><span className="gallery__open-label">{lifestyle.galleryButton}</span>
        </button>
      </div>

      {open !== null && (
        <div className="lightbox" role="dialog" aria-modal="true" aria-label="Galerie">
          <button type="button" className="lightbox__close" onClick={close} ref={closeRef} aria-label="Galerie schließen"><IconClose /></button>
          <button type="button" className="lightbox__nav lightbox__nav--prev" onClick={() => step(-1)} aria-label="Vorheriges Bild"><IconChevronLeft /></button>
          <figure className="lightbox__fig">
            <img src={items[open].image} alt={items[open].alt} />
            <figcaption><span className="head">{items[open].title}</span><span className="lightbox__count">{open + 1} / {items.length}</span></figcaption>
          </figure>
          <button type="button" className="lightbox__nav lightbox__nav--next" onClick={() => step(1)} aria-label="Nächstes Bild"><IconChevronRight /></button>
        </div>
      )}
    </section>
  );
}
