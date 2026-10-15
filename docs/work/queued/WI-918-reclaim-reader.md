+++
id = "WI-918"
title = "An unmarked re-claim commit closes a loop lane's trailer window, so the merge slot reads the attended commits after it as a person's"
workstream = "process"
sr_refs = ["SR-209"]
specref = "docs/plans/2026-10-11-review-churn/README.md#owner-rulings-2026-10-11"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["WI-917"]
+++

## Context

Filed on trunk on 2026-10-14 by the attended coordinator. It was split from
P9 (WI-917) by the owner's ruling (2026-10-14, in session). The spec of
record is the plan's revision 36 ruling "Headless coordinator legs are marked
now": a lane claimed headless lands headless, or the attended coordinator
re-claims it before committing in it, and "how a re-claim clears the loop
mark" is P9's design. WI-917 states the rule and has the attended coordinator
write the re-claim commit by recipe from its landing. Nothing reads that
commit until this row. Where this row and a ruling differ, the ruling
governs.

**How the slot reads a lane today.** The merge slot reads whose lane it is
off the lane's commits (`integrate._loop_window`, through
`provenance.loop_lane_window`). A lane is the loop's:

- from its claim, when the claim commit on trunk carries the trailer
  (`integrate._loop_claimed` reads the newest claim commit for the branch);
- or from the first marked commit one of the loop's own writers made in its
  range.

Every commit of a loop lane must then carry a well-formed trailer. SR-209
gives a person's commit there only two ways out: "carry the trailer or move
to the person's own lane".

**Why the re-claim must sit in the lane.** A headless leg marks a lane at
every sitting: the entry point's `commit_telemetry` commits carry the
loop-writer subject `telemetry: session`, and P2 adds one per Sol or Terra
call. So a newer unmarked claim commit on trunk, which `_loop_claimed` would
read, clears a claim's mark but never a sitting's. The re-claim has to be a
record in the lane's own range, ordered with the lane's commits, an order a
rebase keeps.

**Why this lands before WI-808.** The slot's trailer rung first reaches a
coordinator lane when WI-808 moves coordinator landings onto the slot. Until
then, coordinator landings are hand squashes, which never run it. The
coordinator adds this row to WI-808's `needs` at filing.

## Deliverables

One lane, one landing. Each item names its ruling, and the builder writes the
rule in the target's own voice.

