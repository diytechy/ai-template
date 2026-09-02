## 2026-09-02 — WI-573: LLR-136 and LLR-158 both MEANING; the re-anchor withheld for a real defect and routed to the successor's merge

**Session type:** amendment adjudication (`brief = "amendment"`,
`safety_class = "adjudication"`), branch
`wi-573-adjudicate-llr-136-llr-158` over trunk `07cbabb5`. Read-and-judge only:
no registry cell, no `Status`, and no file under `docs/archive/last_approved/`
was touched.

Deferred open items: none — the correction is drafted as this row's ## Dispositions successor and minted at merge; no question is owner-owed.

**The two rulings** (verdict:
[../reviews/wi-573-adjudicate-llr-136-llr-158/001-ADJUDICATE-07cbabb.md](../reviews/wi-573-adjudicate-llr-136-llr-158/001-ADJUDICATE-07cbabb.md),
governing line `VERDICT: MEANING rows=2`). `LLR-136` `Detail` — **MEANING**: the
amendment adds two binding statements (`read_specs` takes its population from
`spec_paths` rather than a second folder walk; `COLUMNS` is pinned equal to
`kitlib.registry.WI_COLUMNS`), each of which turns a design legal under the old
text into a defect. `LLR-158` `Detail` — **MEANING**: the old text obliged one
comparison function; the new text obliges a shared two-tree walk
(`_spine_row_sides`), four named consumers, the exempts-vs-reports invariant,
and a declared registry partition. The other twenty-five drifted rows in the
material were excluded from the count as already closed by WI-566 and WI-547.

**The withhold, and the defect behind it.** The rung is released to the loop, so
the re-attestation was this session's own act to take. It was WITHHELD, under the
exception the released-rung arm of
[../../project-trajectory/prompts/adjudicate-amendment.template.md](../../project-trajectory/prompts/adjudicate-amendment.template.md)
states: `LLR-158`'s new closing clause is false of the code the row owns —
`staged_approval_acts` and `lane_approval_refusal` walk `APPROVAL_ACT_CSVS`
(the spine three plus `stakeholder-needs.toml`), not `SPINE_CSVS`;
`OUTSIDE_THE_APPROVAL_ACT` holds three registries, not four; and the pinned
identity is `SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT`
(`acceptance_record.py:144`, `:162`, `:165`). The cell was written at `d5b3e124`
and never re-read against the widening that landed at `94b77a26`. Since
`copy_live` mirrors whole registry FILES, `LLR-136` could not be anchored
without `LLR-158` riding along, so both stay drifted — visibly, on the
re-attestation surface (`trace.reattest_model` → `docs/ratify/CURRENT.md` and
the generated `open-items.html`), which is a loop-side surface and not a pending
owner signature. The correction is drafted in the closed spec's
`## Dispositions`.

**Round 002 and this rework.** The supervisor-drawn round
([../reviews/wi-573-adjudicate-llr-136-llr-158/002-REVIEW-A-446e19e-supervisor.md](../reviews/wi-573-adjudicate-llr-136-llr-158/002-REVIEW-A-446e19e-supervisor.md))
confirmed both rulings and the withhold independently, and returned
CHANGES-REQUESTED on three findings. The MAJOR: the drafted successor told its
own worker lane to take the anchor, but that row mints `safety_class = "spine"`,
so it is an ordinary lane, and `lane_approval_refusal` refuses any lane delta
touching `SNAPSHOT_DIR` — the instructed commit would have hard-refused the
successor's merge, and it is the same author-blesses-own-work separation the
2026-09-01 ruling exists to prevent
([../plans/2026-09-01-approval-act-adjudicator-only.md](../plans/2026-09-01-approval-act-adjudicator-only.md)
§2a). No guard is owed; the defect was in the drafted scope. This rework
rewrites that scope so the successor corrects the `LLR-158` `Detail` text and
its `code_symbol` cell and STOPS — running no `intake.py snapshot` and writing
nothing under `docs/archive/last_approved/` — and states where the re-anchor
happens instead: at that successor's own merge, through the amendment
adjudication its `staged_spine_amendments` hit mints, whose trunk-side
adjudicator re-attests on a released rung with `Status` left at `Approved` and
`intake.py snapshot --approves` taken on trunk in its own reviewed commit. That
one act also re-anchors `LLR-136` and the WI-566 MEANING set. The two MINORs are
fixed with it: the verdict's "owner's re-attestation brief" sentence is
re-worded to the accurate loop-side surface (the single machine line
`VERDICT: MEANING rows=2` unchanged, re-issued in place), and this fragment is
the record round 002 found missing.
