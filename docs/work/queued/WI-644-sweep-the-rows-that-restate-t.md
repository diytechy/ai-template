+++
id = "WI-644"
title = "Sweep the rows that restate a reversed sitting-2 ruling (LLR-051/056/057/124/139, SR-151/152/175, IF-041)"
workstream = "requirements"
specref = "docs/plans/2026-09-25-c1-sitting-package.md#22-rows-elsewhere-that-restate-a-reversed-ruling"
sr_refs = ["SR-151", "SR-152", "SR-175"]
needs = ["WI-643"]
buildtier = "medium"
safety_class = "spine"
priority = 4
+++

## Context

The C1 sitting reverses rulings 13k, 13n and 13u, the REL-003 reading and part of the hosted-CI cut (package §2). Nine rows still state them: five design rows call the generated views 'not a system output', three requirement rationales argue from REL-003 or the cut, and IF-041's note says invoking an agent CLI crosses no boundary. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each of the nine rows is amended as a Drafted change stating the redrawn frame (the read crossing, the model-runner crossing, hosted CI as a party), through the ordinary adjudication route.
- IF-041's tie-back to the model-runner crossing is left to the interface-allocation work, not done here.
