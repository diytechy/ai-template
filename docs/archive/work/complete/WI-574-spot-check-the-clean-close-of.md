+++
id = "WI-574"
title = "spot-check the clean close of WI-572 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

Sample spot-check of the GREEN close of WI-572 (the approval act is the
adjudicator's, on trunk). One question asked: does what shipped answer what the
row asked for? **Verdict: the close STANDS WITH FINDINGS — two successors are
owed.** Nothing about the WI-572 merge is reversed; a spot-check finding is a
successor row, never a reversal.

**What shipped answers what the row asked for.** Every arm the row's `## Context`
named was checked at this branch's HEAD, by reading the shipped code rather than
the record that describes it:

- **The lane refusal exists and is wired.** `acceptance_record.staged_approval_acts`
  (:511) reports the flip and the born-`Approved` mint over `APPROVAL_ACT_CSVS`
  (:144, four spine tiers, SN included); `lane_approval_refusal` (:685) words the
  stop and also names every `SNAPSHOT_DIR` file the delta touched, worded by its
  `--name-status` letter through `_SNAPSHOT_ACT` (:606) — so the "each worded by
  what the branch DID to it" claim is true of the snapshot half as well as the
  row half, which is the half that was easiest to state and not do. It is
  construction-first as claimed: one shared two-tree walk `_spine_row_sides`
  (:422) feeds all four readers. `integrate._approval_act_refusal` (:1127) is the
  rung and it is CALLED, at integrate.py:2425 — the check verified, not the
  definition.
- **The first-approval arm exists, dial-filtered at both ends.**
  `intake._first_approval_drafts` (:809) over `_released_drafted_rows` (:748),
  which filters through `agent_common.human_approves_spine` (:895) off the single
  `SPINE_APPROVAL_RUNGS` table (:809) — and `adjudicate_brief` reads the SAME
  predicate (:517), which is the round-1 MAJOR's actual fix rather than a guard
  bolted beside it. `Adjudicates` is a real `wi_convert` column (:173, :220) and
  is serialized at intake.py:1546, so the recorded scope the merge slot joins
  against is carried, not assumed.
- **The aftermath slot, the chain, the round trip.** `adjudicate_brief._aftermath`
  (:522) is bound into the amendment template's `{aftermath}` (:86);
  `trace.spine_chain` / `chain_buckets` (:3085, :3076) are public;
  `baseline_snapshot.format_approves` / `parse_approves` (:300, :273) sit in the
  module that owns the `;` separator.
- **The bound is CLOSED, not merely declared.** `OUTSIDE_THE_APPROVAL_ACT` (:165)
  names the three off-spine registries and the comment states the invariant
  `SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT` that
  `tests/test_acceptance_record.py` pins — which is what makes a tier added to
  `baseline_snapshot.SNAPSHOTTED` unable to reach no approval reader at all.

**THE FINDING: two deliberately-named follow-ons reached no working surface.**
WI-572's compiled record (`docs/log.md`, "Not done here" and the
`Deferred open items:` line) names two follow-ons it consciously did not take,
and then declares `Deferred open items: none — the ruling this row executes is
already recorded. Two candidate follow-ons are NAMED above rather than owed back
as decisions`. That satisfied `gen_open_items.py --check`, and the row closed
clean. But NAMING a follow-on in a log fragment files it nowhere: `docs/log.md`
is what happened, not what is next. Grep of `docs/work/` (all eight folders) and
`docs/requirements/open-items.toml` for either follow-on returns nothing. Both
are verified still live at this HEAD:

