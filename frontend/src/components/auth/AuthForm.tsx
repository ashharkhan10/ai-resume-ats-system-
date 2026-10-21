"use client";
/**
 * AuthForm — used by both /login and /register.
 * If someone tries to log in without an account, we show a "Create account" button.
 */
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { login, register } from "@/lib/api";
import { saveLogin } from "@/lib/auth";

type Props = { mode: "login" | "register" };

export function AuthForm({ mode }: Props) {
  const router = useRouter();
  const isLogin = mode === "login";

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const reply = isLogin ? await login(email, password) : await register(name, email, password);
      saveLogin(reply.token, reply.user);
      // Go back to the page that sent us here (e.g. /analyze), or to the checker.
      const next = new URLSearchParams(window.location.search).get("next");
      router.push(next?.startsWith("/") ? next : "/analyze");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  const noAccount = isLogin && error?.includes("create an account");

  return (
    <form onSubmit={handleSubmit} className="rise flex w-full max-w-md flex-col gap-4 rounded-3xl border border-line bg-surface/90 p-8 shadow-[0_30px_80px_rgb(0_0_0/0.45)] backdrop-blur">
      <div>
        <h1 className="font-display text-3xl font-extrabold">{isLogin ? "Welcome back" : "Create your account"}</h1>
        <p className="mt-1 text-muted">
          {isLogin ? "Log in to see your saved versions." : "Save every version and track your score."}
        </p>
      </div>

      {!isLogin && <Field label="Name" value={name} onChange={setName} autoComplete="name" />}
      <Field label="Email" type="email" value={email} onChange={setEmail} autoComplete="email" required />
      <Field
        label="Password"
        type="password"
        value={password}
        onChange={setPassword}
        autoComplete={isLogin ? "current-password" : "new-password"}
        hint={isLogin ? undefined : "At least 8 characters"}
        required
      />

      {error && (
        <div className="rounded-xl bg-bad-soft p-3 text-sm font-medium text-bad-ink">
          {error}
          {noAccount && (
            <Link href="/register" className="btn btn-primary mt-3 w-full">
              Create account
            </Link>
          )}
        </div>
      )}

      <button type="submit" disabled={loading} className="btn btn-primary btn-lg">
        {loading ? "Please wait…" : isLogin ? "Log in" : "Create account"}
      </button>

      <p className="text-center text-sm text-muted">
        {isLogin ? "New here? " : "Already have an account? "}
        <Link href={isLogin ? "/register" : "/login"} className="font-semibold text-brand hover:underline">
          {isLogin ? "Create an account" : "Log in"}
        </Link>
      </p>
    </form>
  );
}

type FieldProps = {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  autoComplete?: string;
  hint?: string;
  required?: boolean;
};

function Field({ label, value, onChange, type = "text", autoComplete, hint, required }: FieldProps) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="text-sm font-semibold">{label}</span>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        autoComplete={autoComplete}
        required={required}
        minLength={type === "password" && hint ? 8 : undefined}
        // Password-manager extensions (e.g. Norton) add their own attributes to inputs.
        // This stops React from warning about it.
        suppressHydrationWarning
        className="rounded-xl border border-line-strong bg-soft px-4 py-3 transition-shadow outline-none hover:border-brand/50 focus:border-brand focus:bg-surface focus:ring-4 focus:ring-brand-soft"
      />
      {hint && <span className="text-xs text-subtle">{hint}</span>}
    </label>
  );
}
