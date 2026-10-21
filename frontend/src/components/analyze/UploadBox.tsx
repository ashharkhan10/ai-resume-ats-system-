"use client";
/**
 * UploadBox — drag & drop (or click) to choose a resume file.
 */
import { useRef, useState } from "react";
import { checkFile } from "@/lib/score";

type Props = {
  file: File | null;
  onChange: (file: File | null) => void;
};

export function UploadBox({ file, onChange }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function pick(chosen: File | undefined) {
    if (!chosen) return;
    const problem = checkFile(chosen);
    setError(problem);
    onChange(problem ? null : chosen);
  }

  return (
    <div>
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          pick(e.dataTransfer.files[0]);
        }}
        className={`flex w-full flex-col items-center justify-center gap-2 rounded-2xl border-2 border-dashed p-8 text-center transition-all active:scale-[0.99] ${
          dragging ? "border-brand bg-brand-soft" : file ? "border-good bg-good-soft" : "border-line-strong bg-soft hover:border-brand"
        }`}
      >
        <span className="text-3xl">{file ? "✅" : "📄"}</span>
        {file ? (
          <>
            <span className="font-semibold">{file.name}</span>
            <span className="text-sm text-subtle">Click to choose a different file</span>
          </>
        ) : (
          <>
            <span className="font-semibold">Drop your resume here or click to upload</span>
            <span className="text-sm text-subtle">PDF or DOCX · max 5 MB</span>
          </>
        )}
      </button>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx"
        className="hidden"
        onChange={(e) => pick(e.target.files?.[0])}
      />
      {error && <p className="mt-2 text-sm font-medium text-bad-ink">{error}</p>}
    </div>
  );
}
