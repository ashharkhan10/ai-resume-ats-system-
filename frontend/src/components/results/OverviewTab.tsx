/**
 * OverviewTab — what to fix (by priority), what's already good, and quick stats.
 */
import type { AnalysisReport } from "@/lib/types";
import { levelClasses } from "@/lib/score";

export function OverviewTab({ report }: { report: AnalysisReport }) {
  const { issues, strengths, stats } = report;

  return (
    <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
      <section className="rounded-3xl border border-line bg-surface p-6">
        <h2 className="mb-4 text-lg font-bold">What to fix</h2>
        {issues.length === 0 ? (
          <p className="text-muted">No problems found. Nice work! 🎉</p>
        ) : (
          <ul className="flex flex-col gap-3">
            {issues.map((issue) => (
              <li key={issue.id} className="rounded-2xl border border-line bg-soft p-4">
                <div className="flex items-center gap-2">
                  <span className={`rounded-full px-2.5 py-0.5 text-xs font-bold ${levelClasses(issue.level)}`}>
                    {issue.level}
                  </span>
                  <span className="font-semibold">{issue.title}</span>
                </div>
                <p className="mt-1.5 text-sm text-muted">{issue.detail}</p>
              </li>
            ))}
          </ul>
        )}
      </section>

      <div className="flex flex-col gap-6">
        {strengths.length > 0 && (
          <section className="rounded-3xl border border-line bg-surface p-6">
            <h2 className="mb-3 text-lg font-bold">What&apos;s working</h2>
            <ul className="flex flex-col gap-2">
              {strengths.map((s) => (
                <li key={s} className="flex gap-2 text-sm">
                  <span className="text-good">✓</span>
                  {s}
                </li>
              ))}
            </ul>
          </section>
        )}

        <section className="grid grid-cols-3 gap-3 rounded-3xl border border-line bg-surface p-6 text-center">
          <Stat value={stats.word_count} label="words" />
          <Stat value={stats.bullets} label="bullets" />
          <Stat value={stats.quantified_bullets} label="with numbers" />
        </section>
      </div>
    </div>
  );
}

function Stat({ value, label }: { value: number; label: string }) {
  return (
    <div>
      <p className="font-display text-2xl font-extrabold">{value}</p>
      <p className="text-xs text-subtle">{label}</p>
    </div>
  );
}
