import { THEME, svgHeaders, esc } from "./svg.js";

const KEY = "ttt:state";
const LINES = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],
  [0, 3, 6], [1, 4, 7], [2, 5, 8],
  [0, 4, 8], [2, 4, 6],
];

function emptyState() {
  return { board: Array(9).fill(null), turn: "X", winner: null };
}

async function getState(env) {
  const raw = await env.PROFILE_KV.get(KEY);
  return raw ? JSON.parse(raw) : emptyState();
}

async function setState(env, state) {
  await env.PROFILE_KV.put(KEY, JSON.stringify(state));
}

function checkWinner(board) {
  for (const [a, b, c] of LINES) {
    if (board[a] && board[a] === board[b] && board[b] === board[c]) return board[a];
  }
  if (board.every(Boolean)) return "draw";
  return null;
}

export async function handleTtt(request, env, path) {
  if (path === "/ttt/board.svg") {
    const state = await getState(env);
    return new Response(renderBoard(state), { headers: svgHeaders() });
  }

  if (path === "/ttt/play") {
    const url = new URL(request.url);
    const cell = Number(url.searchParams.get("cell"));
    let state = await getState(env);

    if (Number.isInteger(cell) && cell >= 0 && cell <= 8 && !state.winner && !state.board[cell]) {
      state.board[cell] = state.turn;
      const winner = checkWinner(state.board);
      if (winner) {
        state.winner = winner;
      } else {
        state.turn = state.turn === "X" ? "O" : "X";
      }
      await setState(env, state);
    } else if (state.winner) {
      // board full / decided — clicking again starts a fresh game
      state = emptyState();
      await setState(env, state);
    }

    return Response.redirect(env.PROFILE_URL || "https://github.com/", 302);
  }

  return new Response("not found", { status: 404 });
}

function renderBoard(state) {
  const { board, winner } = state;
  const size = 180;
  const cell = size / 3;
  let cells = "";
  for (let i = 0; i < 9; i++) {
    const r = Math.floor(i / 3);
    const c = i % 3;
    const x = c * cell + cell / 2;
    const y = r * cell + cell / 2 + 6;
    if (board[i]) {
      cells += `<text class="mono" x="${x}" y="${y}" font-size="34" text-anchor="middle" fill="var(--bone)">${board[i]}</text>`;
    }
  }
  let grid = "";
  for (let i = 1; i < 3; i++) {
    grid += `<line x1="${i * cell}" y1="4" x2="${i * cell}" y2="${size - 4}" stroke="var(--rule)"/>`;
    grid += `<line x1="4" y1="${i * cell}" x2="${size - 4}" y2="${i * cell}" stroke="var(--rule)"/>`;
  }
  const status = winner ? (winner === "draw" ? "draw — click any cell to reset" : `${winner} wins — click any cell to reset`) : `${state.turn}'s turn`;

  return `<svg viewBox="0 0 ${size} ${size + 28}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Tic-tac-toe board">
  <style>${THEME}</style>
  <rect x="0" y="0" width="${size}" height="${size + 28}" fill="none"/>
  ${grid}
  ${cells}
  <text class="mono" x="${size / 2}" y="${size + 20}" font-size="11" fill="var(--muted)" text-anchor="middle">${esc(status)}</text>
</svg>`;
}
