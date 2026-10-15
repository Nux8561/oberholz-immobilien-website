import { useState } from 'react';
import { relatedTopics as rt } from '../../data/content';
import SectionIntro from '../SectionIntro/SectionIntro';
import { IconMinus, IconPlus, TopicIllustration } from '../Icons';
import SmartLink from '../SmartLink/SmartLink';
import './RelatedTopics.css';

const COLLAPSED = 3;

/** Weitere Themen – Desktop: Icon + Text links, zwei Linkspalten rechts (2×258px).
 *  <960px: eine Linkspalte, nur 3 Links sichtbar + „Mehr anzeigen“ (Referenz 390px). */
export default function RelatedTopics() {
  const [open, setOpen] = useState<Record<number, boolean>>({});

  return (
    <section className="wrap" aria-labelledby="themen-title">
      <SectionIntro variant="inline" line={false} eyebrow={rt.eyebrow} title={rt.title} id="themen-title" />
      <ul className="topics">
        {rt.groups.map((g, gi) => {
          const all = [...g.haus, ...g.wohnung];
          const expanded = !!open[gi];
          return (
            <li key={g.title} className={`topic${expanded ? ' is-expanded' : ''}`}>
              <div className="topic__intro">
                <TopicIllustration name={g.icon} className="topic__icon" />
                <div>
                  <h3 className="topic__title head">{g.title}</h3>
                  <p className="topic__text">{g.text}</p>
                </div>
              </div>
              <div className="topic__links" id={`topic-links-${gi}`}>
                <ul className="topic__col">
                  {g.haus.map((l) => <li key={l}><SmartLink label={l} className="topic__link" /></li>)}
                </ul>
                <ul className="topic__col">
                  {g.wohnung.map((l) => <li key={l}><SmartLink label={l} className="topic__link" /></li>)}
                </ul>
                <ul className="topic__col topic__col--mobile">
                  {all.map((l, i) => (
                    <li key={l} hidden={!expanded && i >= COLLAPSED}><SmartLink label={l} className="topic__link" /></li>
                  ))}
                </ul>
                <button type="button" className="topic__toggle" aria-expanded={expanded} aria-controls={`topic-links-${gi}`}
                  onClick={() => setOpen((o) => ({ ...o, [gi]: !o[gi] }))}>
                  {expanded ? 'Weniger anzeigen' : 'Mehr anzeigen'}
                  {expanded ? <IconMinus /> : <IconPlus />}
                </button>
              </div>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
