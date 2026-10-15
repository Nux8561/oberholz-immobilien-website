import { Link } from 'react-router-dom';
import { brand } from '../../data/content';
import type { Crumb } from '../../layout/PageMeta';
import { IconChevronRight } from '../Icons';
import './Breadcrumb.css';

/** Breadcrumb über dem Footer (Referenz: 12px, zwischen Kontakt-Section und Footer). */
export default function Breadcrumb({ items }: { items: Crumb[] }) {
  const all: Crumb[] = [{ label: brand.name, to: '/' }, ...items];
  return (
    <nav className="crumbs" aria-label="Brotkrumen-Navigation">
      <ol>
        {all.map((c, i) => (
          <li key={c.label}>
            {c.to && i < all.length - 1 ? <Link to={c.to}>{c.label}</Link> : <span aria-current={i === all.length - 1 ? 'page' : undefined}>{c.label}</span>}
            {i < all.length - 1 && <IconChevronRight size={12} />}
          </li>
        ))}
      </ol>
    </nav>
  );
}
