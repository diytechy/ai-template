# layout.sh: where this repository's coordinator tools find things, derived from
# this file's location, so no machine or user is named. Sourced by the review
# and spine-author wrappers. The tools live in scripts/coordinator/ of the
# primary checkout; the lanes, the review scratch root and the overnight logs
# live in its sibling folder, <checkout>.wt. Git Bash gets the Windows form
# (C:/...), which the codex CLI needs; other shells the plain path.
_coord_here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
case "$(uname -s)" in
  MINGW* | MSYS* | CYGWIN*) REPO=$(cd "$_coord_here/../.." && pwd -W) ;;
  *) REPO=$(cd "$_coord_here/../.." && pwd) ;;
esac
WTROOT="$REPO.wt"
TMPROOT="$WTROOT/review-tmp"
