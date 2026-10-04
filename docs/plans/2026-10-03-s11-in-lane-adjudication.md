# S11, narrowed: adjudicate in the lane, and fix returns in the lane

**Status:** plan for the owner's ruling. Written 2026-10-03, read-only against trunk
`refactor_again` at `d040ad75`. Nothing in it is built. Code cites are `path:line`
under `project-trajectory/scripts/` unless another root is given.

## 1. The direction and the evidence

The owner, 2026-10-03, verbatim:

> "In regards to S11 - Yes, the judges response for rework within lane should
> implement changes within the lane prevent churn / iterative WI creation and
> prevent context cycling."

This answers the coordinator's offer in
[the wave-9 handoff](../handoff-2026-10-03-wave9-coordinator.md) and at the end of
[the wave-8 log fragment](../log.d/2026-10-03-wave8-coordinator.md) (batch Q). The
offer: an independent adjudicator judges a lane's spine text **before** it lands, and
a return becomes a fix round **inside** the lane, not a minted follow-up row plus a
fresh sitting.

**The chain** (`git log --first-parent 46ececa8..d040ad75`). It was fed by two build
items: WI-747 (the observation cadence rows) and WI-667 (the assumption-only cases).
Batch O sat both, so the two chains merged there.

| round | sitting (act) | returned | rework lane |
|---|---|---|---|
| 1 | batch N, WI-766/767 (no act) | all 13 of WI-747's rows | WI-770 |
| 2 | batch O, WI-768/769/772/773 (seq 22) | TC-306; WI-667's LLR-296, TC-309, TC-310; its cross-review found an IF-200 seam ERROR and TC-055's stale `expected` | WI-774 |
| 3 | batch P, WI-775/776 (seq 23, **retaken** after arbitration) | SR-215 (arbiter ruled B); TC-309, TC-310 | WI-778 |
| 4 | batch Q, WI-779/780 (seq 24) | TC-309, TC-310 (test tightness) | WI-781 |
| 5 | WI-783, pending (must share one act with WI-782) | — | — |

WI-747's rows took four sittings and a retake. WI-667's took three, with a fourth
pending. The cost is counted after the two build landings (`1f1dc64e`, `4ba58905`):

