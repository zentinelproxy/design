/**
 * Vendor the build output into the consumer repos: `deno task sync`.
 *
 * Consumers are sibling checkouts (../zentinelproxy.io, ../zentinelproxy.io-docs).
 * Each one commits its copy, so it builds on its own without this repo (the
 * same model as cyanea-bio/design -> www/docs). A missing sibling is skipped.
 *
 *   deno task sync            copy files into every consumer that is checked out
 *   deno task sync --check    copy nothing; exit 1 if any consumer's copy is stale
 *
 * Run `deno task build` first: sync copies dist/ as it is on disk.
 */

const CHECK = Deno.args.includes("--check");

const FONT_FILES = [...Deno.readDirSync("fonts")]
  .filter((e) => e.isFile && /\.(woff2|txt)$/.test(e.name))
  .map((e) => e.name)
  .sort();

const fonts = (dest: string) => FONT_FILES.map((f) => [`fonts/${f}`, `${dest}/${f}`] as const);

const CONSUMERS: Record<string, ReadonlyArray<readonly [string, string]>> = {
  // zentinelproxy.io: Zola + Sass. style.scss imports tokens, fonts, frame.
  "../zentinelproxy.io": [
    ["dist/scss/_tokens.scss", "sass/_tokens.scss"],
    ["dist/scss/_fonts.scss", "sass/_fonts.scss"],
    ["dist/scss/_frame.scss", "sass/_frame.scss"],
    ...fonts("static/fonts"),
  ],
  // zentinelproxy.io-docs: Zola + the tanuki theme (a submodule we do not edit).
  // Plain CSS under static/css/, linked from the site's own template overrides
  // after the theme stylesheet: fonts.css, tokens.css, bridge.css, frame.css.
  "../zentinelproxy.io-docs": [
    ["dist/css/tokens.css", "static/css/zentinel-tokens.css"],
    ["dist/css/fonts.css", "static/css/zentinel-fonts.css"],
    ["dist/css/bridge.css", "static/css/zentinel-bridge.css"],
    ["dist/css/frame.css", "static/css/zentinel-frame.css"],
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

let stale = 0;
for (const [root, files] of Object.entries(CONSUMERS)) {
  try {
    await Deno.stat(root);
  } catch {
    console.log(`skip ${root} (not checked out)`);
    continue;
  }
  for (const [src, rel] of files) {
    const dest = `${root}/${rel}`;
    if (await same(src, dest)) continue;
    stale++;
    if (CHECK) {
      console.log(`stale ${dest}`);
    } else {
      await Deno.mkdir(dest.slice(0, dest.lastIndexOf("/")), { recursive: true });
      await Deno.copyFile(src, dest);
      console.log(`  wrote ${dest}`);
    }
  }
}

if (CHECK && stale) {
  console.error(`${stale} consumer file(s) out of date; run \`deno task build && deno task sync\``);
  Deno.exit(1);
}
console.log(CHECK ? "consumers up to date" : stale ? "done; commit the changes in each consumer repo" : "nothing to sync");
