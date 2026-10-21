"use client";
/**
 * VersionList — every saved check. Tick two to compare them.
 */
import Link from "next/link";
import { useState } from "react";
import type { AnalysisSummary } from "@/lib/types";
import { scoreColor } from "@/lib/score";

type Props = {
  versions: AnalysisSummary[];
  selected: string[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
};

export function VersionList({ versions, selected, onToggle, onDelete }: Props) {
  const [confirming, setConfirming] = useState<string | null>(null);

  return (
    <section className="rounded-3xl border border-line bg-surface p-6">
      <h2 className="text-lg font-bold">All versions</h2>
      <p className="mb-4 text-sm text-muted">Tick any two to compare them.</p>

      <ul className="flex flex-col gap-2">
        {versions.map((v, i) => {
          const checked = selected.includes(v.id);
          return (
            <li
              key={v.id}
              className={`flex flex-wrap items-center gap-3 rounded-2xl border p-3 transition-colors ${
                checked ? "border-brand bg-brand-soft" : "border-line bg-soft"
              }`}
            >
              <input
                type="checkbox"
                checked={checked}
                onChange={() => onToggle(v.id)}
                aria-label={`Select version ${versions.length - i}`}
                className="h-5 w-5 accent-[var(--color-brand)]"
              />
              <span
                className="flex h-11 w-11 items-center justify-center rounded-xl font-display font-extrabold text-[#140f13]"
                style={{ background: scoreColor(v.score) }}
              >
                {v.score}
              </span>
              <div className="min-w-0 flex-1">
                <p className="truncate font-semibold">
                  v{versions.length - i} · {v.file_name}
                </p>
                <p className="truncate text-sm text-subtle">
                  {v.target_title || "No target"} · {new Date(v.created_at).toLocaleDateString()}
                </p>
              </div>
              <Link href={`/report/${v.id}`} className="btn btn-outline">
                Open
              </Link>
              <button
                onClick={() => {
                  if (confirming === v.id) onDelete(v.id);
                  else setConfirming(v.id);
                }}
                onBlur={() => setConfirming(null)}
                className={`btn ${confirming === v.id ? "bg-bad text-white" : "btn-ghost"}`}
              >
                {confirming === v.id ? "Sure?" : "Delete"}
              </button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
