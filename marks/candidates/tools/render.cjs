// node render.cjs <node_project_dir> in.svg out.png width  (resvg 2.6.2; currentColor renders black)
const [, , dir, i, o, w] = process.argv;
const { Resvg } = require(require.resolve("@resvg/resvg-js", { paths: [dir] }));
const fs = require("fs");
fs.writeFileSync(o, new Resvg(fs.readFileSync(i, "utf8"), { fitTo: { mode: "width", value: +w } }).render().asPng());
