"use client";
/**
 * Header — logo on the left, links on the right.
 * Sticks to the top with a frosted-glass look. Hidden when printing.
 */
import Link from "next/link";
import { Logo } from "@/components/ui/Logo";
import { logout } from "@/lib/auth";
import { useUser } from "@/lib/useUser";

export function Header() {
  const { user, ready } = useUser();

  return (
    <header className="sticky top-0 z-20 mb-4 border-b border-line bg-ground/60 backdrop-blur-lg print:hidden">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-3 px-4 py-4">
        <Logo />
        <nav className={`flex items-center gap-1 transition-opacity sm:gap-2 ${ready ? "opacity-100" : "opacity-0"}`}>
          {user ? (
            <>
              <Link href="/versions" className="btn btn-ghost">
                My versions
              </Link>
              <button onClick={logout} className="btn btn-ghost">
                Log out
              </button>
            </>
          ) : (
            <Link href="/login" className="btn btn-ghost">
              Log in
            </Link>
          )}
          <Link href="/analyze" className="btn btn-dark hidden sm:inline-flex">
            Check resume
          </Link>
        </nav>
      </div>
    </header>
  );
}
