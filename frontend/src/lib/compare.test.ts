import { describe, expect, it } from "vitest";
import { compareReports, formatChange } from "./compare";
import type { AnalysisReport } from "./types";

function report(score: number, date: string, issueIds: string[], content: number): AnalysisReport {
  return {
    score,
    created_at: date,
    categories: [{ id: "content", label: "Content", score: content, weight: 25 }],
    issues: issueIds.map((id) => ({ id, level: "High", title: `Issue ${id}`, detail: "" })),
  } as AnalysisReport;
}

describe("compareReports", () => {
  const v1 = report(58, "2026-10-01", ["no_numbers", "weak_verbs"], 40);
  const v2 = report(74, "2026-10-05", ["weak_verbs", "too_long"], 70);

  it("works out the changes from old to new", () => {
    const result = compareReports(v1, v2);
    expect(result.scoreChange).toBe(16);
    expect(result.categories[0]).toMatchObject({ before: 40, after: 70, change: 30 });
    expect(result.fixedIssues).toEqual(["Issue no_numbers"]);
    expect(result.newIssues).toEqual(["Issue too_long"]);
  });

  it("puts the versions in date order whatever order they're passed in", () => {
    expect(compareReports(v2, v1).scoreChange).toBe(16);
  });
});

describe("formatChange", () => {
  it("adds a plus sign to gains", () => {
    expect(formatChange(5)).toBe("+5");
    expect(formatChange(-3)).toBe("-3");
    expect(formatChange(0)).toBe("0");
  });
});
