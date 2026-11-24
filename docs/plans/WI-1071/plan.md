# WI-1071 plan, revision 1: the eighth sitting's verdict answered

Written in the worktree `D:/ai-template-wt-wi1071`, branch `maint/wi-1071`,
cut from `refactor_again` at `ec188f984`. `planmode = "single"`: this commit
carries the plan alone, and nothing else changes until the coordinator's
go-ahead.

Read in full: the spec `docs/work/queued/WI-1071-answer-eighth-sitting.md`;
its scope critique `docs/reviews/2026-11-24-scope-critiques/WI-1071.md`; the
eighth sitting's verdict
`docs/reviews/wi-1068-adjudicate-eighth-sitting/001-ADJUDICATE-fbd50be.md`
(the MEANING lines for LLR-047, LLR-039, LLR-199, LLR-281 and TC-398, the
RETURN lines for TC-530, TC-571, LLR-423 and TC-533, both `## Dispositions`);
WI-1024's slice-1 record `docs/plans/WI-1024/slice-1.md` (§3, §5, §6).
Rows read, live and in the acceptance record
(`docs/archive/last_accepted/`): SR-007, SR-046, SR-070, SR-178, SR-224,
SR-229, SR-237; LLR-039, LLR-047, LLR-142, LLR-199, LLR-281, LLR-300,
LLR-301, LLR-359, LLR-403, LLR-420, LLR-423, LLR-484; TC-042, TC-047,
TC-135, TC-170, TC-195, TC-291, TC-315, TC-316, TC-317, TC-339, TC-342,
TC-345, TC-370, TC-398, TC-460, TC-465, TC-480, TC-530, TC-533, TC-571;
IF-274, IF-275, IF-277. Code read: `run_menu.py` (`load_capabilities`),
`kitlib/config.py` (`read_stack_ini`), `gen_okf.py` (whole),
`gen_components.py` (whole), `trunk_step.py` (`REGEN_STEPS`, `regen`),
`gen_skills_index.py` (the floor and `main`), `adjudicate_act.py` (the
unequal-identity message), `coordinator_adjudicate.py` (the act turn's
refusal), `intake.py` (`_routed_amendments`, `_amendment_drafts`),
`coordinator_guard.py` (`guard_config`, `SESSION_ENV` and its readers),
`kitlib/shell_line.py` (probed on the unclosed forms). Tests read: the
modules named in §7, `tests/test_generated_freshness_*.py`,
`tests/test_check_lane.py`, `tests/test_trunk_step_plan.py` and
`tests/test_llr_trace_cells.py`.

## Ids

None minted. Nothing here re-cuts a row; the brief's ranges (LLR 490 to
492, TC 581 to 585) stay unused.

## 1. The four rows' dropped clauses (Done-when 1)

Each row's live `detail` diffed against its acceptance-record copy. Every
clause the rewrite dropped is listed: the verdict's, and any more the diff
shows. The four rows' `constrains` links stay as they are (WI-1070 makes
the brief show them).

### LLR-047 (run menu)

| Dropped clause | Code | Settled |
|---|---|---|
| No interpolation | `run_menu.load_capabilities` reads through `kitlib.config.read_stack_ini`, whose parse sets interpolation off ("a `%` in a value is literal"). No test drives it. | Restated; new test |
| Capability names keep their case | `read_stack_ini(path, fold_keys=False)`; the loader's docstring: "a capability may be `Serve`". No test drives it. | Restated; new test |
| An orphan description row is dropped | the loader collects `.desc` rows into a map and lists only commands. No test drives it. | Restated; new test |
| An empty-value command is dropped | `... for name, cmd in commands if cmd`. No test drives it. | Restated; new test |

No accepted spine row states these: SR-046's rationale gives the
declaration grammar to LLR-047 by name, and SR-007 and LLR-155 speak of
the policy file and toolchain, not the run section. Everything else the
rewrite changed is wording (`--list`, `shell=True`, `--for-run`,
`run.command` restated in contract terms).

Amended `detail` (text only, `Accepted` kept, owed), in full:

> The run menu reads the run section of the stack profile into a list of
> name, command and description in declaration order, with no
> interpolation, so a percent sign in a value is literal, and keeping each
> name's case; a name's description row attaches to its command, and a
> description row naming no command, or a command with an empty value, is
> dropped. Its list form prints one line per capability: the name, a tab
> and the description. A capability named on the command line is launched
> by exact name, an unknown name exiting 2, and the launch runs the declared
> line through the shell and passes the child's exit code straight through.
> The launch puts first on the search path a directory whose bare python
> resolves to the menu's own interpreter: on Windows that interpreter's own
> directory, and on POSIX a per-launch temporary directory of executable
> shims that run its exact path. On Windows the command processor searches
> the line's working directory before the search path, so a python
> executable there, at the repository root or in a directory the line
> enters, runs instead and is outside this guarantee; with no interpreter
> there, the prepended directory governs the search. On POSIX that directory
> also makes bare python3 exact, and a line meant to run on Windows declares
> python; the POSIX construction is a shim rather than a link so a virtual
> environment keeps its configuration. With no argument it prints the
> numbered menu, reads a pick from standard input, and returns without
> hanging when the input is closed; an absent or empty run section prints
> guidance and exits 1. Every run launcher resolves one interpreter by
> running, in order, its repository virtual-environment candidates and then
> the candidates of its dev-setup's ordinary runtime search, taking the
> first that reports Python 3.11 or later as its executable path, and runs
> the menu on exactly that path. The no-argument launchers change to the
> repository root and invoke dev-setup's readiness operation for a bare run
> once before the menu, handing it that interpreter when one resolves; a
> nonzero result prints guidance and leaves the menu unopened. The direct
> and list forms bypass that operation and, on Windows, the closing pause,
> and exit 1 with guidance when no interpreter resolves; the macOS launcher
> delegates to the POSIX one so it does not duplicate the operation, and
> non-interactive menu input remains available after it.

