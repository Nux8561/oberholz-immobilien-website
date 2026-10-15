// Impressum, Datenschutz, Cookie-Hinweise und „Mein Bereich“.
import { Link } from 'react-router-dom';
import { page, type RichBlock } from '../../data/oberholz';
import { brand } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { findProperty, type Property } from '../../data/properties';
import { usePageMeta } from '../../layout/PageMeta';
import { useFavorites, useSavedSearches } from '../../lib/store';
import Rich from '../../components/Rich/Rich';
import PropertyCard from '../../components/PropertyCard/PropertyCard';
import SectionIntro from '../../components/SectionIntro/SectionIntro';
import { openCookieSettings } from '../../components/Cookies/Cookies';
import { notify } from '../../components/Toast/Toast';
import { TeaserBand, TOOL_TEASERS } from './shared';

export function Impressum() {
  usePageMeta({ title: 'Impressum', crumbs: [{ label: 'Impressum' }], footer: 'accordion' });
  const b = page('impressum').blocks;
  // Die EU-Plattform zur Online-Streitbeilegung (ODR) wurde am 20.07.2025 eingestellt – der Hinweis darauf entfällt.
  const verbraucher = b.filter((x) => x.t === 'p' && /^Verbraucherinformation/.test(x.text) && !/ODR|Online-Streitbeilegung/.test(x.text));
  return (
    <div className="legal">
      <h1 className="head">Impressum</h1>
      <Rich blocks={[
        { t: 'h3', text: 'Angaben gemäß § 5 DDG' },
        { t: 'p', text: brand.company },
        { t: 'p', text: `${brand.street.replace('straße', 'str.')}, D-48147 Münster` },
        { t: 'p', text: 'Tel. +49 (0)251 – 28 42 90 90 · Fax +49 (0)251 – 28 42 90 91' },
        { t: 'p', text: `E-Mail: ${brand.email} (Impressum-Kontakt: info@sv-oberholz.de) · Bürotermine nach Vereinbarung` },
        { t: 'h3', text: 'Steuer & Aufsicht' },
        { t: 'p', text: 'Finanzamt Münster-Innenstadt · USt.-IdNr. DE297711149' },
        { t: 'p', text: 'Berufsaufsichtsbehörde (Erlaubnis nach § 34c GewO): Stadt Münster, Ordnungsamt, Klemensstr. 10, Münster' },
        { t: 'h3', text: 'Versicherungen' },
        { t: 'p', text: 'Eine Vermögensschadenhaftpflichtversicherung besteht bei der ERGO Versicherungsgruppe AG, Victoriaplatz 2, 40198 Düsseldorf. Eine Vertrauensschadenhaftpflichtversicherung besteht über den Immobilienverband Deutschland IVD bei der ERGO Versicherungsgruppe AG, Victoriaplatz 2, 40198 Düsseldorf.' },
        { t: 'h3', text: 'Verbraucherinformationen' },
        ...verbraucher,
      ]} />
    </div>
  );
}

/** Abschnitte der bisherigen Datenschutzerklärung, die nicht zu dieser Website passen
 *  (Vimeo wird nicht eingesetzt; „Widget“-Abschnitt und Aufsichtsbehörde betrafen ein anderes Unternehmen/Bundesland). */
const DROP = ['Einbindung von Diensten und Inhalten Dritter', 'Oberholz Immobilien Widget', 'Der Landesbeauftragte für den Datenschutz und die Informationsfreiheit'];

