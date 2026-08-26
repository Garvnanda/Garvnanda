// Regenerates assets/activity.svg — the last 31 days of contributions as a line +
// area chart with dated gridlines, in the same layout (proportions, axes, line style)
// as haragam22/haragam22's contribution-telemetry.svg, restyled to this profile's
// ink-only black/white theme instead of that panel's fixed dark colors.
//
// This replaced github-readme-activity-graph.vercel.app, which the README used to
// embed. That deployment now answers 402 DEPLOYMENT_DISABLED for every URL including
// its own root — permanently gone, along with its two earlier free-tier mirrors — so
// the panel is drawn locally instead of depending on a host someone else can switch
// off.
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

// 760x240 canvas, chart box at x=40..740 / y=40..210 — same proportions as the
// reference panel, so the axes, tick density and line weight read the same way.
const L = 40, R = 740, TOP = 40, BOT = 210;
const STEPS = 4;
const scale = Math.max(1, peak);
const px = (i) => L + (i * (R - L)) / Math.max(1, days.length - 1);
const py = (v) => BOT - (v / scale) * (BOT - TOP);
const pts = counts.map((v, i) => [px(i), py(v)]);

const line = pts.map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)},${y.toFixed(1)}`).join(" ");
const area = `${line} L${R},${BOT} L${L},${BOT} Z`;

// Ten evenly spaced ticks (first and last always included), showing the bare
// day-of-month the way the reference panel does — no month name, since a 31-day
// window only ever touches at most two months and the crossover is obvious from the
// numbers wrapping past the end of the month.
const TICKS = 10;
const tickIdx = Array.from({ length: TICKS }, (_, i) => Math.round((i * (days.length - 1)) / (TICKS - 1)));
const xLabels = [...new Set(tickIdx)]
  .map((i) => `<text x="${px(i).toFixed(1)}" y="222" font-size="8" text-anchor="middle">${Number(days[i].date.slice(-2))}</text>`)
  .join("\n    ");

const grid = Array.from({ length: STEPS + 1 }, (_, i) => {
  const v = Math.round((scale / STEPS) * i);
  const y = py((scale / STEPS) * i).toFixed(1);
  return `<line class="grid" x1="${L}" y1="${y}" x2="${R}" y2="${y}"/><text class="axis" x="${L - 8}" y="${(Number(y) + 3).toFixed(1)}" font-size="8" text-anchor="end">${v}</text>`;
}).join("\n    ");

function buildSvg(ink) {
  return `<svg viewBox="0 0 760 240" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Contribution activity over the last ${days.length} days">
  <style>
    :root { --ink:${ink}; }
    .mono { font-family:ui-monospace,"SFMono-Regular","SF Mono",Menlo,Consolas,"Liberation Mono",monospace; fill:var(--ink); }
    .title { font-size:13px; font-weight:700; letter-spacing:2px; }
    .axis { opacity:.6; }
    .rule { stroke:var(--ink); stroke-width:1; }
    .grid { stroke:var(--ink); stroke-width:1; opacity:.16; }
    .area { fill:var(--ink); opacity:.12; }
    .line { fill:none; stroke:var(--ink); stroke-width:1.5; stroke-linejoin:round; }
    .sweep { animation:sweep 1.2s cubic-bezier(.4,0,.2,1) forwards; }
    @keyframes sweep { from { clip-path:inset(0 100% 0 0); } to { clip-path:inset(0 0 0 0); } }
    @media (prefers-reduced-motion:reduce) { .sweep { animation:none; } }
  </style>

  <g class="mono">
    <text class="title" x="40" y="24">${TITLE}</text>
    <line class="rule" x1="40" y1="40" x2="740" y2="40"/>

    <g class="axis">
      ${grid}
    </g>

    <g class="sweep">
      <path class="area" d="${area}"/>
      <path class="line" d="${line}"/>
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
