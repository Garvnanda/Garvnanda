# garvnanda-profile worker

Backs the three interactive widgets in the profile README: shared tic-tac-toe, guestbook, and an instant-reply chess board.

## Deploy

```
cd worker
npm install
npx wrangler login
npx wrangler kv namespace create PROFILE_KV
```

Copy the returned `id` into `wrangler.toml` under `kv_namespaces`, then:

```
npx wrangler deploy
```

Wrangler prints your Worker URL, e.g. `https://garvnanda-profile.<subdomain>.workers.dev`.

## Wire it into the README

In `README.md`, replace every `https://garvnanda-profile.garvnanda.workers.dev/` with your actual Worker URL from the deploy output.

## Routes

- `GET /ttt/board.svg` — live board image
- `GET /ttt/play?cell=0-8` — visitor move, redirects to your profile
- `GET /guestbook/wall.svg` — last 8 messages, rendered as SVG
- `GET /guestbook/sign` — HTML form
- `POST /guestbook/submit` — form handler
- `GET /chess/board.svg` — live board image
- `GET /chess/moves` — lists legal moves as clickable links
- `GET /chess/move?uci=e2e4` — applies visitor move, worker replies via a one-ply greedy-capture heuristic, redirects to your profile

All state lives in one KV namespace (`PROFILE_KV`), keyed `ttt:state`, `guestbook:entries`, `chess:fen`.
