// Regenerates assets/tree.svg (+ dark variant) as a system-map style diagram:
// one core node labeled ME in the center, wired out to the 6 repos most
// recently pushed to. Run via GitHub Action on a schedule.

const USERNAME = process.env.GH_USERNAME || "Garvnanda";
const TOKEN = process.env.GITHUB_TOKEN;
const NODE_COUNT = 6;

const headers = { "User-Agent": "tree-widget", Accept: "application/vnd.github+json" };
if (TOKEN) headers.Authorization = `Bearer ${TOKEN}`;

const res = await fetch(`https://api.github.com/users/${USERNAME}/repos?type=owner&sort=pushed&per_page=100`, { headers });
if (!res.ok) throw new Error(`GitHub API ${res.status}: ${await res.text()}`);
const repos = await res.json();

const picked = repos
  .filter((r) => !r.fork && !r.archived && r.name.toLowerCase() !== USERNAME.toLowerCase())
  .slice(0, NODE_COUNT);

while (picked.length < NODE_COUNT) picked.push({ name: "—", language: "", description: "" });

const esc = (s = "") => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const short = (s = "", n = 26) => (s.length > n ? s.slice(0, n - 1) + "…" : s);

// hex layout around a central core, canvas 1000x620
const CENTER = { x: 500, y: 310, w: 190, h: 56 };
const NODES = [
  { x: 60, y: 90, w: 190, h: 54 },
  { x: 750, y: 90, w: 190, h: 54 },
  { x: 20, y: 283, w: 190, h: 54 },
  { x: 790, y: 283, w: 190, h: 54 },
  { x: 140, y: 476, w: 190, h: 54 },
  { x: 670, y: 476, w: 190, h: 54 },
];

const cx = CENTER.x + CENTER.w / 2;
const cy = CENTER.y + CENTER.h / 2;

const wires = NODES.map((n, i) => {
  const nx = n.x + n.w / 2;
  const ny = n.y + n.h / 2;
  return `<line class="wire w${i + 1}" x1="${cx}" y1="${cy}" x2="${nx}" y2="${ny}"/>`;
}).join("\n    ");

const flows = NODES.map((n, i) => {
  const nx = n.x + n.w / 2;
  const ny = n.y + n.h / 2;
  return `<line class="flow" x1="${cx}" y1="${cy}" x2="${nx}" y2="${ny}"/>`;
}).join("\n    ");

const nodeBlocks = NODES.map((n, i) => {
  const repo = picked[i];
  const title = esc((repo.name || "—").toUpperCase());
  const meta = esc(short(repo.language ? `${repo.language} · repo` : repo.description || "repository"));
  const tx = n.x + n.w / 2;
  return `<g class="pop p${i + 1}">
      <rect class="node" x="${n.x}" y="${n.y}" width="${n.w}" height="${n.h}" rx="2"/>
      <text fill="var(--bone)" class="mono" x="${tx}" y="${n.y + 23}" font-size="12" letter-spacing="1" text-anchor="middle">${title}</text>
      <text fill="var(--muted)" class="mono" x="${tx}" y="${n.y + 42}" font-size="9" letter-spacing="1" text-anchor="middle">${meta}</text>
    </g>`;
}).join("\n    ");

function buildSvg(vars) {
  return `<svg viewBox="0 0 1000 620" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Live ecosystem tree: me at the center, wired out to my 6 most active repos">
  <style>
    :root { --bone: ${vars.bone}; --muted: ${vars.muted}; --dim: ${vars.dim}; --rule: ${vars.rule}; --node-bg: ${vars.nodeBg}; --core-bg: ${vars.coreBg}; --accent: ${vars.accent}; }
    .mono { font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }
    .node { fill: var(--node-bg); stroke: var(--rule); stroke-width: 1; }
    .core { fill: var(--core-bg); stroke: var(--rule); stroke-width: 1.5; }
    .wire { stroke: var(--rule); stroke-width: 1; stroke-dasharray: 500; stroke-dashoffset: 500; animation: draw 1.6s cubic-bezier(.6,0,.2,1) forwards; }
    @keyframes draw { to { stroke-dashoffset: 0; } }
    .w1{animation-delay:.2s}.w2{animation-delay:.32s}.w3{animation-delay:.44s}.w4{animation-delay:.56s}.w5{animation-delay:.68s}.w6{animation-delay:.8s}
    .flow { stroke: var(--muted); stroke-width: 1; opacity: .25; stroke-dasharray: 3 9; animation: march 1.4s linear infinite; }
    @keyframes march { to { stroke-dashoffset: -12; } }
    .pop { opacity: 0; animation: pop .7s cubic-bezier(.2,.7,.2,1) forwards; }
    @keyframes pop { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
    .p0{animation-delay:.1s}.p1{animation-delay:.9s}.p2{animation-delay:1.0s}.p3{animation-delay:1.1s}.p4{animation-delay:1.2s}.p5{animation-delay:1.3s}.p6{animation-delay:1.4s}
    .breathe { animation: breathe 3.2s ease-in-out infinite; }
    @keyframes breathe { 0%,100%{opacity:1} 50%{opacity:.55} }
    @media (prefers-reduced-motion: reduce) {
      .wire,.flow,.pop,.breathe { animation: none; }
      .wire{stroke-dashoffset:0} .pop{opacity:1} .flow{opacity:.12}
    }
  </style>

  <line x1="48" y1="40" x2="952" y2="40" stroke="var(--rule)"/>
  <text fill="var(--muted)" class="mono" x="48" y="28" font-size="11" letter-spacing="3.5">LIVE ECOSYSTEM TREE — 6 MOST RECENTLY SHIPPED REPOS</text>
  <text fill="var(--muted)" class="mono" x="952" y="28" font-size="11" letter-spacing="3.5" text-anchor="end">FIG. 01</text>

  <g>
    ${wires}
  </g>
  <g>
    ${flows}
  </g>

  <g class="pop p0 breathe">
    <rect class="core" x="${CENTER.x}" y="${CENTER.y}" width="${CENTER.w}" height="${CENTER.h}" rx="4"/>
    <text fill="var(--bone)" class="mono" x="${cx}" y="${CENTER.y + 24}" font-size="14" font-weight="800" letter-spacing="2" text-anchor="middle">ME</text>
    <text fill="var(--accent)" class="mono" x="${cx}" y="${CENTER.y + 42}" font-size="8.5" letter-spacing="1" text-anchor="middle">@${USERNAME}</text>
  </g>

  ${nodeBlocks}

  <line x1="48" y1="590" x2="952" y2="590" stroke="var(--rule)"/>
  <text fill="var(--dim)" class="mono" x="952" y="612" font-size="10" letter-spacing="2" text-anchor="end">DASHED LINES — DATA IN MOTION</text>
</svg>
`;
}

const LIGHT = { bone: "#000000", muted: "#000000", dim: "#000000", rule: "#000000", nodeBg: "#FFFFFF", coreBg: "#FFFFFF", accent: "#000000" };
const DARK = { bone: "#FFFFFF", muted: "#FFFFFF", dim: "#FFFFFF", rule: "#FFFFFF", nodeBg: "#0D1117", coreBg: "#0D1117", accent: "#FFFFFF" };

const { writeFileSync, mkdirSync } = await import("node:fs");
mkdirSync("assets/dark", { recursive: true });
writeFileSync("assets/tree.svg", buildSvg(LIGHT));
writeFileSync("assets/dark/tree.svg", buildSvg(DARK));
console.log(`wrote assets/tree.svg + assets/dark/tree.svg with nodes: ${picked.map((r) => r.name).join(", ")}`);
