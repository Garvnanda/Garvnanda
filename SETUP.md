# Setup

## 1. Push this to the `Garvnanda/Garvnanda` repo
GitHub renders `README.md` as the profile page when the repo name matches your username.

## 2. Commits widget (`assets/commits.svg`)
Works out of the box — `.github/workflows/commits-widget.yml` runs hourly using the default `GITHUB_TOKEN`, no secret needed.

## 3. Interactive widgets (tic-tac-toe / guestbook / chess)
Deployed as a Cloudflare Worker — see `worker/README.md`. Already deployed at `https://garvnanda-profile.garvnanda.workers.dev`, but **needs redeploying** to pick up the bigger chess board (320→480px) and the new `/chess/legal-moves.json` endpoint:

```
cd worker
npx wrangler deploy
```

## 4. Chess move panel (README §"Play me at Chess")
The board and every legal-move badge are baked directly into `README.md` between `<!-- CHESS_START -->` / `<!-- CHESS_END -->` markers — no separate "view moves" link. `.github/workflows/chess-widget.yml` regenerates this section every 15 minutes by calling the worker's `/chess/legal-moves.json`, so it needs the worker redeployed first (step 3), then run the "Update chess panel" workflow once manually (Actions tab → Run workflow) to populate it immediately.
