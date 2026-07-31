# Setup

## 1. Push this to the `Garvnanda/Garvnanda` repo
GitHub renders `README.md` as the profile page when the repo name matches your username.

## 2. Commits widget (`assets/commits.svg`)
Works out of the box — `.github/workflows/commits-widget.yml` runs hourly using the default `GITHUB_TOKEN`, no secret needed.

## 3. Airstrike widget (`assets/airstrike.svg`)
Needs a Personal Access Token with `read:user` scope — the default Actions token can't read contribution data.

1. GitHub → Settings → Developer settings → Personal access tokens → Fine-grained (or classic with `read:user`).
2. Repo → Settings → Secrets and variables → Actions → New repository secret: name it `CONTRIB_TOKEN`, paste the PAT.
3. Run the "Update airstrike widget" workflow once manually (Actions tab → Run workflow) to populate it immediately instead of waiting for the 6-hourly schedule.

## 4. Interactive widgets (tic-tac-toe / guestbook / chess)
Deployed separately as a Cloudflare Worker — see `worker/README.md`. Already deployed at `https://garvnanda-profile.garvnanda.workers.dev`; redeploy with `cd worker && npx wrangler deploy` after any change to `worker/src/`.
