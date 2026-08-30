## 2026-08-30 — WI-521 slice 3: M-06's second monolith split, `test_trace.py`'s IF-seam tier walks

**Summary.** `tests/test_trace.py`'s IF-### interface-seam tier moved verbatim to
a new `tests/test_trace_interfaces.py` — the standing decomposition-debt owner's
second M-06 delivery, and the first taken after OI-68's 2026-08-30 ruling
re-homed the row's §3 sensor/axis question to `WI-537`/`WI-538`.

**Why this target.** The three remaining M-06 monoliths were re-measured:
`test_trace.py` **2,323** (grew from 2,099 at slice 2 — the sensor gap in
action), `test_trajectory_arch.py` **2,290**, `test_agent_loop.py` **1,640**. The
top two are 33 lines apart — no line-count winner — so the row's own rule
("split by stable behaviour boundary, not by line count") decided it: `test_trace`
carries a genuinely self-contained subsystem, `trace.py`'s IF-### interface-seam
tier (`process.md` §8), with its own carrier, closed vocabularies, reachability
advisory and nine dedicated helpers; `test_trajectory_arch`'s sections are
heterogeneous rules with no comparable seam.

**Deliverable.**
- New `tests/test_trace_interfaces.py` (978 lines / 40 tests): the IF-### tier —
  id integrity + owner-shape `--strict` findings, the warn-first IF+CMP schema
  tier, the endpoint reachability advisory, the OI-67 owner/consumers reshape and
  IF carriage, and the WI-065 seam-citation join (`Verifies` cell ↔
  `interfaces.toml`). Moved verbatim as one contiguous banner block.
- `tests/test_trace.py` shrinks 2,323 → 1,370 (52 tests): the SN→SR→LLR→TC spine.
  The two-line `_report` reader moved with its cluster; its four remaining core
  call sites were inlined to the family's own `report.md`-read idiom (the only
  non-move edit — ruff rewrapped those four lines, the +6 over a pure removal).
- `tests/conftest.py`: `test_trace_interfaces` joins `SLOW_MODULES` beside
  `test_trace` (same heavy class — a real `trace.py` subprocess per test), so
  smoke membership is unchanged.
- `docs/test/test-cases.toml`: three `TC` `Evidence` cells re-pointed to the new
  module for the tests that moved (`test_if_tier_integrity`,
  `test_channel_refuses_an_unknown_value_as_a_warn`,
  `test_missing_required_if_field_is_a_warn`); the sibling ids that stayed were
  left. `Evidence` is a TRACED cell — no row minted, no attested prose moved.

**The proof is node-id set equality.** The sorted collected node-id sets of the
two modules are byte-identical as a set to the pre-split `test_trace.py` at
`56e7e52b` (92 ids, `diff` empty). Both run 91 passed / 1 skipped (the skip is
the POSIX-only provenance test on Windows).

fig: derived="the sorted collected node ids of tests/test_trace.py + tests/test_trace_interfaces.py, stripped to `::name`, diffed against tests/test_trace.py at 56e7e52b — empty diff, 92 ids each side; 52+40 by module"

**Deviations from spec.** None. The slice follows the row's §2 (standalone
M-06 split, boundary-first) and the slice-2 precedent (verbatim move, node-id
equality proof, SLOW_MODULES co-membership, TRACED-only Evidence re-point). §3's
sensor gap is not touched — OI-68 re-homed it to `WI-538` (soft edge, IF-054),
recorded in the spec's slice-3 section.

**Byte deltas on budgeted files:** none touched (no `AGENTS.template.md`,
`PROCESS.md`, `PROCESS_OPTIONS.md`, `CLAUDE.md`, or guard skill in the diff).

**Commit bar (this branch, Git Bash on Windows):** `-m smoke` **1378 passed, 6
skipped in 31.21 s**; `check_smoke_budget --mode enforce` **27.4 s vs 60 s →
within**; `check_docs --root . --stale` **0 broken** (the two `interfaces.toml`
stale hints are pre-existing, not in this diff). The two split modules alone:
**91 passed, 1 skipped in 241.60 s**. `trace.py --strict` interface-findings=0 /
integrity=0; `check_trajectory --strict` clean, graph acyclic.

**Full suite** (`pytest -q -n auto`, Git Bash on Windows): **1 failed, 3107
passed, 16 skipped in 618.70 s**. The single failure is
`test_derive_stage.py::test_this_repo_s_committed_stage_is_current` — the
expected work-branch generated-artifact staleness, NOT a defect: `docs/stage`'s
fingerprint hashes `docs/test/test-cases.toml` bytes (a `kitlib.stage`
DECLARED_INPUT), so this slice's Evidence re-point drifted the input hash.
`derive_stage.py --check` confirms **every derived value is unchanged** (stage
`DevStg-LLReqs`, all per-phase values identical) — only the input fingerprint
moved. `docs/stage` is a generated artifact the trunk lane regenerates after
each merge (§5.2), which is why the pre-commit hook SKIPS its freshness check on
a work branch; it is not re-stamped here (editing a generated artifact on a work
branch is forbidden and would only collide with the trunk lane's regen). The two
split modules and everything else pass.

fig: cmd="python -m pytest -q -n auto" rev=c9203f47

**M-06 after this slice: two of four done** (`test_integrate`, slice 2;
`test_trace`, here). `test_trajectory_arch.py` (2,290) and `test_agent_loop.py`
(1,640) remain. This row stays open — it is a standing debt owner.

Deferred open items: none — this slice defers nothing new (the §3 sensor/axis
question was owner-ruled and re-homed, per the summary above).
