// Regenerates assets/activity.svg — the last 31 days of contributions as a line +
// area chart, with a bordered panel, gridlines, per-day dots, three date labels and a
// totals row underneath.
//
// This replaced github-readme-activity-graph.vercel.app, which the README used to
// embed. That deployment now answers 402 DEPLOYMENT_DISABLED for every URL including
// its own root — permanently gone, along with its two earlier free-tier mirrors — so
// the panel is drawn locally instead of depending on a host someone else can switch
// off.
//
// Text sizing: font-size here is set relative to the viewBox width, not an absolute
// pixel count — GitHub scales the whole SVG to fit the README column, so what actually
// reads on screen is that ratio. This panel targets ~1.7% for body text and ~2.4% for
// the title, above every other widget in the profile (commits.svg, the previous
// highest, sits at ~1.6%) — deliberately, since this is the panel that kept coming
// back illegible at the profile's usual ~1.0-1.3%.
//
// Source is contributionsCollection, the same query the GitHub Stats widget uses and
// the same one GitHub's own contribution graph is drawn from, so the panels agree.

const USERNAME = process.env.GH_USERNAME || "Garvnanda";
const TOKEN = process.env.GITHUB_TOKEN;
const DAYS = 31;

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
    const all = data.user.contributionsCollection.contributionCalendar.weeks
      .flatMap((w) => w.contributionDays)
      .filter((d) => d.date <= to.toISOString().slice(0, 10))
      .sort((a, b) => a.date.localeCompare(b.date));
    return all.slice(-DAYS);
  });
}

const days = await contributionDays();
if (!days.length) throw new Error("contribution calendar came back empty");

const counts = days.map((d) => d.contributionCount);
const total = counts.reduce((a, b) => a + b, 0);
const peak = Math.max(...counts);
const peakDay = days[counts.indexOf(peak)].date;
const avg = (total / days.length).toFixed(1);

// 1000x480 canvas — same viewBox width as every other widget (so file sizes stay
// comparable across the profile), but noticeably taller, so the chart itself has real
// vertical room instead of being squeezed into a flat banner.
const L = 76, R = 948, TOP = 120, BOT = 380;
const scale = Math.max(1, peak);
const px = (i) => L + (i * (R - L)) / Math.max(1, days.length - 1);
const py = (v) => BOT - (v / scale) * (BOT - TOP);

const points = counts.map((v, i) => [px(i), py(v)]);
const line = points.map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)},${y.toFixed(1)}`).join(" ");
const area = `${line} L${R},${BOT} L${L},${BOT} Z`;
const dots = points.map(([x, y]) => `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3.4"/>`).join("");

const MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
const label = (iso) => {
  const d = new Date(`${iso}T00:00:00Z`);
  return `${MONTHS[d.getUTCMonth()]} ${d.getUTCDate()}`;
};

const midIdx = Math.floor((days.length - 1) / 2);
const ticks = [
  [0, "start"],
  [midIdx, "middle"],
  [days.length - 1, "end"],
].map(([i, anchor]) => `<text x="${px(i).toFixed(1)}" y="404" font-size="17" letter-spacing="1" text-anchor="${anchor}" opacity=".8">${label(days[i].date)}</text>`)
  .join("\n    ");

const summary = `${days.length} DAYS &#183; ${total} CONTRIBUTIONS &#183; PEAK ${peak} ON ${label(peakDay)} &#183; AVG ${avg}/DAY`;

function buildSvg(ink) {
  return `<svg viewBox="0 0 1000 480" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Contribution activity over the last ${days.length} days">
  <style>
    :root { --ink:${ink}; }
    .mono { font-family:ui-monospace,"SFMono-Regular","SF Mono",Menlo,Consolas,"Liberation Mono",monospace; fill:var(--ink); }
    .panel,.rule { fill:none; stroke:var(--ink); stroke-width:1; }
    .grid { stroke:var(--ink); stroke-width:1; opacity:.22; stroke-dasharray:3 6; }
    .area { fill:var(--ink); opacity:.13; }
    .line { fill:none; stroke:var(--ink); stroke-width:3; stroke-linejoin:round; stroke-linecap:round; }
    .dot { fill:var(--ink); }
    .sweep { animation:sweep 1.2s cubic-bezier(.4,0,.2,1) forwards; }
    @keyframes sweep { from { clip-path:inset(0 100% 0 0); } to { clip-path:inset(0 0 0 0); } }
    @media (prefers-reduced-motion:reduce) { .sweep { animation:none; } }
  </style>
  <rect class="panel" x="24" y="20" width="952" height="440" rx="3"/>

  <g class="mono">
    <text x="52" y="64" font-size="24" font-weight="700" letter-spacing="3">CONTRIBUTION TELEMETRY</text>
    <text x="948" y="64" font-size="15" letter-spacing="2" text-anchor="end" opacity=".8">LAST ${days.length} DAYS</text>
    <line class="rule" x1="52" y1="84" x2="948" y2="84"/>

    <line class="grid" x1="${L}" y1="${TOP}" x2="${R}" y2="${TOP}"/>
    <line class="grid" x1="${L}" y1="${(TOP + BOT) / 2}" x2="${R}" y2="${(TOP + BOT) / 2}"/>
    <line class="rule" x1="${L}" y1="${BOT}" x2="${R}" y2="${BOT}"/>

    <text x="66" y="${TOP + 6}" font-size="17" text-anchor="end" opacity=".8">${scale}</text>
    <text x="66" y="${BOT + 6}" font-size="17" text-anchor="end" opacity=".8">0</text>

    <g class="sweep">
      <path class="area" d="${area}"/>
      <path class="line" d="${line}"/>
      <g class="dot">${dots}</g>
    </g>

    ${ticks}

    <text x="52" y="440" font-size="17" letter-spacing="1" opacity=".8">${summary}</text>
  </g>
</svg>
`;
}

const { writeFileSync, mkdirSync } = await import("node:fs");
mkdirSync("assets/dark", { recursive: true });
writeFileSync("assets/activity.svg", buildSvg("#000000"));
writeFileSync("assets/dark/activity.svg", buildSvg("#FFFFFF"));
console.log(`wrote assets/activity.svg + assets/dark/activity.svg — ${days.length} days, total:${total} peak:${peak} on ${peakDay} avg:${avg}`);
