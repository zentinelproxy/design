/**
 * Colour maths shared by build.ts (contrast gate) and scripts/ramps.ts
 * (palette derivation). sRGB <-> OKLab/OKLCH after Björn Ottosson, and the
 * WCAG 2.x relative-luminance contrast ratio.
 */

export type Rgb = [number, number, number];

export function hexToRgb(hex: string): Rgb {
  const h = hex.replace(/^#/, "");
  if (!/^[0-9a-fA-F]{6}$/.test(h)) throw new Error(`not a #rrggbb colour: ${hex}`);
  return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)) as Rgb;
}

function srgbToLinear(c: number): number {
  const v = c / 255;
  return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
}

function linearToSrgb(c: number): number {
  const v = Math.min(1, Math.max(0, c));
  const s = v <= 0.0031308 ? 12.92 * v : 1.055 * v ** (1 / 2.4) - 0.055;
  return Math.round(s * 255);
}

/** WCAG 2.x relative luminance. */
export function luminance(hex: string): number {
  const [r, g, b] = hexToRgb(hex).map(srgbToLinear);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** WCAG 2.x contrast ratio, 1..21. */
export function contrast(a: string, b: string): number {
  const [lo, hi] = [luminance(a), luminance(b)].sort((x, y) => x - y);
  return (hi + 0.05) / (lo + 0.05);
}

/** Alpha-composite `fg` (#rrggbb) at `alpha` over opaque `bg`. */
export function over(fg: string, alpha: number, bg: string): string {
  const f = hexToRgb(fg), b = hexToRgb(bg);
  const mix = f.map((c, i) => Math.round(c * alpha + b[i] * (1 - alpha)));
  return "#" + mix.map((c) => c.toString(16).padStart(2, "0")).join("");
}

export function toOklch(hex: string): [number, number, number] {
  const [r, g, b] = hexToRgb(hex).map(srgbToLinear);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s;
  const A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
  const B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
  return [L, Math.hypot(A, B), ((Math.atan2(B, A) * 180) / Math.PI + 360) % 360];
}

function oklabToLinear(L: number, a: number, b: number): Rgb {
  const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const s = (L - 0.0894841775 * a - 1.291485548 * b) ** 3;
  return [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
  ];
}

/** OKLCH -> #rrggbb, reducing chroma until the colour fits in sRGB. */
export function fromOklch(L: number, C: number, H: number): string {
  const rad = (H * Math.PI) / 180;
  let c = C;
  let lin = oklabToLinear(L, c * Math.cos(rad), c * Math.sin(rad));
  while (c > 0 && lin.some((v) => v < -1e-4 || v > 1 + 1e-4)) {
    c -= 0.002;
    lin = oklabToLinear(L, Math.max(c, 0) * Math.cos(rad), Math.max(c, 0) * Math.sin(rad));
  }
  return "#" + lin.map((v) => linearToSrgb(v).toString(16).padStart(2, "0")).join("");
}
