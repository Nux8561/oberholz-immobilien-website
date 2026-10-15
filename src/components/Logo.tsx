import { Link } from 'react-router-dom';
import { brand } from '../data/content';
import './Logo.css';

/** Oberholz-Logo (Original-Datei der bisherigen Website); Fläche wie im Referenz-Header (299×60 Desktop). */
export default function Logo({ compact = false }: { compact?: boolean }) {
  return (
    <Link to="/" className={`logo${compact ? ' logo--compact' : ''}`} aria-label={`${brand.name} – Startseite`}>
      <img className="logo__img" src={brand.logo} alt={brand.name} width={519} height={238} />
    </Link>
  );
}
