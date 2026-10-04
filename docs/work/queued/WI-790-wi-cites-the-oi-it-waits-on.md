+++
id = "WI-790"
title = "Work items cite the open items they wait on; open items stop carrying wi_refs"
workstream = "process"
specref = "docs/requirements/interfaces.toml"
sr_refs = ["SR-148"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-03, at the owner's direction, while
OI-101 was being raised for WI-788. The owner's words:

> "In regard to acceptance criteria: Would this be okay where unknowns can reference
> the open items and then other details can be flushed out? That was responses to
> open items can specifically update work items with the OI reference, but in this
> case OIs no longer need to carry the WI link (Because instead the WI would
> reference them). This perhaps needs to be a separate item to align that detail."

**This reverses part of WI-746's design** (ruled 2026-10-02, landed `9dbb5103`).
WI-746 made the open-item registry own the block: a queued row named in a pending
open item's `wi_refs` is not offered, "the work-item row format does not change",
and ruling the item "releases the row with no edit to it". It also said "`needs`
stays work-item to work-item only. No `needs = ["OI-..."]` edge and no new
`blocked_by` key."

The owner's new flow removes WI-746's main reason. A ruling now edits the work item
on purpose: it writes the decided criteria into the spec, citing the OI. A row that
is edited at every ruling gains nothing from a block that needs no edit. The block
then lives where the unknown is cited: in the work item.

What exists (checked 2026-10-03):

- **Two readers already gate readiness on open items** (`schedule.hard_preds_satisfied`):
  - the `wi_refs` block (WI-746; IF-073, IF-054, LLR-288, LLR-289, TC-301, TC-302);
  - the legacy `OI-###` token in a row's `needs` (`kitlib/spine.split_pred_edges`),
    which is satisfied once the item leaves `pending` and fails closed when the item
    is absent. It is kept only because approved TC-253 (IF-176, LLR-058) requires it,
    and nothing mints such tokens now.
- WI-788's owner ruling on risk 7 lists that legacy reader as a dual path to retire
  or justify. This item justifies it, by making it the one path, and retires the
  other.
- Row states: LLR-288, LLR-289, TC-301, TC-302, LLR-058 and TC-253 are Approved;
  IF-054, IF-073, IF-176, IF-264 and IF-265 are Drafted. So amending them goes
  through in-lane adjudication.
- Live pending open items with `wi_refs`: OI-98 (WI-684) and OI-101 (WI-788). OI-100
  names none.

## Owner rulings (2026-10-03)

The owner confirmed the design below ("Yes") and added three directions. In the
owner's words:

> "note open-items.toml (including the template) can indicate that older versions may
> reference a WI token, but has since been updated such that OIs no longer have a WI
> pointer, and instead WIs point to open items. Note also them that the surface to
> generate open-items.html changes: Open items only surface there if queued
> work-items points to an open item. This should also modify the adjudicator brief so
> that items that get created as work items at intake ALSO require a work item
> placeholder to point to that work item. This also guarantees that any open items
> that is minted in reaction to a handback ALSO has a queued work item on the
> frontier."

The coordinator's reading:

- Rows filed before this item may still carry `wi_refs`, as inert history that no
  code reads. The registry header says so.
- Every pending open item is surfaced by a queued work item that cites it, and only
  through one. Without one it is invisible, so that is a finding.
- "On the frontier" means the queue. A row blocked by a pending item shows in the
  status snapshot's Blocked list, not the ready frontier, until the ruling releases
  it.
- Today's mint already ties an open item minted from a disposition (the handback
  path) to its successor, because `intake.py`'s `[open_item]` table lives in the
  successor's block ("A standalone OI exit no longer exists"). For that path, only
  the link's direction and the brief change.
- The gap is a hand-filed open item, which must now be filed with its placeholder
  row. OI-100 has none today.

## Design (confirmed 2026-10-03)

1. **The edge is the `OI-###` token in `needs`**: the reader TC-253 already approves,
   with no new key. A work item's Done-when cites the same OI where the unknown sits,
   for example "the glossary's home: OI-101 Q5".
2. **A ruling updates the work item.** Whoever records the ruling writes the decided
   criteria into the spec, citing the OI. The `needs` token stays as satisfied
   history, like a done predecessor.
3. **Open items carry no work-item pointer (IF-073).** New rows have no `wi_refs`.
   The header of `docs/requirements/open-items.toml` and of
   `project-trajectory/registries/open-items.template.toml` says that older rows may
   carry it as history and that work items now point to open items. The template's
   example row drops the cell.
4. **The owner surface follows the queue (IF-074).** `open-items.html`'s pending
   decisions show an open item only when a queued work item's `needs` cites it,
   beside the rows that cite it. The status snapshot's open-items list uses the same
   projection. The approval and re-attestation sections are unchanged.
5. **Every minted open item has a placeholder row.** The disposition brief
   (`prompts/adjudicate-disposition.template.md`) says that the successor carrying an
   `[open_item]` table is the work item that puts the decision on the queue, and
   intake writes the minted id into that successor's `needs` (reverting WI-746's
   writer change). A hand-filed open item is filed with a queued placeholder row
   citing it. The coordinator's status.md note "File new work into an open item's
   Context before minting a row" changes to match.
6. **Checks.** Two `check_trajectory` findings:
   - a `needs` token that names no open item;
   - a pending open item that no queued work item cites. The owner could never see
     it.
7. **Migration.**
   - OI-98's and OI-101's `wi_refs` move into WI-684's and WI-788's `needs`, and
     those pending rows lose the cell.
   - OI-100 gets a queued placeholder row: the build of its gaps.
   - Ruled rows keep `wi_refs` as history.
   - The RESYNC entry does the same for adopters, with no transition reader kept
     (WI-788 risk 9).

## Done-when

- A queued row whose `needs` cites a pending open item is not offered by readiness,
  and is offered once the item is ruled, with a test. The `wi_refs` reader is gone,
  with no second path left.
- `open-items.html` shows a pending open item only when a queued work item cites it,
  beside the citing rows. The status snapshot's open-items and Blocked lists use the
  same projection. Tests cover an uncited pending item (not shown, and a finding)
  and a cited one.
- The open-items registry header, in this repo and in the shipped template, says
  that older rows may carry `wi_refs` as history and that work items now point to
  open items. New rows carry no `wi_refs`.
- intake writes the minted open item's id into the successor's `needs`, and the
  disposition brief says that the successor is the open item's placeholder on the
  queue. A test shows that a handback disposition with an `[open_item]` table yields
  a queued, blocked row citing the new item.
- `check_trajectory` reports a `needs` OI token that resolves to no open item, and a
  pending open item that no queued work item cites.
- IF-073, IF-074, IF-054, IF-176, LLR-058, LLR-288, LLR-289, TC-253, TC-301 and
  TC-302, plus whatever pins the disposition brief's open-item clause and the
  snapshot's lists, are amended (or retired where they only describe `wi_refs`)
  through in-lane adjudication. The rule is stated once, in IF-054 and IF-073, and
  PROCESS.md, `docs/work/README.md` and the templates link to it.
- Migration as in design 7. The status.md filing note is updated.
- A RESYNC_PACK entry migrates adopters.
- The commit bar passes.
