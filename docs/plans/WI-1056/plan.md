# WI-1056 plan, revision 1: F-3's five unblessed rows re-landed under an amended SR-221, and SR-248's chain repaired

Written in the worktree `D:/ai-template-wt-wi1056`, branch `maint/wi-1056`, head `3c33b3783` (cut from trunk `refactor_again`). `planmode = "single"`: this plan settles the choices before any edit; the build waits for the coordinator's go-ahead.

Read in full: the spec `docs/work/queued/WI-1056-answer-wi-1055-verdict.md`; its specref, the third sitting's verdict `docs/reviews/wi-1055-adjudicate-third-sitting/001-ADJUDICATE-982063e.md`; its scope critique `docs/reviews/2026-11-22-scope-critiques/WI-1056.md`; the five reverted cells at `8e08b3029`; the live rows SR-157, SR-212, SR-221, SR-248, LLR-201, LLR-244, LLR-263, LLR-403 to LLR-407, LLR-153, LLR-199, LLR-204, TC-239, TC-258, TC-466 and TC-480 to TC-484; WI-1018's spec. Code read: `arch_inputs.implements_index`, `gen_arch_map.backlink_ids`, `scan_backlinks` and `_walk_roots`, `kitlib.config.declared_headers`, `arch_tags.generated_evidence`, `evidence_regen` and `write_evidence`, `trace._cmd_tests_for` and `_cmd_regen_evidence`, `kitlib.spine.llr_placement`, `unplaced_llrs`, `module_tests` and `resolve_modules`, `trace_text.placement_line`, `traj_parse.placed_llrs`, `intake._placement` and `_code_map_lines`, `check_trajectory._placed_sr_components`, `assumption_rules.if_reached_srs`, `component_srs` and `interface_form_gate_findings`, `arch_interfaces.contract_homes`, `check_assumption_gate.step_findings`, `coherence.spine_orphan_findings`, `spine_carrier.undeclared_key_findings` and `load`, `acceptance_record.SPINE_TRACED_CELLS` and `spine_cell_class`, `migrate_carrier.drop_llr_trace_cells`. Tests read: `tests/test_llr_trace_cells.py`, `tests/test_if_owner_component.py` (TC-466), `tests/test_assumption_gate.py` (TC-239's arm), `tests/test_evidence_join.py` (TC-258), `tests/test_trace.py::test_draft_llr_is_exempt_from_tc_rule`, the context-block tests in `tests/test_intake.py` and the pack-citation tests in `tests/test_trajectory_arch.py`.

## Rules this plan holds every row to

- **No code name in row text.** In every cell this branch writes, a function, file, flag, step or test name gives way to contract terms ("the regeneration command", "the architecture arm's step"). That includes the code names the accepted text of LLR-244, TC-239 and TC-258 already carries and the `8e08b3029` text kept: the re-landed cells drop them rather than carry them forward. Registry column names (`SR-Refs`, `DA-Refs`, `BridgedBy`, `Coincident`, `EffectAt`, `Boundary-Refs`, `Verifies`, `Evidence`) and the stage tokens (`DevStg-Arch`, `DevStg-Boundary`) stay: they are the schema's and the ladder's vocabulary.
- **One obligation per new or rewritten row, every clause tested.** One `shall` per SR; no unbounded absolute in an acceptance criterion; each clause of a new or rewritten LLR driven by a test its TC names, or cut.
- On the six `Accepted` rows (SR-212, SR-221, LLR-244, LLR-263, TC-239, TC-258) only text changes; every new or rewritten row is `Drafted`. No status flips, no snapshot.

## Ids

Minted from the launch ranges, then `trace.py --root . --bump-ids`:

| Id | What it is |
|---|---|
| SR-249 | design-row placement (from SR-248) |
| SR-250 | the files realizing a design row read from the code's back-links (from SR-248's acceptance) |
| SR-251 | generation of a test case's evidence parts (LLR-406's new parent) |
| LLR-408 | design-row discharge (from LLR-403) |
| TC-485 | verifies SR-248 and LLR-408 (discharge) |

SR-252, LLR-409 to LLR-412 and TC-486 to TC-495 stay unminted.

## 1. SR-248's split

SR-248 holds two `shall`s and a third obligation in its acceptance (verdict: "two separate obligations ... omits back-link file reading from Requirement while putting it in AcceptanceCriteria ... uses an unbounded absolute ('never fails a check')"). It becomes three rows of one obligation each.

