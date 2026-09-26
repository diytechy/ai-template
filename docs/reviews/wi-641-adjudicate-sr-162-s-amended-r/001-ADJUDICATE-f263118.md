# ADJUDICATE — WI-641 — amendment at f263118

Question judged, per row, and the only one: did the amendment change the
requirement's MEANING, or only its CLARITY?

## The anchor

The rendered brief names its baseline as `docs/archive/last_approved`, "copied
2026-09-06 (commit cde260dd)". That stamp is the newest write anywhere in the
snapshot directory, and cde260dd copied `stakeholder-needs.toml` alone. The copy
this row is measured against is
`docs/archive/last_approved/docs/requirements/system-requirements.toml`, last
written at 27a30842 (2026-08-23) (`git log -1` on that path). The stamp's
imprecision is part of the brief defect filed as WI-646.

## In-scope amended row: adjudicated here, counted (1)

This row's scope is SR-162, which its title and `## Context` name. Loading both
sides and diffing every key: SR-162 differs in `rationale` alone. `title`,
`requirement`, `acceptance_criteria`, `sn_refs`, `boundary_refs`, `hat_refs`,
`priority`, `verification`, `status` and `phase` are byte-identical, and the row
is `Approved` on both sides.

The amendment deletes the tail of the rationale's last sentence. BEFORE: "…is a
REVIEW obligation this row does not claim to mechanize, and no SR states it
yet." AFTER: "…is a REVIEW obligation this row does not claim to mechanize."
Nothing else in the cell moved. The deleted words were a claim about the rest of
the registry, not about this row, and that claim has since gone false: SR-185
("Coordinated requirement/interface change review", Drafted, citing SN-037) now
states SN-037's last clause as its own obligation.

- [CLARITY] SR-162 Rationale -> every promised behavior's entry and exit resolves at a declared boundary (resolution hard, coverage advisory), every referenced interface is typed discrete or variable with incompatible types a finding, and SN-037's coordinated-review clause is named as a residual this row does not mechanize -> the same three statements, with the residual still named and still disclaimed -> the only words removed describe whether some other SR carries the residual; they impose nothing on a builder or a test of this row, and the `requirement` and `acceptance_criteria` cells that state the obligation are untouched.

## Rendered, out of scope, excluded from the count (19)

The amendment brief (`adjudicate_brief.amendment_values`) renders every drifted
approved row in the tree, not this row's scope: an amendment mint writes no
typed `Adjudicates` cell, and the assembler does not filter by one. The count
above follows the rule WI-566's review corrected its own verdict to
(`docs/reviews/wi-566-adjudicate-llr-058-llr-144/001-ADJUDICATE-05fb6a3.md`) and
WI-573 applied: a verdict counts its own row's scope. The whole-tree rendering is
filed as WI-646. **The rows below are not adjudicated here and are not counted
by the `VERDICT:` line.**

- SR-024, SR-033, SR-043, SR-052, SR-053, SR-054, SR-111, SR-112, SR-129,
  SR-144, SR-146, SR-147, SR-149, SR-167, SR-175, SR-176, SR-177 (`rationale`
  only): ruled CLARITY at WI-547 (fb0ed7c), WI-593 (ae3d788) and WI-599
  (993e455). Their live text is byte-identical to what WI-593 judged: each row
  was loaded from `ae3d788:docs/requirements/system-requirements.toml` and from
  the working tree, and all seventeen compare equal.
- LLR-061 (`detail`): adjudicated by WI-601.
- LLR-167 (`detail`): adjudicated by WI-603.

## Aftermath

None owed. A CLARITY verdict leaves the row's attestation standing, and nothing
in the registries was edited here.

The anchor still lags the live row, so the drift detector keeps raising SR-162
until an approval act copies the requirements registry (the WI-593 observation).
WI-642 is that act. Its snapshot must name this verdict and WI-547's for
`system-requirements.toml` (`--approves`), because the tool refuses to absorb
drifted approved text that a Status flip alone does not authorise.

VERDICT: CLARITY rows=1
