/**
 * Landing page ( / ).
 */
import { Header } from "@/components/layout/Header";
import { Hero } from "@/components/landing/Hero";
import { FeatureGrid } from "@/components/landing/FeatureGrid";
import { HowItWorks } from "@/components/landing/HowItWorks";

export default function HomePage() {
  return (
    <>
      <Header />

      <main className="flex-1">
        <Hero />
        <FeatureGrid />
        <HowItWorks />
      </main>

      <footer className="py-8 text-center text-sm text-subtle">Built for students · AI Resume ATS</footer>
    </>
  );
}