**No existing SR states the back-link reading.** I searched the requirement registry for back-link, `Implements` and tag in title, requirement and acceptance. The near misses: SR-163 maps shipped files to needs through the shipped-file inventory, and its child LLR-204 owns the declaration grammar but says its own report "asks whether each live design row is NAMED by some source declaration", not which files realize a row; SR-159 reports connectivity gaps; SR-212 and SR-221 (as amended below) read the back-links for their own outcome but state no reading for every reader. So the reading takes a new row, SR-250.

**SR-248 keeps discharge.** Its rationale's first paragraph, its coincident and the retired SR-180 it replaced are all about discharge; placement and the back-link reading leave.

### SR-248 (Drafted, rewritten): discharge

- title: "A design row past Drafted is discharged by a test case verifying it"
- requirement: "The delivered harness shall report as undischarged each design-tier row past its Drafted status that no live test case verifies."
- acceptance_criteria: "A design row that at least one live test case verifies, of any verification kind, is discharged and is not reported; one past Drafted that none verifies is reported by the orphan rules naming the row, and the strict check exits nonzero for it; a Drafted row that none verifies is not reported while it stays Drafted."
- rationale: the current first paragraph (the bottom rung's claim is discharged by evidence of the row's own kind; a Drafted row makes no claim yet; binding discharge to a code symbol pointed down at the code), less its forward-looking sentence on interface-realization discharge.
- sn_refs `["SN-002"]` (was SN-002 and SN-003; SN-003 goes to SR-250, whose text-read-in-any-language property it was cited for). boundary_refs `["B-09"]`, hat_refs `["TEST-ENGINEER"]`, unchanged.
- coincident, kept: "The needs ask for a chain verified rather than asserted; a design row reported undischarged when no test case verifies it is that verification's verdict."
- Decomposed by **LLR-408** (new, section 3); verified by **TC-485** (new).

### SR-249 (Drafted, new): placement

- title: "Where a design row sits is derived from the interfaces its verifying test cases name"
- requirement: "The delivered harness shall derive the components each design-tier row sits in from the interfaces its verifying test cases name, counting a row placed in none as unplaced rather than refusing it."
- acceptance_criteria: "A design row is placed at the owner component of each interface that a test case verifying it names, once per component; an interface owned by an external party places nothing, and a row placed at several components is placed at each. The generated component view lists each placed row in its components and each unplaced row in its unplaced table, the state view shows each design row's components or that it is unplaced, and the strict check's report counts the placed and the unplaced rows; a row's being unplaced changes no check's exit code."
- rationale: SR-248's second paragraph (placement follows from what a row is verified at; a row placed nowhere is a decomposition whose interface is not yet named, legal and visible) and LLR-403's reason (a row naming its component restated by hand a fact the interfaces and cases hold, and the copy drifted).
- sn_refs `["SN-002", "SN-023"]`: SN-002 for the derived, never-restated link; SN-023 ("how its parts connect") because the component and state views are where placement is read. boundary_refs `["B-09"]`, hat_refs `["MAINTAINER"]`, aspect `trajectory`, priority M, verification Test, phase 6.
- coincident: "The needs ask for a chain verified rather than asserted and a view of how the parts connect; each design row shown at the components its verifying cases' interfaces are owned by, derived rather than restated, with an unplaced row counted in view, is that view as the reviewer reads it."
- Decomposed by **LLR-403** (re-pointed from SR-248); verified by **TC-480** (re-pointed from SR-248).

### SR-250 (Drafted, new): the back-link reading LLR-405 serves

