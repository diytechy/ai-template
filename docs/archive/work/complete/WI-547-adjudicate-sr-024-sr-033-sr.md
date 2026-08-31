+++
id = "WI-547"
title = "adjudicate: SR-024, SR-033, SR-043, SR-052, SR-053, SR-054, SR-111, SR-112, SR-129, SR-144, SR-146, SR-147, SR-149, SR-167, SR-175, SR-176, SR-177 - approved/routed cell(s) amended on merged trunk 579abf1..b057b09 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-024", "SR-033", "SR-043", "SR-052", "SR-053", "SR-054", "SR-111", "SR-112"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
+++

## Deliverable

Ruled by the independent adjudicator (ANTHROPIC-OPUS-STRONG, session 001 of the
lane, 96 s wall) at the lane's claim commit, from the before/after cells alone:

    VERDICT: CLARITY rows=17

Every one of the seventeen amended cells is a `Rationale` cell, and every
amendment strips (or, at SR-175, restructures in place) the `Hat-derived
(hat.X):` provenance label while keeping the charter clause and the obligation
the row imposes — a builder or test acting on the BEFORE text acts identically
on the AFTER text. The verdict, one line per row, is the lane's own record at
`docs/reviews/wi-547-adjudicate-sr-024-sr-033-sr/001-ADJUDICATE-fb0ed7c.md`.

Consequence: the seventeen rows' attestation STANDS — all seventeen read
`Approved` on trunk (the amendment never flipped them), so a CLARITY ruling
owes no flip and no re-attest; nothing in the registries was edited by this
row (the brief forbids it, and the ruling asks for nothing). No `##
Dispositions` block: no scope moved, so no follow-up row is drafted.

Closed by the supervising session, not the adjudicator: the amendment brief
(`adjudicate-amendment.template.md`) carries no C6 close step — only the
disposition brief received one in WI-548 — so the lane's spec stayed in
`active/` after the verdict commit. Recorded as a kit finding in
`docs/decisions-for-review-2026-08-31.md`.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-024 `Rationale`: "Realizes SN-002 — dimensional coverage is generated from the SR's declared inputs, not hand-listed. Hat-derived (hat.TE…" -> "Realizes SN-002 — dimensional coverage is generated from the SR's declared inputs, not hand-listed. Systematic expansio…"
- SR-033 `Rationale`: 'Realizes SN-004 — the release gate has a generated checklist surfacing the budgets a human must tick off, because a war…' -> 'Realizes SN-004 — the release gate has a generated checklist surfacing the budgets a human must tick off, because a war…'
- SR-043 `Rationale`: 'Realizes SN-006 (a walk-away run stays safe — bounded, supervised fan-out with the override held by the human, not the …' -> 'Realizes SN-006 (a walk-away run stays safe — bounded, supervised fan-out with the override held by the human, not the …'
- SR-052 `Rationale`: 'Realizes SN-024 and SN-023 — an accessibility bar left unstated silently reads as no bar at all, so the obligation is s…' -> 'Realizes SN-024 and SN-023 — an accessibility bar left unstated silently reads as no bar at all, so the obligation is s…'
- SR-053 `Rationale`: 'Realizes SN-024 and SN-023 — how alike is alike enough is subjective at the margins, which is why this row states the c…' -> 'Realizes SN-024 and SN-023 — how alike is alike enough is subjective at the margins, which is why this row states the c…'
- SR-054 `Rationale`: 'Realizes SN-024 and SN-023 — task-level usability is perceptual (is this findable, is this legible), so a test can conf…' -> 'Realizes SN-024 and SN-023 — task-level usability is perceptual (is this findable, is this legible), so a test can conf…'
- SR-111 `Rationale`: 'Realizes SN-007 — without a recorded origin an adopter cannot tell which kit version they are on, so a re-sync degrades…' -> 'Realizes SN-007 — without a recorded origin an adopter cannot tell which kit version they are on, so a re-sync degrades…'
- SR-112 `Rationale`: 'Realizes the dissolved edge expectation that a generated artifact drifting from its source fails its --check — one skil…' -> 'Realizes the dissolved edge expectation that a generated artifact drifting from its source fails its --check — one skil…'
- SR-129 `Rationale`: 'WHAT THE ROW STATES IS THE CAPABILITY. The spec folder layout (status = directory, TOML frontmatter, Deliverable in the…' -> 'WHAT THE ROW STATES IS THE CAPABILITY. The spec folder layout (status = directory, TOML frontmatter, Deliverable in the…'
- SR-144 `Rationale`: 'Five successive dedup mechanisms leaked because each reconstructed the return event from a MUTABLE proxy; a document th…' -> 'Five successive dedup mechanisms leaked because each reconstructed the return event from a MUTABLE proxy; a document th…'
- SR-146 `Rationale`: 'Prose steers the sessions this loop launches and had been reviewable only by reading Python source, which makes the pro…' -> 'Prose steers the sessions this loop launches and had been reviewable only by reading Python source, which makes the pro…'
- SR-147 `Rationale`: 'THE ROW STATES ONE OBLIGATION, and the migration history - the two prior carriers and the cutover - is no part of it: n…' -> 'THE ROW STATES ONE OBLIGATION, and the migration history - the two prior carriers and the cutover - is no part of it: n…'
- SR-149 `Rationale`: "Realizes SN-004 (the ladder's vocabulary is the one the project is held to) and SN-010 (docs stay honest). This check i…" -> "Realizes SN-004 (the ladder's vocabulary is the one the project is held to) and SN-010 (docs stay honest). This check i…"
- SR-167 `Rationale`: 'Realizes SN-008 (a reader can believe a green — a breach on a row the project chose to hard-gate must red the run, not …' -> 'Realizes SN-008 (a reader can believe a green — a breach on a row the project chose to hard-gate must red the run, not …'
- SR-175 `Rationale`: 'Hat-derived (hat.DATA-PROTECTION, with hat.SECURITY C-SEC-5 and hat.LEGAL C-LEG-3 converging on the same boundary contr…' -> "Repository content is briefed to external model providers, and for an adopter that content's history carries every cont…"
- SR-176 `Rationale`: 'Hat-derived (hat.DATA-PROTECTION, C-DPR-2 — clause text in docs/plans/2026-08-16-blind-derivation-c-hats.md): the findi…' -> 'The finding record is the one artifact guaranteed to contain the personal data it reports, created by the control itsel…'
- SR-177 `Rationale`: 'Hat-derived (hat.PERFORMANCE, C-PRF-1 — clause text in docs/plans/2026-08-16-blind-derivation-c-hats.md): the charter r…' -> "The charter refuses a declared budget with no measurement behind it, and SN-027 is that finding inverted — the system's…"

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Cancelled precedent on the same SRs (do not re-propose the refuted)
- WI-298 (cancelled) Dashboard --border misses the 3:1 graphical-boundary floor in both th… — reason: RETIRED 2026-07-24 as NOT-A-DEFECT, owner-ruled after verification against the artifact. The finding claimed --border supplies sub-3:1 boundaries for 'focusabl…

