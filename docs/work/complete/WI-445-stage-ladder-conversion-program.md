+++
id = "WI-445"
title = "OI-21 execution program (all five questions ruled 2026-08-13): retire every G* tag for the eight-rung stage ladder (Needs / Boundary / Reqs / Arch / LLReqs / Tests / Impl / Release — requirements BEFORE architecture, boundary happens once, rungs 2-3 recurse, rung 4 terminal via OI-20's binding rule). The label is the identifier (DevStg-<Label>), position DERIVED (stage-ord/stage-of on the basis line), every comparison through a STAGE_ORDER lookup that RAISES on unknown — fix the two label typos (Arcitecture, Impliment) before they become identifiers. The sweep is TAG-SCOPED (the word gate survives where it means a-check-that-can-fail), lands WITH the refusal enforcer on retired vocabulary in authored surfaces (archive and attestation quotes exempted), and carries the ~30 attestation-quote carve-out sites verbatim with a header note. docs/gate migrates on the proven precedent: field-compatible, one forced regenerate. Six contract breaks handled: check.py --gate choices, stack.ini gates=, WI bar: enum, the [phase]-[gN] title archetype, the basis-line format, LOG.template.md's sign-off table (sittings stay their own axis — rows name the rung range they certify; ruled with D-10's approval log or they diverge at birth). The gate-advance skill rewrites through the materializer. The dial MAPS onto the ladder (shape i); keying approval to artifact depth+tier is ruled there too, never defaulted. Rung predicates land as ONE sequence with the D-9 ladder migration (repo-lock section 5 step 7) — including the IF/CMP maturity vocabulary joining the min-fold, which is what makes the recursion self-reporting. The adopter recipe goes into ADOPTING section 6 as prose NOW and migrates into the OI-27 pack as its inaugural entry."
workstream = "lock-program"
sr_refs = []
needs = ["WI-441", "~WI-444"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Deliverable

Completed 2026-08-13, all stages. The G* TAGS retired; the word "gate" survives
where it means a check that can fail. The eight-rung ladder
(`DevStg-Needs · Boundary · Reqs · Arch · LLReqs · Tests · Impl · Release`)
and its three bars (`DevBar-Reqs`/`-Tests`/`-Release`, each named for the top
rung it certifies) are computed by `derive_gate.py`; the label is the
identifier, position is derived (`stage-ord`/`stage-of` on the basis line), and
every comparison routes through `stage_ord`/`bar_ord`, which RAISE on an
unknown value. Both ruled typo candidates fixed before they became identifiers.

All six contract breaks disposed: `--gate` keeps the retired tags as WARNED
aliases; `stack.ini gates=` and the WI `bar:` enum translate silently; the
`[phase]-[gN]` archetype converts for new titles while the committed anchors
parse forever; the basis line took one forced regenerate with no compat shim;
`## Gate Sign-offs` became `## Sittings` (heading, `RESERVED_HEADINGS` and its
test together), rows naming the rung range they certify.

The dial was MAPPED, not re-keyed: `agent_common.DIAL_HOLDS` is the declared
lookup replacing `stage < level`, preserving every pre-existing answer for the
four spine rungs and holding the two inserted rungs with the rung BELOW them.
Rungs 1 and 3 compute from the IF and CMP registries through one declared
maturity table, both APPLIES-WHEN, which is what makes the recursion
self-reporting.

The enforcer landed WITH the sweep as ruled: `check_vocab.py` (new, shipped
downstream, SR-149/LLR-169/TC-163), warn-first and ERROR under `--strict` from
`DevBar-Tests` on. `tests/test_stage_ladder.py` greps for lexical comparisons
on a ladder value and caught a real one on its first run (`check.py --list`
printed each step's bars in alphabetical order, which the retired tags made
accidentally right). The carve-out — archive, the log's dated entries, the
attestation briefs, closed WI specs, generated surfaces — is preserved verbatim
with header notes in `docs/log.md` and the new `docs/ratify/README.md`.

RESYNC_PACK gained the anchored §3 recipe and the §4 translation row; ADOPTING
§6 records the `docs/gate` preserve-always override in place; the
`gate-advance` skill was rewritten through the materializer.

Evidence: full unfiltered suite 2450 passed / 7 skipped; smoke 1091 passed /
3 skipped; `trace.py --strict-integrity` rc 0 (orphans=0, integrity=0);
`check_vocab --strict` clean over 386 live authored files; a real scaffold
bootstrapped from this tree runs its own harness green with `docs/gate`,
`stack.ini`, hooks and CI all speaking the new vocabulary. Registry rows
flipped: SR-004 and SR-053 Verified -> Modified.
