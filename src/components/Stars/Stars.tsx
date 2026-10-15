import './Stars.css';

export default function Stars({ value }: { value: number }) {
  return (
    <span className="stars" aria-label={`${value.toFixed(1).replace('.', ',')} von 5 Sternen`}>
      {[0, 1, 2, 3, 4].map((i) => (
        <svg key={i} width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
          <path d="m12 2.8 2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4L2.8 9.5l6.4-.8Z" fill={value >= i + 0.75 ? '#e2b34a' : '#e6e6e6'} />
        </svg>
      ))}
    </span>
  );
}
