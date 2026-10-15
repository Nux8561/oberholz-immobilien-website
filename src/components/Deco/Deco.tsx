import './Deco.css';

// Dekor: vertikale Stäbe mit wellenförmig variierender Höhe (eigene Grafik, Fläche 2828×250 wie Referenz)
const BARS = Array.from({ length: 124 }, (_, i) => ({ x: 11 + i * 22.8, top: 34 + 26 * Math.sin(i / 7.2) + 10 * Math.sin(i / 2.3) }));

export default function Deco({ className = '' }: { className?: string }) {
  return (
    <div className="deco-wrap" aria-hidden="true">
    <svg className={`deco ${className}`} viewBox="0 0 2828 250" preserveAspectRatio="xMidYMax slice">
      {BARS.map(({ x, top }) => (
        <g key={x}>
          <rect x={x} y={top} width="2" height={250 - top} fill="#d9d6cf" />
          <rect x={x - 1} y={top + 82} width="4" height={58} fill="#cdcac3" />
          <rect x={x - 1} y={top + 146} width="4" height={250} fill="#cdcac3" />
        </g>
      ))}
    </svg>
    </div>
  );
}
