
### SR-199 — BEFORE (live registries at HEAD f17b62a30; condensed — verbatim text in the scratch dump)

SN excerpt: **SN-043** “**Scope: template (adopters + this repo).** A reviewer can see, for each stakeholder outcome, what its deliver …” · **SN-008** “A reader can believe a **pass verdict**: gates are **honest**, and a pass verdict never hides a skipped check, …” · **SN-024** “A reviewer can trust subjective/perceptual acceptance — a realistic-looking render, an artifact comparison wit …”

**SR requirement** (203 chars): The delivered process shall record each observation result apart from its test case, with its outcome, when it was observed, who or what observed it, when it expires and a digest of the inputs it judged.

**SR acceptance_criteria** (631 chars): An observation record names its observation test case and carries an outcome of pass or fail, an observation time, the person or process that observed, an expiry no later than the test case's declared lifetime after the observation, and the digest of the test case's declared inputs as judged, which is empty where the test case declares no inputs; a record missing any of these, naming a test case that is not an observation test case, or expiring later than the lifetime allows, is refused when written and fails the check when found; writing a record never edits the test case; a partly written re …


| LLR | title | module (basename) | code_symbol tokens | detail chars | identifiers | opening of detail |
|---|---|---|---|---|---|---|
| LLR-234 | The observation record: format, strict reader and atomic write | observation.py | 8 | 1047 | 18 | A kitlib module that imports no sibling script, in the pattern of kitlib/evidence.py. One TOML file per record … |
| LLR-235 | The observation writer | record_observation.py | 4 | 876 | 14 | record_observation.py --tc TC-### --outcome pass\|fail --by <provenance> [--expires <UTC>] resolves the test c … |
| LLR-236 | Records found on disk are checked | assumption_rules.py; trace.py | 1 | 506 | 7 | trace.main reads the records once after analyze, which stays free of file reads, and observation_record_findin … |

| TC | verifies | level/tier | method chars | expected (opening) | evidence files | node ids |
|---|---|---|---|---|---|---|
| TC-229 | SR-199, LLR-234, IF-214 | Unit/Smoke | 684 | Satisfies SR-199's acceptance clauses on the record's fields, the empty digest for a case … | 1 | 0 |
| TC-230 | SR-199, LLR-235, IF-215 | Integration/Full | 752 | Satisfies SR-199's acceptance: a malformed or out-of-policy record refused when written; w … | 1 | 0 |
| TC-231 | SR-199, LLR-236 | Integration/Full | 473 | Satisfies SR-199's acceptance clause that a malformed or out-of-policy record found on dis … | 1 | 0 |

### SR-199 — AFTER (proposed; full text)

**SR requirement** (211 chars): The delivered process shall keep each result of an observation test as a record of its own, apart from the test case, stating the outcome, who or what observed it, when, until when it stands, and what it judged.

**SR acceptance_criteria** (512 chars): A reader finds the latest result of an observation test as a separate record naming the case, a pass or fail outcome, the observer, the observation time, an expiry no later than the case's declared lifetime, and a digest of the inputs the case declares (empty where it declares none); a record that is incomplete, malformed, aimed at a case that is not an observation test, or expiring beyond that lifetime is reported and is not read as a result; and recording a result leaves the test case's own row unchanged.


**LLR-234** — *A result is one whole record in the observation store, or nothing* (keeps its id)  
module: `project-trajectory/scripts/kitlib/observation.py` · code_symbol: `parse/write_atomic` · detail 521 chars  
detail: Each result is one file of its own in the observation store, named by its test case and its instant, so results written on different lanes do not collide and a new sample does not edit an old one. A file is a result only when every field is present and well-formed, both instants are in the one canonical UTC form, the expiry is not before the observation and the observer is named; anything short of that reads as no result rather than as a wrong one. A write lands a whole record or leaves nothing where a reader looks.  
rationale: A half-written or hand-mangled file must evidence nothing: every way a record can be wrong gets the same answer, so no reader needs a second rule.

**LLR-235** — *One record policy, applied when a result is written and when one is found* (absorbs LLR-236)  
module: `project-trajectory/scripts/record_observation.py;project-trajectory/scripts/assumption_rules.py` · code_symbol: `record_refusal/observation_record_findings` · detail 700 chars  
detail: Results enter the store through one command, which refuses — writing nothing — a result the record policy forbids: a case the registry does not declare or that is automated, an outcome outside pass and fail, a missing observer, or an expiry later than the case's lifetime allows; it does not open the test-case registry for writing. The digest it stamps covers the case's declared inputs in their declared order and reads a file the same whatever its line endings, so only a change of content moves it. The traceability check judges each record it finds by the same policy and fails its strict run naming the file, so a record that reached the repository without the command stands on no other terms.  
rationale: Writer and checker share one predicate so they cannot disagree about what may stand; a policy enforced only at the writer would let a hand-placed record pass.

**TC-229** (keeps its id) verifies SR-199, LLR-234, IF-214 · Unit/Smoke  
method: pytest over the record module in a temporary directory; no scaffold, subprocess or git.  
expected: A whole, well-formed record reads back as the result it states, while a record missing any field, cut off mid-file, outside the canonical time form, expiring before its observation or naming no observer reads as no result, and no partly written file is visible to a reader at any moment.  
evidence: `tests/test_observation_record.py`

**TC-230** (absorbs TC-231) verifies SR-199, LLR-235, IF-215 · Integration/Full  
method: pytest over a bootstrapped scaffold, driving the writer and the traceability check as commands.  
expected: Each result the policy forbids is refused at the command with nothing written and, when planted on disk instead, fails the strict check naming the file; an admitted result leaves the test-case registry byte-identical and carries a digest that changes only when a declared input's content changes.  
evidence: `tests/test_observation_writer.py`

