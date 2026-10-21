/**
 * ScoreBar — a label, a percentage and a thin bar that fills up.
 */
type Props = {
  label: string;
  value: number; // 0–100
  color?: string;
};

export function ScoreBar({ label, value, color = "var(--color-brand)" }: Props) {
  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex justify-between text-sm">
        <span className="text-muted">{label}</span>
        <span className="font-semibold">{value}%</span>
      </div>
      <div className="h-2 rounded bg-track">
        <div
          className="h-2 rounded transition-[width] duration-500"
          style={{ width: `${Math.max(0, Math.min(100, value))}%`, background: color }}
        />
      </div>
    </div>
  );
}
