+++
id = "WI-610"
title = "adjudicate: combined approved-cell amendments after PC authoring (OI-88 transfer)"
workstream = "process"
sr_refs = ["SR-024", "SR-033", "SR-043", "SR-052", "SR-053", "SR-054", "SR-111", "SR-112", "SR-129", "SR-144", "SR-146", "SR-147", "SR-148", "SR-149", "SR-156", "SR-161", "SR-162", "SR-167", "SR-175", "SR-176", "SR-177"]
needs = ["WI-608", "WI-611"]
specref = "docs/reviews/wi-609-resolution/DECISION.md"
buildtier = "strong"
safety_class = "adjudication"
supersedes = "WI-601;WI-603;WI-605"
brief = "amendment"
adjudicates = ["LLR-058", "LLR-061", "LLR-123", "LLR-140", "LLR-144", "LLR-149", "LLR-150", "LLR-151", "LLR-152", "LLR-153", "LLR-154", "LLR-158", "LLR-161", "LLR-167", "LLR-183", "LLR-207", "SR-024", "SR-033", "SR-043", "SR-052", "SR-053", "SR-054", "SR-111", "SR-112", "SR-129", "SR-144", "SR-146", "SR-147", "SR-148", "SR-149", "SR-156", "SR-161", "SR-162", "SR-167", "SR-175", "SR-176", "SR-177", "TC-058", "TC-061", "TC-138", "TC-143", "TC-144", "TC-145", "TC-146", "TC-147", "TC-148", "TC-153", "TC-154", "TC-156", "TC-161", "TC-178", "TC-205"]
+++

## Context

Owner-authorized one-time supervised ownership transfer under OI-88 and docs/reviews/wi-609-resolution/DECISION.md. This is the complete atomic Approved-change scope of the committed PC source candidate, not a consolidation-census judgment, acceptance of any row, or authority to run a control window. Authoring predecessor WI-608 remains a hard edge. The original separate scopes and full proposal Context are preserved in the restructured specs and Git; their original proposal blobs and the stopped WI-605 evidence remain authoritative history. The old owners have not accepted their rows and are not complete.

Judge each scoped row cumulatively from the bound approved snapshot to the final live candidate, including parents, siblings, traced tests, and every meaning-changing use. Use the existing primary Approval payload, real immutable per-cell before/after blob IDs, actual committed current-turn judgment/session evidence, complete absorption ledger, and ordinary independent review. Inventories are discovery aids, not use acceptance. All changed Approved rows in the affected whole-file snapshot set require accepted scoped decisions; all Drafted riders stay Drafted and their existing first-approval owners remain unchanged. Missing, stale, contradictory, unjudged, or outside-authority evidence must refuse publication. A RETURN remains a truthful zero-effect outcome with required dispositions, not semantic approval. No manual snapshot copy, verifier bypass, substitute protocol, or widened bound turn.

In particular, the PC singleton LLR-061 and TC-061 must be judged together against the exact cumulative LLR text. Review all batch-test retirement obligations in PC-BATCH-USES.md before any deletion. TC-205's pre-existing citation to test_a_two_row_batch_close_peels_under_one_canonical_order is absent in the current source: resolve it truthfully in the judgment or return a scoped authoring continuation; do not claim nonexistent evidence passed. Registry authoring belongs before selection; this adjudicator cannot change live source cells in a bound candidate.

Done when the existing exclusive primary publisher validates the real decisions, impact and whole-file absorption evidence plus independent review/provenance, then atomically publishes an accepted outcome or a truthful RETURN with required scoped dispositions. Keep the coordinator paused; this WI authorizes no control window, push or main merge. Until actual live contract acceptance, do not delete PC batch implementation.

The absorbed rows' acceptance criteria, carried across UNCHANGED. This is the spec this row must still satisfy — the ids are historical, the obligations are not:

### WI-601 (absorbed) — its Done-when, verbatim

(this row's spec declared no `## Done-when` section)

### WI-603 (absorbed) — its Done-when, verbatim

(this row's spec declared no `## Done-when` section)

### WI-605 (absorbed) — its Done-when, verbatim

(this row's spec declared no `## Done-when` section)

Advisory registry joins (WI-388; never gating):

### Cancelled precedent on the same SRs (do not re-propose the refuted)
- WI-298 (cancelled) Dashboard --border misses the 3:1 graphical-boundary floor in both th… — reason: RETIRED 2026-07-24 as NOT-A-DEFECT, owner-ruled after verification against the artifact. The finding claimed --border supplies sub-3:1 boundaries for 'focusabl…

### Decomposition code map (LLR/TC on the same SRs)
- LLR-014 [project-trajectory/scripts/check_perf.py :: evaluate] tests: (see TC-014) — Budget comparator
- LLR-024 [project-trajectory/scripts/gen_cases.py :: main] tests: (see TC-024) — Permutation expander
- LLR-025 [project-trajectory/scripts/gen_skills_index.py :: main] tests: (see TC-025) — Skills index generator
- LLR-033 [project-trajectory/scripts/gen_release_checklist.py :: main] tests: (see TC-033) — Release checklist generator
- LLR-040 [project-trajectory/scripts/subagent_gate.py :: decide/main] tests: (see TC-043) — Subagent spawn gate
- LLR-043 [project-trajectory/scripts/gen_skills_index.py :: check_agent_sync] tests: (see TC-045) — Cross-agent skill fan-out drift check

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-004 scripts/check_perf -> scripts/check: stdout check_perf: OK - <summary> or FAIL - <summary>, plus one <status> - <PB-ID> <metric> line per non-clean budget
- IF-147 scripts/check_perf -> scripts/check: exit-code 0 OK, SKIP or WARN · 1 a Gate=fail budget breached in the run tier, or --update-baseline with no metrics

Pre-selection prerequisite: WI-611 repairs terminal-continuation intake and the stale TC-205 citations found by the supervised preflight. The original scope and all semantic obligations above remain; the exact final TC-205 text and its actual coverage must still be judged.
