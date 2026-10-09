## 2026-10-09 (overnight leg 01) — Coordinator: WI-870 and WI-853 built on their lanes; Codex limit

Resumed from [handoff-2026-10-09b-overnight-coordinator.md](../handoff-2026-10-09b-overnight-coordinator.md).
The next resume map is [handoff-2026-10-09-leg01-coordinator.md](../handoff-2026-10-09-leg01-coordinator.md).

**Claimed** WI-870 and WI-853 under one scoped unpause (`0b832cc2`, restored
byte-identical in `c5076d62`). The first claim attempt was refused because
status.md's resume list named both ids; the list now names the rows by
subject (`ad4e72e8`).

**WI-870** (lane `wi-870`, tip `e72e3a2d`).
- **Built:** a kit-builder (Opus) put one strict review VERDICT-line reader,
  `review_line`, in `kitlib.sitting`. The merge gate and the filing boundary
  both read through it.
- **The shared per-line reader** refuses a duplicated field.
- **PROCESS.md's review block** teaches the one machine line (D-001).
- **Re-run by the coordinator:** 241 passed; smoke 2305 passed, 2 skipped,
  enforce 37.5 s (within 60).
- **Spine:** Terra amended LLR-046, LLR-207, LLR-310, LLR-313, TC-083,
  TC-327, IF-046 and IF-287. It wrongly dropped `_keyword_count_refusal`
  from LLR-310's `code_symbol`, which was restored. Sitting 001 judged all
  six approved rows MEANING and re-attested them.
- **Sol:** the full-lane review died on the Codex usage limit.

**WI-870's migration check** (the spec's Done-when). Every adjudication verdict
under `docs/reviews/` reads as before. 86 review files now read as unparseable
and were NOT rewritten (D-002). The causes are a `Verdict:` header beside the
machine line, trailing tokens, or several VERDICT lines in one multi-round
log. The files:
- **Lane rounds:**
  - `1-g3-WI-272-230f/011-` and `015-REVIEW-A`;
  - `wi-579-…/022-` and `036-REVIEW-A`;
  - `wi-586-…/010-REVIEW-A`;
  - `wi-589-…/011-REVIEW-A`.

  Their four rollups regenerate at the landing.
- **Other lane files:**
  - `wi-685-…/001-ADJUDICATE-fe96ec6` (an `anchors=` token);
  - the REJUDGE files of wi-765, wi-777 and wi-796.
- **Flat files:**
  - `012`, `014`, `017`, `019`, `023`, `036` and `130-REVIEW-A`;
  - `077-CRITIQUE` and `101-GROUNDING`;
  - `2026-09-27-wave5/sol-tc055`, `retier-v2/ROUND-2-SOL-TERRA` and
    `wi451-retier/ROUND-2-SOL`.
- **`WI-<n>-REVIEW-A.md` files** for WI-277, 280, 346, 355, 366–381, 383–389,
  391–398, 401–406, 409–412, 414, 442, 453, 454, 535, 538, 543, 547–550,
  552, 553, 555, 563, 566, 568, 569, 571, 573 and 575.

**WI-853** (lane `wi-853`, tip `ea348d61`).
- **Built:** a kit-builder made `plan_coverage.py --findings` read a review
  verdict. `finding_clauses` is the shared F# step. An exclusion that cites a
  dispute verdict must cite an accepted DISMISS of that finding.
- **Re-run by the coordinator:** 112 passed; smoke 2308 passed, 2 skipped,
  enforce 36.3 s.
- **Spine:** Terra amended LLR-069, TC-069 and IF-046. The sitting is held
  until WI-870 lands, so act seqs stay unique.
- **Sol:** the review died on the usage limit.

**Codex limit** at 02:23. Reset 06:13, so the handoff carries
`Resume-not-before`.

**Full suite** at `c5076d62` (trunk's tip; a detached worktree, fixed basetemp under
`review-tmp/2026-10-09-leg01/`, deleted once recorded): **5492 passed, 17 skipped, 0
failed** in 762.6 s.

**Decisions:**
- `wi-870.toml` D-001 to D-003;
- `wi-853.toml` D-001 to D-003;
- `coordinator-2026-10-09-leg01.toml` D-001 to D-003.

All await the owner's confirm or overrule.

Deferred open items: none — no item was deferred this leg.
