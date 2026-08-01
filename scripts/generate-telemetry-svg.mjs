// Regenerates assets/telemetry.svg (+ dark variant): live language distribution,
// shipping velocity (repos started per year), and profile counters — pulled
// straight from the GitHub API. Run via GitHub Action on a schedule.

const USERNAME = process.env.GH_USERNAME || "Garvnanda";
const TOKEN = process.env.GITHUB_TOKEN;

const headers = { "User-Agent": "telemetry-widget", Accept: "application/vnd.github+json" };
if (TOKEN) headers.Authorization = `Bearer ${TOKEN}`;

async function get(url) {
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`GitHub API ${res.status} on ${url}: ${await res.text()}`);
  return res.json();
}

const repos = (await get(`https://api.github.com/users/${USERNAME}/repos?type=owner&sort=updated&per_page=100`)).filter(
  (r) => !r.fork && !r.archived
);

// language bytes, aggregated across repos (capped to keep API calls bounded)
const langTotals = {};
for (const r of repos.slice(0, 40)) {
  try {
    const langs = await get(r.languages_url);
    for (const [lang, bytes] of Object.entries(langs)) langTotals[lang] = (langTotals[lang] || 0) + bytes;
  } catch {
    // ignore individual repo language fetch failures
  }
}
const totalBytes = Object.values(langTotals).reduce((a, b) => a + b, 0) || 1;
const topLangs = Object.entries(langTotals)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 6)
  .map(([lang, bytes]) => ({ lang, pct: Math.round((bytes / totalBytes) * 100) }));
const maxPct = Math.max(...topLangs.map((l) => l.pct), 1);

// shipping velocity: repos created per calendar year, last 3 years
const now = new Date();
const years = [now.getFullYear() - 2, now.getFullYear() - 1, now.getFullYear()];
const perYear = years.map((y) => repos.filter((r) => new Date(r.created_at).getFullYear() === y).length);
const maxYear = Math.max(...perYear, 1);

// counters
const totalRepos = repos.length;
const platforms = [...new Set(topLangs.map((l) => l.lang))].slice(0, 4).join(" / ") || "MULTI";

const esc = (s = "") => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const barRows = topLangs
  .map((l, i) => {
    const y = 108 + i * 38;
    const w = Math.max(6, Math.round((l.pct / maxPct) * 230));
    return `<text fill="var(--bone)" x="48" y="${y - 8}">${esc(l.lang.toLowerCase())}</text>       <rect class="bar g${i + 1}" x="48" y="${y}" width="${w}" height="6" fill="var(--accent)"/><text fill="var(--muted)" x="${48 + w + 10}" y="${y + 7}" font-size="10">${l.pct}%</text>`;
  })
  .join("\n    ");

// sparkline points across a 616-wide, 160-tall plot area
const plotX0 = 392, plotX1 = 656, plotY0 = 252, plotY1 = 92;
const step = (plotX1 - plotX0) / (perYear.length - 1);
const points = perYear.map((v, i) => {
  const x = plotX0 + i * step;
  const y = plotY0 - (v / maxYear) * (plotY0 - plotY1);
  return { x, y };
});
const polyline = points.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(" ");
const dots = points
  .slice(1)
  .map((p, i) => `<circle class="dot d${i + 1}" cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="2.5" fill="var(--bone)"/>`)
  .join("\n    ");
const lastPoint = points[points.length - 1];
const trend = perYear[perYear.length - 1] >= perYear[0] ? "accelerating" : "steady";

