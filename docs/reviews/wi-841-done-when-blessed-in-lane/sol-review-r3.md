5d7c0ed8 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/acceptance_record.py:896 — The WIDENED fix still refuses valid acts using supported CSV registries. `_reattested_registries` resolves rows through the carrier-aware reader but returns the canonical `.toml` path. In a real bootstrapped repository with `system-requirements.csv`, a combined sitting re-attesting SR-001 and approving SN-091 writes the CSV snapshot but authorizes the TOML path. Merge therefore refuses `WIDENED to docs/requirements/system-requirements.csv`. Round-2 MAJOR 1 is closed for TOML, but remains for CSV; LLR-278’s cross-registry guarantee is still false for that supported carrier. Resolve the actual carrier consistently and add a CSV regression case.

**MINOR**

none

**Verified**

Round-2’s IF-287 finding is closed. The original TOML act failures are red against `9e846812` and green at the reviewed tip; unrelated snapshot copies remain refused. Unreadable claims now hold, while absent claims release. The SR-232/LLR-310 split satisfies R2, and the eight retags match their modules and symbols. The only existing Status flips are LLR-309 and TC-326, approved by adjudication 002. RESYNC covers the shipped changes and anchors at trunk ancestor `dd595b62`. Requested tests: **244 passed in 151.39 seconds**. This review changed no worktree files.

**Commands**

All Python runs disabled bytecode writes. No full suite or smoke tier ran.

- `Get-Content` and `rg -n` over CLAUDE.md, PROCESS.md, skills, the complete spec, prior review, decisions, verdicts, changed cells, implementation and tests — inspected scope, wording and consumers.
- `git diff 9e846812..5d7c0ed8`, including scoped, `--stat`, `--numstat` and `--name-only` variants — inspected all 26 changed files.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-sol3 tests/test_done_when_blessing.py tests/test_snapshot_readers.py tests/test_intake.py tests/test_adjudicate_brief.py` — 244 passed.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-sol3-independent-confirm.py` — confirmed baseline failures, TOML fixes, preserved WIDENED refusal, CSV failure and claim behavior.
- Inline `python.exe -B -` TOML/AST comparisons — checked changed cells, snapshot differences, Status flips and back-links.
- `git log`, `git show`, `git branch --list`, `git worktree list --porcelain`, and ancestry checks — confirmed `dd595b62` belongs to integration trunk `refactor_again`; the initial `main` check used a different branch.
- `git diff --check 9e846812..5d7c0ed8`, with scoped variants — authored paths clean; one telemetry-log whitespace warning.
- `git status --short`, `git rev-parse HEAD`, and `git diff --name-only 5d7c0ed8 HEAD` — later commits contain telemetry only; reviewed sources remain unchanged.
- Scratch-only `Set-Content` — created the reproduction script under the authorized scratch root.