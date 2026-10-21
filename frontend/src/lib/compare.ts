/**
 * Compares two versions of a resume report: what went up, what went down,
 * which problems got fixed and which are new.
 */
import type { AnalysisReport } from "./types";

export type CategoryChange = { id: string; label: string; before: number; after: number; change: number };

export type Comparison = {
  scoreChange: number;
  categories: CategoryChange[];
  fixedIssues: string[]; // titles
  newIssues: string[];
};

/** "older" and "newer" are put in date order automatically. */
export function compareReports(a: AnalysisReport, b: AnalysisReport): Comparison {
  const [older, newer] = a.created_at <= b.created_at ? [a, b] : [b, a];

  const categories = newer.categories.map((cat) => {
    const before = older.categories.find((c) => c.id === cat.id)?.score ?? 0;
    return { id: cat.id, label: cat.label, before, after: cat.score, change: cat.score - before };
  });

  const olderIds = new Set(older.issues.map((i) => i.id));
  const newerIds = new Set(newer.issues.map((i) => i.id));

  return {
    scoreChange: newer.score - older.score,
    categories,
    fixedIssues: older.issues.filter((i) => !newerIds.has(i.id)).map((i) => i.title),
    newIssues: newer.issues.filter((i) => !olderIds.has(i.id)).map((i) => i.title),
  };
}

/** "+12", "-3" or "0" */
export function formatChange(n: number): string {
  return n > 0 ? `+${n}` : `${n}`;
}
