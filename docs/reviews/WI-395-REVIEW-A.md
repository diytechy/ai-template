# WI-395 — REVIEW-A (2026-08-01)
Verdict: CHANGES-REQUESTED

1. [MAJOR] The close commit (`1fca2e87 close: WI-395 -> complete/`) moves the spec to
   a terminal folder but leaves its `specref` frontmatter set, and the repo's own
   strict trajectory check convicts the branch for it. Driven on branch HEAD:
   `check_trajectory.py --root . --strict` →
   `check_trajectory: ERROR - R-F WI-395: status=done but SpecRef
   'docs/concurrency-restructure.md#7-migration-plan-each-phase-is-itself-spine-class-solo-serial'
   is still set (a terminal WI clears the SpecRef and archives the spec to
   docs/archive/specs/ — the docs/specs/README.md lifecycle)` …
   `1 error(s) in docs/work.`, **rc=1**. The same command on trunk
   (`ConcurrencyTrainRewrite`) is `clean (400 work item(s), 370 done (92%), 17
   cancelled, graph acyclic).`, rc=0 — so the red is introduced by this branch's
   close, not inherited. This is bar-visible, not pedantry: the WI-396 branch
   review ran `check_trajectory --root . --strict` rc=0 as a close bar, and
   WI-391's REVIEW-A proved R-F by mutation on a terminal row (`restoring
   specref on the cancelled row gives ERROR - R-F WI-391`). Sibling completed
   specs carry no `specref` line (`grep -n "^specref"
   docs/work/complete/WI-{387,396}*.md` → no hits; only WI-395's hits at line 5).
   Remedy: delete the `specref = …` line from
   `docs/work/complete/WI-395-a-blockref-is-a-label-not-a-subscription.md`
   (the target is a shared design doc that stays un-archived by the R4 ruling,
   so clearing the pointer is the whole fix). The wording deliverable itself is
   unaffected by this remedy.

2. [MINOR] The new bullet describes the release path in the present tense —
   "a handed-back row is disposed by the dispatcher's handback-intake arm,
   which mints the disposition row when the handback merge lands" — but no such
   machinery exists on this tree: `project-trajectory/scripts/` has no
   `dispatch.py` and `grep -rn "handback-intake\|intake arm" …/scripts/*.py`
   returns nothing. The arm is a RULED design carried in the amended WI-388
   spec (queued; its 2026-08-01 amendment names the `## Handback`-triggered
   disposition mint verbatim) and the log's R3 Decisions entry commits to it
   ("Executes across WI-395 (wording) and WI-388 (the intake arm)"). Pointing
   at the arm IS the amendment's instruction, and the ruling's own grammar is
   present-tense ("transient by construction"), so **no wording change is
   owed**; recorded so the dependency is visible: the exemplar's promise
   becomes true only when WI-388 ships, and cancelling or re-scoping WI-388
   would re-open exactly the false-promise defect this row exists to close.

3. [MINOR] The repo-wide sweep for the retired sentence
   (`grep -rl "readiness is the scheduler" . --exclude-dir=.git`) leaves one
   live-doc carrier: `docs/concurrency-restructure.md:361` still states
   "readiness is the scheduler's to derive" inside the §7 Phase-2 design note —
   the WI's own SpecRef document. Out of the ruled scope by the amendment's own
   words ("This row is now ONLY the wording fix: correct the two byte-identical
   exemplar paragraphs"), so no remedy is owed from this WI; recorded from the
   sweep so nobody re-derives it. The other hits are quotations of the defect,
   not promises: `docs/backlog-plan-2026-08-01.md:162` (dated ruling brief —
   its present-tense "the repo's own exemplar text promises the opposite" is
   now stale but sits on a record surface), `PROJECT_STATE.html` (the WI-395
   title), the spec's own title, `docs/log.d/WI-395-blockref-wording-fix.md`,
   and `docs/reviews/WI-391-REVIEW-A.md`.

Verified — all driven by me on this tree, none inherited (the `docs/log.d/`
fragment was excluded as evidence for independence):

- **Pair edited together and byte-identical.** The branch diff carries one
  identical hunk in each file (old: "frontmatter key naming the reason;
  readiness is the scheduler's to derive, so / a second encoding…"; new: the
  presence-derivation + release-path bullet). Pre-images share blob
  `9269b786`, post-images share blob `0058dc13` (`git hash-object` both →
  `0058dc13ff3a048f7cf6434121c74bf858a7ea1c`), and `cmp` is clean →
  BYTE-IDENTICAL.
- **Sync guard green.** `/Users/diytechy/Documents/ai-template/.venv/bin/python
  -m pytest -q tests/test_dogfood_sync.py` → `25 passed in 0.08s`.
- **Wording matches the mechanism as built.** `schedule.py:752-753` is
  `if st == "queued" and wi["blockref"]: return "blocked",
  ["excluded:blocked:%s" % wi["blockref"]]` — presence-only, never resolving
  the target — exactly the bullet's "derives `blocked` from the key's
  **presence** — it never consults the state of what the key names".
- **Amendment compliance.** Option A not built: the diff touches four doc
  files and zero scripts. No human sweep named: the residual "reviewed edit
  deleting the `blockref`" path is a per-row edit with no cadence or owner —
  the same residual mechanism `docs/rulings-context-2026-08-01.md` §R3 itself
  states ("the only release today is a person … editing the file") — and the
  ruling's "owner surface remains fallback visibility" is not contradicted.
- **Deliverable filled and true.** The spec's Deliverable section matches the
  shipped hunk claim-for-claim, and its verification claim reproduces (25
  passed here too).

VERDICT: CHANGES-REQUESTED findings=3

---

## Round 2 (2026-08-01) — remedy verification
Verdict: APPROVE

Judging only the execution of the round-1 remedy, all re-driven by me on the
tree at `e1d8bffd` (`rework: WI-395 clears SpecRef at close (REVIEW-A finding
1, R-F)`):

- **Finding 1 remedied, exactly as prescribed and nothing beyond.** The rework
  diff on the spec is a single deleted line — `-specref =
  "docs/concurrency-restructure.md#7-migration-plan-each-phase-is-itself-spine-class-solo-serial"`
  — and `grep -n "^specref"
  docs/work/complete/WI-395-a-blockref-is-a-label-not-a-subscription.md` now
  returns nothing (rc=1), matching its completed siblings. Re-driven:
  `check_trajectory.py --root . --strict` → `check_trajectory: clean (400 work
  item(s), 371 done (93%), 17 cancelled, graph acyclic).`, **rc=0**, and the
  `R-F WI-395` line is gone (grep count 0). The WARNs that remain (WI-389 +
  WI-390 SpecRef-freshness, IF-055/IF-081, the two connectivity notes) are the
  same set trunk shows — pre-existing, not this branch's.
- **Blast radius of the rework is clean.** Three files only: the spec (the one
  deleted line), the log fragment (remedy note appended), and the round-1
  review file committed verbatim. The deliverable pair is untouched — both
  copies still hash `0058dc13ff3a048f7cf6434121c74bf858a7ea1c`, and
  `pytest -q tests/test_dogfood_sync.py` → `25 passed in 0.08s`. Working tree
  matches HEAD (`git diff --stat HEAD` empty) apart from this appended round.
- **Finding 3's disposition is recorded, not silently dropped.** The fragment
  (readable this round, round 1 being on record) states: "REVIEW-A finding 3
  (the retired sentence still readable at `docs/concurrency-restructure.md:361`)
  is recorded here, not edited: that doc is design history by the §A9.1
  standing rule." Consistent with round 1's no-remedy-owed stance, and the
  record now sits where the next reader of the close will look.
- **Finding 2 stands as recorded** — informational, no remedy owed; the
  exemplar's promise lands on WI-388, and that dependency is now visible in
  two surfaces (this review and the log's R3 Decisions entry).

No new findings.

VERDICT: APPROVE findings=3
