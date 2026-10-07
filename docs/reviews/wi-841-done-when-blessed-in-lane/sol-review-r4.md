264d0e5d NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. docs/requirements/low-level-requirements.toml:2855; project-trajectory/scripts/acceptance_record.py:304 — LLR-278’s newly stated markdown guarantee is false. In a bootstrapped repository using supported `stakeholder-needs.md`, a combined act re-attesting SN-001 and approving SR-001 writes the correct snapshots and stays within both scopes, yet merge refuses `snapshot WIDENED to docs/requirements/stakeholder-needs.md`. `_carrier_rows_at` tries only TOML and CSV, returning no need rows; `_reattested_registries` consequently authorizes no markdown copy. Confirmed with a real scratch repository. Resolve and parse the needs carrier too, and add this mixed-act regression.

**MINOR**

1. docs/requirements/interfaces.toml:1126 — IF-175 omits its new requestor, `scripts/acceptance_record`. The module now calls the extracted reader through its alias at project-trajectory/scripts/acceptance_record.py:1000, but the seam’s recorded far side excludes it. A reader following IF-175 cannot discover this merge-validation dependency.

2. docs/requirements/interfaces.toml:1128 — The amended Data cell is 197 characters, exceeding PROCESS.md §8’s 160-character limit. Calling `trace.if_data_advisories` on this row produces the corresponding advisory. Shorten the typed summary and keep the definition in the owner’s contract body.

**Verified**

The round-3 CSV failure is closed: the same real act fails at `997b4c20` and merges at `264d0e5d`. The extracted verdict reader preserves behavior and alias identity; its LLR-278 back-link resolves. No SR cells or Status values change. TC-278 cites the new, meaningful CSV regression. RESYNC includes both shipped files and anchors at trunk ancestor `dd595b62`. Requested tests passed; strict trajectory check passed with warnings. Later adjudicator changes were excluded. I changed no worktree files.

**Commands**

All Python runs disabled bytecode writes; no smoke tier or full suite ran.

- `Get-Content`, `rg -n`, and `Select-Object` over the guide, applicable skills, full WI spec, prior review, decisions, PROCESS.md, amended cells, implementation and tests — inspected scope, rules, wording and consumers.
- `git diff 997b4c20..264d0e5d`, including `--stat` and scoped variants; `git log --oneline 997b4c20..264d0e5d` — reviewed all eight changed files.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-sol4 tests/test_snapshot_readers.py tests/test_acceptance_record.py tests/test_import_layers.py` — **53 passed in 124.77 seconds**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -B C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-sol4-confirm.py` — confirmed CSV baseline failure/fix, markdown refusal and verdict-reader equivalence.
- Inline `python.exe -B -` checks — verified changed cells, preserved statuses, back-link resolution and IF-175’s length advisory.
- `git diff --check 997b4c20..264d0e5d` — clean.
- `git branch --list refactor_again`; `git merge-base --is-ancestor dd595b62 refactor_again` — RESYNC anchor belongs to integration trunk.
- `git rev-parse HEAD`, `git status --short`, and `git diff` against `264d0e5d` — reviewed sources unchanged by concurrent adjudication.
- Scratch-only `Set-Content` and Python writes — created reproduction evidence; a scratch cleanup command was rejected by policy, so scratch files remain.