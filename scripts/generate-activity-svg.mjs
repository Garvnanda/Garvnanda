// Regenerates assets/activity.svg — the last 31 days of contributions as a smooth
// area chart.
//
// This is a local redraw of what github-readme-activity-graph.vercel.app used to
// serve. That deployment answers 402 DEPLOYMENT_DISABLED for every URL including its
// own root, so the README embed rendered as a broken image and no alternative host of
// the project is still up. The layout here follows the settings the old embed asked
// for — transparent background, no border, filled area, custom title — so the panel
// reads the way it did before, without a third party who can switch it off.
//
// Source is contributionsCollection, the same query the GitHub Stats widget uses and
// the same one GitHub's own contribution graph is drawn from, so the panels agree.

const USERNAME = process.env.GH_USERNAME || "Garvnanda";
const TOKEN = process.env.GITHUB_TOKEN;
const DAYS = 31;
const TITLE = "CONTRIBUTION TELEMETRY";

const headers = { "User-Agent": "activity-widget", Accept: "application/vnd.github+json" };
if (TOKEN) headers.Authorization = `Bearer ${TOKEN}`;

async function withRetry(fn) {
  try {
    return await fn();
  } catch {
    await new Promise((r) => setTimeout(r, 3000));
    return await fn();
  }
}

// The calendar always comes back as whole weeks, so ask for a wider window than needed
// and trim to the exact day count afterwards.
async function contributionDays() {
  return withRetry(async () => {
    const to = new Date();
    const from = new Date(to.getTime() - (DAYS + 10) * 86400000);
    const query = `query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar { weeks { contributionDays { date contributionCount } } }
        }
      }
    }`;
    const res = await fetch("https://api.github.com/graphql", {
      method: "POST",
      headers: { ...headers, "Content-Type": "application/json" },
      body: JSON.stringify({ query, variables: { login: USERNAME, from: from.toISOString(), to: to.toISOString() } }),
    });
    if (!res.ok) throw new Error(`graphql ${res.status}`);
    const { data, errors } = await res.json();
    if (errors) throw new Error(`graphql: ${errors.map((e) => e.message).join("; ")}`);
    return data.user.contributionsCollection.contributionCalendar.weeks
      .flatMap((w) => w.contributionDays)
      .filter((d) => d.date <= to.toISOString().slice(0, 10))
      .sort((a, b) => a.date.localeCompare(b.date))
      .slice(-DAYS);
  });
}

const days = await contributionDays();
if (!days.length) throw new Error("contribution calendar came back empty");

const counts = days.map((d) => d.contributionCount);
const peak = Math.max(...counts);

// Chart box inside a 1000x400 canvas. A flat-zero month would divide by zero, so the
// scale floors at 1, and it rounds up to a whole number of gridline steps.
const L = 80, R = 960, TOP = 96, BOT = 300;
const STEPS = 4;
const scale = Math.max(STEPS, Math.ceil(Math.max(1, peak) / STEPS) * STEPS);
const px = (i) => L + (i * (R - L)) / Math.max(1, days.length - 1);
const py = (v) => BOT - (v / scale) * (BOT - TOP);
const pts = counts.map((v, i) => [px(i), py(v)]);

// Catmull-Rom through every point, converted to cubic Beziers — the old graph drew a
// curve rather than straight segments, and with 31 daily points the difference is what
// makes it read as a trend instead of a sawtooth.
function smoothPath(p) {
  if (p.length < 2) return `M${p[0][0]},${p[0][1]}`;
  let d = `M${p[0][0].toFixed(1)},${p[0][1].toFixed(1)}`;
  for (let i = 0; i < p.length - 1; i++) {
    const p0 = p[i - 1] || p[i];
    const p1 = p[i];
    const p2 = p[i + 1];
    const p3 = p[i + 2] || p2;
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
  }
  return d;
}

const line = smoothPath(pts);
const area = `${line} L${R},${BOT} L${L},${BOT} Z`;
const dots = pts.map(([x, y]) => `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3"/>`).join("");

const MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
const label = (iso) => {
  const d = new Date(`${iso}T00:00:00Z`);
  return `${MONTHS[d.getUTCMonth()]} ${d.getUTCDate()}`;
};

// Every other day, angled, the way the original laid its dates out. All 31 upright
// would collide at this width.
const xLabels = days
  .map((d, i) => (i % 2 === 0 || i === days.length - 1 ? { d, i } : null))
  .filter(Boolean)
  .map(({ d, i }) => {
    const x = px(i).toFixed(1);
    return `<text x="${x}" y="322" font-size="10" text-anchor="end" transform="rotate(-45 ${x} 322)">${label(d.date)}</text>`;
  })
  .join("\n      ");

const grid = Array.from({ length: STEPS + 1 }, (_, i) => {
  const v = (scale / STEPS) * i;
  const y = py(v).toFixed(1);
  return `<line class="grid" x1="${L}" y1="${y}" x2="${R}" y2="${y}"/><text class="axis" x="${L - 16}" y="${(Number(y) + 4).toFixed(1)}" font-size="11" text-anchor="end">${v}</text>`;
}).join("\n      ");

function buildSvg(ink) {
  return `<svg viewBox="0 0 1000 400" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Contribution activity over the last ${days.length} days">
  <style>
    :root { --ink:${ink}; }
    .mono { font-family:ui-monospace,"SFMono-Regular","SF Mono",Menlo,Consolas,"Liberation Mono",monospace; fill:var(--ink); }
    .title { font-size:26px; font-weight:700; letter-spacing:4px; }
    .axis { opacity:.6; }
    .grid { stroke:var(--ink); stroke-width:1; opacity:.16; }
    .base { stroke:var(--ink); stroke-width:1; opacity:.45; }
    .area { fill:var(--ink); opacity:.18; }
    .line { fill:none; stroke:var(--ink); stroke-width:2.5; stroke-linejoin:round; stroke-linecap:round; }
    .dot { fill:var(--ink); }
    .sweep { animation:sweep 1.4s cubic-bezier(.4,0,.2,1) forwards; }
    @keyframes sweep { from { clip-path:inset(0 100% 0 0); } to { clip-path:inset(0 0 0 0); } }
    @media (prefers-reduced-motion:reduce) { .sweep { animation:none; } }
  </style>

  <g class="mono">
    <text class="title" x="500" y="52" text-anchor="middle">${TITLE}</text>

    <g class="axis">
      ${grid}
    </g>
    <line class="base" x1="${L}" y1="${BOT}" x2="${R}" y2="${BOT}"/>

    <g class="sweep">
      <path class="area" d="${area}"/>
      <path class="line" d="${line}"/>
      <g class="dot">${dots}</g>
    </g>

    <g class="axis">
      ${xLabels}
    </g>
  </g>
</svg>
`;
}

const { writeFileSync, mkdirSync } = await import("node:fs");
mkdirSync("assets/dark", { recursive: true });
writeFileSync("assets/activity.svg", buildSvg("#000000"));
writeFileSync("assets/dark/activity.svg", buildSvg("#FFFFFF"));
console.log(`wrote assets/activity.svg + assets/dark/activity.svg — ${days.length} days, peak:${peak}, y-scale:0..${scale}`);
