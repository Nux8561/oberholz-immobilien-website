import { useCallback, useEffect, useRef, useState } from 'react';
import { hero } from '../../data/content';
import { IconArrowRight, IconPause, IconPlay } from '../Icons';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../data/routes';
import { findProperty, formatPrice, type Property } from '../../data/properties';

const SLIDES = hero.slideIds.map(findProperty).filter((p): p is Property => !!p);
import './HeroCarousel.css';

// Referenz: 5 Slides (Videos à ~15 s), automatischer Wechsel nach Ablauf, Fortschrittsbalken unten mittig.
export const SLIDE_DURATION = 15000;
const SWIPE_THRESHOLD = 50;

export default function HeroCarousel() {
  const slides = SLIDES;
  const [index, setIndex] = useState(0);
  const [paused, setPaused] = useState(false);
  const [progress, setProgress] = useState(0); // 0..1 des aktiven Slides
  const elapsed = useRef(0);
  const last = useRef<number | null>(null);
  const drag = useRef<{ x: number; y: number; dx: number } | null>(null);
  const [dragX, setDragX] = useState(0);
  const dragged = useRef(false); // Wischgeste auf der Bildunterschrift soll den Link nicht auslösen

  const go = useCallback((i: number) => {
    setIndex((i + slides.length) % slides.length);
    elapsed.current = 0;
    setProgress(0);
  }, [slides.length]);

  useEffect(() => {
    if (paused) { last.current = null; return; }
    let raf = 0;
    const tick = (t: number) => {
      if (last.current !== null) elapsed.current += t - last.current;
      last.current = t;
      if (elapsed.current >= SLIDE_DURATION) { go(index + 1); return; }
      setProgress(elapsed.current / SLIDE_DURATION);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => { cancelAnimationFrame(raf); last.current = null; };
  }, [paused, index, go]);

  const onPointerDown = (e: React.PointerEvent) => {
    if ((e.target as HTMLElement).closest('button')) return;
    drag.current = { x: e.clientX, y: e.clientY, dx: 0 };
    dragged.current = false;
  };
  const onPointerMove = (e: React.PointerEvent) => {
    if (!drag.current) return;
    drag.current.dx = e.clientX - drag.current.x;
    if (Math.abs(drag.current.dx) > 8) { dragged.current = true; setDragX(drag.current.dx); }
  };
  const onPointerUp = () => {
    if (!drag.current) return;
    const { dx } = drag.current;
    drag.current = null;
    setDragX(0);
    if (dx <= -SWIPE_THRESHOLD) go(index + 1);
    else if (dx >= SWIPE_THRESHOLD) go(index - 1);
  };

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowRight') go(index + 1);
    if (e.key === 'ArrowLeft') go(index - 1);
  };

  return (
    <div className="hcar" role="region" aria-roledescription="carousel" aria-label="Ausgewählte Immobilien" tabIndex={0} onKeyDown={onKey}
      onPointerDown={onPointerDown} onPointerMove={onPointerMove} onPointerUp={onPointerUp} onPointerCancel={onPointerUp} onPointerLeave={onPointerUp}>
      <ul className={`hcar__track${dragX ? ' is-dragging' : ''}`} style={{ transform: `translateX(calc(${-index * 100}% + ${dragX}px))` }} aria-live={paused ? 'polite' : 'off'}>
        {slides.map((s, i) => (
          <li key={s.id} className="hcar__slide" aria-roledescription="slide" aria-label={`${i + 1} von ${slides.length}`} aria-hidden={i !== index}>
            <img src={s.images[0]} alt={s.title} draggable={false} loading={i === 0 ? 'eager' : 'lazy'} />
            <Link to={ROUTES.expose(s.id)} className="hcar__caption" tabIndex={i === index ? 0 : -1} draggable={false}
              onClick={(e) => { if (dragged.current) { e.preventDefault(); dragged.current = false; } }}>
              <span className="hcar__title head">{s.title}</span>
              <span className="hcar__price">{s.district ? `${s.city}-${s.district}` : s.city} · {formatPrice(s)}<IconArrowRight /></span>
            </Link>
          </li>
        ))}
      </ul>
      <button type="button" className="hcar__pause" onClick={() => setPaused((p) => !p)} aria-label={paused ? 'Abspielen' : 'Pause'}>
        {paused ? <IconPlay /> : <IconPause />}
      </button>
      <div className="hcar__bars" role="tablist" aria-label="Slide auswählen">
        {slides.map((s, i) => (
          <button key={s.id} type="button" role="tab" aria-selected={i === index} aria-label={`Slide ${i + 1}: ${s.title}`}
            className="hcar__bar" onClick={() => go(i)}>
            <span className="hcar__fill" style={{ transform: `scaleX(${i < index ? 1 : i === index ? progress : 0})` }} />
          </button>
        ))}
      </div>
    </div>
  );
}