1. **The harness-bar asymmetry.** `tests/test_derive_stage.py:528`
   (`test_this_repo_s_committed_stage_is_current`) asserts
   `recorded["fingerprint"] == kitstage.fingerprint(ROOT, memo=None)`
   unconditionally — no work-branch exemption — while its commit-bar twin
   `derive_stage.py --check` skips on a work branch (observed live in this
   session's own commit hook: `derived-stage: skipped (work branch
   'wi-574-spot-check-the-clean-close-of' — generated freshness is the trunk
   lane's, concurrency-restructure §5.2)`). WI-572 is what makes this bite: it
   makes lane-side amendment of a settled spine row the NORMAL path (a lane
   amends, an adjudicator approves), and every such amendment moves the
   `docs/stage` input digest. WI-572 predicted "the same red will now greet
   routine lanes" and left it on no queue. Successor drafted below.
2. **The owner's brief was never narrowed, and the narrowing is owner-owed.**
   The plan's §2a table says rows above the threshold do not surface to the
   owner; WI-572 recorded that `trace.py --approve modified` still renders every
   `Drafted` chain, held or released, and that narrowing it "is the owner's
   call". Verified: `human_approves_spine` has exactly two callers,
   `intake.py:768` (the mint) and `adjudicate_brief.py:517` (the brief);
   `trace.py` calls it nowhere. So the dial filter that WI-572 installed at both
   adjudication ends is absent from the surface the OWNER reads, and the plan
   row describing the owner's surface is unsatisfied. Because it changes what
   the owner sees at a sitting, it routes as a pending open item gating a
   successor (OI-73 exit (B)), not as a plain queued row.

**Not a finding, recorded so the next reader does not re-derive it.** The
`wi_convert.read_specs` folder-home walk — the third follow-on WI-572 named
through round 3 — WAS taken in lane at round 4, and the four `test_wi_convert.py`
guards it un-darkened run green here. The `docs/log.md` narrative still carries
the round-3 text calling it "a harness-bar repair on its own row"; the final
Deliverable supersedes it. The two counts also disagree between surfaces (the
compiled log says "five at the merge slot"; the Deliverable says seven plus six
scope cases) because the log text predates the round-028 rework — the Deliverable
is the record and it matches the tree.

**Bar (real output, this worktree, 2026-09-02; interpreter
`/Users/diytechy/Documents/ai-template/.venv/bin/python` — this worktree has no
`.venv` and must not grow one).**

- `pytest -q -n auto` (FULL, unfiltered) -> **3282 passed, 25 skipped in 566.57s**
  — no reds at all, including the two WI-572's own close analysed: neither the
  `docs/stage` currency red nor the `wi_convert` folder-home red reproduces here
  (the first because this lane amends no spine row, the second because round 4
  fixed it in lane)
- `pytest -q -n auto -m smoke` -> **1459 passed, 8 skipped in 24.96s**
- `check_smoke_budget.py --mode enforce` -> **smoke wall-clock budget: 22.6s vs
  60s budget -> within** (exit 0)
- `check_docs.py --root . --stale` -> **OK - 1227 doc(s), 1590 intra-repo
  link(s), 0 broken**
- `pytest -q tests/test_derive_stage.py` -> **18 passed in 17.97s** (so finding 1
  is LATENT here — this lane amends no spine row — not a red I am handing on)

fig: cmd="/Users/diytechy/Documents/ai-template/.venv/bin/python -m pytest -q -n auto" rev=e2a8dfcb
fig: cmd="/Users/diytechy/Documents/ai-template/.venv/bin/python -m pytest -q -n auto -m smoke" rev=e2a8dfcb
fig: cmd="/Users/diytechy/Documents/ai-template/.venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=e2a8dfcb
fig: cmd="/Users/diytechy/Documents/ai-template/.venv/bin/python -m pytest -q tests/test_derive_stage.py" rev=e2a8dfcb

This row authored and amended NO spine rows and moved no `Status`, so it owes no
approval-brief regeneration.

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-572-the-approval-act-is-the-adjudi.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.

## Dispositions

```toml
title = "Give the committed-stage currency test the work-branch exemption its derive_stage --check twin already has"
workstream = "process"
buildtier = "quick"
priority = 3
```

`tests/test_derive_stage.py:528` (`test_this_repo_s_committed_stage_is_current`)
asserts `recorded["fingerprint"] == kitstage.fingerprint(ROOT, memo=None)` with
no work-branch exemption, while the commit-bar step that makes the same claim
(`derive_stage.py --check`, run through `check.py`) SKIPs on a work branch
because generated freshness is the trunk lane's (concurrency-restructure §5.2).
The mismatch was near-unreachable until WI-572 made lane-side amendment of a
settled `Approved` spine row the normal path; each such amendment moves the
`docs/stage` input digest, so a routine lane now meets a red that the trunk lane
clears one merge later. IN SCOPE: give the test the same branch-awareness its
twin has — reuse whatever `check.py` already consults to decide "work branch"
rather than adding a second notion of it, and pin the exemption with a test so
the skip cannot silently swallow a genuinely stale trunk `docs/stage`. Show the
test green on a work branch that amends a settled spine row, and still RED on
trunk with a stale `docs/stage`; the second half is the point — an exemption that
also disarms trunk would trade a false red for a missed one. EXPLICITLY NOT IN
SCOPE: any change to `derive_stage.py`'s own derivation, or to which artifacts
the work-branch skip covers.

```toml
title = "Rule whether the owner's approval brief narrows to the held rungs, then apply the ruling to trace --approve"
workstream = "process"
buildtier = "medium"
priority = 4
open_item = "WI-572 moved the first-approval act to the adjudicator and filtered the minted population by the human-approval dial at both adjudication ends (intake's mint and adjudicate_brief's composition, through agent_common.human_approves_spine). The plan's §2a table row 'Surfaces to the owner' says rows on a RELEASED rung no longer surface to the owner - but trace.py --approve modified still renders every Drafted chain, held or released, and calls human_approves_spine nowhere. Should the owner's approval brief narrow to the rungs the dial still HOLDS (so a sitting shows only what the owner actually owes a signature on), or keep rendering every Drafted chain (so the owner retains sight of what adjudicators are approving on their behalf)? WI-572 deliberately did not decide this: it changes what the owner sees at a sitting, which is the owner's call and not a side effect of moving who acts."
```

Gated on the owner's ruling by construction: the `open_item` cell above makes
`intake._inject_open_item` mint a `pending` OI at this row's merge and land its
id in THIS row's `needs`, so the successor parks `waiting:open-item-pending`
until the ruling lands (OI-73 exit (B) — there is no standalone OI exit). IN
SCOPE once ruled: apply the ruling to `trace.py`'s `--approve modified`
population and to whatever `docs/ratify/CURRENT.md` renders, reading the dial
through the EXISTING `agent_common.human_approves_spine` — a third copy of the
rung table is the exact defect WI-572's round-1 MAJOR was about — plus the
PROCESS_OPTIONS.md §2a table row that describes the owner's surface, which is
unsatisfied prose until this lands either way. EXPLICITLY NOT IN SCOPE: the
adjudication-side filter (shipped and correct), and any change to
`SPINE_APPROVAL_RUNGS` itself.