function buildSvg(vars) {
  return `<svg viewBox="0 0 1000 330" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Telemetry: language distribution, shipping velocity, live profile counters">
  <style>
    :root { --bone: ${vars.bone}; --muted: ${vars.muted}; --dim: ${vars.dim}; --rule: ${vars.rule}; --accent: ${vars.accent}; }
    .mono { font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }
    .bar { transform: scaleX(0); animation: grow 1.2s cubic-bezier(.2,.7,.2,1) forwards; }
    @keyframes grow { to { transform: scaleX(1); } }
    .g1{transform-origin:48px 0;animation-delay:.3s}.g2{transform-origin:48px 0;animation-delay:.45s}.g3{transform-origin:48px 0;animation-delay:.6s}
    .g4{transform-origin:48px 0;animation-delay:.75s}.g5{transform-origin:48px 0;animation-delay:.9s}.g6{transform-origin:48px 0;animation-delay:1.05s}
    .spark { stroke-dasharray: 700; stroke-dashoffset: 700; animation: draw 2.2s cubic-bezier(.6,0,.2,1) .5s forwards; }
    @keyframes draw { to { stroke-dashoffset: 0; } }
    .dot { opacity: 0; animation: fade .4s ease forwards; }
    .d1{animation-delay:1.3s}.d2{animation-delay:1.9s}
    @keyframes fade { to { opacity: 1; } }
    .rise { opacity: 0; animation: rise .8s cubic-bezier(.2,.7,.2,1) forwards; }
    @keyframes rise { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
    .n1{animation-delay:.5s}.n2{animation-delay:.7s}.n3{animation-delay:.9s}.n4{animation-delay:1.1s}
    .ping { animation: ping 2.2s ease-out infinite; transform-origin: ${lastPoint.x.toFixed(1)}px ${lastPoint.y.toFixed(1)}px; }
    @keyframes ping { 0%{transform:scale(.4);opacity:.9} 80%,100%{transform:scale(2.8);opacity:0} }
    @media (prefers-reduced-motion: reduce) {
      .bar,.spark,.dot,.rise,.ping { animation: none; }
      .bar{transform:scaleX(1)} .spark{stroke-dashoffset:0} .dot,.rise{opacity:1} .ping{opacity:0}
    }
  </style>

  <line x1="48" y1="40" x2="952" y2="40" stroke="var(--rule)"/>
  <text fill="var(--muted)" class="mono" x="48" y="28" font-size="11" letter-spacing="3.5">TELEMETRY — WHAT THE HANDS ARE DOING</text>
  <text fill="var(--muted)" class="mono" x="952" y="28" font-size="11" letter-spacing="3.5" text-anchor="end">FIG. 02</text>
  <line x1="360" y1="64" x2="360" y2="296" stroke="var(--rule)" opacity=".4"/>
  <line x1="688" y1="64" x2="688" y2="296" stroke="var(--rule)" opacity=".4"/>

  <text fill="var(--dim)" class="mono" x="48" y="78" font-size="10" letter-spacing="2.5">LANGUAGE DISTRIBUTION · LIVE</text>
  <g class="mono" font-size="11">
    ${barRows}
  </g>

  <text fill="var(--dim)" class="mono" x="392" y="78" font-size="10" letter-spacing="2.5">SHIPPING VELOCITY · ${years[0]} → ${years[2]}</text>
  <g>
    <line x1="392" y1="252" x2="656" y2="252" stroke="var(--rule)"/>
    <polyline class="spark" points="${polyline}" stroke="var(--accent)" stroke-width="1.5" fill="none"/>
    ${dots}
    <circle class="ping" cx="${lastPoint.x.toFixed(1)}" cy="${lastPoint.y.toFixed(1)}" r="4" stroke="var(--accent)" fill="none"/>
    <circle class="dot d2" cx="${lastPoint.x.toFixed(1)}" cy="${lastPoint.y.toFixed(1)}" r="3" fill="var(--accent)"/>
    <text fill="var(--dim)" class="mono" x="392" y="272" font-size="9.5" letter-spacing="1.5">'${String(years[0]).slice(2)}</text>
    <text fill="var(--dim)" class="mono" x="524" y="272" font-size="9.5" letter-spacing="1.5">'${String(years[1]).slice(2)}</text>
    <text fill="var(--dim)" class="mono" x="640" y="272" font-size="9.5" letter-spacing="1.5">'${String(years[2]).slice(2)}</text>
    <text fill="var(--muted)" class="mono dot d2" x="392" y="300" font-size="10" letter-spacing="1.5">trend — <tspan fill="var(--accent)">${trend}</tspan></text>
  </g>

  <g>
    <g class="rise n1"><text fill="var(--bone)" class="mono" x="720" y="118" font-size="44">${totalRepos}</text><text fill="var(--muted)" class="mono" x="790" y="112" font-size="10" letter-spacing="2.5">REPOSITORIES</text></g>
    <g class="rise n2"><text fill="var(--bone)" class="mono" x="720" y="178" font-size="44">6</text><text fill="var(--muted)" class="mono" x="790" y="172" font-size="10" letter-spacing="2.5">PROJECTS DOCUMENTED</text></g>
    <g class="rise n3"><text fill="var(--bone)" class="mono" x="720" y="238" font-size="44">${topLangs.length}</text><text fill="var(--muted)" class="mono" x="790" y="232" font-size="10" letter-spacing="2.5">TOP LANGUAGES — ${esc(platforms.toUpperCase())}</text></g>
    <g class="rise n4"><text fill="var(--accent)" class="mono" x="718" y="298" font-size="44">∞</text><text fill="var(--muted)" class="mono" x="790" y="292" font-size="10" letter-spacing="2.5">TERMINAL TABS OPEN RIGHT NOW</text></g>
  </g>
</svg>
`;
}

const LIGHT = { bone: "#000000", muted: "#000000", dim: "#000000", rule: "#000000", accent: "#000000" };
const DARK = { bone: "#FFFFFF", muted: "#FFFFFF", dim: "#FFFFFF", rule: "#FFFFFF", accent: "#FFFFFF" };

const { writeFileSync, mkdirSync } = await import("node:fs");
mkdirSync("assets/dark", { recursive: true });
writeFileSync("assets/telemetry.svg", buildSvg(LIGHT));
writeFileSync("assets/dark/telemetry.svg", buildSvg(DARK));
console.log(`wrote assets/telemetry.svg + assets/dark/telemetry.svg — top langs: ${topLangs.map((l) => l.lang).join(", ")}`);
