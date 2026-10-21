/**
 * Your report ( /report/<id> ).
 * The id comes from the URL; the report itself is loaded in the browser.
 */
import { Suspense } from "react";
import { Header } from "@/components/layout/Header";
import { ReportLoader, ReportSkeleton } from "@/components/results/ReportLoader";

export default function ReportPage({ params }: PageProps<"/report/[id]">) {
  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-5xl flex-1 px-4 pb-16">
        <Suspense fallback={<ReportSkeleton />}>
          <Report params={params} />
        </Suspense>
      </main>
    </>
  );
}

async function Report({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <ReportLoader id={id} />;
}
