// Renders a GitHub-style contribution grid where a plane flies over and "bombs" each
// contributed day in ascending order of commit count — cell flips to red on hit, plane
// keeps flying and exits right after the last (highest-count) day is hit.
//
// Uses SMIL (<animate>/<animateMotion>) instead of CSS animation-path — SMIL is native
// to the SVG spec and renders consistently across GitHub, VS Code's preview, and browsers,
// where CSS `offset-path` support is inconsistent.
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

const CELL = 10;
const GAP = 3;
const STEP = CELL + GAP;
const MARGIN_TOP = 34;
const MARGIN_LEFT = 10;

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

// Bombable = days with at least one contribution, ascending by count (ties by date).
const bombable = days
  .filter((d) => d.contributionCount > 0)
  .sort((a, b) => a.contributionCount - b.contributionCount || a.date.localeCompare(b.date));

const N = bombable.length;
const TARGET_FLIGHT = 16; // seconds, total time to bomb every cell
const perCellDelay = N ? Math.min(0.35, Math.max(0.05, TARGET_FLIGHT / N)) : 0;
const lastHit = N ? (N - 1) * perCellDelay + 0.2 : 0;
const flyOffTail = 1.8;
const totalDuration = Math.max(2, lastHit + flyOffTail);

const width = MARGIN_LEFT + weeks.length * STEP + 8;
const height = MARGIN_TOP + 7 * STEP + 10;

const baseCells = days
  .map((d) => `<rect class="lvl${level(d.contributionCount)}" x="${d.x}" y="${d.y}" width="${CELL}" height="${CELL}" rx="2"/>`)
  .join("\n  ");

const hitCells = bombable
  .map((d, i) => {
    const begin = (i * perCellDelay).toFixed(3);
    return `<rect class="hit" x="${d.x}" y="${d.y}" width="${CELL}" height="${CELL}" rx="2" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="${begin}s" dur="0.15s" fill="freeze"/></rect>`;
  })
  .join("\n  ");

const bursts = bombable
  .map((d, i) => {
    const begin = (i * perCellDelay).toFixed(3);
    const cx = d.x + CELL / 2;
    const cy = d.y + CELL / 2;
    return `<circle class="burst" cx="${cx}" cy="${cy}" r="1" opacity="0"><animate attributeName="r" from="1" to="11" begin="${begin}s" dur="0.45s" fill="freeze"/><animate attributeName="opacity" from=".9" to="0" begin="${begin}s" dur="0.45s" fill="freeze"/></circle>`;
  })
  .join("\n  ");

const planeY = MARGIN_TOP - 18;
const planePath = `M -24 ${planeY} C ${width * 0.25} ${planeY - 12}, ${width * 0.55} ${planeY + 14}, ${width + 30} ${planeY}`;

const svg = `<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Contribution airstrike">
  <style>
    :root {
      --bg: #FFFFFF; --muted: #57606A; --bone: #24292F;
      --lvl0: #EBEDF0; --lvl1: #9BE9A8; --lvl2: #40C463; --lvl3: #30A14E; --lvl4: #216E39;
      --smoke: #6E7781;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #0D1117; --muted: #8B949E; --bone: #C9D1D9;
        --lvl0: #161B22; --lvl1: #0E4429; --lvl2: #006D32; --lvl3: #26A641; --lvl4: #39D353;
        --smoke: #8B949E;
      }
    }
    .mono { font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }
    .lvl0 { fill: var(--lvl0); } .lvl1 { fill: var(--lvl1); } .lvl2 { fill: var(--lvl2); }
    .lvl3 { fill: var(--lvl3); } .lvl4 { fill: var(--lvl4); }
    .hit { fill: #DA3633; }
    .burst { fill: none; stroke: #F85149; stroke-width: 1.2; }
    .plane-wrap { fill: var(--bone); }
  </style>

  <rect x="0" y="0" width="${width}" height="${height}" fill="var(--bg)"/>
  <text class="mono" x="${MARGIN_LEFT}" y="18" font-size="10.5" fill="var(--muted)" letter-spacing="2">CONTRIBUTION AIRSTRIKE — ${N} DAYS TARGETED, LOWEST FIRST</text>

  ${baseCells}
  ${hitCells}
  ${bursts}

  <g class="plane-wrap">
    <path d="M -13 4 L 5 0 L -13 -4 L -7 0 Z"/>
    <animateMotion path="${planePath}" begin="0s" dur="${totalDuration}s" fill="freeze"/>
  </g>
</svg>
`;

const { writeFileSync, mkdirSync } = await import("node:fs");
mkdirSync("assets", { recursive: true });
writeFileSync("assets/airstrike.svg", svg);
console.log(`wrote assets/airstrike.svg — ${N} bombable cells, ${totalDuration.toFixed(1)}s flight`);
