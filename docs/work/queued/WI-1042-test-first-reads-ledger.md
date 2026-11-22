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

**Settled by the scope critique (2026-11-21), and the cut by the
coordinator's ruling, 2026-11-22, on the builder's stop: D3 stands; option 2
with LLR-257's at-or-before reading.**

- **The cut (D3).** The vocabulary move `2bee2b551` (2026-11-16) is the
  record's cut. Entries, copies and keys before it are in an earlier
  spelling (the record's directory `docs/archive/last_approved/`, the
  ledger's keys `approved`/`reattested`, the copies' status `Approved`) and
  are never read: no compatibility readers in the core tooling, and formats
  in git history are cut cleanly (the operator's D3, 2026-11-11; test-tiers
  HANDOFF §5, and §9.9, which declined this reader for this check). Every
  acceptance the move carries, pre-ledger ones included, is read as at or
  before the commit that brought the move onto trunk's first-parent line.
  That is LLR-257's existing rule for a row moved into Accepted from a word
  outside the status vocabulary: it settles the order when it falls at or
  before the landing, and for a requirement's own acceptance at or before
  the declared start; otherwise the requirement is reported unread, never
  as a pass. The declared start `[checks] test_first_since` is that commit
  (`f6dd5b87a`, per §9.9's precedent), so those requirements fall out of
  scope here. An act made on a side branch is ordered by the first trunk
  commit that contains it, as a landing is. WI-1040's finding that
  `baseline_snapshot._ledger_commits` reads the ledger's current path only
  is this cut working as intended, not a defect: the walk keeps reading the
  current path only.
- **Pairs.** A pair reads accepted at the first act whose snapshot copy
  holds the test case accepted while it names the requirement, directly or
  through a design row whose `sr_refs` name the requirement in that same
  copy. A re-pointing is so dated at the act that re-accepted it, as the
  acceptance-act rule dates it today.
- **Completeness.** Before the ledger is trusted, every commit since the cut
  that changes a snapshot copy is checked to add a ledger entry, read in the
  current spelling only: flips to Accepted, and re-acceptances that carry a
  direct or design-row re-pointing. The move commit is the cut, not a gap.
  A snapshot change with no entry is a gap: it is filed, and the check reads
  the rows it touched as unread, never as a pass and never dated at a later
  act.

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
  - an acceptance before the cut: at or before the cut's trunk commit, as
    above;
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
      quoted; any gap is filed, not patched over. Measured before any reader
      change: read in the current spelling from seq 1, one change carries
      flips or new pairs with no entry, the move commit `2bee2b551`, which is
      the cut; since the cut, none.
- [ ] Both readings come from the ledger and the snapshot copies under the
      rules above; no first-parent replay of the registries remains.
- [ ] The record before the cut is never read; a test shows an acceptance
      the cut carries dated at or before the cut's trunk commit, never at a
      later act and never read from the earlier spelling.
- [ ] Each state in the Trust ruling has a test, and one test that fails on
      today's code shows a ledger-read date.
- [ ] The check's verdicts on this repository are unchanged, or each change
      is explained in the Deliverable.
- [ ] IF-220 names CMP-007 among its consumers; the cross-component rule
      reports nothing uncovered.
- [ ] LLR-257's text says so (text only); the Deliverable lists its drift as
      the act owed, and the audit note's site 3 is marked resolved.
