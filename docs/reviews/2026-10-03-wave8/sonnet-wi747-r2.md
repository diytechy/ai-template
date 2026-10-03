# Sonnet review — WI-747 fix round 1 (build/wi-747 at d4f991a0)

Reviewer: Claude Sonnet 5.5 (read-only). Range `dfe92989..d4f991a0`, answering
[sonnet-wi747-r1.md](sonnet-wi747-r1.md).

d4f991a0 SOUND

**BLOCKER:** none. **MAJOR:** none — the r1 MAJOR is closed.

**MINOR**
1. `intake.py` `_cmd_rejudge` docstring still read "Release preparation's entry";
   the CLI now serves stage-gate too. *(Fixed at the landing.)*
2. `choices=rejudge.CHECKPOINTS[1:]` relies on `merge` being first in
   `CHECKPOINTS`; a reorder would make a by-hand merge checkpoint a CLI choice.
   Suggested an assertion in the stage-gate test. *(Added at the landing.)*
3. The `REJUDGE_CELLS` comment named only Method and Expected as required, with
   `MaxAge` now in the tuple. *(Fixed at the landing.)*
4. The stage-gate CLI entry is documented in LLR-293 (module
   `observation_cadence.py`) while the code sits in `intake.py` under LLR-255.
   Acceptable under ruling R2.

**LLR-255:** leave it. Its detail ("`intake.py rejudge --checkpoint release` is
the release-preparation entry") is incomplete about stage-gate, not false;
amending an Approved row for a clause adding no obligation costs a fresh
approval. Fold a clause in at its next amendment if strict placement is wanted.

**Verified:** the stage-gate CLI files exactly one row for a
`Trigger = "stage-gate"` case past its floor, none at merge, and suppresses a
duplicate; `merge` is refused by argparse; SR-215 is unchanged since dfe92989
and reads true; `checkpoint_for` is behaviour-equivalent to the inline mapping
(the only extra value, a literal `Trigger = "merge"`, maps to merge either way);
the `MaxAge` move preserves the missing-cell order; `rejudge_values` 14,
`checkpoint_for` 3.

**Commands:** `pytest -q -n 2 tests/test_rejudge.py tests/test_rejudge_rubric.py
tests/test_intake.py tests/test_adjudicate_brief.py`: `219 passed in 104.03s`;
`check_trajectory.py --strict`: clean (758 work items).
