---
name: coordinator-cycle
description: Use when coordinating work in this template repo, from scope critique at filing or minting through lane claims, code iteration, spine checkpoints, independent review, disputes and landing.
stacks: [any]
domains: [any]
phases: [dev, gate]
tags: [coordinator, lane, review, adjudication, dispute, landing, workflow]
scope: this-repo
---

# Coordinator cycle (this template repo)

This skill is the coordinator's **procedure**, its one home; the current
handoff is **state** (what landed, what is open, what the owner owes). Read
`CLAUDE.md` and `docs/status.md` first. Exact commands, landing steps and
environment traps are in [references/recipes.md](references/recipes.md). Read
it before your first claim and when a step below points there.

Read beside it:

- `session-protocol`: standing rules (§2), commit bar (§3), records and
  coordinator close-out (§4), commit style (§5).
- `spine-authoring`: "Three ways a spine grows" and its
  `references/in-lane.md`.

Record procedural corrections in this skill or its recipes at close-out, never
as a handoff section. Why: corrections in handoffs force every successor to
reconstruct the chain.

## Roles

| Role | Who | Session |
|---|---|---|
| Build | the `kit-builder` agent (Claude Opus, medium) | one per round; leaves its change uncommitted |
| Spine author | GPT Terra (`gpt-5.6-terra`, medium) | **one retained session per lane**, resumed each turn |
| Code review and scope critique | Codex 6.1 Sol (`gpt-6.1-sol`, medium) | **fresh per review** |
| Adjudication | a retained Claude Opus home, via `coordinator_adjudicate.py` from the lane | the entry point retains it; never a subagent |

Keep judgement independent: Terra authors and Opus judges, Opus builds and
Sol reviews. The adjudicator never drafts the text it judges. Its ruling on a
dispute is final.

## 1. Before the claim: settle scope and trust where the row is born

Settle scope when filing a row or minting a successor, disposition or split;
do not add a lane-size tripwire to an existing row. Before the claim, render
the scope critique with `review_brief.py critique` over the spec and
`docs/rubrics/scope-critique.md` (recipes §1), and send it to one fresh Sol
session with these questions:

- **Name each independently landable deliverable, and which lands first.** If
  the owner keeps several together on purpose, record that in the spec so no
  later session argues it again.
- **Does any deliverable give a file authority over a hold, an act or a gate?**
  If yes, the spec gains a `## Trust` section before the claim:
  - **Producer:** who writes the file, by which route, and what a failed write
    looks like (failed call, timeout, structured error, partial file).
  - **Consumers:** every reader, found by grep and listed by path.
  - **Ruling:** what each consumer does with an absent, unreadable, failed or
    malformed input, and what the authority binds to.

  Route the Ruling to the owner for confirmation or overrule (§5). Apply
  `project-trajectory/PROCESS.md` §3, "When a guard is owed".
  Why: an unstated trust boundary produces separate fixes in every consumer.

Name the change set's **anchor** in the spec: the approved SN or SR it hangs
from. Label any derived SR with its lens (`spine-authoring` §2(c)). File splits
and preparatory rows on trunk before claiming them.

## 2. Claim

Take the coordinator lease at the session's start, before design work; keep a
design session and a claiming session apart. Claim the whole batch under one
scoped unpause: a reviewed deletion of `docs/work/pause`, the claims, and a
byte-identical restore. The steps and the traps are in recipes §2.

## 3. The lane: intent, iterate, checkpoint

Run intent, iterate and checkpoint. Draft the connected spine set once,
iterate code, then reconcile and judge the set against settled code.
Why: alternating code fixes and row re-attestations buys a sitting per fix.

Omit spine authoring and sittings when no new rows, row-text amendments or
Done-when change are owed; traced-only updates owe no sitting.

### Intent: once, at the start

1. The builder builds the first round. Re-run its claimed results yourself,
   then verify, regenerate and commit.
2. Dispatch Terra once to author the **whole change set**, from the anchor
   down, plus the arms map (`spine-authoring`, `references/in-lane.md`). Keep
   new spine rows `Drafted` and existing statuses unchanged; interface rows
   have no approval status. Verify and commit the set without a sitting yet.
   These rows give reviewers the obligations the code is meant to meet.

### Iterate: code only

Each round:

1. **Confirm the commit landed** (`git log -1` moved) before any review. A
   hook-refused commit makes Sol review an empty range.
2. **A narrow Sol review** of the round's delta, from a brief rendered by
   `review_brief.py review --scope narrow`, naming the round file it answers;
   never a hand-written brief (recipes §1). The kit reviewer template carries
   its two clauses: name the failure classes the change admits and hunt those
   first, and say why a guard-adding remedy cannot instead make the defect
   unrepresentable. Keep the spec and Drafted intent as the code's
   obligations; row wording is deferred to the checkpoint, and proposed
   wording goes to the spine change list. File the review as the lane's round
   file with `review_brief.py file`; it refuses a review without exactly one
   `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<n>` line.
3. **Triage under the review threat model** (`project-trajectory/PROCESS.md`
   §6, "Review threat model"). Dismiss a finding whose reproduction needs a
   compromised or contrived host in one recorded line, in the lane's
   `docs/decisions/<branch>.toml`, and never answer it with code. Send a
   contested or third-round finding to a dispute sitting (step 6).
4. **A coverage plan before any fix.** The builder's first answer to a round
   file is a `Plan-WI` table, one row per finding `F#` (F1..Fn in the order
   written): its class, every site of the class with the search that found
   it, and the one owning boundary that ends the class. Run
   `plan_coverage.py --findings` over it (recipes §1) and dispatch the fix
   only on exit 0: every finding covered by a row, or excluded with a reason.
   Carry the table into the next review and ask Sol to try an unlisted site
   per class. Why: an instance fix leaves sibling sites for the next reviewer.
