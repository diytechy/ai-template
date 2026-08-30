## 2026-08-30 — WI-508 review round 011 (gpt-5.6-sol): eight findings dispositioned, two by running the kit's own rules against the fix each asked for

Deferred open items: none — the two generator/instrument gaps below are
carried to the owner in the supervisor's decisions file, not owed a ruling.

Round 011 (`docs/reviews/wi508-architectural-remap/010-REVIEW-A-5175065.md`,
strong cross-family route) returned 3 BLOCKER / 4 MAJOR / 1 MINOR. Each was
either driven or located; none was accepted or rejected on reading alone.

**1–3. The blind-derivation brief was not committed before the returns; both
teams saw the harness context; Team A's census is 25 not 24 — OUT OF THIS
LANE'S DIFF.** `git diff --stat 7e2d3f82..HEAD` touches 27 files and none of
`docs/plans/2026-08-25-blind-minimal-map-*.md`; slice 2 landed on trunk on
2026-08-25 (`docs/log.md`, "WI-508 slice 2") and disclosed the contamination
itself ("Blindness was NOT total and both teams disclosed it… a future run of
this instrument must strip the harness context"). A rerun is a new row, not a
rework of a close whose diff does not contain the derivation. The census
arithmetic (25 modules with the zero-SR F5) is a real MINOR against the
2026-08-25 record and is carried to the owner's list.

**4. The `last_approved` snapshot must keep `580df781`'s `Approved` for
TC-199/TC-200 — REFUTED BY THE KIT'S OWN INTEGRITY RULE, driven.** The fix
was applied exactly as asked (`git checkout 580df781 --
docs/archive/last_approved/docs/test/test-cases.toml`, live left `Drafted`)
and `trace.py --strict-integrity` then reports
`FINDING (integrity): docs/archive/last_approved/docs/test/test-cases.toml is
NOT byte-identical to docs/test/test-cases.toml in this commit — the snapshot
is the record of what a human blessed, so it may only ever be written by
copying the live file (intake.py snapshot)` — `integrity=1
approval-record=1`, a red `registry-integrity` step at the merge slot. The
kit's rule is snapshot == live, and `intake.py --root . snapshot` on this
tree is a byte-for-byte no-op (round 010's record), so the committed snapshot
IS the kit-written one. Reverted to the committed state. Two independent
reviewers have now read §4 as "written only by the approval act"; the
instrument reads it as "always equal to live". The instrument decides the
bar; the wording tension is the owner's.
<!-- fig: cmd="git checkout 580df781 -- docs/archive/last_approved/docs/test/test-cases.toml && python project-trajectory/scripts/trace.py --strict-integrity" rev=892ee28f -->

**5–6. Drop `SR-163` from TC-199/TC-200's `verifies` — REFUTED BY THE ORPHAN
RULE, driven.** Applied (`verifies = ["LLR-203"]` / `["LLR-204"]`):
`trace.py --strict` moves from `orphans=2` to `orphans=3` with
`FINDING (orphan): SR SR-163 has no test (TC)` — the one rung the ladder is
held on, raised by one. A `Drafted` TC is non-evidence by definition, which
is what the round-1 rework chose and the archived Deliverable now states in
so many words; the false SR-163 green the reviewer fears cannot arise while
the rows stay `Drafted`, and re-approving them is nobody's act in this lane.
Reverted.
<!-- fig: cmd="python project-trajectory/scripts/trace.py --strict" rev=892ee28f -->

**7. `docs/stage`, `PROJECT_STATE.html` and the generated status block are
stale on the lane — TRUE, AND THE REFRESH'S JOB.** A work branch never
commits a generated artifact; `integrate.py refresh` runs `trunk_step --regen`
(derived-stage, trajectory, status, open-items, component-view, the two
references) BEFORE its bar, on the merged tree. The refresh that reached the
bar earlier today failed only on `approval-fresh`, since fixed (`085de8de`),
with every regen step green.

**8. Hand-authored `docs/status.md` still narrates this lane as OPEN and
calls LLR/TC blessing the owner's act — TRUE, TRUNK-OWNED.** `status.md` is
the trunk lane's file (§5.2); the supervising session removes the closed-lane
recap and points approval authority at `docs/process.toml` in its own trunk
commit after this branch merges, so the edit cannot conflict with the
refresh's regenerated block.

**Deviations from spec:** none — a review-round record; the two trial edits
above were reverted before this commit, and the tree is byte-identical to
`892ee28f` outside this fragment.

**Byte deltas on budgeted files:** none touched.

**pytest totals:** smoke tier on this tree **1378 passed, 6 skipped in 24.63 s**; the budget read **28.7 s vs 60 s -> within**; `check_docs --stale`: 0 broken; `trace.py --strict-integrity` on the reverted tree: `integrity=0 approval-record=0`. (Round 012 asked for the commit bar on the record commit; here it is, run alone on the box.)
