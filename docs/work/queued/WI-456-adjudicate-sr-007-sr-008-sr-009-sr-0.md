+++
id = "WI-456"
title = "adjudicate: SR-007, SR-008, SR-009, SR-010, SR-011, SR-020, SR-022, SR-024, SR-032, SR-033, SR-034, SR-036, SR-043, SR-111, SR-113, SR-133 - ratified/routed cell(s) amended on merged trunk 1539f07..7674e4a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-007", "SR-006", "SR-009", "SR-010", "SR-011", "SR-020", "SR-022", "SR-024"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
+++

## Context

> **Two of the rows in this row's title no longer exist (2026-08-15).** `SR-008`
> and `SR-133` were DEMOTED to the design tier and deleted — SR-008's obligation
> into `LLR-008` under `SR-007` + `SR-006`, SR-133's into `LLR-141` under
> `SR-006` + `SR-156`. Both were `Verified`, and both demotions deliberately
> override that attestation under the owner's 2026-08-15 ruling. So their rows
> in the amendment table below are HISTORY, not an adjudication still owed: what
> this WI must judge for those two is whether the DEMOTION moved scope, on the
> receiving rows, not whether the boundary-ref edit did. The title is left
> unchanged on purpose — editing it renames the file and re-dates the clock.
> Forwarding and reasoning: `docs/log.md`, entry `2026-08-15b`.

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Ratified and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-007 `Boundary-Refs`: '' -> 'B-05'
- SR-007 `area`: 'Declared stack profile' -> ''
- SR-008 `Boundary-Refs`: '' -> 'B-05'
- SR-008 `area`: 'Declared stack profile' -> ''
- SR-009 `Boundary-Refs`: '' -> 'B-05'
- SR-009 `area`: 'Conditional scaffold profiles' -> ''
- SR-010 `Boundary-Refs`: '' -> 'B-05'
- SR-010 `area`: 'Scaffold generation' -> ''
- SR-011 `Boundary-Refs`: '' -> 'B-05'
- SR-011 `area`: 'Scaffold generation' -> ''
- SR-020 `Boundary-Refs`: '' -> 'B-01;B-04'
- SR-020 `area`: 'Git hooks' -> ''
- SR-022 `Boundary-Refs`: '' -> 'B-05'
- SR-022 `area`: 'Vendored-doc drift' -> ''
- SR-024 `Boundary-Refs`: '' -> 'B-05'
- SR-024 `area`: 'Permutation case gen' -> ''
- SR-032 `Boundary-Refs`: '' -> 'B-05'
- SR-032 `area`: 'Onboarding + dev-setup' -> ''
- SR-033 `Boundary-Refs`: '' -> 'B-05'
- SR-033 `area`: 'Release checklist' -> ''
- SR-034 `Boundary-Refs`: '' -> 'B-05'
- SR-034 `area`: 'Portability' -> ''
- SR-036 `Boundary-Refs`: '' -> 'B-05'
- SR-036 `area`: 'Scaffold generation' -> ''
- SR-043 `Boundary-Refs`: '' -> 'B-04'
- SR-043 `area`: 'Unattended coordinator' -> ''
- SR-111 `Boundary-Refs`: '' -> 'B-05'
- SR-111 `area`: 'Scaffold generation' -> ''
- SR-113 `Boundary-Refs`: '' -> 'B-05'
- SR-113 `area`: 'Onboarding + dev-setup' -> ''
- SR-133 `Boundary-Refs`: '' -> 'B-05'
- SR-133 `area`: 'Gate harness' -> ''

Outcomes (§A5.2): flip rows back to Verified where no scope moved
(per the declared ratification level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-007 [project-trajectory/scripts/check.py :: load_profile] tests: (see TC-007) — Stack profile loader
- LLR-008 [project-trajectory/scripts/check.py :: load_profile] tests: (see TC-008) — Profile validation
- LLR-009 [project-trajectory/scripts/bootstrap.py :: select_skills/matches_scope] tests: (see TC-009) — Conditional profile seeding
- LLR-010 [project-trajectory/scripts/bootstrap.py :: MAPPING/main] tests: (see TC-010) — Scaffold writer
- LLR-011 [project-trajectory/scripts/bootstrap.py :: write/--force + write_kit_version] tests: (see TC-011) — Idempotent write + kit-version stamp
- LLR-020 [project-trajectory/hooks/pre-push :: pre-push] tests: (see TC-020) — Pre-push outgoing scan

### Knowledge packs the touched components declare (read before building)
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-001 (Provides) scripts/trace <-> scripts/check: trace.py CLI: --strict-integrity exits 1 on a duplicate/malformed id or mis-columned row; --strict adds orpha…
- IF-002 (Provides) scripts/check_docs <-> scripts/check: check_docs.py CLI: --stale exits 1 on a broken intra-repo link, a missing PROJECT-VISION tag, or a generated …
- IF-003 (Provides) scripts/check_flows <-> scripts/check: check_flows.py CLI: --no-placeholders; exits 1 when an authored runtime-flow diagram violates its structural …
- IF-004 (Provides) scripts/check_perf <-> scripts/check: check_perf.py CLI: --tier T exits nonzero when a measured metric regresses beyond its declared PB budget tole…
- IF-005 (Provides) scripts/check_privacy <-> scripts/check: check_privacy.py CLI: --repo scans the tree and exits 1 on a secret (always-on floor) or, under docs/privacy-…
- IF-006 (Provides) scripts/check_stubs <-> scripts/check: check_stubs.py CLI: --strict exits 1 on a stub/NotImplemented/pass-only public symbol at the declared gate; c…
