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

## Owner rulings, third pass (2026-10-03): the sync rule is an error, and it is specific

> "Related to the change, it should just fail / error instead of warn, but perhaps
> shoudl be more specific: If an open item transitions from to closed (such that it
> no longer appears in open-items.html), the work item must also be modified and it's
> "Done When" and other applicable fields must be updated."

This supersedes the second pass's warn-tier reading. The coordinator's reading:
- **The trigger** is an open item cited in an open row's `needs` leaving `pending`,
  which is the moment it leaves `open-items.html`.
- **The obligation** falls on every open row citing that item. Its Done-when section
  must differ from what it was before the transition. Its `specref` must stop naming
  the open-items registry once none of its cited items is pending.
- **The other fields** (`title`, `buildtier`, `sr_refs`, `safety_class`) are "where
  applicable". The rule cannot tell when a change is owed, so the ruling's recorder
  and the row's reviewer judge them, and the brief says so.
- **Closing the row** (cancelled or restructured) in the same change also satisfies
  the rule, since a terminal row has no criteria to update.
- **In practice:** the commit that rules an open item updates its rows, or the bar
  stays red until they are updated.

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
     The ruling fills it in (design 2), and design 6's sync error enforces that.
6. **Checks.** Two `check_trajectory` findings:
   - a `needs` token that names no open item;
   - a pending open item that no queued work item cites. The owner could never see
     it.

   One sync ERROR, a commit-time block (third pass; mechanism OI-102 Q3). The rule
   reads one diff, a commit against its own parent, and no further history:
   - For every open item whose row goes from `pending` to non-pending in that diff,
     take each work item that is open in the parent tree and cites the item in
     `needs` there.
   - The same diff must update or remove that row's Done-when section (read from the
     raw spec text), or remove or close the row.
   - Otherwise the commit is refused, naming the row and the item.
   - Removing the `needs` token in the same commit does not discharge the obligation,
     because the citing set comes from the parent tree.
   - Where it runs: the pre-commit hook (HEAD against the staged tree), which is where
     a session iteration's commit lands, and the merge slot, which checks each lane
     commit against its first parent (as it already does for `Loop-Session`
     trailers), so a commit made with `--no-verify` is still refused before it reaches
     trunk. It is one function over two trees in both places, not two rules.
   - A first commit has an empty parent tree, so it closes nothing. A shallow clone, a
     lane and a fresh scaffold all have a commit's parent.
   - Separately, a state check needing no diff: an open row whose cited items are all
     non-pending must not keep a `specref` naming the open-items registry.

   Backlog staleness keeps its two existing arms (SR rows and the SpecRef file). A
   `specref` into the open-items registry is clocked per cited item, not per file.
   Otherwise every new open item would warn every placeholder.
7. **Surface the block** (agreed). An open-item edge gates as `blocked` with its
   item named, not as `waiting`:
   - status.md's Blocked list shows the row beside each pending item that holds it;
   - the dashboard's Next-work card names the item;
   - `schedule`'s `waiting:open-item-pending` reason folds into the single blocked
     disposition, which leaves no second state.
8. **Migration.**
   - OI-98's `wi_refs` moves into WI-684's `needs`, and that pending row loses the
     cell. OI-100, OI-101 and OI-102 were ruled on 2026-10-03, so their `wi_refs` stay
     as history. OI-100's build row is WI-791.
   - Ruled rows keep `wi_refs` as history.
   - The RESYNC entry does the same for adopters, with no transition reader kept
     (WI-788 risk 9).

## Amendments from the Sol review (2026-10-03)

Codex Sol (gpt-6.1-sol, high effort, read-only, at `83abd4d2`) reviewed this
proposal and rated it NOT-SOUND as written: the edge reversal is buildable, but
design 6 was under-defined, and designs 3 to 5 missed readers, writers and checks.
Its brief and review are in `docs/reviews/2026-10-03-wi790-proposal/`. The
coordinator checked findings 3 to 7 against the code. The amendments below bind the
build and supersede the design text where they differ. Three decisions are the
owner's, in OI-102.

- **A1 Sync error (design 6).** The mechanism is design 6's commit-time block
  (OI-102 Q3, ruled 2026-10-03). Also binding:
  - Read the Done-when from the raw spec text (`registry.done_when_section` over the
    whole file), never from the Deliverable parse, which clips at `## Context`.
  - An affected open row must keep a non-empty Done-when.
  - Removing a `needs` token does not discharge a ruling's obligation.
  - The script decides only the mechanical condition. Whether the change carries the
    ruling, and whether `title`, `buildtier`, `sr_refs` or `safety_class` must move,
    is the independent reviewer's judgement. No script approves anything (OI-45).
  - The rule reads only a commit and its parent, so it never skips for missing
    history, and it has no second path.
- **A2 Uncited pending items (design 4, design 6).** The uncited-pending finding is
  an unconditional ERROR (not only under `--strict`). It is evaluated before
  `check_trajectory`'s "vacuously clean" return, which today exits before any
  open-item finding when no work items exist. Cards, counts, the status entries and
  the finding come from one queue projection. While any uncited pending item
  exists, `open-items.html` shows an integrity notice naming each one, linked to its
  registry record, and drops the "owner queue is empty" claim (OI-102 Q2).