- **Trunk commits: 19**, a 20th pending: 10 `mint:` commits (one, `3a32d5a9`, also
  carried WI-777's cadence re-judge, minted anyway), 4 sittings, 4 rework landings and
  1 hand carry-in (`2256e4e3`).
- **Minted rows: 15** (WI-766..770, 772..776, 778..781, 783).
- **Fresh sessions: 20**: 5 adjudicators and 1 arbiter, 6 cross-reviews, 4 builders
  and 4 reviewers, each rebuilding its context. Two coordinator cutovers, both at full
  context, fell inside the chain.
- **Coupling:** WI-771 waited on batch O, WI-782 and WI-783 must share one act, and
  rows were carried into sittings by hand twice. All three come from approved rows
  left drifted on trunk between a merge and its sitting (§4.3).

The rounds were not waste: every return named a real defect, and the cross-reviews of
batches O and P caught defects in the acts. The waste was the overhead around each
round: a mint commit, a row, a lane, and a fresh adjudicator and builder re-reading
everything. In the lane, a round costs no trunk commit and no row, and both sessions
keep their context. **The plan promises cheaper rounds, not fewer.**

Older evidence agrees. The hand path's sweep twice minted a redundant amendment row,
WI-706 and WI-710, where an amendment and its settling act shared one squash
([wave-5 log](../log.d/2026-09-27-wave5-coordinator.md), "Batch C's sweep"). In-lane
adjudication makes that case the normal one, so it is fixed first (§4.2).

## 2. Today's path, step by step

1. **Build and review.** The lane authors `Drafted` rows and amends text, including on
   `Approved` rows. It never flips a `Status` and never writes
   `docs/archive/last_approved/`. The review verdict must name the lane's current
   non-record tree (`integrate.py:1445-1535`, identity at `:1456-1466`).
2. **Merge slot ladder** (`integrate.py:2858-2910`), then `--no-ff` (`:2966`). The
   approval-act rung (`:2894`, body `:1154-1192`) admits a flip only when every claimed
   spec is `adjudication` kind (`_adjudication_lane`, `:1139-1151`); on a work lane
   `lane_approval_refusal` (`acceptance_record.py:901-968`) refuses any flip or
   snapshot write, for two reasons (`:909-916`): **context** (one work item does not
   hold the chain) and **concurrency** (two lanes conflict; the snapshot must not move
   across a workstream).
3. **Mint, inside the held slot** (`integrate.py:3006-3013` →
   `intake.intake_after_merge`, `intake.py:2373-2401`): **amendment rows** by
   `_routed_amendments` (`intake.py:680-699`) over `staged_spine_amendments`
   (`acceptance_record.py:1022-1088`), and **first-approval rows** by
   `_released_drafted_rows` (`intake.py:834-856`, held rungs filtered) over
   `staged_drafted_rows` (`acceptance_record.py:971-1019`). The hand path replays this
   with `intake.py sweep --merged … --before --after`
   ([wave-5 handoff](../handoff-2026-09-28-wave5-coordinator.md), "Hand integration").
4. **A later sitting** composes the brief (`adjudicate_brief.py:1281-1315`). APPROVE
   flips and copies in one reviewed commit; `copy_live` numbers the act `max(seq)+1`
   (`baseline_snapshot.py:1544`), and `refresh_refusal` refuses while any unnamed
   approved row in a copied registry has drifted (`:870-975`). RETURN writes
   `## Dispositions` and edits no cell (`prompts/adjudicate-amendment.template.md:96`;
   `adjudicate-first-approval.template.md:99`). A cross-review is owed under
   `adjudication_review = "when-minting"` (`docs/process.toml:176`;
   `agent_policy.py:945-981`).
5. **The sitting's merge mints the follow-up** (`intake.py:1570-1614`, adjudication
   kind only at `:1582`). The follow-up's own merge mints the next sitting, and the
   cycle goes back to step 3.

**Why the act is trunk-side.** The 2026-09-01 ruling
([plan](2026-09-01-approval-act-adjudicator-only.md) §1; `PROCESS_OPTIONS.md:435-513`)
gives the same two reasons, and neither needs trunk. Context needs an independent
session with a composed brief, wherever its worktree lives. Concurrency needs serial
acts, which §4.1 keeps without making the spine exclusive for a whole sitting.

**Hand integration differs.** The coordinator squashes one commit per item, keeps lane
tips in `archive/lanes` (owner direction 2026-09-28), and sweeps.
`lane_approval_refusal`'s only caller is the merge slot (`integrate.py:1189`). So the
hand path can adjudicate in-lane with no merge-slot change. The loop cannot.

## 3. The proposed path: a spine lane's lifecycle

A lane that hands over no spine text (no released `Drafted` rows and no routed
amendments) is unchanged. It lands on its review verdict, and the merge ladder is its
final pass (pack B2).

1. **Claim, build and review**, as today.
2. **Preview the mint.** Compute what a merge of `merge-base..tip` *would* mint (the
   same `_amendment_drafts` and `_first_approval_drafts`, minting nothing). If nothing,
   go to step 9; otherwise their `adjudicates` lists are the in-lane scope, exactly
   what a sitting receives today.
3. **ADJUDICATE in the lane.** An independent session in the lane worktree, from the
   same composed brief, rules each row APPROVE, MEANING/CLARITY or RETURN. A RETURN
   writes a **required fix** into its verdict file (the finding, and exact replacement
   cells where it can, as Dispositions drafts do today). No act yet; no cell edited.
