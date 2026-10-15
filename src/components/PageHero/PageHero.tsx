import type { ReactNode } from 'react';
import { Button, type Btn } from '../../blocks/Blocks';
import { IconCheck } from '../Icons';
import { Faces, clean } from '../Rich/Rich';
import './PageHero.css';

type Props = {
  eyebrow?: string;
  title: string;
  text?: string;
  checks?: string[];
  buttons?: Btn[];
  image: string;
  alt?: string;
  /** freigestelltes Personenfoto (PNG) – unten bündig statt formatfüllend */
  cutout?: boolean;
  rating?: boolean;
  children?: ReactNode;
};

/** Seitenkopf der Inhaltsseiten – Aufbau wie das Split-Hero der Referenz-Unterseiten (Text links, Bild rechts, Creme). */
export default function PageHero({ eyebrow, title, text, checks, buttons, image, alt = '', cutout, rating, children }: Props) {
  return (
    <section className="b-shero phero">
      <div className="b-shero__grid">
        <article className="b-shero__body">
          {eyebrow && <p className="eyebrow phero__eyebrow">{eyebrow}</p>}
          <h1 className="b-shero__title head">{clean(title)}</h1>
          {text && <p className="b-shero__text">{clean(text)}</p>}
          {checks && checks.length > 0 && (
            <ul className="phero__checks">
              {checks.map((c) => <li key={c}><span className="rich__tick"><IconCheck size={14} /></span>{clean(c)}</li>)}
            </ul>
          )}
          {children}
          {buttons && <div className="b-shero__btns">{buttons.map((x) => <Button key={x.label} b={x} />)}</div>}
          {rating && <Faces />}
        </article>
        <div className={`b-shero__media${cutout ? ' phero__media--cutout' : ''}`}><img src={image} alt={alt} /></div>
      </div>
    </section>
  );
}
