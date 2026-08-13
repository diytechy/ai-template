+++
id = "WI-443"
title = "OI-14 part B program (ruled B1, 2026-08-13): declare the interface contract and build IF's first schema tier, warn-first, then convert interfaces.csv and components.csv to the TOML carrier in the same batch (they have waited on this ruling precisely to convert once). The contract: an IF row is an INTERFACE only — what crosses, typed discrete-vs-variable (a NEW column plus its validation; zero rows carry any typing today) — with a Rationale home added so the why stops squatting in Contract. The schema tier: required fields; closed vocabularies for Stability, for Status (OI-13/D-9 parked IF's Status HERE — rule it in this pass; Stable currently appears in Status and Stability on one row meaning different things), and for the new type; a refusal when a component boundary has an uncovered crossing. The four negative rules, warn-first then promoted to ERROR once the corpus converges: refuse a work-item id in Contract (fires on ~24 percent today), refuse a repo-lock D-n citation (14 rows), warn on rationale connectives (because / rather than / so that / since), warn above a 500-character ceiling (34 rows). Existing cells migrate as rows are touched (B1, not B2 — no bulk rewrite nobody can review). Sequenced after part A because A decides which rows exist."
workstream = "lock-program"
sr_refs = []
needs = ["WI-441"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Deliverable

Completed 2026-08-13, all four stages. The contract is declared in PROCESS.md
§8 (an IF row is an interface only; Contract = what crosses + its Signal; the
why lives in Rationale; Stability the one maturity field; +829 B, baseline
re-stamped through the materializer). Both remaining registries joined the
TOML carrier ([interface.IF-###], [component.CMP-###]) via migrate_carrier
with the round-trip proven, CSVs deleted (dual-carrier = hard refusal), the
shipped templates converted, 13 reader modules rewired. The IF tier changed
shape: Status RETIRED (D-9's parked question executed — undeclared,
self-overlapping, and the LLM brief surface no longer carries it), signal
(discrete|variable — 7/106 live, 25 with a signal_note) and rationale added,
the four Provisional values mapped to Experimental. The warn-first schema
tier landed in trace.py's own REQUIRED_FIELDS/ENUM_FIELDS dicts routed
through a schema_advisories twin (exit untouched at every gate): live counts
— WI-id-in-Contract 38 warns / 27 rows, D-n citations 3 (the brief's 14 did
not reproduce: 11 rows cite a D-n somewhere, 3 in Contract — measured
correction), rationale connectives 24, >500 chars 34, vocabulary guards
zero-to-zero, and the endpoint advisory the data pack demanded (48 vacuous
rows classified: 24 files, 13 actors, 11 RESOLVING TO NOTHING — real rot
surfaced immediately, 8 endpoints fixed where this commit staled them).

Surprises recorded: "Status read by nothing mechanical" was FALSE — two
hidden check_trajectory readers found and re-keyed onto Stability, one of
which had been a tautology that could only report zero (103 of 108 Stable
seams carry no contract test — now one honest summary line). At the serial
merge the coordinator ported 443's ADOPTING §6 recipe delta into the pack as
the carrier-batch-3 entry [since 2eb1c0c8] (ADOPTING had shrunk under
WI-447), generalized WI-450's snapshot helper to the TOML carrier, and
retired status.md's now-false "waits on" prose. +18 new tests, ~35 rewired.
Builder bars: full 2403 passed / 1 pre-existing containment failure (healed
by the LLR-168 seed before this merge); smoke 1058 passed post-merge; strict
integrity clean; real scaffold green.
