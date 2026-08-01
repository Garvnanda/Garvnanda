// Regenerates assets/commits.svg from the user's recent public push events.
// Run via GitHub Action (.github/workflows/commits-widget.yml) on a schedule.

const USERNAME = process.env.GH_USERNAME || "Garvnanda";
const TOKEN = process.env.GITHUB_TOKEN;
const MAX_ROWS = 6;

const headers = { "User-Agent": "commits-widget", Accept: "application/vnd.github+json" };
if (TOKEN) headers.Authorization = `Bearer ${TOKEN}`;

const res = await fetch(`https://api.github.com/users/${USERNAME}/events/public?per_page=30`, { headers });
if (!res.ok) throw new Error(`GitHub API ${res.status}: ${await res.text()}`);
const events = await res.json();

const rows = [];
for (const ev of events) {
  if (rows.length >= MAX_ROWS) break;
  if (ev.type !== "PushEvent") continue;
  const repo = ev.repo.name.split("/")[1];

  if (ev.payload?.commits?.length) {
    for (const c of ev.payload.commits) {
      if (rows.length >= MAX_ROWS) break;
      rows.push({ repo, msg: c.message.split("\n")[0].slice(0, 52) });
    }
    continue;
  }

  // GitHub omits the commits array for unauthenticated/anon requests — fall back to fetching by sha.
  const sha = ev.payload?.head;
  if (!sha) continue;
  const cRes = await fetch(`https://api.github.com/repos/${ev.repo.name}/commits/${sha}`, { headers });
  if (!cRes.ok) continue;
  const commit = await cRes.json();
  const msg = commit?.commit?.message?.split("\n")[0]?.slice(0, 52);
  if (msg) rows.push({ repo, msg });
}
while (rows.length < MAX_ROWS) rows.push({ repo: "", msg: "" });

const rowH = 24;
const top = 92;
const width = 760;
const height = top + rows.length * rowH + 24;

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const lines = rows
  .map((r, i) => {
    if (!r.repo) return "";
    const y = top + i * rowH;
    return `<text class="mono row" style="animation-delay:${(i * 0.08).toFixed(2)}s" x="24" y="${y}" font-size="13"><tspan fill="var(--accent)">${esc(r.repo)}</tspan><tspan fill="var(--dim)"> — </tspan><tspan fill="var(--bone)">${esc(r.msg)}</tspan></text>`;
  })
  .join("\n  ");

function buildSvg(vars) {
  return `<svg viewBox="0 0 ${width} ${height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Recent commits">
  <style>
    :root { --win: ${vars.win}; --bar: ${vars.bar}; --bone: ${vars.bone}; --dim: ${vars.dim}; --accent: ${vars.accent}; --rule: ${vars.rule}; }
    .mono { font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }
    .row { opacity: 0; animation: rise .5s ease forwards; }
    @keyframes rise { from { opacity: 0; transform: translateX(-4px); } to { opacity: 1; transform: translateX(0); } }
    @media (prefers-reduced-motion: reduce) { .row { animation: none; opacity: 1; } }
  </style>

  <rect x="0" y="0" width="${width}" height="${height}" rx="10" fill="var(--win)" stroke="var(--rule)"/>
  <rect x="0" y="0" width="${width}" height="36" rx="10" fill="var(--bar)"/>
  <rect x="0" y="26" width="${width}" height="10" fill="var(--bar)"/>
  <circle cx="22" cy="18" r="6" fill="#FF5F56"/>
  <circle cx="42" cy="18" r="6" fill="#FFBD2E"/>
  <circle cx="62" cy="18" r="6" fill="#27C93F"/>
  <text class="mono" x="${width / 2}" y="22" font-size="12" fill="var(--dim)" text-anchor="middle">garv@github — zsh</text>

  <text class="mono" x="24" y="60" font-size="13" fill="var(--accent)">garv@github <tspan fill="var(--dim)">~</tspan> % <tspan fill="var(--bone)">git log --oneline -${MAX_ROWS}</tspan></text>

  ${lines}
</svg>
`;
}

const LIGHT = { win: "#FFFFFF", bar: "#F0F0F0", bone: "#000000", dim: "#000000", accent: "#000000", rule: "#000000" };
const DARK = { win: "#0D1117", bar: "#161B22", bone: "#FFFFFF", dim: "#FFFFFF", accent: "#FFFFFF", rule: "#FFFFFF" };

const { writeFileSync, mkdirSync } = await import("node:fs");
mkdirSync("assets/dark", { recursive: true });
writeFileSync("assets/commits.svg", buildSvg(LIGHT));
writeFileSync("assets/dark/commits.svg", buildSvg(DARK));
console.log(`wrote assets/commits.svg + assets/dark/commits.svg with ${rows.filter((r) => r.repo).length} commit rows`);
