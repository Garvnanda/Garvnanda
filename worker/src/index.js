import { handleTtt } from "./ttt.js";
import { handleGuestbook } from "./guestbook.js";
import { handleChess } from "./chess.js";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    try {
      if (path.startsWith("/ttt/")) return handleTtt(request, env, path);
      if (path.startsWith("/guestbook/")) return handleGuestbook(request, env, path);
      if (path.startsWith("/chess/")) return handleChess(request, env, path);
      return new Response("garvnanda-profile worker: ok", { status: 200 });
    } catch (err) {
      return new Response(`error: ${err.message}`, { status: 500 });
    }
  },
};
