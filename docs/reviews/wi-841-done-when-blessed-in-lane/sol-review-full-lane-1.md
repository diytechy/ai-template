efc4c776 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/kitlib/done_when.py:329 — A rejected combined sitting still releases the Done-when holds. Confirmed with a committed verdict containing a valid, matching `## done-when` BLESSED line but an amendment section missing its `VERDICT:` line. Combined validation refuses it, yet dispatch, staged close and merge all return no hold; merge-time intake also mints nothing. `_verdicts` consumes the blessing without validating the sitting containing it. This contradicts SR-232’s requirement that an invalid section refuse the sitting without another kind acting.

2. project-trajectory/scripts/kitlib/sitting.py:35; project-trajectory/scripts/adjudicate_brief.py:324 — Unrequested adjudication sections can pass combined validation. A sitting requesting only amendment accepted a verdict containing valid amendment content, an additional `## red-tc` section, and `SITTING: JUDGED kinds=amendment`. The heading parser recognizes only the three combinable kinds, so the extra section disappears from the comparison. SR-232 explicitly requires extra sections to refuse.

**MINOR**

1. docs/requirements/interfaces.toml:2562; docs/requirements/interfaces.toml:2584 — Amended IF-285 and new IF-287 have Data cells of 236 and 188 characters, exceeding PROCESS.md §8’s 160-character limit. `trace.if_data_advisories` reports both. Keep short schema pointers here and the definitions in the owner modules’ contract bodies.

**Verified**

The requested tests passed: **293 in 140.58 seconds**. The trajectory check passed with warnings. Two representative behavior tests were red against `76b1d212`. Carrier-conversion authorization, unauthorized-copy refusals, exact-digest releases, subsequent-edit holds, Context briefing and successor intake passed their focused tests. Changed function back-links resolve; SR Requirement cells satisfy R2; no pre-existing spine Status flipped. RESYNC’s `dd595b62` anchor is a trunk ancestor, and byte stamps match. I changed no worktree files. Concurrent approval records were excluded from the requested review range.

**Commands**

Python runs disabled bytecode writes. No full suite or smoke tier ran.

- `Get-Content`, `Select-Object`, and `rg -n` over the guides, full spec, decisions, reviews r1–r6, adjudications 001–007, changed cells, code and tests — inspected the full lane and downstream consumers.
- `git diff 76b1d212..efc4c776`, scoped variants, `--stat`, `--name-only`, and `--numstat` — reviewed the committed range.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-final tests/test_done_when_blessing.py tests/test_snapshot_readers.py tests/test_acceptance_record.py tests/test_adjudicate_brief.py tests/test_intake.py tests/test_spine_carrier.py` — **293 passed**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `python.exe -B …/wi841-final-probe.py` — confirmed both MAJOR findings in scratch.
- `python.exe -B …/wi841-final-red.py` — two representative tests red against `76b1d212`.
- Inline `python.exe -B -` checks — confirmed invalid-sitting intake suppression, interface lengths, changed cells, unchanged existing Status values, 44 changed-function back-links and byte deltas.
- `git merge-base --is-ancestor dd595b62 76b1d212`; `git log -1 --format="%h %s" dd595b62` — anchor ancestry confirmed, exit 0.
- `git ls-files --eol` for the measured documents — index and working files use LF.
- `git diff --check 76b1d212..efc4c776` — trailing whitespace in one recorded telemetry line.
- `git status --short`, `git rev-parse HEAD`, `git log`, `git show efc4c776:<path>`, and diffs against `efc4c776` — checked concurrent changes; implementation and test bodies remained unchanged.
- Scratch-only `Set-Content`, archive extraction and temporary repositories — reproduction artifacts stayed under the authorized scratch root.