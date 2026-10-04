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

## Owner rulings, second pass (2026-10-03): placeholder rows and keeping the pair in sync

The coordinator checked what a work item must contain today:
- **Hard requirements:** an `id` matching the filename and valid frontmatter.
- **Needed to schedule:** a `safety_class`; without one the row is "unclassified" and
  never scheduled.
- **Needed to claim:** a resolving `specref`; the claim refuses without one.
- **Done-when:** a missing Done-when only warns at claim (S13, warn-first).

So a row that holds only its open item is legal, and intake already mints rows
nearly that thin. The coordinator proposed a Done-when refusal at claim for rows that
cite an open item. The owner pointed out that it fails when a row cites several open
items, because its Done-when may be only partly written. The owner chose this
instead:

> "I think the easiest way to mechanize it is a check that says if an open item
> becomes closed and has a documented decisison, the work item pointing at it should
> also be modified or removed. That would help encourage keeping the two in sync."

And on the coordinator's finding that today an open-item token in `needs` reads as
"waiting", not "blocked", so it is missing from status.md's Blocked list and the
Next-work card never names the item: "Agreed with surfacing the block."

The coordinator's reading:
- The check is a third cited source in the existing backlog-staleness warning
  (`check_trajectory.backlog_staleness_findings`, WI-205). It already compares an
  open row's last content edit against each cited SR row and its SpecRef file, and
  warns when a source is newer. A content edit to the row clears it. It is warn-tier
  and never joins the exit code, which is the "encourage" the owner asked for.
- It compares each open item separately, so a row citing several items warns for
  each one ruled after the row was last edited.
- "Removed" is covered: a row that goes terminal leaves the check's population, and
  dropping the token is itself an edit.
- It inherits that check's stated limits:
  - The clock is line-granular, so a later edit to a ruled item warns again.
  - A title edit renames the file and does not clear the warning (WI-362).
  - An unrelated edit made after the ruling also clears it.

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
   - **A placeholder may hold nothing but its open item:** a `title`,
     `safety_class`, `needs = ["OI-###"]`, and a `specref` naming the open-items
     registry, which is its spec of record until the ruling. It needs no Done-when.
     The ruling fills it in (design 2), and design 6's sync warning prompts that.
6. **Checks.** Two `check_trajectory` findings:
   - a `needs` token that names no open item;
   - a pending open item that no queued work item cites. The owner could never see
     it.

   One sync warning: backlog staleness gains a third cited source. For each
   `OI-###` in an open row's `needs` whose item is ruled, it warns when the item's
   registry row changed after the row's last content edit: "modify or remove the
   work item". It stays warn-tier, like the rest of that check.
   - A `specref` into the open-items registry is clocked per cited item, not per
     file. Otherwise every new open item would warn every placeholder.
7. **Surface the block** (agreed). An open-item edge gates as `blocked` with its
   item named, not as `waiting`:
   - status.md's Blocked list shows the row beside each pending item that holds it;
   - the dashboard's Next-work card names the item;
   - `schedule`'s `waiting:open-item-pending` reason folds into the single blocked
     disposition, which leaves no second state.
8. **Migration.**
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
- Backlog staleness warns for each ruled open item in an open row's `needs` whose
  registry row changed after the row's last content edit. Tests cover:
  - a row citing two items, one ruled after its last edit (one warning);
  - an edit to the row (cleared);
  - a terminal row (exempt);
  - a placeholder whose `specref` names the open-items registry, which is not warned
    by an unrelated new open item.
- A row held by a pending open item reads as blocked, with the item named, in
  `schedule`, status.md's Blocked list and the Next-work card. No `waiting` state is
  left for open-item edges.
- A placeholder row carrying only a title, `safety_class`, its `needs` token and a
  `specref` to the open-items registry passes every check and is blocked, with a
  test.
- IF-073, IF-074, IF-054, IF-176, LLR-058, LLR-288, LLR-289, TC-253, TC-301 and
  TC-302, plus whatever pins the disposition brief's open-item clause, the
  snapshot's lists and backlog staleness (WI-205's rows), are amended (or retired where they only describe `wi_refs`)
  through in-lane adjudication. The rule is stated once, in IF-054 and IF-073, and
  PROCESS.md, `docs/work/README.md` and the templates link to it.
- Migration as in design 8. The status.md filing note is updated.
- A RESYNC_PACK entry migrates adopters.
- The commit bar passes.
