ef02f2bb NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/kitlib/sitting.py:225 — A coordinator-rejected sitting still releases the holds when its verdict drops a requested kind. Confirmed with a brief requesting `amendment;done-when` and a verdict containing only a valid Done-when section plus `SITTING: JUDGED kinds=done-when`. Coordinator validation rejects it, but `kind_part` validates against the verdict’s own kind list. Dispatch, staged close and merge all release; intake mints nothing. This violates SR-232’s missing-section refusal and leaves the earlier rejected-sitting MAJOR partly open.

2. project-trajectory/scripts/kitlib/done_when.py:345; project-trajectory/scripts/kitlib/sitting.py:145 — The covering reader accepts machine lines the validator never checked. Confirmed with two Done-when lines: the first carries all required fields and an older checklist’s digest; the second carries the current digest but omits `changes=`. Validation checks only the first line, while `_verdicts` accepts both. Dispatch, staged close and merge consequently release the current checklist using the incomplete second line. The prompt requires exactly one machine line, and LLR-308 requires both fields.

**MINOR**

1. docs/test/test-cases.toml:2687 — TC-257’s amended Method incorrectly says a covered change “mints none.” A valid, matching SUCCESSOR cover with a Dispositions draft mints that successor; confirmed through intake. State that a covered change mints no **goalposts adjudication**, preserving LLR-262 and TC-328’s successor arm.

**Verified**

The requested tests passed: **272 in 145.89 seconds**. The original malformed-amendment and extra `red-tc` examples are now refused; IF-285 and IF-287 Data cells are within 160 characters. Carrier conversion, scoped combined acts, exact-digest releases, subsequent-edit holds and successor intake passed their tests. Changed SR Requirement cells satisfy R2; existing spine Status values remain unchanged; 48 changed-function back-links resolve. The RESYNC anchor is a trunk ancestor and byte stamps match. Two representative tests were red against the base. I changed no worktree files; concurrent commits changed records only.

**Commands**

Python runs disabled bytecode writes and used the requested Git ceiling. No full suite or smoke tier ran.

- `Get-Content`, `Select-Object`, and `rg -n` over the guides, full spec, decisions, adjudications, prior review, changed cells, implementation and tests — inspected scope, contracts and consumers.
- `git diff 76b1d212..ef02f2bb`, including scoped, `--stat`, `--name-only`, and `--unified=0` variants — reviewed the fixed lane range.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-final2 tests/test_done_when_blessing.py tests/test_snapshot_readers.py tests/test_acceptance_record.py tests/test_adjudicate_brief.py tests/test_intake.py` — **272 passed**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `python.exe -B …/wi841-final2-probe.py` and inline `python.exe -B -` reproductions — confirmed both MAJORs and the covered SUCCESSOR mint.
- `python.exe -B …/wi841-final-red.py` — two representative tests red against `76b1d212`.
- Inline `python.exe -B -` TOML, AST and byte comparisons — checked changed rows, Status values, back-links, interface lengths, snapshot differences and byte deltas.
- `git merge-base --is-ancestor dd595b62 76b1d212`; `git log -1 --format='%h %s' dd595b62` — anchor ancestry confirmed.
- `git ls-files --eol` for measured documents — LF in index and worktree.
- `git diff --check 76b1d212..ef02f2bb` — trailing whitespace in recorded telemetry.
- `git status --short`, `git rev-parse HEAD`, and diffs against `ef02f2bb` — implementation, tests and live requirement cells unchanged by concurrent record commits.
- Scratch-only `Set-Content`, temporary archive extraction and repository fixtures — all reproduction writes stayed under the authorized scratch root.