/**
 * OverviewTab — role fit, what to fix (by priority), what's already good, and quick stats.
 */
import type { AnalysisReport, RoleFit } from "@/lib/types";
import { levelClasses, scoreColor } from "@/lib/score";
import { Checklist } from "./Checklist";

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
        {report.fit && report.fit.score !== null && <RoleFitCard fit={report.fit} title={report.target.title} />}

        {report.requirements && report.requirements.length > 0 && (
          <Checklist title="Job requirements" checks={report.requirements} />
        )}

        {report.ats_checks && report.ats_checks.length > 0 && (
          <Checklist title="Can an ATS read your resume?" checks={report.ats_checks} />
        )}

        {report.language_issues && report.language_issues.length > 0 && (
          <section className="rounded-3xl border border-line bg-surface p-6">
            <h2 className="mb-3 text-lg font-bold">Spelling &amp; grammar</h2>
            <ul className="flex flex-col gap-2 text-sm">
              {report.language_issues.map((issue) => (
                <li key={issue.text}>
                  <span className="text-bad-ink line-through">{issue.text}</span>
                  <span className="text-subtle"> → </span>
                  <span className="font-medium text-good-ink">{issue.fix}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

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

function RoleFitCard({ fit, title }: { fit: RoleFit; title: string }) {
  const score = fit.score ?? 0;
  return (
    <section className="rounded-3xl border border-line bg-surface p-6">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h2 className="text-lg font-bold">Fit for {title || "this role"}</h2>
        <span className="font-display text-2xl font-extrabold" style={{ color: scoreColor(score) }}>
          {score}%
        </span>
      </div>
      {fit.verdict && <p className="text-sm text-muted">{fit.verdict}</p>}
      {fit.gaps.length > 0 && (
        <ul className="mt-3 flex flex-col gap-1.5 text-sm">
          {fit.gaps.map((gap) => (
            <li key={gap} className="flex gap-2">
              <span className="text-bad-ink">✕</span>
              {gap}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
