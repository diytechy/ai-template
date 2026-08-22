## 2026-08-21 — The post-program owner session: the dial drops to Needs, three close items execute, two campaigns and two briefs mint

Deferred open items: none still owed — SUPERSEDED 2026-08-22: this session
deferred the stale-cell repair route and the Consumes-owner reading (53
and 54 in the OI space, named off the declaration line so the parser
reads the live state); the owner ruled both the next day — (b)+(d) and
(a) respectively — and the execution rows are queued. The first was
updated in place before ruling (the dial change moved its recommendation
to the tracked-repair route); the second was minted this session to give
the wi455 lane's blocking question the row it had lacked since 2026-08-20
(the OI-41 founding class, corrected).

The owner's session, in order:

- **WI-473 ruled complete** ("no preference, move to complete"): closed to
  `docs/work/complete/` with the supersession recorded in the Deliverable —
  the floor shipped, refuted C-01's framing, seeded OI-51, and was then
  deliberately deleted by the program its discovery produced. Completion
  records work done, not perpetual existence.
- **The approval dial drops to `DevStg-Needs`** (the owner's own edit to
  `docs/process.toml`, committed here): only the Needs tier is human-held;
  SR/LLR/TC approval and amendment proceed under ordinary review. Driven:
  `ratification_through` reads `DevStg-Needs`, `human_holds` True only at
  Needs. Declared-policy staleness sweep per the session protocol:
  CLAUDE.md's "every spine tier is human-held" paraphrase now points at the
  dial instead of restating it; status.md's two "the sitting's act"
  predicates re-worded; OI-53's recommendation updated in place.
- **`docs/process.toml` dropped from `DECLARED_INPUTS`** (owner ruling,
  amending plan §2): the derivation never read it, and the real cost of
  over-inclusion was a red commit bar after every policy-dial edit — not
  the "milliseconds" the original comment argued. Pinned by
  `test_process_toml_is_NOT_an_input`; the two fingerprint tests that used
  it as their example input re-pointed at a real input; `docs/stage`
  regenerated under the new definition; plan §2 carries the dated
  amendment.
- **PB-002 re-measured on the live pair** (its `fig:` named the deleted
  `derive_gate`): 6.79/6.82/6.93 s over three warm runs for
  `derive_stage.py --check` + `gen_trajectory.py --check`, median 6.82 s —
  within noise of the pre-unification 6.46 s, ~3x headroom kept.
  <!-- fig-ok: the row's own fig: marker carries cmd+rev -->
- **The ratification→approval rename ruled** ("ratification holds a weight
  the semantics here don't need") and minted as **WI-499** — a REVIEWED
  campaign in the WI-498 sweep's proven shape, records untouched (the
  slice-5 recovery's reverted-hunks lesson written into the spec), the
  adopter-facing dial key riding the WI-493 migration precedent. Not an
  OI: the owner ruled the direction in session; the row records it.
- **WI-500 minted** — the test-evidence carrier that makes `DevStg-Release`
  reachable, which the ruled plan named as "its own row" and which had no
  id (the same announced-but-rowless class).
- **OI-54 minted** — the Consumes-`owner` reading question blocking the
  wi455 lane's last half, with options and a recommendation ((a),
  provider-as-owner with the consumers set carrying WI-469's verified
  modules).

Watermark `WI` 498 → 500 and `OI` 53 → 54 via `trace.py --bump-ids`;
surfaces regenerated; commit-bar figures in the commit body.
