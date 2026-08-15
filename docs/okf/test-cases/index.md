---
type: "Index"
title: "test-cases"
description: "tier index"
tags: []
resource: "generated"
---
> **GENERATED — a reference copy, not the source of truth.** Derived from docs/test/test-cases.toml by scripts/gen_okf.py; edit the registry/doc, then rerun it (docs/process.toml [checks] okf_export = false silences the layer).

# test-cases — index

| id | summary |
|---|---|
| [TC-001](TC-001.md) | Run the trace suite; a linked chain is orphan-free and an injected orphan fails --strict. |
| [TC-002](TC-002.md) | Run the registry-checks suite; duplicate/malformed ids and mis-columned rows fail --stric… |
| [TC-003](TC-003.md) | Run the registry-checks suite; leftover -000 rows, empty/out-of-vocab fields, and (once t… |
| [TC-004](TC-004.md) | Run the acceptance-criteria advisory suite; an unpinned comparative warns without changin… |
| [TC-005](TC-005.md) | Run the off-spine registry suites; PB and current REPO/legacy MOD back-link findings fire… |
| [TC-006](TC-006.md) | Run the check-harness suite; gate steps run and a missing required tool fails with SKIP(m… |
| [TC-007](TC-007.md) | Run the stack-profile suite; commands and tiers/coverage/arch-map resolve from stack.ini. |
| [TC-008](TC-008.md) | Run the stack-profile suite; malformed/non-integer/missing-binary profiles fail loudly. |
| [TC-009](TC-009.md) | Run the profile suite; a non-Python profile omits Python-only files and seeds files-mode … |
| [TC-010](TC-010.md) | Run the bootstrap suite; a fresh scaffold's harness runs green. |
| [TC-011](TC-011.md) | Run the bootstrap suite; a re-run leaves existing files unchanged, --force overwrites, an… |
| [TC-012](TC-012.md) | Run the check-docs suite; a broken link or missing vision tag fails --stale. |
| [TC-013](TC-013.md) | Run the check-flows suite; a conformant flow passes and a malformed one fails. |
| [TC-014](TC-014.md) | Run the check-perf suite; a within-tolerance metric passes and a regression fails. |
| [TC-015](TC-015.md) | Run the perf-budgets suite; an unresolvable or empty PB Refs is a finding. |
| [TC-016](TC-016.md) | Run the check-stubs suite; a stub at the declared gate fails and clean source passes. |
| [TC-017](TC-017.md) | Run the check-privacy suite; a staged secret is blocked with privacy-check off. |
| [TC-018](TC-018.md) | Run the check-privacy suite; PII/identity classes fire only with privacy-check on and hon… |
| [TC-019](TC-019.md) | Run the pre-commit-hook suite; a failing integrity/secrets check blocks the commit. |
| [TC-020](TC-020.md) | Run the pre-push-hook suite; a secret/identity in the push range blocks the push. |
| [TC-021](TC-021.md) | Run the hook suites' python-probe cases; a missing/aliased python3 reports clearly withou… |
| [TC-022](TC-022.md) | Run the check-vendored suite; a drifted vendored copy is a finding. |
| [TC-023](TC-023.md) | Run the gen-arch-map suite; --check fails on a stale map and regeneration rewrites only t… |
| [TC-024](TC-024.md) | Run the gen-cases suite; the spec grammar expands to the expected case set. |
| [TC-025](TC-025.md) | Run the skills-index suite; INDEX.csv regenerates from the SKILL.md frontmatter. |
| [TC-026](TC-026.md) | Run the agent-loop suite; the dispatcher and its workers resume headless (registry + rese… |
| [TC-027](TC-027.md) | Run the agent-loop suite; preflight exits a typed code on a non-git dir / missing CLI / p… |
| [TC-028](TC-028.md) | Run the agent-loop suite; a zero-commit repo is guarded and an all-ERROR region reads as … |
| [TC-029](TC-029.md) | Run the agent-loop suite's lock tests (ported from the retired tracks suite): a hard-exit… |
| [TC-030](TC-030.md) | Run the agent-loop suite's lock tests (ported from the retired tracks suite): a second co… |
| [TC-031](TC-031.md) | Run the process-config and policy suites: every enforcer reads one value per dial from do… |
| [TC-032](TC-032.md) | Run the onboard/dev-setup suite; the scaffolded scripts run to a green setup and dev-setu… |
| [TC-033](TC-033.md) | Run gen_release_checklist.py over a warn-tier PB budget; assert the generated checklist l… |
| [TC-034](TC-034.md) | Run the dependency-ledger suite; an AST scan asserts every kit script's top-level imports… |
| [TC-035](TC-035.md) | Analyze the CI matrix result across Linux/Windows/macOS x Python 3.11/latest. |
| [TC-036](TC-036.md) | Inspect a re-sync done per ADOPTING.md section 6 against the docs/kit-version diff — kit-… |
| [TC-037](TC-037.md) | Run WI id, predecessor, cycle, placeholder, absent-registry, and opt-out validation cases. |
| [TC-038](TC-038.md) | Generate the core offline dashboard and inspect completeness, spine hierarchy, and roadma… |
| [TC-040](TC-040.md) | Run the agent-loop suite; a REVIEW-B-mapped phase invokes the second fake CLI and not the… |
| [TC-041](TC-041.md) | Run the doc-refs suite; a dangling path warns then gates under --strict, non-path backtic… |
| [TC-042](TC-042.md) | Run the gen-okf suite; typed linked concepts generate, Process Guide concepts emit for pr… |
| [TC-043](TC-043.md) | Run the subagent-gate suite; a Task/Agent spawn under deny is refused (permissionDecision… |
| [TC-044](TC-044.md) | Run IF id, SR back-link, Component membership, and endpoint-advisory trace cases. |
| [TC-045](TC-045.md) | Run the skills-sync suite: a hand-edited per-agent copy fails gen_skills_index --check-ag… |
| [TC-046](TC-046.md) | Run pair-row parsing, resolution, Env, cooldown, family preference/fallback, and tier-sel… |
| [TC-047](TC-047.md) | Run the run-menu suite: --list prints name<TAB>desc for each declared capability in decla… |
| [TC-048](TC-048.md) | Run Critique scope detection and redacted rubric/intent/artifact brief cases. |
| [TC-049](TC-049.md) | Run TOP_VIEW_MAX, containment, nesting, opt-out, and vacuity cases. |
| [TC-050](TC-050.md) | derive the gate from fixture states across every per-artifact rule and guard the cache; -… |
| [TC-051](TC-051.md) | Run the dashboard suite; the Process tab renders its three panels from the live registrie… |
| [TC-052](TC-052.md) | Run When-view phase/workstream thresholds, delivery-phase labels, and parent-edge aggrega… |
| [TC-055](TC-055.md) | A fresh, family-heterogeneous CRITIQUE session (LLR-048/LLR-082 loop) adjudicates the gen… |
| [TC-056](TC-056.md) | Run the dashboard suite; the Process tab renders both working loops (intake loop A + huma… |
| [TC-057](TC-057.md) | Run the dashboard suite; the tiered decomposition views render one horizontal parent->chi… |
| [TC-058](TC-058.md) | Run schedule.py against a fixture registry; the ready frontier, the exclusions with reaso… |
| [TC-059](TC-059.md) | Drive the pure classifier over every declared safety and policy input and compare consume… |
| [TC-060](TC-060.md) | Drive trunk_step --regen and the status-map freshness gate on fixture repos; assert the s… |
| [TC-061](TC-061.md) | Run two concurrent workers from explicit --wi/--train/worktree assignments; assert no lan… |
| [TC-067](TC-067.md) | Run the cross-component import coverage matrix. |
| [TC-068](TC-068.md) | Run the armed-spec interface-section matrix. |
| [TC-069](TC-069.md) | Run rival plan coverage, reference, graph, absent-registry, and malformed-input cases. |
| [TC-070](TC-070.md) | Drive typed round transitions, budgets, caps, repairs, revisions, swapped arbiters, persi… |
| [TC-071](TC-071.md) | Assemble every hat brief with sentinel data outside the allowlist and strict template var… |
| [TC-072](TC-072.md) | Drive planner_pair and planner_fallback across diverse, degraded, cooled, nonresponsive, … |
| [TC-073](TC-073.md) | Drive the coverage adapter through clean, first-finding repair, repeated finding, malform… |
| [TC-074](TC-074.md) | Build a fixture round and verify allocation, stable stage writes, selected-WI filing, dep… |
| [TC-075](TC-075.md) | Run the hand-edited/generated status source-of-truth matrix. |
| [TC-076](TC-076.md) | Run the full fresh-session dual-plan round including fallback and position-swapped arbitr… |
| [TC-077](TC-077.md) | Run Deliverable/status coherence and strict open-SpecRef cases. |
| [TC-078](TC-078.md) | Generate with and without module/component and OKF bundles. |
| [TC-079](TC-079.md) | Run deterministic, responsive, stale/missing, Git as-of, and no-Git generation cases. |
| [TC-080](TC-080.md) | Run endpoint/direction, source-sink, Active-citation, Contracts, opt-out, and strict non-… |
| [TC-081](TC-081.md) | Generate dashboard and architecture views with and without declared seams. |
| [TC-082](TC-082.md) | Run review-policy 0/1/2, prompt-map, redaction, selection logging, verdict, and unmanaged… |
| [TC-083](TC-083.md) | Run substance components, corroboration, tripwires, decay, verdict parsing, and CLI cases. |
| [TC-084](TC-084.md) | Drive swap, tier-up, shared failure, contradiction, tripwire, and the ratification-level … |
| [TC-085](TC-085.md) | Run critique approval, rework, configured-cap exhaustion, and the ratification-level disp… |
| [TC-086](TC-086.md) | Run Critique vocabulary/LLR-completeness and staged closure-ratchet cases. |
| [TC-087](TC-087.md) | Generate nested/flat How-SW containment and boundary aggregation cases. |
| [TC-088](TC-088.md) | Run component-to-module How-SW tier and top-width-bound cases. |
| [TC-089](TC-089.md) | Render seams at hierarchy ports and crossing container boundaries. |
| [TC-090](TC-090.md) | Exercise pointer/keyboard descent and breadcrumb restoration. |
| [TC-091](TC-091.md) | Classify missing, unknown, structurally contradictory, critique, checkpoint, and dual-pla… |
| [TC-097](TC-097.md) | Run direct worker/flag refusal and PlanMode-derived classification/contradiction cases. |
| [TC-098](TC-098.md) | Run dispatcher SELECT, human-held PAGE, loop-held PAGE continuation, regeneration failure… |
| [TC-100](TC-100.md) | Run check_trajectory over registries with a done+SpecRef row, an uncited live spec, a def… |
| [TC-101](TC-101.md) | Run the check_coverage suite; a module below its floor exits 1 naming it, a declared modu… |
| [TC-102](TC-102.md) | Generate the dashboard against two fixture registries and assert the LLR-052 '>3' rule me… |
| [TC-103](TC-103.md) | Generate the dashboard from a tiered fixture registry and assert the drill emits <nav cla… |
| [TC-104](TC-104.md) | Three complementary checks. (1) Unit: _svg_role classifies a native <a href> body, and ta… |
| [TC-105](TC-105.md) | Assert the U5 palette-decollision invariants directly against the declared Python constan… |
| [TC-106](TC-106.md) | Generate the dashboard from a tiered fixture registry and a flat OKF bundle and assert: (… |
| [TC-107](TC-107.md) | Generate the dashboard with the Process tab enabled (DevBar-Tests gate) and assert --nhea… |
| [TC-108](TC-108.md) | Two halves, one floor. (a) Compute _ring_ink for every fill declared in STATUS_FILL/TIER_… |
| [TC-109](TC-109.md) | Collect every #rrggbb literal declared in gen_trajectory's module-level palette collectio… |
| [TC-110](TC-110.md) | Render every emitter, walk each node group, and assert per node kind: it carries tabindex… |
| [TC-113](TC-113.md) | Over the shipped dashboard plus seven fixture renders, collect every focusable element (t… |
| [TC-114](TC-114.md) | Enumerate every declared colour vocabulary and compute pairwise CIE76 deltaE over all cro… |
| [TC-115](TC-115.md) | Over the shipped dashboard plus seven fixture renders, assert each declared --w-*/--o-*/-… |
| [TC-116](TC-116.md) | Over the shipped dashboard plus seven fixture renders, assert each declared scale step is… |
| [TC-117](TC-117.md) | Over the shipped dashboard plus seven fixture renders: derive every querySelectorAll sele… |
| [TC-118](TC-118.md) | Over the shipped dashboard plus seven fixture renders: resolve the document's token defin… |
| [TC-119](TC-119.md) | Reflect every UPPERCASE module-level constant RECURSIVELY (nested dicts/tuples/sets and b… |
| [TC-120](TC-120.md) | Generate the dashboard from a zero-active/all-queued fixture — the condition under which … |
| [TC-121](TC-121.md) | Generate the dashboard and derive EVERY emitted <svg> from the document (not a hand list,… |
| [TC-122](TC-122.md) | Sweep EVERY emitter document (the shipped artifact plus a fixture per emitter, the A2-rev… |
| [TC-123](TC-123.md) | Drive gen_open_items over temp repos: assert a pending registry row renders as a brief an… |
| [TC-124](TC-124.md) | Generate the dashboard over a tiered fixture carrying one sentence-length stakeholder nee… |
| [TC-125](TC-125.md) | Sweep the union of emitter documents (the shipped PROJECT_STATE.html plus a fixture per e… |
| [TC-126](TC-126.md) | Run the spine stand-alone suite; a WI id or process-doc citation in a normative cell of a… |
| [TC-127](TC-127.md) | Run the requirement-form suite; each of the six rules fires on its own defect shape, and … |
| [TC-128](TC-128.md) | Run the paraphrase-advisory suite; an echoing child warns while a real decomposition nami… |
| [TC-129](TC-129.md) | Run the converter suite: the live registry round-trips in whichever home is authoritative… |
| [TC-130](TC-130.md) | Run the trunk-step suite: committed fragments compile in git order with links rebased and… |
| [TC-131](TC-131.md) | Run the pause suites: the tracked home pauses via pause_reason with the unchanged return … |
| [TC-132](TC-132.md) | Run the integrator suite: each claim refusal fires by name and the green claim moves the … |
| [TC-134](TC-134.md) | Run the check-harness lane suite: a claimed work branch skips the declared freshness step… |
| [TC-135](TC-135.md) | Run the trunk-step regen suite: --regen skips absent artifact families with a notice and … |
| [TC-136](TC-136.md) | Run the pending-surface pause suite: the block renders since/reason verbatim (no clock), … |
| [TC-137](TC-137.md) | Run the drive suite: an unwired agent command refuses before any claim while an empty que… |
| [TC-138](TC-138.md) | Run the handback suite: a partial close moves each claimed spec to the terminal partial/ … |
| [TC-139](TC-139.md) | Run the spec_move suite: an archival move redirects inbound links from every depth (text … |
| [TC-140](TC-140.md) | Run the figure-provenance suite: the three 2026-08-01 false figures (the stale mutation l… |
| [TC-141](TC-141.md) | Fixture-drive the SN-coverage rung: an uncovered ratified SN caps raw at DevBar-Below (th… |
| [TC-142](TC-142.md) | Fixture-drive --next-phase: on a spine whose non-draft max phase is 3 with a Draft row at… |
| [TC-143](TC-143.md) | Run the dispatch admission suite: an exclusive row + a busy lane answers wait (never a pa… |
| [TC-144](TC-144.md) | Run the dispatch loop suite on real git repos with the real bar: a spine batch claims as … |
| [TC-145](TC-145.md) | Run the integrator claim suite: a spine claim succeeds on an idle station (the deleted sa… |
| [TC-146](TC-146.md) | Run the schedule + integrate suites' adjudication cases: the kind classifies exclusive at… |
| [TC-147](TC-147.md) | Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys… |
| [TC-148](TC-148.md) | Run the integrator + dispatcher suites' intake-arm cases: a merged branch that amended a … |
| [TC-149](TC-149.md) | Run the shipped-tier suite; it derives the adopter-facing check set from check.py's own l… |
| [TC-150](TC-150.md) | Run the process-config suite: it sources the SHIPPED hook's own sh functions and drives t… |
| [TC-151](TC-151.md) | Run the ratification-level suite: the full level x stage matrix against the ladder the sh… |
| [TC-152](TC-152.md) | Run the migration cases in the process-config suite: a full conversion deletes every lega… |
| [TC-153](TC-153.md) | Run the attestation-digest suite: it DRIVES the premise rather than asserting it - the am… |
| [TC-154](TC-154.md) | Run the loop-order suite: an adjudication row admits ahead of a ready spine batch while t… |
| [TC-155](TC-155.md) | Run the queue-conflict cases: each of the three signals fires with both ids in determinis… |
| [TC-156](TC-156.md) | Run the handback suite over real git worktrees: a partial close is clean under the REAL t… |
| [TC-157](TC-157.md) | Run the prompts and routing suites: strict slot filling and its refusals, the preflight o… |
| [TC-158](TC-158.md) | Run the id-watermark suite. It drives trace.py's CLI so the rules are asserted on the EXI… |
| [TC-159](TC-159.md) | Run the carrier-converter suite: it converts the live spine, re-parses the emitted TOML w… |
| [TC-160](TC-160.md) | Drive the carrier reader over a REAL repo whose spine is cut over from CSV to TOML in one… |
| [TC-161](TC-161.md) | Drive the real loop against a fake agent CLI over throwaway git repos, one per ROUTED bri… |
| [TC-162](TC-162.md) | Load well-formed, malformed (falsey table, unknown key, bad grammar) and absent rosters; … |
| [TC-163](TC-163.md) | Plant a retired tag in a live authored file and one in each declared carve-out class (arc… |
| [TC-164](TC-164.md) | Construct a needs registry whose need cell plants one token of each declared class (an in… |
| [TC-165](TC-165.md) | Scaffold with a non-Python bootstrap profile into a temp dir and run trace.py --strict-in… |
| [TC-166](TC-166.md) | Run trace.py's component pass over fixture component registries: (a) a complete derivatio… |
