"use client";
/**
 * CompareView — side-by-side changes between two versions.
 */
import { useEffect, useState } from "react";
import { getAnalysis } from "@/lib/api";
import { compareReports, formatChange, type Comparison } from "@/lib/compare";

function changeColor(n: number) {
  if (n > 0) return "text-good-ink";
  if (n < 0) return "text-bad-ink";
  return "text-subtle";
}

export function CompareView({ ids }: { ids: [string, string] }) {
  const [result, setResult] = useState<Comparison | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [first, second] = ids;

  useEffect(() => {
    Promise.all([getAnalysis(first), getAnalysis(second)])
      .then(([a, b]) => setResult(compareReports(a, b)))
      .catch((e: Error) => setError(e.message));
  }, [first, second]);

  if (error) return <p className="rounded-xl bg-bad-soft p-4 text-bad-ink">{error}</p>;
  if (!result) return <div className="h-64 animate-pulse rounded-3xl bg-track" />;

  return (
    <section className="rounded-3xl border border-line bg-surface p-6">
      <div className="mb-5 flex flex-wrap items-baseline gap-3">
        <h2 className="text-lg font-bold">Older → newer</h2>
        <span className={`font-display text-3xl font-extrabold ${changeColor(result.scoreChange)}`}>
          {formatChange(result.scoreChange)} points
        </span>
      </div>

      <ul className="grid gap-2 sm:grid-cols-2">
        {result.categories.map((c) => (
          <li key={c.id} className="flex items-center justify-between rounded-xl border border-line bg-soft px-4 py-3">
            <span className="font-medium">{c.label}</span>
            <span className="text-sm">
              <span className="text-subtle">
                {c.before} → {c.after}
              </span>{" "}
              <span className={`font-bold ${changeColor(c.change)}`}>({formatChange(c.change)})</span>
            </span>
          </li>
        ))}
      </ul>

      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <IssueList title="✓ Fixed" items={result.fixedIssues} empty="Nothing fixed yet" className="text-good-ink" />
        <IssueList title="New problems" items={result.newIssues} empty="No new problems 🎉" className="text-bad-ink" />
      </div>
    </section>
  );
}

function IssueList({ title, items, empty, className }: { title: string; items: string[]; empty: string; className: string }) {
  return (
    <div>
      <p className={`mb-2 font-semibold ${className}`}>{title}</p>
      {items.length === 0 ? (
        <p className="text-sm text-subtle">{empty}</p>
      ) : (
        <ul className="flex flex-col gap-1 text-sm">
          {items.map((item) => (
            <li key={item}>• {item}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
