// Merkliste und gespeicherte Suchen – nur im Browser (localStorage), keine Übermittlung.
import { useEffect, useState } from 'react';

const EVT = 'oh-store';

function read<T>(key: string, fallback: T): T {
  try {
    const v = window.localStorage.getItem(key);
    return v ? (JSON.parse(v) as T) : fallback;
  } catch { return fallback; }
}
function write<T>(key: string, value: T) {
  try { window.localStorage.setItem(key, JSON.stringify(value)); } catch { /* privater Modus */ }
  window.dispatchEvent(new CustomEvent(EVT, { detail: key }));
}

function useStored<T>(key: string, fallback: T): [T, (v: T) => void] {
  const [value, setValue] = useState<T>(() => read(key, fallback));
  useEffect(() => {
    const sync = (e: Event) => {
      const k = e instanceof StorageEvent ? e.key : (e as CustomEvent<string>).detail;
      if (k === key) setValue(read(key, fallback));
    };
    window.addEventListener(EVT, sync);
    window.addEventListener('storage', sync);
    return () => { window.removeEventListener(EVT, sync); window.removeEventListener('storage', sync); };
  }, [key]);
  return [value, (v: T) => write(key, v)];
}

export function useFavorites() {
  const [ids, setIds] = useStored<string[]>('oh-favoriten', []);
  return {
    ids,
    has: (id: string) => ids.includes(id),
    toggle: (id: string) => {
      const on = !ids.includes(id);
      setIds(on ? [...ids, id] : ids.filter((x) => x !== id));
      return on;
    },
  };
}

export type SavedSearch = { id: string; label: string; url: string; created: string };

export function useSavedSearches() {
  const [list, setList] = useStored<SavedSearch[]>('oh-suchen', []);
  return {
    list,
    add: (label: string, url: string) => {
      if (list.some((s) => s.url === url)) return false;
      setList([{ id: String(Date.now()), label, url, created: new Date().toISOString() }, ...list]);
      return true;
    },
    remove: (id: string) => setList(list.filter((s) => s.id !== id)),
  };
}
