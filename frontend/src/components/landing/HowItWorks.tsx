/**
 * HowItWorks — 3 simple steps and a final call to action.
 */
import Link from "next/link";

const STEPS = [
  { title: "Upload", text: "Drop your resume as PDF or DOCX." },
  { title: "Choose a target", text: "Paste a job description or pick a role." },
  { title: "Improve", text: "Fix the issues, use the rewrites, check again." },
];

export function HowItWorks() {
  return (
    <section className="mx-auto w-full max-w-6xl px-4 py-16">
      <h2 className="font-display text-3xl font-extrabold tracking-tight md:text-4xl">How it works</h2>

      <ol className="mt-8 grid gap-4 md:grid-cols-3">
        {STEPS.map((step, i) => (
          <li key={step.title} className="rounded-2xl border border-line bg-surface p-6">
            <span className="font-display text-4xl font-extrabold text-brand">{i + 1}</span>
            <h3 className="mt-2 text-lg font-bold">{step.title}</h3>
            <p className="mt-1 text-muted">{step.text}</p>
          </li>
        ))}
      </ol>

      <div className="mt-12 flex flex-col items-center gap-4 glow-card rounded-3xl px-6 py-14 text-center">
        <h2 className="font-display text-3xl font-extrabold">Ready to see your score?</h2>
        <p className="text-muted">It takes less than a minute.</p>
        <Link href="/analyze" className="btn btn-primary btn-lg">
          Check my resume
        </Link>
      </div>
    </section>
  );
}
