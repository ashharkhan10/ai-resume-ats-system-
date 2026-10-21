/**
 * KeywordsTab — matched vs missing keywords, and which skills have proof.
 */
import type { AnalysisReport } from "@/lib/types";

export function KeywordsTab({ report }: { report: AnalysisReport }) {
  const { keywords, skills } = report;
  const listedOnly = keywords?.listed_only ?? [];
  const used = (keywords?.matched ?? []).filter((k) => !listedOnly.includes(k));

  return (
    <div className="flex flex-col gap-6">
      <section className="rounded-3xl border border-line bg-surface p-6">
        {keywords ? (
          <>
            <h2 className="text-lg font-bold">Job match: {keywords.match_pct}%</h2>
            <p className="mb-4 text-sm text-muted">Add the missing ones — only if you really have them.</p>
            <ChipGroup title={`Missing (${keywords.missing.length})`} items={keywords.missing} className="bg-bad-soft text-bad-ink" />
            <ChipGroup
              title={`Used in your work (${used.length})`}
              items={used}
              className="bg-good-soft text-good-ink"
            />
            <ChipGroup
              title={`Only listed — not shown in a recent project or job (${listedOnly.length})`}
              items={listedOnly}
              className="bg-warn-soft text-warn-ink"
            />
          </>
        ) : (
          <p className="text-muted">
            Add a job description or pick a role to see which keywords you&apos;re missing.
          </p>
        )}
      </section>

      <section className="rounded-3xl border border-line bg-surface p-6">
        <h2 className="text-lg font-bold">Skill proof</h2>
        <p className="mb-4 text-sm text-muted">Recruiters trust skills you&apos;ve actually used in a project or job.</p>
        <ul className="grid gap-2 sm:grid-cols-2">
          {skills.map((s) => (
            <li key={s.name} className="flex items-center justify-between gap-3 rounded-xl border border-line bg-soft px-4 py-2.5 text-sm">
              <span className="font-medium">{s.name}</span>
              {s.proof ? (
                <span className="truncate text-good-ink">✓ {s.proof}</span>
              ) : (
                <span className="text-warn-ink">No proof yet</span>
              )}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

function ChipGroup({ title, items, className }: { title: string; items: string[]; className: string }) {
  if (items.length === 0) return null;
  return (
    <div className="mb-4">
      <p className="mb-2 text-sm font-semibold text-subtle">{title}</p>
      <div className="flex flex-wrap gap-2">
        {items.map((item) => (
          <span key={item} className={`rounded-full px-3 py-1 text-sm font-medium ${className}`}>
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}
