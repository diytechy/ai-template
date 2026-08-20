+++
id = "WI-493"
title = "Re-key human_ratification_through from the 0-4 tier ordinal to DevStg-* stage strings (OI-21 D4 shape (ii), owner-directed 2026-08-20; supersedes shape (i) at execution)"
specref = "docs/requirements/open-items.toml#OI-21"
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

DEFERRED BY THE OWNER AT MINT (2026-08-20): the direction is decided — the
dial converts to a string — but it sits here until the owner wakes it.
OI-21 ruled shape (i) (the int dial MAPPED onto the stage ladder via
`agent_common.DIAL_HOLDS`, executed by WI-445) and named this exact
conversion as shape (ii), available to supersede (i) after OI-14 landed
(it ruled 2026-08-13). This WI is the owner exercising that clause; at
execution it retires shape (i)'s bridge, and `agent_common.py`'s "THE DIAL
DOES NOT MOVE" block updates to record that it moved here, deliberately.

- **The conversion:** `human_ratification_through` takes a `DevStg-*` rung
  from the closed `LADDER_RUNGS` vocabulary instead of an int 0-4; the
  legacy int (and the `LEGACY_RATIFICATION` modes) read through a
  migration shim or are rejected with a naming message — the session
  decides which, and the choice ships downstream (RESYNC entry owed
  either way; `process.toml.template` and `docs/process.toml` both move).
- **The touch surface** (verified 2026-08-20): `agent_common.py` — the
  `PROCESS_ONLY_KEYS` int type row, `PROCESS_KEY_RANGES` (0,4),
  `ratification_level()` + `RATIFICATION_FALLBACK`, `DIAL_HOLDS` (retired
  or re-keyed), `human_holds()`/`human_approves()`; `bootstrap.py`
  scaffold defaults; help/comment citations in `intake.py`, `dispatch.py`,
  `check_need_form.py`; docs (`PROCESS.md`, `PROCESS_OPTIONS.md`,
  `KICKOFF_PROMPT.md`, `README.md`s, `gate-policy` legacy pair, the
  gate-advance skill's three materialized copies); and the asserting
  tests — `test_ratification_level.py` (its "the dial did NOT move" pin
  inverts), `test_bootstrap.py`, `test_process_config.py`,
  `test_gate_policy.py`, `test_intake.py` (malformed-value arms),
  `test_dual_plan_round.py`, `test_agent_loop_critique.py`,
  `test_rule_sync.py`, `test_check_need_form.py`.
- **Semantics guard:** the dial's MEANING (which spine tiers' ratification
  the human holds) does not change — only its vocabulary does. The
  OI-30 D3 constraint stands: a generated file never carries an approval.
- **Wake condition:** owner's word; the natural moment OI-21 named is
  IF/CMP maturity joining the ratifiable fold, but the deferment is the
  owner's dial, not a dependency edge.