4. **FIX round.** The builder, resumed, applies the fix as its rework scope. The
   ordinary review round reviews it.
5. **Re-judge.** The adjudicator, resumed, rules the fixed rows. Steps 4 and 5 repeat
   at most N times (§4.6).
6. **Fallback.** After N returns, the unresolved rows stay `Drafted` or drifted, and
   today's mint takes them at merge. This needs no new code.
7. **ACT, last.** After a refresh onto trunk, the adjudicator makes one commit: the
   flips plus `intake.py snapshot --approves … --reattests …`, scoped to the rows it
   approved.
8. **Final review of the post-act tree.** RULING-7's tree identity demands it anyway,
   so it is the act's cross-review (§4.5). If it rejects the act, the act commit is
   **dropped** (reset to its parent, sha archived), not reverted: a revert writes a
   snapshot copy unequal to live (wave-9 handoff, "A retake cannot revert an act").
   Back to step 3 or 4.
9. **Merge.** The loop merges `--no-ff`; the hand path squashes and archives. A new
   rung refuses a stale act (§4.1). The mint finds nothing for settled rows; it still
   mints held-rung and fallback rows, cadence re-judges, Done-when drafts and close
   dispositions.

**Changes by file:**

- `intake.py`: `_routed_amendments` skips rows the range's own act settled (§4.2); a
  preview entry point (e.g. `sweep --dry-run`).
- `integrate.py`: the approval-act rung's actor test moves from "every claimed spec is
  adjudication kind" to "the act lies in a recorded ADJUDICATE range, scoped to the
  lane's previewed rows" (§4.7); an act-freshness rung (§4.1).
- `acceptance_record.py`: `lane_approval_refusal`, reworded to judge the act against
  the lane's own scope.
- `kitlib/verdict.py`: an ADJUDICATE scope rule beside `scope_offenders`.
- `agent_loop.py`: the lifecycle; RETURN routed like CHANGES-REQUESTED via
  `apply_rework_scope` (`:1961-1981`); a round budget patterned on the critique's
  (`:679-705`); the adjudicator resumed through the built-but-off retention layer
  (`session_keep.py`; `docs/process.toml:284-293`).
- Prompts: both adjudication templates gain the in-lane RETURN.
- Docs: `PROCESS.md:443-448` and the table in `PROCESS_OPTIONS.md:435-513`.
- Spine: amend LLR-158 (its detail names `lane_approval_refusal` as the slot's
  refusal of a work branch's act), LLR-140 (the integrator) and LLR-154 (the
  post-merge intake arm). IF-080 ("nonzero exit on any refusal") is unchanged.

## 4. The mechanics

### 4.1 Where the adjudicator sits, and how acts stay serial

**Problem.** Acts are serial today because the adjudication lane is exclusive. With
acts in build lanes, two lanes could both take seq N+1, or each seal a registry the
other's act changes. Holding the merge slot through an LLM sitting is not an option:
the slot is held "for well under a second" by design (`integrate.py:3016-3030`).

**Answer: serialize the act, not the judging.** Judging and fix rounds run in parallel
lanes. The act is each lane's last work commit, taken right after a refresh. A new
slot rung compares trunk's `last_approved/acts.toml` at HEAD with the same file at the
act's parent.

