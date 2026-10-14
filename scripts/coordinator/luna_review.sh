#!/usr/bin/env bash
# luna_review.sh — run one Codex Luna review of a lane through the codex CLI.
#
#   bash luna_review.sh <worktree> <prompt.md> <out.md> [effort]
#
# effort defaults to "high" (owner, 2026-10-03). Run it from the coordinator with
# the Bash tool's run_in_background; the review's final message lands in <out.md>
# and the CLI transcript in <out.md>.log.
#
# Why each flag (probed 2026-10-03):
# - the VS Code extension's bundled codex.exe: older CLIs refuse new models with
#   a misleading "ChatGPT account" error, so take the newest extension folder;
# - -s workspace-write: under -s read-only Python finds no usable temp directory
#   and no test can run;
# - --add-dir review-tmp: the reviewer's ONE writable scratch root outside the
#   lane; prompts pass a LITERAL --basetemp under it, because the sandbox shell is
#   PowerShell, where "$TEMP" is empty and pytest then writes to C:\;
# - windows.sandbox="unelevated": the elevated sandbox cannot read the user's
#   Python install.
# workspace-write could let a reviewer edit the lane, so this script compares
# the lane's HEAD and status before and after the run and reports any change;
# it never reverts on its own.
set -u
WT=${1:?worktree}; PROMPT=${2:?prompt.md}; OUT=${3:?out.md}; EFFORT=${4:-high}
TOOLS=$(cd "$(dirname "$0")" && pwd)
TMPROOT=C:/Projects/ai-template.wt/review-tmp
EXT=$(ls -d "$HOME"/.vscode/extensions/openai.chatgpt-*-win32-x64 2>/dev/null | sort -V | tail -1)
CODEX="$EXT/bin/windows-x86_64/codex.exe"
[ -x "$CODEX" ] || { echo "luna_review: no codex.exe under $EXT" >&2; exit 2; }
[ -f "$PROMPT" ] || { echo "luna_review: no prompt file $PROMPT" >&2; exit 2; }
mkdir -p "$TMPROOT"
before_head=$(git -C "$WT" rev-parse HEAD)
before_status=$(git -C "$WT" status --porcelain)
echo "luna_review: $("$CODEX" --version) gpt-6-luna effort=$EFFORT lane=$WT head=${before_head:0:8}"
"$CODEX" exec -m gpt-6-luna -c model_reasoning_effort="$EFFORT" \
  -c 'windows.sandbox="unelevated"' -s workspace-write \
  --add-dir "$TMPROOT" -C "$WT" --skip-git-repo-check \
  -o "$OUT" - < "$PROMPT" > "$OUT.log" 2>&1
rc=$?
after_head=$(git -C "$WT" rev-parse HEAD)
after_status=$(git -C "$WT" status --porcelain)
if [ "$before_head" != "$after_head" ] || [ "$before_status" != "$after_status" ]; then
  echo "luna_review: WARNING - the reviewer changed the lane (HEAD ${before_head:0:8} -> ${after_head:0:8}); inspect before trusting the review:"
  git -C "$WT" status --short
  rc=3
fi
echo "luna_review: exit $rc; review -> $OUT"
head -1 "$OUT" 2>/dev/null
exit $rc