export function Datenschutz() {
  usePageMeta({ title: 'Datenschutzerklärung', crumbs: [{ label: 'Datenschutz' }], footer: 'accordion' });
  const src = page('datenschutzerklaerung').blocks.slice(1);
  const out: RichBlock[] = [];
  let skip = false;
  for (const x of src) {
    if (x.t === 'h2') skip = DROP.includes(x.text);
    if (!skip) out.push(x);
  }
  return (
    <div className="legal">
      <h1 className="head">Datenschutzerklärung</h1>
      <Rich blocks={[
        { t: 'h2', text: 'Verantwortlicher' },
        { t: 'p', text: `${brand.company}, ${brand.street}, ${brand.city.replace(', Deutschland', '')} · Telefon ${brand.phoneDisplay} · E-Mail ${brand.email}` },
        ...out,
        { t: 'h2', text: 'Merkliste, gespeicherte Suchen und Anfragen' },
        { t: 'p', text: 'Merkliste und gespeicherte Suchen werden ausschließlich im lokalen Speicher Ihres Browsers abgelegt und nicht an uns übertragen. Sie können diese Daten jederzeit unter „Mein Bereich“ oder in den Cookie-Einstellungen löschen.' },
        { t: 'p', text: 'Anfrageformulare dieser Website übermitteln keine Daten an einen Server. Ihre Angaben werden zu einer E-Mail zusammengestellt, die Sie selbst über Ihr E-Mail-Programm an uns senden. Die Verarbeitung erfolgt anschließend wie unter „Kontaktaufnahme“ beschrieben.' },
        { t: 'p', text: 'Die Rechner (Budget-, Finanzierungs- und Wert-Hebel-Rechner) rechnen vollständig in Ihrem Browser; Ihre Eingaben werden nicht gespeichert oder übertragen.' },
        { t: 'h2', text: 'Kontakt per WhatsApp' },
        { t: 'p', text: 'Sie können uns über den Messenger-Dienst WhatsApp der WhatsApp Ireland Limited, 4 Grand Canal Square, Grand Canal Harbour, Dublin 2, Irland (Teil der Meta-Gruppe) erreichen. WhatsApp ist auf dieser Website nicht eingebunden: Erst wenn Sie einen WhatsApp-Link anklicken, öffnet sich WhatsApp bzw. die Website von WhatsApp, und es gelten die Datenschutzbestimmungen von WhatsApp. Dabei können Daten (z. B. Telefonnummer, Nachrichteninhalte, Metadaten) auch in Drittländer wie die USA übertragen werden.' },
        { t: 'p', text: 'Die Kommunikation per WhatsApp ist freiwillig. Wir verarbeiten Ihre Nachricht und Telefonnummer zur Beantwortung Ihrer Anfrage (Art. 6 Abs. 1 lit. b DSGVO bei vorvertraglichen Anfragen, sonst Art. 6 Abs. 1 lit. f DSGVO). Sensible Unterlagen senden Sie uns bitte per E-Mail oder persönlich. Wenn Sie WhatsApp nicht nutzen möchten, erreichen Sie uns jederzeit telefonisch oder per E-Mail.' },
        { t: 'h2', text: 'Links zu Partnern und externen Diensten' },
        { t: 'p', text: 'Diese Website enthält Links zu Google Maps, Google-Bewertungen, LinkedIn sowie zu unseren Kooperations- und Finanzierungspartnern und Immobilienportalen. Beim bloßen Aufruf unserer Seiten werden keine Daten an diese Anbieter übertragen. Erst wenn Sie einen Link anklicken, verlassen Sie unsere Website; für die Verarbeitung auf der Zielseite ist der jeweilige Anbieter verantwortlich.' },
        { t: 'h2', text: 'Aufsichtsbehörde' },
        { t: 'p', text: 'Gemäß Art. 77 DSGVO können Sie sich bei einer Aufsichtsbehörde beschweren, insbesondere in dem Mitgliedstaat Ihres Aufenthaltsorts, Ihres Arbeitsplatzes oder des Orts des mutmaßlichen Verstoßes. Zuständig für uns ist die Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen, Kavalleriestraße 2–4, 40213 Düsseldorf.' },
      ]} />
    </div>
  );
}