5. **Findings are claims.** The builder confirms or refutes each one on the
   real code path before changing anything. It acts only on verified evidence
   that no setting or OS retry mitigates. Restate a reviewer's direction as a
   construction ("takes the selected row and never reads the registry"); a
   builder has implemented a direction backwards.
6. **A dispute goes to the adjudicator, and you stay neutral.** When the
   builder or you contest a finding, or a finding class reaches its third
   review round, write the findings file and run a `dispute` sitting before
   another build round (recipes §1). Route the builder's position verbatim; do
   not argue the finding. Each finding comes back FIX, DISMISS with a reason
   class, or ESCALATE to the owner; the ruling is final. Record each ruling in
   the lane's decisions record, never re-raise a dismissed finding, and
   exclude it from the next coverage plan by citing the verdict.
7. **A consolidation outside the spec's named surface stops the round.** When
   the fix needs one owner for something several modules outside the spec
   already read, the builder reports it rather than building it. You file a
   preparatory row on trunk, land it as its own lane, and rebase this lane onto
   it. The §1 Consumers list usually predicts this before the build starts.
8. **Trace fields only.** The builder keeps `Implements:`, the LLR module and
   symbols, and the TC evidence current on each commit. Check structural
   integrity and trajectory (recipes §1); append proposed row-text changes to
   the lane's spine change list. Defer spine authoring and sittings to the
   checkpoint, subject to the Done-when hold below.

If the lane changes its Done-when, obtain a verdict bound to that exact text
or an owner ruling before dispatching another build or closing the row.
Use an early checkpoint if necessary; the ordinary cadence does not release
this hold (`project-trajectory/PROCESS.md` §4).

### Checkpoint: when a narrow round has no BLOCKER or MAJOR

1. **Terra, resumed, reconciles the whole set** against the settled code: the
   accumulated spine change list plus the arms map. Verify, regenerate and
   commit the reconciled text before composing the sitting.
2. **The closure check passes** before the sitting (`spine-authoring`,
   `references/in-lane.md`: parents, the arms, TC-to-LLR-and-SR, interface
   citations, the strict integrity checks).
3. **One combined sitting** (`--brief combined`) judges every amendment, first
   approval and Done-when change together, top-down (recipes §1). Carry retired
   rows into scope explicitly. A parent's return carries its children; have
   the verdict distinguish children returned only for their chain. Route returns:
   - spine text goes to Terra;
   - code goes to the builder;
   - a byte-exact one-assertion fix you may apply yourself, openly and
     recorded.
   A follow-up answered in the lane moves out of `## Dispositions` to another
   heading. Re-sit returned rows and any affected chain or newly changed rows.
4. **The fresh, full-lane Sol gate**, from the lane's trunk base to its tip
   (`review_brief.py review --scope full`), reviews code and rows together. If
   it finds code defects, go back to iterate, and hold one more checkpoint
   before landing. Let findings determine the number of checkpoints. When the
   first build needs no narrow round, sit the checkpoint first: one fresh
   full-lane review is then both the first review and the gate.

Before the final gate, restore the trunk-only generated views on the lane
(recipes §3). The module-size stamp is the exception: the lane carries it.

## 4. Land

Parallel lanes are normal; adjudication is a latched event. Sit a lane's acts
only after the lanes ahead of it have landed and it has rebased, so its acts
and the id watermark pull up as each lane lands. A lane that took acts on an
older base gets duplicate act seqs on rebase, and git applies the later act
commits cleanly. Lanes that take acts land one at a time.

1. Rebase onto current trunk before the final act. Use recipes §3–§4; if the
   rebase changes code or authored rows, repeat the affected checkpoint and
   fresh full-lane gate.
2. Keep the adjudicator's act as the lane's last **spine** commit: Status flips
   and the snapshot only, with verdicts committed first. Telemetry may follow.
3. Squash, regenerate, run `check_trajectory.py --strict`, close the row,
   archive the tips, sweep, and close the re-mint citing the act. Every step
   and its trap is in recipes §3.

## 5. Decisions and the owner

Record calls not already settled by the spec or a ruled item in
`docs/decisions/<branch>.toml` (`coordinator-<date>.toml` for calls on trunk),
with the riskiest in `high_risk`. Ask the owner to **confirm or overrule**,
never to approve. A decision only the owner can make, and that blocks a row,
becomes a pending open item cited by the row's `needs` in the same commit; then
move to the next row. Stop that row for an owner signature on a new need, a
frame external crossing or an explicit owner checkpoint. A high-risk finding
goes to the owner. Leave held signatures and open-item rulings to the owner,
along with push and merge to main.

## 6. Close-out

Follow `session-protocol` §4, "Coordinator close-out", including the lease
handback or relaunch. Record procedural corrections here or in the recipes.
The handoff links the one it replaces, points here for procedure, and holds
state only: what landed, what is open, what the owner owes, and the session
prompt. It carries no cycle, recipe or "corrections learned" section.

## Never

Owner-reserved acts and standing prohibitions:

- Push or merge to main. Push is the owner's.
- Rule an open item, or sign a held rung or any act reserved to the owner.
- Leave `docs/work/pause` deleted.
- Read `OWNER_SCRATCHPAD.md` or the adjudicator's token file. Keep only the
  token file's path.
- Self-review, or adjudicate through a subagent. If Codex is rate-limited,
  wait for its reset. After Codex has been unavailable for more than two hours,
  use a fresh independent Opus reviewer and record the same-family relaxation
  in the decisions record.
- Skip a hook, or add a fallback, degenerate or legacy path. Fix the single
  point of failure instead.
- Change `~/.claude` settings, or install software the handoff does not name.
