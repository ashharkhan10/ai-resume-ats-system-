"use client";
/**
 * ShareButton — turns on the public link and copies it.
 */
import { useState } from "react";
import { shareAnalysis } from "@/lib/api";

export function ShareButton({ analysisId }: { analysisId: string }) {
  const [state, setState] = useState<"idle" | "working" | "copied" | "error">("idle");

  async function share() {
    setState("working");
    try {
      await shareAnalysis(analysisId);
      await navigator.clipboard.writeText(`${window.location.origin}/share/${analysisId}`);
      setState("copied");
      setTimeout(() => setState("idle"), 2500);
    } catch {
      setState("error");
    }
  }

  const label = {
    idle: "🔗 Share link",
    working: "Creating link…",
    copied: "Link copied ✓",
    error: "Couldn't share — try again",
  }[state];

  return (
    <button onClick={share} disabled={state === "working"} className="btn btn-outline">
      {label}
    </button>
  );
}
