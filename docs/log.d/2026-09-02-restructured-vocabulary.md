## 2026-09-02 — the restructured terminal state and list-valued supersedes

Steps 1 and 2 of §2.4 of
[the backlog-restructure plan](../plans/2026-09-02-backlog-restructure-and-consolidation.md),
executed as two hand trunk commits rather than as a lane: they touch the very
mechanisms the loop has not yet shown trustworthy (the verdict carrier, the
close, the mint), and the vocabulary has to exist before the restructure that
uses it. Nothing under `docs/work/` or `docs/archive/work/` was moved here —
that is a later step, by someone else.

### Step 1 — `restructured`, the fourth terminal word

**Why a fourth word rather than one of the three.** A consolidation absorbs
several queued rows into one successor. `cancelled` cannot carry that, and the
reason is mechanical rather than aesthetic: `intake.context_block` joins every
CANCELLED row on the same SRs into a "Cancelled precedent on the same SRs (do
not re-propose the refuted)" section of every later worker brief — so an
absorbed row filed as cancelled would brief its own successor against the very
scope it was minted to carry. `partial` cannot carry it either: it means a lane
stopped early, and it owes an immutable per-close report under
`docs/handbacks/` plus a minted disposition, neither of which a consolidation
produces. `restructured` says what happened — the scope text stays
byte-identical, the `## Deliverable` is exactly one line
`Restructured into WI-<successor>.`, and the row's inbound hard edges are
re-pointed to the successor at the close. Terminal means terminal: nothing
re-claims it and no lane closes into it.

**Readers extended.** `kitlib.registry.SPEC_STATUS_DIRS` and
`wi_convert.STATUS_DIRS` (the status↔directory bijection, both directions);
`agent_common.TERMINAL_STATUSES` (a worker refuses the assignment);
`check_trajectory.TERMINAL_STATUSES` (R-A owes the successor line, R-F clears
the SpecRef, and the status is out of `OPEN_STATUSES` and
`BACKLOG_STALE_STATUSES`, so the stale-backlog and shared-spec warnings treat
it as closed) and `_DEAD_PRED_STATES`; `schedule._TERMINAL_DISPOSITION`
(`restructured:absorbed`) and `_waiting_reasons`
(`waiting:hard-pred-restructured:`); `bootstrap.py`'s directory manifest, so an
adopter scaffolds the folder.

**One reader the plan's list missed**, found by grep rather than by the read
the plan rests on: `traj_render.STATUS_BUCKET` / `STATUS_GLYPH`. Every dashboard
surface routes through `traj_views._wi_status`, which falls back to `queued` for
a status the bucket table does not know — so without this the dashboard would
have labelled an absorbed row *queued*, silently and in the one place a human
looks. It now shares `cancelled`'s swatch (both mean "this row will not
advance") and takes its own glyph, `⇥`, because what they mean differs.

**Deliberately NOT extended, each with the reason written down beside the
constant** — a negative that no check can enforce is worth stating where the
next author will read it: `kitlib.station.CLAIMED_OUTCOMES` and
`integrate.Outcome` (a lane that could close into it would be asserting that
another row's scope had been absorbed, a judgement it is structurally not
holding); `intake._closed_spec`'s directory sets and `SWEEP_OUTCOMES` (a
restructure is not a close and mints no disposition); and `context_block`'s
cancelled join, which is the whole reason the word exists. `next_wi_id` already
rglobs both roots, so an absorbed row's id can never be re-issued — verified,
not assumed. `spec_move.py` needed no change at all: it names no status and
creates the destination's parent, which is what a declared-status-word
vocabulary is supposed to cost.

**Checked and found to say nothing:** `docs/registry-machinery-reference.md`
scopes itself out of the work-item registry in its own §Scope, and
`docs/enforcement-audit.md` has no sentence listing the terminal states. Neither
needed an edit. `docs/work/README.md` and its shipped twin
`project-trajectory/work/README.template.md` did, and so did the WI-000 exemplar
in both copies; `project-trajectory/RESYNC_PACK.md` gains an entry (additive —
an adopter gains a folder and nothing they hold changes meaning).

### Step 2 — `supersedes` accepts a list

A consolidation's successor continues SEVERAL rows, and `supersedes` was
single-valued end to end. It now accepts EITHER a bare id string (unchanged in
every respect — the same cell, the same bytes in the spec file) or a TOML list.
`intake.supersedes_ids` is the one reader of both spellings; the registry cell
is `;`-joined; `_apply_supersede` passes the whole set to
`_replace_inbound_edges`, which re-points every dependent in ONE pass rather
than one pass per absorbed id — a dependent that hard-needed two absorbed rows
would otherwise be rewritten twice, with the second write reading its own first
one. The successor enters a `needs` list at most once however many of its
predecessors a dependent named.

The tolerance is on the FRONTMATTER, not on the column: `Supersedes` stays a
scalar cell (`kitlib.registry.LIST_TOLERANT_SCALARS` is the one-key exception
both the loader and the converter read through), because widening the cell would
have re-typed a column and every reader of it for a shape most rows never carry,
and would have made `wi_convert` re-emit every existing one-id row as a
one-element list — changing bytes for nothing.

**Two refusals, and where each can live.** `_supersedes_refusal` has a shape arm
(a token that is not a `WI-###` id matches no dependent's `needs`, so the
re-point is a silent no-op and the lineage cell is a typo nobody reads) and a
liveness arm (an id that is no live row — for a consolidation that means the
verdict named a row that does not exist, leaving one of the rows it meant to
absorb queued beside its own successor). `_draft_refusal` can only run the
shape arm: it validates a hand-authored `## Dispositions` block before any
registry is loaded. Liveness runs at `_mint_shape_refusal`, which is the rung
that holds the pre-mint registry. One existing fixture
(`test_the_oi_mint_refuses_on_a_non_toml_registry`) had a `supersedes` naming a
row it never wrote; the new rung pre-empted the refusal that test is about, so
the fixture now writes the row — the fixture was unrealistic, not the rung.

`adjudicate-disposition.template.md`'s one sentence now says a string or a list
is accepted. No other prose in that template changed.

### Bar and ratchets

Every ratchet movement is a reviewed bump, reason stamped in the baseline entry
as well as here: `bootstrap.py` 1657 → 1658 (one manifest row),
`check_trajectory.py` 2273 → 2275 (the `_TERMINAL_DELIVERABLE_REASON` table
replacing a two-armed conditional, plus a line on the dead-edge message),
`intake.py` 1249 → 1286 (the shared parse and the two-armed refusal), and the
smoke membership ceiling 1467 → 1480 against a measured 1473. The seconds budget
was not touched and was not close: 21 s against 60.

Guards added: 13. Three in `test_wi_folder_loaders` (a restructured spec loads
as itself from both roots and reads R-A clean; the empty-Deliverable mutation
twin; a live hard edge onto an absorbed row is reported, with the re-pointed
control), two in `test_schedule`, six in `test_intake` (the cancelled-precedent
join drops the SAME row when it is re-filed as restructured; no disposition is
minted and the id stays taken; three absorbed rows with two dependents each
re-point exactly once, including the dependent that named two of them; the
string form is byte-identical to a one-element list; both refusal arms; the
frontmatter list reads back as the joined cell through both readers), one in
`test_integrate_admission` (a trunk-side restructured row is inert for an
unrelated lane's outcome read, and a lane that closes into the folder names
nothing and the merge refuses), one in `test_spec_move` (queued → the archive
folder through the real ritual, links following both ways).
