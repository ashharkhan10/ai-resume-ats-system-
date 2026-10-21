"use client";
/**
 * ScorePreview — the interactive card in the hero.
 * Click "Before" / "After" to see how the AI rewrite lifts the score.
 */
import { useState } from "react";
import { ScoreRing } from "@/components/ui/ScoreRing";
import { ScoreBar } from "@/components/ui/ScoreBar";

const VERSIONS = {
  before: {
    score: 58,
    color: "var(--color-warn)",
    bars: [
      { label: "Keywords", value: 52 },
      { label: "Content", value: 48 },
      { label: "Formatting", value: 80 },
    ],
    bullet: "Worked on the college website using React.",
  },
  after: {
    score: 84,
    color: "var(--color-good)",
    bars: [
      { label: "Keywords", value: 86 },
      { label: "Content", value: 82 },
      { label: "Formatting", value: 90 },
    ],
    bullet: "Built the college fest website in React, serving 3,000+ students with 40% faster page loads.",
  },
};

type Version = keyof typeof VERSIONS;

export function ScorePreview() {
  const [version, setVersion] = useState<Version>("before");
  const v = VERSIONS[version];

  return (
    <div className="w-full max-w-md rounded-3xl border border-line bg-surface p-6 shadow-[0_30px_80px_rgb(0_0_0/0.45)]">
      {/* Before / After switch */}
      <div className="mb-6 flex rounded-xl bg-tab p-1">
        {(["before", "after"] as Version[]).map((key) => (
          <button
            key={key}
            onClick={() => setVersion(key)}
            className={`flex-1 rounded-lg py-2 text-sm font-semibold capitalize transition-all active:scale-95 ${
              version === key ? "bg-surface text-ink shadow-sm" : "text-subtle hover:text-ink"
            }`}
          >
            {key === "before" ? "Before" : "After AI rewrite"}
          </button>
        ))}
      </div>

      <div className="flex items-center gap-6">
        <ScoreRing score={v.score} size={128} color={v.color} />
        <div className="flex flex-1 flex-col gap-3">
          {v.bars.map((bar) => (
            <ScoreBar key={bar.label} label={bar.label} value={bar.value} color={v.color} />
          ))}
        </div>
      </div>

      <div className="mt-6 rounded-xl border border-line bg-soft p-4">
        <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-subtle">Example bullet</p>
        <p className="text-sm leading-relaxed">{v.bullet}</p>
      </div>
    </div>
  );
}