- title: "The files realizing a design row are read from the code's back-link declarations"
- requirement: "The delivered harness shall take the files realizing each design-tier row only from the back-link declarations on the declared source surface."
- acceptance_criteria: "A file on the declared source surface whose back-link declaration names a design row is read as realizing that row, and a mention of the row's id that is not a declaration is not; a row no declaration names is read as realized by no file; an absent source root, or a file that cannot be read as text, contributes no file and the rest of the surface is still read."
- rationale: SR-248's third paragraph (nothing obliges source to carry a back-link; read where present), and why the cells went: the file and symbol cells pointed down at facts the back-links already stated upward, and drifted. No "never demanded" absolute: the back-link coverage report (LLR-204) can gate under its own declared threshold, so the row says only what is read.
- sn_refs `["SN-002", "SN-003"]`: SN-002 for a trace read from the code rather than hand-kept; SN-003 because the declarations are read as text, holding on any stack with no parser. boundary_refs `["B-09"]`, hat_refs `["MAINTAINER"]`, aspect `trajectory`, priority M, verification Test, phase 6.
- coincident: "The needs ask for a chain verified rather than hand-maintained and a process that holds on any stack; the files a design row is realized in, read as text from declarations the code itself carries, with no copy kept on the row, is that link as a reader receives it."
- Decomposed by **LLR-405** (re-pointed from SR-248); verified by **TC-482** (which gains SR-250 in `verifies`).

### Re-pointing, all on Drafted rows

| Row | Cell | Before | After |
|---|---|---|---|
| LLR-403 | sr_refs | SR-248 | SR-249 |
| LLR-405 | sr_refs | SR-248 | SR-250 |
| LLR-406 | sr_refs | SR-157 | SR-251 (section 2) |
| TC-480 | verifies | SR-248, LLR-403 | SR-249, LLR-403 |
| TC-482 | verifies | LLR-405, LLR-263 | SR-250, LLR-405, LLR-263 |
| TC-483 | verifies | SR-157, LLR-406 | SR-251, LLR-406 |

No `Accepted` row's `sr_refs` or `verifies` moves, so the branch owes no routed traced change. The code's back-link declarations that name SR-248 beside LLR-403 or LLR-405, and SR-157 beside LLR-406, move to the new parents (docstring lines in `arch_inputs.py`, `gen_components.py`, `kitlib/spine.py`, `trace_text.py`, `traj_parse.py`, `arch_tags.py`, `trace.py`), and the orphan pass's design-row rule in `coherence.py` gains `SR-248, LLR-408`.

## 2. The SR stating generation for LLR-406

**No existing SR states generated registry content.** I searched every requirement for generate, derive, regenerate, rewrite, in place and evidence. The candidates and why each fails:

- SR-070: "The delivered generator set shall derive each artifact it produces from the tracked registries alone ...". Its artifacts are views declared generated, freshness-gated and derived *from* registries; the evidence column is a registry's own content, derived from test files, and no generated-artifact freshness step holds it.
- SR-112 (per-agent skill copies a generated fan-out of one source) and SR-173 (shared regeneration ordered, no partial result) are about other artifacts.
- SR-247 (a migrator rewriting earlier vocabulary in place) and SR-036 (re-sync) rewrite for upgrades, not from declarations.

So a new row, **SR-251**:

