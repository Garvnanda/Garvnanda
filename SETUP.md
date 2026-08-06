# Setup

## 1. Push this to the `Garvnanda/Garvnanda` repo
GitHub renders `README.md` as the profile page when the repo name matches your username.

## 2. Commits widget (`assets/commits.svg`)
Works out of the box — `.github/workflows/commits-widget.yml` runs hourly using the default `GITHUB_TOKEN`, no secret needed.

## 3. Interactive widgets (tic-tac-toe / guestbook / chess)
Deployed as a Cloudflare Worker — see `worker/README.md`. Live at `https://garvnanda-profile.garvnanda.workers.dev`. Redeploy after any change under `worker/`:

```
cd worker
npx wrangler deploy
```

## 4. Chess move panel (README §"Play me at Chess")
The board and every legal-move badge are baked directly into `README.md` between `<!-- CHESS_START -->` / `<!-- CHESS_END -->` markers — no separate "view moves" link. `.github/workflows/chess-widget.yml` regenerates this section from the worker's `/chess/legal-moves.json`.

## 5. `GH_DISPATCH_TOKEN` — makes the chess badges refresh immediately (required)
Without this the panel only refreshes on the cron, and GitHub throttles scheduled
runs hard — a `*/5` cron was actually being delivered about 12 times a day. Between
ticks the badges point at moves that are no longer legal, the worker silently drops
them, and the board looks stuck after one move.

`pingReadmeRefresh()` in `worker/src/chess-handler.js` fires a `repository_dispatch`
after every move to rebuild the panel right away, but it is a **no-op until this
secret exists**. To enable it:

1. Create a fine-grained personal access token scoped to the `Garvnanda/Garvnanda`
   repository with **Contents: read and write** (classic tokens: the `repo` scope).
2. Store it on the worker — this prompts for the value, so the token never lands in
   a file or in shell history:

   ```
   cd worker
   npx wrangler secret put GH_DISPATCH_TOKEN
   ```

3. Confirm it took effect: play one move from the README, then check the Actions tab
   for an "Update chess panel" run with a **repository_dispatch** trigger. If every
   recent run still says `schedule`, the secret is not being read.

`GH_REPO` is already set in `worker/wrangler.toml`; both it and the token must be
present or the ping stays a no-op.
