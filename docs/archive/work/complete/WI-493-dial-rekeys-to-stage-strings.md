+++
id = "WI-493"
title = "Re-key human_ratification_through from the 0-4 tier ordinal to DevStg-* stage strings (OI-21 D4 shape (ii), owner-directed 2026-08-20; supersedes shape (i) at execution)"
specref = ""
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

FOLDED INTO WI-498 slice 5 and closed there (commit named in
docs/log.d/2026-08-21-wi498-stage-unification.md, "Slice 5"). The owner's ruled
stage-unification plan names this fold, which was this row's wake condition: the
deferment was the owner's dial, and the plan exercising OI-21's shape-(ii)
clause is the owner exercising it.

**The dial takes a rung.** `[attestation] human_ratification_through` is a
`DevStg-*` value — the HIGHEST rung a human still ratifies — and every rung AT
OR BELOW it is human-held. `DevStg-Below` means nothing is held. The shipped
default is `"DevStg-Release"` (everything), which is what `4` meant.

**`DIAL_HOLDS` RETIRED RATHER THAN RE-KEYING, and that is the finding this row
did not anticipate.** Its spec said "DIAL_HOLDS (retired or re-keyed) — the
session decides". The table existed to bridge TWO vocabularies: an ordinal
counting ratifiable TIERS and a ladder of labelled RUNGS. Shape (i)'s own
argument against the retired `stage < level` arithmetic was that it compared two
different ladders that happened to line up. Under one vocabulary there is only
one ladder, so the comparison stops being a coincidence and becomes the
definition — `stage_ord(stage) <= stage_ord(dial)`, the exact mirror of the
at-or-above rule slice 2 gave check selection. The bridge had nothing left to
bridge.

**Equivalence driven BEFORE the table was deleted, not asserted after**: all
five former levels hold precisely the same rung sets under the ordinal rule
(0 → 0 rungs, 1 → 2, 2 → 4, 3 → 5, 4 → 8). The old table's most hand-reasoned
property — `DevStg-Boundary` rides `DevStg-Needs` and `DevStg-Arch` rides
`DevStg-Reqs`, chosen because it errs toward MORE human involvement — falls out
of the LADDER ORDER for free, because each inserted rung sits immediately above
the rung it was made to ride. A hand-reasoned property became a structural one.

**The migration is loud, not silent, and it cost a defect to get right.** A
legacy 0-4 int is READ, translated through `LEGACY_DIAL_ORDINALS` and WARNED
about once per run naming `bootstrap.py --migrate-config`, which rewrites it in
place. The first shape of that window declared "the previous TYPE is still
accepted", and it was wrong in a way worth recording: it accepted every int, so
`human_ratification_through = -1` — the single input the retired `(0, 4)` range
row existed to refuse, because it is the one that reads as LESS human
involvement than the owner asked for — stopped being refused at all. The window
is now the exact SET of translated values (`PROCESS_KEY_LEGACY_VALUES`, filled
from the translation table so the two cannot disagree), with a bool guard because
`True == 1` in Python and a `true` dial must take the wrong-type refusal.
Out-of-range ints and unknown strings are refused by `config_conflicts` and fall
back to the most conservative rung. Driven across the whole value matrix.

**The range row became a VOCABULARY row.** `PROCESS_KEY_RANGES`' `(0, 4)` entry
retired with the ordinal and `PROCESS_KEY_VOCAB` carries the same guarantee on
the new value's terms — a misspelled rung is unrecognized, so it falls to a
default rather than to what was meant, which is the identical hazard.

**What did NOT move, per OI-21's emphasis:** the dial still says which SPINE
rungs a human ratifies. It was NOT re-keyed to artifact DEPTH — that is a change
to WHEN A HUMAN IS RE-ENGAGED whose wrong-answer direction is silently less
human involvement, and it stays its own decision. `APPROVAL_RUNGS` (OI-30 D3's
off-spine sibling) is unchanged.

Touched, per the spec's verified surface: `agent_common.py` (the type row, the
range/vocabulary tables, `ratification_level` → **`ratification_through`**,
`RATIFICATION_FALLBACK`, `LEGACY_RATIFICATION`, `DIAL_HOLDS` deleted,
`human_holds`), `bootstrap.py` (its F5 copy of the legacy table, the new
`LEGACY_DIAL_ORDINALS` pinned equal by `test_rule_sync`, and
`_migrate_dial_ordinal` on the `--migrate-config` arm), `docs/process.toml` +
`process.toml.template`, and the docs that teach the dial. `agent_common.py`'s
"THE DIAL DOES NOT MOVE" block now records that it moved here, deliberately —
which is what the spec asked for.

RESYNC entry: shipped, inside slice 5's single migration entry set rather than
as its own, because an adopter takes both in one re-sync and the dial's steps
belong in the recipe they will actually run.

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
