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

## Design (proposed; the owner confirms or corrects at claim)

1. **The edge is the `OI-###` token in `needs`**: the reader TC-253 already approves,
   with no new key. A work item's Done-when cites the same OI where the unknown sits,
   for example "the glossary's home: OI-101 Q5".
2. **A ruling updates the work item.** Whoever records the ruling writes the decided
   criteria into the spec, citing the OI. The `needs` token stays as satisfied
   history, like a done predecessor.
3. **`wi_refs` leaves the open-item schema (IF-073).** The open-items card's "Work
   items" field and the status snapshot's Blocked list are derived by reverse lookup
   of `needs`: generated, not hand-maintained.
4. **intake writes the edge into the raising row's `needs`** again, and the shipped
   disposition prompt says so (reverting WI-746's writer change).
5. **Checks.** A `needs` token naming no open item is a `check_trajectory` finding. A
   pending open item that no work item cites is legitimate: not every decision gates
   work.
6. **Migration.** Pending items' `wi_refs` move into the named rows' `needs`. Ruled
   items drop the key; their history stays in git and the log. The RESYNC entry does
   the same for adopters, with no transition reader kept (WI-788 risk 9).

## Done-when

- A queued row whose `needs` cites a pending open item is not offered by readiness,
  and is offered once the item is ruled, with a test. The `wi_refs` reader and its
  key are gone, with no second path left.
- The open-items view and the status snapshot show each blocked row beside its
  gating open item, derived from `needs`.
- intake and the disposition prompt write the edge into `needs`.
- `check_trajectory` reports a `needs` OI token that resolves to no open item.
- IF-073, IF-054, IF-176, LLR-058, LLR-288, LLR-289, TC-253, TC-301 and TC-302 are
  amended (or retired where they only describe `wi_refs`) through in-lane
  adjudication. The rule is stated once, in IF-054 and IF-073, and PROCESS.md,
  `docs/work/README.md` and the templates link to it.
- OI-98's and OI-101's `wi_refs` are migrated into WI-684's and WI-788's `needs`.
  The ruled rows' `wi_refs` are removed.
- A RESYNC_PACK entry migrates adopters.
- The commit bar passes.
