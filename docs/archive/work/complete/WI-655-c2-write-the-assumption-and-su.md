+++
id = "WI-655"
title = "C2: write the assumption and surrogate rows, and each boundary interface's bridged_by or coincident"
workstream = "requirements"
specref = ""
needs = ["WI-643", "WI-616"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Deliverable

Built by one builder in two commits with three Codex Sol rounds (wave-5
arbitration rulings 26 to 30 and 32), SOUND at 063e4225 plus SR-174's
crossing, which the coordinator set at integration (ruling 32). The C2 step
of the assumption-tier plan (§11), warn-only, with the arms off.

- **The assumption registry** holds DA-001 to DA-015 and SUR-001 to
  SUR-003, all Drafted, each landing on a declared crossing (`effect_at`).
  The surrogates emulate EXT-005, EXT-001 and EXT-006, each with its
  fidelity DA. DA-011 carries the spine map's D5 premise (a sampled new
  reader's result generalizes beyond the sample) and is evidenced by the new
  Drafted inspection case TC-279. Its result reads NOT YET TAKEN.
- **Every SR carries `da_refs` or `coincident`.** 78 are recorded
  coincident with a reason. The others cite the DAs they rest on. Among
  WI-616's premises listed for C2, "every commit", "every finished branch",
  "never meets that refusal", "each part" and "3.11+" became DA-004,
  DA-013, DA-014, DA-011 and DA-012.
- **The `boundary_refs` re-point** that the C1 package deferred to C2: 72
  SRs moved off B-05, to B-09 (a run-time observable the kit reports) or
  B-10 (an exchange with a runner). Each SR lists every crossing its approved
  text names, including B-01 for governed writes (SR-156, SR-170, SR-174,
  SR-215 and others).
- **Every boundary interface** carries `bridged_by` (9) or `coincident` (34).
- **The bridging report** (WI-654's SR-211 advisories) reads 0: 43 with the
  DA rows and no interface cells, 0 after.
  fig: `python project-trajectory/scripts/trace.py --root .`, lines containing "realizes boundary crossing", at the landing tree.

Remaining advisories, each named. Three SRs span frames because their
approved text names both (SR-139, SR-146, SR-148); splitting them would
amend approved requirement text. B-11 is named by no requirement, because
SR-151 and SR-152's rationale argues B-05 and DA-005 carries the
hosted-runner premise. SN-040's only SR is argued as B-05 alone. There are
114 "declares no Form" advisories: `form` is approved content outside this
row's grant, and C3 or C4 takes it. SN-007 is not served by a derived
obligation, because no SR states that the bar is green before a change
lands; that is a need-coverage question for the owner.

## Context

The assumption-tier plan's step C2 (plan §11; the briefing's step 2; the C1 package's deferrals): write the DA and surrogate rows derived from the person-facing needs, each a new Drafted claim; give every SR `da_refs` or `coincident`; re-point the SRs' `boundary_refs` to the redrawn frame's bundles (the C1 package defers that to C2 so each SR is touched once); and give each boundary interface its `bridged_by` or `coincident`. Warn-only, arms off. The mockup's eight DAs and three surrogates are the starting draft. SN-041's first acceptance sentence (a reader new to the code, spine map D5) becomes an assumption row with a sampled test here.

Filed 2026-09-26 as the condition of OI-94's ruling: the owner accepted making SR-211's bridging report vacuous "as long as" queued work returns to close the gap. C2 was a plan step with no queued item until now. C3 (evidence) and C4 (activation) follow it and are not filed here.

## Done-when

- The assumptions registry holds the drafted DA and surrogate rows, each landing on a declared crossing (`effect_at`).
- Every SR carries `da_refs` or `coincident`; every boundary interface carries `bridged_by` or `coincident`, and the bridging report (WI-654) is clean or each remaining advisory is named in the log.
- The rows go to adjudication through the normal route; nothing is approved by this item; the commit bar and `trace.py --strict` pass.
