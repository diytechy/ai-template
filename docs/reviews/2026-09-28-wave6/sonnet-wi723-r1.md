<!-- Claude Sonnet (read-only) review of WI-723, build/wi-723 28d35286..17b88731. Built by Codex Sol; committed by the coordinator. -->

17b88731 NOT YET SOUND

BLOCKER: none

MAJOR:
1. **SR-024's `delivered_with = ["SR-157"]` is not argued from its own rationale.** *Coordinator: in scope for fix round 1. The builder keeps a sibling only where it can name the sentence that carries the relationship; otherwise the row stays unclassified.*
   - The rationale says generation answers the charter's coverage half and disclaims the negative-test half. It names no sibling.
   - SR-015's pairing with SR-157, by contrast, is stated on both sides. SR-024's reads as SR-015's reused.
   - Weaker, and less clear-cut: SR-129 → SR-148, and SR-225's third sibling SR-148, rest on need or hat proximity rather than a textual link.
2. **`assumption_rules.py` made room under the 1000-SLOC ratchet by compaction.** It went from 997 to exactly 1000. *Coordinator: in scope. Restore the text and the single computation. Decompose or re-stamp with a reason. Add a wording test.*
   - The room came from shortening user-facing advisory text:
     - "SR {sid} is unclassified" lost its explanation of what unclassified means;
     - "has DA-Refs and Coincident; keep one" lost "the two contradict each other; keep the one that is true".
   - `_classify` now swallows which ids are undeclared. `sr_classification_advisories` recomputes the same two set differences, so there are two sources of truth.
   - The tests only check that an id appears in some message, so CI passed while the report degraded.

MINOR:
- In both skill copies, `SKILL.md:170-171`, a pre-existing bullet's continuation lines were re-indented from 4 spaces to 2. *Coordinator: in scope.*

**Clean:**
- **The owner's directions** are met:
  - no inheritance (`da_citing_srs` reads only direct DA-Refs);
  - an undeclared sibling fails, naming the row;
  - a sibling sharing no need is reported;
  - `Delivered-With` is in `SPINE_APPROVED_CELLS` beside `Coincident`, so it re-opens attestation the same way;
  - SR-193's combination rules match the code.
- **The amendments stayed inside the grant.** No status moved.
- **All nine sibling lists share a need.** None of the nine belongs at LLR.
- **Schema and carrier:**
  - the bijection is intact;
  - the template uses the `-000` placeholder;
  - the two skill copies are byte-identical;
  - the RESYNC_PACK entry has the right format and position (`[since 28d35286]`).

**Run:** `python -m pytest -q -n 2 tests/test_assumption_rules.py tests/test_cell_classes.py tests/test_traj_views.py tests/test_dogfood_sync.py tests/test_rule_sync.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py tests/test_resync_pack.py -p no:cacheprovider` → **359 passed, 1 skipped in 52.45s**. `trace.py --strict-integrity` was skipped, because it writes `report.md`.