### SR-157 — BEFORE (live registries at HEAD f17b62a30; condensed — verbatim text in the scratch dump)

SN excerpt: **SN-002** “A reviewer can trust the chain from need to requirement to design to test because it is **mechanically verifie …” · **SN-012** “A team can keep small changes small: the process is **right-sized**, not ceremony for its own sake — small cha …” · **SN-025** “**With no human curating what comes next**, a configured LLM agent implements toward the vision — fully autono …”

**SR requirement** (361 chars): The delivered harness shall report every declared spine and work-registry rule violation — broken joins, integrity and schema faults, leftover placeholders, requirement-form findings and work-item coherence contradictions — naming the at-fault row and cell, gating the declared failure set at the declared gate while advisory classes never change the exit code.

**SR acceptance_criteria** (1026 chars): Each declared registry rule violation is reported with row-level attribution; the declared strict set exits nonzero at its gate and advisory classes never join the exit code; absent or placeholder-only optional registries and declared opt-outs are vacuous; the declared verification vocabulary (including Critique) is accepted and an unknown value fails. The declaration this is read against is the rule inventory the delivered checkers themselves publish — the id shapes, the required cells and the closed vocabularies (with the interface and component entries advisory by their own recorded ruling) …


| LLR | title | module (basename) | code_symbol tokens | detail chars | identifiers | opening of detail |
|---|---|---|---|---|---|---|
| LLR-001 | SN->SR->LLR->TC join + orphan set | trace.py | 1 | 233 | 2 | Loads the four registries, computes the orphan set (SR without LLR/TC, LLR/TC without a parent, SN without an … |
| LLR-002 | Id + registry-CSV-structure + citation integrity | trace.py | 3 | 404 | 8 | Duplicate/malformed id detection per ID_PATTERNS, a per-row column-count check over each CSV registry, and SR/ … |
| LLR-003 | Placeholder + schema checks | trace.py | 3 | 725 | 8 | -000 example-row scan and required-field + closed-vocabulary validation over the real (non-placeholder) rows, … |
| LLR-004 | Comparative-term advisory | trace_text.py | 1 | 206 | 1 | Flags an AcceptanceCriteria comparative term with no predicate marker in the cell; warn-only, never joins the … |
| LLR-005 | Off-spine integrity + back-links | trace.py | 2 | 451 | 5 | Integrity-checks the PB/REPO/PART/ASSET ids plus legacy MOD compatibility and resolves REPO/MOD DelegatedSRs a … |
| LLR-034 | WI dependency-DAG validation | check_trajectory.py | 2 | 550 | 3 | Loads the WI registry - the docs/work/ spec folder, the ONE home since the CSV home retired at concurrency-res … |
| LLR-075 | Generated-status source-of-truth guard | check_trajectory.py | 1 | 167 | 1 | Finds done WI tokens only in hand-edited status.md, with plain/strict severity, and stands down for the genera … |
| LLR-077 | WI row coherence | check_trajectory.py | 2 | 92 | 0 | Enforces Deliverable iff done on every run and resolvable open-WI SpecRef under strict mode. |
| LLR-083 | Critique verification vocabulary | trace.py | 2 | 204 | 0 | Accepts Critique as a verification value while retaining the LLR completeness requirement. An unknown Verifica … |
| LLR-084 | Critique closure ratchet | check_trajectory.py | 1 | 243 | 3 | Warns when a Critique-scoped WI closes after CHANGES-REQUESTED with no TC, test, or rubric delta. A closure fo … |
| LLR-097 | Spec-lifecycle close-side findings | check_trajectory.py | 1 | 339 | 2 | Emits R-F findings - done WI with non-empty SpecRef; live docs/specs file (README/-000 excluded, the spec_inte … |
| LLR-133 | Spine stand-alone rule | trace_text.py | 2 | 740 | 13 | provenance_findings flags a WI id or a process-doc citation across the normative cells of all three spine regi … |
| LLR-134 | Requirement form rules | trace_text.py | 1 | 536 | 3 | form_findings applies six rules — one obligation per requirement, no non-obligation modal, no actorless passiv … |
| LLR-135 | Paraphrase advisory | trace_text.py | 1 | 665 | 3 | paraphrase_advisories compares a child cell's significant words (alphabetic runs of four characters or more, l … |
| LLR-365 | Test-file declarations of their test cases | gen_arch_map.py; trajectory_arch.py | 2 | 1831 | 0 | A test-file back-link declaration names test cases, and each named id must be a live test case. In a Python te … |
| LLR-160 | The mechanical queue-overlap pre-filter | check_trajectory.py | 3 | 617 | 2 | Three signals over OPEN rows only — Jaccard over title token sets at a deliberately high bar, shared `SR-Refs` … |
| LLR-179 | EARS statement-pattern advisory | trace_text.py | 1 | 452 | 2 | ears_advisories reads the opening of each non-example SR Requirement cell and reports the row when that openin … |
| LLR-197 | The spine ROW vocabulary as one home below both modules that judge a row | spine.py | 17 | 2504 | 34 | What one registry row's cells MEAN, stated once below every reader: the three Status predicates of the closed … |
| LLR-201 | Checker cross-row coherence module below its engine | coherence.py | 9 | 1347 | 6 | Every rule of the checker that needs MORE THAN ONE ROW to have an opinion, in one module below the engine that … |
| LLR-260 | An approved test case's tier agrees with where its evidence runs | spine.py | 2 | 938 | 5 | evidence_items(cell) reads a test case's Evidence cell as (path, node) pairs: items separated by `;` or whites … |
| LLR-274 | The absolute-term advisory: an absolute in a need, requirement or design row that names no closed domain | absolute_terms.py | 7 | 1990 | 13 | absolute_advisories(needs, srs, llrs) reads the tier matrix ABSOLUTE_CELLS: a need's need and acceptance cells … |
| LLR-272 | A spine row missing its Status or Phase cell is an integrity finding and owes an act in the brief | spine.py; trace.py; baseline_snapshot.py | 4 | 906 | 7 | kitlib.spine.missing_cell_findings(tiers) takes the SN, SR, LLR and TC rows and returns one line per row and m … |

| TC | verifies | level/tier | method chars | expected (opening) | evidence files | node ids |
|---|---|---|---|---|---|---|
| TC-001 | SR-157, LLR-001 | Integration/Full | 89 | Satisfies the acceptance folded into LLR-001 (parent SR-157) | 1 | 0 |
| TC-002 | SR-157, LLR-002 | Integration/Full | 101 | Satisfies the acceptance folded into LLR-002 (parent SR-157) | 1 | 0 |
| TC-003 | SR-157, LLR-003 | Integration/Full | 226 | Satisfies the acceptance folded into LLR-003 (parent SR-157) | 1 | 0 |
| TC-004 | SR-157, LLR-004 | Unit/Full | 105 | Satisfies the acceptance folded into LLR-004 (parent SR-157) | 1 | 0 |
| TC-005 | SR-157, LLR-005 | Integration/Full | 116 | Satisfies the acceptance folded into LLR-005 (parent SR-157) | 3 | 0 |
| TC-037 | SR-157, LLR-034 | Integration/Full | 90 | Valid graphs pass; malformed ids, unknown predecessors and cycles fail with named offender … | 1 | 7 |
| TC-075 | SR-157, LLR-075 | Unit/Smoke | 60 | Hand-edited done ids warn/fail by mode; generated/open/unknown/vacuous cases stay silent. | 2 | 7 |
| TC-077 | SR-157, LLR-077 | Integration/Full | 63 | Both coherence mismatches fail every run and empty/dangling open specs fail strict; compli … | 1 | 5 |
| TC-086 | SR-157, LLR-083, LLR-084 | Integration/Full | 74 | Satisfies the acceptance folded into LLR-083 and LLR-084 (parent SR-157) | 2 | 3 |
| TC-100 | SR-157, LLR-097 | Unit/Full | 138 | Done-with-SpecRef and orphan-spec cases WARN plain (exit 0) and fail --strict (exit 1); th … | 1 | 4 |
| TC-126 | SR-157, LLR-133 | Unit/Full | 183 | Satisfies the acceptance folded into LLR-133 (parent SR-157) | 2 | 2 |
| TC-127 | SR-157, LLR-134 | Unit/Full | 211 | Satisfies the acceptance folded into LLR-134 (parent SR-157) | 1 | 1 |
| TC-128 | SR-157, LLR-135 | Unit/Full | 165 | Satisfies the acceptance folded into LLR-135 (parent SR-157) | 1 | 1 |
| TC-155 | SR-157, LLR-160 | Unit/Smoke | 264 | Satisfies the acceptance folded into LLR-160 (parent SR-157) | 1 | 0 |
| TC-174 | SR-157, LLR-179 | Unit/Full | 276 | Satisfies the acceptance folded into LLR-179 (parent SR-157) | 1 | 1 |
| TC-193 | SR-157, LLR-197 | Unit/Smoke | 1189 | Satisfies the acceptance folded into LLR-197 (parent SR-157) | 2 | 7 |
| TC-197 | SR-157, LLR-201 | Unit/Smoke | 1508 | Satisfies the acceptance folded into LLR-201 (parent SR-157) | 1 | 16 |
| TC-255 | SR-157, LLR-260 | Unit/Smoke | 967 | Satisfies LLR-260: the cell read as its path and node pairs, a bracketed parametrization k … | 1 | 9 |
| TC-270 | SR-157, LLR-272 | Integration/Full | 890 | Satisfies LLR-272 (parent SR-157): a spine row missing its Status cell, or its Phase cell … | 1 | 2 |
| TC-273 | SR-157, LLR-274, IF-252 | Unit/Smoke | 1817 | Satisfies LLR-274 (parent SR-157): the ruled cells of needs, requirements and design rows … | 1 | 0 |
| TC-275 | SR-157 | Unit/Smoke | 760 | Satisfies SR-157's advisory class for method coherence: an Inspection row whose requiremen … | 1 | 0 |
| TC-404 | SR-157, LLR-365 | Unit/Full | 312 | The declared read positions yield their test-node ids, Python levels union without a repea … | 1 | 8 |
| TC-405 | SR-157, LLR-365 | Unit/Full | 237 | Each declaration outside a permitted read position, including a pytest-fixture docstring, … | 1 | 2 |
| TC-406 | SR-157, LLR-365 | Unit/Full | 135 | Each invalid declaration, including a next line continuing a valid list, is a malformed fi … | 1 | 5 |
| TC-407 | SR-157, LLR-365 | Unit/Full | 140 | Absent, example and retired ids are unknown findings while a live id still maps and a Draf … | 2 | 2 |
| TC-408 | SR-157, LLR-365 | Unit/Full | 83 | Each unreadable test file yields an unreadable finding that names its file, line and shape … | 1 | 1 |
| TC-409 | SR-157, LLR-365, IF-131, IF-263 | Integration/Full | 200 | Each finding is a plain warning and a strict error naming file, line and shape; absent inp … | 1 | 5 |

### SR-157 — AFTER (proposed; full text)

**SR requirement** (229 chars): The delivered harness shall report each violation of a declared spine or work-registry rule naming the row and cell at fault, failing the declared gate on a gating finding while an advisory finding leaves the exit code unchanged.

**SR acceptance_criteria** (441 chars): Each violation of a declared rule is reported naming its row and cell; the gate exits nonzero only while a gating finding is present and exits zero while advisories are listed; an absent optional registry, an example row and a declared opt-out produce no finding; and the rule inventory is whatever the checkers declare at their own sites, so an unreported violation of a declared rule is a defect of this row rather than an amendment to it.


**LLR-911** — *Every rule is a pure predicate composed by one engine* (absorbs LLR-001, LLR-002, LLR-003, LLR-005, LLR-201 (the engine and its rule kinds))  
module: `project-trajectory/scripts/trace.py;project-trajectory/scripts/coherence.py;project-trajectory/scripts/trace_text.py` · code_symbol: `analyze` · detail 435 chars  
detail: A rule takes loaded rows and returns findings, each naming tier, row and cell; it reads no file, repository or argument. One engine loads the registries, runs every rule, and writes the report and the console, and nothing else calls a rule. Rules that join across rows, rules that read one row's prose, and sweeps that read the carrier itself are kept apart, so a rule's inputs say which kind it is and a new rule has one obvious home.  
rationale: A rule that performs its own reads cannot be driven in isolation, and a checker with one engine has one place where the exit code is composed.

**LLR-912** — *A finding's class, declared beside its rule, decides the exit code* (absorbs LLR-004, LLR-083, LLR-133, LLR-134, LLR-135, LLR-179, LLR-272, LLR-274 (each a rule; its class is the design decision))  
module: `project-trajectory/scripts/trace.py` · code_symbol: `exit_code` · detail 791 chars  
detail: Each rule declares whether its findings gate or advise, and the class is chosen by decidability: a decidable fault — a broken join, a duplicate or malformed id, a missing or out-of-vocabulary cell, a row carrying its own history, a requirement that is not one testable obligation — gates, while a lexical judgement about meaning — a child re-wording its parent, a condition opened outside the statement pattern, an absolute over an unnamed domain — advises. A gating finding joins the failure set of the strict flag family that owns it and fails the declared gate; an advisory is counted on the console under its own name and listed in the report, and changes the exit code under no flag. An absent optional registry, an example row and a declared opt-out produce no finding of either class.  
rationale: A reader acts on the counter's name, so an advisory sharing a gating counter would be read as a failure; a rule that gated on a lexical reading would put standing false accusations in the report.

**LLR-913** — *What a row's cells mean is defined once, below every reader* (absorbs LLR-197, LLR-260 (the shared row vocabulary and the evidence-cell reading))  
module: `project-trajectory/scripts/kitlib/spine.py` · code_symbol: `is_approved/evidence_items` · detail 542 chars  
detail: The meaning of a spine row's cells — the closed status vocabulary, which verification methods need no design row, how a phase cell parses, how a reference list splits, what an example row is, and how an evidence cell reads as test paths and nodes — is defined in one place that every reader imports: the checker, the stage derivation and the scaffolder. A reader restates none of it, so two surfaces cannot answer differently about one cell, and a test case's declared tier is judged against where its evidence runs through that same reading.  
rationale: A disagreement between the checker and the stage derivation is a false green or a false red at a gate; stating the vocabulary once makes the drift unrepresentable instead of detected.

**LLR-914** — *The work registry is one folder, read once and judged whole* (absorbs LLR-034, LLR-075, LLR-077, LLR-084, LLR-097, LLR-160 (the work-registry rules))  
module: `project-trajectory/scripts/check_trajectory.py` · code_symbol: `load_wis/validate` · detail 501 chars  
detail: Work items live in one specification folder whose directory is the item's state, and a second carrier of the same registry is itself a finding. Every coherence rule — id shape, predecessor resolution, acyclicity over hard edges, status against deliverable and specification reference, the generated status surface, the overlap pre-filter and the critique closure ratchet — reads the one loaded row set and shares its vacuity: an absent or example-only registry and a declared opt-out silence them all.  
rationale: Two readers of the work graph would dispatch two different frontiers; one loaded row set and one vacuity rule keep the checker and the scheduler on the same registry.

**LLR-915** — *A test-case declaration in a test file can only add a finding* (rewrites LLR-365)  
module: `project-trajectory/scripts/gen_arch_map.py;project-trajectory/scripts/trajectory_arch.py` · code_symbol: `read_test_tags/tc_tag_findings` · detail 378 chars  
detail: A test file declares the test cases it holds at fixed positions, read by one grammar kept apart from source-file reading. A valid declaration maps the case to its test; a misplaced, malformed, unknown or unreadable one is a finding naming file, line and shape, and no declaration can make a test disappear. Without a tests root or a test-case registry there is nothing to judge.  
rationale: A tag that silently fails to read would make a test case appear absent with nothing attributable to fix; keeping the grammar apart from source reading stops a new input from changing established source analysis.

**TC-911** (absorbs TC-001, TC-002, TC-003, TC-086, TC-193 (shipping half), TC-197 (rules half), TC-255, TC-270) verifies SR-157, LLR-911, LLR-912, LLR-913 · Integration/Full  
method: pytest over a bootstrapped scaffold, running the traceability check as a command under each strict flag family.  
expected: An orphan at any tier, a duplicate or malformed id, a mis-shaped row, a leftover example row, a missing or out-of-vocabulary status, phase or verification cell, an unresolvable citation and an approved smoke case with no smoke-tier evidence each fail the declared strict run naming the row and cell, while a fully linked, well-formed spine exits clean and an absent optional registry adds nothing.  
evidence: `tests/test_trace.py; tests/test_registry_checks.py; tests/test_snapshot_readers.py; tests/test_evidence_join.py; tests/test_trace_coherence.py`

**TC-912** (absorbs TC-126, TC-127) verifies SR-157, LLR-911, LLR-912 · Unit/Full  
method: pytest over the gating text rules with rows built in memory.  
expected: A requirement carrying two obligations, a non-obligation modal, an actorless passive, an unfalsifiable or open-ended term, or a citation of its own history fails the strict run naming row and cell, while a Drafted row, a multi-clause acceptance and a shipped script name do not.  
evidence: `tests/test_trace_rules.py`

**TC-913** (absorbs TC-004, TC-128, TC-174, TC-273, TC-275) verifies SR-157, LLR-912, IF-252 · Unit/Full  
method: pytest over the advisory rules with rows built in memory, then one planted advisory driven through the engine under every flag.  
expected: A child that re-words its parent, a requirement opening on a condition outside the statement pattern, a comparative with no predicate, an absolute over an unnamed domain and a verification method contradicting its own prose are each reported naming row and cell with the exit code unchanged under every flag, and a recorded waiver in the tier's reason cell silences the absolute-term advisory.  
evidence: `tests/test_trace_rules.py; tests/test_ac_advisory.py; tests/test_absolute_terms.py; tests/test_verification_coherence.py`

**TC-914** (absorbs TC-193 (vocabulary half), TC-255 (cell-reading half)) verifies SR-157, SR-049, LLR-913 · Unit/Smoke  
method: pytest, driving the checker, the stage derivation and a fresh scaffold through the shared row vocabulary.  
expected: The checker, the stage derivation and a fresh scaffold answer alike for a row's status, exemption, phase, references and evidence items — a whitespace-padded or differently cased cell included — and a retired status spelling is approved nowhere.  
evidence: `tests/test_rule_sync.py; tests/test_evidence_join.py; tests/test_bootstrap.py`

**TC-915** (absorbs TC-037, TC-075, TC-077, TC-086 (ratchet half), TC-100, TC-155) verifies SR-157, LLR-914 · Integration/Full  
method: pytest over registries built in temporary work folders, the plain and strict runs as commands.  
expected: A malformed or duplicate work-item id, an unresolved predecessor, a hard-edge cycle, a done item that still cites a specification or lacks a deliverable, an open item with a dangling specification reference and a done id hand-written into the status surface are each named, warning in the plain run and failing the strict one where the rule gates; the overlap pre-filter and the critique ratchet report on the warn-only line; and an absent or example-only registry, a declared opt-out and the generated status marker are silent.  
evidence: `tests/test_trajectory.py; tests/test_trajectory_staged.py; tests/test_trajectory_forward_only.py; tests/test_loop_order.py`

**TC-916** (absorbs TC-005) verifies SR-157, LLR-911 · Integration/Full  
method: pytest over scaffolds carrying each optional off-spine registry.  
expected: A budget, repository, part or asset row whose reference resolves to no requirement, design row or module fails the integrity run naming it, and an absent optional registry or an example row adds no finding.  
evidence: `tests/test_modules_registry.py; tests/test_procurement.py; tests/test_assets.py`

**TC-917** (absorbs TC-404, TC-405, TC-406, TC-407, TC-408, TC-409) verifies SR-157, LLR-915, IF-131, IF-263 · Integration/Full  
method: pytest over tagged test trees and a bootstrapped scaffold, in plain and strict modes.  
expected: A valid test-case declaration maps to its test; a misplaced, malformed, unknown or unreadable one is reported naming repository-relative file, line and shape, warning below the implementation rung and failing at it; and a tree with no tests root or no registry yields nothing.  
evidence: `tests/test_gen_arch_map.py; tests/test_trajectory_arch.py`

### SR-156 — BEFORE (live registries at HEAD f17b62a30; condensed — verbatim text in the scratch dump)

SN excerpt: **SN-027** “A team gets more than one piece of ready work moving at once: ready work **fans out across bounded parallel la …” · **SN-008** “A reader can believe a **pass verdict**: gates are **honest**, and a pass verdict never hides a skipped check, …” · **SN-025** “**With no human curating what comes next**, a configured LLM agent implements toward the vision — fully autono …”

**SR requirement** (507 chars): The delivered loop content shall run exactly one work item per lane on bounded, mutually isolated lanes and narrow every lane back to the integration branch through one serial, fail-closed seam that runs the declared bar on the composed tree — parking a red candidate and stopping the queue loudly, draining claiming to a clean merged stop under a declared pause, and reconstructing claim and queue state from version-control history alone at any crash boundary, never a half-integrated authoritative state.

**SR acceptance_criteria** (1665 chars): Every executable lane claim names exactly one work item; empty or multi-item claim, assignment and resume inputs refuse before changing state, while historical multi-item records remain readable as evidence and are never run as claims. A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated working trees, and a single-lane setting preserves the serial semantic; a finished branch reaches the integration branch only through the serial seam with the declared bar green on the composed tree — a red parks the candidate and stops the queue loudly; a declar …


| LLR | title | module (basename) | code_symbol tokens | detail chars | identifiers | opening of detail |
|---|---|---|---|---|---|---|
| LLR-138 | Tracked pause reader (dual-home) | agent_common.py | 2 | 433 | 4 | pause_reason reads the ONE tracked home docs/work/pause via tracked_pause (TOML reason/since; malformation fai … |
| LLR-140 | Local integrator (claim + queue + audit) | integrate.py | 6 | 3470 | 26 | claim: when the coordinator context guard is enabled and the claim does not hold the dispatch lock (the live d … |
| LLR-145 | Link-aware spec-move ritual (move + relink indivisible) | spec_move.py | 5 | 911 | 3 | move_spec moves a registry/spec file and keeps every markdown link in the repo true as ONE indivisible operati … |
| LLR-150 | Lane mechanics: worktree, worker subprocess, §A2 refresh subprocess | dispatch.py; lane.py | 7 | 1122 | 8 | One lane's mechanics extracted from the dispatcher (docs/concurrency-v2.md §A4.2): ensure the lane worktree (i … |
| LLR-151 | Dispatch-lock ownership and single-WI claim | integrate.py; bookkeeping.py | 6 | 1143 | 8 | The §A4.1 authority flip's integrator half (docs/concurrency-v2.md §A4.1): _claim_refusal's safety_class != or … |
| LLR-207 | The verdict record: what carries a governing verdict, and what binds it to the tree it judged | verdict.py; station.py; integrate.py | 41 | 6977 | 41 | tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ an … |
| LLR-262 | The record a merge judges stays as its author committed it | verdict.py; done_when.py; agent_loop.py; agent_brief.py; integrate.py; intake.py | 29 | 4942 | 40 | The coordinator's session log records each session's phase and its exact commit range (`# commits: before..aft … |
| LLR-307 | A Done-when blessing binds the exact changed checklist | done_when.py | 19 | 3434 | 10 | bound_items reads each current Done-when item that only ticks or evidences a claim-time item as that claim-tim … |
| LLR-308 | Done-when adjudication brief binds its claim and context | adjudicate_brief.py | 3 | 675 | 7 | The done-when class accepts exactly one work item in Adjudicates, reads its claim at the lane integration base … |
| LLR-309 | Changed Done-when text is held at every build, close and merge transition | agent_loop.py; integrate.py | 4 | 1054 | 5 | After routed_session selects a build or rework session, build_hold asks LLR-307's lane_hold and returns the wo … |
| LLR-339 | The trunk is one declared name | agent_common.py; bootstrap.py | 5 | 1152 | 0 | The integration branch is named by one declaration in the policy home, read by every reader that needs the tru … |

| TC | verifies | level/tier | method chars | expected (opening) | evidence files | node ids |
|---|---|---|---|---|---|---|
| TC-131 | SR-156, LLR-138 | Unit/Full | 194 | Satisfies SR-156 AcceptanceCriteria via the LLR-138 detail contract | 1 | 2 |
| TC-132 | SR-156, LLR-140, LLR-207 | Unit/Full | 1247 | Satisfies SR-156 AcceptanceCriteria via the LLR-140 claim/integration contract and the LLR … | 4 | 0 |
| TC-139 | SR-156, LLR-145 | Unit/Full | 941 | Satisfies SR-156 AcceptanceCriteria via the LLR-145 detail contract | 2 | 1 |
| TC-144 | SR-156, LLR-150 | Integration/Full | 914 | Satisfies SR-156 AcceptanceCriteria via the LLR-150 detail contract | 1 | 0 |
| TC-145 | SR-156, LLR-151, IF-186 | Unit/Full | 1879 | Satisfies SR-156 AcceptanceCriteria via the LLR-151 detail contract | 2 | 0 |
| TC-205 | SR-154, SR-156, LLR-140, LLR-207, LLR-262, IF-175 | Unit/Full | 15874 | Satisfies SR-156: the serial seam's verdict rung is computed from committed evidence a log … | 5 | 89 |
| TC-257 | SR-154, SR-156, LLR-262, IF-242 | Integration/Full | 1780 | Satisfies LLR-262: a review session's range may change only its verdict file, checked righ … | 6 | 19 |
| TC-259 | SR-154, SR-156, LLR-262, IF-242 | Unit/Smoke | 1185 | Satisfies LLR-262's pure rules: only the REVIEW session's own verdict file is in scope; th … | 2 | 0 |
| TC-317 | SR-156, SR-229, LLR-300, LLR-140, IF-271, IF-272, IF-273, IF-274, IF-275 | Integration/Full | 705 | Every guarded route to a new claim refuses after the threshold, without blocking close-out … | 4 | 20 |
| TC-325 | SR-156, LLR-307, LLR-309, IF-286 | Integration/Full | 3885 | An in-lane changed Done-when holds subsequent build or rework dispatch, staged close and s … | 3 | 33 |
| TC-326 | SR-156, LLR-307, LLR-309, IF-286 | Integration/Full | 1486 | Only an accepted, bound, valid verdict whose call succeeded, or an owner ruling that binds … | 1 | 22 |
| TC-327 | SR-156, SR-232, LLR-308, LLR-310, IF-115, IF-287 | Integration/Full | 1817 | The done-when brief displays the claim-bound checklist, changes, digest and bounded Contex … | 3 | 26 |
| TC-328 | SR-156, LLR-262, IF-286 | Integration/Full | 1038 | Merge handles all four LLR-262 Done-when arms: uncovered mint, including an invalid sittin … | 1 | 10 |
| TC-369 | SR-156, LLR-339, IF-179, IF-189 | Integration/Full | 1010 | The declared branch is read without consulting the current checkout or worktree list; ever … | 9 | 15 |
| TC-370 | SR-240, LLR-340, SR-156, LLR-140, SR-229, SR-237, LLR-300, IF-297 | Integration/Full | 890 | An inactive commit floor makes each agent route refuse before work and name the applicable … | 3 | 25 |

### SR-156 — AFTER (proposed; full text)

**SR requirement** (550 chars): The delivered loop content shall run each claimed work item on its own isolated lane, up to the configured lane ceiling, and land every lane through one serial, fail-closed seam that admits only a tree on which the declared bar and the declared independent review are green — parking a red candidate and stopping the queue loudly, draining to a clean stop under a declared pause, holding a lane whose own completion checklist changed until that change is blessed, and recovering claim and queue state from version-control history alone after a crash.

**SR acceptance_criteria** (694 chars): With independent ready work and a lane ceiling of N, N lanes run at once in separate working trees and a ceiling of one keeps the serial behaviour; a claim names exactly one work item and refuses before changing anything otherwise; nothing reaches the integration branch except through the seam, which refuses — naming the reason — a tree whose bar is red, whose review evidence is absent, partial, stale or dissenting, or whose completion checklist changed without a blessing, and parks the candidate; a declared pause stops new claims while in-flight lanes still land; and after a kill at any step a restart re-derives each claim and queue entry from history with no work item assigned twice.


**LLR-901** — *Claim, finish and outcome are facts of the tree* (absorbs LLR-138, LLR-140 (claim, queue, audit), LLR-150, LLR-151)  
module: `project-trajectory/scripts/integrate.py;project-trajectory/scripts/dispatch.py;project-trajectory/scripts/lane.py` · code_symbol: `claim/finished_branches` · detail 932 chars  
detail: A claim is one commit that moves one queued work specification into the lane's active folder and cuts the branch; a lane is finished when its tip holds no specification there; and its outcome is the terminal folder the specification moved to. The dispatcher decides and a lane runs — one working tree, one worker process and the lane's own refresh of the bar — so a ceiling of one is the ordinary serial loop and concurrency is a table size, not a second path. A claim refuses before any write: a tracked pause, a claim lock held by a live dispatcher, an unsafe branch name, a specification that is not exactly one readable file, an empty or multi-item input, an item off the ready frontier. A declared pause is a tracked file read fail-closed that stops claims and nothing else. No state file and no back-channel exist; the tree and exit codes are the whole protocol, which is what lets a restart re-derive each claim from history.  
rationale: A protocol kept in the tree is recovered by reading the tree; a state file beside it is a second truth that a crash can leave disagreeing with the first.

**LLR-902** — *A lane lands only when the integration branch is already its ancestor* (absorbs LLR-140 (integrate_one and audit))  
module: `project-trajectory/scripts/integrate.py` · code_symbol: `integrate_one` · detail 645 chars  
detail: The seam admits a branch only when the integration branch is an ancestor of it, so a merge conflict is unrepresentable and the composed tree is the branch tree: the bar runs once per lane, on the branch at its refresh, and a red refresh is attributable to the lane that caused it. The seam reads the bar's result and the review verdict off that tree fail-closed — a nonzero exit or any skipped step refuses — and lands with a non-fast-forward merge, deleting the branch on green and parking the candidate and stopping the queue on red. A window audit names any commit in the landing window that touched product paths outside the bookkeeping set.  
rationale: Requiring ancestry moves composition failures to the refresh, where they are attributable, instead of to a candidate worktree where they would need a conflict arm and a half-merge to park.

**LLR-903** — *Moving a specification and fixing every link to it is one changeset* (rewrites LLR-145)  
module: `project-trajectory/scripts/spec_move.py` · code_symbol: `move_spec` · detail 356 chars  
detail: A specification moves between work folders together with every link that pointed at it and every link it carries, re-aimed and staged in the same changeset, so the two-thirds state — moved but not relinked — cannot exist. A crashed claim's own relink writes are recognised as such and excused when the claim is re-cut, while any other edit to prose is not.  
rationale: A bare move strands both link directions and the break surfaces late, on the composed tree; a constraint that leaves the broken state unrepresentable beats a check that detects it afterwards.

**LLR-904** — *A verdict counts only while it names the tree it judged* (absorbs LLR-207, LLR-262 (review half))  
module: `project-trajectory/scripts/kitlib/verdict.py;project-trajectory/scripts/integrate.py;project-trajectory/scripts/agent_loop.py` · code_symbol: `tree_identity/governing_rev` · detail 977 chars  
detail: The identity of a lane's work is a digest of its tree with the record paths — reviews, logs, iteration notes — left out, so a verdict names that identity and counts only while it is unchanged; there is no ordering rule and no time comparison. One reader answers both questions asked of the evidence — may this branch land, and which review phase does this lane still owe — over the same declared phase count, so the two cannot disagree. Review evidence is a round read as the session that produced it committed it, joined to that session's log for its phase and scope, and a dissent counts as served while refusing the landing. Machine-authored commits that move the tree without changing what the lane claims — the bar refresh and the machinery's own close of an adjudicated row — are verified as such and seen through, and each unverified case resolves toward more review. A trailer written back onto the commit is a cross-check that can refuse but cannot create an approval.  
rationale: A verdict judged by commit time or by position promotes an approval of earlier work onto later work; binding it to the tree it saw answers staleness directly and lets two readers share one answer.

**LLR-905** — *A completion checklist is fixed at claim and released only by a blessing* (absorbs LLR-307, LLR-308 (hold-relevant half), LLR-309, LLR-262 (Done-when half))  
module: `project-trajectory/scripts/kitlib/done_when.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/integrate.py` · code_symbol: `blessing_owed/lane_hold` · detail 786 chars  
detail: Each claimed item's completion checklist is read at the claim and compared with its current text with ticks and appended evidence in the closed form stripped, so a tick with evidence is not a change and any other rewording, narrowing, deletion or addition is. One predicate — the item's id with the digest of its carried checklist — is asked at the lane's next build dispatch, at a hand close, at the landing and at an ordinary commit on the integration branch, and is released only by an accepted verdict or an owner ruling that binds that exact digest; a later change owes a fresh blessing. The commit that makes the change, review and critique sessions, adjudication rows and test runs are not held; an unreadable claim or current copy holds naming why, and an absent claim releases.  
rationale: A release condition that a lane can keep consuming its changed goalpost through is no condition; one predicate at every transition makes the verdict or ruling the sole release without forbidding the edit that creates the obligation.

**LLR-906** — *The integration branch is one declared name* (rewrites LLR-339)  
module: `project-trajectory/scripts/agent_common.py;project-trajectory/scripts/bootstrap.py` · code_symbol: `trunk_name` · detail 485 chars  
detail: Every reader that judges or writes against the integration branch takes its name from one declaration in the policy home and does not infer it from the branch a checkout is on, so a linked working tree and a single checkout agree about the same branch; an absent, empty, non-text or non-local declaration is refused by name by each such reader. A new scaffold writes the branch it is created on into a policy configuration it creates itself and leaves an adopter's existing file alone.  
rationale: Guessing the trunk from a checkout lets linked worktrees and single checkouts disagree about the same integration branch.

**TC-901** (absorbs TC-131, TC-132 (claim and station half), TC-144, TC-145) verifies SR-156, LLR-901, IF-186 · Integration/Full  
method: pytest over real git repositories, the dispatcher and the integrator driven with the real bar.  
expected: Independent ready work runs on as many lanes as the ceiling allows; each claim moves exactly one specification in one commit and refuses by name, before anything is written, an empty or multi-item input, a pause, a held claim lock or an unsafe name; a finished lane is detected from its tree; a pause lets in-flight lanes land and stops new claims; and a kill at any lifecycle step is resumed from history with no item assigned twice.  
evidence: `tests/test_dispatch.py; tests/test_integrate.py; tests/test_integrate_admission.py; tests/test_bookkeeping.py; tests/test_agent_loop_policy.py`

**TC-902** (absorbs TC-132 (verdict and attest half), TC-205) verifies SR-156, SR-154, LLR-902, LLR-904, IF-175 · Integration/Full  
method: pytest over two-branch git fixtures with the integration branch checked out, the seam and both evidence readers driven on the same trees.  
expected: A branch lands only with the integration branch already its ancestor, its refreshed bar green and a verdict from a logged reviewer session naming its current identity; a red bar parks the candidate and stops the queue; a verdict naming an earlier tree, a dissent, a missing phase, a narrow or retained-session round, or a trailer contradicting the rounds refuses by name; a verified refresh or mechanical close moves the tip without re-owing a round; and the loop and the seam give one answer about what the lane owes.  
evidence: `tests/test_verdict_record.py; tests/test_integrate_station.py; tests/test_bar_attestation.py; tests/test_integrate_attest.py`

**TC-903** (rewrites TC-139) verifies SR-156, LLR-903 · Unit/Full  
method: pytest over fixture trees and a real repository, the move driven with and without its relink half.  
expected: An archival move leaves every inbound and outbound link true and the documentation check green, the same move without its relink half fails that check, and a crashed claim whose only extra writes are its own relinks is re-cut while one with any other prose edit is convicted.  
evidence: `tests/test_spec_move.py; tests/test_integrate.py; tests/test_handback.py`

**TC-904** (absorbs TC-257, TC-259) verifies SR-156, SR-154, LLR-904, IF-242 · Integration/Full  
method: pytest over git repositories and the loop driven with a fake agent.  
expected: A review session's range may change only its own verdict file — any other path stops the run for a human or refuses the landing by name from the committed logs; a later rewrite of a round or of a session log changes nothing the seam counts; an uncommitted verdict is not acted on; and a review whose leftovers cannot be stashed stops the run with nothing re-drawn.  
evidence: `tests/test_review_scope.py; tests/test_agent_loop_review.py; tests/test_agent_loop_critique.py; tests/test_verdict_record.py`

**TC-905** (absorbs TC-325, TC-326, TC-327 (hold half), TC-328) verifies SR-156, LLR-905, IF-286 · Integration/Full  
method: pytest over git fixtures holding a claimed specification, each hold point driven with and without a binding blessing.  
expected: A lane that rewords, narrows, deletes or adds a checklist item is held at its next build dispatch, at a hand close, at the landing and at an ordinary trunk commit until an accepted verdict or owner ruling binds that exact text, while a tick with evidence, the editing commit itself, a review or adjudication session and a test run are not held; the uncovered change is minted as an adjudication at the landing and a covered one is not.  
evidence: `tests/test_done_when_blessing.py; tests/test_done_when.py; tests/test_intake.py`

**TC-906** (rewrites TC-369) verifies SR-156, LLR-906, IF-179, IF-189 · Integration/Full  
method: pytest over repositories with and without the declaration, in single checkouts and linked working trees, plus a fresh scaffold.  
expected: The declared branch is read without consulting the current checkout; each absent, empty, non-text or non-local declaration is refused by name by every reader that judges or writes against the integration branch; a linked working tree on that branch is judged as it; and a fresh scaffold records the branch it was created on while an existing policy file keeps its value.  
evidence: `tests/test_trunk_name.py; tests/test_done_when_blessing.py; tests/test_bootstrap.py; tests/test_process_config.py; tests/test_step_path_trigger.py`