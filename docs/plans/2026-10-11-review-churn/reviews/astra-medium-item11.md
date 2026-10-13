<!-- Independent analysis of the item 11 LLR-fitness question (item-11-llr-interface-check-handoff.md, with plan revision 13), at commit eae8e1cbe (GPT-6 Astra, medium effort, codex exec with the Sol launcher's flags; brief: brief-item11.md). Recorded verbatim; its per-LLR table is item11-classes-astra.csv; the judged synthesis is ../item-11-llr-fitness-report.md. -->

# Item 11: retain the behavioural spine; do not make IF reachability its only discharge rule

**Answer: 68 fit, 226 reword, 8 reframe-or-retire out of 302 LLRs.**
This is a screening census, not 302 adjudicated approvals: **38 rows were read by hand with test bodies; 264 use disclosed script rules**.
The hand sample is **14 fit, 21 reword, 3 reframe-or-retire**.
Interface availability is separately **228 existing-IF candidates, 65 boundary-artifact candidates, 5 kernel/internal-edge cases, 4 without a sensible seam for the current whole claim**.
The **55-of-302 no-owner claim reproduces**; it is not a count of requirements without observable behaviour.

**Item 11 as designed does not establish a reduction in rework.** Removing requirements' implementation pointers does; item 5 already supplies that benefit.
Making every LLR traverse an IF adds an architectural allocation that can itself change during refactoring, weakens precise code-to-obligation orientation, and leaves wording and verification defects intact.
Recommend **E: D as the durable baseline, with B's fitness review and C's artifact treatment used selectively**.
Keep code → LLR, remove downward implementation references, retain real architectural IFs, and author IF → LLR only when it states a useful, independently reviewed behavioural allocation.
Use one delivered-dashboard interface for its exposed contract if that allocation earns its cost; do not mint internal renderer or kernel seams to meet a quota.

**Owner calls remain:** universal IF carriage versus selective allocation; one direction with OI-112; the replacement for SR-180's discharge condition; IF ownership/approval; minimum-profile treatment; and whether recursive decomposition is a separate change.
Recommend selective allocation, IF → LLR with SR ancestry derived, independent design ownership, and separate consideration of recursion.
No migration, source edit, commit, dashboard generation or test execution was performed.

## Scope, sources and reproducibility

- Repository: `C:/Projects/ai-template.wt/item11-fit-astra-m`; `git rev-parse HEAD` returned `eae8e1cbe7540636b05a2c67462e64932d47384a`.
- Governing proposal: `context/README.md`, revision 13, owner rulings and section 11; query: `context/item-11-llr-interface-check-handoff.md`, read first in full.
- Here **LLR** means a row in `docs/requirements/low-level-requirements.toml`; **TC** means `docs/test/test-cases.toml`; **IF** means `docs/requirements/interfaces.toml`.
- **OI** means `docs/requirements/open-items.toml`; SR-180 is in `docs/requirements/system-requirements.toml`. All repository-relative citations refer to the pinned worktree.
- Read `CLAUDE.md`, antidote and spine-authoring skills, and `project-trajectory/prompts/spine-questions.md`; the newer prohibition overrides their older LLR naming guidance.
- `OWNER_SCRATCHPAD.md` was not opened. All outputs are beside this report, outside the repository.
- Reproduce: `python -B C:/Projects/ai-template.wt/review-tmp/2026-10-12-item11-fit/astra-analysis.py`.
- The script reads TOML and source text/AST only, then writes `astra-classes.csv` and `astra-counts.json` in its own review directory.
- It contains the exact lexical rules, candidate-ranking rule and hand decisions. Re-running reproduces the judgments; it does not independently validate them.
- `astra-read-tests.py` preserves one extraction batch; the hand-evidence inventory below identifies the remaining bodies read.

### Fitness labels and corrected tests

The census evaluates **title/detail/rationale after the universally required trace-cell removal**.
Literally, no complete current LLR row complies with ruling 5: all **302** have both `module` and `code_symbol`.
Calling every row unfit solely for those cells would hide the substantive question. Their removal is a common migration cost: **604 cells**, two per row.
`fit` means no additional wording/evidence defect identified, not permission to carry the complete present row unchanged into the new schema.
`reword` includes evidence repair where test 3 fails; prose edits alone do not fix those cases.
`reframe-or-retire` means a scope/obligation decision precedes wording, not deletion of every useful behaviour in the row.
Interface availability is independent: an existing IF can carry a bad requirement, and a good requirement can lack a registered IF.

| Test | Handoff problem | Corrected test used in the CSV |
|---|---|---|
| 1 | Every definition inside an LLR encourages schema duplication; keyword matches are not semantic proof. | Given the LLR and explicitly identified normative vocabulary/policy, can readers decide input domain, outcome, threshold and refusal? The implementation or TC cannot supply a missing decision. |
| 2 | “User-observable” can exclude a component's consumer; exposed technical vocabulary is not always an implementation carrier. | State behaviour at the chosen component or delivered-artifact boundary that survives a behaviour-preserving refactor. Remove implementation symbols, topology and incidental emitter syntax. |
| 3 | “At the level the user sees it” can demand system tests for local contracts or confuse static markup checks with runtime proof. | Stimulate the relevant boundary and assert its promised result, or use adequate structural/inspection evidence for an expressly bounded property. Evidence paths must still reach that instrument. |

A helper input/output test may prove local behaviour without justifying an architectural IF row.
A browser is appropriate for LLR-088/100's promised navigation effect; it is not automatically necessary for an expressly structural naming invariant.
Test 3 assesses the instrument, not whether it passed in this checkout: tests were read, not run.

### Original versus corrected reading

The original phrase “user sees” has no defined observer or abstraction level. A unique whole-corpus original-test count would pretend that ambiguity was settled.
These contrasts use its strict **system-operator/runtime** reading and report the material relaxations in the hand sample; other sampled rows retain their failed-test sets.

| LLR | Original failures / fitness | Corrected failures / fitness | Reason |
|---|---|---|---|
| 070 | 1;3 / reword | 1 / reword | TC-070 drives round dispositions directly; UI unnecessary, but policy/table remains insufficiently defined. |
| 071 | 3 / reword | none / fit | TC-071 inspects the actual brief supplied to the planner, the relevant consumer. |
| 073 | 3 / reword | none / fit | Real coverage subprocess and round machine expose IF-058's disposition. |
| 101 | 2;3 / reword | 2 / reword | Structural evidence fits declared scope; `_svg_role` and emitter syntax remain. |
| 108 | 2;3 / reword | none / fit | Accessible names and landmark distinction are exposed properties, not helper implementation identities. |
| 120 | 2;3 / reword | 2 / reword | Geometry inspection fits box-intersection scope; helper/history text remains. |
| 182 | 2;3 / reword | 2 / reword | Outcome selection is observable to its caller; enum/re-export/import prescriptions remain. |
| 184 | 2;3 / reframe-or-retire | 2 / reframe-or-retire | Ordering/refusal tests are useful; identity/import topology needs architectural disposition. |
| 192 | 2;3 / reword | 2 / reword | Record binding and stale verdict need no whole-product run; package topology still leaks. |

This does not assert the handoff intended the strict reading; it shows why that reading is the wrong migration gate.

## Counts and exact units

`tomllib` loads every entry under `design`, `interface`, `test` and `requirement`, without a status filter.
Thus the population includes retired-content LLR-050; IDs are not assumed contiguous. Histograms count each CSV row once.

| Component | Fit | Reword | Reframe-or-retire | Total | Hand-read |
|---|---:|---:|---:|---:|---:|
| CMP-006 | 12 | 80 | 5 | 97 | 10 |
| CMP-007 | 10 | 21 | 1 | 32 | 8 |
| CMP-008 | 22 | 79 | 2 | 103 | 9 |
| CMP-009 | 24 | 46 | 0 | 70 | 11 |
| Total | 68 | 226 | 8 | 302 | 38 |

| Fitness | Existing IF candidate | Boundary artifact | Kernel/internal edge | No seam for whole claim |
|---|---:|---:|---:|---:|
| Fit | 48 | 20 | 0 | 0 |
| Reword | 179 | 43 | 4 | 0 |
| Reframe-or-retire | 1 | 2 | 1 | 4 |

Failures overlap: test 1 **13**, test 2 **223**, test 3 **9**, counted by membership in `failed_tests`.
These are **detected failures**, not estimates of all defects. A scripted row without `3` is not evidence-certified.
The script flags vague terms and implementation-shaped prose and checks for a resolvable evidence file, not full behavioural coverage.
Lexical false positives and missed mechanisms/domains are possible. No statistical confidence interval or sample extrapolation is claimed.
The sample deliberately spans components and difficult cases; it is not random.

### Reproducing 55 rather than 90

Normalize by trimming whitespace, replacing backslashes with `/`, applying lexical POSIX path normalization, removing one leading `project-trajectory/`, and removing a trailing `.py` only.
Preserve case, directories, other suffixes and `__init__`; no symlink resolution, directory collapsing, basename matching or consumer-as-owner matching.
Split each LLR `module` on `;`, normalize entries and deduplicate within the cell. Normalize IF `owner` identically.
Count a no-owner LLR iff its module set has **empty intersection** with the IF owner set. One owning module excludes a multi-module row; no row counts twice.

- **55 LLRs**, spanning **36 distinct module keys**, have no owning-module match.
- **101 LLRs** have at least one unmatched module; **59 distinct unmatched module keys** occur across the population.
- **482 per-row module memberships**, **146 distinct module keys**, **85 multi-module rows**: respectively sum of set sizes, union size, and number of sets larger than one.
- The handoff's **90 / 64** does not reproduce under either quantifier. Its algorithm was not supplied, so the discrepancy cannot be diagnosed from its number alone.
- **12 renderer LLRs** is correct only for cells naming `rendering/traj_render.py` alone; exact token membership including multi-module cells gives **18**.
- These are ownership counts, not semantic allocation. LLR-073 lacks an owner match but has a plausible disposition boundary through IF-058.

The complete 55-ID list and renderer counts are in `astra-counts.json`; their rules are executable in the script.

### Other counts used here

| Measurement | Result | Rule |
|---|---:|---|
| IF / TC / SR rows | 243 / 316 / 131 | Parsed table sizes. |
| Drafted IFs | 243 | Exact `status == Drafted`; not an absent approval schema. |
| SR boundary cells / links | 131 / 166 | Nonempty `boundary_refs` / sum of array lengths. |
| IF crossing rows | 46 | Nonempty `interface_from_external` OR `interface_to_external`, once per row; README's 47 does not reproduce under this rule. |
| TCs naming IF | 95 | At least one `verifies` target resolves in IF registry. |
| LLR → SR / TC → LLR links | 338 / 344 | Sum parent arrays / `verifies` tokens resolving in LLR table. |
| Python files | 117 | Recursive `*.py` under `project-trajectory/scripts`; no imports executed. |
| Implements lines / targets | 898 / 1,955 | After stripping whitespace/comment markers, line begins `Implements:`; count lines / SR-or-LLR ID occurrences. |
| Implements files / live LLR IDs / file–LLR pairs | 97 / 228 / 321 | Distinct projections of that scan. |
| Contract tokens / file–IF pairs / IDs / files | 410 / 206 / 205 / 83 | `Contracts:` header or `Contract IF-…` body opener; count tokens then distinct projections. |
| Contracts header tokens | 204 | Plural `Contracts:` lines only; different unit from header-plus-body mentions. |

Source counts exclude hooks, other languages and tests: a physical-marker census, not the production parser's accepted-declaration inventory.
The live LLR gap is **74 = 302 − 228** under this scope, not proof of missing implementation.
`module_contracts` in `project-trajectory/scripts/gen_arch_map.py:515` also accepts early comment headers, so “module docstring only” is too narrow; function-body citations still are not its IF grammar.

## What the sample says

| Fitness class | Examples |
|---|---|
| Fit | LLR-001/TC-001: strict CLI orphans; LLR-011/TC-011: preserved versus replaced scaffold file; LLR-058/TC-058: readiness and CLI JSON; LLR-071/TC-071: permitted brief content and excluded sentinel. |
| Reword/evidence repair | LLR-087/TC-089: undefined ports and incomplete endpoint assertion; LLR-100/TC-103: markup and handler substring; LLR-186/TC-181: sound stage behaviour wrapped in delegation narrative; LLR-025/TC-025: cited suite lacks the promised stale-index mutation. |
| Reframe-or-retire | LLR-180/TC-175: downward-symbol discharge; LLR-181/TC-176: scaffold completeness mixed with topology/helper policies; LLR-184/TC-179: ordering mixed with object identity; LLR-050: explicitly asserts nothing live. |

| Interface class | Examples and disposition |
|---|---|
| Existing IF | LLR-001 → IF-145, LLR-011 → IF-014, LLR-058 → IF-055, LLR-073 → IF-058. Allocate by measurable result, not solely owner-module matching. |
| Boundary artifact | LLR-035/087/100/101 → proposed delivered project-state dashboard. LLR-190 → hosted verification workflow; LLR-192 → whole-suite evidence record. These are proposals, not allocated IDs. |
| Kernel/internal edge | LLR-184/185/205/260: preserve ordering, freshness, credential-class and evidence-tier semantics where needed; no IF per helper/import. LLR-182 mixes a registered vocabulary seam with an internal outcome decision. |
| No seam for whole current claim | LLR-031/050/181/197: one-home structure, retirement narrative or topology/policy bundles cannot honestly become one exposed behaviour. Reframe retained outcomes; this does not make policy reading or scaffold delivery unobservable. |

For scripted rows, `existing-if` means an owner/data-ranked candidate, not proof the entire requirement is carried there.
Every scripted row records uncertainty. Proposed artifact names are a worklist, not a recommendation to mint every name.
Semantic review may merge names or find an existing seam; **65 rows does not mean 65 new interfaces**.

### Delivered-dashboard interface and test defects

IF-011 is an **exit-code** interface: clean/vacuous versus invalid or stale output. It is not the document's interactive or structural contract.
Searching IF `data`/`notes` for `dashboard`/`PROJECT_STATE` and reading matches finds renderer consumers/vocabulary, not a dashboard HTML output interface.
IF-093 supplies outcome vocabulary; IF-227 supplies an assumption view-model. Neither carries breadcrumb restoration or the delivered page as a whole.
One proposed artifact-class IF, **Delivered project-state dashboard**, is reasonable, with concrete artifact bindings generated outside its row.
The IF need not name `PROJECT_STATE.html`; ruling 5 allows that shipped-artifact name at LLR/TC only.
“Non-code realizations” in item 11 addresses declarations, not semantic allocation; it does not turn the exit-code IF into a document IF.

LLR-087's `test_when_view_seams_wire_to_block_ports` compares sets of x-coordinates and an emitter-derived gap.
It does not assert semantic source/target or y-coordinate: another row's port at the same x-coordinate can evade this assertion.
`test_boundary_aggregation_dedupes_cross_component_edges` checks one aggregated title on its fixture, not every visible tier universally.
LLR-100's test asserts `trail=trail.slice(0,i+1)`; that can pass while the navigation action is unwired or broken.
LLR-101's fixture/shipped-artifact walks and predicate cases are stronger for its deliberately narrow structural claim, not full accessibility certification.
These observations come from `tests/test_traj_views.py` and `tests/test_traj_render.py` bodies, not TC level labels.

### Capability-voice rewrite sketches, not registry edits

- **LLR-087:** “At each displayed hierarchy level, each connection leaves its source's output port and reaches its destination's input port; connections with the same displayed source and destination appear once and identify all represented interfaces.” Decide permitted clearance independently of an emitter constant.
- **LLR-100:** “After descending into a container, selecting any displayed ancestor restores that ancestor's view and removes later ancestors from the navigation trail.” Activate navigation and inspect the resulting view in evidence.
- **LLR-101:** “In the delivered dashboard, an interactive descendant is not hidden from accessibility navigation by its enclosing graphic's presentation semantics; a non-interactive graphic exposed as one object has its own accessible name.” Preserve artifact/fixture scope; do not quietly expand to universal browser behaviour.
- **LLR-184 retained behaviour:** “Stage comparison follows the declared stage order and refuses an unrecognized stage.” Separately decide the home and value of import/identity constraints and tests.

## Alternatives and maintenance price

An authored link is an independently maintained source-to-target assertion, not a generated reverse edge or transitive path.
Two source-site citations remain two maintenance sites even when a coarse `(file, target)` projection merges them.
The common **338 LLR-parent and 344 TC-LLR edges** remain valuable under every option; changing code trace does not remove them.
Keep LLR → component as independent design intent under ruling 5; deriving it from code removes the independent allocation check.
Let **L** be code–LLR links, **C** code–IF links, **R** IF–LLR allocations, **Q** authored IF–SR links, **F** file–component declarations, **O** independent IF design-owner/role assertions.
Use a consistent granularity. Formulas below exclude unchanged parent/test/component allocations and count the connection choices under discussion.
Current coarse Python anchors are **L=321, C=206**; source occurrences are higher and are not interchangeable with those numbers.

| Design | One-time migration | Ongoing authored links / what breaks them | Orientation | Behaviour independence |
|---|---|---|---|---|
| A: proposed | Common trace cleanup; replace Implements; allocate every LLR; change grammar/readers/ownership/profiles/approval. Bad prose/evidence persists without separate work. | `C+R+Q+F+O`; at least one R per retained LLR. File splits move C/F; IF splits/versioning change R/Q; role changes affect O. | Architecture entry is strong; each citing function inherits all IF obligations, losing fine allocation. | Moves spare requirement rows, but allocation churn remains and code-shaped prose still reopens. |
| B: reword then A | A plus fitness judgments: screening identifies 226 repairs and 8 reframings; close scripted uncertainties before attachment. | Same as A, potentially fewer retained rows; every new allocation still needs semantic review. | Better contracts, still coarse many-to-many joins. | Better prose stability; universal IFs still pressure internal constraints into architectural rows. |
| C: boundary artifacts | B-quality assessment plus artifact grouping; dashboard contract/runtime evidence need work; reuse genuine existing artifact IFs. | Same as A if universal carriage stays. Fewer invented C/owner sites than helper seams; R remains per obligation; broad artifacts broaden impact sets. | Strong at delivered outputs, weak at locating individual renderers. | Good for stable outputs; does not by itself solve kernel/topology claims. |
| D: minimal | Item 5 cleanup, required direct-trace gaps, justified IF allocations only; keep Implements readers. | `L+C+R_optional+F_optional+O`; code extraction moves L; real interface changes affect C/O and optional R. | Most precise code-to-purpose path, with optional architecture context. | Meets core aim: moving implementation changes upward tags, never requirement rows. |
| E: selective D+B+C | D; corrected fitness review on changed obligations; artifact allocation when valuable; no internal pseudo-interface or quota. | D's formula; Q=0; derive indexes, SR ancestry and impact views; encode allocation once. | Direct purpose plus reviewed contract context; transitive IF impact means possible exposure. | Stable behavioural spine and real boundaries; topology-only claims belong in architecture. |

A lower bound shows why deleting tag syntax is not automatically a large saving.
Keeping all 302 rows means A needs **at least 302 IF–LLR edges**. With today's 206 coarse code–IF pairs, that is **508**, before new citations, Q/F/O or multiple carrying IFs.
D's present code-side total is **527 = 321 + 206**, before optional allocation/gap closure. The apparent difference is only **19**, not the 898 physical Implements lines.
This is **not an equal-completeness forecast**: A has not allocated the rows; D's scoped census misses 74 LLR targets.
Demanding complete direct coverage would add at least one citation per uncovered ID, hence **at least 74 links** within this census if all remain.
A also needs citations for new artifact contracts and otherwise unreachable obligations. A reliable final link total or hours estimate awaits real allocations.
If every scanned Python file gains a component declaration, that adds **117 sites**, common to alternatives adopting that rule; other source/artifact kinds add more.

Rewording and evidence repair are not IF-migration savings: unchanged trace design still owes them under ruling 5 and current behavioural promises.
For fit rows, A spends attachment/citation work where D may need only common cleanup; B avoids knowingly relocating defects.
For reword rows, changing their location helps only after promise and evidence align. For reframe rows, A risks immortalizing dead/architectural claims.
For artifacts, one coherent delivery seam beats call seams per emitter. For kernel cases, OI-48 supplies a reuse exemption rather than edge proliferation.

## Findings and owner decisions

**F1 — highest priority: discharge is not reachability.** SR-180's rationale defines where decomposition ends and explicitly disclaims mandatory back-links.
Item 5 requires replacing the old mechanism; “cited IF + verifying TC” proves named paths, not that implementation meets the obligation.
Decide structural completeness separately from semantic correspondence and passing evidence. Keep reviewer judgment over omissions; do not label a transitive join proof.

**F2 — ownership is not carriage.** IF-011/LLR-100 demonstrate an owned exit-code seam that cannot substitute for an interactive document.
IF-093/LLR-182 demonstrate vocabulary carriage that does not cover every outcome-selection/topology clause.
Choose selective allocation; never populate authoritative lists from owner-module joins without judging meaning.

**F3 — one home per relation.** Rule item 11 with OI-112; reject SR → IF and IF → SR lists for the same allocation.
Derive SR ancestry through IF → LLR → SR. Boundary-crossing joins provide coarse coverage, not proof that every IF there carries every SR there.
The 131 SR boundary cells and 46 crossing IF rows already provide coarse orientation; an authored IF–SR list needs additional justification.
Keep WI `needs` authored: runtime provider order does not determine build order. Optional IF references can warn of overlap, not establish dependencies.

**F4 — ownership checks can become circular.** `project-trajectory/scripts/trajectory_arch.py::contract_body_findings` currently checks stray declarations against an authored owner.
Deriving both owner and validation from citations removes independence. Typed producer/consumer citations recover roles, not independent design intent.
Keep an authored design-owner component/party ID per real IF, generate physical bindings, and review implementations against it; this needs an owner ruling.
Judge requirement-bearing allocations through approval with OI-112. All current IFs being Drafted does not make semantic migration free.

**F5 — do not invent helper contracts.** OI-48 ruled (d), a declared kernel exemption; the library-usage objection is in option-(b)'s analysis, not a universal ban on call interfaces.
`docs/kernel-modules-allow` names the reuse surface and deliberately excludes station, whose vocabulary edge remains IF-093.
Keep genuine calls such as IF-058. Neither “all kitlib is exempt” nor “every observable helper needs an IF” follows from the ruling.

**F6 — separate design smells, left unfixed.** LLR-050 remains live while asserting nothing live; LLR-159 says its red-TC census is structurally dead under the closed vocabulary.
LLR-188/197 mix placement history with behaviour: decide scope before attachment. Retain useful tests even when a requirement identity retires.
TC-029/030 point to `tests/test_agent_loop.py`, but lock tests moved to `tests/test_agent_loop_support.py`; unsupported-filesystem degradation there is absent from unconditional LLR-030.
LLR-087's endpoint oracle and LLR-100's handler-string oracle are separate defects. LLR-025's referenced suite is weaker than its TC narrative.
Spine-authoring guidance still tells authors to name LLR modules/symbols; reconcile it with the ruled migration or authors will recreate the defect.

**F7 — minimum profile and recursion need separate calls.** `project-trajectory/PROCESS.md` opening minimum-profile list omits IFs; section 8 permits skipping them for a single module.
Keep direct trace instead of a ceremonial IF. Do not introduce an undocumented second discharge policy as a minimum-profile exception.
Recursive LLR decomposition may stabilize SR altitude, but needs parent/leaf semantics, cycle checks and composition evidence; this census does not prove its need.
Decide recursion separately: postponing it does not prevent E from delivering refactor independence now.

## Hand evidence inventory

Each entry identifies bodies actually read, alongside TC method/expected/evidence metadata. It is not a TC-level inference.
This supports the stated instrument judgments and findings, not exhaustive clause coverage for every sampled row.

| LLRs | TCs | Evidence read and observation |
|---|---|---|
| 001 | 001 | `tests/test_trace.py::test_happy_chain_is_orphan_free`, `test_orphan_sr_fails_strict`: subprocess exit and report ID. |
| 004 | 004 | `tests/test_ac_advisory.py::test_unpinned_comparative_term_warns_but_never_fails`: stdout/report warning, unchanged exit. |
| 015 | 015 | `tests/test_perf_budgets.py::test_budget_referencing_unknown_id_fails_strict`: injected reference, named diagnostic. |
| 023 | 023 | `tests/test_gen_arch_map.py::test_files_mode_end_to_end_and_staleness`, `test_splice_replaces_between_markers`: output file/CLI and pure splice. |
| 067 | 067 | `tests/test_trajectory_arch.py::test_cross_cmp_import_without_seam_warns_plain_fails_strict`, `test_declared_kernel_destination_is_not_a_seam`: actual checker fixture. |
| 180 | 175 | `tests/test_check_doc_refs.py::test_llr_symbol_anchor_reds_on_a_planted_defect`: old gate bites. |
| 181 | 176 | `tests/test_bootstrap.py::test_the_common_package_ships_complete`: scaffold set plus subprocess import, not all helper policies. Additional TC-331 metadata was read, not all its bodies. |
| 184 | 179 | `tests/test_kitlib_ladder.py::test_stage_ord_is_the_position_and_RAISES_on_an_unknown_label`, `test_every_reader_resolves_to_this_one_object`: behaviour plus identity. |
| 186 | 181 | `tests/test_derive_stage.py::test_ONE_drafted_row_does_not_drop_the_effective_stage`, `test_the_check_py_STEP_goes_red_on_a_stale_cache`: derivation and wired harness. |
| 192 | 187 | `tests/test_test_evidence.py::test_check_reports_the_verdict_and_exits_nonzero_when_it_does_not_hold`, binding/residue tests: validity under input edits. |
| 006 | 006 | `tests/test_check_harness.py::test_missing_command_is_designed_failure`: direct step returns FAIL or lenient SKIP. |
| 008 | 008 | `tests/test_stack_profile.py::test_malformed_profile_fails_loudly`, threshold/missing-binary cases: CLI and step boundary. |
| 016 | 016 | `tests/test_check_stubs.py::test_strict_gates_when_stubs_present`: strict CLI and named failure. |
| 019 | 019 | `tests/test_pre_commit_hook.py::test_hook_blocks_duplicate_id_but_not_orphan`, `test_hook_secrets_floor_blocks_staged_key_with_privacy_off`: trace and shell hook. |
| 021 | 021 | Same file, `test_hook_never_runs_the_checks_on_an_older_python`: actual refusal with install guidance. |
| 098 | 101 | `tests/test_check_coverage.py::test_cli_fails_on_a_breach`: CLI report and exit. |
| 190 | 185 | `tests/test_ci_tier_declaration.py::test_reference_workflow_tiers_match_the_declaration`, `test_bite_a_retiered_workflow_step_is_caught`: structural inspection/mutation. |
| 191 | 186 | `tests/test_test_evidence.py::test_a_GREEN_run_writes_a_record_that_HOLDS`, `test_a_RED_run_writes_NOTHING`: producer with substituted harness outcome. |
| 027 | 027 | `tests/test_agent_loop.py::test_missing_cli_fails_preflight_never_hangs`, privacy-author refusal: exits before session. |
| 029, 030 | 029, 030 | `tests/test_agent_loop_support.py::test_lock_auto_released_when_holder_dies`, `test_lock_excludes_a_second_process`, contention and unsupported-filesystem cases: subprocess locks/degradation. |
| 058, 059 | 058, 059 | `tests/test_schedule.py::test_oi_edge_pending_holds_the_wi_blocked`, `test_missing_and_unknown_safetyclass_fail_closed_only_for_that_wi`, `test_cli_ready_json_matches_library`: predicate and CLI. TC-253's metadata also read. |
| 070 | 070 | `tests/test_plan_round.py::test_coverage_findings_bounce_once_then_page`, `test_budget_exhaustion_pages`: round state/disposition. |
| 071 | 071 | `tests/test_plan_briefs.py::test_assembled_brief_has_registry_material_never_sentinel`: assembled consumer text. |
| 073 | 073 | `tests/test_plan_coverage_step.py::test_clean_pass_advances_the_round`, `test_findings_repeat_after_repair_pages`, `run`: real subprocess and round integration. |
| 182 | 177 | `tests/test_kitlib_station.py::test_outcome_of_names_one_outcome_or_none`: decision, not full vocabulary-IF carriage. |
| 009 | 009 | `tests/test_profile.py::test_node_scaffold_gates_python_artifacts_and_appends_checklist`: delivered scaffold. |
| 011 | 011 | `tests/test_bootstrap.py::test_rerun_skips_existing_files`, `test_force_overwrites_existing_files`: actual subprocess. |
| 024 | 024 | `tests/test_gen_cases.py::test_pairwise_covers_all_pairs_with_documented_count`, boundary corners and TOML/CSV format cases: values and stdout. |
| 025 | 025 | `tests/test_skills_index.py::test_index_row_count_matches_skill_dirs`, `test_check_refuses_a_description_under_the_floor`: collection count and description refusal. |
| 035 | 038 | `tests/test_gen_trajectory.py::test_generates_self_contained_dashboard`: file content/offline check. |
| 087 | 089 | `tests/test_traj_views.py::test_when_view_seams_wire_to_block_ports`, `test_boundary_aggregation_dedupes_cross_component_edges`: geometry/string limits above. |
| 088, 100 | 090, 103 | Same file, `test_when_view_double_click_descends_a_layer`, `test_when_view_breadcrumb_restores_parent`: static strings, no activation. |
| 101 | 104 | `tests/test_traj_render.py::test_a2_no_focusable_node_sits_inside_a_children_presentational_svg`, role-predicate and shipped-dashboard cases: bounded walks. |
| 108 | 113 | Same file, `test_a2_every_control_name_is_present_and_not_a_bare_id`, `test_a2_landmark_names_are_distinct`: names/landmarks. |
| 120 | 125 | `tests/test_traj_graph.py::test_t8_no_wire_passes_through_an_unrelated_node_box`: sampled paths/boxes and non-vacuity. |
