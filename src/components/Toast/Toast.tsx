import { useEffect, useState } from 'react';
import './Toast.css';

// Kurze Rückmeldungen (Merkliste, gespeicherte Suche, Teilen).
type Listener = (msg: string) => void;
const listeners = new Set<Listener>();
export const notify = (msg: string) => listeners.forEach((l) => l(msg));

export default function Toast() {
  const [msg, setMsg] = useState<string | null>(null);
  useEffect(() => {
    let t: number;
    const l: Listener = (m) => { setMsg(m); window.clearTimeout(t); t = window.setTimeout(() => setMsg(null), 3600); };
    listeners.add(l);
    return () => { listeners.delete(l); window.clearTimeout(t); };
  }, []);
  return (
    <div className={`toast${msg ? ' is-visible' : ''}`} role="status" aria-live="polite">
      {msg}
    </div>
  );
}
