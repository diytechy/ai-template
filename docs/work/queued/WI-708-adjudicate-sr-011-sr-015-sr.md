+++
id = "WI-708"
title = "adjudicate: SR-011, SR-015, SR-024, SR-031, SR-033, SR-040, SR-111, SR-112, SR-129, SR-147, SR-149, SR-174, SR-177 - approved/routed cell(s) amended on merged trunk 83d866c..5934f4c (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-011", "SR-015", "SR-024", "SR-031", "SR-033", "SR-040", "SR-111", "SR-112"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-011", "SR-015", "SR-024", "SR-031", "SR-033", "SR-040", "SR-111", "SR-112", "SR-129", "SR-147", "SR-149", "SR-174", "SR-177"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-011 `Coincident`: 'The need asks for a re-run that costs the adopter none of its own edits; a re-run leaving each existing file byte-uncha…' -> "The need asks that a re-sync onto an existing repository never clobber the repository's own files; a re-run that leaves…"
- SR-011 `Rationale`: 'Realizes SN-001 (safe drop-in onto an existing repo) and SN-007 — an adopter picking up kit updates must not lose their…' -> "Realizes SN-001 (a re-sync onto an existing repo never clobbers the repo's own files) — an adopter picking up kit updat…"
- SR-011 `SN-Refs`: 'SN-001;SN-007' -> 'SN-001'
- SR-015 `Coincident`: 'The need asks for a budget row a reviewer can trace to what it constrains; each unresolvable reference reported is that…' -> ''
- SR-024 `Coincident`: 'The need asks for dimensional coverage generated rather than hand-listed; the expanded case set is that output, whole.' -> ''
- SR-031 `Coincident`: 'The needs ask for one declared value per policy dial, read the same way by every enforcer; the enforcers agreeing is th…' -> 'The need asks for every policy dial in one hand-edited, machine-read file whose shape is a checked contract because two…'
- SR-031 `Rationale`: 'Realizes SN-004 (policies drive the gate) and SN-005 (one source, every enforcer reads it the same way). Partition with…' -> 'Realizes SN-028 (every policy dial in one home, a single hand-edited, machine-read file, whose two readings are pinned …'
- SR-031 `SN-Refs`: 'SN-004;SN-005' -> 'SN-028'
- SR-033 `Coincident`: 'The need asks for a release gate whose warn-tier budgets reach a reader; the emitted checklist listing each budget is t…' -> ''
- SR-040 `Coincident`: 'The need asks for an unattended run whose per-phase sessions start as declared; routing each phase through its declared…' -> 'The need asks that the owner configure several model families selected per job, so that work benefiting from an indepen…'
- SR-040 `Rationale`: 'Realizes SN-006 and the dissolved edge expectation that an unattended run never blocks on a prompt, at launch or mid-ru…' -> 'Realizes SN-026 (several model families selected per job, so that work benefiting from an independent second opinion is…'
- SR-040 `SN-Refs`: 'SN-006' -> 'SN-026'
- SR-111 `Coincident`: 'The needs ask for an adopter able to pick up kit updates from a known base; the stamp recording the kit commit a scaffo…' -> ''
- SR-111 `Rationale`: 'Realizes SN-007 — without a recorded origin an adopter cannot tell which kit version they are on, so a re-sync degrades…' -> "Contributes to SN-001's re-sync clause (a re-sync onto an existing repo never clobbers the repo's own files) by supplyi…"
- SR-111 `SN-Refs`: 'SN-001;SN-007' -> 'SN-001'
- SR-112 `Coincident`: 'The need asks for a repository paying only for what it uses; one neutral skill source with a checked, generated per-age…' -> 'The need asks that AI agents and humans work from the same playbook. The skills are part of that playbook, and each age…'
- SR-112 `SN-Refs`: 'SN-012' -> 'SN-005'
- SR-129 `Coincident`: 'The needs ask for a registry whose cells survive a change of representation; a conversion preserving every cell, and re…' -> ''
- SR-129 `SN-Refs`: 'SN-002;SN-012' -> 'SN-025'
- SR-147 `Coincident`: 'The needs ask for a spine a machine can verify; one machine-parseable representation, reached by a migration proven ove…' -> 'The need asks that the chain from need to test be mechanically verified, not manually asserted, with the strict check r…'
- SR-147 `SN-Refs`: 'SN-002;SN-012' -> 'SN-002'
- SR-149 `Coincident`: 'The needs ask for authored surfaces that stay honest to the current vocabulary; each retired tag reported with its file…' -> 'The need asks that a reader can trust the documentation: navigable and honest. A retired process tag surviving in a liv…'
- SR-149 `Rationale`: "Realizes SN-004 (the ladder's vocabulary is the one the project is held to) and SN-010 (docs stay honest). This check i…" -> 'Realizes SN-010 (a reader can navigate the documentation and trust it: navigable and honest). This check is a CONDITION…'
- SR-149 `SN-Refs`: 'SN-004;SN-010' -> 'SN-010'
- SR-174 `Coincident`: 'The needs ask for ids a reader can trust to name one thing; an identity allocated at most once and not re-issued after …' -> ''
- SR-174 `Rationale`: 'Identity allocation is its own decision, not a consequence of serialization: serializing the writer makes a COLLISION u…' -> 'Identity allocation is its own decision, not a consequence of serialization: serializing the writer makes a COLLISION u…'
- SR-174 `SN-Refs`: 'SN-008;SN-025' -> 'SN-025'
- SR-177 `Coincident`: "The need asks for a team seeing whether its parallel lanes pay off; the per-run utilisation reported from the run's own…" -> ''

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-011 [project-trajectory/scripts/bootstrap.py :: copy_kit_files/--force + write_kit_version] tests: (see TC-011) — Idempotent write + kit-version stamp
- LLR-015 [project-trajectory/scripts/trace.py :: analyze] tests: (see TC-015) — PB back-link resolution
- LLR-024 [project-trajectory/scripts/gen_cases.py :: main] tests: (see TC-024) — Permutation expander
- LLR-025 [project-trajectory/scripts/gen_skills_index.py :: main] tests: (see TC-025) — Skills index generator
- LLR-031 [project-trajectory/scripts/check_privacy.py :: _first_declared_line] tests: (see TC-031) — Shared declared-line parse
- LLR-033 [project-trajectory/scripts/gen_release_checklist.py :: main] tests: (see TC-033) — Release checklist generator

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-005 scripts/check_privacy -> scripts/check: stdout one line per leak: <location>: [<label>] <excerpt>, then one summary line naming the scan and the armed layers
- IF-148 scripts/check_privacy -> scripts/check: exit-code 0 clean or both layers off · 1 one or more findings in the tracked-file sweep
