"use client";
/**
 * ResultsView — the full report: score card, action buttons, then tabs.
 *
 * readOnly = true on public share links (no AI tabs, no share button).
 * "Download PDF" opens the browser's print dialog → "Save as PDF".
 * When printing, every section is shown one after another instead of tabs.
 */
import Link from "next/link";
import { useState } from "react";
import type { AnalysisReport } from "@/lib/types";
import { ScoreRing } from "@/components/ui/ScoreRing";
import { ScoreBar } from "@/components/ui/ScoreBar";
import { scoreColor } from "@/lib/score";
import { OverviewTab } from "./OverviewTab";
import { KeywordsTab } from "./KeywordsTab";
import { RewritesTab } from "./RewritesTab";
import { InterviewTab } from "./InterviewTab";
import { CoverLetterTab } from "./CoverLetterTab";
import { ShareButton } from "./ShareButton";

const TABS = [
  { id: "overview", label: "Overview", ai: false },
  { id: "keywords", label: "Keywords", ai: false },
  { id: "rewrites", label: "AI rewrites", ai: false },
  { id: "interview", label: "Interview prep", ai: true },
  { id: "cover", label: "Cover letter", ai: true },
] as const;

type TabId = (typeof TABS)[number]["id"];

type Props = {
  report: AnalysisReport;
  readOnly?: boolean;
};

export function ResultsView({ report, readOnly = false }: Props) {
  const [tab, setTab] = useState<TabId>("overview");
  const color = scoreColor(report.score);
  const tabs = TABS.filter((t) => !readOnly || !t.ai);

  return (
    <div className="flex flex-col gap-6">
      {/* Score card */}
      <section className="grid gap-8 rounded-3xl border border-line bg-surface p-6 md:grid-cols-[auto_1fr] md:p-8">
        <div className="flex flex-col items-center gap-3">
          <ScoreRing score={report.score} color={color} />
          <span className="rounded-full px-3 py-1 text-sm font-bold text-[#140f13]" style={{ background: color }}>
            {report.rating}
          </span>
          {report.band && <span className="text-center text-sm font-semibold text-muted">{report.band}</span>}
        </div>

        <div className="flex flex-col gap-4">
          <div>
            <p className="text-sm text-subtle">
              {report.file_name}
              {report.created_at && ` · ${new Date(report.created_at).toLocaleDateString()}`}
            </p>
            {report.target.title && (
              <p className="text-sm font-semibold text-brand">
                {report.target.kind === "job" ? "Job: " : "Role: "}
                {report.target.title}
              </p>
            )}
            <h1 className="font-display text-2xl font-extrabold md:text-3xl">{report.summary}</h1>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {report.categories.map((c) => (
              <ScoreBar key={c.id} label={c.label} value={c.score} color={scoreColor(c.score)} />
            ))}
          </div>
        </div>
      </section>

      {/* Actions */}
      <div className="flex flex-wrap gap-2 print:hidden">
        {!readOnly && <ShareButton analysisId={report.id} />}
        <button onClick={() => window.print()} className="btn btn-outline">
          ⬇ Download PDF
        </button>
        <Link href="/analyze" className="btn btn-primary sm:ml-auto">
          {readOnly ? "Check your own resume" : "Check another version"}
        </Link>
      </div>

      {/* Tabs (screen only) */}
      <div className="flex flex-col gap-6 print:hidden">
        <div className="flex gap-1 overflow-x-auto rounded-xl bg-tab p-1">
          {tabs.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`flex-1 whitespace-nowrap rounded-lg px-4 py-2 text-sm font-semibold transition-all active:scale-95 ${
                tab === t.id ? "bg-surface text-ink shadow-sm" : "text-subtle hover:text-ink"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "overview" && <OverviewTab report={report} />}
        {tab === "keywords" && <KeywordsTab report={report} />}
        {tab === "rewrites" && <RewritesTab rewrites={report.rewrites} />}
        {tab === "interview" && <InterviewTab analysisId={report.id} />}
        {tab === "cover" && <CoverLetterTab analysisId={report.id} />}
      </div>

      {/* Everything at once (print / PDF only) */}
      <div className="hidden flex-col gap-6 print:flex">
        <OverviewTab report={report} />
        <KeywordsTab report={report} />
        <RewritesTab rewrites={report.rewrites} />
      </div>
    </div>
  );
}
