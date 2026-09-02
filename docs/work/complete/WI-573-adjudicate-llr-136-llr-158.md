+++
id = "WI-573"
title = "adjudicate: LLR-136, LLR-158 - approved/routed cell(s) amended on merged trunk 4d0b972..4248072 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
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

- LLR-136 `Detail`: 'Converts between the spec folder (the live docs/work/ home) and the retired CSV form (docs/requirements/work-items.csv)…' -> 'Converts between the spec folder (the live docs/work/ home) and the retired CSV form (docs/requirements/work-items.csv)…'
- LLR-158 `Detail`: 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…' -> 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

## Dispositions

```toml
title = "LLR-158's declared registry bound is stale: state the shipped APPROVAL_ACT_CSVS partition in the Detail and code_symbol cells"
workstream = "process"
safety_class = "spine"
buildtier = "medium"
priority = 2
specref = "docs/requirements/low-level-requirements.toml"
bar = "DevStg-Reqs"
```

VERDICT THIS CONTINUES: `docs/reviews/wi-573-adjudicate-llr-136-llr-158/001-ADJUDICATE-07cbabb.md`,
governing line `VERDICT: MEANING rows=2` over `LLR-136` and `LLR-158`. Both are
MEANING, so the flip-back arm does not apply; this successor exists because the
re-attestation the rung released to the loop was WITHHELD, and why it was
withheld is a build gap rather than a signature gap.

IN SCOPE — one cell's last clause and one `code_symbol` cell.
`LLR-158`'s `Detail` closes with *"every reader here walks `SPINE_CSVS`, the
three spine registries … the four other registries a snapshot anchors are listed
in `OUTSIDE_THE_APPROVAL_ACT`"*. The module it owns says otherwise:
`staged_approval_acts` and `lane_approval_refusal` walk `APPROVAL_ACT_CSVS` —
the spine three PLUS `stakeholder-needs.toml` (`acceptance_record.py:144`, :541;
`tests/test_acceptance_record.py:216`) — `OUTSIDE_THE_APPROVAL_ACT` holds three
registries and not four (:165), and the pinned exhaustive identity is
`SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT` (:162,
`tests/test_acceptance_record.py:234-235`). The cell was written at `d5b3e124`
and the widening landed after it at `94b77a26`; the row was never re-read
against its own rework. Re-state the bound as shipped, add `APPROVAL_ACT_CSVS`
to the row's `code_symbol` beside `OUTSIDE_THE_APPROVAL_ACT`, and say which
constant each of the four readers walks — the row's whole claim is that a tier
joining the snapshot cannot reach no approval reader, and a false partition
makes that claim unfalsifiable rather than merely imprecise.

OUT OF SCOPE — the design. `APPROVAL_ACT_CSVS` covering the need tier is the
2026-09-01 ruling as WI-572 round 028 applied it, and this row does not reopen
it. Nothing in `acceptance_record.py`, `intake.py` or the tests changes; this is
a requirement-tier correction to make the row true of the code that shipped.

NOT ON THIS LANE — the anchor. This lane corrects the text and then STOPS. It
does not run `python project-trajectory/scripts/intake.py snapshot` in any
form and it writes nothing under `docs/archive/last_approved/`. Taking the
snapshot is never a work lane's act — the approval act (the `Status` flip and
the anchor that records it) belongs to a trunk-side adjudication session
(`docs/plans/2026-09-01-approval-act-adjudicator-only.md` §2a) — and
`lane_approval_refusal` refuses any lane merge whose delta touches
`SNAPSHOT_DIR`, so taking the anchor here would hard-refuse this very row's
merge.

WHERE THE RE-ANCHOR HAPPENS INSTEAD — at THIS successor's merge. Correcting an
Approved row's text stages a `staged_spine_amendments` hit, which mints an
amendment adjudication at that merge. That trunk-side adjudicator, on a rung
released to the loop and with the defect this verdict withheld against now
corrected, performs the re-attestation under the released-rung aftermath arm of
`project-trajectory/prompts/adjudicate-amendment.template.md`: every row's
`Status` stays `Approved`, and `python project-trajectory/scripts/intake.py
snapshot --approves "docs/requirements/low-level-requirements.toml=<that
adjudication row's id>"` is taken on trunk in its own reviewed commit. Nothing
about that is owed to this lane, and nothing about it is owed to the owner: the
LLR rung sits above the approval threshold.

Because `copy_live` mirrors whole registry files, that one act also re-anchors
`LLR-136` — whose amended text this adjudication verified accurate and would
have blessed on its own — and `LLR-058`, `LLR-144`, `LLR-198`, the WI-566
MEANING set whose text likewise matches the tree. Naming only the LLR registry
there is deliberate: the SR and TC registries hold rows this row did not judge.
