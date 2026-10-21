/**
 * FeatureGrid — the 6 main features as cards.
 */
const FEATURES = [
  { icon: "✍️", title: "AI bullet rewriter", text: "Turn weak bullets into strong, measurable ones." },
  { icon: "🎯", title: "Target role mode", text: "No job post? Pick from 16 roles and we check against it." },
  { icon: "💬", title: "Interview prep", text: "Questions made from your own resume and the job." },
  { icon: "✉️", title: "Cover letter", text: "A tailored cover letter in 3 tones, ready to edit." },
  { icon: "📈", title: "Version tracking", text: "Save every version and watch your score climb." },
  { icon: "🔗", title: "Shareable report", text: "Send a link to a mentor or friend for feedback." },
];

export function FeatureGrid() {
  return (
    <section id="features" className="mx-auto w-full max-w-6xl px-4 py-16">
      <h2 className="font-display text-3xl font-extrabold tracking-tight md:text-4xl">Everything in one place</h2>
      <p className="mt-2 text-muted">Plus ATS score, keyword match and clear feedback on every upload.</p>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {FEATURES.map((f) => (
          <div
            key={f.title}
            className="rounded-2xl border border-line bg-surface p-6 transition-all hover:-translate-y-1 hover:border-brand hover:shadow-[0_12px_30px_rgb(197_139_182/0.18)]"
          >
            <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-soft text-xl">
              {f.icon}
            </span>
            <h3 className="mt-4 text-lg font-bold">{f.title}</h3>
            <p className="mt-1 text-muted">{f.text}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
