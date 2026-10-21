/**
 * ScoreRing — a circular score (0–100) with the number in the middle.
 * The ring animates when the score changes.
 */
type Props = {
  score: number;
  size?: number;
  color?: string; // CSS colour, defaults to the brand blue
  label?: string;
};

export function ScoreRing({ score, size = 168, color = "var(--color-brand)", label = "out of 100" }: Props) {
  const stroke = size * 0.095;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const filled = (Math.max(0, Math.min(100, score)) / 100) * circumference;
  const center = size / 2;

  return (
    <div className="relative flex-none" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
        <circle cx={center} cy={center} r={radius} stroke="var(--color-track)" strokeWidth={stroke} fill="none" />
        <circle
          cx={center}
          cy={center}
          r={radius}
          stroke={color}
          strokeWidth={stroke}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={`${filled} ${circumference}`}
          transform={`rotate(-90 ${center} ${center})`}
          className="transition-[stroke-dasharray,stroke] duration-500"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-display font-extrabold leading-none" style={{ fontSize: size * 0.32 }}>
          {score}
        </span>
        <span className="text-sm text-subtle">{label}</span>
      </div>
    </div>
  );
}
