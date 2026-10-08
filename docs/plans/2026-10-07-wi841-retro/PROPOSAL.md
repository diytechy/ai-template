# WI-841 retrospective: five changes to the coordinator's in-lane cycle

Written 2026-10-07 for the owner and the next coordinator session. Evidence:
the `wi-841` lane (114 commits), `docs/reviews/wi-841-done-when-blessed-in-lane/`,
`docs/decisions/wi-841.toml`, and the Codex rollouts under
`~/.codex/sessions/2026/10/0{6,7}`.

## 0. What the evidence says about the cycle that ran

| Question | Finding |
|---|---|
| Was Terra retained? | **Yes.** One codex session, 25 turns, from 18:49 on Oct 6 to 15:50 on Oct 7. Turn 1 was a 5 kB brief; later turns were ~1 kB deltas ("Round 19 … apply the Round 17 section of the builder's spine list"). There was one extra fresh Terra session at 21:10. Retention worked and was not a cost. |
| Was Sol retained? | **No, by design.** 17 one-turn sessions, plus one more that died on the usage limit at 02:33. |
| Were Sol's prompts the kit's reviewer template? | **No.** The coordinator hand-writes each one. The kit's `prompts/reviewer.template.md` asks the reviewer to *name the worst failure classes this change admits and hunt those first*, and to say for each guard-adding fix *why the defect cannot be made unrepresentable* (the antidote clause). The hand prompt asks for neither; it asks for individual confirmed findings. |
| Does the kit have a "cover every finding" gate? | **Built, not wired.** `plan_coverage.py --findings` (WI-803) makes each open finding an `F#` clause a replan must cover. Nothing in the loop or in the coordinator's path passes `--findings`. |
| Did anything force Terra and the adjudicator to run after every round? | **Nothing I found.** The cadence was the coordinator's habit, written in the handoff cycle as "Terra authors → adjudicator judges" per change. (Verify before relying on this; see §5's risk.) |
| Where does the cycle live? | In 12 chained handoffs (2,071 lines). Each says "the wave-N cycle plus these deltas": wave 18 → 17 → 11 → 10 → 8. Every wave appends "corrections learned". |
| The overnight gaps | 02:33–04:17 was the second Codex usage limit (confirmed in the rollout). From 05:00 to 13:11 nothing ran after gate 7, the gate whose MAJOR 1 needed your row-coverage ruling (D-027, committed 13:31). |

**Answer to "does code-first move spine editing back out to another WI?"**
No. Spine editing stays in the lane. What changes is the order inside the lane:
code iterates against Drafted intent, and the rows are amended and judged at
checkpoints rather than after every round. The lane-checkpoint sitting WI-841
built is the tool for exactly that (§5). WI-841 just couldn't use it on itself.

---

## 1. Scope is settled when a row is filed or minted

**Owner ruling (2026-10-07).** No size tripwire. A lane's size is context you
can derive after it lands. If scope is a problem, it is handled where a row
comes into being (a hand filing, or a mint from a lane), not by a guard on a
row that already exists. WI-841 was permitted to be large on purpose. Its pain
came from bouncing between code and spine (§5), not from its size.

