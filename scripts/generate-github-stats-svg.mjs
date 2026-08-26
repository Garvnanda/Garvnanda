// Regenerates assets/github-stats.svg from live GitHub data: stars, PRs, issues,
// commits this year, and languages by repo (counted by each repo's primary
// language, same unit the 3D contribution calendar's own legend uses, so the
// two panels agree). Run via GitHub Action on a schedule.

const USERNAME = process.env.GH_USERNAME || "Garvnanda";
const TOKEN = process.env.GITHUB_TOKEN;
const YEAR = new Date().getUTCFullYear();

const headers = { "User-Agent": "github-stats-widget", Accept: "application/vnd.github+json" };
if (TOKEN) headers.Authorization = `Bearer ${TOKEN}`;

async function get(url) {
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`GitHub API ${res.status} on ${url}: ${await res.text()}`);
  return res.json();
}

async function getAllPages(url) {
  const items = [];
  let page = 1;
  for (;;) {
    const sep = url.includes("?") ? "&" : "?";
    const batch = await get(`${url}${sep}per_page=100&page=${page}`);
    items.push(...batch);
    if (batch.length < 100) break;
    page++;
  }
  return items;
}

const repos = await getAllPages(`https://api.github.com/users/${USERNAME}/repos?type=owner&sort=pushed`);
// Exclude forks and the profile repo itself (its "language" is badge/workflow plumbing, not real project work).
const owned = repos.filter((r) => !r.fork && r.name.toLowerCase() !== USERNAME.toLowerCase());

const stars = owned.reduce((sum, r) => sum + (r.stargazers_count || 0), 0);

const langCounts = {};
for (const r of owned) {
  if (!r.language) continue;
  langCounts[r.language] = (langCounts[r.language] || 0) + 1;
}
const languages = Object.entries(langCounts)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 5);
const maxLang = languages.length ? languages[0][1] : 1;

// Search API has its own strict rate limit (30 req/min) separate from the core quota, so a
// single transient failure is expected occasionally. Retry once; if it still fails, throw —
// letting a bad fetch silently become a committed "0" is worse than the workflow step going red.
async function withRetry(fn) {
  try {
    return await fn();
  } catch {
    await new Promise((r) => setTimeout(r, 3000));
    return await fn();
  }
}

async function searchCount(q) {
  return withRetry(async () => {
    const data = await get(`https://api.github.com/search/issues?q=${encodeURIComponent(q)}`);
    return data.total_count ?? 0;
  });
}

// Raw commit search only counts commits (misses PR opens/issue opens/reviews, and its index
// lags), so it undercounts against the number GitHub actually shows on the contribution graph.
// contributionsCollection is the same source the graph itself is drawn from — ground truth.
async function contributionsThisYear() {
  return withRetry(async () => {
    const query = `query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) { contributionsCollection(from: $from, to: $to) { contributionCalendar { totalContributions } } }
    }`;
    const variables = { login: USERNAME, from: `${YEAR}-01-01T00:00:00Z`, to: `${YEAR}-12-31T23:59:59Z` };
    const res = await fetch("https://api.github.com/graphql", {
      method: "POST",
      headers: { ...headers, "Content-Type": "application/json" },
      body: JSON.stringify({ query, variables }),
    });
    if (!res.ok) throw new Error(`graphql ${res.status}`);
    const { data, errors } = await res.json();
    if (errors) throw new Error(`graphql: ${errors.map((e) => e.message).join("; ")}`);
    return data.user.contributionsCollection.contributionCalendar.totalContributions;
  });
}

const [pullRequests, issues, contributionsYear, publicRepos] = await Promise.all([
  searchCount(`author:${USERNAME} type:pr`),
  searchCount(`author:${USERNAME} type:issue`),
  contributionsThisYear(),
  get(`https://api.github.com/users/${USERNAME}`).then((u) => u.public_repos),
]);

const esc = (s = "") => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function statRow(y, label, value) {
  return `<text x="52" y="${y}" font-size="13" letter-spacing="1">${esc(label)}</text><text x="436" y="${y}" font-size="15" text-anchor="end">${value}</text>`;
}

function langRow(i, name, count) {
  const y = 94 + i * 36;
  const textY = 105 + i * 36;
  const width = Math.max(2, Math.round((count / maxLang) * 270));
  const delay = i === 0 ? "" : ` g${i + 1}`;
  return `<text x="548" y="${textY}" font-size="12">${esc(name.toUpperCase())}</text><rect class="bar" x="660" y="${y}" width="270" height="12"/><rect class="fill grow${delay}" x="660" y="${y}" width="${width}" height="12"/>`;
}

function buildSvg(ink) {
  const langRows = languages.map(([name, count], i) => langRow(i, name, count)).join("\n    ");
  return `<svg viewBox="0 0 1000 310" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GitHub statistics and repository languages">
  <style>
    :root { --ink:${ink}; }
    .mono { font-family:ui-monospace,"SFMono-Regular","SF Mono",Menlo,Consolas,"Liberation Mono",monospace; fill:var(--ink); }
    .panel,.rule,.bar { fill:none; stroke:var(--ink); stroke-width:1; }
    .fill { fill:var(--ink); }
    .grow { transform:scaleX(0); transform-origin:left; animation:grow .8s cubic-bezier(.2,.7,.2,1) forwards; }
    .g2{animation-delay:.1s}.g3{animation-delay:.2s}.g4{animation-delay:.3s}.g5{animation-delay:.4s}
    @keyframes grow { to { transform:scaleX(1); } }
    @media (prefers-reduced-motion:reduce) { .grow { animation:none; transform:scaleX(1); } }
  </style>
  <rect class="panel" x="24" y="20" width="456" height="270" rx="2"/>
  <rect class="panel" x="520" y="20" width="456" height="270" rx="2"/>

  <g class="mono">
    <text x="52" y="58" font-size="17" font-weight="700" letter-spacing="2">GITHUB STATS</text>
    <line class="rule" x1="52" y1="72" x2="452" y2="72"/>
    ${statRow(110, "TOTAL STARS", stars)}
    ${statRow(146, `${YEAR} CONTRIBUTIONS`, contributionsYear)}
    ${statRow(182, "TOTAL PULL REQUESTS", pullRequests)}
    ${statRow(218, "TOTAL ISSUES", issues)}
    ${statRow(254, "PUBLIC REPOSITORIES", publicRepos)}

    <text x="548" y="58" font-size="17" font-weight="700" letter-spacing="2">LANGUAGES BY REPOSITORY</text>
    <line class="rule" x1="548" y1="72" x2="948" y2="72"/>
    ${langRows}
  </g>
</svg>
`;
}

const { writeFileSync, mkdirSync } = await import("node:fs");
mkdirSync("assets/dark", { recursive: true });
writeFileSync("assets/github-stats.svg", buildSvg("#000000"));
writeFileSync("assets/dark/github-stats.svg", buildSvg("#FFFFFF"));
console.log(
  `wrote assets/github-stats.svg + assets/dark/github-stats.svg — stars:${stars} prs:${pullRequests} issues:${issues} contributions:${contributionsYear} repos:${publicRepos} langs:${languages.map((l) => l.join(":")).join(",")}`,
);
