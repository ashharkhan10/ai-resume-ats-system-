/**
 * Background — soft plum glows on the near-black page, plus a dark vignette at the edges.
 * It sits behind everything (-z-10) and ignores clicks.
 */
const GLOWS = [
  "radial-gradient(ellipse 55% 45% at 15% 0%, rgb(150 90 135 / 0.38), transparent 70%)",
  "radial-gradient(ellipse 45% 40% at 90% 25%, rgb(105 60 110 / 0.30), transparent 70%)",
  "radial-gradient(ellipse 60% 40% at 50% 105%, rgb(190 120 170 / 0.20), transparent 70%)",
  "radial-gradient(ellipse 120% 90% at 50% 50%, transparent 55%, rgb(0 0 0 / 0.55) 100%)", // vignette
].join(", ");

export function Background() {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 -z-10 print:hidden"
      style={{ backgroundImage: GLOWS }}
    />
  );
}
