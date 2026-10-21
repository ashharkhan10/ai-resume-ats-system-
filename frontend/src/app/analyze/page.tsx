"use client";
/**
 * Analyze page ( /analyze ): upload → wait → open the saved report at /report/<id>.
 */
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Header } from "@/components/layout/Header";
import { UploadBox } from "@/components/analyze/UploadBox";
import { TargetPicker, type TargetMode } from "@/components/analyze/TargetPicker";
import { AnalyzingSteps } from "@/components/analyze/AnalyzingSteps";
import { analyzeResume } from "@/lib/api";
import { useUser } from "@/lib/useUser";

export default function AnalyzePage() {
  const router = useRouter();
  const { user, ready } = useUser();
  const [file, setFile] = useState<File | null>(null);
  const [mode, setMode] = useState<TargetMode>("job");
  const [jobDescription, setJobDescription] = useState("");
  const [role, setRole] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleAnalyze() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeResume({
        file,
        // Only send the target from the tab that's open.
        jobDescription: mode === "job" ? jobDescription : "",
        targetRole: mode === "role" ? role : "",
      });
      router.push(`/report/${result.id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
      setLoading(false);
    }
  }

  return (
    <>
      <Header />

      <main className="mx-auto w-full max-w-5xl flex-1 px-4 pb-16">
        {loading ? (
          <AnalyzingSteps />
        ) : (
          <div className="mx-auto flex max-w-2xl flex-col gap-6">
            <div>
              <h1 className="font-display text-3xl font-extrabold tracking-tight md:text-4xl">Check your resume</h1>
              <p className="mt-2 text-muted">Two quick steps, then you get your full report.</p>
            </div>

            <section className="rounded-3xl border border-line bg-surface p-6">
              <h2 className="mb-3 font-bold">1. Upload your resume</h2>
              <UploadBox file={file} onChange={setFile} />
            </section>

            <section className="rounded-3xl border border-line bg-surface p-6">
              <h2 className="mb-3 font-bold">2. What are you applying for?</h2>
              <TargetPicker
                mode={mode}
                onModeChange={setMode}
                jobDescription={jobDescription}
                onJobDescriptionChange={setJobDescription}
                role={role}
                onRoleChange={setRole}
              />
            </section>

            {ready && !user && (
              <p className="rounded-xl bg-brand-soft p-4 text-sm text-brand-dark">
                <Link href="/login" className="font-semibold underline">
                  Log in
                </Link>{" "}
                to save every version and track your score over time.
              </p>
            )}

            {error && <p className="rounded-xl bg-bad-soft p-4 font-medium text-bad-ink">{error}</p>}

            <button onClick={handleAnalyze} disabled={!file} className="btn btn-primary btn-lg">
              Analyze my resume
            </button>
          </div>
        )}
      </main>
    </>
  );
}
