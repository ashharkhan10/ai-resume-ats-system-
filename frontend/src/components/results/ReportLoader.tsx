"use client";
/**
 * ReportLoader — fetches a report by id, then shows it.
 *   shared = false → /report/<id>  (your own report, all tabs)
 *   shared = true  → /share/<id>   (public, read-only)
 */
import Link from "next/link";
import { useEffect, useState } from "react";
import { getAnalysis, getSharedReport } from "@/lib/api";
import type { AnalysisReport } from "@/lib/types";
import { ResultsView } from "./ResultsView";

type Props = { id: string; shared?: boolean };

export function ReportLoader({ id, shared = false }: Props) {
  const [report, setReport] = useState<AnalysisReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = shared ? getSharedReport : getAnalysis;
    load(id)
      .then(setReport)
      .catch((e: Error) => setError(e.message));
  }, [id, shared]);

  if (error) {
    return (
      <div className="mx-auto flex max-w-md flex-col items-center gap-3 rounded-3xl border border-line bg-surface p-10 text-center">
        <span className="text-4xl">🔍</span>
        <p className="font-semibold">{error}</p>
        <p className="text-sm text-muted">If this is your report, make sure you&apos;re logged in.</p>
        <Link href="/analyze" className="btn btn-primary">
          Check a resume
        </Link>
      </div>
    );
  }

  if (!report) return <ReportSkeleton />;

  return (
    <>
      {shared && (
        <p className="mb-4 rounded-xl bg-brand-soft p-3 text-center text-sm font-medium text-brand-dark print:hidden">
          You&apos;re viewing a shared resume report.
        </p>
      )}
      <ResultsView report={report} readOnly={shared} />
    </>
  );
}

export function ReportSkeleton() {
  return (
    <div className="flex animate-pulse flex-col gap-6">
      <div className="h-64 rounded-3xl bg-track" />
      <div className="h-11 rounded-xl bg-track" />
      <div className="h-80 rounded-3xl bg-track" />
    </div>
  );
}
