"use client";
/**
 * AnalyzingSteps — the animated checklist shown while we wait for the backend.
 * Each step ticks after a short delay; the last one stays "in progress" until the result arrives.
 */
import { useEffect, useState } from "react";

const STEPS = ["Reading your resume", "Finding your skills", "Matching keywords", "Writing suggestions"];

export function AnalyzingSteps() {
  const [done, setDone] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setDone((n) => Math.min(n + 1, STEPS.length - 1)), 1800);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="mx-auto flex max-w-md flex-col gap-3 rounded-3xl border border-line bg-surface p-8">
      <h2 className="font-display text-2xl font-extrabold">Checking your resume…</h2>
      <p className="mb-2 text-muted">This takes about 10 seconds.</p>
      {STEPS.map((step, i) => (
        <div key={step} className="flex items-center gap-3">
          {i < done ? (
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-good text-sm text-[#140f13]">✓</span>
          ) : i === done ? (
            <span className="h-6 w-6 animate-spin rounded-full border-[3px] border-brand-soft border-t-brand" />
          ) : (
            <span className="h-6 w-6 rounded-full border-2 border-line-strong" />
          )}
          <span className={i <= done ? "font-medium" : "text-subtle"}>{step}</span>
        </div>
      ))}
    </div>
  );
}
