Deferred open items: OI-98, OI-105

## 2026-10-04 — Wave-14 coordinator: the context guard and the lane-lifecycle program

Roles as the wave-13 handoff states them: Claude Opus builds (kit-builder,
medium), GPT Terra (medium) authors spine rows, Codex 6.1 Sol (high) reviews,
independent Claude Opus agents adjudicate. OI-98 and OI-105 stay the owner's.

- **One scoped unpause** (`d15f33f8` delete, seven claims, `8b1103b5`
  byte-identical restore) claimed the ready batch: WI-822, WI-797, WI-803,
  WI-806, WI-818, WI-821, WI-796. The deletion and the restore each carry the
  regenerated `open-items.html`, which renders the pause.

### WI-796: TC-055 RECORDED pass, two judge findings refuted

Six Codex Luna (high) judges over 284 tiles at `5fb0fc74` (390/1280/1680 px x
light/dark, four tabs): four APPROVE, two CHANGES-REQUESTED (T5 at 390 light:
an amber focus ring; T2 at 1680 dark: 31 SN blocks on the What tab's root). An
independent Opus adjudicator refuted both against the render: a browser probe
focused every node in both themes and found no amber stroke (weakest ring
4.76:1), and the What view starts collapsed as LLR-099 requires. Recorded pass
with that provenance (`docs/decisions/wi-796.toml` D-001, high risk). Follow-ups
for a new row: binding notes on rubric anchors T2 and T5 (and the dead SR-089
cite), the rendered Retired tab missing from the shot matrix, and the judges'
prompt given LLR-099's and LLR-105's scope lines.

### WI-797: the kit glossary ships

`project-trajectory/GLOSSARY.md` (kit-owned, scaffolds to `docs/glossary.md`)
carries the note's glossary reconciled with A1, a strength entry, and Planned
labels on unbuilt machinery; PROCESS.md links to it in one sentence, because it
has no lane-lifecycle section to rename (`docs/decisions/wi-797.toml` D-001).
Sol round 1: one MAJOR (the losing drafter's concession is a second
independence exception, Q-5), confirmed and fixed; round 2 SOUND at
`35ee2d87`. No spine rows changed, so no act. RESYNC re-anchored at the
landing's parent.

### WI-803: the plan gate (act seq 32)

`plan_coverage.py` becomes a gate: a SINGLE run's clauses are the item's
Done-when (`D#`) and open findings (`F#`), each covered or excluded with a
reason; it also diffs the item's SRs (cite-only) and their TCs. Sol round 1
raised two MAJORs: an excludable item SR (confirmed, fixed) and DUAL gaps kept
as payload, which the builder disputed. An independent Opus adjudicator ruled
(a): an unexplained DUAL gap fails too; the fixtures' report bytes are
unchanged, only the exit code and the FAIL lines move. Sol round 2: one MINOR
(a bold `Excludes:` label), fixed. GPT Terra amended LLR-069, TC-069, IF-060,
IF-152, IF-153 and IF-242. The in-lane adjudicator returned LLR-069, TC-069
and IF-153 with exact texts, added IF-161's consumer, found two untested
behaviours (tests added, each red under its mutant), then re-attested LLR-069
and TC-069 as MEANING, act seq 32, the verdict and the act in separate commits.
WI-804's Done-when drops the `Excludes:` line it would have added. Smoke
2054 passed (21.0 s vs 60 s).

### In flight at the close: WI-822 and WI-806

Both lanes were built and taken through review and in-lane adjudication rounds,
and neither has taken its act yet.

- **WI-822, the context guard.**
  - Sol round 1 raised 6 MAJOR and 4 MINOR. Sol round 2 raised 2 MAJOR and 2
    MINOR. All are fixed.
  - A real Claude Code 2.1.289 compaction transcript came from a local Haiku
    probe (coordinator D-012) and is the recorded fixture.
  - GPT Terra drafted SR-229, SR-230, LLR-300, LLR-301 and TC-315 to TC-318, and
    the interface seams IF-271 to IF-275.
  - The coordinator removed IF-276, which consumed its own state, and kept
    `external:agent CLI` rather than a new external party, which would have
    changed the frame.
  - The in-lane adjudicator returned all eight new rows with exact fixes, after 14
    mutation probes; five mutants survived. The builder then added the tests that
    kill them.
  - Terra's round 3 applied the fixes and minted IF-277 to IF-280. It stopped at
    the Codex plan limit (reset 2026-10-05 02:34), uncommitted.
- **WI-806, spine text before the act.**
  - Built, and rebased onto trunk after a merge refresh tripped registry
    integrity.
  - Sol REVIEW-A raised a BLOCKER and a MAJOR, now with the builder.
  - Luna REVIEW-B raised a MAJOR, which the coordinator refuted with evidence, and
    a MINOR, which is the builder's deliberate all-parents design. Both are for
    the adjudicator to rule.
  - The adjudicator returned all four rows with exact fixes.
  - SN-029's acceptance and why cells become untrue at the landing, and are filed
    for the owner then.
- **WI-818 and WI-821** stay claimed with no lane cut.
- **Why the session stopped:** at about 41% of its context, with both lanes
  needing several Codex rounds and Codex out for 2.5 hours, it closed out by the
  guard's own rule.

The exact owed steps per lane and the corrections learned are in
[the wave-14 handoff](../handoff-2026-10-05-wave14-coordinator.md).
