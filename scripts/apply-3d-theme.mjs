// Recolors the yoshi389111/github-profile-3d-contrib "green" output to the
// pure black-on-white / white-on-transparent monochrome theme used across
// the rest of the profile (see apply-pure-theme.mjs). Runs after the action
// generates profile-3d-contrib/*.svg, before those files are committed.

import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";

const ROOT = join(dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1")), "..");
const DIR = join(ROOT, "profile-3d-contrib");

const LEVELS_LIGHT = [
  [240, 240, 240, 224, 224, 224, 208, 208, 208],
  [180, 180, 180, 160, 160, 160, 140, 140, 140],
  [120, 120, 120, 100, 100, 100, 80, 80, 80],
  [70, 70, 70, 55, 55, 55, 40, 40, 40],
  [20, 20, 20, 10, 10, 10, 0, 0, 0],
];

const LEVELS_DARK = [
  [40, 40, 40, 32, 32, 32, 24, 24, 24],
  [90, 90, 90, 75, 75, 75, 60, 60, 60],
  [150, 150, 150, 130, 130, 130, 110, 110, 110],
  [200, 200, 200, 180, 180, 180, 160, 160, 160],
  [255, 255, 255, 235, 235, 235, 215, 215, 215],
];

function rgb(r, g, b) {
  return `rgb(${r}, ${g}, ${b})`;
}

// The action also renders a per-language pie chart + legend (top-languages
// breakdown) using GitHub's official per-language colors via inline
// fill="#rrggbb" / style="fill: #rrggbb;" attributes — not the cont-* classes
// above. Remap each distinct color found to an evenly spaced gray so the
// slices stay distinguishable but monochrome.
function recolorLanguagePie(src, { light }) {
  const colors = new Set();
  const attrRe = /fill="(#[0-9A-Fa-f]{6})"/g;
  const styleRe = /style="fill: (#[0-9A-Fa-f]{6});"/g;
  for (const re of [attrRe, styleRe]) {
    let m;
    while ((m = re.exec(src))) colors.add(m[1].toLowerCase());
  }

  const known = new Set(["#000000", "#ffffff", "#00000f", "#0d1117"]);
  const list = [...colors].filter((c) => !known.has(c)).sort();
  if (list.length === 0) return src;

  const [lo, hi] = light ? [70, 210] : [80, 235];
  const step = list.length > 1 ? (hi - lo) / (list.length - 1) : 0;

  let out = src;
  list.forEach((color, i) => {
    const v = Math.round(lo + step * i);
    const gray = `#${v.toString(16).padStart(2, "0").repeat(3)}`;
    out = out.split(`fill="${color}"`).join(`fill="${gray}"`);
    out = out.split(`fill: ${color};`).join(`fill: ${gray};`);
    const upper = color.toUpperCase();
    out = out.split(`fill="${upper}"`).join(`fill="${gray}"`);
    out = out.split(`fill: ${upper};`).join(`fill: ${gray};`);
  });
  return out;
}

function recolor(src, levels, { fg, weak, strong, bg }) {
  let out = src;

  for (let n = 0; n < levels.length; n++) {
    const [tr, tg, tb, lr, lg, lb, rr, rg, rb] = levels[n];
    out = out.replace(
      new RegExp(`cont-top-${n} \\{ fill: rgb\\([^)]*\\)`, "g"),
      `cont-top-${n} { fill: ${rgb(tr, tg, tb)}`
    );
    out = out.replace(
      new RegExp(`cont-left-${n} \\{ fill: rgb\\([^)]*\\)`, "g"),
      `cont-left-${n} { fill: ${rgb(lr, lg, lb)}`
    );
    out = out.replace(
      new RegExp(`cont-right-${n} \\{ fill: rgb\\([^)]*\\)`, "g"),
      `cont-right-${n} { fill: ${rgb(rr, rg, rb)}`
    );
  }

  out = out.replace(/\.fill-bg \{ fill: [^;]*;/, `.fill-bg { fill: ${bg};`);
  out = out.replace(/\.stroke-bg \{ stroke: [^;]*;/, `.stroke-bg { stroke: ${bg};`);
  out = out.replace(/\.fill-fg \{ fill: [^;]*;/, `.fill-fg { fill: ${fg};`);
  out = out.replace(/\.stroke-fg \{ stroke: [^;]*;/, `.stroke-fg { stroke: ${fg};`);
  out = out.replace(/\.fill-strong \{ fill: [^;]*;/, `.fill-strong { fill: ${strong};`);
  out = out.replace(/\.fill-weak \{ fill: [^;]*;/, `.fill-weak { fill: ${weak};`);
  out = out.replace(/\.stroke-weak \{ stroke: [^;]*;/, `.stroke-weak { stroke: ${weak};`);
  out = out.replace(/<rect x="0" y="0" width="1280" height="850" class="fill-bg"><\/rect>|<rect x="0" y="0" width="1280" height="850" class="fill-bg">/, "");

  return recolorLanguagePie(out, { light: fg === "#000000" });
}

const lightPath = join(DIR, "profile-green.svg");
const darkPath = join(DIR, "profile-night-green.svg");

writeFileSync(
  lightPath,
  recolor(readFileSync(lightPath, "utf8"), LEVELS_LIGHT, { fg: "#000000", weak: "#666666", strong: "#000000", bg: "none" })
);
writeFileSync(
  darkPath,
  recolor(readFileSync(darkPath, "utf8"), LEVELS_DARK, { fg: "#ffffff", weak: "#999999", strong: "#ffffff", bg: "none" })
);

console.log("3D contribution calendar recolored to monochrome theme");