The only change from the live text is its first sentence. `rationale`
unchanged.

Test cases: **TC-047 must change** (its method states none of the four
clauses, and it carries inherited code names: `--list`, `run_menu.py`,
`[run]`, `name.desc`, `scripts/run_menu.py`, `run.*`, `RUN_CMD`, `PATH`,
`python.exe`). Amended `method`:

> Run the run menu's suite: the list form prints each declared capability's
> name, a tab and its description in declaration order (an empty
> description renders as a trailing tab); a run section holding percent
> signs and a mixed-case name lists the percent signs literally and the
> name in its case, launches that name and refuses its lower-case spelling
> as unknown, and a description row naming no command and a command with an
> empty value are neither listed nor launchable; the direct form runs the
> named command and returns its exit code (a nonzero passes through); the
> no-argument menu launches a capability from piped standard input and
> returns without hanging on closed standard input; an unknown name exits 2
> and an absent or empty run section prints guidance and exits 1; a
> description row renders in the menu; and the scaffold ships the run menu
> plus run launchers that delegate to it, carrying no command of their own.
> With a real pre-3.11 interpreter first on the search path, run a declared
> bare-python capability on every platform; on POSIX also put another
> python beside the menu interpreter and drive the written bare-python and
> bare-python3 shims.

Amended `expected`:

> Satisfies SR-046 AcceptanceCriteria. The run section's values read
> literally, a name keeps its case, and a description row naming no command
> or a command with an empty value is not listed. A declared bare-python
> capability runs on the menu interpreter rather than the first interpreter
> on the search path when its Windows working directory contains no python
> executable; a python executable in that directory precedes the search
> path on Windows and is outside this case. On POSIX, bare-python and
> bare-python3 remain exact even where the menu interpreter's directory has
> another python, and each shim preserves the named virtual environment.

