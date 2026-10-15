import type { ReactNode } from 'react';
import './SectionIntro.css';

type Props = {
  eyebrow?: string;
  title: string;
  text?: ReactNode;
  level?: 'h1' | 'h2';
  /** 'section' = eigener Wrapper (896px), 'inline' = innerhalb eines Content-Wrappers */
  variant?: 'section' | 'inline';
  line?: boolean;
  /** auch <960px zentriert (z. B. Kontakt – wie Referenz) */
  center?: boolean;
  id?: string;
};

/** Section-Intro – Referenz: ≥1240px zentriert (max. 896px) mit 2×72px Akzentlinie darüber (96px Abstand),
 *  960–1239px zentriert auf 685px, darunter linksbündig mit Akzentlinie links. */
export default function SectionIntro({ eyebrow, title, text, level = 'h2', variant = 'section', line = true, center = false, id }: Props) {
  const H = level;
  const inner = (
    <header className={`sintro${line ? ' sintro--line' : ' sintro--plain'}${level === 'h1' ? ' sintro--lg' : ''}${center ? ' sintro--center' : ''}`}>
      <div className="sintro__head">
        {eyebrow && <p className="eyebrow sintro__eyebrow">{eyebrow}</p>}
        <H className="sintro__title head" id={id}>{title}</H>
      </div>
      {text && <p className="sintro__text">{text}</p>}
    </header>
  );
  return variant === 'section' ? <section className="sintro-wrap" aria-labelledby={id}>{inner}</section> : <div className="sintro-inline">{inner}</div>;
}
