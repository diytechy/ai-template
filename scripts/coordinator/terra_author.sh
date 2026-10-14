#!/usr/bin/env bash
# terra_author.sh — run one GPT Terra (gpt-5.6-terra, medium) spine-authoring
# session in a lane through the codex CLI on PATH (wave-11 roles, owner
# 2026-10-04: Terra authors SN/SR/LLR/TC/IF rows; an independent Opus judges).
#
#   bash terra_author.sh <worktree> <prompt.md> <out.md> [effort]
#
# Unlike a review, this session EDITS the lane (registries only, per its
# brief) and leaves the change uncommitted for the coordinator. The flags are
# the wave-11 handoff's: unelevated sandbox, workspace-write, and the one
# scratch root for pytest's --basetemp.
set -u
WT=${1:?worktree}; PROMPT=${2:?prompt.md}; OUT=${3:?out.md}; EFFORT=${4:-medium}
. "$(dirname "$0")/layout.sh"  # TMPROOT, beside the checkout
[ -f "$PROMPT" ] || { echo "terra_author: no prompt file $PROMPT" >&2; exit 2; }
mkdir -p "$TMPROOT"
before_head=$(git -C "$WT" rev-parse HEAD)
echo "terra_author: $(codex --version) gpt-5.6-terra effort=$EFFORT lane=$WT head=${before_head:0:8}"
codex exec -m gpt-5.6-terra -c model_reasoning_effort="$EFFORT" \
  -c 'windows.sandbox="unelevated"' -s workspace-write \
  --add-dir "$TMPROOT" -C "$WT" --skip-git-repo-check \
  -o "$OUT" - < "$PROMPT" > "$OUT.log" 2>&1
rc=$?
after_head=$(git -C "$WT" rev-parse HEAD)
[ "$before_head" = "$after_head" ] || { echo "terra_author: WARNING - HEAD moved ${before_head:0:8} -> ${after_head:0:8} (the brief forbids commits)"; rc=3; }
echo "terra_author: exit $rc; report -> $OUT"
git -C "$WT" status --short
exit $rc