1. **The re-claim, composed once and read once**
   (`project-trajectory/scripts/kitlib/provenance.py`; shipped, so a RESYNC
   entry):
   - **The composer, `reclaim_subject(branch)`.** It returns `reclaim:
     <branch> (attended)`, byte for byte the subject WI-917's recipe writes.
     The subject carries no claim suffix, so no claim reader sees it, and it
     shares no pattern with `LOOP_WRITER_SUBJECTS`.
   - **The reader, `loop_lane_window`.** It walks the lane's commits oldest
     first:
     - the window opens at a loop claim or a marked loop-writer commit, as
       today;
     - a re-claim closes it: an empty commit (exactly one parent, and a tree
       equal to that parent's), with this branch's exact subject and no
       `Loop-Session` trailer at all. A commit that fails any of the four is
       not a re-claim and is judged like any other commit in the window, so a
       non-empty commit under the subject without the trailer is refused,
       naming it;
     - the trailer rule judges only commits inside an open window;
     - a lane with no loop mark stays a person's (`None`);
     - a lane ever marked returns a list, possibly empty, so
       `_held_status_refusal`'s `None` test reads as today.
   - **The module's narrative and IF-194's contract text** name both, and
     state the one exception to "a forged loop-writer subject only makes a
     lane MORE governed".
2. **`project-trajectory/scripts/integrate.py`'s docstrings** follow
   (`_loop_window`, `_loop_trailer_refusal`, `_held_status_refusal`). Its
   code changes only if `_loop_window` must hand the reader what the
   emptiness check reads (each commit's parents and tree), and no further.
3. **The `coordinator-cycle` skill's re-claim step** (kit source
   `project-trajectory/skills/coordinator-cycle/`, synced to
   `.claude/skills/`; `scope: this-repo`, so no RESYNC entry). The step
   composes the subject through `provenance.reclaim_subject`, now the
   subject's one home, in place of the literal WI-917's recipe carries. Its
   "until WI-918 lands, nothing reads it" sentence becomes the reader's
   rule.

## Trust

Written before the claim, answering S2 under `project-trajectory/PROCESS.md`
§3, "When a guard is owed". The ruling goes to the owner to confirm or
overrule (coordinator-cycle §1 and §5).

**The carrier.** A re-claim commit in a lane: an unmarked commit whose subject
is `provenance.reclaim_subject(<the lane's branch>)`, which carries no
`Loop-Session` trailer, and which is empty: exactly one parent, and a tree
equal to that parent's. The merge slot reads it through
`provenance.loop_lane_window`, the one reader. It closes the trailer rung's
window for the commits after it, which no record can do today ("a person's
commit inside a loop lane is refused too", `integrate._loop_trailer_refusal`).
It is the first record that makes a lane less governed. Today a forged
loop-writer subject "only makes a lane MORE governed" (the module's own rule).

**Producer and write route.**

- **Producer:** the attended, unmarked coordinator, as its first commit in a
  lane a headless leg marked. It makes the commit with
  `git commit --allow-empty` and that subject (the skill's recipe), with
  nothing else in it. Before this row, the recipe writes the subject as a
  literal; after it, through the composer. The reader holds the record to
  that shape (below), so a commit that is not empty earns nothing.
- **Failed writes:** if the hooks refuse the commit, or it is never made,
  there is no re-claim. The window stays open, and the slot refuses the
  attended commits after it, naming the first.
- **Under the marker:** the floor refuses a porcelain commit without the
  trailer, and a commit with the trailer is not a re-claim. So a marked
  process cannot close its own window through porcelain.
- **Forgery:** a plumbing or `--no-verify` forgery is outside the review
  threat model and outside the procedure (the Never list). It would exempt
  later commits from the trailer rung alone.

**What the authority binds to.** Three things only:

- the re-claim's own shape, validated against its commit's parent at every
  read: one parent and an unchanged tree (a record written at the event and
  checked against its parent, ruling 2 and the scope rubric's B3);
- the re-claim's place in the lane's own range as the slot reads it
  (trunk..branch, oldest first; a rebase keeps the lane's order);
- the trailer rung.

The commits before the re-claim stay judged. A marked loop-writer commit
after it re-opens the window, and no other rung reads it. A re-claim written
under WI-917's recipe before this row landed is read exactly as one written
after.

**Consumers and rulings** (grep over `project-trajectory/scripts` for
`loop_lane_window`, `_loop_window` and the re-claim subject):

- **The trailer rung**, `integrate._loop_trailer_refusal` via `_loop_window`.
  It judges the commits inside an open window. A re-claim that is absent or
  misspelled, names another branch, carries any `Loop-Session` trailer
  (well-formed or malformed), or is not empty (a merge, or a tree that
  differs from its parent's) is not a re-claim. The window then stays as it
  was, and that commit and any later commit without a trailer are refused,
  naming the first. A range
  git cannot read is refused, as today.
- **The held-status rung**, `integrate._held_status_refusal` via
  `_loop_window` (unchanged). A lane with any loop mark is judged whole,
  re-claimed or not. WI-851 replaces this rung with a state rule that judges
  every lane alike, and WI-808 needs WI-851.
- **Not consumers, checked:**
  - `agent_common.claim_base`, `integrate._loop_claimed` and
    `integrate._abandoned_claim` read the claim grammar, which the re-claim
    subject does not carry.
  - `provenance.loop_writer_commit` reads a disjoint grammar.
  - `check_trajectory.loop_held_status_findings` reads each commit's
    trailer. A re-claim carries none and moves nothing.

## Done-when

- Every deliverable above is in its target, each citing the ruling it
  carries.
- **Tests** (`tests/test_loop_provenance.py`). Each fails on the code before
  the change:
  - a lane claimed under the marker, re-claimed, then committed in without a
    trailer passes the trailer rung, and the same commit placed before the
    re-claim is refused;
  - a lane claimed attended and then marked by a sitting's telemetry commit
    is judged from that commit, and a re-claim after it clears it;
  - a re-claim carrying a `Loop-Session` trailer (well-formed or malformed),
    or another branch's subject, is not one;
  - a commit with the exact subject and no trailer that changes the tree,
    or that has two parents, does not close the window and is itself refused
    by the trailer rung, naming it;
  - a marked loop-writer commit after a re-claim re-opens the window;
  - a lane never marked stays a person's, and the held-status rung judges a
    re-claimed lane whole;
  - a re-claim whose subject was written literally by WI-917's recipe,
    before this row landed, is read the same way as one composed by
    `reclaim_subject`.
- The change's trace rows are authored and sat at the lane's checkpoint:
  SR-209's acceptance, LLR-248, TC-242 and IF-194 are amended, and the act is
  taken through WI-912's act turn.
- `RESYNC_PACK.md` carries one entry for `kitlib/provenance.py`, with no
  forced migration: no adopter lane carries a re-claim, so every window reads
  as before.
- The skill copy in `.claude/skills/` matches the kit source
  (`bootstrap.py --dest . --sync`).
- The lane's plan is produced after the claim and passes the plan gate (S4).
- The bar is green on the landing tip:
  - the smoke tier within its budget;
  - `check_trajectory.py --strict` clean;
  - `trace.py --strict` with no finding beyond LLR-292's (WI-914 fixes that
    one).

## Scope answers

- **S1:** one landable unit. The composer and the reader are one
  construction; the recipe edit makes the composer the subject's one home
  and rides with it; and the docstrings and spine amendments describe it.
  It was split from WI-917 by the owner (2026-10-14), and WI-917 lands
  first.
- **S2:** yes. The re-claim commit gains authority over the merge slot's
  trailer rung; see `## Trust`.
- **S3:** closed by construction, with deny by default.
  - **The window:** each lane commit is exactly one of three things: a
    re-claim (one parent, an unchanged tree, the exact subject, no
    trailer), a marked loop-writer commit, or neither. The window's state
    changes only at the first two. A subject or trailer outside those two
    forms is neither.
  - **Records written before this row:** WI-917's recipe writes the same
    literal subject, so every such record is read the same (a Done-when
    test).
  - **Lanes in flight:** a lane holding a re-claim written under WI-917's
    recipe is read with it from this landing; a lane without one reads as
    today; and no adopter lane carries one.
- **S4:** `single`, for three reasons:
  - the row has a Trust section;
  - it touches two script families (`kitlib/provenance.py`, and the merge
    slot's `integrate.py`);
  - it changes an interface seam (IF-194).
- **Architectural delta:** yes, carried within scope by SR-209's, LLR-248's,
  TC-242's and IF-194's amendments. No preparatory refactor is needed, and
  no boundary is crossed.
  - **A new state:** a lane can go from a loop window back to a person
    window.
  - **A new domain value:** the re-claim subject, in the grammar the window
    reads.
  - **A new input:** the slot's trailer window depends on re-claim commits.
- **B3 and B4:**
  - **B3:** the slot reads the re-claim from the commit written at the event,
    in the lane's own range, and validates its shape against that commit's
    parent (one parent, an unchanged tree) at every read. It never re-derives a lane's mode from the
    environment, the lease or dates.
  - **B4:** no Done-when item needs an owner act or credential. SR-209 sits
    on a rung this repo's dial releases, so its amendment act is the
    adjudicator's.
- **Dependencies:**
  - **`needs` WI-917, hard.** This row amends the skill section WI-917 adds,
    and reads the subject WI-917's recipe writes. WI-912's act turn, which
    takes this row's act, lands before WI-917 by that row's hard edge.
  - **Before WI-808:** the coordinator adds WI-918 to WI-808's `needs` at
    filing. WI-808's slot is where this reader first binds a coordinator
    lane.
  - **A mechanism change:** this row lands alone. Its reader first runs at a
    slot landing of a lane holding a re-claim. Whether the next mechanism
    lane waits for that is the coordinator's call at the landing, recorded
    as a decision.
  - **Later rows, not edges:** WI-851 replaces the held-status rung's
    loop-lane reading with a state rule for every lane.
  - **No third-party dependency.**
- **Design call Q3, how a re-claim clears the loop mark** (recorded at
  filing as `docs/decisions/coordinator-2026-10-14.toml` D-017): an
  unmarked, empty, subject-typed commit in the lane, read by the window.
  - A trunk-side second claim commit was rejected: it cannot clear a
    sitting's mark.
  - Removing authority instead of adding it would mean dropping SR-209's
    loop-lane rule for the managed loop too.
  - So the new authority is held to its narrowest form: one rung, only the
    commits after it, and a marked process cannot make one through
    porcelain.
  - The ruling on it goes to the owner with the Trust section.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-14; CHANGES-REQUESTED, one finding):

- **S2/S3/B3, MAJOR: adopted.** The reader accepted any commit with the
  exact subject and no trailer, so a non-empty commit could close the window.
  The re-claim is now validated against its commit's parent at every read:
  deliverable 1's reader takes "an empty commit (exactly one parent, and a
  tree equal to that parent's)", and "A commit that fails any of the four is
  not a re-claim and is judged like any other commit in the window"; the
  Trust section binds the authority to "the re-claim's own shape, validated
  against its commit's parent at every read", and the trailer rung's ruling
  refuses such a commit, "naming the first"; the Done-when adds "a commit
  with the exact subject and no trailer that changes the tree, or that has
  two parents, does not close the window and is itself refused by the
  trailer rung, naming it". The owning check is the one reader,
  `provenance.loop_lane_window`.
