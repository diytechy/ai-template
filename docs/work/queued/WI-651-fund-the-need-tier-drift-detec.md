+++
id = "WI-651"
title = "Add the need tier to the snapshot drift comparison and render a need section in the re-attestation brief (SR-178)"
workstream = "scripts"
specref = "docs/log.d/2026-09-26-owner-rulings-oi82-oi94.md"
sr_refs = ["SR-178"]
needs = ["WI-633", "WI-634", "WI-638"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

OI-91 ruled 2026-09-26: fund the detector. Approved SR-178 reports a recorded artifact whose text moved from its acceptance copy, "stakeholder needs included"; `baseline_snapshot.SNAPSHOT_TIERS` excludes the need tier, and the re-attestation brief (`trace.py --approve modified`) renders no need section, so OI-85 and OI-86 were each found by hand. OI-85's ruling deferred exactly this pass; the parked note is in `baseline_snapshot.py`'s approval predicate docstring.

IN SCOPE: add the need tier to the snapshot comparison (row-level refusal then covers it too, spine map D18), render a need section in the re-attestation brief with the word-level diff the other tiers get, and route a drifted approved need through the same `intake.py snapshot --reattests` re-anchor. The owner's note from OI-86 applies: a need whose meaning did not change is re-anchored through the amendment adjudication, not re-signed by the owner. Sequenced after the assumption tier's build (OI-91's recommendation).

Extended 2026-09-27 (arbitration ruling 15(i) of `docs/reviews/2026-09-26-wave3/ARBITRATION.md`): the stakeholder tier (`STK-ID` in the needs file) is absent from `SNAPSHOT_TIERS` too, so the C1 sitting's approval of STK-01..STK-04 is recorded only in the snapshot stamp's ref text and not in `docs/archive/last_approved/acts.toml`'s row list (IF-220). Add the stakeholder tier with the need tier, with a regression showing an approved STK row recorded by the act ledger.

## Done-when

- A drifted approved need is reported by the snapshot comparison and appears in `trace.py --approve modified`'s brief with its diff; a test drives both on a scaffold.
- `intake.py snapshot` refuses an unnamed drifted need as it does the other tiers, and `--reattests SN-###` re-anchors it.
- The commit bar passes.
