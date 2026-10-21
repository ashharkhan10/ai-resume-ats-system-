"use client";
/**
 * InterviewTab — likely interview questions made from this resume.
 * Click a question to see why they ask it and how to answer.
 */
import { useState } from "react";
import { getInterviewPrep } from "@/lib/api";
import type { InterviewQuestion } from "@/lib/types";

const TYPE_COLORS: Record<string, string> = {
  Technical: "bg-brand-soft text-brand-dark",
  Project: "bg-good-soft text-good-ink",
  Behavioral: "bg-warn-soft text-warn-ink",
  HR: "bg-tab text-muted",
};

export function InterviewTab({ analysisId }: { analysisId: string }) {
  const [questions, setQuestions] = useState<InterviewQuestion[] | null>(null);
  const [open, setOpen] = useState<number | null>(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load(fresh: boolean) {
    setLoading(true);
    setError(null);
    try {
      const prep = await getInterviewPrep(analysisId, fresh);
      setQuestions(prep.questions);
      setOpen(0);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  if (!questions) {
    return (
      <div className="flex flex-col items-center gap-3 rounded-3xl border border-line bg-surface p-10 text-center">
        <span className="text-4xl">💬</span>
        <h2 className="text-lg font-bold">Practice the questions you&apos;ll actually get</h2>
        <p className="max-w-md text-muted">Made from your projects, your skills and the job — with tips for each one.</p>
        {error && <p className="text-sm font-medium text-bad-ink">{error}</p>}
        <button onClick={() => load(false)} disabled={loading} className="btn btn-primary">
          {loading ? "Thinking…" : "Generate questions"}
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {questions.map((q, i) => (
        <div key={q.question} className="rounded-2xl border border-line bg-surface">
          <button
            onClick={() => setOpen(open === i ? null : i)}
            className="flex w-full items-start gap-3 p-5 text-left transition-colors hover:bg-soft"
          >
            <span className={`mt-0.5 rounded-full px-2.5 py-0.5 text-xs font-bold ${TYPE_COLORS[q.type] ?? TYPE_COLORS.HR}`}>
              {q.type}
            </span>
            <span className="flex-1 font-semibold">{q.question}</span>
            <span className={`text-subtle transition-transform ${open === i ? "rotate-180" : ""}`}>▾</span>
          </button>
          {open === i && (
            <div className="flex flex-col gap-2 border-t border-line px-5 py-4 text-sm">
              <p>
                <span className="font-semibold">Why they ask: </span>
                <span className="text-muted">{q.why}</span>
              </p>
              <p>
                <span className="font-semibold">💡 How to answer: </span>
                <span className="text-muted">{q.tip}</span>
              </p>
            </div>
          )}
        </div>
      ))}
      {error && <p className="text-sm font-medium text-bad-ink">{error}</p>}
      <button onClick={() => load(true)} disabled={loading} className="btn btn-outline self-center">
        {loading ? "Thinking…" : "New questions"}
      </button>
    </div>
  );
}
