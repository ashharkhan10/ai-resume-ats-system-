/**
 * Hero — the first thing visitors see: headline, buttons and the live preview.
 */
import Link from "next/link";
import { ScorePreview } from "./ScorePreview";

export function Hero() {
  return (
    <section className="mx-auto grid w-full max-w-6xl items-center gap-12 px-4 py-16 md:grid-cols-2 md:py-24">
      <div>
        <span className="mb-5 inline-block rounded-full bg-brand-soft px-3 py-1 text-sm font-semibold text-brand">
          Free for students
        </span>
        <h1 className="font-display text-4xl font-extrabold leading-tight tracking-tight md:text-6xl">
          Get your resume past the <span className="text-brand">ATS</span> and into the interview.
        </h1>
        <p className="mt-5 max-w-lg text-lg text-muted">
          Upload your resume, paste a job or pick a role. Get a score, missing keywords, AI rewrites, interview
          questions and a cover letter in seconds.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link href="/analyze" className="btn btn-primary btn-lg">
            Check my resume
          </Link>
          <a href="#features" className="btn btn-outline btn-lg">
            See features
          </a>
        </div>
      </div>

      <div className="flex justify-center md:justify-end">
        <ScorePreview />
      </div>
    </section>
  );
}
