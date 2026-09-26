# ADJUDICATE — WI-603 — amendment at f263118

Question judged, per row, and the only one: did the amendment change the
requirement's MEANING, or only its CLARITY?

## The anchor

The rendered brief names its baseline as `docs/archive/last_approved`, "copied
2026-09-06 (commit cde260dd)". That stamp is the newest write anywhere in the
snapshot directory, and cde260dd copied `stakeholder-needs.toml` alone. The copy
this row is measured against is
`docs/archive/last_approved/docs/requirements/low-level-requirements.toml`, last
written at 2e1197fd (2026-09-04) (`git log -1` on that path). The stamp's
imprecision is part of the brief defect filed as WI-646.

## In-scope amended row: adjudicated here, counted (1)

This row's scope is LLR-167, which its title and `## Context` name. Loading both
sides and diffing every key: LLR-167 differs in `detail`, the approved cell the
brief shows, and in `code_symbol`, a traced cell ruled non-attesting (§A5.1).
The traced cell is read here anyway, because a re-anchor copies it too.
`sr_refs`, `title`, `module`, `rationale`, `test_refs`, `status`, `component`
and `phase` are byte-identical, and the row is `Approved` on both sides.

The two `detail` cells agree up to "A refusal falls back to the worker
assignment and PRINTS why." BEFORE then ends: "`conflict` and `amendment` are
deliberately unrouted, each with its missing derivation named in the module
header." AFTER ends instead: every shipped brief is routed; `conflict` is
RETIRED rather than filled, because it had a template and a verdict grammar but
never a mint, an assembler or a reader for the `needs=` its own grammar
demanded; and `consolidate_values` composes the consolidation brief from the
row's `Adjudicates` cluster, re-derived live, with every row of that cluster or
none, refusing when the cluster's overlap has dissolved. `code_symbol` gains
`consolidate_values`, which restates the same change.

- [MEANING] LLR-167 Detail -> the assemblers' shared no-partial contract, with `conflict` and `amendment` shipped as templates that deliberately refuse as unrouted -> the same contract, with `amendment` routed, `conflict` no longer shipped, and a new consolidation assembler carrying its own all-or-none rule and a dissolved-overlap refusal -> the obligation moves in three places: a correct implementation of the BEFORE text (`amendment` refusing as unrouted, `conflict` shipped and refusing, no consolidation brief) fails the AFTER text on each one.

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
- SR-162 (`rationale`): adjudicated by WI-641.
- LLR-061 (`detail`): adjudicated by WI-601.

## Aftermath: judged blessable, joint re-anchor pending

The design-row tier sits above `human_approval_through = "DevStg-Needs"`, so the
brief's derived aftermath says a MEANING verdict here is re-attested by the
adjudicator, in its own reviewed commit after this verdict. Before that, the
AFTER text was checked as text I would bless:

- **Within its parents.** SR-146 requires every launched prompt to be a
  shipped, reviewable file with strictly filled slots. Retiring a template that
  nothing could fill, and routing the rest, serves it directly. The
  consolidation brief is a new prompt within that class, shipped as its own
  reviewable template. SR-148 admits ready adjudication rows first, and a
  consolidation row needs a brief to be admitted into. SR-144's relationship is
  unchanged: its immutable per-close report is still read by the untouched
  `disposition_values` arm. No new actor, external input or surface class
  appears.
- **True of the code at f263118.** `BRIEF_PROMPTS` and `_ASSEMBLERS` both hold
  the same five keys (`amendment`, `first-approval`, `disposition`,
  `consolidate`, `red-tc`), with no `conflict`; the prompts directory ships no
  conflict template; `consolidate_values` refuses a dissolved cluster by name.
- **Exercised.** TC-161's evidence file, `tests/test_adjudicate_brief.py`, pins
  it: `test_every_shipped_brief_is_routed_and_the_retired_one_is_gone` (routed
  equals shipped; a `conflict` row refuses as an unknown brief),
  `test_the_consolidate_brief_composes_every_slot_from_the_registry`, and the
  refusal arms `test_a_consolidation_declaring_no_scope_refuses`,
  `test_a_consolidation_with_no_digests_cell_refuses` and
  `test_a_cluster_whose_overlap_dissolved_refuses_rather_than_briefing`.

Judged blessable. The re-attestation is the re-anchor itself: one separate
commit that also carries WI-601's LLR-061, scoped to
`docs/requirements/low-level-requirements.toml`. WI-601's verdict lists the
file-scope collateral that copy takes: Drafted rows and traced cells, none of
which is an approval.

## Findings

1. **TC-161 contradicts the row it verifies.** Its `method` still ends "Pin the
   two unrouted briefs as unrouted, naming themselves in the refusal." The
   amended LLR-167 says no brief is unrouted, and the test in TC-161's own
   evidence file now pins the opposite. The module docstring of
   `tests/test_adjudicate_brief.py` and the section comment above that test
   still describe the old pinning as well. The method also does not name the
   consolidation arm or its refusals. An approved case whose text asserts what
   its test disproves is a false record, so it gets a follow-up.
2. **Two routed assemblers are named by no design row.** `amendment_values` and
   `first_approval_values` ship and are routed, but no `code_symbol` names
   them. LLR-167's cell lists `compose`, `disposition_values`, `red_tc_values`
   and `consolidate_values`, and LLR-176 names only `adjudicate_brief.compose`.
   The AFTER text's "EVERY shipped brief is routed" is true of the code, so this
   does not withhold the blessing. It predates this amendment: the BEFORE cell
   named neither.

Neither finding touches the text judged here, and neither is fixed in place (the
brief forbids a judge to edit a row it is judging). Both, with WI-601's TC-061
finding, go into the one follow-up drafted in the `## Dispositions` section of
this row's own spec and filed as WI-645. It needs WI-642, because amending the
approved TC-161 or TC-061 creates new drift in `test-cases.toml`. If that landed
before the phase-6 approval act, the act's refresh of that registry would carry
it unread, which is the D28 hazard again.

VERDICT: MEANING rows=1
