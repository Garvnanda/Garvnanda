import { Chess } from "chess.js";
import { THEME, svgHeaders, esc } from "./svg.js";

const KEY = "chess:fen";

const VALUES = { p: 1, n: 3, b: 3, r: 5, q: 9, k: 0 };

async function getGame(env) {
  const fen = await env.PROFILE_KV.get(KEY);
  const game = new Chess();
  if (fen) {
    try {
      game.load(fen);
    } catch {
      /* corrupt state — start fresh */
    }
  }
  return game;
}

async function saveGame(env, game) {
  await env.PROFILE_KV.put(KEY, game.fen());
}

// Greedy one-ply reply: prefer captures by material gain, else a random legal move.
function pickReply(game) {
  const moves = game.moves({ verbose: true });
  if (!moves.length) return null;
  let best = null;
  let bestScore = -Infinity;
  for (const m of moves) {
    const score = m.captured ? VALUES[m.captured] : 0;
    if (score > bestScore) {
      bestScore = score;
      best = m;
    }
  }
  return bestScore > 0 ? best : moves[Math.floor(Math.random() * moves.length)];
}

export async function handleChess(request, env, path) {
  if (path === "/chess/board.svg") {
    const game = await getGame(env);
    return new Response(renderBoard(game), { headers: svgHeaders() });
  }

  if (path === "/chess/moves") {
    const game = await getGame(env);
    const moves = game.moves();
    return new Response(movesPage(moves, game), { headers: { "Content-Type": "text/html; charset=utf-8" } });
  }

  if (path === "/chess/legal-moves.json") {
    const game = await getGame(env);
    const verbose = game.moves({ verbose: true });
    const moves = verbose.map((m) => ({ uci: m.from + m.to + (m.promotion || ""), san: m.san }));
    const body = JSON.stringify({
      turn: game.turn() === "w" ? "white" : "black",
      gameOver: game.isGameOver(),
      moves,
    });
    return new Response(body, {
      headers: { "Content-Type": "application/json", "Cache-Control": "no-store, max-age=0", "Access-Control-Allow-Origin": "*" },
    });
  }

  if (path === "/chess/move") {
    const url = new URL(request.url);
    const uci = url.searchParams.get("uci") || "";
    const game = await getGame(env);

    if (game.isGameOver()) {
      const fresh = new Chess();
      await saveGame(env, fresh);
      return Response.redirect(env.PROFILE_URL || "https://github.com/", 302);
    }

    const from = uci.slice(0, 2);
    const to = uci.slice(2, 4);
    const promotion = uci.slice(4, 5) || "q";

    try {
      const move = game.move({ from, to, promotion });
      if (move && !game.isGameOver()) {
        const reply = pickReply(game);
        if (reply) game.move(reply);
      }
      await saveGame(env, game);
    } catch {
      // illegal move — ignore, board unchanged
    }

    return Response.redirect(env.PROFILE_URL || "https://github.com/", 302);
  }

  return new Response("not found", { status: 404 });
}

function movesPage(moves, game) {
  const status = game.isGameOver() ? "game over — next move resets the board" : `${game.turn() === "w" ? "white" : "black"} to move`;
  const links = moves
    .map((san) => {
      const verbose = game.moves({ verbose: true }).find((m) => m.san === san);
      const uci = verbose ? verbose.from + verbose.to + (verbose.promotion || "") : "";
      return `<a href="/chess/move?uci=${uci}" style="margin:4px;display:inline-block;padding:6px 10px;background:#000;color:#fff;text-decoration:none;font-family:ui-monospace,monospace">${esc(san)}</a>`;
    })
    .join("");
  return `<!doctype html><html><head><meta charset="utf-8"><title>Legal moves</title></head>
<body style="font-family:ui-monospace,monospace;max-width:640px;margin:48px auto">
<p>${esc(status)}</p>
<div>${links || "no legal moves"}</div>
<p><a href="https://github.com/Garvnanda">Back to profile</a></p>
</body></html>`;
}

function renderBoard(game) {
  const size = 480;
  const sq = size / 8;
  const board = game.board(); // 8x8, [0]=rank8..[7]=rank1
  let squares = "";
  let pieces = "";

  const glyph = { p: "♟", n: "♞", b: "♝", r: "♜", q: "♛", k: "♚", P: "♙", N: "♘", B: "♗", R: "♖", Q: "♕", K: "♔" };

  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      const dark = (r + c) % 2 === 1;
      const x = c * sq;
      const y = r * sq;
      squares += `<rect x="${x}" y="${y}" width="${sq}" height="${sq}" fill="${dark ? "var(--rule)" : "var(--paper)"}"/>`;
      const piece = board[r][c];
      if (piece) {
        const ch = piece.color === "w" ? piece.type.toUpperCase() : piece.type;
        pieces += `<text x="${x + sq / 2}" y="${y + sq / 2 + sq * 0.16}" font-size="${sq * 0.62}" text-anchor="middle" fill="var(--bone)">${glyph[ch]}</text>`;
      }
    }
  }

  return `<svg viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Chess board">
  <style>${THEME}</style>
  ${squares}
  ${pieces}
</svg>`;
}
