// Regenerates the chess panel in README.md (between CHESS_START/CHESS_END markers) from
// the live Worker's current legal moves — so the board and every clickable move badge are
// baked directly into the profile page itself, not hidden behind a separate link.

const WORKER = process.env.WORKER_URL || "https://garvnanda-profile.garvnanda.workers.dev";
const README = "README.md";

const res = await fetch(`${WORKER}/chess/legal-moves.json`);
if (!res.ok) throw new Error(`legal-moves.json ${res.status}`);
const { turn, gameOver, moves } = await res.json();

const cacheBust = Date.now();
const boardUrl = `${WORKER}/chess/board.svg?v=${cacheBust}`;

function badge(m) {
  const label = `${m.uci.slice(0, 2)}--${m.uci.slice(2, 4)}`;
  return `<a href="${WORKER}/chess/move?uci=${m.uci}"><img src="https://img.shields.io/badge/PLAY-${label}-0d1117?style=for-the-badge&logo=github&logoColor=39D353" alt="Play ${m.san}"/></a>`;
}

const half = Math.ceil(moves.length / 2);
const left = moves.slice(0, half).map(badge).join("<br/><br/>");
const right = moves.slice(half).map(badge).join("<br/><br/>");

const statusLine = gameOver
  ? "game over — next move played anywhere resets the board"
  : `${turn} to move · ${moves.length} legal move${moves.length === 1 ? "" : "s"} shown below`;

const panel = `<!-- CHESS_START -->
<p align="center">
  <b>Click any move badge to play against Garv's AI Bot</b><br/>
  <font color="#8B949E">${statusLine} · replies instantly</font>
</p>

<table border="0">
<tr>
<td align="center" valign="middle">
${left || "&nbsp;"}
</td>
<td align="center" valign="middle" width="560">
<img src="${boardUrl}" alt="GitHub Profile Chess Game" width="480"/>
</td>
<td align="center" valign="middle">
${right || "&nbsp;"}
</td>
</tr>
</table>
<!-- CHESS_END -->`;

const { readFileSync, writeFileSync } = await import("node:fs");
const readme = readFileSync(README, "utf8");
const pattern = /<!-- CHESS_START -->[\s\S]*?<!-- CHESS_END -->/;
if (!pattern.test(readme)) throw new Error("CHESS_START/CHESS_END markers not found in README.md");
writeFileSync(README, readme.replace(pattern, panel));
console.log(`updated chess panel — ${moves.length} moves, ${turn} to move`);
