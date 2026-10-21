/**
 * Talking to the backend. Every function throws an Error with a friendly message.
 */
import { getToken, logout } from "./auth";
import type { AnalysisReport, AnalysisSummary, CoverLetter, InterviewQuestion, Tone, User } from "./types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

/** Sends a request (with the login token if there is one) and returns the JSON reply. */
async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (typeof options.body === "string") headers.set("Content-Type", "application/json");

  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, { ...options, headers });
  } catch {
    throw new Error("Can't reach the server. Is the backend running?");
  }

  if (response.status === 401 && token) logout(); // token expired

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail = body?.detail;
    // FastAPI validation errors come as a list
    const message = Array.isArray(detail) ? "Please check the form and try again." : detail;
    throw new Error(message ?? "Something went wrong. Please try again.");
  }
  return response.status === 204 ? (undefined as T) : response.json();
}

const json = (data: unknown) => JSON.stringify(data);

// ---------- analysis ----------

type AnalyzeInput = { file: File; jobDescription: string; targetRole: string };

export function analyzeResume({ file, jobDescription, targetRole }: AnalyzeInput) {
  const form = new FormData();
  form.append("resume", file);
  form.append("job_description", jobDescription);
  form.append("target_role", targetRole);
  return request<AnalysisReport>("/analyze", { method: "POST", body: form });
}

export const getAnalysis = (id: string) => request<AnalysisReport>(`/analyses/${id}`);
export const listAnalyses = () => request<AnalysisSummary[]>("/analyses");
export const deleteAnalysis = (id: string) => request<void>(`/analyses/${id}`, { method: "DELETE" });
export const shareAnalysis = (id: string) => request<{ id: string }>(`/analyses/${id}/share`, { method: "POST" });
export const getSharedReport = (id: string) => request<AnalysisReport>(`/share/${id}`);

export const getInterviewPrep = (id: string, fresh = false) =>
  request<{ questions: InterviewQuestion[] }>(`/analyses/${id}/interview?fresh=${fresh}`, { method: "POST" });

export const getCoverLetter = (id: string, tone: Tone, fresh = false) =>
  request<CoverLetter>(`/analyses/${id}/cover-letter`, { method: "POST", body: json({ tone, fresh }) });

// ---------- accounts ----------

type AuthReply = { token: string; user: User };

export const register = (name: string, email: string, password: string) =>
  request<AuthReply>("/auth/register", { method: "POST", body: json({ name, email, password }) });

export const login = (email: string, password: string) =>
  request<AuthReply>("/auth/login", { method: "POST", body: json({ email, password }) });
