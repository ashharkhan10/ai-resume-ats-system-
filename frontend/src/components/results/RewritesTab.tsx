"use client";
/**
 * RewritesTab — weak bullet → stronger AI version, with a copy button.
 */
import { useState } from "react";
import type { Rewrite } from "@/lib/types";

export function RewritesTab({ rewrites }: { rewrites: Rewrite[] }) {
  if (rewrites.length === 0) {
    return <p className="rounded-3xl border border-line bg-surface p-6 text-muted">Your bullets already look strong.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="text-sm text-muted">Replace anything in [brackets] with your real numbers.</p>
      {rewrites.map((r) => (
        <RewriteCard key={r.before} rewrite={r} />
      ))}
    </div>
  );
}

function RewriteCard({ rewrite }: { rewrite: Rewrite }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    await navigator.clipboard.writeText(rewrite.after);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div className="rounded-3xl border border-line bg-surface p-6">
      <p className="text-xs font-bold uppercase tracking-wide text-bad-ink">Before</p>
      <p className="mt-1 text-muted line-through decoration-bad/40">{rewrite.before}</p>

      <p className="mt-4 text-xs font-bold uppercase tracking-wide text-good-ink">After</p>
      <p className="mt-1 font-medium">{rewrite.after}</p>

      <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm text-subtle">💡 {rewrite.why}</p>
        <button onClick={copy} className="btn btn-outline print:hidden">
          {copied ? "Copied ✓" : "Copy"}
        </button>
      </div>
    </div>
  );
}
