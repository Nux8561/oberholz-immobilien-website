import { useEffect, useId, useMemo, useRef, useState } from 'react';
import { hero } from '../../data/content';
import { IconBuildings, IconCheck, IconChevronDown, IconChevronUp, IconClose, IconSearch, IconSparkle } from '../Icons';
import { PLACES, parseWish, WISH_EXAMPLES } from '../../lib/freeSearch';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '../../data/routes';
import './PropertySearch.css';

type Mode = (typeof hero.modes)[number];

export default function PropertySearch({ initialMode = 'Kaufen', initialQuery = '' }: { initialMode?: Mode; initialQuery?: string }) {
  const navigate = useNavigate();
  const [mode, setMode] = useState<Mode>(initialMode);
  const [type, setType] = useState('Wohnen');
  const [typeOpen, setTypeOpen] = useState(false);
  const [query, setQuery] = useState(initialQuery);
  const [suggestOpen, setSuggestOpen] = useState(false);
  const [active, setActive] = useState(-1);
  const rootRef = useRef<HTMLFormElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const listId = useId();
  const typeId = useId();

  const suggestions = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (q.length < 2) return [];
    return PLACES.filter((p) => p.toLowerCase().includes(q)).slice(0, 6);
  }, [query]);

  useEffect(() => {
    const onDown = (e: MouseEvent) => {
      if (rootRef.current && !rootRef.current.contains(e.target as Node)) { setTypeOpen(false); setSuggestOpen(false); }
    };
    document.addEventListener('mousedown', onDown);
    return () => document.removeEventListener('mousedown', onDown);
  }, []);

  const pickType = (t: string) => { setType(t); setTypeOpen(false); inputRef.current?.focus(); };
  const pickPlace = (p: string) => { setQuery(p); setSuggestOpen(false); setActive(-1); };

  const onInputKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!suggestOpen || suggestions.length === 0) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); setActive((a) => (a + 1) % suggestions.length); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setActive((a) => (a <= 0 ? suggestions.length - 1 : a - 1)); }
    else if (e.key === 'Enter' && active >= 0) { e.preventDefault(); pickPlace(suggestions[active]); }
    else if (e.key === 'Escape') { setSuggestOpen(false); }
  };

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    setSuggestOpen(false);
    const where = query.trim();
    if (mode === 'KI-Suche') { navigate(parseWish(where).url); return; }
    const params = new URLSearchParams();
    if (where) params.set('ort', where);
    if (type === 'Kapitalanlage') params.set('anlage', '1');
    else if (type !== 'Wohnen') params.set('typ', type);
    navigate(`${mode === 'Mieten' ? ROUTES.mieten : ROUTES.kaufen}${params.size ? `?${params}` : ''}`);
  };

  const isAI = mode === 'KI-Suche';

  return (
    <form className="psearch" ref={rootRef} onSubmit={submit} role="search" aria-label="Immobiliensuche">
      <fieldset className="psearch__modes">
        <legend className="sr-only">Wählen Sie eine Vermarktungsart</legend>
        {hero.modes.map((m) => (
          <label key={m} className={`psearch__mode${mode === m ? ' is-selected' : ''}`}>
            <input type="radio" name="mode" value={m} checked={mode === m} onChange={() => setMode(m)} className="sr-only" />
            {m === 'KI-Suche' && <IconSparkle size={20} />}
            <span>{m}</span>
          </label>
        ))}
      </fieldset>

      <div className={`psearch__box${typeOpen ? ' is-type-open' : ''}${suggestOpen && suggestions.length ? ' is-suggest-open' : ''}`}>
        {!isAI && (
          <div className="psearch__type">
            <button type="button" className="psearch__type-btn" aria-label="Dropdown-Menü für Objektarten" aria-haspopup="listbox"
              aria-expanded={typeOpen} aria-controls={typeId} onClick={() => { setTypeOpen((o) => !o); setSuggestOpen(false); }}>
              <IconBuildings />
              {typeOpen ? <IconChevronUp /> : <IconChevronDown />}
            </button>
            {typeOpen && (
              <ul className="psearch__types" role="listbox" id={typeId} aria-label="Objektart">
                {hero.propertyTypes.map((g) => (
                  <li key={g.group} className="psearch__group">
                    <button type="button" role="option" aria-selected={type === g.group}
                      className={`psearch__opt psearch__opt--group${type === g.group ? ' is-selected' : ''}`} onClick={() => pickType(g.group)}>
                      {g.group}{type === g.group && <IconCheck />}
                    </button>
                    {g.options.length > 0 && (
                      <ul>
                        {g.options.map((o) => (
                          <li key={o}>
                            <button type="button" role="option" aria-selected={type === o}
                              className={`psearch__opt${type === o ? ' is-selected' : ''}`} onClick={() => pickType(o)}>
                              {o}{type === o && <IconCheck />}
                            </button>
                          </li>
                        ))}
                      </ul>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
        <div className={`psearch__field${query ? ' has-value' : ''}`}>
          <input
            ref={inputRef}
            className="psearch__input"
            type="text"
            value={query}
            placeholder={isAI ? 'z. B. 3-Zimmer-Wohnung in Essen bis 300.000 €' : hero.placeholder}
            aria-label={isAI ? 'KI-Suche' : 'Standort'}
            role="combobox"
            aria-expanded={suggestOpen && suggestions.length > 0}
            aria-controls={listId}
            aria-autocomplete="list"
            aria-activedescendant={active >= 0 ? `${listId}-${active}` : undefined}
            autoComplete="off"
            onChange={(e) => { setQuery(e.target.value); setSuggestOpen(true); setActive(-1); setTypeOpen(false); }}
            onFocus={() => setSuggestOpen(true)}
            onKeyDown={onInputKey}
          />
          {query && (
            <button type="button" className="psearch__clear" aria-label="Eingabe löschen" onClick={() => { setQuery(''); inputRef.current?.focus(); }}>
              <IconClose size={20} />
            </button>
          )}
          {suggestOpen && suggestions.length > 0 && !isAI && (
            <ul className="psearch__suggest" role="listbox" id={listId}>
              {suggestions.map((s, i) => (
                <li key={s} id={`${listId}-${i}`} role="option" aria-selected={i === active}
                  className={i === active ? 'is-active' : ''} onMouseDown={(e) => { e.preventDefault(); pickPlace(s); }}>
                  {s}
                </li>
              ))}
            </ul>
          )}
        </div>
        <button type="submit" className="psearch__submit" aria-label="Suchen"><IconSearch /></button>
      </div>
      {isAI && (
        <div className="psearch__examples">
          <span>Zum Beispiel:</span>
          {WISH_EXAMPLES.map((ex) => <button key={ex} type="button" onClick={() => navigate(parseWish(ex).url)}>{ex}</button>)}
        </div>
      )}
    </form>
  );
}
