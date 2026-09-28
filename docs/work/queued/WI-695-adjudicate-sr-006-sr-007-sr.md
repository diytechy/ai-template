+++
id = "WI-695"
title = "adjudicate: SR-006, SR-007, SR-009, SR-011, SR-015, SR-022, SR-024, SR-026, SR-027, SR-028, SR-031, SR-033, SR-035, SR-040, SR-043, SR-049, SR-052, SR-053, SR-054, SR-070, SR-111, SR-112, SR-113, SR-129, SR-137, SR-144, SR-146, SR-147, SR-148, SR-149, SR-150, SR-154, SR-155, SR-156, SR-157, SR-158, SR-159, SR-161, SR-162, SR-164, SR-165, SR-166, SR-167, SR-168, SR-169, SR-170, SR-171, SR-172, SR-173, SR-174, SR-175, SR-176, SR-177, SR-180, SR-181, SR-182, SR-183, SR-185, SR-186, SR-187, SR-188, SR-189, SR-190, SR-191, SR-192, SR-193, SR-194, SR-195, SR-196, SR-197, SR-198, SR-199, SR-200, SR-201, SR-202, SR-203, SR-204, SR-205, SR-206, SR-207, SR-208, SR-210, SR-211, SR-212, SR-213, SR-214, SR-215, SR-216, SR-217, SR-218, SR-219, SR-221 - approved/routed cell(s) amended on merged trunk 4719865..bcf1e9a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-006", "SR-007", "SR-009", "SR-011", "SR-015", "SR-022", "SR-024", "SR-026"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-006", "SR-007", "SR-009", "SR-011", "SR-015", "SR-022", "SR-024", "SR-026", "SR-027", "SR-028", "SR-031", "SR-033", "SR-035", "SR-040", "SR-043", "SR-049", "SR-052", "SR-053", "SR-054", "SR-070", "SR-111", "SR-112", "SR-113", "SR-129", "SR-137", "SR-144", "SR-146", "SR-147", "SR-148", "SR-149", "SR-150", "SR-154", "SR-155", "SR-156", "SR-157", "SR-158", "SR-159", "SR-161", "SR-162", "SR-164", "SR-165", "SR-166", "SR-167", "SR-168", "SR-169", "SR-170", "SR-171", "SR-172", "SR-173", "SR-174", "SR-175", "SR-176", "SR-177", "SR-180", "SR-181", "SR-182", "SR-183", "SR-185", "SR-186", "SR-187", "SR-188", "SR-189", "SR-190", "SR-191", "SR-192", "SR-193", "SR-194", "SR-195", "SR-196", "SR-197", "SR-198", "SR-199", "SR-200", "SR-201", "SR-202", "SR-203", "SR-204", "SR-205", "SR-206", "SR-207", "SR-208", "SR-210", "SR-211", "SR-212", "SR-213", "SR-214", "SR-215", "SR-216", "SR-217", "SR-218", "SR-219", "SR-221"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-006 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-006 `Coincident`: '' -> 'The needs ask for a gate that passes only when its bar is met and a pass verdict that hides no skipped check; the harne…'
- SR-007 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-007 `Coincident`: '' -> 'The need asks for a toolchain swapped by editing one declaration; the harness reading its commands from that declaratio…'
- SR-009 `Coincident`: '' -> 'The needs ask for a non-Python stack adopting the kit and a repository getting only what it uses; the set a profile see…'
- SR-011 `Coincident`: '' -> 'The need asks for a re-run that costs the adopter none of its own edits; a re-run leaving each existing file byte-uncha…'
- SR-015 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-015 `Coincident`: '' -> 'The need asks for a budget row a reviewer can trace to what it constrains; each unresolvable reference reported is that…'
- SR-022 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-022 `Coincident`: '' -> 'The need asks for documentation a reader can trust; a drifted vendored copy reported as a finding is that outcome, with…'
- SR-024 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-024 `Coincident`: '' -> 'The need asks for dimensional coverage generated rather than hand-listed; the expanded case set is that output, whole.'
- SR-026 `Boundary-Refs`: 'B-05' -> 'B-10'
- SR-027 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-027 `Coincident`: '' -> 'The need asks for a run that refuses a broken footing rather than hanging; the typed nonzero exit before the run starts…'
- SR-028 `Boundary-Refs`: 'B-05' -> 'B-09;B-10'
- SR-031 `Coincident`: '' -> 'The needs ask for one declared value per policy dial, read the same way by every enforcer; the enforcers agreeing is th…'
- SR-033 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-033 `Coincident`: '' -> 'The need asks for a release gate whose warn-tier budgets reach a reader; the emitted checklist listing each budget is t…'
- SR-035 `Coincident`: '' -> 'The needs ask for a non-Python adopter passing the registry checks unmodified; the shipped scheme carrying no language-…'
- SR-040 `Boundary-Refs`: 'B-05' -> 'B-09;B-10'
- SR-040 `Coincident`: '' -> 'The need asks for an unattended run whose per-phase sessions start as declared; routing each phase through its declared…'
- SR-043 `Coincident`: '' -> 'The need scopes this as supervision rather than security: a spawn refused, deferred or admitted per the declared dial, …'
- SR-049 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-049 `Coincident`: '' -> 'The needs ask for a gate advanced only by the work and a verdict no hand can bump; a stage derived from the artifact st…'
- SR-052 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-053 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-054 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-070 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-070 `Coincident`: '' -> 'The needs ask for generated views that cannot silently rot and cost a repository nothing it does not use; a view derive…'
- SR-111 `Coincident`: '' -> 'The needs ask for an adopter able to pick up kit updates from a known base; the stamp recording the kit commit a scaffo…'
- SR-112 `Coincident`: '' -> 'The need asks for a repository paying only for what it uses; one neutral skill source with a checked, generated per-age…'
- SR-113 `Coincident`: '' -> 'The need asks for a working gated process without hand-building the tooling; the developer setup wiring the commit floo…'
- SR-129 `Boundary-Refs`: 'B-05' -> 'B-01;B-09'
- SR-129 `Coincident`: '' -> 'The needs ask for a registry whose cells survive a change of representation; a conversion preserving every cell, and re…'
- SR-137 `Coincident`: '' -> 'The need asks for one home for every dial and a double declaration refused rather than resolved; the refusal naming the…'
- SR-144 `Boundary-Refs`: 'B-05' -> 'B-01;B-09'
- SR-144 `Coincident`: '' -> 'The need asks for parallel work whose failures leave a clean, reviewable state; a lane closed into a terminal partial s…'
- SR-146 `Boundary-Refs`: 'B-05' -> 'B-05;B-10'
- SR-146 `Coincident`: '' -> 'The need asks for prompts held to the same playbook as everything else; each prompt being a shipped file whose digest i…'
- SR-147 `Coincident`: '' -> 'The needs ask for a spine a machine can verify; one machine-parseable representation, reached by a migration proven ove…'
- SR-148 `Boundary-Refs`: 'B-05' -> 'B-05;B-09;B-10'
- SR-149 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-149 `Coincident`: '' -> 'The needs ask for authored surfaces that stay honest to the current vocabulary; each retired tag reported with its file…'
- SR-150 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-150 `Coincident`: '' -> 'The need asks for a stakeholder recognizing their outcome in each need; each offending phrase reported with its row is …'
- SR-154 `Boundary-Refs`: 'B-05' -> 'B-09;B-10'
- SR-155 `Boundary-Refs`: 'B-05' -> 'B-01;B-09;B-10'
- SR-156 `Boundary-Refs`: 'B-05' -> 'B-01;B-10'
- SR-157 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-157 `Coincident`: '' -> 'The needs ask for a chain that is mechanically verified rather than asserted, work-registry contradictions that surface…'
- SR-158 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-158 `Coincident`: '' -> 'The needs ask for documentation that cannot silently rot and a pass that hides nothing; each drift class reported at it…'
- SR-159 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-159 `Coincident`: '' -> 'The needs ask for a reviewer seeing how the parts connect from a chain that is checked; each declared-architecture gap …'
- SR-161 `Coincident`: '' -> 'The need asks for each decomposition examined from every declared perspective; the machine-readable record of each pers…'
- SR-162 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-162 `Coincident`: '' -> 'The need asks for a stakeholder seeing where each promised behaviour enters or leaves the system; each reference resolv…'
- SR-164 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-164 `Coincident`: '' -> "The need asks for an adopter telling each need's scope without inferring it; the scope value on each row, checked again…"
- SR-165 `Coincident`: '' -> 'The need asks for a repeatable explanation of the component partition; the recorded candidates, objective, scores, sele…'
- SR-166 `Coincident`: '' -> 'The needs ask for a delivered package that arrives complete and a kit held to its own template; every manifest file mat…'
- SR-167 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-167 `Coincident`: '' -> 'The needs ask for a pass verdict that hides no breached budget and budgets that cost only where adopted; failing the ba…'
- SR-168 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-168 `Coincident`: '' -> 'The needs ask for a reviewer seeing progress from one file; the one state view carrying completeness, decomposition, wo…'
- SR-169 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-169 `Coincident`: '' -> 'The need asks for a reviewer seeing how the parts connect; the navigable component and interface graph is that outcome,…'
- SR-170 `Boundary-Refs`: 'B-05' -> 'B-01;B-09'
- SR-171 `Boundary-Refs`: 'B-05' -> 'B-09;B-10'
- SR-172 `Boundary-Refs`: 'B-05' -> 'B-09;B-10'
- SR-173 `Boundary-Refs`: 'B-05' -> 'B-01;B-09'
- SR-173 `Coincident`: '' -> 'The needs ask for generated views that are never committed half-regenerated; ordered regeneration that stops at the fir…'
- SR-174 `Boundary-Refs`: 'B-05' -> 'B-01'
- SR-174 `Coincident`: '' -> 'The needs ask for ids a reader can trust to name one thing; an identity allocated at most once and not re-issued after …'
- SR-175 `Boundary-Refs`: 'B-05' -> 'B-10'
- SR-175 `Coincident`: '' -> 'The row promises the declared inclusion rule and the stated scope of consent, and deliberately claims no bound on what …'
- SR-176 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-176 `Coincident`: '' -> "The need asks for a secret or identity not republished by the kit's own records; a finding recorded by its class and lo…"
- SR-177 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-177 `Coincident`: '' -> "The need asks for a team seeing whether its parallel lanes pay off; the per-run utilisation reported from the run's own…"
- SR-180 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-180 `Coincident`: '' -> 'The needs ask for a chain verified rather than asserted; a design row reported undischarged when none of its named symb…'
- SR-181 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-181 `Coincident`: '' -> 'The needs ask for a gate that drops honestly; a stage-dropping edit required to carry its phase tag where it is authore…'
- SR-182 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-182 `Coincident`: '' -> 'The need asks for maintainers holding the kit to its own standard; the duplication count reported against its stamped b…'
- SR-183 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-183 `Coincident`: '' -> "The needs ask for maintainers holding the kit to its own standard while small changes stay cheap; each function's compl…"
- SR-185 `Coincident`: '' -> 'The need asks for an architecture that changes with the promises it serves; the change record naming the affected count…'
- SR-186 `Coincident`: '' -> "The need asks for a decomposition that stays proportionate; each additional child's recorded purpose, and the recorded …"
- SR-187 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-187 `Coincident`: '' -> "The needs ask for a stakeholder seeing where each promised behaviour crosses the boundary and a premise's landing being…"
- SR-188 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-188 `Coincident`: '' -> "The needs ask for a reviewer seeing where each outcome's delivery lands; the need reported when nothing answering it re…"
- SR-189 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-189 `Coincident`: '' -> 'The need asks for each need naming whose outcome it is; the stakeholder references resolved, and a need naming none rep…'
- SR-190 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-190 `Coincident`: '' -> 'The need asks for a need checkable against the document it was drawn from; the pointer resolving to an existing file an…'
- SR-191 `Coincident`: '' -> 'The need asks for each premise recorded once, with where its outcome lands, when it holds and what would break it; the …'
- SR-192 `Coincident`: '' -> 'The need asks for each premise recorded and checked; a stand-in recorded as a surrogate row naming the parties it answe…'
- SR-193 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-193 `Coincident`: '' -> 'The need asks for each requirement naming its premises or saying why it needs none; each requirement doing neither repo…'
- SR-194 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-194 `Coincident`: '' -> 'The needs ask for a reviewer seeing how each requirement is met; each requirement declaring no form reported is that ou…'
- SR-195 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-195 `Coincident`: '' -> 'The needs ask for a premise shown landing where its stakeholders are; each unreached need and each idle landing reporte…'
- SR-196 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-196 `Coincident`: '' -> 'The need asks for each relied-on premise being checkable; an assumption no requirement cites, or one declaring no falsi…'
- SR-197 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-197 `Coincident`: '' -> "The need asks for a premise's evidence counted apart from the system's; a test case naming the assumptions it evidences…"
- SR-198 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-198 `Coincident`: '' -> "The needs ask for an observation's result that goes stale honestly; the declaration of its inputs, lifetime and samplin…"
- SR-199 `Coincident`: '' -> 'The needs ask for each premise showing whether a current result evidences it; the observation result recorded apart, wi…'
- SR-200 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-200 `Coincident`: '' -> 'The needs ask for a premise relied on without evidence being visible as such; the evidence level derived from current r…'
- SR-201 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-201 `Coincident`: '' -> 'The needs ask for a premise shown false being reported with what relies on it; every requirement and test case relying …'
- SR-202 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-202 `Coincident`: '' -> 'The needs ask for an accepted risk that cannot quietly outlive what it accepted; the assumption read as unproven on a f…'
- SR-203 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-203 `Coincident`: '' -> 'The needs ask for an owner approving a premise for what it lets the requirements claim; the brief showing each assumpti…'
- SR-204 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-204 `Coincident`: '' -> 'The needs ask for a gate that moves only on the work; the assumption, surrogate and stakeholder tiers read at their run…'
- SR-205 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-205 `Coincident`: '' -> 'The needs ask for a boundary gate that holds each requirement to its premises; the failure naming the requirement, the …'
- SR-206 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-206 `Coincident`: '' -> 'The needs ask for a release gate that holds each relied-on premise to current evidence or an accepted risk; the failure…'
- SR-207 `Coincident`: '' -> 'The need asks for an approval act that blesses only what it shows; refusing to refresh a record while unapproved drift …'
- SR-208 `Coincident`: '' -> "The need asks for a held tier changed only by a person; the loop's own status changes refused before they land is that …"
- SR-210 `Coincident`: '' -> 'The needs ask for a reviewer seeing a machine change a human-held tier; each loop-trailered commit that changes a held …'
- SR-211 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-211 `Coincident`: '' -> 'The needs ask for a reviewer seeing, for each boundary seam, what carries its reading to an outcome; each boundary inte…'
- SR-212 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-212 `Coincident`: '' -> 'The needs ask for a gate that holds interface-form requirements to their crossings and seams; each failure naming the r…'
- SR-213 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-213 `Coincident`: '' -> 'The need asks for each perspective traceable to whose voice it is; the recorded stakeholder resolved, and an undeclared…'
- SR-214 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-214 `Coincident`: '' -> "The needs ask for an obstacle's origin being checkable; each named perspective resolved against the roster, and an unde…"
- SR-215 `Boundary-Refs`: 'B-05' -> 'B-01'
- SR-215 `Coincident`: '' -> "The needs ask for an observation's result re-judged when what it judged changes; one re-judge item filed per stale case…"
- SR-216 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-217 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-217 `Coincident`: '' -> "The need asks for the record showing a requirement's test cases approved before its implementation; each requirement im…"
- SR-218 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-218 `Coincident`: '' -> "The needs ask for a reviewer seeing each outcome's premises and whether they are evidenced; the per-need view of each a…"
- SR-219 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-219 `Coincident`: '' -> 'The need asks for a stakeholder seeing which system each promised behaviour belongs to; the system derived from a requi…'
- SR-221 `Boundary-Refs`: 'B-05' -> 'B-09'
- SR-221 `Coincident`: '' -> 'The need asks for small changes staying cheap; the tests the spine links to a module, listed from the registries with n…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-006 [project-trajectory/scripts/check.py :: steps/run_step] tests: (see TC-006) — Gate step plan + missing-tool guard
- LLR-007 [project-trajectory/scripts/check.py :: load_profile] tests: (see TC-007) — Stack profile loader
- LLR-008 [project-trajectory/scripts/check.py :: load_profile] tests: (see TC-008) — Profile validation
- LLR-009 [project-trajectory/scripts/bootstrap.py :: select_skills/matches_scope] tests: (see TC-009) — Conditional profile seeding
- LLR-011 [project-trajectory/scripts/bootstrap.py :: copy_kit_files/--force + write_kit_version] tests: (see TC-011) — Idempotent write + kit-version stamp
- LLR-014 [project-trajectory/scripts/check_perf.py :: evaluate] tests: (see TC-014) — Budget comparator

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-002 scripts/check_docs -> scripts/check: exit-code 0 pass · 1 broken link, README finding, or strict-mode orphan
- IF-003 scripts/check_flows -> scripts/check: exit-code 0 pass | 1 findings | 2 usage
