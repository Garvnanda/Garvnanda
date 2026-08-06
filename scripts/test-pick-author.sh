#!/usr/bin/env bash
#
# Self-check for pick-author.sh. Fakes the GitHub API with a curl shim placed
# ahead of the real one on PATH, then asserts the identity picked for each
# response shape -- especially the failure shapes, where anything other than the
# bot would silently attribute a day of automated commits to the owner.
#
# Run: bash scripts/test-pick-author.sh

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SHIM="$(mktemp -d)"
trap 'rm -rf "$SHIM"' EXIT

OWNER="Garvnanda|184491525+Garvnanda@users.noreply.github.com"
BOT="github-actions[bot]|41898282+github-actions[bot]@users.noreply.github.com"
failures=0

fake_curl() {
  printf '#!/usr/bin/env bash\n%s\n' "$1" > "$SHIM/curl"
  chmod +x "$SHIM/curl"
}

run() { PATH="$SHIM:$PATH" bash "$HERE/pick-author.sh"; }

check() {
  local desc="$1" want="$2" got="$3"
  if [ "$got" = "$want" ]; then
    printf 'ok   - %s\n' "$desc"
  else
    printf 'FAIL - %s\n       want: %s\n        got: %s\n' "$desc" "$want" "$got"
    failures=$((failures + 1))
  fi
}

export GITHUB_TOKEN="fake-token"
export GITHUB_REPOSITORY="Garvnanda/Garvnanda"

fake_curl 'echo "[]"'
check "first commit of the day -> owner" "$OWNER" "$(run)"

fake_curl 'echo "[{\"sha\":\"abc123\"}]"'
check "owner already committed today -> bot" "$BOT" "$(run)"

fake_curl 'echo "{\"message\":\"API rate limit exceeded\"}"'
check "error object instead of array -> bot" "$BOT" "$(run)"

fake_curl 'exit 22'
check "curl exits non-zero -> bot" "$BOT" "$(run)"

fake_curl 'echo "not json at all"'
check "unparseable body -> bot" "$BOT" "$(run)"

fake_curl 'echo ""'
check "empty body -> bot" "$BOT" "$(run)"

saved_token="$GITHUB_TOKEN"
unset GITHUB_TOKEN
fake_curl 'echo "[]"'
check "missing GITHUB_TOKEN -> bot" "$BOT" "$(run)"
export GITHUB_TOKEN="$saved_token"

unset GITHUB_REPOSITORY
fake_curl 'echo "[]"'
check "missing GITHUB_REPOSITORY -> bot" "$BOT" "$(run)"
export GITHUB_REPOSITORY="Garvnanda/Garvnanda"

if [ "$failures" -eq 0 ]; then
  printf '\nall checks passed\n'
else
  printf '\n%d check(s) failed\n' "$failures"
fi
exit "$failures"
