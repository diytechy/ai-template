+++
id = "WI-721"
title = "Clear the slow-tier reds the wave-5 close found: retire.py's live-id reader misses non-TOML registries, the skills-index freshness test trips the description floor, and measure the full suite's wall time"
workstream = "process"
specref = "docs/log.d/2026-09-27-wave5-coordinator.md#the-close-out-the-full-suite-wi-721-and-the-next-sessions-roles"
sr_refs = ["SR-226"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

The wave-5 close ran the full unfiltered suite once, at bc3310f3
(`python -m pytest -q -n auto`): **5 failed, 4810 passed, 15 skipped in
6683.90 s (1:51:23)**. One failure was an untracked handoff not yet linked,
cleared at the close. The other four are real, and every lane missed them
because each ran only its named slow modules:

- **`tests/test_trace_golden.py`, all three goldens (clean, offspine,
  orphan).**
  - The cause: `retire.live_ids` parses only the four TOML registries at
    fixed paths (`retire.TIERS`). The golden scaffolds keep their spine in
    the legacy CSV and Markdown forms, which `trace.py` still reads through
    the kit's registry reader.
  - The effect: every live row reads as a spent id with no retirement
    record, for example "4 spent spine id(s) have no retirement record ...:
    SN-001, SR-001, LLR-001, TC-001" on a spine where all four are live.
  - The advisory is warn-only, but it is false. It would reach any adopter
    whose registries `live_ids` cannot parse.
  - The fix reads live ids through the one registry reader that `trace.py`
    uses (0->A->B), not a second parser. The goldens must not be
    re-stamped over a false advisory.
- **`tests/test_generated_freshness_wiring.py::test_skills_index_step_reds_when_a_skill_is_added`.**
  - The test plants a skill with a 32-character description and expects
    `gen_skills_index --check` to report STALE.
  - The generator now reports SHORT first, against its 100-character
    description floor.
  - The fix is the test fixture's description, so the test again pins
    STALE. The floor stays.
- **The wall time.** The same suite was recorded at about 10 minutes on a
  quiet box and 3–4× that under load. This run took 111 minutes, with only
  light read-only commands beside it. The cause is unmeasured.

## Done-when

- `retire.live_ids` (or its replacement) reads every registry form the
  kit's registry reader supports. A test on a CSV-registry scaffold shows
  no advisory for a live row, and still names a spent id with no record.
- The three trace goldens pass without the retirement advisory, and no
  golden is regenerated to absorb it.
- `test_skills_index_step_reds_when_a_skill_is_added` pins STALE again with
  a fixture description above the floor. The floor is unchanged.
- The full unfiltered suite's slowest tests are measured
  (`--durations=30`) and recorded in the log fragment with the total wall
  time. A regression large enough to explain the jump is fixed or filed.
- The full unfiltered suite passes, and its real output is pasted in the
  log fragment.