**WI-841's evidence.** The row bundled three deliverables: the Done-when blessing,
the done-when brief class, and the combined sitting. Only 3 of Sol's ~30
findings concerned the blessing; the combined sitting drove the rest. The row
was filed by hand from a conversation ("the owner agreed the design in
conversation") and claimed straight into a build. It never met the critique or
the plan gate the loop path runs.

**What exists.** The loop has a PLAN/CRITIQUE round (`plan_round.py`,
`critique.template.md`) and a SINGLE-plan coverage gate. The coordinator's hand
path skips both.

**Proposal.**
**Proposal: a scope critique where a row is born.** When a row is filed by
hand, or minted from a lane (a successor draft, a disposition, a split), one
independent critique pass (cross-family, i.e. Sol) runs the kit's
`critique.template.md` over the spec before it can be claimed. It adds two
questions:
- Name each independently landable deliverable. If there is more than one,
  say which lands first. The owner may keep them together, as at WI-841; the
  answer is then recorded in the spec, not re-litigated.
- Does any deliverable give a file authority over a hold, an act or a gate?
  If so, see §2.

A split becomes successor rows filed on trunk before the claim, so R1 holds.

**Enforcement point.** Coordinator procedure, done by rendering the kit's
template (see §6).

## 2. A trust section whenever a file gains authority

**WI-841's evidence.** A verdict file came to release holds, suppress the
intake mint, and authorize merge acts. D-004 called verdicts "trusted as
written by its session", while Sol treated them as hostile. Gates 1–8 were
eight different routes around that one unstated boundary. Your row-tied
authority ruling (D-027) arrived at gate 7. It was a design decision, not a fix.

**What exists.** PROCESS.md §3 "When a guard is owed" already names the boundary
classes (a file on disk, another process, a model's output). Nothing makes a
spec apply it.

**Proposal.** When the §1 scope critique answers "yes, a file gains authority", the
spec gains a `## Trust` section *before the claim*, with three parts:
- **Producer:** who writes the file, by which route, and what "failed" looks
  like (failed call, timeout, structured error, partial write).
- **Consumers:** every reader, found by grep and listed by path. This is the
  list the builder must route through one reader.
- **Ruling:** what each consumer does with an absent, unreadable, failed or
  malformed input (hold or refuse), and what the authority binds to (for
  WI-841: the rows it judged).
The section links to §3 rather than restating it. The owner confirms or
overrules the Ruling line like any decision.

**Enforcement point.** The critique question plus the spec section. No new
script. If you want it mechanical later, `plan_coverage` could treat each
Consumers entry as a clause.

## 3. Land the consolidation first

**WI-841's evidence.** In round 2 the builder created `kitlib/sitting.py`
(D-010). In rounds 5–7 it unified carrier resolution in `spine_carrier`
(D-016–D-018). From gate 3 on it centralized verdict acceptance across the
coordinator and loop routes (D-021–D-026). Each of these was a cross-cutting
refactor of machinery older than the row, done inside a feature lane and
reviewed together with the feature.

**Proposal.** A builder round that needs to consolidate code *outside the
spec's named surface* reports it instead of doing it. It stops with "this
needs one owner for X; these N modules currently read X". The coordinator
then:
1. files a preparatory row on trunk;
2. builds and lands it as its own small lane, with its own Sol round;
3. rebases the feature lane onto it.
The §2 Consumers list usually predicts this before the build starts. That is
the cheap moment to file it.

**Enforcement point.** A `kit-builder.md` standing rule plus the coordinator
procedure. Your sanctioned "rearchitect, don't moth-ball" stands: this changes
*which lane* the rearchitecture lands in, not whether it happens.

## 4. Sweep each finding's class before fixing it

**WI-841's evidence.** Each builder round did answer every finding in its
review: round 1 fixed all five MAJORs in one commit. The trouble was that each
fix covered the *instance*:
- WIDENED was fixed for TOML, then CSV, then markdown, then a conversion;
- "a rejected sitting releases" was fixed in `done_when`, `kind_part`,
  `acceptance_record`, then the loop.
The next fresh reviewer found the sibling. The wave-18 handoff added "fix
crafted-input findings as a class" afterwards, as one more line of prose.

**Proposal: three linked changes.**
- (a) **Sol reviews from the kit's reviewer template**, rendered by
  `prompts.py`, with the coordinator's lane facts (range, basetemp, test list)
  as its fill values. Two things follow:
  - every finding arrives with its failure class and the unrepresentable
    clause;
  - the hand prompt stops drifting from the template.
- (b) **A sweep table before the fix.** The builder's first output for a review
  is a table, one line per finding: finding → class → every site the class
  applies to (with the grep that found them) → the one owning boundary that
  makes the class unrepresentable. The fix follows the table. Wire it to the
  existing gate: the round's plan runs `plan_coverage.py --item SPEC
  --findings REVIEW` and must cover every `F#` (WI-803's built, unwired arm).
  The table travels into the next review.
- (c) **The narrow re-review checks the table, not the diff alone:** "for each
  class, try one site the table does not list."

**Enforcement point.** (a) and (c) are prompt rendering. (b) is
`plan_coverage --findings` exit status, checked by the coordinator before
dispatching the fix. It's the same gate the loop's replan should call, so the
loop and the coordinator share it.

## 5. In-lane spine work: one connected change set, judged at checkpoints

Two different things made the spine iterate in WI-841. They need different
fixes.

**(A) Bouncing between code and spine.** About 20 builder rounds and 21 Terra
rounds produced 19 adjudication verdicts. LLR-262 and LLR-310 were each
re-attested about eight times, because each code fix moved a row that names
the mechanism ("one accepted-verdict reader", "per physical line"). Most of
the 19 verdicts were these amendment re-sits.

**(B) An incomplete subtree** (owner's observation, 2026-10-07). Several
first-approval returns were the tree itself settling, not wording or behaviour:
- **Verdict 002:** returned LLR-308 because it bundled two obligations and the
  combined sitting had no SR parent ("to be split and re-parented"). SR-232
  was derived mid-lane as a result. TC-327 came back with it ("its Verifies
  and Expected must follow that split").
- **Verdict 005:** returned TC-327 "only for its chain" (007's words), i.e.
  for its parent, not for itself.
- **Coverage gaps:** TC-325 and TC-328 were returned (002, 005, 007) because
  they did not cover every arm their LLR states: the serial-landing hold, and
  LLR-262's four mint outcomes.
- **Missing edges:** Sol round 2 found IF-287 with no citing TC. The wave-18
  handoff carries "a TC citing an LLR must also cite that LLR's SR" as a
  correction.

**Why (B) needs its own mode.** A spine grown from a vision is stepped tier by
tier: SN approved, then SRs derived from it, then LLRs, then TCs. Each tier's
judgement is the input to the next, and the spine-authoring skill is organised
that way (§1 SN intake, §2 SR derivation, §3 LLR and TC).

An in-lane change is different. It is a found defect or a new scope that hangs
from rows already approved. Its whole subtree (any new or derived SR, its
LLRs, TCs and IFs, and the approved rows it amends) can be authored in one
pass and judged in one sitting. That only works if the set is closed: every
edge present, and every arm a parent states verified by a child. Otherwise the
sittings converge one link at a time, as 002 → 005 → 007 → 009 did.

**Proposal: an in-lane change set, inside three lane phases.**
1. **Intent (once, at the start).**
   - The spec names the change set's **anchor**: the approved SN or SR the
     change hangs from. A derived SR names its lens. This is part of the §1
     scope critique.
   - Terra authors the **whole connected subtree in one turn**, at obligation
     level, from the spec and the §2 Trust section. New rows stay `Drafted`
     and owe no sitting yet.
   - Terra's brief requires an **arms map**: for each LLR, the outcomes and
     refusals it states, and for each arm the TC clause that verifies it.
     That is the semantic edge that TC-325 and TC-328 were missing.
2. **Iterate (code only).**
   - Builder ↔ narrow Sol rounds. The builder keeps the traced cells in step
     (`Implements:`, `code_symbol`, TC evidence; they owe no adjudication),
     so `check_trajectory --strict` stays green on every commit.
   - The builder appends every row change it *would* make to the spine
     change list it already keeps (`wi841-builder-spine-list.md` had
     per-round sections).
   - Sol's narrow prompt says the rows are stale by design until the
     checkpoint; judge the code only.
3. **Checkpoint (when a narrow round has no BLOCKER or MAJOR).**
   - One Terra turn reconciles the whole set against the settled code: the
     accumulated list plus the arms map.
   - **A closure check before the sitting:**
     - every row's parent is in the set or Approved;
     - every LLR in the set has a verifying TC for each mapped arm;
     - every TC cites its LLR and that LLR's SR;
     - every new or changed IF has a citing TC.
     The ID-level parts are what `trace.py --strict-integrity` and
     `check_trajectory --strict` already check (confirm they can run scoped
     to the set). The arms map is the part that needs judgement.
   - **One combined sitting** judges the whole set top-down: amendments,
     first approvals and any Done-when change, WI-841's class built for
     exactly this. A parent's return carries its children; the verdict says
     which children were returned only for their chain, so they are not
     re-authored on their own.
   - Then the fresh full-lane gate reviews code and rows together.
   - If that gate finds code defects, go back to phase 2, then hold one more
     checkpoint before landing. Expect 2–3 checkpoints per lane, not 15.

**Where it lives.** A short "In-lane change set" section in the
spine-authoring skill: the anchor, the whole-subtree pass, the arms map, the
closure check, and the top-down sitting. It sits beside the tier-stepped
sections, which stay as they are for vision-grown work. If PROCESS.md needs the
rule at all, it gets one sentence that links to the skill.

**Risk to check first.** I found nothing that forces a per-round re-sit, but I
did not prove it. Before adopting, run one lane with a deliberately stale
approved-row amendment held to the checkpoint. Confirm that no pre-commit step
refuses the iterate-phase commits and that the merge integrity step is the
first to object.

**Enforcement point.** Coordinator procedure and the spine-authoring skill.
The tooling (the combined sitting, the spine list, the traced-cell exemptions,
the integrity checks) already exists. A small WI is owed only if the closure
check cannot run scoped to the set.

---

## 6. Is the coordinator's hand path growing past what you intended?

Yes, and that is the root of 4 and 5. The hand path is now a second
implementation of the loop's cycle:
- **Its own prompts**, hand-composed per round for builder, Sol and Terra,
  instead of the kit's rendered templates.
- **Its own sequencing**, with no PLAN, CRITIQUE or findings-replan gate.
- **Its procedure kept as accreting prose**: 12 handoffs, each a delta on the
  last, with a "corrections learned" list each wave.

That breaks the kit's own rules (single source, generated rather than
hand-maintained, enforced at the commit). Each WI-841-style lesson becomes one
more prose line the next session may or may not apply.

There's a working precedent for the fix: adjudication. The coordinator used to
hand-run adjudicators. `coordinator_adjudicate.py` now composes through the
same `adjudicate_brief.compose` the loop uses. WI-847 (the loop's reviewer
resumes in a lane) moves review the same way.

**Recommended order, smallest first:**
1. **No code, next session.** Two skill changes:
   - Replace the handoff chain's cycle with one `scope: this-repo` skill,
     `coordinator-cycle`, holding:
     - the lane phases of §5;
     - the sweep table of §4(b);
     - the scope critique at filing and minting, §1;
     - the Trust section of §2;
     - the stop-and-file rule of §3.
     Handoffs go back to holding *state only*. This consolidates, so the next
     "correction" edits the skill instead of adding a 13th delta.
   - Add "Three ways a spine grows" to the spine-authoring skill: the mode
     table and the parent-first rule in `SKILL.md`, the two lane modes in
     `references/in-lane.md` (§5, §7).
   Drafts: `drafts/` beside this file, reviewed by Sol (`sol-skill-review.md`).
2. **Small WI:** the coordinator renders Sol's review prompt (and the
   critique) through `prompts.py` from the kit templates, as
   `coordinator_adjudicate.py` already does for adjudication. Bring the
   untracked `coordinator-tools` into the repo. Closes §4(a).
3. **Small WI:** wire `plan_coverage --findings` into both the loop's rework
   and the coordinator's round. Closes §4(b) as a gate.
4. **WI:** the parent-first approval check (§7.2). It comes first among the
   guards because the spine already breaks the rule.
5. **WI:** the state-based protection of held-rung rows (§7.1).
6. **Small WI:** compose `spine-authoring`'s tier questions into the
   adjudication briefs at render time (§7.3).
7. **Small WI:** the verdict rollup reads the coordinator's review files too
   (§7.4).
8. **Direction, not yet a row:** the coordinator drives the loop's phases
   (`agent_loop --wi`) per lane instead of reimplementing them. Steps 2–3 make
   that cheap. WI-847 is the first piece.

The first change set run under §5 is also the test of §5's open risk. A
set-scoped closure check is not needed: a clean whole-repo strict run covers
the set, and arm coverage is a judgement either way.

---

## 7. Guards on spine approval (owner rulings, 2026-10-07)

### 7.1 Held-rung rows are protected by state, not by who committed

**Today.** Two checks protect a rung the dial holds for a human:
- `held-status`, at pre-commit and as a merge-slot rung, refuses a held
  Status move. It is armed only for commits carrying the `Loop-Session`
  trailer ("A person's own lane is not governed").
- `held_reattest_refusal` refuses an adjudication act that re-attests a held
  row without naming a CLARITY verdict.

None of the coordinator path's commits carry the trailer, so a coordinator
lane is treated as a person's: nothing mechanical stops it flipping an SN.
Every commit here also has the same git author, so identity cannot come from
the author either.

**The owner's rule.** Judge by state alone: the live registry, the snapshot
and the dial.
- **Where:** on every commit against its parent (pre-commit: staged against
  HEAD; at the merge slot: each lane commit against its parent, as
  text-then-act already walks).
- **Which rows:** a row whose registry's rung the dial holds, with the dial
  read as committed on trunk.
- **What counts as an approval:** the commit moved the row's snapshot copy and
  left the live row equal to it. That covers a first approval (the row enters
  the snapshot as Approved) and a re-attestation (amended text re-copied).
- **Allowed:** the row's Status is unchanged and a verdict in the commit's
  range rules that row CLARITY, bound to its exact text by a digest.
- **Otherwise:** refused, naming the row, its rung and the dial.

**Where it applies: what arrives from a lane, never a direct trunk commit**
(owner, 2026-10-07). A human or authorized approver approves held rows on
trunk, and that channel is not judged, so no owner record is needed. The rule
judges each lane commit as it lands.

**But the coordinator does not land through the merge slot.** It lands with a
hand `git merge --squash`. On that path only the pre-commit hook runs, and it
judges the squashed commits for text-then-act (it reads git's `SQUASH_MSG`).
None of the slot's rungs run:
- the approval-act rung, including WI-841's accepted-verdict and row-coverage
  checks;
- the held-status rung;
- the Done-when merge hold. Only its separate hand-close hook step runs.

The S11 plan chose this ("the hand path can adjudicate in-lane with no
merge-slot change… these checks stay the coordinator's recorded procedure"),
and the loop's half of it (the approval-act rung admitting a recorded
ADJUDICATE range) was never built. Through the slot as it stands, WI-841's
lane (`safety_class = "ordinary"`) would have been refused for carrying acts at
all.

So the state rule must ride the lane-commit walk that both the slot and the
hook's squash path share, as text-then-act does. The fuller fix is for
coordinator landings to go through the slot, once its approval-act rung admits
in-lane adjudication ranges. That is the S11 plan's unbuilt `integrate.py`
change, and part of step 8.

**Residual:** an agent session making a plain commit on trunk is not judged.
That stays review-enforced, by the coordinator's Never list, as today.

**Consolidation.** The rule subsumes both checks above. Retire the
trailer-armed `held-status` arm and the act-ledger `--verdict` arm in the same
WI (the 0→A→B rule). **Downstream:** an adopter's own trunk approvals are
untouched. A loop lane that lands a held-rung act it is not entitled to is
refused, as today, but by state instead of by trailer.

### 7.1b The approval act is kit-wide in the lane (owner ruling (a), 2026-10-07)

An independent adjudicator may take the approval act in the authoring lane.
This supersedes the trunk-side clause of the 2026-09-01 ruling. One row lands
the doc and the check together:
- **The doc:** PROCESS.md's "Fixed points" sentence, process-options "Who
  performs the approval act" (its division-of-labour table), and the
  `spine-authoring` preamble ("on the serial trunk side").
- **The check:** the merge slot's approval-act rung stops asking "is every
  claimed spec of the `adjudication` kind?" and asks whether every act is
  backed by an accepted verdict from an independent session that judged that
  act's own rows. WI-841 already built that question:
  `kitlib.sitting.unaccepted_refusal` and `uncovered_refusal`, today reached
  only on adjudication lanes.
- **The landing:** once the rung admits in-lane acts, coordinator lanes land
  through `integrate.py integrate` rather than a hand squash, so every slot
  rung runs on them.

**Order.** The skill row's `in-lane.md` already describes acts taken in the
lane. Either land this row first, or land both in one batch.

### 7.2 A child is approved only after its parent

The owner expected this check to exist. It does not:
- **LLR-281 and TC-291 are Approved under SR-224, which is `Drafted`**,
  and have been since WI-615 (2026-09-28).
- Neither `trace.py --strict-integrity` nor plain `trace.py` mentions it.

**Rule.**
- An SR is approved only once every SN it cites is.
- An LLR is approved only once every SR it cites is.
- A TC is approved only once every row it verifies is.
- `Founded` counts as approved.

**Enforcement.**
- **At the commit:** refuse a commit that leaves an approved child under a
  non-approved parent, where the commit moved either one's status.
- **Standing integrity finding** for what is already there.
- **The two live cases are fixed first.** SR-224 sits on a released rung
  here, so an adjudication sitting can approve it. Otherwise the children go
  back to `Drafted`.

### 7.3 One home for the adjudicator's questions

`spine-authoring` calls itself "the adjudicator's question list per tier", but
no adjudication brief references it. `adjudicate-first-approval.template.md`
carries its own short method instead. A brief cannot simply point at a skill:
skills are opt-in accelerators an adopter may not install, and the brief feeds
a gate. So compose the relevant skill section into the brief at render time,
the way the combined brief composes the per-kind briefs. That gives one
source, generated, with a self-contained brief.

### 7.4 The rollup is blind to the coordinator path

`docs/reviews/rollup/` is generated on trunk from the loop's round files
(`NNN-REVIEW-A-<sha>.md`). The coordinator's `sol-review-*.md` files use
another format, so no coordinator-era lane (WI-806 to WI-841) has a rollup.
Step 2 (render reviews through the kit) fixes this at the source. Until then
the rule is only: a lane never commits a rollup.

---

## 8. Reconciliation with the queue (2026-10-07)

All 29 queued rows were read against the nine rulings
(`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`). The main finding: the
owner-approved WI-788 design (`docs/plans/2026-10-04-wi788-design/`, OI-104,
filed as the S788 rows WI-798 to WI-817) already moves approval acts into the
lane (its change 8, superseding the 2026-09-01 division). It also already has
"the adjudicator drafts" spine text (change 4, WI-812). So ruling 6 is the
direction the queue was already heading, and several P-rows overlap it.

### 8.1 What each proposed row becomes

| Row | Verdict | Why |
|---|---|---|
| P1 skills | **File.** One owner question first (§8.3 Q1) | Drafts ready. If the S788 authoring model wins, the coordinator-cycle text changes |
| P2 approval act in the lane | **File narrowed:** docs plus the approval-act rung only | The landing switch is WI-808's ("Both paths yield one landing per lane"). WI-809 then narrows to the loop's lifecycle on top of P2's rung |
| P3 parent-first | **File** | Not covered anywhere. Settle SR-224's chain first (released rung: adjudicate it, or return LLR-281 and TC-291) |
| P4 state-based held rung | **File**, after WI-828 | WI-828 builds the hook's merge walk P4 rides. WI-800, WI-807, WI-809 and WI-810 amend LLR-246 under the trailer-armed design P4 retires, so P4 goes before them |
| P5 coordinator renders briefs | **File render-only** | WI-801 owns the launch path (`ask.py`). Bringing the coordinator's launch scripts into the repo would make a second launcher WI-801 must delete |
| P6 findings gate | **File the shared step plus the coordinator wiring** | The loop half belongs in WI-805's replan, which is designed with "the open findings" as clauses |
| P7 tier questions in briefs | **File**, before WI-812 | Same templates |
| P8 rollup reads coordinator reviews | **Fold into P5** | Once coordinator reviews are written as kit round files, the generator sees them. WI-816 retires the legacy hand-rollup window, so slot landings for coordinator lanes need P5 first |

### 8.2 Queued rows that need an edit

**Applied in this commit:** `docs/status.md` (the PROCESS.md dial follow-up,
already fixed in `bec70dc5`), WI-823 (its mint premise: the open re-judge
WI-831 suppresses a second mint) and WI-817 (D6 also retires WI-841's carrier
consumers).

**Proposed, for the owner to accept (no new ids needed):**
- **WI-828:** widen the merge walk to the hook's one lane-commit walk, with
  text-then-act as its first rider. Add "LLR-302's detail and a TC are
  amended to state the walk" (the row makes LLR-302 untrue).
- **WI-834:**
  - L303: "authored as one connected change set and judged in one combined
    sitting at the lane's checkpoint".
  - L179-181: the close-out recipe's home becomes `coordinator-cycle` once P1
    lands.
  - Part C: its interactive OAuth sign-in step is superseded by WI-846's
    token. Defer to WI-846 and drop the consent text, or land WI-846 first,
    as status already advises.
- **WI-846:** say SR-227's "retire it at once when a call on it fails" is
  amended to exclude an authentication failure. Add the session-protocol
  sign-in text to its deliverables.
- **WI-805:** "the replan's gate runs `plan_coverage --item <spec> --findings
  <review>`; the build is refused until every `F#` is covered or excluded".
- **WI-801:** replace "the S11 hand recipe" with "the `coordinator-cycle`
  skill".
- **WI-847:** "SR-227 amended to cover the review class, or a new SR".
- **Optional, ruling 3 closure:** WI-798, WI-800, WI-801 and WI-807 name a new
  LLR or IF with no TC. WI-798, WI-799 and WI-804 omit an anchoring SR from
  `sr_refs`.

**Proposed once the P-rows have ids:** add P2 and P4 (and P3) to the `needs`
of WI-808 and WI-809. Rewrite WI-809's held-CLARITY bullet to ride P4. Give
WI-810's minted successors the scope critique (ruling 2's loop side). Have
WI-833 ride the shared walk if it builds before P2. Count a recorded dispute
as covered in WI-811 for P6. Sequence P5 with or before WI-847.

**Sequencing:** SR-227 is amended by WI-834, WI-846 and WI-847. Run them one
after another, each rebased on the last, so the approved SR is not re-sat
three times in parallel. WI-823 goes before WI-831.

### 8.3 Questions only the owner can answer

**Outcome, 2026-10-07:** Q1 ruled. An author (Terra, or another declared author
role) does the first authoring pass, and the adjudicator judges. WI-812 is
re-scoped to match, and README changes 4 and 14 are annotated as superseded.
Q2 to Q5 are filed as OI-108 to OI-111, each cited in the `needs` of the row
that waits on it (WI-801; WI-800 and WI-807; WI-846; WI-811).


1. **One authoring model for in-lane spine text.** Today's coordinator
   practice, which the P1 draft records: Terra authors the whole set and an
   independent Opus judges it. The S788 design (WI-812, OI-101 Q1): the
   adjudicator drafts or adopts the text inside JUDGE, an adjudication
   reviewer edits it, and the adjudicator's unchanged final pass is the act.
   Ruling 3 asks for one consistent decomposition, so one of these should win.
2. **Ruling 7 under A1.** WI-801 makes the review kinds OPENAI-only, and A1
   makes an absent family "not eligible", so the two-hour Opus relaxation
   could not be drawn after WI-801. Add a declared relaxation to `ask`
   (logged, a "Decisions to review" entry)?
3. **Ruling 8 under the station authority.** WI-800 and WI-807 run
   `trunk_step` lane-side under the authority, and that step writes the
   rollup. Does generation on the landing tree under the authority count as
   "on trunk", or does the rollup step stay out of the lane-side run?
4. **WI-846's token dial.** Is the dial naming the token file tracked? If so,
   it commits the owner's personal path.
5. **WI-811's reviewer family.** "The final-review family excludes every
   author", read as a hard rule, forbids ruling 7's fallback. Reword it as a
   ranked preference (A1 step 3)?

### 8.4 Corrections to this proposal's own drafts

- `drafts/spine-authoring/references/in-lane.md` tells a held CLARITY act to
  name its verdict with `--verdict`. That is today's mechanism and the arm P4
  retires, so P4 updates that line when it lands.
- `drafts/coordinator-cycle/SKILL.md` says "file splits and preparatory rows
  on trunk". WI-810 moves coordinator filings into station lanes, so that line
  changes when WI-810 lands.