If equal, no act landed in between: this act's seq is trunk's max+1 and its copies
were taken over trunk's current record. If not, the rung refuses and names the retake
coordinators already do by hand
([wave-7 handoff](../handoff-2026-10-03-wave7-coordinator.md), "Parallel adjudications
take the same act seq"): confirm `refresh_refusal` is empty for the same arguments,
reset `last_approved/` to trunk, re-run the exact command.
The ledger's monotonic-seq check (`baseline_snapshot.py:1419-1431`) is the backstop.
**Cost:** one rung, plus a retake whenever two spine lanes race: rare here, possible
downstream under `lanes = 2`. Who retakes is Q6.

### 4.2 The re-mint trap

**Confirmed.** `_routed_amendments` (`intake.py:680-699`) is a pure two-tree diff over
`staged_spine_amendments`, which skips a row only when its `Status` differs between
the sides or is not approved text (`acceptance_record.py:1083`), and never reads
`last_approved/`. So an `Approved` row amended and re-attested in one range keeps its
Status, shows changed text, and mints a redundant amendment row: WI-706 and WI-710.

`staged_drafted_rows` is safe. It reports only rows `Drafted` on the after side
(`acceptance_record.py:998`), so a row approved in the lane is absent, even one that
was returned first.

**Answer.** `_routed_amendments` drops a record when an act entry the range added
names the row (`reattested_between`, `acceptance_record.py:844-864`, already reads
this) **and** the row's text at `after` equals its record copy at `after`. The second
test keeps the mint for a row amended again after its act.

**Cost.** One function and two tests, shared by sweep and slot; useful today.

### 4.3 Act sequence and snapshot coupling

**Problem.** `refresh_refusal` is scoped to the copied registries but judged per row
(`baseline_snapshot.py:870-975`). It refuses while any approved row in a copied
registry has drifted unnamed. An in-lane adjudicator may name only its own lane's
rows, so two cases block it. **Foreign drift**: another unsettled amendment sits on
trunk in the same registry. **Internal drift**: the lane's own returned amendment to an
approved row is still unblessed while a sibling `Drafted` row is ready (why WI-782 and
WI-783 must share one act).

**Answer.** Internal drift: the act waits for the last round; under fallback that
registry's approvals fall back too, which is today's behaviour confined to one lane.
Foreign drift: the lane falls back, since it never carries another item's rows; as
lanes land settled this grows rarer. The owner's held-rung drift
(SN-003/008/009/025/043) still blocks only acts copying the needs registry. **Cost:**
none new.

### 4.4 Held rungs

**Problem.** `human_approval_through = "DevStg-Boundary"` (`docs/process.toml:124`)
holds the needs and the system frame. "A held rung's approval is the owner's act"
(`PROCESS.md:648-655`), and `adjudication_action` answers `recommend` on a held tier
(`intake.py:2605-2627`).

**Answer.** On a held-rung row the in-lane adjudicator only recommends; the row lands
`Drafted` or drifted and the owner approves it later through the approval brief, as
today. Held first approvals are never minted (`intake.py:834-856`); held amendments
still are, since `_routed_amendments` has no held filter, costing one recommend-only
sitting per held amendment (Q5). CLARITY re-attestation on held rungs belongs to the
companion open item on held-rung CLARITY re-attestation and is not designed here.
**Cost:** none in slice 1.

### 4.5 Review roles

**Problem.** `when-minting` owes a cross-review when a verdict drafts a `spine` or
`high-risk` successor (`agent_policy.py:945-981`). An in-lane RETURN drafts none, so
read literally, no in-lane act is ever cross-reviewed. Yet the cross-reviews of
batches O and P caught act defects: the IF-200 seam ERROR, a stale re-attested
`expected`, and SR-215's misleading rationale.

**Answer.** Two existing reviews cover it. Each fix round gets its ordinary review,
which must read amended cells against PROCESS.md (wave-8 correction: "Code review does
not catch requirement-text defects"). The act gets the final review of the post-act
tree, which RULING-7 owes anyway. The dial's meaning is Q4. **Cost:** one review
round per spine lane, replacing the sitting's cross-review.

### 4.6 Who edits what, independence, and the bound

**Problem.** "A row whose findings need answering is RETURNED … never fixed in place by
its judge" (`adjudicate-amendment.template.md:96`). A resumed adjudicator re-judging
text built to its own required fix is partly judging its own words.

**Answer.** The adjudicator edits no cell; it states what the fix must achieve. The
builder authors the cells and may deviate with a stated reason; the fix reviewer
checks them. Independence is bought once, at the end, by a fresh cross-family review
of the act, so the resumed adjudicator is independent enough. This is the retention
plan's rule-3 trade, continuity over independence on the same item
([plan](2026-08-29-adjudicator-session-retention-plan.md) §3.6, §5 item 2(b)), and it
already has a dial, `reset_on_same_artifact` (`session_keep.py:122`, `:506`).

The bound is N = 3 fix rounds, then fallback. Both chains this wave needed exactly
three (770/774/778 and 774/778/781), every return real; N = 2 would have sent both
back to fallback.

**Cost.** The loop must first verify the retention layer on this box (that plan's §5
item 4). The hand path already resumes agents with SendMessage.

### 4.7 S9: the reviewer-commit check

**Problem.** S9 keys on a session's recorded phase and range. `review_scope_refusal`
(`kitlib/verdict.py:949-990`) checks only REVIEW-A/B logs (`:189`, `:919-946`). Each
such range must add exactly its own verdict file (`scope_offenders`, `:822-842`). A
spine lane gains ADJUDICATE and FIX ranges.

**Answer**, designed together as the sister plan's §4 asks. REVIEW ranges keep their
rule unchanged; there are just more of them (one per fix round, plus the final
review). ADJUDICATE ranges get a sibling rule that also enforces "the judge never
fixes": the range may add only its verdict file, the act's `Status` cells on in-scope
rows, the snapshot directory and ledger, and the regenerated views the hook demands
(the wave-8 log records the hook refusing stale views until they were regenerated into
the act). FIX ranges are BUILD ranges, unrestricted; a flip in one is refused by the
approval-act rung, which now asks whether each flip or snapshot write lies inside an
ADJUDICATE range. The hand path writes no session logs, so there these checks stay
the coordinator's recorded procedure, as today.

**Cost.** One reader and one rule, in slice 2.

## 5. What adopters see; RESYNC impact

**No forced migration.** No registry schema change, no required `process.toml` key,
no owner-signed data moved. Each slice carries a RESYNC entry.

**Slice 1** touches only kit-owned files a resync overwrites: a mint that stops
re-minting settled amendments (a fix needing no action), reworded PROCESS.md §4 and
PROCESS_OPTIONS text, and two prompt templates' in-lane RETURN.

**Slices 2-3:** a loop adopter's spine lanes run ADJUDICATE, FIX and a final review
before merge instead of minting sittings. Queued adjudication rows stay valid (the
trunk-side path is the fallback); at `lanes = 2` stale-act retakes can occur. It
changes every adopter loop's default (Q7).

## 6. What this settles, what it leaves, and the owner's questions

**Settled.** Of the S11 sub-questions (sister
[plan](2026-09-23-owner-notes-spine-sessions-and-tests.md) §3.5 and §5's S11 row;
[pack](2026-09-24-owner-review-pack.md) B1), this plan settles in-lane adjudication in
the merge slot (serial acts plus a freshness rung), held-rung rows (they land and wait
for the owner), the amendments this path needs (the 2026-09-01 division of labour,
LLR-158/140/154, RESYNC), and S9's extension.

**Left,** because none bears on churn or context cycling: squash in the loop (RULING-6,
LLR-140's `--no-ff`, IF-080, `branch -d`; the hand path already squashes); the claim
from lane branches (one commit, not a sitting); kept lane refs (`--no-ff` keeps them
reachable); partial-close ranges and held partials (they keep their SR-144
adjudication); the folded mint (near-empty for spine lanes); and cross-lane batching
of sittings (its need largely goes). Option (d) stays its own plan, now smaller.

**Questions for the owner:**

> **Ruled 2026-10-03.** The owner stated these questions were already ruled (OI-101 Q6,
> `docs/log.d/2026-10-03-owner-rulings-oi100-oi102.md`). The repo had recorded only the
> direction ("adjudication in the lane: yes", wave-9 log), so they are recorded here as
> their recommendations stand:
> - Q1: yes.
> - Q2: 3 returns.
> - Q3: the same adjudicator, resumed.
> - Q4: the final review is always owed.
> - Q5: keep the recommend-only sitting for now.
> - Q6: a session retakes a stale act.
> - Q7: one path, no dial.
>
> Under the owner's no-fallback rule (WI-788 risk 7), Q7's "fallback" is not a second
> code path: a lane whose rounds are exhausted lands, and today's mint takes its
> unsettled rows.

1. Amend the 2026-09-01 ruling so that an independent adjudicator session may take
   the approval act in the authoring lane, as that lane's last commit, scoped to the
   rows the lane itself drafted or amended, and admitted only if no other act reached
   trunk since? **Recommend yes:** both of the ruling's reasons survive (§2, §4.1).
2. Bound the in-lane fix rounds at 3 returns, after which the lane lands with the
   unresolved rows unsettled and today's mint takes them? **Recommend 3:** both of
   this wave's chains needed three.
3. Re-judge with the same adjudicator, resumed (continuity), rather than a fresh one
   each round (independence)? **Recommend resumed,** with independence bought once,
   by a fresh cross-family final review of the act.
4. Is the final review of the post-act tree always owed for a lane that took an act,
   whatever `adjudication_review` says? **Recommend always:** RULING-7 owes it anyway,
   and cross-reviews caught act defects in two of this wave's four sittings.
5. For a held-rung amendment the in-lane adjudicator already recommended on, keep
   minting today's recommend-only sitting, or skip it? **Recommend keep for now,** and
   revisit with the companion open item on held-rung CLARITY re-attestation.
6. When an act goes stale because another act landed first, must a session retake it
   (the adjudicator resumed, or the coordinator under recorded delegation), or may the
   merge slot re-run the recorded command itself? **Recommend a session only:** the
   slot refuses and names the retake, which keeps OI-45's single door.
7. Ship in-lane adjudication as the one path for adopters, with fallback to today's
   path, rather than behind a dial? **Recommend one path, no dial:** the fallback
   already keeps every queued row valid.

## 7. Slice plan

**Slice 1: the hand recipe plus the re-mint fix.** This is the smallest slice that
delivers the owner's benefit, on the path this repo lands by.

- **Owner:** rules on Q1-Q4.
- **Kit:** the §4.2 fix with two tests; the mint preview, so `compose.py` scopes
  briefs from the kit's own drafts.
- **Docs:** `PROCESS.md:443-448` and the `PROCESS_OPTIONS.md` table (stating that the
  loop's slot keeps the stricter trunk-side form until slice 2); both templates'
  in-lane RETURN; a RESYNC entry.
- **Recipe, for the next handoff:** after a SOUND review, preview the mint and
  compose against the lane; dispatch a fresh Opus adjudicator in the lane worktree; on
  a RETURN, SendMessage the builder with the fix, Luna-review it, SendMessage the
  adjudicator; refresh, act; Luna-review the post-act tree; squash, archive, sweep.
- **Measure:** over the next three spine lanes, record trunk commits, minted rows and
  fresh sessions per item, and compare with §1.
- **First use:** the first spine lane after the WI-782/783 sitting. That sitting runs
  the old way.

**Slice 2: the merge slot.** The `integrate.py`, `acceptance_record.py` and
`kitlib/verdict.py` changes of §3 (actor test, freshness rung, S9 ADJUDICATE rule),
the LLR-158/140/154 amendments, and a RESYNC entry. It only stops refusing a correctly
placed act; the loop still acts trunk-side.

**Slice 3: the loop lifecycle.** The `agent_loop.py` changes of §3: the ADJUDICATE and
FIX phases, the round budget and fallback, dropping a rejected act, and the adjudicator
resume once the retention layer is verified on this box. It starts only after
`docs/work/pause` lifts.
