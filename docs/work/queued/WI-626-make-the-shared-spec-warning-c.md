+++
id = "WI-626"
title = "Make the shared-spec warning compare section anchors, so distinct sections of one plan are distinct specs"
workstream = "scripts"
sr_refs = ["SR-157"]
specref = "docs/requirements/low-level-requirements.toml#LLR-160"
buildtier = "medium"
priority = 2
safety_class = "spine"
+++

## Context

Filed at the owner's request, 2026-09-24.

`queue_conflict_pairs` (`check_trajectory.py:3172-3173`) pairs two open work
items whenever their SpecRefs name the same file, with the anchor stripped.
Items filed from one plan's sections therefore read as possible duplicates:
nine queued items citing different sections of the sister plan produce 36
pairs, and the strict check's advisory count here rose from 85 to 124. A
warning that fires on every documented split stops being read, which is the
failure the check's own comments warn about.

Stripping the anchor is the APPROVED design: LLR-160's detail says "a shared
anchor-stripped `SpecRef`". So this item changes approved meaning. The lane
amends LLR-160's text and leaves its Status alone, and the merge routes it to
the adjudicator as a MEANING amendment for re-attestation.

The proposed rule: two SpecRefs share a spec when their files match and either
their anchors are equal or either one has no anchor (a whole-document reference
covers every section). Two different sections of one document are two specs.
The near-duplicate title signal and the shared-SR signal are unchanged, so a
real duplicate filed against two sections is still caught by its title.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-001 [project-trajectory/scripts/trace.py :: main] tests: (see TC-001) — SN->SR->LLR->TC join + orphan set
- LLR-002 [project-trajectory/scripts/trace.py :: integrity_findings/structure_findings/triangle_findings] tests: (see TC-002) — Id + registry-CSV-structure + citation integrity
- LLR-003 [project-trajectory/scripts/trace.py :: placeholder_findings/schema_findings/phase_approved_findings] tests: (see TC-003) — Placeholder + schema checks
- LLR-004 [project-trajectory/scripts/trace_text.py :: ac_advisories] tests: (see TC-004) — Comparative-term advisory
- LLR-005 [project-trajectory/scripts/trace.py :: integrity_findings/module_findings] tests: (see TC-005) — Off-spine integrity + back-links
- LLR-034 [project-trajectory/scripts/check_trajectory.py :: load_wis/validate] tests: (see TC-037) — WI dependency-DAG validation

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-009 scripts/check_trajectory -> scripts/check: exit-code 0 clean · 1 hard error · 2 usage
- IF-021 docs/requirements/ -> scripts/trace;external:downstream adopter: file id-keyed TOML, one file per spine tier; ids are the table keys

## Done-when

- The shared-SpecRef signal pairs two open items only when their files match
  and either their anchors are equal or one of them has none; the other two
  signals are unchanged.
- LLR-160's detail is amended to state the rule, in the same lane, Status
  untouched, for the adjudicator's re-attestation.
- Tests: different anchors in one file do not pair; the same anchor pairs; an
  anchor-less reference pairs with an anchored one in the same file; two
  anchor-less references to one file pair.
- The strict check's warning count on this repo, before and after, is quoted.
