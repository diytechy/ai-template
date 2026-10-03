# Sonnet review — WI-747 (build/wi-747 at dfe92989)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol). Range `87736778..dfe92989`.

dfe92989 NOT YET SOUND

**BLOCKER:** none

**MAJOR**
- The stage-gate checkpoint has no production caller. SR-215's amended requirement says the harness "shall file one re-judge work item ... when ... a stage gate is checked", and PROCESS.md says gate preparation "can file through `intake.mint_rejudge(root, rev, "stage-gate")`", but the intake CLI is `choices=("release",)` (`intake.py:3193`) and no caller of `mint_rejudge`/`checkpoint_drafts` exists outside `intake.py` and `rejudge.py`; the only non-test `stage-gate` reference is `adjudicate_brief.py:1150`. A `Trigger = "stage-gate"` case never fires except by `MaxAge`. No row uses it today. Either wire a caller (a CLI choice or the gate-advance path) or narrow SR-215/LLR-293/PROCESS.md to say API-only.

**MINOR**
- Two tests failed once under `-n 2` and passed on rerun (`test_floor_alone_does_not_fire_trigger[files:other/*.txt-merge-src/b.txt]`; `test_the_release_checklist_carries_the_required_rejudge_item`, `tests/test_rejudge.py:606`); cause not captured, likely contention.
- LLR-293/294 and TC-306/307 Drafted while SR-215 is Approved: fine if the adjudication follows.
- `rejudge_values` (`adjudicate_brief.py:1138-1170`) gained a ~15-line case-lookup and trigger-to-checkpoint block; extracting it into `rejudge.checkpoint_for(case)` would remove the duplicated `("release","stage-gate")` literal and the complexity row.

**Verified:** counting is deterministic at the checkpoint revision (`git log since..revision --diff-filter=A --no-renames -- docs/archive/work`, distinct WI ids from complete/cancelled/partial, `observation_cadence.py:84-98`; policy read from the snapshot's process.toml); squash closes count each id once; moves between terminal folders do not double-count; first judgement and expiry bypass the floor (`rejudge.py:349-353`); floor `max(default, case)`; release/stage-gate fire only at their checkpoint; files and component triggers tested; default 10 in process.toml and the template, documented in PROCESS.md and RESYNC; five rubrics short, numbered, faithful; each observation row references a rubric; `observation_rubric_findings` warns; SR-215/LLR-254/TC-247/TC-248 match the code apart from stage-gate; TC-279 trimmed to the rubric and DA-011, `trigger = "release"`; dogfood and rule sync pass.

**Commands:** `pytest -q -n 2 tests/test_rejudge.py tests/test_rejudge_rubric.py tests/test_dogfood_sync.py tests/test_rule_sync.py tests/test_adjudicate_brief.py`: `2 failed, 196 passed, 1 skipped` (both passed in isolation: `6 passed`; `tests/test_rejudge.py` rerun `50 passed`); `check_trajectory.py --strict`: clean (758 WIs).
