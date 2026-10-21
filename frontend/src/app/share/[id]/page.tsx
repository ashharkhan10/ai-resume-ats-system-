/**
 * Public shared report ( /share/<id> ) — read-only, no login needed.
 */
import { Suspense } from "react";
import { Header } from "@/components/layout/Header";
import { ReportLoader, ReportSkeleton } from "@/components/results/ReportLoader";

export default function SharePage({ params }: PageProps<"/share/[id]">) {
  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-5xl flex-1 px-4 pb-16">
        <Suspense fallback={<ReportSkeleton />}>
          <SharedReport params={params} />
        </Suspense>
      </main>
    </>
  );
}

async function SharedReport({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <ReportLoader id={id} shared />;
}
