## 2026-09-02 — WI-574: spot-check the clean close of WI-572

**Spec of record:** `../archive/work/complete/WI-572-the-approval-act-is-the-adjudi.md`
(the closed row itself). Sampled because `docs/process.toml [attestation]
complete_review` is `sample`, not because anything was alleged. The close stands;
a finding here is a successor row, never a reversal.

**Verdict: the close STANDS WITH FINDINGS — two successors drafted.** The
per-arm verification and the finding's evidence are in the row's own
`## Deliverable`; this fragment records how the session was run and what a
reader of the log needs that the Deliverable does not carry.

### How it was checked

Read-level, but at the TREE and not at the record: every arm WI-572's `## Context`
named was located in the shipped code by symbol and line, and the wiring was
verified as a CALL SITE rather than a definition (`integrate.py:2425` invokes
`_approval_act_refusal`; `human_approves_spine` has exactly two callers). The
lesson from WI-563's first pass — an environment claim excusing a check the
environment can run — was taken seriously: the toolchain was located and the
declared bar was run, not attested around.

### The finding, in one line

WI-572 named two follow-ons it deliberately did not take, declared
`Deferred open items: none`, and closed clean — so both live only in
`docs/log.md` prose, which is what happened and not what is next. Neither
appears anywhere in `docs/work/` or `docs/requirements/open-items.toml`. Both
verified still live at this HEAD; both now carry a drafted successor.

**A process observation, offered rather than filed.** The naming-vs-filing gap is
not WI-572's alone: `gen_open_items.py --check` is satisfied by
`Deferred open items: none`, and a fragment may then name any number of
follow-ons in prose that reach no queue. WI-572's own sentence — "NAMED above
rather than owed back as decisions" — reads as a deliberate, sanctioned exit
because nothing contradicts it. Whether a named follow-on should have to land in
`## Dispositions` or an OI is a doctrine question a spot-check should not settle
unilaterally, so it is recorded here for a sitting rather than minted as a third
successor.

### Environment note (this Mac)

This worktree has **no `.venv`** and must not grow one — a lane-created `.venv`
symlink is what broke the trunk environment mid-intake during the WI-572 cycle.
The interpreter used throughout was the trunk repo's:
`/Users/diytechy/Documents/ai-template/.venv/bin/python`. The commit hook,
however, runs under ambient `/usr/local/bin/python3`, which has no `ruff`, so it
printed its "A DECLARED CHECK DID NOT RUN — format" banner on every commit of
this branch. Recorded honestly rather than papered over: this row changes no
Python, so `ruff format` had nothing to grade here, but the banner is real and a
lane that DOES touch Python on this box must run the format step through the
trunk interpreter itself.

### Bar

Real output, quoted with its interpreter and revision in the row's
`## Deliverable` under the `fig:` markers. Smoke **1459 passed, 8 skipped in
24.96s**; budget **22.6s vs 60s -> within**; `check_docs --stale` **OK, 0
broken**; `tests/test_derive_stage.py` **18 passed** (finding 1 is latent on this
lane — it amends no spine row — so no red is handed on).

Pre-existing and NOT this row's: the `check_trajectory` WARN that WI-574's own
Title is 150 characters. It arrived with the mint, and editing the Title renames
the spec file mid-lane; left for the trunk side.

### Spine

This row authored and amended NO spine rows and moved no `Status`, so it owes no
approval-brief regeneration and performs no approval act.

Deferred open items: none owed back as a decision by this row — the one
owner-owed question it found (whether the owner's approval brief narrows to the
held rungs) is carried as the `open_item` cell of the second `## Dispositions`
draft, so the mint files it as a `pending` OI gating that successor rather than
leaving it in prose. Which is precisely the failure mode this spot-check found.
