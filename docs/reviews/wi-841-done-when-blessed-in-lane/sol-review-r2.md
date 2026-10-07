9e846812 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/acceptance_record.py:801 — Combined act authorization remains incomplete. A sitting scoped to `amendment:SR-001` and `first-approval:LLR-001` correctly re-attests SR-001 and approves LLR-001, but merge refuses the SR snapshot as `WIDENED` at project-trajectory/scripts/acceptance_record.py:830: it compares every snapshot registry against approval flips alone. The same refusal occurs when first-approval returns every row and the amendment section takes its valid re-attestation; an amendment-only control accepts that identical act. Both scenarios were reproduced in real scratch repositories. Round-1 MAJOR 2 is therefore only partly closed. tests/test_snapshot_readers.py:652 covers approval and amendment in the same registry, masking this failure and leaving LLR-278’s mixed-act guarantee untrue.

2. docs/requirements/interfaces.toml:2579 — New seam IF-287 has no citing TC. The amended TC-327 exercises its functions but omits IF-287 from `verifies`. On this tip, the requested `check_trajectory.py --strict` exits 1 specifically for IF-287, violating PROCESS.md §8’s requirement that every interface have a contract/fixture test cited through a TC.

**MINOR**

none

**Verified**

Round-1 MAJORs 1, 3, 4 and 5, and the MINOR, are closed. All five original failure scenarios were reproduced against `e62499b6` and corrected in the tip; MAJOR 2’s scope parsing is fixed, with the remaining act failure above. The requested tests passed: **231 in 128.93 seconds**. Amended cells and back-links were inspected; SR cells remain unchanged, satisfying R2, and no existing Status flipped. The RESYNC entry includes the new shipped module and uses trunk-ancestor anchor `dd595b62`. Byte stamps match. The worktree remains clean.

**Commands**

All Python runs disabled bytecode writes; Git commands used the requested ceiling. No full suite or smoke tier ran.

- `Get-Content` and `rg -n` over rules, the full spec, prior review, decisions, amended cells, implementation and tests — inspected scope, wording, back-links and consumers.
- `git diff e62499b6..9e846812`, including scoped variants, `--stat` and `--numstat` — reviewed all 24 changed files.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-sol2 tests/test_done_when_blessing.py tests/test_snapshot_readers.py tests/test_intake.py tests/test_adjudicate_brief.py` — 231 passed.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 1; repeated with filtered output to confirm IF-287 is the sole error.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-sol2-probes.py` — confirmed both valid combined-act refusals and the accepting amendment-only control.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-sol2-red.py` — confirmed five original failures against baseline modules; initial relative-import error corrected in scratch.
- Inline TOML and byte comparison through `python.exe -B -` — unchanged SRs, no Status flips; PROCESS.md −36 bytes and budget skill −5 bytes.
- `git merge-base --is-ancestor dd595b62 76b1d212` and `git log` — verified anchor ancestry and lane history.
- `git diff --check e62499b6..9e846812`; `git status --short` / `--porcelain` — no whitespace errors; clean worktree.
- Scratch-only `New-Item` / `Set-Content` — created reproduction scripts and baseline copies solely under the designated scratch directory.