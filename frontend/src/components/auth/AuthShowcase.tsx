/**
 * AuthShowcase — the glowing panel next to the login / sign-up form.
 * Shows what you get, with a small score card that "jumps" from 58 to 84.
 */
import { ScoreRing } from "@/components/ui/ScoreRing";

const PERKS = [
  "Save every version of your resume",
  "Watch your ATS score climb over time",
  "Interview questions and cover letters, saved",
];

export function AuthShowcase() {
  return (
    <div className="glow-card hidden rounded-3xl p-10 lg:flex lg:flex-col lg:justify-between">
      <div className="relative">
        <h2 className="font-display text-4xl leading-tight font-extrabold">
          Beat the ATS.
          <br />
          <span className="text-brand-dark">Land the interview.</span>
        </h2>
        <ul className="mt-6 flex flex-col gap-3 text-muted">
          {PERKS.map((perk) => (
            <li key={perk} className="flex items-center gap-3">
              <span className="flex h-6 w-6 flex-none items-center justify-center rounded-full bg-brand-soft text-sm font-bold text-brand-dark ring-1 ring-brand/30">
                ✓
              </span>
              {perk}
            </li>
          ))}
        </ul>
      </div>

      {/* mini before → after card */}
      <div className="relative mt-10 flex items-center gap-5 self-start rounded-2xl border border-line bg-black/40 p-5 backdrop-blur-md">
        <div className="opacity-60">
          <ScoreRing score={58} size={72} color="var(--color-warn)" label="before" />
        </div>
        <span className="text-2xl text-subtle">→</span>
        <ScoreRing score={84} size={92} color="var(--color-good)" label="after" />
        <p className="max-w-[9rem] text-sm font-medium text-muted">Average jump after using the AI rewrites</p>
      </div>
    </div>
  );
}
