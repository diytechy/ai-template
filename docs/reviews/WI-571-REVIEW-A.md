# WI-571 — REVIEW-A rollup

Compiled by the supervising session (2026-09-02) from the round files under
`docs/reviews/wi-571-the-snapshot-copies-only-what/`, time-ordered, governing
line last. All three rounds were mechanized (the loop's review policy at 1,
cross-family and family-alternating under the escalation policy); the verdict
gate requires this per-WI rollup and nothing in the kit writes it yet (the
verdict-carrier repair is queued), so it is compiled by hand.

### Supervisor note — NOT a round, does not govern

An independent read-only Opus pass over the first build confirmed the lane's
standing constraint held: no `docs/archive/last_approved/` file and no
registry Status cell was touched; every new test drives the scoped copy on a
tmp-tree scaffold. The three rounds each caught something real, and the
second caught a defect of exactly the class this row exists to close (a
demotion authorising a registry-wide copy) before it shipped. The refresh
was refused once on `doc-navigability` for a broken link in TRUNK's compiled
log — the supervisor's own approval-act ruling fragment had authored its
plan link docs-relative, so the compile rebased it wrong — fixed on trunk
before the merge, not on this lane.

### REVIEW-A — Round 2 — OPENAI-TERRA (medium) — tip 61180ab

Two MINORs: a refresh authorised solely by a `Status` move copied the scoped
registry but never wrote the prose stamp (the new contract requires the stamp
to name every copied registry and its authority), leaving a flip-only act
unauditable; and the reseal row's new triage text assumed a bare snapshot
would copy the LLR registry when both its rows are already Approved, so the
planned regeneration would copy nothing. Remedies: stamp every non-seed
refresh; name the intended registries with `--approves` in the reseal row.
(Full text: `002-REVIEW-A-61180ab.md`.)

VERDICT: CHANGES-REQUESTED findings=2

### REVIEW-A — Round 4 — OPENAI-TERRA (medium) — tip 0e12c51

One MAJOR: `_authorised_registries` treated every Status difference as an
approving flip, so an `Approved` → `Drafted` change on one SR authorised a
registry-wide copy that absorbed an unrelated approved-SR amendment (driven
on a tmp tree: `amendment_absorbed=True`). Remedy: authorise only an actual
approval transition (Drafted → Approved, or a new approved row) and add the
demotion-plus-amendment regression.
(Full text: `004-REVIEW-A-0e12c51.md`.)

VERDICT: CHANGES-REQUESTED findings=1

### REVIEW-A — Round 6 — ANTHROPIC-OPUS (medium) — tip 389e829

The rework verified; two MINORs, neither blocking: the named-scoping refusal
core (`resolve_registry` on an unknown name, `parse_approves` on a malformed
pair) has no direct regression test, only the happy path; and two functions
(`_authorised_registries` new at ~19, `copy_live` 19 → 21) exceed the
cognitive threshold without a `docs/complexity-baseline` row or re-stamp
(the sensor is dormant below DevStg-Impl, as the WI-552 close recorded).
(Full text: `006-REVIEW-A-389e829.md`.)

VERDICT: APPROVE findings=2
