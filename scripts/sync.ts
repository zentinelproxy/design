/**
 * Vendor the build output into the consumer repos: `deno task sync`.
 *
 * Consumers are checkouts named after their repo under one root directory,
 * by default this repo's parent (../zentinelproxy.io, ../zentinelproxy.io-docs,
 * ../api.zentinelproxy.io, ../registry.zentinelproxy.io). Each one commits its
 * copy, so it builds on its own without this repo (the same model as
 * cyanea-bio/design -> www/docs). A consumer that is not checked out is
 * skipped, unless --strict.
 *
 *   deno task sync                       copy files into every consumer that is checked out
 *   deno task sync --check               copy nothing; exit 1 if any consumer's copy is stale
 *   deno task sync --check --root <dir>  look for the consumers under <dir> instead of ..
 *   deno task sync --check --strict      also fail when a consumer is not checked out (CI)
 *
 * The root can also come from DESIGN_CONSUMER_ROOT; --root wins. Run
 * `deno task build` first: sync copies dist/ as it is on disk.
 */

const args = Deno.args;
const CHECK = args.includes("--check");
const STRICT = args.includes("--strict");

function flag(name: string): string | undefined {
  const i = args.indexOf(name);
  if (i === -1) return undefined;
  const v = args[i + 1];
  if (!v || v.startsWith("--")) {
    console.error(`${name} needs a value`);
    Deno.exit(2);
  }
  return v;
}

const ROOT = (flag("--root") ?? Deno.env.get("DESIGN_CONSUMER_ROOT") ?? "..").replace(/\/+$/, "");

const FONT_FILES = [...Deno.readDirSync("fonts")]
  .filter((e) => e.isFile && /\.(woff2|txt)$/.test(e.name))
  .map((e) => e.name)
  .sort();

const fonts = (dest: string) => FONT_FILES.map((f) => [`fonts/${f}`, `${dest}/${f}`] as const);

// Zola + Sass: style.scss imports tokens, fonts, frame.
const sassConsumer = [
  ["dist/scss/_tokens.scss", "sass/_tokens.scss"],
  ["dist/scss/_fonts.scss", "sass/_fonts.scss"],
  ["dist/scss/_frame.scss", "sass/_frame.scss"],
  ...fonts("static/fonts"),
] as const;

const CONSUMERS: Record<string, ReadonlyArray<readonly [string, string]>> = {
  "zentinelproxy.io": sassConsumer,
  "registry.zentinelproxy.io": sassConsumer,
  // Zola + the tanuki theme (a submodule we do not edit). Plain CSS under
  // static/css/, linked from the site's own template overrides after the theme
  // stylesheet: fonts.css, tokens.css, bridge.css, frame.css.
  "zentinelproxy.io-docs": [
    ["dist/css/tokens.css", "static/css/zentinel-tokens.css"],
    ["dist/css/fonts.css", "static/css/zentinel-fonts.css"],
    ["dist/css/bridge.css", "static/css/zentinel-bridge.css"],
    ["dist/css/frame.css", "static/css/zentinel-frame.css"],
    ...fonts("static/fonts"),
  ],
  // Plain CSS, linked from its own templates.
  "api.zentinelproxy.io": [
    ["dist/css/tokens.css", "static/css/tokens.css"],
    ["dist/css/fonts.css", "static/css/fonts.css"],
    ["dist/css/frame.css", "static/css/frame.css"],
    ...fonts("static/fonts"),
  ],
};

async function same(a: string, b: string): Promise<boolean> {
  try {
    const [x, y] = await Promise.all([Deno.readFile(a), Deno.readFile(b)]);
    return x.length === y.length && x.every((v, i) => v === y[i]);
  } catch {
    return false;
  }
}

const staleBy: Record<string, string[]> = {};
const missing: string[] = [];
let written = 0;

for (const [name, files] of Object.entries(CONSUMERS)) {
  const root = `${ROOT}/${name}`;
  try {
    await Deno.stat(root);
  } catch {
    missing.push(name);
    console.log(`${STRICT ? "missing" : "skip"} ${root} (not checked out)`);
    continue;
  }
  for (const [src, rel] of files) {
    const dest = `${root}/${rel}`;
    if (await same(src, dest)) continue;
    if (CHECK) {
      (staleBy[name] ??= []).push(rel);
      console.log(`stale ${dest}`);
    } else {
      await Deno.mkdir(dest.slice(0, dest.lastIndexOf("/")), { recursive: true });
      await Deno.copyFile(src, dest);
      written++;
      console.log(`  wrote ${dest}`);
    }
  }
}

const stale = Object.keys(staleBy);
const failed = (CHECK && stale.length > 0) || (STRICT && missing.length > 0);

// In GitHub Actions, also write a per-consumer table to the job summary.
const summaryPath = Deno.env.get("GITHUB_STEP_SUMMARY");
if (CHECK && summaryPath) {
  const rows = Object.keys(CONSUMERS).map((name) => {
    const state = missing.includes(name)
      ? "not checked out"
      : staleBy[name]
      ? `**stale**: ${staleBy[name].map((f) => `\`${f}\``).join(", ")}`
      : "up to date";
    return `| \`${name}\` | ${state} |`;
  });
  await Deno.writeTextFile(
    summaryPath,
    `### Design drift\n\n| Consumer | State |\n|---|---|\n${rows.join("\n")}\n\n` +
      (stale.length ? "Fix: see *Drift* in the design repo's README.\n" : ""),
    { append: true },
  );
}

if (CHECK && stale.length) {
  console.error(`\nstale consumers: ${stale.join(", ")}`);
  for (const name of stale) console.error(`  ${name}: ${staleBy[name].length} file(s) differ from design/dist`);
  console.error("fix: in the design repo, `deno task build && deno task sync`, then commit the copies in each stale consumer");
}
if (STRICT && missing.length) {
  console.error(`not checked out under ${ROOT}: ${missing.join(", ")}`);
}
if (failed) Deno.exit(1);
console.log(CHECK ? "consumers up to date" : written ? "done; commit the changes in each consumer repo" : "nothing to sync");
