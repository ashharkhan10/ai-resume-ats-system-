/**
 * The report shape the backend sends back (matches backend/app/schemas/analysis.py).
 */
export type Level = "High" | "Medium" | "Low";

export type CategoryScore = { id: string; label: string; score: number; weight: number };
export type KeywordMatch = { matched: string[]; missing: string[]; match_pct: number };
export type SkillProof = { name: string; proof: string | null };
export type Issue = { id: string; level: Level; title: string; detail: string };
export type Rewrite = { before: string; after: string; why: string };
/** How well the background fits the target role (null when there's no target). */
export type RoleFit = { score: number | null; verdict: string; gaps: string[] };

export type AnalysisReport = {
  score: number;
  rating: string;
  summary: string;
  target: { kind: "job" | "role" | "none"; title: string };
  categories: CategoryScore[];
  keywords: KeywordMatch | null;
  fit?: RoleFit | null;
  skills: SkillProof[];
  issues: Issue[];
  rewrites: Rewrite[];
  strengths: string[];
  stats: { word_count: number; bullets: number; quantified_bullets: number };
  // Set once the report is saved
  id: string;
  file_name: string;
  created_at: string;
  shared: boolean;
};

/** One row in "My versions". */
export type AnalysisSummary = {
  id: string;
  file_name: string;
  target_title: string;
  score: number;
  created_at: string;
};

export type User = { id: number; name: string; email: string };

export type InterviewQuestion = { type: string; question: string; why: string; tip: string };

export type Tone = "professional" | "friendly" | "confident";
export type CoverLetter = { tone: Tone; text: string };
