/**
 * Palette derivation helper: `deno task ramps`.
 *
 * Prints the colour ramps in tokens.json from the two brand accents. It does
 * NOT write tokens.json: tokens.json is the source of truth, and this script
 * documents how its ramps were derived and lets you regenerate them if you
 * retune a curve. Paste the printed JSON over `color` in tokens.json, then
 * run `deno task build` so the contrast gate re-checks every pairing.
 *
 * Method: each ramp walks a lightness curve in OKLCH at the brand hue, with a
 * chroma envelope that peaks in the middle and a small hue drift (warmer
 * lights, redder darks for orange). Out-of-gamut steps lose chroma until they
 * fit sRGB. The brand hexes are then pinned exactly at their step:
 * #f68d31 = orange-400, #9b4d8a = plum-600.
 */

import { fromOklch, toOklch } from "../lib/color.ts";

const STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950];
const ENVELOPE = [0.18, 0.32, 0.55, 0.8, 1.0, 1.0, 0.95, 0.85, 0.72, 0.6, 0.5];
const SEMANTIC_L = [0.975, 0.945, 0.895, 0.83, 0.76, 0.68, 0.59, 0.5, 0.42, 0.345, 0.27];

function ramp(
  L: number[],
  C: number,
  H: number,
  envelope = ENVELOPE,
  drift: number[] = STEPS.map(() => 0),
  pin?: [number, string],
): Record<string, string> {
  const out: Record<string, string> = {};
  STEPS.forEach((step, i) => (out[step] = fromOklch(L[i], C * envelope[i], H + drift[i])));
  if (pin) out[pin[0]] = pin[1];
  return out;
}

const ORANGE = "#f68d31";
const PLUM = "#9b4d8a";
const [, oC, oH] = toOklch(ORANGE); // L 0.742, C 0.161, H 56.7
const [, pC, pH] = toOklch(PLUM); //   L 0.537, C 0.130, H 336.1

const neutral: Record<string, string> = {};
// Plum-tinted neutrals (hue 330), chroma kept low; 850 is the raised surface on dark.
for (
  const [step, L, C] of [
    [50, 0.978, 0.006], [100, 0.952, 0.009], [200, 0.905, 0.012], [300, 0.83, 0.016],
    [400, 0.72, 0.02], [500, 0.6, 0.022], [600, 0.49, 0.024], [700, 0.39, 0.026],
    [800, 0.3, 0.026], [850, 0.255, 0.024], [900, 0.215, 0.022], [950, 0.175, 0.02],
  ]
) neutral[step] = fromOklch(L, C, 330);

const color = {
  orange: ramp(
    [0.975, 0.945, 0.895, 0.83, 0.742, 0.67, 0.585, 0.5, 0.42, 0.345, 0.27],
    oC, oH, ENVELOPE, [8, 7, 5, 3, 0, -2, -4, -6, -8, -9, -10], [400, ORANGE],
  ),
  plum: ramp(
    [0.975, 0.945, 0.89, 0.81, 0.72, 0.63, 0.537, 0.46, 0.39, 0.32, 0.25],
    pC, pH, [0.15, 0.28, 0.5, 0.75, 0.92, 1.0, 1.0, 0.92, 0.8, 0.68, 0.55], undefined, [600, PLUM],
  ),
  neutral,
  green: ramp(SEMANTIC_L, 0.15, 150),
  amber: ramp(SEMANTIC_L, 0.16, 85),
  red: ramp(SEMANTIC_L, 0.19, 25),
  blue: ramp(SEMANTIC_L, 0.14, 250),
};

console.log(JSON.stringify(color, null, 2));
