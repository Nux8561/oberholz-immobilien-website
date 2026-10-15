import { Link } from 'react-router-dom';
import { usePageMeta } from '../layout/PageMeta';

export default function NotFound() {
  usePageMeta({ title: 'Seite nicht gefunden', crumbs: [{ label: 'Seite nicht gefunden' }], footer: 'accordion', noindex: true });
  return (
    <section className="wrap" style={{ textAlign: 'center', padding: '120px 40px' }}>
      <p className="eyebrow">Fehler 404</p>
      <h1 className="head" style={{ fontSize: 40, lineHeight: '48px', color: 'var(--c-text)', margin: '12px 0 24px' }}>Diese Seite gibt es nicht</h1>
      <Link to="/" className="btn">Zur Startseite</Link>
    </section>
  );
}
