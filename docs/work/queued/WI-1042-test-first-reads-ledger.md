+++
id = "WI-1042"
title = "The test-first check reads when each row was accepted from the act ledger instead of replaying registry history"
workstream = "process"
sr_refs = ["SR-217"]
needs = ["WI-1022"]
specref = "docs/reviews/2026-11-history-readers/README.md"
buildtier = "strong"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Context

Filed on trunk on 2026-11-21 from WI-1036's history-reader audit, class (c)
site 3 (`docs/reviews/2026-11-history-readers/README.md`). Its two calls
serve one decision, so one row covers both (the coordinator's ruling at
WI-1036's review).

The test-first check needs to know when each requirement was first accepted,
and when each pair of a test case and a requirement it names first read
accepted. Today it replays every first-parent commit touching the
registries and applies the acceptance-act rule to each commit and its
parent. That recomputes a recorded decision (PROCESS.md §3; the review-churn
plan's item 2). The record exists: each act-ledger entry lists the rows it
accepted and re-accepted, its commit is the one that added it, and the
snapshot copy at that commit holds the accepted rows, test cases' `verifies`
cells included. Acceptance happens only in an act, so reading the acts gives
the same order SR-217 asks for, still from the committed history.

**Settled by the scope critique (2026-11-21).**

- **Before the ledger.** An acceptance before the ledger's first entry
  (seq 1, 2026-09-27) has no entry. It is read from seq 1's snapshot copy as
  at or before seq 1's commit, under the module's existing at-or-before rule
  (LLR-257): it settles the order when it falls at or before the landing,
  and for a requirement's own acceptance at or before the declared start;
  otherwise the requirement is reported unread, never as a pass. This
  repository's start (`[checks] test_first_since`, 2026-11-19) is after
  seq 1, so here the rule reaches only test-case pairs.
- **Pairs.** A pair reads accepted at the first act whose snapshot copy
  holds the test case accepted while it names the requirement, directly or
  through a design row whose `sr_refs` name the requirement in that same
  copy. A re-pointing is so dated at the act that re-accepted it, as the
  acceptance-act rule dates it today.
- **Completeness.** Before the ledger is trusted, every commit since seq 1
  that changes a snapshot copy is checked to add a ledger entry: flips to
  Accepted, and re-acceptances that carry a direct or design-row
  re-pointing. A snapshot change with no entry is a gap: it is filed, and
  the check reads the rows it touched as unread, never as a pass and never
  dated at a later act.
- **The ledger's earlier path.** The ledger moved from
  `docs/archive/last_approved/` to `docs/archive/last_accepted/` on
  2026-11-16; an entry's commit is read across that move, so no earlier
  entry is dated at the move commit. WI-1040 made one walk over the
  ledger's commits, `baseline_snapshot._ledger_commits`, shared by the
  brief's heading (`last_act`) and the accepted-risk reader
  (`risk_acceptance_act`). It reads the current path only, so today it
  dates every earlier entry at the move. The cross-move reading lands in
  that walk, which fixes all three readers in one place (WI-1040's
  finding, 2026-11-22).

SR-217 and LLR-257 (both Accepted) state the replay, so this row amends
LLR-257's text, which drifts for automated adjudication.

**The architectural delta.** The test-first check (`check_test_first.py`,
CMP-007) comes to read the act ledger and the snapshot copies, which
`baseline_snapshot.py` (CMP-006) writes through IF-220. IF-220 gains CMP-007
among its consumers. That cell is one WI-1022 (F-2) rewrites into component
ids, so this row builds after it and writes the cell in F-2's form.

## Trust

The act ledger and the snapshot copies gain authority over the test-first
check's dates, which decide its exit under `--strict` (IF-198). The guard is
owed under PROCESS.md §3 "When a guard is owed".

- **Producer:** `intake.py snapshot` (`baseline_snapshot.copy_live`) appends
  one entry per act, in the act's own commit, beside the copies it wrote. An
  act on a malformed ledger is refused before it moves any byte, so a failed
  write leaves the record as it stood. A malformed ledger is refused whole on
  `trace.py`'s integrity floor (IF-220's notes).
- **Consumers:** IF-220's `consumers` cell lists them; this row adds the
  test-first check there, and the cell stays their one list.
- **The ruling, for each state a supported route produces:**
  - an entry and its adding commit both readable: the act's commit dates
    the rows it names;
  - an acceptance before seq 1: at or before seq 1's commit, as above;
  - no ledger, or an empty one, while a registry holds accepted rows: those
    acceptances cannot be dated, so each requirement whose order turns on
    them is reported unread, never as a pass;
  - an entry whose adding commit lies beyond a shallow clone's window, a
    gap the completeness check found, or a malformed ledger on the walk:
    unread, never as a pass, as IF-198 rules for history that cannot show
    the order.

  A hand edit of the ledger or a snapshot copy is outside the ruling.

## Done-when

- [ ] The completeness check above is run on this repository and its result
      quoted; any gap is filed, not patched over.
- [ ] Both readings come from the ledger and the snapshot copies under the
      rules above; no first-parent replay of the registries remains.
- [ ] The cross-move reading is in `_ledger_commits`; a test shows an entry
      added before the move dated at its own commit by the test-first
      reading, `last_act` and `risk_acceptance_act`.
- [ ] Each state in the Trust ruling has a test, and one test that fails on
      today's code shows a ledger-read date.
- [ ] The check's verdicts on this repository are unchanged, or each change
      is explained in the Deliverable.
- [ ] IF-220 names CMP-007 among its consumers; the cross-component rule
      reports nothing uncovered.
- [ ] LLR-257's text says so (text only); the Deliverable lists its drift as
      the act owed, and the audit note's site 3 is marked resolved.
