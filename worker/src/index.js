import { handleTtt } from "./ttt.js";
import { handleGuestbook } from "./guestbook.js";
import { handleChess } from "./chess-handler.js";
import { ProfileState } from "./state-do.js";

export { ProfileState };

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Single global DO instance — RPC calls are strongly consistent, no KV propagation lag.
    const id = env.PROFILE_DO.idFromName("singleton");
    const stub = env.PROFILE_DO.get(id);
    const patchedEnv = { ...env, PROFILE_KV: stub };

    try {
      if (path.startsWith("/ttt/")) return handleTtt(request, patchedEnv, path);
      if (path.startsWith("/guestbook/")) return handleGuestbook(request, patchedEnv, path);
      if (path.startsWith("/chess/")) return handleChess(request, patchedEnv, path);
      return new Response("garvnanda-profile worker: ok", { status: 200 });
    } catch (err) {
      return new Response(`error: ${err.message}`, { status: 500 });
    }
  },
};
