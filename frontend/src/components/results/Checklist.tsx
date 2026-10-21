/**
 * Checklist — a list of passed / failed checks with a short explanation each.
 * Checks that couldn't run (ok = null) are hidden.
 */
import type { Check } from "@/lib/types";

export function Checklist({ title, checks }: { title: string; checks: Check[] }) {
  const shown = checks.filter((c) => c.ok !== null);
  if (shown.length === 0) return null;
  const passed = shown.filter((c) => c.ok).length;

  return (
    <section className="rounded-3xl border border-line bg-surface p-6">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h2 className="text-lg font-bold">{title}</h2>
        <span className="text-sm font-semibold text-subtle">
          {passed}/{shown.length}
        </span>
      </div>
      <ul className="flex flex-col gap-2.5">
        {shown.map((check) => (
          <li key={check.id} className="flex gap-2.5 text-sm">
            <span
              className={`mt-0.5 flex h-5 w-5 flex-none items-center justify-center rounded-full text-xs font-bold ${
                check.ok ? "bg-good-soft text-good-ink" : "bg-bad-soft text-bad-ink"
              }`}
            >
              {check.ok ? "✓" : "✕"}
            </span>
            <span>
              <span className="font-medium">{check.label}</span>
              {check.detail && <span className="block text-subtle">{check.detail}</span>}
            </span>
          </li>
        ))}
      </ul>
    </section>
  );
}
