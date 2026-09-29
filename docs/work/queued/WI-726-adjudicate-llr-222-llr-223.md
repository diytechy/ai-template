+++
id = "WI-726"
title = "adjudicate: LLR-222, LLR-223, SR-015, SR-033, SR-111, SR-174, SR-177, SR-193, SR-223, SR-225, TC-220, TC-222 - approved/routed cell(s) amended on merged trunk e86cae4..3b87247 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-015", "SR-033", "SR-111", "SR-174", "SR-177", "SR-193", "SR-223", "SR-225"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-222", "LLR-223", "SR-015", "SR-033", "SR-111", "SR-174", "SR-177", "SR-193", "SR-223", "SR-225", "TC-220", "TC-222"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-015 `Delivered-With`: '' -> 'SR-157'
- SR-033 `Delivered-With`: '' -> 'SR-006;SR-049'
- SR-111 `Delivered-With`: '' -> 'SR-011;SR-036'
- SR-174 `Delivered-With`: '' -> 'SR-148;SR-170'
- SR-177 `Delivered-With`: '' -> 'SR-156;SR-170'
- SR-193 `AcceptanceCriteria`: 'A requirement citing one or more assumptions, each a declared assumption, is classified bridged; a requirement recordin…' -> 'A requirement citing one or more assumptions, each a declared assumption, is classified bridged; a requirement naming i…'
- SR-193 `Requirement`: 'The delivered harness shall report each system requirement that neither cites the assumptions its argument relies on no…' -> 'The delivered harness shall report each system requirement that neither cites the assumptions its argument relies on, n…'
- SR-223 `Delivered-With`: '' -> 'SR-154;SR-175'
- SR-225 `Delivered-With`: '' -> 'SR-139;SR-140'
- LLR-222 `Detail`: 'The requirement tier gains da_refs (a list, mapped to DA-Refs and listed in migrate_carrier.REF_COLS) and coincident (f…' -> 'The requirement tier carries da_refs (a list, mapped to DA-Refs and listed in migrate_carrier.REF_COLS), delivered_with…'
- LLR-223 `Detail`: 'sr_classification_advisories(srs, das) returns (failures, advisories). A non-empty DA-Refs whose every entry is a decla…' -> 'sr_classification_advisories(srs, das) returns (failures, advisories). A non-empty Delivered-With whose entries are dec…'
- TC-220 `Expected`: "Satisfies SR-193's acceptance: bridged, coincident, unclassified and both classified as stated; an undeclared citation …" -> "Satisfies SR-193's acceptance: bridged, joint, coincident, unclassified and contradictory combinations classified as st…"
- TC-220 `Method`: 'sr_classification_advisories and da_citing_srs called on in-memory rows. A requirement citing declared assumptions is b…' -> 'sr_classification_advisories and da_citing_srs called on in-memory rows. A requirement citing declared assumptions is b…'
- TC-222 `Expected`: 'Satisfies the cell-class clauses of SR-189, SR-190, SR-193, SR-194, SR-197, SR-198, SR-211 and SR-214: each traced cell…' -> 'Satisfies the cell-class clauses of SR-189, SR-190, SR-193, SR-194, SR-197, SR-198, SR-211 and SR-214: each traced cell…'
- TC-222 `Method`: "Driven on git repositories through the amendment classifier. Changing an approved row's traced cell — a requirement's D…" -> "Driven on git repositories through the amendment classifier. Changing an approved row's traced cell — a requirement's D…"

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-015 [project-trajectory/scripts/trace.py :: analyze] tests: (see TC-015) — PB back-link resolution
- LLR-033 [project-trajectory/scripts/gen_release_checklist.py :: main] tests: (see TC-033) — Release checklist generator
- LLR-121 [project-trajectory/scripts/bootstrap.py :: write_kit_version] tests: (see TC) — Kit-version stamp
- LLR-153 [project-trajectory/scripts/intake.py :: intake_after_merge/mint_gap_rows/parse_dispositions/next_wi_id/context_block/flip_verified] tests: (see TC-147) — The unified trunk-side intake mint + the context block + th…
- LLR-154 [project-trajectory/scripts/integrate.py :: integrate_one/_lane_bar_directives/_refresh_bar] tests: (see TC-148) — The merge slot's post-merge intake arm
- LLR-196 [project-trajectory/scripts/agent_common.py :: regenerate_index/per_turn_pace/per_turn_context] tests: (see TC-191) — Per-session fan-out utilisation telemetry, unaggregated

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-014 scripts/bootstrap -> external:downstream adopter: bytes the scaffolded template tree written under the destination root
- IF-015 scripts/agent_loop -> external:downstream adopter: git 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paused · 9 REVIEW-OWED …
