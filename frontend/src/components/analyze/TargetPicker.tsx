"use client";
/**
 * TargetPicker — "Paste a job description" OR "Pick a role" (two tabs).
 */
import { ROLES } from "@/lib/roles";

export type TargetMode = "job" | "role";

type Props = {
  mode: TargetMode;
  onModeChange: (mode: TargetMode) => void;
  jobDescription: string;
  onJobDescriptionChange: (text: string) => void;
  role: string;
  onRoleChange: (role: string) => void;
};

export function TargetPicker(props: Props) {
  const { mode, onModeChange, jobDescription, onJobDescriptionChange, role, onRoleChange } = props;

  return (
    <div>
      <div className="mb-4 flex rounded-xl bg-tab p-1">
        <Tab active={mode === "job"} onClick={() => onModeChange("job")}>
          Paste a job description
        </Tab>
        <Tab active={mode === "role"} onClick={() => onModeChange("role")}>
          Pick a role
        </Tab>
      </div>

      {mode === "job" ? (
        <textarea
          value={jobDescription}
          onChange={(e) => onJobDescriptionChange(e.target.value)}
          placeholder="Paste the job description here…"
          rows={8}
          className="w-full rounded-2xl border border-line-strong bg-soft p-4 outline-none focus:border-brand focus:ring-4 focus:ring-brand-soft"
        />
      ) : (
        <div className="flex flex-wrap gap-2">
          {ROLES.map((name) => (
            <button
              key={name}
              type="button"
              onClick={() => onRoleChange(role === name ? "" : name)}
              className={`rounded-full border px-4 py-2 text-sm font-medium transition-all hover:-translate-y-0.5 active:scale-95 ${
                role === name
                  ? "border-brand bg-brand-soft text-brand-dark shadow-[0_6px_20px_rgb(197_139_182/0.35)]"
                  : "border-line-strong bg-surface hover:border-brand"
              }`}
            >
              {name}
            </button>
          ))}
        </div>
      )}
      <p className="mt-2 text-sm text-subtle">Optional — but you get a much better report with a target.</p>
    </div>
  );
}

function Tab({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex-1 rounded-lg py-2 text-sm font-semibold transition-all active:scale-95 ${
        active ? "bg-surface text-ink shadow-sm" : "text-subtle hover:text-ink"
      }`}
    >
      {children}
    </button>
  );
}
