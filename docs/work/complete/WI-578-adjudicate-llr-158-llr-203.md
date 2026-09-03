+++
id = "WI-578"
title = "adjudicate: LLR-158, LLR-203, LLR-204 - approved/routed cell(s) amended on merged trunk 2f660cb..0ae37a1 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
+++

## Deliverable

Adjudication verdict recorded on the lane; this row is closed MECHANICALLY at its DONE (OI-70/OI-73). Its `## Dispositions` successors mint at this row's own merge (drafts-not-mints), the mint replaces the superseded row's inbound hard edges, and any human-owed answer becomes a `pending` open item the successor depends on. The verdict artifact is under `docs/reviews/`.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-158 `Detail`: 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…' -> 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…'
- LLR-203 `Detail`: "MAPPING is the declaration SR-163's own reasoning designates as the coverage universe: one row per shipped source, the …" -> "MAPPING is the declaration SR-163's own reasoning designates as the coverage universe: one row per shipped source, the …"
- LLR-203 `Rationale`: 'Naming the inventory that exists rather than a purpose-coverage checker that does not is what keeps this row falsifiabl…' -> 'Naming the INVENTORY, and only the inventory, is what keeps this row falsifiable. The declaration, its exclusion carrie…'
- LLR-203 `Title`: 'The shipped-file inventory and its declared exclusions, carrying no purpose reference' -> 'The shipped-file inventory, its declared exclusions, and its tolerant purpose reference'
- LLR-204 `Detail`: 'backlink_ids is the ONE definition of a purpose declaration in the source surface: an Implements token OPENING a line, …' -> 'backlink_ids is the ONE definition of a purpose declaration in the source surface: an Implements token OPENING a line, …'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

## Dispositions

```toml
title = "The snapshot's scoped writer and unscoped refusal disagree on registry scope"
workstream = "process"
safety_class = "spine"
buildtier = "medium"
priority = 2
specref = "docs/requirements/low-level-requirements.toml"
bar = "DevStg-Impl"
```

VERDICT THIS CONTINUES:
`docs/reviews/wi-578-adjudicate-llr-158-llr-203/001-ADJUDICATE-921f947.md`,
governing line `VERDICT: MEANING rows=3` over `LLR-158`, `LLR-203` and
`LLR-204`. All three are MEANING, so the flip-back arm does not apply. This
successor exists because the re-attestation the rung released to the loop could
not be TAKEN — not because the text is unblessable. WI-573 withheld the same
anchor for a content reason (`LLR-158`'s bound was false); that reason is
closed, and what stands in the way now is the mechanism itself.

THE OBSERVABLE, reproducible at this row's tip. Running the prescribed act,
naming only the registry ruled on —

    python3 project-trajectory/scripts/intake.py snapshot \
      --approves "low-level-requirements.toml=<ref>"

— is REFUSED, and `low-level-requirements.toml` is absent from the refusal:
every row listed is an `SR-###` or `TC-###` the caller did not judge.
`baseline_snapshot.refresh_ledger` at this commit reads
`system-requirements.toml` 17 absorbed rows, `low-level-requirements.toml` 7,
`test-cases.toml` 3, no `flips` anywhere.

THE CONTRADICTION. `copy_live` has been SCOPED since WI-571: it writes only the
registries `--approves` names plus those an approving `Status` move happened in
(`_authorised_registries`), and its own docstring says "an untouched registry is
not written". `refresh_refusal` builds `blocked` from the WHOLE ledger
(`if e["absorbed"] and not e["flips"] and rel not in named`), so it judges
registries the refresh would not touch. WI-571 scoped the writer and left the
gate global.

WHY IT DOES NOT SELF-CLEAR. The 17 SR rows are WI-547's CLARITY verdict, and a
CLARITY verdict owes nothing further by rule — nothing will ever authorise those
cells, so their drift is permanent by design. The 3 TC rows are WI-566's MEANING
verdict, owed on a different registry and a different lane. Under today's gate
the LLR anchor is unreachable until someone signs for registries they did not
rule on, which is the false claim this rung exists to prevent.

IN SCOPE — RULE FIRST, THEN BUILD. Two readings are open and this row must pick
one on the evidence, not assume:

  (a) The gate should be scoped to the writer — `blocked` restricted to the
      registries the refresh will actually write — so a per-registry
      adjudication can complete its own act and untouched registries keep both
      their stale bytes and their visible drift.
  (b) The refusal text is the intended contract ("naming EACH registry above"),
      the snapshot is meant to move as a whole, and what needs rethinking is
      the per-registry adjudication rung that hands one adjudicator authority
      over one registry.

Whichever is ruled, the acceptance is the same shape: a test that a scoped,
authorised, single-registry approval either COMPLETES (a) or is refused with a
message that says why a single-registry act cannot exist (b) — the current
message claims the caller has authorised nothing, which is false, and that
alone is worth correcting under either reading.

THE ANCHOR IS NOT THIS ROW'S STEP (REVIEW-A round 002, finding 1). A `spine`
row is a WORKER LANE, and `acceptance_record.lane_approval_refusal` refuses a
lane that writes `SNAPSHOT_DIR` — by construction, at merge. So this row's
whole scope is the ruling on (a)/(b), the `refresh_refusal` change it implies,
and the test. The re-anchor of `low-level-requirements.toml` is the SUCCESSOR
CONDITION: once this row lands and the act is takeable, the trunk-side
amendment-adjudication rung — the same rung that minted WI-578 — takes it. The
verdict file records that all seven of that file's drifted Approved rows were
re-driven against the tree and are blessable (`LLR-158`/`LLR-203`/`LLR-204`
here, `LLR-058`/`LLR-144`/`LLR-198` by WI-566, `LLR-136` by WI-573, none
amended since); `LLR-206` is `Drafted` on both sides and its first approval
stays its own act.

OUT OF SCOPE — the three rows' text. Nothing in
`low-level-requirements.toml` changes: the cells are correct as they stand and
this row does not reopen them. Nor does it rule on the SR or TC drift; those
belong to the verdicts that own them.
