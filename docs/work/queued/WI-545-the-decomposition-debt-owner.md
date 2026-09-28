+++
id = "WI-545"
title = "The decomposition debt owner (cont.): three wide modules, check_trajectory's remaining fusion, and M-06's last two test monoliths"
workstream = "process"
specref = "docs/plans/2026-08-25-remap-alignment.md"
buildtier = "strong"
priority = 1
safety_class = "ordinary"
supersedes = "WI-521"
needs = ["WI-579", "WI-580", "WI-581", "WI-620", "WI-583"]
+++

## Context

Drafted by WI-542 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

`needs` added 2026-08-31: this row decomposes `agent_loop.py`, `integrate.py`
and `dispatch.py` — the modules the OI-70 repair rows (`WI-552`, `WI-553`)
change. Sequencing it behind them avoids two ratchet re-stamps and a merge
conflict (`docs/handoff-2026-08-31.md` §2).

Recorded 2026-09-28 (WI-657 part 4's research sample, `docs/plans/2026-09-28-duplicated-stage-detection.md`), for the owner's burn-down decision and not an obligation of this row: live code duplicates the samples turned up. `intake.normalize_bar` and `integrate._normalize_bar` (one bar vocabulary in two tables); `plan_artifacts.parse_plan_wis` (its docstring still cites the retired F5 rule); the two `_clip` functions, whose elision markers have diverged; `trace.if_note_advisories` and `trace_text.cite_advisories`; `check_trajectory.approval_brief_findings` and `trace.ruled_open_item_texts`; `trunk_step`'s two argv builders; `spec_move.rewrite_text` and `trunk_step.rebase_links`; and the four small census copies. A split this row makes may take one where it is a pure move.

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
