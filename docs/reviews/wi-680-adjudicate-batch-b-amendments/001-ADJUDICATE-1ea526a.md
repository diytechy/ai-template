# ADJUDICATE — WI-680 — amendment at 1ea526ac

Independent adjudication of the 29 approved rows whose attesting cells the
fourth build wave amended in place (WI-582, WI-656, WI-672, WI-638). The one
question: MEANING or CLARITY, per row. Brief: the kit's amendment brief
rendered for this row (`adjudicate_brief.compose`, 29 blocks, anchor
`docs/archive/last_approved` copied at bc6a245f for the SR, LLR and TC
registries), with the caller's one addition to its method: each new text was
checked against the code and the tests it names on this tree before it was
blessed, and the tier cells were checked against `tests/conftest.py`
`SLOW_MODULES` as loaded in process. I directed none of the amendments and
did not read the amending sessions' accounts of them. HEAD stayed at
1ea526ac throughout; the worktree was clean before this file was written.

The dial: `human_approval_through = "DevStg-Boundary"` in
`docs/process.toml`, so the SR, LLR and TC rungs are released and a MEANING
verdict is re-attested by this session, in the one snapshot act shared with
WI-681.

- [MEANING] TC-036 inputs, max_age -> the inspection's judgement stood indefinitely, over an undeclared reading -> the judgement reads three declared inputs (ADOPTING.md, the downstream-resync skill, SR-036) and expires after 90 days; a change to an input or the lapse of the lifetime drafts a re-judge item (LLR-254) -> a result lifetime and an input set are acceptance conditions the old row did not carry, and SR-198's own acceptance says declaring them re-opens the case's attestation. Blessed: every declared path exists, the row id resolves, 90 >= the seven-day floor, and `assumption_rules.input_escape` passes all three.
- [MEANING] TC-055 inputs, max_age, expected -> the critique verdict recorded in Evidence stood with no lifetime, as "a one-time judgement that nothing re-fires", the row's assurance "as old as its Evidence" -> five declared inputs (the rubric, SR-054, LLR-055, gen_trajectory.py, the rendering package), a 90-day lifetime, and an Expected whose standing limit reads: "the verdict recorded in Evidence is re-judged at a merge or release checkpoint when no result of it is on record, when a declared input changes, or when the record passes its declared max_age, never on every commit", the assurance "as old as its latest recorded verdict" -> a lifetime, an input set and a re-judgement regime are acceptance conditions the old row denied outright. BLESSED on this final text (the third sitting, 2026-09-27, below): the three triggers are `rejudge._judge`'s three in the order it asks them (`WHY_NEVER`, `WHY_CHANGED`, `WHY_EXPIRED`), the two checkpoints are `rejudge.CHECKPOINTS`, "never on every commit" is true of them, `due_cases('.', HEAD)` returns TC-055 "no result recorded", which the cell now states, the five inputs pass `input_escape` and 90 clears the seven-day floor. Two earlier wordings of this cell were judged on the way here and are kept only as sitting history: the first sitting's ("nothing re-fires", false beside the lifetime; my line called it true and was wrong) and the second sitting's ("only when" an input changes or the record expires, omitting the no-record trigger; withheld).
- [CLARITY] SR-054 rationale -> the one unmechanized clause "rests on a recorded one-time judgement rather than on a standing re-judgement — the residue named at the child" -> "rests on a recorded judgement, re-judged when a declared input changes or the record expires rather than on every commit — the residue named at the child" -> the requirement and acceptance are byte-identical (the acceptance still says the clause "rests on a recorded human judgement, a stated limit rather than an implied coverage"); the rationale's account of HOW that judgement is kept current moved from never to the checkpoint's declared triggers, which it names as instances ("when ... or ...") and not as the closed set, so it states nothing the code contradicts. A builder or test author correct under the old rationale is correct under the new one. Blessed.
- [CLARITY] SR-151 rationale -> the shipped workflow file's declarations are pinned by test; the runner is outside design control, and the frame handles it as REL-002/REL-003 do -> the same obligation on the shipped workflow; the runner is now drawn as its own party, hosted CI (EXT-007) crossing at B-11 -> the requirement and acceptance cells are byte-identical; the rationale re-attributes the runner to the redrawn frame (EXT-007 and B-11 exist in external.toml) without moving what a builder ships or a test pins. A reader correct under the old rationale builds the same workflow.
- [CLARITY] SR-152 rationale -> the CI re-run has no crossing of its own in the frame, and the frame handles an uncontrollable external as at REL-003 -> the re-run crosses at B-11 with the row still attached to B-05 -> the requirement, acceptance and Boundary-Refs (B-05) are unchanged; the paragraph that changed is the rationale's account of the frame, and the honest-limit obligation (no continue-on-error, no conditional skip, the harness's exit as the job's) reads identically on both sides.
- [CLARITY] SR-157 rationale -> realizes SN-025 as "(queue-overlap visibility)" -> realizes SN-025 as "(the tracked work-item graph the loop derives its next work from is kept coherent)" -> a four-word parenthetical replaced by the need's own acceptance language; this is the correction WI-604's finding 4 asked for and it names the same need. The requirement, the acceptance and the rule inventory they range over are untouched.
- [MEANING] LLR-160 detail -> the third signal fires on a shared anchor-stripped SpecRef: two open rows citing any two sections of one document are one pair -> two SpecRefs share a spec when their files match and their anchors are equal or one has none: two different sections of one document are two specs, a whole-document reference covers every section -> a pair the old text reported (`thing.md#part-a` beside `thing.md#part-b`) is silent under the new one; the case set moved. Blessed: `check_trajectory.queue_conflict_pairs` reads `kitlib.registry.shared_spec` and `tests/test_loop_order.py` drives all four anchor cases (TC-155's evidence).
- [MEANING] TC-077 tier -> Smoke: the evidence runs in the per-commit bar -> Full: it runs at the gate bar -> the condition on when the evidence must be green moved (the WI-669 ruling on TC-192). Blessed: its evidence is `tests/test_trajectory.py`, a `SLOW_MODULES` member, so the old cell was false and the new one is true.
- [MEANING] TC-086 tier -> Smoke -> Full -> as TC-077. Blessed: `test_trace.py` and `test_trajectory_staged.py` are both slow.
- [MEANING] TC-100 tier -> Smoke -> Full -> as TC-077. Blessed: `test_trajectory.py` is slow.
- [MEANING] TC-067 tier -> Smoke -> Full -> as TC-077. Blessed: `test_bootstrap.py` and `test_trajectory_arch.py` are both slow.
- [MEANING] TC-068 expected, tier -> "unknown OR UNJUSTIFIED seams warn/fail strict; resolvable, JUSTIFIED, intra-module and unarmed cases pass", at Smoke -> "unknown seams warn/fail strict; resolvable, intra-module and unarmed cases pass, and a draft seam cited with no rationale is silent", at Full -> the Expected cell withdrew a case (the rationale-on-a-draft-seam arm) and replaced it with its negation; a checker that still demanded the rationale would pass the old cell and fail the new one. The tier moved as TC-077's did. Blessed: `test_the_anti_duplication_rationale_arm_is_RETIRED_not_re_keyed` asserts "with no rationale" never prints and IF-050 is never named, plain or `--strict`, and all five pointers passed; `test_trajectory_arch.py` is slow.
- [MEANING] TC-198 tier -> Smoke -> Full -> as TC-077. Blessed: `test_trajectory_staged.py` is slow.
- [MEANING] TC-189 tier -> Smoke -> Full -> as TC-077. Blessed: `test_trace.py` and `test_trace_interfaces.py` are both slow.
- [CLARITY] LLR-051 detail -> renders the Process tab's three panels, byte-deterministic, `--check` unchanged; "the tab is part of the adopted toolkit's generated project-state view (REL-002 output), not a system output" -> the same panels and determinism; "the tab is part of the generated project-state view, an output of the kit in operation read by the human operator across B-09" -> every clause a builder implements or a test pins is unchanged; the closing sentence re-places the rendered view in the redrawn frame (an operation-system output across B-09 rather than an out-of-system REL-002 output). The frame moved by the C1 ruling; this cell followed it and changed no obligation.
- [CLARITY] LLR-056 detail -> the station-cycle panel; "(REL-002 output), not a system output" -> the same panel; "an output of the kit in operation read by the human operator across B-09" -> as LLR-051.
- [CLARITY] LLR-057 detail -> the tiered decomposition polish; "(REL-002 output), not a system output" -> the same polish; "an output of the kit in operation ... across B-09" -> as LLR-051.
- [CLARITY] LLR-139 detail -> the pause bullet in the pending region; "(REL-002 output), not a system output" -> the same bullet; "an output of the kit in operation ... across B-09" -> as LLR-051.
- [CLARITY] LLR-124 detail -> the status snapshot is regenerated by the trunk lane only; "an adopted-toolkit output surface (REL-002), not a system-under-development output; a work branch never commits the artifact" -> the same trunk-only regeneration; "an output of the kit in operation, read by the human operator across B-09; a work branch never commits the artifact" -> as LLR-051; the work-branch prohibition survives verbatim.
- [CLARITY] SR-175 rationale -> the pull-channel limit: the declared rule cannot technically bound an invoked runner, "the same no-design-control reading the frame applies to external actors at REL-003 and the B-06/B-07 cut" -> the same limit: "the loop's invocation crosses the operation frame at B-10, and the runner on its far side (EXT-005) is outside this system's design control" -> the requirement and acceptance are unchanged; the rationale's last clause re-cites the redrawn frame (EXT-005 and B-10 exist in external.toml). The obligation on what the loop ASSEMBLES and what the consent surface CONSENTS to reads identically.
- [MEANING] LLR-180 detail -> three verdicts (untraced, dangling, anchored) over the union of every listed module's bindings, and four skips -> the same three verdicts, plus a new untraced-class count: for an anchored row listing two or more checkable modules, each listed module in which none of the row's identifier tokens binds is an unbound module, listed by `--show-untraced`, counted in the summary, never dangling and never the exit code; `main` and any name every CLI module defines do not bind for that count -> a new reported class with a stated grammar (which rows are judged, which tokens are generic, which channel carries it); a checker correct under the old text reports nothing for it. Blessed: `check_doc_refs.unbound_modules` and `_generic_names` read exactly as the cell says (two or more checkable modules; `main` plus the intersection over two or more CLI modules; the `UNBOUND` phrase carried per entry) and `symbol_findings` returns it as its fourth value into the untraced total.
- [MEANING] TC-175 method -> the anchor suite over planted registries: nine arms -> the same nine arms, then the unbound-module count exercised on its own: counted for a listed module none of the tokens binds in, listed only by `--show-untraced`, never a warning or the exit code; a generic token does not bind; a one-module row is left to the anchor verdict; the summary counts entries and not the phrase -> four new arms a test must drive. Blessed: the four named `test_check_doc_refs.py` tests exist and passed with the rest of the module.
- [MEANING] SR-198 requirement, acceptance_criteria -> refuse an observation case declaring a lifetime under seven days or a policy outside the pair -> also refuse one declaring an input path outside the repository (absolute, or still climbing out with `..` once normalized) -> a new refusal class: a registry the old harness accepted (an absolute input) now fails the check naming the row. One `shall`, the EARS shape unchanged. Blessed: `assumption_rules.input_escape` and `_escape_failures` implement exactly that rule, in either separator style, with `docs/../src` inside.
- [MEANING] LLR-233 detail -> `observation_tc_findings`' failure set: max_age, sampling, sample_size, acceptance_rule, one model cell without the other -> the same set plus an inputs entry naming a path outside the repository (`input_escape`) -> a new failure composed into the always-on integrity class. Blessed: the code names `input_escape` as the one rule the declaration check, the writer and the checkpoint all apply, and `rejudge._support_paths` reads it.
- [MEANING] TC-228 expected, method -> a lifetime under seven, an out-of-pair policy or a malformed model fails -> also an input path outside the repository fails, in either separator style, naming the row and the input, while `docs/../src/a.txt` passes -> a new arm a test must drive. Blessed: `test_an_input_outside_the_repository_fails_naming_the_row_and_input` (parametrized over the absolute, drive-qualified and climbing shapes) and `test_an_input_inside_the_repository_passes` exist and passed; the tier stays Smoke and `test_assumption_rules.py` is not slow.
- [MEANING] SR-212 title, requirement, acceptance_criteria, rationale -> fail the ARCHITECTURE gate for an interface-form requirement no boundary interface reaches, or reached by an interface neither coincident nor bridged by a cited assumption -> also fail the BOUNDARY gate, once per declared crossing the requirement names on which no assumption it cites lands, unless the requirement is recorded coincident; an undeclared crossing is not judged here -> a second gate at an earlier rung with its own failure grammar: a harness correct under the old text passes a boundary-rung tree the new text fails. The requirement keeps one `shall` under its `Where`. The title and rationale follow the same change. Blessed: `assumption_rules.crossing_gate_findings` reads Boundary-Refs against `EffectAt` over cited DA-Refs, skips a coincident row and an undeclared crossing, and `check.py` lists `crossing-allocation` at `STAGE_BOUNDARY` beside `interface-allocation` at `STAGE_ARCH`.
- [MEANING] LLR-244 detail, title -> `module_srs`, `if_reached_srs`, `interface_form_gate_findings`, the `interface-allocation` step at DevStg-Arch -> the same, plus `crossing_gate_findings(srs, das, bifs)` as the Boundary arm and a built-in `crossing-allocation` step at the DevStg-Boundary threshold, gated by the same setting -> a new function and a new step. Blessed: both exist as named; `code_symbol` and `module` (traced cells) moved with them.
- [MEANING] TC-239 expected, method -> the interface-allocation step's cases at DevStg-Arch -> also the crossing-allocation step's seven cases (coincident passes; an assumption landing on the crossing passes; one landing elsewhere fails naming both; two crossings bridged on one fails naming only the other; citing none fails; an assumption-form requirement and an undeclared crossing are not judged), advisory with the gate off, listed at DevStg-Boundary -> new arms a test must drive. Blessed: `test_the_boundary_arm_fails_each_crossing_neither_coincident_nor_bridged`, `test_the_boundary_arm_is_advisory_with_the_gate_off` and `test_the_boundary_step_lists_at_the_boundary_rung_and_is_built_in` exist and passed; the tier is Full and `test_assumption_gate.py` is slow.
- [MEANING] LLR-254 detail -> `checkpoint_drafts` digests each case's declared inputs as read from git at the revision -> the same, and a committed link is not content: never written into the extracted tree, excluded from the digest by the writer's own link predicate, so a declared link reads as absent, a link inside a declared directory contributes nothing, and a change to a link's target makes no case due -> a class of input (a link) whose treatment the old text left to the implementation is now fixed the other way from what a naive reader would do (follow it). Blessed: `rejudge._archive_chunk` collects link members without writing them and `_digest` hands them to `record_observation.inputs_digest` as `links`, the one predicate `is_link`.
- [MEANING] TC-247 method -> the checkpoint driven on a real repository: changed, expired, absent, unchanged, no-input, open-item and archive cases; inputs read at the revision -> the same, plus the committed-link arm: a result recorded on a declared link or a directory holding one is not due where the platform cannot create a link, a change to the link's target does not make it due, a directory link to itself is harmless -> new arms a test must drive. Blessed: `test_a_committed_link_is_not_content` (parametrized over the link and its directory) and `test_a_directory_link_to_itself_is_harmless` exist and passed on this box; the tier is Full and `test_rejudge.py` is slow.

## How the cells were read

- Before and after were compared as obligations, per the brief. The nine
  CLARITY rulings are all on a rationale or on the closing frame-attribution
  sentence of a `detail` cell, where the requirement, acceptance and every
  mechanism clause are byte-identical on both sides and only the account of
  WHY, or of WHERE in the C1 frame the artifact sits, moved. On each I asked
  whether a builder or a test author correct under the old text could fail
  the new one; none could.
- The twenty MEANING rulings each add or withdraw a case, a class, a rung, a
  lifetime or a tier, and each was checked against the code and the tests
  named above before being blessed. No MEANING row is withheld from the
  re-attest.
- The CLARITY rows' text also differs from the snapshot copy. The act's
  `--reattests` names the MEANING rows only; if the copy refuses on a CLARITY
  row's drift, that refusal and its resolution are recorded in the act's
  commit and in the report, never by widening the verdict.

Bar I produced (not claimed), on this tree with `python -m pytest -q -n 4
-p no:cacheprovider`:

- `tests/test_check_doc_refs.py`, `tests/test_assumption_gate.py`,
  `tests/test_rejudge.py`, `tests/test_loop_order.py`, the five named
  `tests/test_trajectory_arch.py` tests (TC-068) and the three named
  `tests/test_gen_arch_map.py` tests (TC-175): **126 passed, 1 skipped in
  48.00s**. The skip is `test_rejudge.py:700`, this box cannot create a
  symlink (WinError 1314), the platform case TC-247's own method names.
- `tests/test_assumption_rules.py` ran in the first-approval batch:
  green (see WI-681's verdict for the counts).
- The seven tier rows were checked against `tests/conftest.py
  SLOW_MODULES` loaded in process: every module they cite is slow.

No failures, no errors.

## Dispositions

At the first sitting none were owed. At the second sitting (below) TC-055's
amended Expected was a MEANING row whose new text was not blessed as worded,
and its corrective clause was drafted in the spec's `## Dispositions`. At the
third sitting the cell carries that clause and is blessed; the draft is
withdrawn and none is owed.

## Non-blocking findings (surfaced, not acted on)

1. **SR-151, SR-152 and SR-175 now argue B-10/B-11 in their rationale while
   their `Boundary-Refs` stay `B-05`**, and `trace.py` reports B-09, B-10 and
   B-11 as crossings named by no requirement. The rationales are consistent
   with the frame (the row constrains what ships at B-05; the runner or
   provider is the far party); whether the frame wants a requirement to NAME
   those crossings is the C1 frame's open question, not this act's.
2. **TC-055's Expected still says the verdict "is a one-time judgement that
   nothing re-fires."** With `max_age = 90` the re-judge checkpoint now does
   re-fire it; the sentence is now the weaker of two true statements. A
   clarity amendment would remove the tension.
3. **SR-198's new acceptance and LLR-233 apply the escape rule to declared
   inputs; TC-036 and TC-055 declare registry ids as inputs** (`SR-036`,
   `SR-054`, `LLR-055`). `rejudge._support_paths` resolves an id through the
   registries, so this is supported, but no cell of SR-198 or LLR-233 says an
   id is a legal input; the rule is stated only in `input_escape`'s docstring.
4. **LLR-160's amended clause names `kitlib.registry.shared_spec` nowhere**
   while the code delegates to it; the cell states the rule, the code's home
   for it is a traced fact. Nothing to fix unless the registry wants the
   symbol in `code_symbol`.

## Second sitting, 2026-09-27 — after wave-5 arbitration ruling 1

The first act (8a960cf1) was reverted (c7c2128e) on Sol's blocker: TC-055
was re-attested while its Expected still called the verdict "a one-time
judgement that nothing re-fires" beside a declared `max_age = 90`. My
first-sitting line called that "the weaker of two true statements"; it was
false, and non-blocking finding 2 below records the error as I wrote it.
The coordinator then amended TC-055's `expected` and SR-054's `rationale`
in place (762534c9), status left Approved, and added SR-054 to this row's
scope: 30 rows. I authored neither amendment.

- TC-055 is re-ruled above on its full amended text: MEANING, and NOT
  blessed as worded, because "re-judged only when a declared input changes
  or the record passes its declared max_age" omits the checkpoint's
  no-record trigger, which is the very reason the next merge will re-judge
  it. Driven, not read: `rejudge.due_cases` on HEAD returns TC-036, TC-055,
  TC-209, TC-210 and TC-211, each "no result recorded".
- SR-054 is ruled above: CLARITY, blessed.
- Per ruling 1 the act is re-taken once. `--reattests` names the 29 rows I
  bless (the 20 first-sitting MEANING rows less TC-055, the nine CLARITY
  rows the copy refused on by name last time, and SR-054); TC-055 is left
  out, as the brief directs for a MEANING row whose text is not blessed. If
  the copy refuses on TC-055's drift, that refusal is reported verbatim and
  the act waits for the one-clause amendment.

Counts after this sitting: 20 MEANING (19 blessed, TC-055 withheld), 10
CLARITY (the nine first-sitting rows and SR-054); 29 rows in the act's
`--reattests`.

## Third sitting, 2026-09-27 — TC-055 re-judged on its amended clause

The coordinator replaced the withheld sentence (bf2b9f5c, status left
Approved, nothing else changed) with the clause the second sitting drafted:
"the verdict recorded in Evidence is re-judged at a merge or release
checkpoint when no result of it is on record, when a declared input changes,
or when the record passes its declared max_age, never on every commit."
Judged again on the full amended text against the checkpoint: the three
triggers are `rejudge._judge`'s three, in the order it asks them
(`WHY_NEVER`, `WHY_CHANGED`, `WHY_EXPIRED`); the two checkpoints are
`rejudge.CHECKPOINTS`; `due_cases('.', HEAD)` still returns TC-055 "no result
recorded", which the cell now says; the five inputs pass `input_escape` and
90 clears the seven-day floor. The closing sentence ("as old as its latest
recorded verdict") stands.

- TC-055: MEANING, BLESSED. Joins `--reattests`; the act re-attests all 30
  rows (20 MEANING, 10 CLARITY). The corrective draft is removed from the
  spec's Dispositions, since the cell carries the fix; the note on the five
  due observation cases with no re-judge row stays there for WI-679.

VERDICT: MEANING rows=30