- **A3 Every `wi_refs` consumer goes (design 3).** The consumers:
  - readiness (`schedule.py` around :315-339);
  - `check_trajectory.open_item_wi_ref_findings`, which is deleted;
  - intake's context join (`intake._pending_oi_lines`, which reads `WI-Refs`), which
    now joins kin rows' `needs` tokens;
  - `gen_open_items`, which derives citing rows from the queue projection.

  Historical `wi_refs` is opaque metadata that the carrier preserves. No consumer of
  readiness, validation, context selection or rendering derives a relationship from
  it.
- **A4 Schema sync (design 3).** `wi_refs` stays in `kitlib/spine.OFFSPINE_KEYS` as
  declared historical metadata. `tests/test_dogfood_sync.py` tells historical keys
  apart from keys a new row authors, so the template can drop the key from its rows
  while this repo's ruled rows keep it. There is no blanket exemption for the
  registry.
- **A5 Every open-item creation path pairs a placeholder (design 5).**
  - The shipped template's pending OI-1 and OI-2 cite only `WI-000`. They become
    inert examples (the `-000` convention) or ship with paired placeholder rows.
  - Bootstrap's OI-3 is created together with its queued placeholder row, and both
    watermarks are raised.
  - The RESYNC entry migrates every pending adopter item, including those with no
    `wi_refs`.
- **A6 Placeholder validity (design 5).**
  - The minimum is: `id` and a valid filename, `title`, `safety_class`, the `needs`
    token, and a resolving `specref`.
  - `_inject_open_item` supplies the registry reference when the successor has no
    real `specref`, because `_draft_row` writes an omitted one as empty.
  - The disposition brief's minimum says so.
  - The reference is row-specific (`docs/requirements/open-items.toml#OI-NNN`). The
    staleness clock and LLR-160's shared-spec overlap read it per item. The build
    confirms that R-E resolves such an anchor.
- **A7 Surfacing (design 7).** A rename of the reason code is not enough:
  - gating ids and titles are filled in from `oi_preds`;
  - blocked records join Next-work;
  - status.md reuses the same records;
  - a row with both kinds of edge keeps its work-item waiting reason as well;
  - a missing open item stays unsatisfied, under the existing dangling-edge ERROR.
- **A8 Definitions (passes and design).**
  - The trigger is the registry state, a row going from `pending` to non-pending. It
    is not page membership: design 4 also drops an item from the page when its sole
    citer leaves `queued`.
  - Every terminal state is exempt from the obligation: done, cancelled, partial and
    restructured. Each keeps its own R-A record and lineage duties.
  - A ruling satisfies readiness, while the sync error can still red the tree. The
    claim checks readiness, not sync. The ruling's commit carries the updates.
- **A9 Spine.**
  - Also amended: IF-264, IF-265, IF-164, LLR-118 and TC-123 ("every pending row"),
    and LLR-153 and TC-147 (intake context and mint).
  - LLR-010 and TC-010 (a green scaffold) are extended.
  - New traced rows cover the sync ERROR and the uncited-pending ERROR. WI-205's
    rows stay advisory and carry only the per-item `specref` clock.
  - Also changed: `kitlib/spine.py`, `spine_carrier.py`, `migrate_carrier.py`,
    `bootstrap.py`, the shipped `ci/check.yml` (if Q3 needs history), both copies of
    the WI exemplar guidance, and the test modules the review lists.

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
- A commit whose diff takes an open item out of `pending` is refused, at the
  pre-commit hook and for every lane commit at the merge slot, unless the same diff
  updates or removes the Done-when of each row that cites the item in the parent tree
  (or removes or closes that row). The refusal names the row and the item. Tests
  cover:
  - a row citing two items, one ruled without its Done-when touched (refused);
  - the same ruling with the Done-when updated in that commit (accepted);
  - the token removed in the ruling commit with the Done-when untouched (refused);
  - a row closed in the ruling commit (accepted);
  - a lane commit made with `--no-verify` that breaks the rule (refused at the merge
    slot);
  - a first commit (nothing to close).
- `check_trajectory` fails when an open row whose cited items are all non-pending
  still names the open-items registry as its `specref`. Backlog staleness clocks a
  registry `specref` per cited item, with a test that an unrelated new item warns no
  placeholder.
- The disposition brief, the open-item template header and the ruling procedure say
  that ruling an item updates the rows citing it in the same commit: their Done-when,
  a real `specref`, and `title`, `buildtier`, `sr_refs` and `safety_class` where they
  change. Even a gate on a person's act gets a confirmation criterion citing the
  item, for example "OI-98 ruled 2026-10-NN: the re-sync was performed" (OI-102 Q1).
- `open-items.html` shows the integrity notice for uncited pending items, with tests
  (OI-102 Q2).
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
- The amendments A1 to A9 are built, with OI-102's rulings (2026-10-03): Q1 is the
  confirmation criterion, Q2 is the integrity notice, and Q3 is design 6's commit-time
  block.
