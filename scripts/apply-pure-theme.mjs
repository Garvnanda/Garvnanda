// Forces every static profile SVG to a pure black-on-white (light) / pure
// white-on-transparent (dark) contrast theme, replicated as two files per
// asset — assets/<name>.svg (light) and assets/dark/<name>.svg (dark) — so
// README can pick the right one via <picture><source media="(prefers-color-scheme: dark)">.
//
// Both files keep the original animated markup; only the trailing :root
// override (appended last, so it wins over the earlier default/media rules
// by source order) changes per variant.
//
// Re-running is safe: an override left by a previous run is stripped before
// the new one goes in, so the rule never stacks up.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";

const ASSETS = join(dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1")), "..", "assets");

const FILES = [
  "header-v1.svg",
  "divider.svg",
  "s01-whoami.svg",
  "s02-stack.svg",
  "s03-ttt.svg",
  "s04-experience.svg",
  "s05-education.svg",
  "s06-projects.svg",
  "s07-achievements.svg",
  "s08-certifications.svg",
  "s09-telemetry.svg",
  "s10-commits.svg",
  "s11-tree.svg",
  "s12-chess.svg",
  "whoami.svg",
  "stack.svg",
  "experience.svg",
  "education.svg",
  "projects.svg",
  "achievements.svg",
  "certifications.svg",
  "footer.svg",
];

const LIGHT = { bone: "#000000", ink: "#000000", muted: "#000000", dim: "#000000", rule: "#000000", accent: "#000000", ghost: "#000000", panel: "#FFFFFF", win: "#FFFFFF", bar: "#F0F0F0", "node-bg": "#FFFFFF", "core-bg": "#FFFFFF" };
const DARK = { bone: "#FFFFFF", ink: "#FFFFFF", muted: "#FFFFFF", dim: "#FFFFFF", rule: "#FFFFFF", accent: "#FFFFFF", ghost: "#FFFFFF", panel: "#0D1117", win: "#0D1117", bar: "#161B22", "node-bg": "#0D1117", "core-bg": "#0D1117" };

function buildOverride(varNames, map) {
  const decls = varNames.filter((v) => map[v]).map((v) => `--${v}: ${map[v]};`);
  return `    :root { ${decls.join(" ")} }`;
}

// Drop the flat `:root { --x: #hex; ... }` line a previous run parked just
// before </style>. The authored rules are indented blocks or live inside a
// media query, so they never match this shape.
function stripPreviousOverride(src) {
  return src.replace(/\n[ \t]*:root \{(?: --[\w-]+: #[0-9A-Fa-f]{6};)+ \}\n([ \t]*)<\/style>/, "\n$1</style>");
}

for (const file of FILES) {
  const path = join(ASSETS, file);
  const src = stripPreviousOverride(readFileSync(path, "utf8"));

  const rootMatch = src.match(/:root\s*\{([^}]*)\}/);
  if (!rootMatch) {
    console.warn(`skip ${file} — no :root block found`);
    continue;
  }
  const varNames = [...rootMatch[1].matchAll(/--([\w-]+)\s*:/g)].map((m) => m[1]);

  const lightOverride = buildOverride(varNames, LIGHT);
  const darkOverride = buildOverride(varNames, DARK);

  const lightOut = src.replace(/(\s*)<\/style>/, `\n${lightOverride}\n  </style>`);
  const darkOut = src.replace(/(\s*)<\/style>/, `\n${darkOverride}\n  </style>`);

  writeFileSync(path, lightOut);
  mkdirSync(join(ASSETS, "dark"), { recursive: true });
  writeFileSync(join(ASSETS, "dark", file), darkOut);
  console.log(`theme applied: ${file}`);
}
