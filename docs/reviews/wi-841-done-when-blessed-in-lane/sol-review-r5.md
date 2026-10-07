9c22f9ce NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/acceptance_record.py:847; project-trajectory/scripts/acceptance_record.py:911 — Carrier authorization still misses removal of an obsolete snapshot carrier. Confirmed on a real scaffold: commit a markdown-to-TOML needs conversion and SN-001’s amended text first, then take one scoped act re-attesting SN-001 and approving SR-002. The snapshot writer correctly writes the TOML copy and deletes the old markdown copy. `_reattested_registries` authorizes TOML, but the widening reader treats the markdown deletion as another registry and refuses `snapshot WIDENED to docs/requirements/stakeholder-needs.md`. Both kind scopes, text-then-act, and snapshot equality pass; removing only that deletion from the inspected delta makes the refusal disappear. This remaining carrier-transition case contradicts LLR-278’s guarantee at docs/requirements/low-level-requirements.toml:2855.

**MINOR**

1. docs/requirements/interfaces.toml:1386 — IF-102’s amended Data cell is 199 characters, exceeding PROCESS.md §8’s 160-character limit. Calling `trace.if_data_advisories` confirms the advisory. The baseline already exceeded the limit at 161 characters; this edit expands that violation. Shorten the summary and keep the definition in the owner’s contract body.

**Verified**

Round 4’s original markdown failure and both IF-175 findings are closed. The same real markdown mixed act fails at `538bc9a3` and passes now. The regression is meaningful; the shared reader reaches the approval, amendment, held-row, text-then-act and squash checks. New back-links resolve, no SR cells or Status values change, and RESYNC includes the shipped resolver with trunk anchor `dd595b62`. Concurrent adjudicator changes were excluded. I changed no worktree files.

**Commands**

All Python runs disabled bytecode writes. No full suite or smoke tier ran.

- `Get-Content`, `rg -n`, `rg --files`, and `Select-Object` — inspected the guide, skills, full spec, rulings, prior reviews, PROCESS rules, amended cells, implementation and tests.
- `git diff 538bc9a3..9c22f9ce`, including scoped, `--stat` and `--name-only` variants; `git log` and `git show` — reviewed the fixed ten-file range.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-sol5 tests/test_snapshot_readers.py tests/test_acceptance_record.py tests/test_spine_carrier.py tests/test_intake.py` — **172 passed in 96.65 seconds**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `python.exe -B …/wi841-sol5-confirm.py` — confirmed baseline failure/current success, markdown squash protection, interface lengths, unchanged statuses and new back-links.
- `python.exe -B …/wi841-sol5-cutover.py`, followed by inline `python.exe -B -` checks — confirmed the carrier-transition refusal and isolated the obsolete snapshot deletion as its sole cause. The initial probe stopped on a nonexistent review helper; the continuation completed.
- Inline TOML comparisons — IF-175 shrank from 197 to 153 characters; IF-102 grew from 161 to 199.
- `git diff --check 538bc9a3..9c22f9ce` — clean.
- `git branch --list refactor_again`; `git merge-base --is-ancestor dd595b62 refactor_again` — RESYNC anchor belongs to trunk.
- `git status --short`, `git rev-parse HEAD`, and diffs against `9c22f9ce` — reviewed implementation and cells remained unchanged during concurrent adjudication.
- Scratch-only `Set-Content` and Python writes — reproduction artifacts stayed under the authorized scratch root.