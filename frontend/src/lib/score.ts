/**
 * Small helpers for showing scores.
 */

/** Green for good, amber for okay, red for weak. */
export function scoreColor(score: number): string {
  if (score >= 70) return "var(--color-good)";
  if (score >= 50) return "var(--color-warn)";
  return "var(--color-bad)";
}

/** Colour classes for an issue's priority badge. */
export function levelClasses(level: "High" | "Medium" | "Low"): string {
  if (level === "High") return "bg-bad-soft text-bad-ink";
  if (level === "Medium") return "bg-warn-soft text-warn-ink";
  return "bg-tab text-muted";
}

/** Check a file before uploading. Returns an error message, or null if it's fine. */
export function checkFile(file: File, maxMb = 5): string | null {
  const name = file.name.toLowerCase();
  if (!name.endsWith(".pdf") && !name.endsWith(".docx")) return "Please upload a PDF or DOCX file.";
  if (file.size > maxMb * 1024 * 1024) return `File is too big. Max ${maxMb} MB.`;
  if (file.size === 0) return "This file is empty.";
  return null;
}
