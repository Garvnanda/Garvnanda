#!/usr/bin/env bash
#
# Chooses the git identity for an automated widget commit.
#
# The profile repo commits ~16 times a day from scheduled workflows. Attributing
# all of them to the repo owner turned every one into a contribution-graph entry
# (~18/day), which says nothing about actual work. This script attributes exactly
# one automated commit per UTC day to the owner and the rest to github-actions[bot],
# whose commits GitHub does not count.
#
# There is no schedule and no stored state: whichever workflow commits first on a
# given UTC day claims the owner slot, and every later commit that day sees a
# non-zero count and falls through to the bot. Dropped or delayed workflow runs
# therefore cost nothing -- the next commit of the day takes the slot instead.
#
# Prints "<name>|<email>" on stdout. Any failure -- missing token, network error,
# rate limit, unexpected response -- falls back to the bot identity, because a
# missed contribution is much cheaper to live with than a run that mistakenly
# attributes a whole day of automated commits to the owner.
#
# Requires GITHUB_TOKEN and GITHUB_REPOSITORY in the environment.

set -uo pipefail

OWNER_LOGIN="Garvnanda"
OWNER_NAME="Garvnanda"
OWNER_EMAIL="184491525+Garvnanda@users.noreply.github.com"
BOT_NAME="github-actions[bot]"
BOT_EMAIL="41898282+github-actions[bot]@users.noreply.github.com"

use_bot() {
  printf '%s|%s\n' "$BOT_NAME" "$BOT_EMAIL"
  exit 0
}

[ -n "${GITHUB_TOKEN:-}" ] || use_bot
[ -n "${GITHUB_REPOSITORY:-}" ] || use_bot

# Commits are matched by account login rather than a literal address so that any
# email attached to the account counts -- including real hand-made commits pushed
# to this repo, which should consume the day's slot just like an automated one.
# per_page=1 keeps the response tiny; only zero-vs-nonzero matters here.
since="$(date -u +%Y-%m-%dT00:00:00Z)"
url="https://api.github.com/repos/${GITHUB_REPOSITORY}/commits?since=${since}&author=${OWNER_LOGIN}&per_page=1"

response="$(curl --silent --show-error --fail --max-time 20 \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -H "User-Agent: garvnanda-profile-pick-author" \
  "$url" 2>/dev/null)" || use_bot

# Deliberately no jq: it is not guaranteed on every runner image, and a missing
# parser would pin this to the bot forever without ever failing loudly. With
# per_page=1 the only success shapes are "[]" (no commits yet today) and a
# one-element array, so stripped-string matching is enough. An error object,
# truncated body or anything unrecognised falls through to the bot.
case "$(printf '%s' "$response" | tr -d '[:space:]')" in
  "[]")  printf '%s|%s\n' "$OWNER_NAME" "$OWNER_EMAIL" ;;
  "[{"*) use_bot ;;
  *)     use_bot ;;
esac
