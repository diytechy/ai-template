#!/usr/bin/env bash
# sol_review.sh — run one Codex 6.1 Sol review of a lane through the codex CLI
# on PATH (0.160.0 since 2026-10-04; the wave-11 roles make Sol the reviewer).
#
#   bash sol_review.sh <worktree> <prompt.md> <out.md> [effort]
#
# The flags are luna_review.sh's (see its header for why each is there); only
# the binary (PATH codex, which now knows gpt-6.1-sol) and the model differ.
# workspace-write could let a reviewer edit the lane, so HEAD and status are
# compared before and after; exit 3 reports a change and nothing is reverted.
set -u
WT=${1:?worktree}; PROMPT=${2:?prompt.md}; OUT=${3:?out.md}; EFFORT=${4:-medium}
TMPROOT=C:/Projects/ai-template.wt/review-tmp
[ -f "$PROMPT" ] || { echo "sol_review: no prompt file $PROMPT" >&2; exit 2; }
mkdir -p "$TMPROOT"
before_head=$(git -C "$WT" rev-parse HEAD)
before_status=$(git -C "$WT" status --porcelain)
echo "sol_review: $(codex --version) gpt-6.1-sol effort=$EFFORT lane=$WT head=${before_head:0:8}"
codex exec -m gpt-6.1-sol -c model_reasoning_effort="$EFFORT" \
  -c 'windows.sandbox="unelevated"' -s workspace-write \
  --add-dir "$TMPROOT" -C "$WT" --skip-git-repo-check \
  -o "$OUT" - < "$PROMPT" > "$OUT.log" 2>&1
rc=$?
after_head=$(git -C "$WT" rev-parse HEAD)
after_status=$(git -C "$WT" status --porcelain)
if [ "$before_head" != "$after_head" ] || [ "$before_status" != "$after_status" ]; then
  echo "sol_review: WARNING - the reviewer changed the lane (HEAD ${before_head:0:8} -> ${after_head:0:8}); inspect before trusting the review:"
  git -C "$WT" status --short
  rc=3
fi
echo "sol_review: exit $rc; review -> $OUT"
head -1 "$OUT" 2>/dev/null
exit $rc