### Decomposition code map (LLR/TC on the same SRs)
- LLR-024 [project-trajectory/scripts/gen_cases.py :: main] tests: (see TC-024) — Permutation expander
- LLR-025 [project-trajectory/scripts/gen_skills_index.py :: main] tests: (see TC-025) — Skills index generator
- LLR-033 [project-trajectory/scripts/gen_release_checklist.py :: main] tests: (see TC-033) — Release checklist generator
- LLR-040 [project-trajectory/scripts/subagent_gate.py :: decide/main] tests: (see TC-043) — Subagent spawn gate
- LLR-043 [project-trajectory/scripts/gen_skills_index.py :: check_agent_sync] tests: (see TC-045) — Cross-agent skill fan-out drift check
- LLR-055 [project-trajectory/scripts/gen_trajectory.py;project-trajectory/scripts/traj_views.py :: build_html/_nav/when_view] tests: (see TC-055) — Dashboard usability rendering

### Knowledge packs the touched components declare (read before building)
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-011 scripts/gen_trajectory -> scripts/check: exit-code 0 clean or vacuous · 1 invalid registry or stale HTML
- IF-014 scripts/bootstrap -> external:downstream adopter: bytes the scaffolded template tree written under the destination root
- IF-017 scripts/gen_cases -> external:downstream adopter: stdout cases as table | params | toml | csv
- IF-018 scripts/gen_release_checklist -> external:downstream adopter: file docs/release-checklist.md — one `- [ ] <ID> — <what to confirm> (refs)` item per human-verified row
- IF-019 scripts/gen_skills_index -> external:downstream adopter: file skills/INDEX.csv: banner comment, header, one row per skill (name, scope, stacks, domains, phases, tags, desc…
- IF-020 scripts/subagent_gate -> external:agent CLI: exit-code 0 allow, ask or defer · 2 deny
