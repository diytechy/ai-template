a4d6f7d4 NOT YET SOUND

## BLOCKER

none

## MAJOR

- project-trajectory/scripts/acceptance_record.py:2315 — **The exact-tip abandoned-squash exemption remains, retained for adjudication.** Squash a valid two-commit lane containing HEAD, abandon its staged changes while retaining `SQUASH_MSG`, then handtype its exact approval-act registries and record as a direct mixed commit. The ordinary guard refuses it; the squash guard returns `[]`, and the actual step exits 0. This still conflicts with Q-8’s direct-trunk separation rule. **D-004’s narrowed description at docs/decisions/wi-806.toml:32 is accurate:** after committing, Git deletes `SQUASH_MSG`, and the new HEAD is no longer an ancestor of the tip. That bounds the residue without resolving the ruling dispute.

## MINOR

- docs/requirements/low-level-requirements.toml:3163; docs/test/test-cases.toml:1745 — **The amended squash sentences overstate refusal.** I committed text before branching, took only the Status-and-copy act in the lane, advanced trunk independently, then squashed the lane. Its tip does not contain HEAD, yet ordinary judging and the actual step pass without a rebase hint. This behavior correctly preserves text-before-act. State the ancestry/equality conditions as conditions for the **exemption**, and qualify the nonancestor refusal as applying when ordinary judging finds mixed text and act. The cited negative test exercises that mixed case only.

## Verified

The combined-cell BLOCKER is fixed: round two admits the reproduction; this revision refuses it with the rebase hint. Both new negative regressions are red against round two. The guard catches omitted bad ancestors and bad commits on merged side branches, admits a valid refresh merge, refuses extra staged LLR text, and ignores ref-shaped `SQUASH_MSG` headers. Changed function back-links match LLR-302. Only its detail and TC-173’s method/evidence changed; no statuses or SR cells changed. The RESYNC anchor is a trunk ancestor. The worktree remained unchanged.

## Commands

- `Get-Content` inspections of CLAUDE.md, antidote/session-protocol skills, the full WI, governing ruling and chapter, PROCESS.md, decisions, prior reviews/adjudications, affected code, rows and tests — checked scope and contracts.
- `rg -n` / `rg --files` inspections — located carriers, bindings, ruling text and finding lines.
- `git diff --stat 98142025..a4d6f7d4`; `git diff 98142025..a4d6f7d4` and scoped diffs — reviewed all eight changed files.
- `git log --oneline 98142025..a4d6f7d4`; `git show --format=fuller --no-patch 2d7f3d39 a4d6f7d4` — checked builder and row-author reports.
- With `GIT_CEILING_DIRECTORIES` and `PYTHONDONTWRITEBYTECODE` set:  
  `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-806 tests/test_text_then_act.py tests/test_acceptance_record.py` — **30 passed, 1 failed in 33.35s**; the failure is the identified shallow-clone setup Win32 error 5.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — clean, warnings only.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -` scratch probes — confirmed the scenarios above, red-before behavior, missing-parent refusal, TOML deltas and AST bindings. Initial probe-helper errors were corrected.
- Scratch invocations of `check.py --run-steps text-then-act` — confirmed actual exit codes for each reproduction.
- `git diff --check 98142025..a4d6f7d4` — reports trailing whitespace in the copied round-two review at docs/reviews/wi-806-text-then-act/sol-review-a-r2.md:25.
- `git merge-base --is-ancestor 883b3edf cde27048`; `git show -s --format='%h %s' 883b3edf` — verified the shipping anchor.
- `git status --short`; `git status --porcelain=v1 --untracked-files=all` — clean.