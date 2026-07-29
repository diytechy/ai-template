+++
id = "WI-071"
title = "Phase gate cadence + phase-vocabulary adoption"
workstream = "docs"
needs = ["WI-053"]
order = 70
+++

## Deliverable

Docs only (FB1+FB2): PROCESS_OPTIONS 'Phase cadence' extended with the gate cadence stated once - mid-phase WI slices end at the commit bar (hook floor + test command + check_docs --stale), the full check.py --gate <gate> runs once at phase close (CI runs it on every push regardless), and test-impact selection is rejected in favor of the declared stack.ini [tiers] smoke tier. The session-protocol skill 'End green' now distinguishes the commit bar from the gate bar (neutral source edited, both .claude/.agents fan-out copies re-synced byte-identical); the root README's registry map adopts the phase vocabulary pointing at the PROCESS_OPTIONS home. No spine change, no re-attestation impact.