export function CookieHinweise() {
  usePageMeta({ title: 'Cookie-Hinweise', crumbs: [{ label: 'Cookie-Hinweise' }], footer: 'accordion', noindex: true });
  return (
    <div className="legal">
      <h1 className="head">Cookie-Hinweise</h1>
      <Rich blocks={[
        { t: 'p', text: 'Diese Website verwendet keine Tracking-, Analyse- oder Marketing-Cookies und bindet keine Dienste Dritter ein, die beim Seitenaufruf Daten erheben. Schriften und Bilder werden von unserem eigenen Server geladen.' },
        { t: 'h2', text: 'Was wir in Ihrem Browser speichern' },
        { t: 'table', rows: [
          ['Eintrag', 'Zweck', 'Speicherdauer'],
          ['oh-cookie-komfort', 'Ihre Auswahl in den Cookie-Einstellungen', 'bis Sie sie löschen'],
          ['oh-favoriten', 'Merkliste (Objektnummern)', 'bis Sie sie löschen'],
          ['oh-suchen', 'Gespeicherte Suchen', 'bis Sie sie löschen'],
          ['oh-hint', 'Merkt sich, dass Sie den Hinweis „Kostenlose Erstberatung“ geschlossen haben', 'bis zum Schließen des Tabs'],
        ] },
        { t: 'p', text: 'Alle Einträge liegen im Speicher Ihres Browsers (localStorage bzw. sessionStorage) und werden nicht an uns übertragen. Technisch notwendige Einträge sind nach § 25 Abs. 2 TDDDG zulässig; die Komfortfunktionen können Sie jederzeit abschalten.' },
        { t: 'h2', text: 'Externe Links' },
        { t: 'p', text: 'Links zu Google Maps, Google-Bewertungen, LinkedIn, WhatsApp sowie zu unseren Partnern öffnen die jeweiligen Anbieter in einem neuen Fenster. Erst dann gelten deren Datenschutzbestimmungen.' },
      ]} />
      <div className="rich"><div className="rich__text"><button type="button" className="btn" onClick={openCookieSettings}>Cookie-Einstellungen öffnen</button></div></div>
    </div>
  );
}

export function MeinBereich() {
  usePageMeta({ title: 'Mein Bereich', crumbs: [{ label: 'Mein Bereich' }], footer: 'accordion', noindex: true });
  const fav = useFavorites();
  const saved = useSavedSearches();
  const items = fav.ids.map(findProperty).filter((p): p is Property => !!p);
  return (
    <>
      <SectionIntro level="h1" eyebrow="Mein Bereich" title="Ihre Merkliste und gespeicherten Suchen"
        text="Alles wird nur in diesem Browser gespeichert – ohne Konto und ohne Anmeldung." />
      <section className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow="Merkliste" title={`${items.length} ${items.length === 1 ? 'gemerkte Immobilie' : 'gemerkte Immobilien'}`} />
        {items.length ? (
          <div className="expo__similar-grid">{items.map((p) => <PropertyCard key={p.id} p={p} compact />)}</div>
        ) : (
          <div className="mb-empty"><p>Noch keine Immobilien gemerkt. Tippen Sie auf das Herz in einer Objektkarte, um sie hier zu sammeln.</p><Link to={ROUTES.kaufen} className="btn">Immobilien entdecken</Link></div>
        )}
      </section>
      <section className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow="Suchaufträge" title="Gespeicherte Suchen" />
        {saved.list.length ? (
          <ul className="saved">
            {saved.list.map((s) => (
              <li key={s.id}>
                <span><Link to={s.url}>{s.label}</Link><small>gespeichert am {new Date(s.created).toLocaleDateString('de-DE')}</small></span>
                <button type="button" onClick={() => { saved.remove(s.id); notify('Suche entfernt.'); }}>Entfernen</button>
              </li>
            ))}
          </ul>
        ) : (
          <div className="mb-empty"><p>Noch keine Suche gespeichert. Nutzen Sie in der Immobiliensuche „Suche speichern“.</p><Link to={ROUTES.kaufen} className="btn">Zur Suche</Link></div>
        )}
        <p className="calc__note" style={{ marginTop: 24 }}>Sie möchten über neue Angebote informiert werden? <Link to={ROUTES.kontakt} className="link-underline">Sprechen Sie uns an</Link> – wir nehmen Ihren Suchauftrag persönlich auf. <button type="button" className="link-underline" onClick={openCookieSettings}>Cookie-Einstellungen</button></p>
      </section>
      <TeaserBand items={[TOOL_TEASERS.budget, TOOL_TEASERS.finanzierung, TOOL_TEASERS.immotipp]} />
    </>
  );
}
