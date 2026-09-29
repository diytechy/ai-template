+++
id = "WI-545"
title = "The decomposition debt owner (cont.): three wide modules, check_trajectory's remaining fusion, and M-06's last two test monoliths"
workstream = "process"
specref = ""
buildtier = "strong"
priority = 1
safety_class = "ordinary"
supersedes = "WI-521"
needs = ["WI-579", "WI-580", "WI-581", "WI-620", "WI-583"]
+++

## Deliverable

The decomposition debt is paid by pure moves into four deep modules, with
nothing re-homed.

- **`agent_loop` → `agent_brief`** (48 symbols): prompts, briefs, the
  guardrails payload and assignment evidence.
- **`agent_common` → `agent_policy`** (59): process configuration,
  approval decisions and coordinator dials.
- **`check_trajectory` → `trajectory_arch`** (66): the architecture
  inventory, seams, components and contract join rules.
- **`bootstrap` → `kitlib/bootstrap_manifest`:** the shipped-file manifest
  (`MAPPING`, `mapping_entries`), which is the one source of truth.

Each move is proven byte-identical by an AST comparison against the base,
checked independently by the reviewer. The old modules keep load-bearing
re-exports for their callers and monkeypatch contracts.

- **What stayed whole, and why:**
  - `agent_loop`'s runtime scheduling and session composition
    (`session_body`'s monkeypatch contract depends on the facade's globals);
  - `bootstrap`'s delivery and generation;
  - `check_trajectory`'s phase, lifecycle, history and CLI composition;
  - `agent_common`'s git, lock, harness, assignment and telemetry
    behaviour.
- **The test splits:**
  - `test_trajectory_arch` → plus `test_trajectory_phase`: 97 moved tests
    and one new re-export test;
  - `test_agent_loop` → plus `test_agent_loop_support`: 72 of 72 node ids.
- **The ratchets:** module-size baselines are re-stamped down
  (`agent_loop` 2752→2390, `agent_common` 1466→1077, `bootstrap`
  1704→1465, `check_trajectory` 2385→1585), and the ratchet names this row
  as the debt owner. Four complexity entries are re-keyed to their new
  modules at unchanged values.
- **Seams:** IF-260 to IF-263 are Drafted, with Contract markers and
  verifying cases. The approved design rows' traced `module` cells follow
  their symbols.
- **Shipping:** the new modules are in `bootstrap.MAPPING`, the README
  table and `test_bootstrap`'s list.
- **What the split nearly broke silently**, caught by review and by the
  full suite:
  - four complexity-ratchet keys (fix 1);
  - four path-keyed content scans, SR-175's authorship-egress sweep among
    them, which read re-export stubs while checking nothing; three of the
    four were actually red (fix 2);
  - one test rebinding `bootstrap.MAPPING` through the alias, found only by
    the full unfiltered suite (fix 3).

  Each fix is shown load-bearing.
- **Evidence:**
  - the full unfiltered suite on trunk plus this lane at 7de50658:
    `1 failed, 4836 passed, 15 skipped in 3951.89s`, with the one failure
    fixed in fix 3;
  - the fix-3 confirmation ran `218 passed`.
- **Review:** Sonnet reviewed it in four rounds.
  - [Round 1](../../../reviews/2026-09-28-wave6/sonnet-wi545-r1.md): NOT
    YET SOUND, the complexity keys.
  - [Round 2](../../../reviews/2026-09-28-wave6/sonnet-wi545-r2.md): NOT
    YET SOUND, the egress scan.
  - [Round 3](../../../reviews/2026-09-28-wave6/sonnet-wi545-r3.md): SOUND.
  - [Round 4](../../../reviews/2026-09-28-wave6/sonnet-wi545-r4.md): SOUND
    at ac3b534b, after the full suite's red.
- **Left for the owner:** the duplicate groups in the Context stay as
  recorded for the burn-down decision. Two approved-row tag mismatches
  (LLR-061's tag at `agent_brief._predecessor_lines`; `bootstrap`'s
  `Implements: LLR-155`) predate the move, as the reviewer confirmed.

## Context

Drafted by WI-542 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

`needs` added 2026-08-31: this row decomposes `agent_loop.py`, `integrate.py`
and `dispatch.py` — the modules the OI-70 repair rows (`WI-552`, `WI-553`)
change. Sequencing it behind them avoids two ratchet re-stamps and a merge
conflict (`docs/handoff-2026-08-31.md` §2).

Recorded 2026-09-28 (WI-657 part 4's research sample, `docs/plans/2026-09-28-duplicated-stage-detection.md`), for the owner's burn-down decision and not an obligation of this row: live code duplicates the samples turned up. `intake.normalize_bar` and `integrate._normalize_bar` (one bar vocabulary in two tables); `plan_artifacts.parse_plan_wis` (its docstring still cites the retired F5 rule); the two `_clip` functions, whose elision markers have diverged; `trace.if_note_advisories` and `trace_text.cite_advisories`; `check_trajectory.approval_brief_findings` and `trace.ruled_open_item_texts`; `trunk_step`'s two argv builders; `spec_move.rewrite_text` and `trunk_step.rebase_links`; and the four small census copies. A split this row makes may take one where it is a pure move.

The standing census (`check_dupes_census.py`, 5/5/52 against a 0/0/0
stamp, warn-only) names five exact-body duplicate groups on trunk
2026-09-28, recorded for the same burn-down decision:
- `agent_common.read_toml_text` / `kitlib/spine._toml_tables`;
- `agent_common.human_approves` / `human_approves_spine`;
- `check_complexity._is_docstring` / `check_stubs._is_docstring`;
- `check_trajectory.read_rows` / `gen_release_checklist.load_csv`;
- `frame_rules._entries` / `kitlib/spine.seam_endpoints`.

## Done-when

- `tests/test_module_size_ratchet.py` names this row as the debt owner in its
  module docstring, its `decompose (…)` finding message and its baseline-entry
  comments, and names no terminal row as the owner.
- `agent_loop`, `agent_common` and `bootstrap` are each re-measured against the
  specref's derived map, then split along it or recorded in this row's
  Deliverable as left whole, with the reason.
- `check_trajectory`'s remaining fused pairs, `tests/test_trajectory_arch.py`
  and `tests/test_agent_loop.py` are split by behaviour boundary rather than
  line count, or re-homed as below.
- Every split is a pure move proven by equality (byte-identical moved symbols,
  node-id set equality), and its module-size baseline is re-stamped down in the
  same commit, never bumped.
- Debt still unpaid at close is re-homed to a named successor, and the close
  commit moves the ratchet's owner pointer to it.
