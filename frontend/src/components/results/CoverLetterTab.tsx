"use client";
/**
 * CoverLetterTab — pick a tone, generate, edit and copy.
 */
import { useState } from "react";
import { getCoverLetter } from "@/lib/api";
import type { Tone } from "@/lib/types";

const TONES: { id: Tone; label: string }[] = [
  { id: "professional", label: "Professional" },
  { id: "friendly", label: "Friendly" },
  { id: "confident", label: "Confident" },
];

export function CoverLetterTab({ analysisId }: { analysisId: string }) {
  const [tone, setTone] = useState<Tone>("professional");
  const [letters, setLetters] = useState<Partial<Record<Tone, string>>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const text = letters[tone];

  async function generate(fresh: boolean) {
    setLoading(true);
    setError(null);
    try {
      const letter = await getCoverLetter(analysisId, tone, fresh);
      setLetters((old) => ({ ...old, [tone]: letter.text }));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  async function copy() {
    if (!text) return;
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div className="flex flex-col gap-4 rounded-3xl border border-line bg-surface p-6">
      <div className="flex flex-wrap items-center gap-2">
        <span className="mr-1 text-sm font-semibold text-subtle">Tone:</span>
        {TONES.map((t) => (
          <button
            key={t.id}
            onClick={() => setTone(t.id)}
            className={`rounded-full border px-4 py-1.5 text-sm font-medium transition-all hover:-translate-y-0.5 active:scale-95 ${
              tone === t.id ? "border-brand bg-brand-soft text-brand-dark" : "border-line-strong bg-surface hover:border-brand"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {text ? (
        <>
          <textarea
            value={text}
            onChange={(e) => setLetters((old) => ({ ...old, [tone]: e.target.value }))}
            rows={16}
            className="w-full rounded-2xl border border-line-strong bg-soft p-4 leading-relaxed outline-none focus:border-brand focus:ring-4 focus:ring-brand-soft"
          />
          <p className="text-sm text-subtle">Edit anything above. Replace [brackets] with real details.</p>
          <div className="flex flex-wrap gap-2">
            <button onClick={copy} className="btn btn-primary">
              {copied ? "Copied ✓" : "Copy letter"}
            </button>
            <button onClick={() => generate(true)} disabled={loading} className="btn btn-outline">
              {loading ? "Writing…" : "Write a new one"}
            </button>
          </div>
        </>
      ) : (
        <div className="flex flex-col items-center gap-3 py-8 text-center">
          <span className="text-4xl">✉️</span>
          <p className="max-w-md text-muted">A tailored cover letter using only what&apos;s really in your resume.</p>
          <button onClick={() => generate(false)} disabled={loading} className="btn btn-primary">
            {loading ? "Writing…" : "Write my cover letter"}
          </button>
        </div>
      )}
      {error && <p className="text-sm font-medium text-bad-ink">{error}</p>}
    </div>
  );
}
