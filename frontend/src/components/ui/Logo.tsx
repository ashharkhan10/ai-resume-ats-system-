/**
 * The app logo: a document with a tick, plus the name.
 */
import Link from "next/link";

type Props = {
  size?: "md" | "lg";
};

export function Logo({ size = "md" }: Props) {
  const box = size === "lg" ? "h-9 w-9" : "h-8 w-8";
  const text = size === "lg" ? "text-xl" : "text-lg";

  return (
    <Link href="/" className="flex items-center gap-2.5">
      <span className={`flex ${box} items-center justify-center rounded-[10px] bg-brand`}>
        <svg
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#FFFFFF"
          strokeWidth="2.2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
          <path d="M14 2v6h6M9 15l2 2 4-4" />
        </svg>
      </span>
      <span className={`font-display ${text} font-extrabold tracking-tight`}>AI Resume ATS</span>
    </Link>
  );
}