TC-342 (the launchers' readiness and interpreter search) drives clauses
the rewrite kept and does not change.

### LLR-039 (the bundle emitter)

| Dropped clause | Code | Settled |
|---|---|---|
| Front matter as JSON-quoted YAML scalars (live says "quoted") | `gen_okf.fm` writes every value with `json.dumps`. Tests assert `type: "System Requirement"`, which a YAML double-quoted scalar also satisfies; none distinguishes JSON quoting. | Restated; new test |
| The freshness check fails after a document edit | a guide's title and summary are derived from its document's first heading and paragraph, so an edit there changes the expected bundle; `main` compares expected with on-disk. No test edits a document. | Restated, bounded to the first heading or paragraph (an edit elsewhere moves nothing, so "a document edit" would overstate it); new test |
| The freshness check fails on a missing bundle file | `stale` takes every expected key whose on-disk copy differs, an absent one included. No test deletes a file. | Restated; new test |
| The legacy opt-out file, read through the migration window | `gen_okf.read_enabled`: the declared `[checks]` value wins; with none declared, a legacy one-word file reading `off` turns the export off. No test drives it. | Restated as the precedence the code holds; new test. The "while the migration window remains open" qualifier is a statement about the future that no test can drive; the row says what holds today (decision D4) |
| Small loaders duplicated, no new sibling import | no longer enforced: the module imports the spine carrier (`import spine_carrier`) and the shared package (`kitlib.config`, `kitlib.spine`); the "small local loaders" section is now one `csv_rows` call and two aliases. | Reported: the code no longer holds it; the row says nothing about it (the live text already omits it) |

No accepted spine row states any of the four kept clauses.

Amended `detail`, in full:

> The bundle generator builds one file per real registry row, sorted and
> deterministic with no timestamp: each file's front matter carries the
> row's cells as JSON-quoted strings, which YAML reads as scalars, and its
> body the row's prose with links up and down the spine, beside per-tier and
> root indexes and a pin of the bundle format's specification. Its write
> mode writes a file only when its content changed and prunes a file the
> bundle no longer holds. A process-guides tier gives each present guide
> document a title and summary taken from its first heading and paragraph,
> inline links stripped so nothing dangles, and points at its source
> document, which is left unmodified; guides are emitted only alongside a
> real spine, so a fresh scaffold stays vacuous. Every link in the bundle
> resolves within it. The freshness check fails after a registry edit,
> after an edit to a guide document's first heading or paragraph, on a
> missing bundle file and on a hand-added extra file, and passes again
> after regeneration. The process settings' bundle opt-out silences the
> step; where the process settings declare no bundle choice, a legacy
> one-word opt-out file reading off silences it too, and a declared choice
> overrides that file. A registry holding only example rows passes
> silently.

Test cases: **TC-042 must change**. Its expected already names "missing
files" and its method "doc edits", but no test drove either, it names
neither the JSON quoting nor the legacy file, and it carries `--check`
and "gen-okf". Its evidence stays file-level (`tests/test_gen_okf.py`,
whose module docstring declares TC-042), so the new tests join it with no
evidence edit. Amended `method`:

> Run the bundle generator's suite: typed linked concepts generate, a
> registry cell holding a double quote, a backslash and a non-ASCII letter
> reading back from its front-matter line as a JSON string; Process Guide
> concepts emit for present documents with derived summaries and unmodified
> sources (and none on a vacuous scaffold); regeneration is byte-stable; the
> freshness check fails after a registry edit, after an edit to a guide
> document's first paragraph, on a deleted bundle file and on a hand-added
> extra, and passes after regeneration; extras are pruned; a registry of
> example rows only is vacuous; the declared opt-out silences the step,
> with no declared choice a legacy opt-out file reading off silences it,
> and a declared choice overrides that file; and the bundle step is wired
> at DevStg-Impl.

Amended `expected`:

> Typed linked concepts with resolvable graph links and JSON-quoted
> front-matter scalars, and derived Process Guides, emit with sources
> unmodified; regeneration is byte-stable; the freshness check fails on a
> registry edit, a guide document edit, a missing file and an extra, and
> passes after regeneration; extras are pruned; placeholder-only is
> vacuous; the declared opt-out silences it, and with no declared choice so
> does the legacy opt-out file.

### LLR-199 (the component view) and LLR-403's placement

**The relation to LLR-403.** LLR-403 (accepted, re-blessed by the eighth
sitting) is the one home of design-row placement, through `constrains` and
through verifying test cases, and it already states that "the generated
component view lists each placed row in its components and each unplaced
row in its unplaced table, counted in its census" (driven by TC-480's
`tests/test_llr_trace_cells.py::test_the_views_show_where_each_design_row_sits`,
which asserts the view's `unplaced` design rows and their census count).
LLR-199 consumes that placement and does not restate it: its text names
LLR-403 for both the placement and the unplaced design rows, so nothing
falls between the two rows (the verdict's second option).

| Dropped clause | Code | Settled |
|---|---|---|
| Unplaced design rows in the counted unplaced table | `gen_components.render` writes `[unplaced] llr_refs` and `design_rows_unplaced`. | Home: **LLR-403** (accepted). LLR-199's text points at it; no restatement |
| The generated-but-live staleness header | `gen_components.BANNER`: generated by the generator, do not hand-edit, cite the spine registries instead, the regeneration command. No test reads it. | Restated; new test |
| The trunk regeneration wiring | the shipped stack profile template's `[generated]` maps the view to kind `components`; `trunk_step.REGEN_STEPS` carries a `component-view` step; the freshness step is wired (its census, TC-206's `test_every_declared_generated_artifact_has_an_enforcer`). No test drives the regeneration of the view. LLR-142, the trunk regeneration row, lists five families and not this view, so it is no home. | Restated: the declaration and the trunk re-derivation; new test. The freshness check is already stated |
| "Registries cannot distinguish missing decomposition from an all-component constraint" | the view lists every unplaced requirement alike; the banner states the reading. | Not an obligation of its own: "a requirement reaching no component appears once in the counted unplaced table" already says each is listed the same way. Not restored |
| "NOT DISCHARGED: no internals; freshness never asks whether the source rows were right" | a disclaimer, no behaviour. | Not restored (the rationale keeps "a requirement list says ... nothing about how its parts fit") |

Amended `detail`, in full:

> The component view is derived from the component, design-row,
> system-requirement, interface and test-case registries and the files'
> component headers. The component registry declares the components, and
> each file's header places that file in one. Each design row is placed
> where LLR-403 places it, and a design row placed in no component is
> listed and counted in the unplaced table as LLR-403 states; a system
> requirement reaches the components its placed design rows sit in. The
> interface registry gives each seam's owner and far side. The view is
> written to the generated component file, which opens with a header saying
> it is generated and not to be edited by hand, that the spine registries
> are what to cite instead, and the command that regenerates it; a
> freshness check compares the file with a regeneration, failing when they
> differ. The kit's stack profile declares the file a generated artifact,
> and the trunk's regeneration step re-derives it. For each component the
> view lists its member design rows, the requirements they decompose, the
> perspectives in effect on those members, its files, and its seams split
> into internal and boundary. A requirement reaching no component appears
> once in the counted unplaced table. A requirement in several components
> appears in each and in each component's shared list. A seam appears in
> each component its endpoint cells name: internal to the lowest component
> enclosing every endpoint through the part-of chain, internal to none when
> an endpoint is an external party or no component encloses them all, and
> boundary to every other; a seam naming no declared component stays in the
> unplaced table. No acceptance or maturity cell appears in the view. With
> no real component row and no view on disk, the generator exits 0 and
> writes nothing.

`rationale` unchanged. The parent check is decision D2.

Test cases: **TC-195 must change** (it states neither the header nor the
wiring). TC-460 and TC-465 drive the files and seams and do not change.
TC-195's `method` gains two sentences before VACUITY, the rest unchanged:

> THE HEADER: the written view opens with the generated-file header naming
> it generated and not to be edited by hand, the registries to cite instead
> and the command that regenerates it. THE TRUNK WIRING: the kit's shipped
> stack profile declares the view a generated artifact, and the trunk's
> regeneration step rewrites a stale view so the freshness check passes.

### LLR-281 (the skills description floor)

| Dropped clause | Code | Settled |
|---|---|---|
| The `SHORT` output marker | `refuse_short_descriptions` prints `gen_skills_index: SHORT - <name>: description is <n> characters, under the 100-character floor; ...`. The test asserts the name and the floor, not the marker. | Restated (an output marker is observable behaviour); new assertion |
| The floor is checked first | `main` calls the floor before reading or comparing the index, and the refusal exits there. No test drives the order (slice 1 cut it for that reason). | Restated; new test |
| Found by the diff: the line names the length | live text keeps "its length", but the test asserts only the name and the floor. | Kept; new assertion |

Amended `detail`, in full:

> The shortest skill description the skills index check accepts is one
> declared floor of 100 characters, room for a trigger and an effect ("Use
> when <trigger> - <what>"). The check applies the floor before it compares
> the index: it prints one line marked SHORT for each skill whose
> description is under the floor, naming the skill, its length and the
> floor, and then exits 1 without comparing the index; a description at
> the floor passes. Regenerating the index does not apply the floor, so a
> short description is refused where the index is checked rather than
> silently written.

`rationale` unchanged. Test cases: **TC-291 must change** (the marker,
the length and the order are new to it, and it carries `--check` and
`short_descriptions`). Amended `method`:

> (a) THE REFUSAL: a planted skills directory under a temporary directory
> holds one skill whose description is under the floor and one exactly at
> it; regenerating the index succeeds, and then the check exits 1 and its
> error output carries one line marked SHORT naming the short skill, its
> length and the floor, and nothing naming the skill at the floor. (b) THE
> FLOOR FIRST: over the same directory with no index written, the check
> exits 1 on the SHORT line alone and prints no stale-index line. (c) THE
> SHIPPED SET: none of the kit's own skills has a description under the
> floor.

Amended `expected`:

> Satisfies SR-224 AcceptanceCriteria: a description under the floor fails
> the check by name on one SHORT line giving its length and the floor,
> before the index is compared; one at the floor passes; and every shipped
> skill clears it.

## 2. TC-398 (Done-when 2)

**The assertion already exists**, so nothing is red first. The unequal
identity's refusal is derived in `adjudicate_act` ("... moved after the
verdict: bound {}, committed {}") and the act turn prints it whole
(`act: refused: {why}`). Three tests TC-398 names assert both digests:
`tests/test_adjudicate_act.py::test_a_held_CLARITY_act_whose_text_changed_after_the_verdict_is_refused`
and `::test_a_held_CLARITY_act_whose_link_moved_after_the_verdict_is_refused`:

```python
    for word in ("SR-001", bound, committed):
        assert word in why, (word, why)
```

and `::test_a_binding_over_accepted_cells_alone_refuses_a_row_carrying_a_link`:
`for word in ("SR-001", old, _sr_digest(repo)): assert word in why`.

Amended `method` (the last-but-one sentence changes):

> Digest a requirement row, then the same row with its id, its Status and
> a trace cell no adjudicator judges changed, with an empty cell against an
> absent one, and on its other carrier; then with an accepted cell moved,
> and with an adjudicated link moved. Compose an amendment brief over
> committed rows whose accepted cells moved, and one over a row whose
> adjudicated link alone moved, and read their judged-text lines. Reserve a
> sitting from a composed prompt, round-trip and read its binding, and
> rewrite it as recorded and as failed. Derive the held act of a CLARITY
> verdict whose binding equals the committed row, one whose row's accepted
> cell moved after it, one whose row's adjudicated link moved after it, one
> whose binding was written over the row's accepted cells alone, one with no
> identity and one with a malformed identity cell, reading each refusal for
> the row and, where the identities are unequal, for the digest the binding
> records and the committed row's digest; and launch the act turn over one
> whose text moved. Judge a held acceptance claim under a CLARITY verdict
> binding its equal digest, and one whose adjudicated link moved after the
> verdict.

Amended `expected` (the fourth sentence changes):

> The digest has the sha256 shape and is unchanged by the id, the Status,
> the unjudged trace cell, empty against absent and the carrier, and
> changes for the accepted cell and the adjudicated link. Each brief states
> one judged-text line per shown row, carrying that row's digest as its
> registry holds it, the link-only row's covering its link. The binding
> records the prompt's identities, reading its requested kinds ignores
> them, and both rewrites keep them. The held act is owed only under the
> equal binding; the moved cell, the moved link and the accepted-cells-only
> binding of a row carrying a link are unequal identities, and each refuses
> it naming the row, the digest its binding records and the committed row's
> digest; the missing and the malformed identity each refuse it naming the
> row; and the act turn refuses before launch. The claim is excepted under
> the equal binding and not when the link moved.

Evidence unchanged.

## 3. TC-530 (Done-when 3)

`Drafted`; LLR-420 is accepted and not amended. Today one commit adds
`constrains` and `dimensions` to one row, so the mint's inclusion of the
row (`intake._routed_amendments`: `if rec["accepted"] or routed_cells`)
holds through the accepted half and never shows that `constrains` alone
routes. The rewrite runs two ranges over one project.

Rewritten `method`:

> Read the class of the constrains cell on the requirement and design-row
> registries and of the two companion cells, and whether the merge's
> amendment walk routes each. Then commit a project whose requirement and
> first design row are accepted with no constrains cell and whose second
> design row is accepted constraining an interface. In a second commit add
> a constrains cell, and nothing else, to the requirement and to the first
> design row; in a third add a dimensions cell and an out-of-domain cell,
> and nothing else, to the second design row. Run the amendment walk and
> the trunk's amendment mint over the first range and, separately, over the
> second.

Rewritten `expected`:

> The constrains cell is traced and routed on both registries and the two
> companion cells are accepted. Over the first range the walk records each
> constrains change in its row's traced half with no accepted cell moved,
> and the mint routes both rows by their constrains cell alone and drafts
> one adjudication row naming them; over the second range the walk records
> the dimensions and out-of-domain changes in the second design row's
> accepted half with no traced cell moved, and the mint drafts the
> adjudication row naming it with no traced cell routed.

Tests, `tests/test_constrains.py`: the combined test
`test_a_constrains_change_on_an_accepted_row_is_a_routed_amendment` is
replaced by `test_a_constrains_only_change_routes_with_no_accepted_cell_moved`
(the walk, `_routed_amendments` and `_amendment_drafts` over the first
range) and `test_a_companion_cell_change_amends_accepted_text_alone` (the
second range); `test_constrains_is_traced_and_routed_and_its_companions_are_accepted`
stays. The requirement joins the first range (decision D11).

## 4. TC-571 (Done-when 4)

`Drafted`; LLR-484 is accepted and not amended. The rendered row that also
moves another trace cell is the one
`tests/test_routed_link_owed.py::test_both_surfaces_label_the_three_groups_alike`
already builds: from a fresh seed it moves the third design row's detail,
adds an interface to its constrains cell and moves its phase, then renders
the acceptance brief and the operator's page and asserts the three labels
in order; `::test_a_rows_other_trace_cells_come_last` reads that row's
cells from the model (`Detail`, `Constrains`, `Phase`).

Rewritten `method` (one sentence added at the end):

> Over a project whose accepted requirements each carry one accepted design
> row and one test case, record an acceptance copy. For each adjudicated
> link of each tier, move that link alone on one accepted row and read the
> acceptance model; check the links moved are the routing table's. Then move
> only the first design row's detail, add an interface to the second design
> row's constrains cell, move the third's detail and add an interface to its
> constrains cell, and move only the fourth's phase and perspective cells;
> read the model, and render the acceptance brief and the operator's
> decision page. Then, from a fresh copy, move the third design row's
> detail, add an interface to its constrains cell and move its phase cell,
> so a rendered row also moves a trace cell no adjudicator judges; read the
> model and render both surfaces.

Rewritten `expected` (its last clause made specific):

> Each single moved link lists its row's chain, the row carrying that link
> as moved with no moved accepted cell. The model lists the first three
> chains and not the fourth; the second row carries its constrains cell,
> before and after, as a moved link alone, the third its detail as an
> accepted cell and its constrains cell as a link, and the first its detail
> alone. The brief and the page show the second and third rows' constrains
> cell by name with its before and after under the sitting label, the
> third's detail under the re-acceptance label and the first's detail with
> no label. Where the third row also moves its phase cell, the model lists
> that cell after its detail and constrains cell, and both surfaces show it
> under the label owing no act, after the re-acceptance and sitting labels.

The test asserts the labels' order but not that the phase cell sits under
the last one; decision D10 adds that assertion.

## 5. The session-variable home (Done-when 5)

Settled at the scope critique: LLR-423 (verified by TC-533) is the one
home. **LLR-423 needs no change**: it states the caller's identification
by the tool's session variable and that any other name identifies no one,
and nothing else. It and TC-533 stay `Drafted`.

**The tests that drove the clause.** Two:
`tests/test_coordinator_guard.py::test_a_claim_names_its_caller_by_claude_code_session_id`
(TC-316; the tool's variable passes, a near-miss name reads unknown) and
`::test_the_guard_reads_its_caller_from_the_agent_tools_session_variable`
(TC-533 already). The first is re-tagged `Implements: TC-533`; the evidence
regeneration then moves it from TC-316's evidence to TC-533's. Every other
TC-316 test sets the variable only as its setup. TC-533's `method` and
`expected` stand ("another variable name" covers both tests' names); its
evidence names both tests.

**LLR-300.** Removing the clause amends the row, so rule 1 scrubs every
inherited code name in it (about twenty: the function names, the variable,
the agent tool's two tool names and two hook event names). Amended
`detail`, in full; every other clause is kept:

> The guard reads the declared coordinator threshold and window: a
> non-positive, out-of-range or malformed threshold is off and a malformed
> window reads as the default. The occupancy reading takes the newest valid
> assistant usage after the live transcript branch's latest compaction
> boundary, never a sidechain record, counting input and cached input; a
> record whose usage is malformed, partial or zero is skipped, and no valid
> usage reads as unknown, never zero. A primary-checkout lease names one
> coordinator session and its transcript. A take refuses while another
> session holds the lease; the operator's release frees the lease and the
> operator's clear unlatches it, each requiring and recording the
> operator's reason; the hand-back accepts only the holder session and a
> handoff carrying a session prompt, frees the lease, and records the
> handoff; it refuses another or unnamed caller, whatever handoff it names,
> while naming the operator's release; it refuses the holder's own pending
> relaunch request, while a previous holder's request does not block it and
> is left for the session end's refusal of a foreign request; with the
> guard off it returns before reading or writing. Elapsed time never
> transfers ownership. A session start installs a session as holder,
> unlatched, only when it presents the successor token the holder's exit
> wrote into the lease, and restates a latched drain to the holder's own
> resumed start. Only the holder's own hook payload on the holder's
> transcript is measured, never a subagent's. The drain latches when the
> unrounded reading reaches the threshold and is retained through lower
> readings, compaction and resume; it ends only through the owner's clear,
> the operator's release, the holder's hand-back, or a successor take. The
> blackout-window refusal runs before the dial on every claim route,
> including the dispatcher, naming the window's end in UTC; the dispatcher
> remains exempt only from the context guard. The claim refusal refuses
> with no lease held or a claimant that is not the holder, and reads and
> latches the holder's transcript itself, so a refusal never depends on a
> hook having run; a claim holding the dispatch lock never consults it.
> While a window is armed, hooks act at every dial and deny the closed list
> of the main session's subagent-launch call, subagent-message call, Bash
> or PowerShell model-CLI command word, and a Bash or PowerShell line
> unreadable only because of an unclosed single quote, unclosed double
> quote, unclosed POSIX dollar quote, unclosed POSIX backtick substitution,
> unclosed dollar-parenthesis substitution, or unclosed PowerShell
> here-string. One quote-aware shell reading per dialect reads quoted
> values as the shell does, and treats quoted separators, comments and
> here-document and here-string bodies as data. It finds the model-CLI
> command word after leading variable assignments, the timeout and env
> prefixes, the shell's reserved words, the chain operators and the call
> operator, and in substitutions written in the line or inside double
> quotes. It reads a PowerShell assignment to a variable as running its
> right-hand command, while a quoted or variable right-hand value stays
> data. A form outside this list gets no dedicated recognition: it may
> incidentally match this reading, and carries no guarantee either way. The
> guard's window check exits nonzero inside an armed window. At every
> session start inside a window, hooks inject the blackout close-down
> instruction; each main session's monitored events inject it at that
> session's first monitored event in the window and every twentieth
> thereafter, counted per session per window: bring each open lane to its
> pause point, using a wrap-up adjudication for an active claim where
> needed; write the handoff naming each lane and its next obligation;
> request no relaunch; and end the session. Hook responses inject the latch
> instruction once and bounded reminders thereafter; inside a blackout
> window the latch is still recorded, but the blackout close-down, which
> requests no relaunch, is injected in its place. Before a compaction the
> guard records its trigger, the occupancy and the latch and request state,
> and the compaction classification reports missed-threshold, manual and
> during-drain cases. Before recording a holder, the lease take refuses an
> inactive commit floor and records no holder. After identifying a session,
> the lease take first reads the guard hooks' state and records no holder
> unless it reads none or on, or a terminal consent installs them and the
> re-read reads on; without a terminal at absent, or at occupied, it
> refuses naming the consent step or the hooks to move.

`rationale` and `title` unchanged (no code names).

**LLR-300's other clauses, against the test cases verifying it** (TC-315,
TC-316, TC-317, TC-339, TC-345, TC-370). Tested: the occupancy reading
(TC-315's thirteen tests, zero usage in
`test_malformed_and_partial_usage_is_skipped_to_the_newest_valid`); the
malformed window (`test_a_malformed_threshold_leaves_the_guard_off`,
TC-317); the primary-checkout lease (`test_a_lane_worktree_shares_the_primary_checkouts_lease`,
TC-317); take, release, clear, hand-back, elapsed time, session start,
holder-only measurement, the latch and its ends, reminders, compaction
telemetry and the blackout latch (TC-316's tests, listed under TC-316
below); the window
refusal naming its end in UTC and the dispatcher's exemption (TC-317,
TC-339); the claim refusal's own reading and the dispatch lock
(`test_the_crossing_replys_claim_refuses_with_no_hook_run`,
`test_the_live_dispatchers_claim_route_is_untouched`, TC-317); the denial
list, the shell reading, assignments and the close-down cadence (TC-339's
tables and `test_session_start_and_the_monitored_events_tell_the_close_down`);
the inactive floor (TC-370); the hooks' state at the take (TC-345). Three
gaps, found here and older than this row (decision D7):

1. **The threshold's bounds.** Only a wrong-typed threshold (`"half"`) and
   0 are driven; a negative and an over-100 threshold are not. The code
   bounds it (`_int_dial(..., 0, 100) or 0`). Plan: parametrize
   `test_a_malformed_threshold_leaves_the_guard_off` (TC-317) over
   `"half"`, -5 and 150.
2. **The window check's exit.** Driven only by
   `tests/test_blackout_window.py::test_the_window_check_subcommand_exits_nonzero_inside`,
   tagged TC-318 and TC-340, which verify LLR-301, not LLR-300. Plan: tag it
   TC-339 as well (evidence only, a trace cell no adjudicator judges).
3. **The unreadable forms.** `UNREADABLE` drives an unclosed single quote,
   an unclosed dollar-parenthesis and a PowerShell single quote; an
   unclosed double quote, POSIX dollar quote, backtick substitution and
   PowerShell here-string are not driven. Probed: `kitlib.shell_line.segments`
   raises `Unreadable` on all four (`an unclosed " quote`, `an unclosed $'
   quote`, `an unclosed ` substitution`, `an unclosed @' here-string`). Plan:
   add the four to `UNREADABLE` (TC-339's
   `test_an_unreadable_command_line_is_denied_inside_the_window`).

**TC-316.** Amended `method`, the second sentence only:

> Drive holder, other-session and subagent hook payloads and guarded claims
> with controlled transcript readings and lease state. Assert that a claim
> refuses, naming its recovery action, with no lease held and from another
> or an unnamed session; that the holder below the threshold may claim;
> [the rest unchanged].

`expected` unchanged (it never named the variable). Its other clauses stay
tested: no lease (`test_with_no_lease_held_a_claim_refuses_naming_the_take`),
another or unnamed (`test_a_non_holders_claim_refuses_naming_the_holder_and_the_release`,
which also reads an empty environment as unknown), the holder below the
threshold, the silent holder, release and clear with their reasons,
release and successor take, the four hand-back cases, the latch by hook
and by claim through compaction and resume, its four ends, bounded
reminders, compaction telemetry and classification, and the blackout
latch, each by the test of that name in its evidence. Its `verifies`
carries IF-277 (the variable and the project-root variable); decision D5
drops it.

## 6. The row rules (Done-when 6)

| Row | Rule 1, no code names | Rule 2, one obligation, every clause tested | Rule 3, within its parent |
|---|---|---|---|
| LLR-047 | added text names none; live text already scrubbed | the run menu's contract; the four restored clauses by the new tests, the rest by TC-047 and TC-342 | SR-046 gives the declaration grammar to this row by name |
| LLR-039 | none | the bundle emitter; restored clauses by the new tests, the rest by `tests/test_gen_okf.py` | SR-070: derived, byte-stable, a freshness contract; the opt-out and legacy file are the "omitting" side |
| LLR-199 | none; LLR-403 is a row id | the component view; header and wiring by the new tests, placement and unplaced rows by LLR-403's TC-480 | SR-070 (D2) |
| LLR-281 | `SHORT` is a printed marker | the floor's refusal; marker, length and order by the new assertions | SR-224: fails naming the skill; the marker and order are design within it |
| LLR-300 | scrubbed (§5) | one admission fact, as its rationale argues (D8); every clause tested once the three gaps close | SR-229 and SR-237; removing a clause cannot exceed them |
| LLR-423 | unchanged, none | one clause, TC-533's two tests | SR-229 |
| TC-047 | scrubbed | each clause by a test it names | verifies LLR-047 and SR-046 and states nothing beyond them |
| TC-042 | scrubbed | file-level evidence, every clause driven by a test in the file | LLR-039 |
| TC-195 | none | each clause by a test it names | LLR-199 |
| TC-291 | scrubbed | each clause by a test it names | LLR-281 |
| TC-398 | none | each clause by a test it names | LLR-359 ("an unequal one naming both digests") |
| TC-530 | none | the two ranges' tests | LLR-420 |
| TC-571 | none | each clause by a test it names | LLR-484 |
| TC-316 | none | each remaining clause by a test it names | LLR-300 |
| TC-533 | none | its two tests | LLR-423 |

## 7. The tests, by module (Phase 2)

New assertions on behaviour the code already enforces cannot be red on
the base tree. Each is shown red against a one-line mutant of the code it
pins, reverted before any commit, the failing line quoted in the
Deliverable (decision D1).

| Module | Test | Done-when | Red first |
|---|---|---|---|
| `tests/test_run_menu.py` (TC-047) | new: a run section's percent signs list literally, a mixed-case name lists in its case and launches by that spelling, its lower-case spelling exits 2 | 1 | mutant: the loader folds keys |
| `tests/test_run_menu.py` (TC-047) | new: a description row naming no command and an empty command are not listed and exit 2 by name | 1 | mutant: the empty-command filter dropped |
| `tests/test_gen_okf.py` (TC-042) | new: a cell holding a double quote, a backslash and a non-ASCII letter reads back from its front-matter line through `json.loads` | 1 | mutant: the front matter quotes by hand |
| `tests/test_gen_okf.py` (TC-042) | new: the check fails after an edit to a guide document's first paragraph and on a deleted bundle file, naming each, and passes after regeneration | 1 | mutant: the comparison skips absent files |
| `tests/test_gen_okf.py` (TC-042) | new: with the declaration removed a legacy file reading off silences a stale check; declared on, it does not | 1 | mutant: the legacy file is not read |
| `tests/test_gen_components.py` (TC-195) | new: the written view opens with the generated-file header (generated, do not hand-edit, cite the registries, the regeneration command) | 1 | mutant: the banner emptied |
| `tests/test_gen_components.py` (TC-195) | new: the shipped stack profile template declares the view kind `components`; the trunk step's component-view regeneration rewrites a stale view and the check then passes | 1 | mutant: the trunk step's component-view row never applies |
| `tests/test_skills_index.py` (TC-291) | extended `test_check_refuses_a_description_under_the_floor`: exactly one line marked SHORT, naming the skill, its length 7 and the floor | 1 | mutant: the marker dropped |
| `tests/test_skills_index.py` (TC-291) | new: with no index written and a short description, the check exits 1 on the SHORT line with no stale-index line | 1 | mutant: the floor applied after the comparison |
| (none) | TC-398: the three tests quoted in §2 already assert both digests | 2 | not new |
| `tests/test_constrains.py` (TC-530) | replaced: a constrains-only range, requirement and design row, walked, routed and drafted | 3 | mutant: `Constrains` out of the routed table |
| `tests/test_constrains.py` (TC-530) | new: a companion-only range amends accepted text and routes no trace cell | 3 | mutant: the companion cells classed traced |
| `tests/test_routed_link_owed.py` (TC-571) | extended `test_both_surfaces_label_the_three_groups_alike`: the phase cell follows the no-act label on both surfaces (D10) | 4 | mutant: other trace cells not rendered |
| `tests/test_coordinator_guard.py` (TC-533) | re-tagged `test_a_claim_names_its_caller_by_claude_code_session_id` | 5 | not new |
| `tests/test_coordinator_guard.py` (TC-317) | parametrized `test_a_malformed_threshold_leaves_the_guard_off` over `"half"`, -5, 150 | 6 (LLR-300) | mutant: the threshold's range check dropped |
| `tests/test_blackout_window.py` (TC-339) | four rows added to `UNREADABLE`; the window-check test also tagged TC-339 | 6 (LLR-300) | mutant: the reader accepts an unclosed double quote |

Registry edits are checked to parse with `tomllib`; the evidence cells are
regenerated by `trace.py --root . --regen-evidence`; then
`trunk_step.py --root . --regen` before the registry commit. No file the
kit ships changes (tests and registries only), so no RESYNC entry is owed.
Runs: the eight modules above, the modules holding every touched TC's tests
(TC-398: `test_adjudicate_act`, `test_adjudicate_brief`,
`test_coordinator_act`, `test_held_status`, `test_held_status_git`,
`test_amendment_brief_links`; TC-047: `test_bootstrap` for its launcher
test; TC-316, TC-317, TC-339: `test_coordinator_guard_e2e` beside the two
above), the four ratchets the brief names, `trace.py --root . --strict`,
`check_trajectory.py --root . --strict`, and `run_menu.py smoke` once at
the end. The smoke tier grows by about six cases (the run-menu and
bundle modules are slow-tier) against `max-tests = 4060`'s 4% headroom.

## 8. Acts owed (preview of the Deliverable's list)

- **Amendments to `Accepted` rows** (text only, owed): LLR-039 `detail`;
  LLR-047 `detail`; LLR-199 `detail`; LLR-281 `detail`; LLR-300 `detail`;
  TC-042 `method`, `expected`; TC-047 `method`, `expected`; TC-195
  `method`; TC-291 `method`, `expected`; TC-316 `method`; TC-398 `method`,
  `expected`. (LLR-039, LLR-047, LLR-199, LLR-281 and TC-398 were already
  owed from the eighth sitting; their re-sitting reads this text.)
- **Routed traced changes to `Accepted` rows**: the four rows' slice-1
  `constrains` (unchanged here, still owed); TC-316 `verifies` losing
  IF-277 (if D5 is confirmed).
- **`Drafted` rows owed a first acceptance**: TC-530 and TC-571
  (rewritten), LLR-423 and TC-533 (LLR-423 unchanged, TC-533's evidence
  gaining a test).
- No act: TC-339's evidence gaining a test (a trace cell no adjudicator
  judges).

## 9. A finding, not fixed here

The component view's header (`gen_components.BANNER`) and its module
docstring still say "a design row sits at the owner component of each
interface a test case verifying it names", which LLR-403's placement
through `constrains` has outgrown. The restored LLR-199 clause names the
header's four elements only, so it does not inherit the stale sentence.
Fixing it changes a shipped file and the committed view, which this row
does not own (D13).

## 10. For the coordinator to confirm

- **D1.** Red first for a characterization assertion is shown against a
  temporary one-line mutant of the code, reverted and never committed, its
  failing line quoted in the Deliverable; the alternative is to record
  those assertions as green on arrival.
- **D2.** LLR-199 restates the trunk wiring itself, under SR-070 alone (a
  generated view's freshness contract is SR-070's, and the accepted text
  carried this clause under SR-070). LLR-142 is no home: it lists five
  families and not the view. Alternatives: amend LLR-142 (outside the list,
  and it is stale for five other families too) or add SR-173 to LLR-199's
  requirements (a second routed link move).
- **D3.** LLR-403 is the home of the unplaced design rows; LLR-199's text
  points at it ("as LLR-403 states") rather than restating it.
- **D4.** LLR-039: the duplicated-loaders clause is reported as no longer
  enforced; the legacy opt-out file is restated as the precedence the code
  holds (no declared choice), without the "migration window" qualifier,
  which no test can drive.
- **D5.** TC-316's `verifies` drops IF-277, since it no longer checks
  anything that interface states (the project-root variable is TC-534's);
  a routed traced change, owed. The alternative keeps the link because its
  claims still pass the variable as setup.
- **D6.** LLR-300's rule-1 scrub restates the agent tool's `Agent` and
  `SendMessage` tool names as its subagent-launch and subagent-message
  calls, and the `SessionStart` and `PreCompact` events in plain words;
  Bash and PowerShell stay (shell names).
- **D7.** The three LLR-300 test gaps (§5) are closed by adding cases and
  a tag, not by cutting the clauses. This adds test edits to TC-317's and
  TC-339's modules, with no change to either row's text.
- **D8.** LLR-300 stays one row. A sitting may return it as more than one
  obligation (the blackout hook denials are arguably SR-237's own); a
  split is a re-cut for its own work item.
- **D9.** TC-398 gains no test: the derivation tests already assert both
  digests, and the act-turn test asserts the refusal before launch.
- **D10.** TC-571's three-label test gains one assertion, that the moved
  phase cell sits under the no-act label on both surfaces, so the test
  drives what the expected states rather than the labels' order alone.
- **D11.** TC-530's constrains-only range moves a requirement's
  constrains cell beside the design row's, so the walk drives LLR-420's
  "a requirement's or design row's" on both tiers.
- **D12.** TC-047, TC-042, TC-195 and TC-291 are amended (accepted,
  owed) so each states the restored clauses its row now holds, their
  inherited code names scrubbed. Without this, the restored clauses would
  be driven by tests no test-case text describes.
- **D13.** The component view header's stale placement sentence (§9) is
  left for a separate row.
