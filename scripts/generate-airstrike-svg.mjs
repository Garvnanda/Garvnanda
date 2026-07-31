// Renders a GitHub-style contribution grid where a plane flies over and "bombs" each
// contributed day in ascending order of commit count — cell flips to red on hit, plane
// keeps flying and exits right after the last (highest-count) day is hit.
//
// Needs a token with `read:user` scope (contributionsCollection isn't reachable with the
// default Actions GITHUB_TOKEN) — see .github/workflows/airstrike-widget.yml.

const USERNAME = process.env.GH_USERNAME || "Garvnanda";
const TOKEN = process.env.CONTRIB_TOKEN || process.env.GITHUB_TOKEN;
if (!TOKEN) throw new Error("Missing CONTRIB_TOKEN (needs read:user scope)");

const query = `
  query($login: String!) {
    user(login: $login) {
      contributionsCollection {
        contributionCalendar {
          weeks {
            contributionDays { date contributionCount weekday }
          }
        }
      }
    }
  }
`;

const res = await fetch("https://api.github.com/graphql", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${TOKEN}`,
    "Content-Type": "application/json",
    "User-Agent": "airstrike-widget",
  },
  body: JSON.stringify({ query, variables: { login: USERNAME } }),
});
if (!res.ok) throw new Error(`GraphQL ${res.status}: ${await res.text()}`);
const json = await res.json();
if (json.errors) throw new Error(`GraphQL errors: ${JSON.stringify(json.errors)}`);

const weeks = json.data.user.contributionsCollection.contributionCalendar.weeks;

const CELL = 11;
const GAP = 3;
const STEP = CELL + GAP;
const MARGIN_TOP = 28;
const MARGIN_LEFT = 8;

const days = [];
weeks.forEach((week, wi) => {
  week.contributionDays.forEach((d) => {
    days.push({ ...d, wi, x: MARGIN_LEFT + wi * STEP, y: MARGIN_TOP + d.weekday * STEP });
  });
});

const maxCount = Math.max(1, ...days.map((d) => d.contributionCount));
function level(count) {
  if (count === 0) return 0;
  const q = count / maxCount;
  if (q > 0.75) return 4;
  if (q > 0.5) return 3;
  if (q > 0.25) return 2;
  return 1;
}
const GREEN = ["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"];

// Bombable = days with at least one contribution, ascending by count (ties by date).
const bombable = days
  .filter((d) => d.contributionCount > 0)
  .sort((a, b) => a.contributionCount - b.contributionCount || a.date.localeCompare(b.date));

const N = bombable.length;
const TARGET_FLIGHT = 16; // seconds, total time to bomb every cell
const perCellDelay = N ? Math.min(0.35, Math.max(0.04, TARGET_FLIGHT / N)) : 0;
const lastHit = N ? (N - 1) * perCellDelay : 0;
const flyOffDuration = 1.5;
const totalDuration = lastHit + flyOffDuration + 0.6;

const width = MARGIN_LEFT + weeks.length * STEP + 8;
const height = MARGIN_TOP + 7 * STEP + 8;

const baseCells = days
  .map((d) => `<rect x="${d.x}" y="${d.y}" width="${CELL}" height="${CELL}" rx="2" fill="${GREEN[level(d.contributionCount)]}"/>`)
  .join("\n  ");

const hitCells = bombable
  .map((d, i) => {
    const delay = (i * perCellDelay).toFixed(3);
    return `<rect class="hit" style="animation-delay:${delay}s" x="${d.x}" y="${d.y}" width="${CELL}" height="${CELL}" rx="2" fill="#DA3633"/>`;
  })
  .join("\n  ");

const bursts = bombable
  .map((d, i) => {
    const delay = (i * perCellDelay).toFixed(3);
    const cx = d.x + CELL / 2;
    const cy = d.y + CELL / 2;
    return `<circle class="burst" style="animation-delay:${delay}s" cx="${cx}" cy="${cy}" r="1"/>`;
  })
  .join("\n  ");

const planeY = MARGIN_TOP - 14;
const plane = `
  <g class="plane">
    <path d="M -14 4 L 4 0 L -14 -4 L -8 0 Z" fill="var(--bone)"/>
  </g>
`;

const svg = `<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Contribution airstrike">
  <style>
    :root { --bone:#444444; --muted:#888888; }
    @media (prefers-color-scheme: dark) { :root { --bone:#DDDDDD; --muted:#777777; } }
    .mono { font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }
    .hit { opacity: 0; animation: hit .2s ease forwards; }
    @keyframes hit { to { opacity: 1; } }
    .burst { fill: none; stroke: #DA3633; stroke-width: 1; opacity: 0; animation: burst .5s ease-out forwards; }
    @keyframes burst { 0% { r: 1; opacity: .9; } 100% { r: 9; opacity: 0; } }
    .plane { offset-path: path("M -20 ${planeY} C 250 ${planeY - 10}, 500 ${planeY + 12}, ${width + 20} ${planeY}"); animation: fly ${totalDuration}s linear forwards; offset-rotate: 0deg; }
    @keyframes fly { to { offset-distance: 100%; } }
    @media (prefers-reduced-motion: reduce) { .hit { animation: none; opacity: 1; } .burst { display: none; } .plane { display: none; } }
  </style>

  <text class="mono" x="${MARGIN_LEFT}" y="16" font-size="10" fill="var(--muted)" letter-spacing="2">CONTRIBUTION AIRSTRIKE — ${N} DAYS TARGETED</text>

  ${baseCells}
  ${hitCells}
  ${bursts}
  ${plane}
</svg>
`;

const { writeFileSync, mkdirSync } = await import("node:fs");
mkdirSync("assets", { recursive: true });
writeFileSync("assets/airstrike.svg", svg);
console.log(`wrote assets/airstrike.svg — ${N} bombable cells, ${totalDuration.toFixed(1)}s flight`);
