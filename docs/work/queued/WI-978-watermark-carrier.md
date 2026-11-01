+++
id = "WI-978"
title = "One mint across parallel lanes: a watermark carrier every lane reserves its spine ids from, a landing that admits only reserved ids, and the keep-or-mint rule"
workstream = "process"
sr_refs = ["SR-174"]
specref = "docs/plans/2026-10-11-review-churn/README.md#16-one-mint-across-parallel-lanes"
needs = ["~WI-977", "OI-116"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Context

Filed from the review-churn plan's item 16, the queue's row P5
(`docs/handoff-2026-10-11-attended-coordinator.md`): "the watermark carrier,
for spine ids only (revision 33: act seqs and WI ids stay as they are), and
the keep-or-mint rule in PROCESS.md §4, after P4". Item 16's content is
revisions 26 (the carrier, keep-or-mint), 29 and 31 (verdicts move between
lanes, acts keep landing order), and 33 (spine ids only). Rulings 1, 3, 4,
5 and 9 shape this spec. coordinator-2026-10-20 D-009 adds two things: WI-810's
"sequential sittings never collide on an id" folds in here (below), and this
spec asks the owner whether the WI space rides the carrier too (OI-116,
`## Ruled by the owner`). The owner ruled it 2026-11-01: no, revision 33
stands. This spec is written for that answer.

**Anchor.** SR-174 (Approved, under SN-025): "allocate each work-item
identity at most once, so that no two concurrent actors receive the same
identity and an identity freed by a deletion is never re-issued". TC-158
already verifies the spine-space watermark rules under SR-174, with IF-101.
No SR states spine-id allocation separately. Keep-or-mint (revision 26, with
revision 31's cross-reference) is applied to SR-174 itself, and the answer
is **keep, widened**. The row's spirit (one allocation per identity, counted
from the high-water mark, never re-issued) is unchanged. Its users (LLR-153,
LLR-154, TC-147, TC-148, TC-158, the SR-170 and SR-173 rationales, and the
`Implements:` tags in the intake and integrator scripts) each read the
work-item half, and that half still holds. Minting a new SR would re-point
TC-158. SR-174's `sn_refs` gain SN-027 (Approved, parallel lanes), and no
SN changes.

**What is true today (read on trunk at `aed0364fd`).**

- `docs/id-watermark` has one `SPACE = N` line per space in
  `trace.WATERMARK_SPACES`: 20 spaces, keyed off `ID_PATTERNS` plus SN, WI,
  OI, DP, B, EXT, REL, STK, DA, SUR. Its header carries the `# correction:`
  records (`_CORRECTION_LINE`, today `B 7 -> 8` and `REL 3 -> 4`, OI-47) and
  a `# basis:` line.
- `trace.py --bump-ids` (`bump_watermark`) raises every mark to the live
  maximum and takes no count. `render_watermark` rewrites the whole file,
  carrying back only the correction lines and the basis, so **a new header
  line kind would be dropped by the next bump**. `--correct-mark`
  (`correct_watermark`) is the one-shot ruled raise.
- `_mark_history_findings` (rules 3 and 4, at every commit through the
  pre-commit `--strict-integrity` floor) refuses a fall, and refuses a rise
  above `max(committed mark, live max)` unless exactly one correction record
  matches the raise. `committed_watermark` and `committed_corrections` read
  HEAD and every other parent, MERGE_HEAD included.
- The spine tiers have no minter. An author writes the next number and runs
  `--bump-ids`. A lane mints at its own base, so parallel lanes draw the
  same numbers. This holds today only by procedure: recipes §4, "Brief each
  lane's Terra with every open lane's ids as a floor, or renumber in the
  later lane". Its rebase row resolves `docs/id-watermark` by taking
  `--ours` and then running `--bump-ids`. That drops a lane's higher mark
  for an id the lane retired, unless the coordinator remembers to keep it.
- The station refresh (`integrate._merge_trunk_in`) refuses any conflict on
  `docs/id-watermark`. The path is deliberately not `[generated]`
  (`integrate.BOOKKEEPING_PREFIXES`' comment). The `# basis:` line changes
  on every bump, so two sides that both bumped always conflict there.
- The WI, OI and DP spaces are minted on trunk: `intake.next_wi_id` and the
  OI mint, and `plan_artifacts` for DP and WI. R1
  (`integrate._minted_id_refusal`) refuses a work branch that adds a spec.
  Its docstring records that a reservation table was the rejected
  alternative for WI ids.
- These stay unchanged. `baseline_snapshot._record_act` numbers an act one
  above the ledger it reads, and acts keep landing order (revisions 31 and
  33). The act ledger, its readers and the latch on acts (`coordinator-cycle`
  §4) do not change.

**Deliverables and landing order (S1).** There are four.

1. **The carrier and its reservation verb.** This covers the carrier ref,
   the reservation record, the fold, and the hand-raise rule re-founded on
   the record.
2. **The landing check.** The landing admits only the ids its own work item
   reserved. It folds the carrier in, and the refresh resolves a watermark
   conflict by the same fold.
3. **The keep-or-mint text.** It goes in PROCESS.md §4, beside the CLARITY
   and MEANING paragraph, and is cited from `spine-questions.md` §0.
4. **The coordinator text** that the carrier replaces. This is the floor
   briefing and the rebase row in recipes §4, plus the "and the id watermark
   pull up" clause of SKILL §4.

Deliverables 1, 2 and 4 are one row. Deliverable 1 alone is a record nothing
enforces, the plan's "authoritative" (step 3) needs both, and deliverable 4
describes their procedure. Deliverable 3 could land alone. It is kept here
because the queue row and revision 26 put it in item 16, and because this
row's own sitting applies it (SR-174's keep). Its cost is one PROCESS.md
paragraph, so splitting it would add a WI's overhead to contain almost
nothing. In the lane, the spine set lands first (TC first), then 1, then 2.
Deliverables 3 and 4 may go in any commit.

**Sequential sittings never collide on an id (folded from WI-810, D-009).**
This was WI-788's in-lane mint invariant ("each sits only after the last
has landed"). Revision 31 lets verdicts be sat for any lane at any time, so
the invariant is re-founded on the carrier. Any two reservations taken one
after another receive disjoint ranges, whether they are in one lane or two,
and whatever each lane's base. That covers a second drafting step, and an
id a sitting's keep-or-mint ruling turns into a mint. This holds by
construction: each reservation starts one above the carrier's mark, and
moves the carrier by compare-and-swap. A WI id a sitting rules (a
SUCCESSOR) is still filed on trunk at the landing, unchanged.

**Coverage (S3).** Each promise below is an enumerated allow-set with a
declared rule for everything else. The bound (PROCESS.md §6 "Review threat
model") is as follows. The carrier is shared by the worktrees of one
repository, and a separate clone is outside the promise. A hand edit of the
carrier ref, of a reservation line or of `docs/id-watermark` is outside the
promise. Two reservations racing from two worktrees are **inside**, and the
compare-and-swap covers them.

*The carrier spaces:* every watermark space except WI, OI and DP, read from
the one space list. A space added to that list later joins the carrier by
default, so it is deny-by-default. WI, OI and DP keep their trunk writers.
Number 0 (the `-000` placeholder convention) is never an allocation and is
never judged.

*The reserve verb* (`trace.py --reserve-ids WI-NNN SPACE=N[,SPACE=N...]`;
the plan names the final spelling):

| Argument | Admits | Refuses |
|---|---|---|
| work item | one well-formed id whose spec the trunk claim holds | empty, a list, malformed, not claimed |
| counts | one or more `SPACE=N`, SPACE a carrier space, N an integer 1 to 50, each space once | WI, OI or DP (the refusal says these are minted on trunk), an unknown space, N not an integer, below 1 or above 50, a repeated space, no pair |

Everything else is refused before any write: the carrier is unmoved, the
working file is unchanged, the verb exits 1 with one line, and argparse
usage errors exit 2. On success it writes one carrier commit. Then it folds
the carrier into the working tree's `docs/id-watermark` and leaves that
change for the caller to commit, as `retire.py` does.

*The record line:* `# reservation: <SPACE> <low>-<high> (<WI-NNN>)`, matched
whole on the stripped line, with `low <= high`, SPACE a carrier space, and
`low` one above the carrier's mark when written. A line that does not match
is not a record. It justifies nothing, so the raise it would have justified
is refused, and a landing carrying it is refused under rule 2 below. It gets
no report of its own.

*The fold:* its inputs are the receiving file (clean, or conflicted, in
which case index stages 2 and 3 are read) and the carrier tip (when there is
none, only the working sides are folded). Its output is, for each space, the
maximum mark; the union of reservation and correction records, sorted by
space and then low; and the basis line recomputed from the receiving tree's
live ids.

*The landing check* is one function with two callers: the merge slot's
landing rungs (beside R1) and the pre-commit judgement of a
`git merge --squash` in progress (beside `held-status`, through
`kitlib.git.squash_commits`). Its inputs are the landing tree, its first
parent, the landing's work item read from the lane's claim, and the carrier
tip.

| Landing state | Ruling |
|---|---|
| no carrier-space id added | passes; nothing reserved is needed (code-only lanes) |
| every added id inside a carrier record naming the landing's work item | passes |
| an added id outside every record naming that work item (no record, another work item's record, or a retired number re-used) | refused, naming each id, the work item and the reserve verb |
| ids added and no carrier ref | refused the same way (the verb creates the carrier) |
| ids added and the work item unreadable from the claim | refused, naming the claim read |
| the landing's watermark carries a record that neither the carrier nor the parent holds | refused, naming the line |

"Added" means live in the landing tree and not live in the parent, under the
watermark's own live-id sweep (one definition of "live"). An id the landing
removes is `retire.py`'s concern, not this check's. A plain trunk commit
that is not a landing is not judged. That is the existing residual
(`held-status`'s "unmarked plain trunk commit"), and in this repository
trunk adds no spine row outside a landing (`BOOKKEEPING_PREFIXES`).

**Planning (S4).** `single`. The row has a `## Trust` section, touches
several script families (the tracer, the integrator's refresh and landing,
the pre-commit step) and promises behaviour over the input spaces above.

**Architectural delta (S5).** It adds new state and a new branch. The
carrier is `refs/heads/id-carrier`, a kit constant. It is an orphan history
whose every commit's tree is one file, `docs/id-watermark`, written by
plumbing (`hash-object`, `mktree`, `commit-tree`, then `update-ref <ref>
<new> <old>`). That is the `archive/lanes` recipe's precedent: no worktree
and no checkout, and its lock is git's own ref lock, never the station lock.
The record is a new line kind in an existing file. The landing gains a new
input, the carrier tip. A new value enters a domain: a space is either a
carrier space or a trunk space. The carrier merges with a landing by content
(the fold), never as a git parent, so `committed_watermark` never reads it.
The new code lives in one new stdlib module that owns the record grammar,
the carrier read/write and the fold. `trace.py` composes it the way it
composes `retire.py`, and is ratcheted at 3741 SLOC. Moving trace.py's
existing watermark section into that module is a refactor row of its own,
filed on trunk if wanted, and not folded in here.

**Dependencies (S6).** `~WI-977` (soft): after it every lane claims one
work item, which is what the landing check keys on. A multi-item claim
would only widen the records read to the claimed set's union, not change
the rule. `OI-116` (hard): the owner's WI-space question, which the
contract of `docs/requirements/open-items.toml` requires a queued row to
cite. This row changes the landing the coordinator runs on, so it lands
alone (revision 37). No new package; git is already the kit's.

**The spine** (one checkpoint sitting, TC first; target meaning only). No
cell names a code file, function or symbol (ruling 5). The LLR and TC rows
may name the watermark, which is a shipped boundary artifact.

- **SR-174** (amended, kept): the delivered content allocates each identity
  it mints at most once. Work items are minted on the integration branch
  alone. The registry identities that parallel lanes author are drawn from
  one shared reservation record. No two concurrent actors receive the same
  identity, and an identity freed by a deletion is never re-issued.
  Acceptance: two lanes reserving in sequence or at once, from any bases,
  receive disjoint ranges; a landing that adds a registry identity outside
  its own work item's reservation is refused before it lands; a mark rises
  only by allocation, by a ruled correction, or by a recorded reservation;
  plus the current three clauses. `sn_refs` gain SN-027.
- **LLR (new): the carrier and its reservation record.** The carrier holds
  the id watermark for the lane-minted spaces. A reservation moves it in one
  compare-and-swap and appends one record per space (space, inclusive range,
  work item). Only the reservation writes a record, and only the fold copies
  one. Committed records are append-only across every parent. Every writer
  of the watermark carries the records verbatim.
- **LLR (new): the landing admits only reserved identities.** This is the
  table above, with the fold at landing and at a refresh conflict.
- **TC-158** (amended): the rules gain a raise justified by a record, a
  raise above every record refused, a committed record altered or deleted
  refused, and a bump that keeps the records.
- **TC (new)** for each new LLR: sequential and concurrent reservations are
  disjoint (the folded sittings rule); a stale-base lane's mint of another
  lane's number is refused; each refusal in the two tables is driven; a
  refresh conflict is resolved by the fold.
- **IF-101** (Drafted, so no sitting is owed): the seam gains the reserve
  and fold calls, the record grammar and the carrier ref, and the landing
  joins its requestors.

This row's own new ids (two LLRs, two TCs) are minted before the carrier
exists, under today's floor briefing. They are then reserved through the
built verb before the landing (its first use creates the carrier from
trunk's watermark), so this row's own landing passes its own check.

## Trust

The reservation record gains authority over two things: the hand-raise rule
(a mark may stand above the live maximum because a record covers it) and the
landing (an added id lands only inside its own work item's record).

**Producer and write route.** The reserve verb is the only writer of a
record, and it writes only on the carrier. It reads the carrier tip (or, on
first use, the trunk's committed watermark), computes the new marks and
records, writes one commit, and moves the ref by compare-and-swap. Each
range starts one above the larger of the carrier's mark and trunk's
committed mark for its space, so a ruled `--correct-mark` on trunk raises
the next reservation's floor, and the correction's record is kept. The fold
is the only copier, into a working file. No model writes a record. A model
or a person runs the verb.

**Failed-write shapes.**

- Before the ref moves (a refusal, a crash, or a lost compare-and-swap): no
  reservation exists. Loose objects are inert. A lost compare-and-swap
  refuses ("another reservation moved the carrier; re-run") and writes
  nothing.
- After the ref moves, before the fold: the carrier holds the reservation
  and the lane's file does not. Re-running the fold copies it. Until then
  the lane's own commits pass, because live ids justify the lane's mark,
  and the landing reads the carrier, not the lane's copy.

**Consumers** (found by grepping `id-watermark`, `watermark` and the reader
names across `project-trajectory/scripts` and `tests`). Each ruling covers
every state a supported route produces: no records (every repository
today), records written or folded by the kit, a conflicted file mid-merge,
no carrier, and a moved carrier.

| Consumer (path) | Reads | Ruling |
|---|---|---|
| `scripts/trace.py` `_mark_history_findings` (every commit, `--strict-integrity`; `--strict`) | marks, live, committed marks, records | a rise is justified up to the highest number a well-formed record in the commit's own file names for that space; a fall is refused regardless; no records means today's rule |
| `scripts/trace.py`, a new committed-record check beside `committed_corrections` | every parent's records | each record a parent carries is present unchanged; it is a union across parents (not longest-wins), so a merge cannot drop a side's records |
| `scripts/trace.py` `read_watermark`, `_watermark_at`, `committed_watermark` | mark lines | unchanged: comment lines are skipped, and the carrier is never a parent |
| `scripts/trace.py` `parse_corrections`, `_correction_record_findings` | `# correction:` lines | unchanged: a reservation line never reads as a correction (pinned by a test) |
| `scripts/trace.py` `bump_watermark`, `render_watermark`, `correct_watermark` | the whole file | they carry every record verbatim and in order; today they would drop them |
| `scripts/intake.py` `next_wi_id`, the OI mint and its bump; `scripts/plan_artifacts.py` (DP, WI) | WI, OI and DP marks | unchanged: trunk spaces only, and their bump carries the records |
| `scripts/retire.py` `read_marks`, `spent_unrecorded` | marks | unchanged: a reserved number never minted reads as spent with no record, an advisory outside every exit code, as a floored id reads today |
| `scripts/integrate.py` `_merge_trunk_in` (refresh) | conflicted paths | a conflict on `docs/id-watermark` is resolved by the fold (a deterministic result, not a content question); any other conflict still refuses, and the hand-raise rule judges the refresh commit as any commit |
| `scripts/integrate.py` landing rungs; `scripts/check.py` squash judgement | landing tree, parent, claim, carrier | the landing check's table (S3) |
| `scripts/integrate.py` `BOOKKEEPING_PREFIXES`; `scripts/handback.py` `BOOKKEEPING_FILES` | the path | unchanged: the carrier lives outside the tree |
| `scripts/bootstrap.py` `raise_watermark`; `kitlib/bootstrap_manifest.py` | scaffold marks | unchanged: a fresh scaffold has no records and no carrier |
| coordinator recipes §4 and SKILL §4 (procedure) | the rebase row, the floor briefing | replaced (Done-when, text) |

## Ruled by the owner (OI-116)

**Ruled 2026-11-01: No (option (a), spine only).** Revision 33 stands and
this spec stands as filed; the owner saw no reason for a lane to open a
work item. The question and its options are kept below as the record.

Does the WI space ride the carrier too? A yes would re-open revision 33,
so that lanes reserve WI ids instead of trunk minting them (D-009 asks it).

- **No (revision 33 stands; what this spec is written for).** WI, OI and
  DP keep their trunk writers. Successors are filed on trunk at the
  landing, and R1 stays.
- **Yes.** WI joins the carrier spaces, and the reserve verb admits it.
  Every WI mint then reserves from the carrier: `intake`'s trunk mint, the
  sweep, `plan_artifacts` and hand filing. Otherwise trunk and the lanes
  are two writers of one space. R1 becomes "a branch adds only the WI ids
  its work item reserved", and the landing check covers WI. SR-174's "on
  the integration branch alone" and LLR-153's "lanes never mint" are
  amended. This revives part of WI-810's in-lane mint, which D-009
  cancelled. The Done-when's carrier, landing and RESYNC items would have
  changed.
- The open item's third option, defer, builds this spec as for No and
  files a yes as its own row later.

**Recommendation: No.** The WI space already has one writer, the trunk under
the coordinator's lease, so it has no collision to remove. The collisions
on record are spine ids and act seqs (the 2026-10-08 D-002 repair). The 54
re-mints that WI-963 targets are settled amendments, not collisions. A yes
moves every trunk mint onto the carrier and re-opens a cancellation the
owner made five days ago. The one thing it buys is a lane citing a
successor by id before landing, and today that is "cite it by subject until
filed".

## Critique dispositions

Scope critique round 1 (Codex Sol at medium, 2026-11-01, headless leg 28;
CHANGES-REQUESTED, findings=2):

- F1 (MAJOR, S3 the spine author's prompt): adopted — the Done-when item
  "The coordinator's spine-author prompt
  (`scripts/coordinator/terra-spine-prompt.template.md`) drafts new ids
  from the reserved ranges its brief names, never from the watermark's
  mark, and its `--bump-ids` instruction is removed; an author who needs
  more ids than a range holds stops and reports the count, and the
  coordinator reserves again."
- F2 (MINOR, S2 a ruled correction): adopted — the Trust producer's
  "Each range starts one above the larger of the carrier's mark and
  trunk's committed mark for its space, so a ruled `--correct-mark` on
  trunk raises the next reservation's floor, and the correction's record
  is kept", and the carrier item "and a reservation after a ruled
  `--correct-mark` on trunk starts above the corrected mark".

## Done-when

**The spine** (the intent turn, TC first; one checkpoint sitting)
- [ ] SR-174 (amended), two new LLRs, TC-158 (amended) and two new TCs carry
  the target meaning above, and IF-101 is updated. No cell names a code
  file, function or symbol.
- [ ] The rows are judged at one checkpoint sitting and acted on from its
  verdict. The SR, LLR and TC rungs are released, so no act here is the
  owner's.

**The carrier**
- [ ] The reserve verb admits and refuses exactly as the S3 table says; each
  refusal is driven, with nothing written.
- [ ] A reservation writes one carrier commit by compare-and-swap. Its first
  use creates the carrier from trunk's committed watermark. A lost race
  refuses with nothing written (driven with two worktrees).
- [ ] Two reservations in sequence, and two from stale bases, receive
  disjoint ranges, each starting one above the carrier's mark. This is the
  folded sittings rule, with a test that fails on today's code; and a
  reservation after a ruled `--correct-mark` on trunk starts above the
  corrected mark.
- [ ] The fold gives each space's maximum, the union of records, and the
  basis from the receiving tree's live ids, on a clean file and on a
  conflicted one.
- [ ] The hand-raise rule admits a rise covered by a record in the commit's
  own file and refuses one above every record. A committed record that is
  altered or deleted is refused across every parent. `--bump-ids` and
  `--correct-mark` keep every record. A reservation line never reads as a
  correction.

**The landing**
- [ ] Every row of the landing table is driven, on both callers (the merge
  slot and a hand squash): a stale-base lane that mints another lane's
  reserved number is refused, and a code-only lane passes with no
  reservation.
- [ ] The landing folds the carrier into trunk's watermark, and a refresh
  that conflicts only on `docs/id-watermark` is resolved by the fold.
- [ ] The act ledger, `_record_act`, act numbering and the act latch are
  unchanged (their tests pass untouched).

**The text**
- [ ] PROCESS.md §4 states keep-or-mint once, beside CLARITY and MEANING.
  Lean toward a new id; keep it when its spirit is retained and keeping
  costs fewer changes overall; keeping needs a cross-reference that checks
  every findable user of the id against the amended meaning, updating one
  the change breaks or minting instead. The `byte-budget-guard` skill
  reports the delta and restamps.
- [ ] `spine-questions.md` §0 cites it (one line, no restatement).
- [ ] The coordinator's spine-author prompt
  (`scripts/coordinator/terra-spine-prompt.template.md`) drafts new ids
  from the reserved ranges its brief names, never from the watermark's
  mark, and its `--bump-ids` instruction is removed; an author who needs
  more ids than a range holds stops and reports the count, and the
  coordinator reserves again.
- [ ] Recipes §4 replace the floor briefing with "reserve before drafting"
  (the coordinator reserves the draft's counts before dispatching the spine
  author, and the brief names the reserved ranges). Its rebase row for
  `docs/id-watermark` becomes the fold. SKILL §4 drops "and the id
  watermark" from the latch sentence. Both copies, shipped and dogfooded,
  stay in sync.

**Shipping and the bar**
- [ ] One RESYNC entry. The carrier exists from the first reservation. A
  lane that adds spine or off-spine registry ids reserves them first, or
  its landing is refused (a forced change for an adopter running lanes; a
  trunk-only repository is unaffected). A lane open at upgrade reserves and
  renumbers before it lands. The watermark gains a record line kind, which
  every writer carries, and no existing file migrates. `--bump-ids` is no
  longer the lanes' spine minter.
- [ ] At this row's landing, every other open lane that adds carrier-space
  ids is named, and each reserves and renumbers before its own landing.
  This row's own ids are reserved through its verb, so its landing passes
  its own check.
- [ ] `docs/cli-reference.md`, `docs/interface-reference.md`,
  `prompts/CATALOG.md` and the other generated pages are regenerated.
- [ ] The commit bar is green, and both strict lints (`trace.py --strict`,
  `check_trajectory.py --strict`) are clean on the landing tip.

**Ruled by the owner**
- [x] OI-116 ruled 2026-11-01 (a), spine only: revision 33 stands, WI ids
  stay minted on trunk and R1 stays, so nothing above changes.