- title: "A test case's evidence parts under the tests root are generated from the test files' declarations"
- requirement: "The delivered harness shall, on request, rewrite the parts of each test case's evidence cell under the declared tests root as the test files' declarations of that case make them, keeping every other part as written."
- acceptance_criteria: "A tests-root part a declaration names is kept, one no declaration names is removed, and a declared test the cell lacks is added; a part outside the tests root, a note, and a part in a file whose declarations cannot be read stay as written; only those cells of the test-case registry change, and a rewrite that would change anything else is refused with nothing written; a run over cells already current changes nothing; with no test-case registry or no tests root nothing is written and the missing input is reported."
- rationale: LLR-406's (a test case's tests were named in two homes, held equal by a check that asked a person to edit the cell); the strict check's evidence rule, under SR-157, stays the check that the column is current, so generation and checking are two obligations.
- sn_refs `["SN-002"]` (a trace generated from the tests' own declarations, not hand-kept). boundary_refs `["B-09"]`, hat_refs `["INTEGRITY-RECOVERABILITY"]` (an in-place writer refusing a rewrite it cannot prove), aspect `trajectory`, priority M, verification Test, phase 6.
- coincident: "The need asks for a chain mechanically verified, not hand-maintained; a test case's evidence written from the test files' own declarations is that trace as the reviewer reads it."

**Why not SR-157.** SR-157: "The delivered harness shall report every declared spine and work-registry rule violation ... naming the at-fault row and cell, gating the declared failure set at the declared gate while advisory classes never change the exit code." Its obligation is a finding at a severity, and its acceptance is findings and exit codes. LLR-406 writes a registry in place and reports no violation; it has no severity and no gate. The equality rule that reports a stale cell (LLR-365, LLR-395) stays under SR-157. That rule is the check; SR-251 is the writer.

## 3. LLR-403, LLR-408 and the placement consumers

### LLR-403 keeps one decision: placement

Its discharge sentence leaves (below). Its reader list is cut to what LLR-403 itself delivers and TC-480 verifies.

- detail: "For each pair of a test case and a design row its verifies cell names, the row is placed at the owner of each interface the same case names, where that owner is a component; an interface owned by an external party places nothing, and a row placed at several components is placed at each. Example rows are not read. A row no case places is unplaced. The generated component view lists each placed row in its components and each unplaced row in its unplaced table, counted in its census; the state view's design-row detail shows a placed row's components and the word unplaced for the rest; and the strict check's report prints one line counting the placed and unplaced rows, naming the first ten unplaced and counting the rest. Being unplaced changes no exit code."
- title and rationale unchanged (both already cover placement only).

**Consumers kept and verified (TC-480):**

| Consumer | Status today | Test |
|---|---|---|
| The derivation itself | verified | existing `test_a_design_row_is_placed_through_the_interfaces_its_cases_name` |
| The component view's placement and unplaced table | verified | same test (`gen_components.build`) |
| The strict check's count line | partly: the ten-id cap is untested | extend the same test: twelve unplaced rows name ten and count "+2 more" |
| No exit-code change | untested | new, `tests/test_trace.py`: a clean minimal project whose design row is unplaced passes `--strict`, its output carrying the count line naming that row |
| The state view's design-row detail | untested | new, `tests/test_llr_trace_cells.py`: the state view's row data (`traj_parse.placed_llrs` over an interface registry in a temporary root, and the rendered tier block if it renders in process) shows each placed row's components and "unplaced" for the others |

**Consumers cut from LLR-403's text, each stated and verified by its own row:**

- The build brief's context block: LLR-153 (Accepted) states it, "the LLR/TC code map with each design row's back-link files and its placement or the word unplaced, the CMP knowledge packs and IF seams of the components the rows are placed in".
- The knowledge-pack advisory: the third of LLR-153's "three consumers" of that block, the same placement-to-knowledge join; its code carries no LLR-403 back-link.
- The interface-form gate's reach where no source is scanned: LLR-244 states it (section 4), and TC-466 and TC-239 verify it.

"No design row carries a component" also leaves LLR-403: LLR-404 (Accepted) states it ("A design row declares no file, symbol or component cell").

### The discharge clause moves to LLR-408, reconciled with LLR-201

LLR-201's relevant text (Accepted, SR-157): "The four-tier orphan rules answer whether each row has the children its tier requires and whether each id it cites resolves - an SR its LLR, TC and SN, an LLR its SR parent and TC, a TC a real spine id ..., an SN at least one citing SR". LLR-201 decides *where* the cross-row rules run (one module below the engine) and lists them. It does not say what discharges a design row or that a Drafted one owes no test case. The code's exemption has stood since WI-089 with no row stating it for design rows. TC-197 drives the Drafted SR's exemption under LLR-201, but LLR-201's detail states neither exemption.

I move the clause rather than amend LLR-201. Amending would add SR-248 to an `Accepted` module-siting row's `sr_refs` (a routed traced change), amend its detail and amend TC-197. That is three more acts on rows the verdict did not return, and it would make a module-siting row the child of a discharge requirement. The successor states the design tier's requirement and names LLR-201 as the pass that runs it, so the two read as decomposition, not paraphrase:

**LLR-408** (Drafted, new), sr_refs `["SR-248"]`, test_refs `TC-485`, phase 6:
- title: "A design row past Drafted is discharged by a test case verifying it, and a Drafted one owes none yet"
- detail: "A design row is discharged when a live test case's verifies cell names it, whatever that case's verification kind. This is what the design tier requires in the cross-row orphan pass LLR-201 places ('an LLR its SR parent and TC'): the pass reports a design row past Drafted that no live case verifies, naming the row, and the strict check fails on it; a Drafted design row that no case verifies is not reported while it stays Drafted."
- rationale: binding discharge to a code symbol pointed down at the code, so a rename reopened an accepted row; the verifying test case is the evidence of the row's own kind; a Drafted row is still being written and makes no claim yet. LLR-201 decides where the rule runs, this row what it requires.

**TC-485** (Drafted, new), verifies `["SR-248", "LLR-408"]`, level Unit, tier Smoke, automated Yes:
- method: run the orphan rules directly over four design rows: an Accepted row verified by an automated case, an Accepted row verified only by an inspection case that is not automated, an Accepted row no case verifies, and a Drafted row no case verifies. Then run the strict check over a project whose design row is verified by no test case, first Drafted, then Accepted.
- expected: the two verified rows are not reported, the unverified Accepted row is reported as having no test case and named, the Drafted row is not reported; the project's check passes with the row Drafted and fails naming it once Accepted.
- tests: new in-process `tests/test_llr_trace_cells.py` test over `coherence.spine_orphan_findings` (its smoke evidence); `tests/test_trace.py::test_draft_llr_is_exempt_from_tc_rule` re-tagged from TC-480 to TC-485.

**TC-480** (Drafted, rewritten), verifies `["SR-249", "LLR-403"]`: method and expected keep the placement scenarios, drop the discharge half (now TC-485's), and add the state view, the cap and the passing strict run.

## 4. The two re-landed chains, checked upward

### SR-212 / LLR-244 / TC-239

**SR-212 `acceptance_criteria`** (Accepted, amended): the boundary-rung sentence unchanged. At the architecture rung, "reached, through the modules its design rows name, by at least one boundary interface" becomes "reached by at least one boundary interface", and one sentence defines reach:

> "At the architecture rung, a boundary interface reaches the requirements of the design rows realized in the one file stating its contract body, the files realizing a design row being those its back-link declarations are in, and an interface whose contract body no file states reaches none; where no source is scanned, an interface instead reaches the requirements of the design rows placed in its owner component."

The pass and fail conditions after it are unchanged.

**LLR-244 `detail`** (Accepted, amended): the `8e08b3029` text, kept in meaning, with its code names replaced: `interface_form_gate_findings` → "the architecture arm"; `crossing_gate_findings(srs, das, bifs)` → "the boundary arm"; "check.py gains a built-in step `interface-allocation`" → "the harness gains a built-in step for the architecture arm"; the same for the boundary arm's step.

**TC-239 `method`** (Accepted, amended): the `8e08b3029` text with "the interface-allocation step" → "the architecture arm's step" and "the crossing-allocation step" → "the boundary arm's step", plus two scenarios:

> "A boundary interface whose contract body no file states, bridged only by an assumption the requirement does not cite, and owning the component a case places that requirement's design row in, reaches nothing: the requirement fails stating that no boundary interface reaches it, and the interface is not named. Driven again with the scan profile reading files only, so no source is scanned, the same interface reaches the requirement through the design row placed in its owner component, and the requirement fails naming that interface."

**TC-239 `expected`** (Accepted, amended, beyond the spec's `method`): it gains "an interface whose contract body no file states reaches none, and where no source is scanned an interface reaches through the design rows placed in its owner component". Without it the method would drive two outcomes the expected never states.

Upward check:

| LLR-244 clause | SR-212 acceptance (amended) | Before the amendment |
|---|---|---|
| reach through the one file stating the body and the back-link index | "the design rows realized in the one file stating its contract body ... back-link declarations" | "through the modules its design rows name": contradicted |
| no body reaches none | "an interface whose contract body no file states reaches none" | absent: exceeded |
| no source scanned: owner-component placement | "where no source is scanned ... placed in its owner component" | absent: exceeded and contradicted |
| judging rules, advisory with the gate off | unchanged clauses | consistent |
| boundary arm over crossings | unchanged boundary sentence | consistent |

TC-239 states each row of that table in its method and expected, and drives the two new ones with a test each (section 5). TC-466 already pins both clauses in process; TC-239 gets its own, driven through the step as its level says.

### SR-221 / LLR-263 / TC-258

**SR-221** (Accepted, amended): `requirement`, `acceptance_criteria`, `rationale`, `coincident`.
- requirement: "The delivered harness shall list, for a file whose back-link declarations name a design row, the test files the requirement spine links to it through those design rows, the test cases verifying them and those cases' evidence, with no hand-kept map."
- acceptance_criteria: "For a file whose back-link declarations name a design row, the listing names every test file under the declared test root that the evidence of a test case verifying one of those design rows cites, files not named for it included, and no other file; a name matching no such file and one matching several are each refused with a distinct outcome, the latter naming the candidates; the listing reads the test-case registry and stack profile of the docs directory it is pointed at and the back-link declarations of the repository holding it; the commit checks are unchanged by it."
- rationale: "module" becomes "file" where it means the thing a builder changes, and "The spine already records which tests carry each design row's evidence, so the listing reads it" becomes: the code's back-links already say which design rows a file realizes, and the spine records which tests carry each row's evidence, so the listing joins the two.
- coincident: "...the tests the spine links to a file, listed through the code's own back-links and the registries with no hand-kept map, ...". The old "listed from the registries" would contradict the requirement.
- title kept: "changing a module" names the file a builder changes and contradicts nothing. The verdict's faults are "a design row names" and "derived from the registries", which the four cells remove. (If the coordinator prefers "file" in SR-221's and LLR-263's titles too, that is two more amendment acts.)

**LLR-263 `detail`** (Accepted, amended): the `8e08b3029` text with "stack.ini [paths] tests" → "the stack profile's declared tests path" and "stack.ini" → "the stack profile". It already names no function or flag.

**LLR-263 `rationale`** (Accepted, amended): the opening sentence corrected from "SR-221 asks for the tests the spine links to a module, derived from the registries" to "SR-221 asks for the tests the spine links to a file, read through the code's back-links with no hand-kept map". The rest is the `8e08b3029` text.

**TC-258 `method` and `expected`** (Accepted, amended): the `8e08b3029` text with trace.py, `--tests-for`, `--docs`, `--root`, `coherence.py` and `frame_rules.py` replaced by contract terms: "the spine checker's own entry point", "the listing", "pointed at a docs directory elsewhere while the repository root it is given is an unrelated empty directory", "the suite of the checker's cross-row coherence module, which no test file is named for", "the frame rules' driven suite beside its unit module". "an unknown module" → "an unknown name". Its tests (`tests/test_evidence_join.py`) already drive the file listing; no test changes.

Upward check:

| LLR-263 clause | SR-221 (amended) | SR-221 today |
|---|---|---|
| listing for a file through the back-link index, the verifying cases, their evidence | requirement and acceptance, "for a file whose back-link declarations name a design row" | "for a module a design row names": contradicted |
| every status, a Drafted case included | "every test file ... that the evidence of a test case ... cites" | consistent |
| resolution by path, suffix or stem; exit 1 for none, 2 naming several | "refused with a distinct outcome, the latter naming the candidates" | consistent |
| registries and profile from the docs directory, back-links from the repository holding it | "reads the test-case registry and stack profile of the docs directory ... and the back-link declarations of the repository holding it" | "reads the registries of the repository it is pointed at": exceeded |
| runs no check | "the commit checks are unchanged by it" | consistent |
| rationale opening | "read through the code's back-links" | "derived from the registries": the echo the verdict names |

TC-258 drives each clause and verifies SR-221, LLR-263 and IF-233 as before.

**WI-1018.** Its spec already says SR-221 "Moved to WI-1056 the same day" and its `sr_refs` never named it. The branch rewrites the leftover "It joins the first set." in the past tense so that set excludes SR-221 unambiguously. No other change.

## 5. Test-case repairs

Every case's evidence is regenerated from the tags (`trace.py --root . --regen-evidence`), never hand-edited.

**What the code already does, and what it does not.** Each behaviour the rows will state was checked against the code today:

| Behaviour stated | In the code today? |
|---|---|
| LLR-405, absent source root | yes: the source walk skips a root that does not exist; listed headers are still read |
| LLR-405, unreadable file | yes: a decode error or a read error skips the file, in the source walk and the header read; a listed header that is not a file is skipped |
| LLR-406, no tests root or no test-case registry | **no.** Nothing is written, but the command then prints "every evidence cell is current", which is false for a repository with no registry. The row will state that the command reports which input is missing (the shape LLR-407, Accepted, already states for its own absent registry: "an absent registry is reported and nothing is written") and exits 0. **Code change, red first** (`arch_tags` and the command's arm in `trace.py`) |
| TC-483, re-read refusal | yes: the rewrite raises "REFUSED ... nothing written" |
| TC-484, absent registry and re-read refusal | yes |
| TC-481's clauses | yes (LLR-404, Accepted, already states them) |
| LLR-244, no body; owner-component fallback | yes |
| LLR-403, state view; ten-id cap; no exit code | yes |
| LLR-408, discharge and the Drafted exemption | yes |

**Red first, and what stands in for it.** One new behaviour, LLR-406's report of a missing input, gets a test shown failing before the code. Every other new test drives behaviour the code already has: newly stated or newly verified, not newly built. Such a test cannot fail first without breaking working code. For each one I will show it bites by mutating the code it drives (in the worktree, reverted with `git checkout`, never committed), running the test red, restoring, and running it green. The Deliverable records the mutation and the failing line. **Coordinator: confirm this stands for "shown failing first" on behaviour that already exists, or say what you want instead.**

Natural inputs for the two re-read refusals, no monkeypatching: a registry whose cell key is written quoted (`"evidence" = ...`, `"module" = ...`) parses as the same key, but the line rewrite does not see it. The regeneration then appends a second key, so its result does not parse; the migration keeps the cell. Each result fails the re-read, and the file stays byte for byte.

### By case

**TC-239**, `tests/test_assumption_gate.py` (slow; the file carries TC-239's tag, so the evidence stays the whole file):
- new: the architecture arm's step over a boundary interface whose body no file states, which reaches nothing (the requirement fails "no boundary interface reaches it" and the interface is not named). Mutation proof.
- new: the same fixture with the scan profile reading files only, which reaches through the owner component's placed design row (the requirement fails naming the interface). Mutation proof.

**TC-480**, `tests/test_llr_trace_cells.py` and `tests/test_trace.py`:
- extend `test_a_design_row_is_placed_through_the_interfaces_its_cases_name`: twelve unplaced rows, ten named, "+2 more". Mutation proof.
- new: the state view's design-row detail shows the components or "unplaced". Mutation proof.
- new, `tests/test_trace.py` (slow): a clean minimal project with an unplaced design row passes `--strict` and prints the count line naming it. Mutation proof.

**TC-485** (new), `tests/test_llr_trace_cells.py` and `tests/test_trace.py`:
- new: the orphan rules over a design row verified by an automated case, one verified only by a non-automated inspection case, an unverified Accepted row and an unverified Drafted row. Mutation proof.
- `test_draft_llr_is_exempt_from_tc_rule`: re-tagged from TC-480.

**TC-481**, `tests/test_llr_trace_cells.py`:
- new: a design row setting a symbol cell and one setting a component cell are each refused, a need-tier row with an undeclared key is refused, and each refusal names the registry file, the row and the key.
- new: the three retired design-row cells are classed traced (`acceptance_record.spine_cell_class`), and an accepted design row's accepted text reads the same with and without them.
- Both are coverage of behaviour LLR-404 already states; mutation proof.

**TC-482**, `tests/test_llr_trace_cells.py`:
- new: the index with the source root removed holds only the listed header's ids; with a file that does not decode, a file whose read fails, and a listed header that does not exist, those contribute nothing and the rest is indexed. Mutation proof.
- new: the build brief's code map lists a declared design row's file and marks an undeclared row as having none (`intake.context_block`, or its code-map helper if the block needs a git repository). Mutation proof.
- The existing test keeps the prose-mention case, which shows the grammar LLR-405 cites.

**TC-483**, `tests/test_llr_trace_cells.py`:
- new: a cell whose only part no declaration names loses its key, and the regeneration command's output names the changed cases. Mutation proof.
- new: the quoted-key registry is refused through the command, and its bytes are unchanged. Mutation proof.
- **new, red first:** a repository with no test-case registry, and one with no tests root: the command names the missing input, writes nothing and exits 0. Fails today (it prints "every evidence cell is current").

**TC-484**, `tests/test_llr_trace_cells.py`:
- new: an absent design-row registry is reported, nothing is written, and the command exits 0.
- new: the quoted-key registry is refused naming the registry, its bytes unchanged.
- Both are coverage of behaviour LLR-407 already states; mutation proof.

### The rewritten rows' text, in outline

- **LLR-405** (Drafted, rewritten): one index maps each spine id to the files whose back-link declaration names it, repository-relative and sorted, over the declared source root and the files the scan profile's header list names. A back-link declaration is what the one declaration grammar LLR-204 states reads as one: the declaration token opening its line, followed on that line by spine ids; an id in prose, or after other text on its line, declares nothing. Read as text; generated on every read, never authored; a row no declaration names is absent. With the source root absent, the index holds what the listed headers declare; a file that cannot be read as text (its bytes do not decode, or the read fails) and a listed header that is not a file contribute nothing while the rest is indexed. The build brief's code map lists each design row's indexed files and marks a row the index lacks as having none.
  - Reader list cut to the build brief (the Done-when's named marking). The file listing is LLR-263's own statement, and TC-482 verifies both rows. The gate's reach is LLR-244's ("the back-link index names for it"), and the consolidation census is LLR-210's ("one source file's back-link tags"); each states its own reading.
  - Title: "The files realizing a design row are read from the code's back-link declarations into one index".
- **LLR-406** (Drafted, rewritten): unchanged but for its parent, SR-251, and one added clause: "With no test-case registry, or no tests root, nothing is written and the regeneration command reports which input is missing."
- **TC-480 to TC-485**: method and expected rewritten to the scenarios above, in contract terms.

## Build order, after the go-ahead

1. The red-first test for LLR-406's missing-input report, shown failing; then the code in `arch_tags` and the command arm. The module size ratchet is re-stamped if a counted file grows.
2. The SR split, LLR-408, TC-485 and the re-pointing; the back-link docstring moves; LLR-403, LLR-405, LLR-406 and TC-480 to TC-484 rewritten; their tests, each with its mutation proof; `--bump-ids`; `--regen-evidence`.
3. The six `Accepted` rows amended; TC-239's two tests; WI-1018's sentence.
4. Before each registry-changing commit: `trunk_step.py --root . --regen`, then the `tomllib` parse of every registry touched. Before the close: the test modules importing each changed module (`trace.py --tests-for`, and a grep of importers), the modules holding every touched TC's tests, `tests/test_import_layers.py`, `tests/test_module_size_ratchet.py`, `tests/test_dogfood_sync.py`, `trace.py --root . --strict`, `check_trajectory.py --root . --strict`, and `run_menu.py smoke` once at the end.
5. The close: the spec's `## Deliverable` (before `## Context`), the move to `docs/archive/work/complete/` with `specref` cleared and its relative links checked from the new depth, and the log fragment `docs/log.d/WI-1056-answer-wi-1055-verdict.md`.

## Acts owed for the fourth sitting (preview; the Deliverable gives the final list)

- **Amendments to `Accepted` rows (text only):** SR-212 `acceptance_criteria`; LLR-244 `detail`; TC-239 `method` and `expected`; SR-221 `requirement`, `acceptance_criteria`, `rationale` and `coincident`; LLR-263 `detail` and `rationale`; TC-258 `method` and `expected`.
- **Routed traced changes to `Accepted` rows:** none planned.
- **First acceptance, `Drafted`:** SR-248 (rewritten); SR-249, SR-250 and SR-251 (new); LLR-403, LLR-405 and LLR-406 (rewritten); LLR-408 (new); TC-480 to TC-484 (rewritten); TC-485 (new).

## For the coordinator's go-ahead

1. **Mutation proof for behaviour that already exists**, standing for "shown failing first" (section 5). Every case except LLR-406's missing-input report is such a case.
2. **LLR-406's missing input:** the command reports which input is missing, writes nothing and exits 0, matching LLR-407's absent-registry clause. This is a code change.
3. **The discharge clause** moves to a new LLR-408, which names LLR-201 as the pass that runs it, instead of amending LLR-201, TC-197 and LLR-201's `sr_refs`.
4. **Consumer lists cut to one home each:** LLR-403's to the derivation, the component view, the state view and the count line; LLR-405's to the build brief's marking. The other readers are stated, and verified, by LLR-153, LLR-244 and LLR-210.
5. **Code names scrubbed** from every re-landed cell, beyond the `8e08b3029` text: function, file, flag and step names, the step names included.
6. **SR-221's and LLR-263's titles kept.** TC-239's `expected` is amended beside its `method`.
7. **sn_refs:** SR-248 narrows to SN-002; SR-249 takes SN-002 and SN-023; SR-250 SN-002 and SN-003; SR-251 SN-002.

## Noticed, not in scope

IF-231's notes (Drafted) say the reach relation "is derived through its owner's design rows". Since F-3 that holds only where no source is scanned; elsewhere the reach goes through the file stating the body. The verdict did not raise it and this branch does not amend it. It is a candidate for WI-1018's list.
