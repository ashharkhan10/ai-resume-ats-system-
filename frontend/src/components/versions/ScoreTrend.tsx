/**
 * ScoreTrend — a simple line chart of your score, oldest version → newest.
 */
import type { AnalysisSummary } from "@/lib/types";

const WIDTH = 640;
const HEIGHT = 200;
const PAD = 32;

export function ScoreTrend({ versions }: { versions: AnalysisSummary[] }) {
  // The list comes newest first; the chart reads left (old) → right (new).
  const points = [...versions].reverse().map((v, i, all) => ({
    x: all.length === 1 ? WIDTH / 2 : PAD + (i * (WIDTH - PAD * 2)) / (all.length - 1),
    y: HEIGHT - PAD - (v.score / 100) * (HEIGHT - PAD * 2),
    score: v.score,
    label: `v${i + 1}`,
  }));
  const line = points.map((p) => `${p.x},${p.y}`).join(" ");

  return (
    <section className="rounded-3xl border border-line bg-surface p-6">
      <h2 className="mb-2 text-lg font-bold">Your score over time</h2>
      <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="h-auto w-full" role="img" aria-label="Score trend chart">
        {/* guide lines at 50 and 100 */}
        {[50, 100].map((value) => {
          const y = HEIGHT - PAD - (value / 100) * (HEIGHT - PAD * 2);
          return (
            <g key={value}>
              <line x1={PAD} x2={WIDTH - PAD} y1={y} y2={y} stroke="var(--color-line)" strokeDasharray="4 4" />
              <text x={4} y={y + 4} fontSize="11" fill="var(--color-subtle)">
                {value}
              </text>
            </g>
          );
        })}
        <polyline points={line} fill="none" stroke="var(--color-brand)" strokeWidth="3" strokeLinejoin="round" />
        {points.map((p) => (
          <g key={p.label}>
            <circle cx={p.x} cy={p.y} r="6" fill="var(--color-surface)" stroke="var(--color-brand)" strokeWidth="3" />
            <text x={p.x} y={p.y - 12} textAnchor="middle" fontSize="12" fontWeight="700" fill="var(--color-ink)">
              {p.score}
            </text>
            <text x={p.x} y={HEIGHT - 8} textAnchor="middle" fontSize="11" fill="var(--color-subtle)">
              {p.label}
            </text>
          </g>
        ))}
      </svg>
    </section>
  );
}
