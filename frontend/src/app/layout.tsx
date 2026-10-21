/**
 * The outer frame of every page: fonts, page title and background.
 */
import type { Metadata } from "next";
import { Bricolage_Grotesque, Inter } from "next/font/google";
import { Background } from "@/components/layout/Background";
import "./globals.css";

// Body text
const inter = Inter({ variable: "--font-inter", subsets: ["latin"] });

// Headings and big numbers
const bricolage = Bricolage_Grotesque({ variable: "--font-bricolage", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Resume ATS — check your resume against any job",
  description:
    "Free ATS resume checker for students: score, missing keywords, AI bullet rewrites, interview prep and cover letters.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${inter.variable} ${bricolage.variable} h-full antialiased`}>
      <body className="isolate flex min-h-full flex-col bg-ground font-sans text-ink">
        <Background />
        {children}
      </body>
    </html>
  );
}
