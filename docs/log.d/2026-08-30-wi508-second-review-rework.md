## 2026-08-30 — WI-508 rework: SR-163's remaining verification is unscheduled

The second REVIEW-A round returned two findings against WI-508's archived
Deliverable. The record assigned `SR-163`'s still-undelivered file→requirement
join and shipped-universe coverage to `WI-519`/`WI-520`/`WI-521`, but those WIs
have empty `sr_refs` and none scopes `SR-163`, `LLR-203`, or `LLR-204`. The
Deliverable now records the remaining acceptance criteria as **unscheduled**;
no ownership is inferred from the fact that those three WIs were filed by the
same remapping program.

The record also now distinguishes the formal links from evidence. `TC-199` and
`TC-200` still list `SR-163` in `verifies`, but their `Drafted` status makes
those direct links non-evidence. Their cited tests exercise only the delivered
arms named by `LLR-203` and `LLR-204`, not `SR-163`'s complete join and universe.

The focused document check also found the archived slice-6 record targeting a
not-yet-compiled `docs/log.md` anchor. Its label already named the real branch
fragment, so the target now resolves to that `docs/log.d` source as well.

### Verification

- `python project-trajectory/scripts/trace.py --strict-integrity` passed. The
  broader `--strict` probe retains the branch baseline: `LLR-197`'s provenance
  finding and `SR-181`'s orphan arms; this record-only rework does not alter
  those unrelated rows.
- `python project-trajectory/scripts/check_docs.py --root . --stale` passed with
  no broken links.
- With Git's installed `sh.exe` added to `PATH`, both the smoke tier and its
  enforced wall-clock budget passed.

Exact results and the unfiltered suite remain for the post-checkpoint close run,
where the measurements can cite a committed revision.

Deferred open items: none — this rework records the existing unscheduled gap;
it neither allocates new work nor requests a new ruling.
