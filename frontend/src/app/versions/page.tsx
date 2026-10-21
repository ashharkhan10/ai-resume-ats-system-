"use client";
/**
 * My versions ( /versions ): score trend, every saved check, and compare two.
 */
import Link from "next/link";
import { useEffect, useState } from "react";
import { Header } from "@/components/layout/Header";
import { ScoreTrend } from "@/components/versions/ScoreTrend";
import { VersionList } from "@/components/versions/VersionList";
import { CompareView } from "@/components/versions/CompareView";
import { deleteAnalysis, listAnalyses } from "@/lib/api";
import { useUser } from "@/lib/useUser";
import type { AnalysisSummary } from "@/lib/types";

export default function VersionsPage() {
  const { user, ready } = useUser();
  const [versions, setVersions] = useState<AnalysisSummary[] | null>(null);
  const [selected, setSelected] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    listAnalyses()
      .then(setVersions)
      .catch((e: Error) => setError(e.message));
  }, [user]);

  function toggle(id: string) {
    setSelected((old) => {
      if (old.includes(id)) return old.filter((x) => x !== id);
      return [...old, id].slice(-2); // keep at most two
    });
  }

  async function remove(id: string) {
    try {
      await deleteAnalysis(id);
      setVersions((old) => old?.filter((v) => v.id !== id) ?? null);
      setSelected((old) => old.filter((x) => x !== id));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Couldn't delete.");
    }
  }

  return (
    <>
      <Header />
      <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-6 px-4 pb-16">
        <div>
          <h1 className="font-display text-3xl font-extrabold tracking-tight md:text-4xl">My versions</h1>
          <p className="mt-2 text-muted">Every resume you check is saved here, so you can see how far you&apos;ve come.</p>
        </div>

        {!ready ? null : !user ? (
          <Message icon="🔒" text="Log in to see your saved versions." href="/login" button="Log in" />
        ) : error ? (
          <p className="rounded-xl bg-bad-soft p-4 font-medium text-bad-ink">{error}</p>
        ) : !versions ? (
          <div className="h-64 animate-pulse rounded-3xl bg-track" />
        ) : versions.length === 0 ? (
          <Message
            icon="📄"
            text="No versions yet. Check your first resume!"
            href="/analyze"
            button="Check my resume"
            showSteps
          />
        ) : (
          <>
            {versions.length > 1 && <ScoreTrend versions={versions} />}
            {selected.length === 2 && <CompareView ids={[selected[0], selected[1]]} />}
            <VersionList versions={versions} selected={selected} onToggle={toggle} onDelete={remove} />
          </>
        )}
      </main>
    </>
  );
}

const STEPS = [
  { icon: "⬆️", text: "Upload your resume" },
  { icon: "🛠️", text: "Fix what the report says" },
  { icon: "📈", text: "Upload again and compare" },
];

type MessageProps = { icon: string; text: string; href: string; button: string; showSteps?: boolean };

function Message({ icon, text, href, button, showSteps = false }: MessageProps) {
  return (
    <div className="rise relative flex flex-col items-center gap-5 overflow-hidden rounded-3xl border border-line bg-surface/90 p-10 text-center shadow-[0_30px_80px_rgb(0_0_0/0.45)] backdrop-blur">
      {/* soft glow behind the icon */}
      <div className="absolute top-0 left-1/2 h-40 w-80 -translate-x-1/2 -translate-y-1/2 rounded-full bg-brand/25 blur-3xl" />

      <span className="relative flex h-20 w-20 items-center justify-center rounded-3xl bg-brand-soft text-4xl ring-1 ring-brand/30">
        {icon}
      </span>
      <p className="relative font-display text-2xl font-extrabold">{text}</p>

      {showSteps && (
        <ol className="relative grid w-full max-w-2xl gap-3 sm:grid-cols-3">
          {STEPS.map((step, i) => (
            <li key={step.text} className="flex items-center gap-3 rounded-2xl border border-line bg-soft p-4 text-left text-sm">
              <span className="flex h-9 w-9 flex-none items-center justify-center rounded-xl bg-surface text-lg shadow-sm">
                {step.icon}
              </span>
              <span>
                <span className="block text-xs font-bold text-brand">Step {i + 1}</span>
                {step.text}
              </span>
            </li>
          ))}
        </ol>
      )}

      <Link href={href} className="btn btn-primary btn-lg relative">
        {button}
      </Link>
    </div>
  );
}
