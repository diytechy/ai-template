# ADJUDICATE — WI-691 — first approval at 1d84d77c

Independent adjudication of the thirteen spine rows WI-616 authored or
re-authored `Drafted` that the `human_approval_through = "DevStg-Boundary"`
dial releases to an adjudication session: batch B's six returns re-authored
(LLR-205, LLR-206, LLR-262, TC-201, TC-203, TC-204) and seven new rows
(LLR-274, LLR-275, LLR-276, TC-273, TC-274, TC-275, TC-276). The one question:
is each row ready to be APPROVED as it stands, or does it go back with
findings. `Approved` blesses the row's TEXT; I ran the tests anyway.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chains of SR-017, SR-154, SR-156, SR-157,
SR-163, SR-176, SR-183 and SR-198 in full, about 200k characters, read in
parts; LLR-272 and TC-270 shown as WI-694's rows; anchor
`docs/archive/last_approved` copied at 464dc7ac). Every row was read upward,
sideways and downward; every evidence pointer resolved by file and function
name; every named code symbol located in its module; every Tier cell checked
against `SLOW_MODULES` loaded in process; every rationale and method read for
the cell-hygiene defects batch B returned these rows for. Disclosure: I read
WI-691's queued spec for its Context, WI-681's verdict and its Dispositions
draft as the statement of what the re-authoring owed, and the arbitration
file (rulings 2, 3, 11 to 16, 18) as context for why, never evidence. HEAD
stayed at 1d84d77c throughout; the worktree was clean before this file was
written.

- [APPROVE] LLR-205 -> `SECRET_CLASSES`, a tuple of `SecretClass(name, scan_pattern, redact_pattern)` rows over seven credential classes, either pattern None as a stated per-class decision; `check_privacy.py`'s `KEY_RE`/`TOKEN_RES` and `agent_common.py`'s `_SECRET_RES` derived by comprehension so LLR-017's and LLR-177's symbols resolve unchanged; no exhaustiveness claim; the redactor deliberately looser on three classes with the reason -> SR-017 and SR-176 both cite it and the divergence it closes is a real gap between their obligations; every clause is true of `kitlib/secret_classes.py` (stdlib `re`/`typing`, seven rows), `check_privacy.py:196-199` and `agent_common.py:2572`; CMP-006 follows the ladder.py precedent the rationale argues -> ready: batch B's return is answered in full — the "Landing Drafted" sentence, the "live, dated finding" phrase and the plan citation are gone from the rationale, the pre-table narration is gone from the detail, and what remains states the standing reason (two consumers compiled apart disagree, so the vocabulary lives below both) and which alternative lost. The rationale's "the same test kitlib/spine.py was ruled into existence for" is an argument by precedent, not the row's own history; noted below.
- [APPROVE] TC-201 -> `Scanner` and `redact_secrets` driven three ways against a shared sample set: a five-sample decision table (a PEM block caught by both; a Bearer token, a short GitHub token and a short API key caught by the redactor alone, the three declared asymmetries); one canonical positive per class reaching each consumer through the comprehension; a frozen, independent pattern record per module compared by matching behaviour over threshold-straddling probes so no class is caught less than that record catches -> `tests/test_kitlib_secret_classes.py` holds the three batteries (green, one parametrized case skipped by design: the generic bearer token has no scan pattern, the None the LLR states); the Method now states each arm as a standing claim with no "now"/"was"/"BEFORE this table" narration -> ready. Tier Full over a fast-only module is LLR-260's advisory class, never false; noted below.
- [APPROVE] LLR-206 -> `cognitive()` by recursive descent with nesting, the elif flattening, the BoolOp run rule, the recursion increment; `census()` keyed on (path, qualified name) with a never-compared public-symbol count; `main()` comparing strictly-over-threshold rows by exact equality both ways, printing the three remedies, honouring no suppression token, `--report`/`--restamp`/`--mode warn`/`--mode enforce` as stated; the shipped template report-only, this repository's `[step:complexity]` at DevStg-Impl running `--mode enforce` over scripts and tests -> every clause is true of `check_complexity.py` (the argparse choices, `return 1 if args.mode == "enforce"`, no pragma) and of `docs/stack.ini` (`[step:complexity]`, `layer = product`, `from-stage = DevStg-Impl`, `--mode enforce`); TC-202 and TC-203 pin it -> ready: batch B's return is answered — the "Landing Drafted" sentence is gone and the rationale ends on the suppression-token argument.
- [APPROVE] TC-203 -> synthetic fixtures run through `check_complexity.py` as a subprocess: `--report` exits 0 with the census, a matching baseline is OK under enforce, growth and an unstamped improvement and a vanished entry each exit nonzero under enforce with the remedies, a suppression-shaped comment changes nothing, repeated `--include` globs widen, an absent directory is vacuously OK; "the module runs at the full tier, each case paying interpreter startup" -> nine tests in `tests/test_check_complexity_cli.py`, green (slow batch); Tier Full is true, the module is slow; the closing sentence now states where the evidence runs and why, with no "Re-tiered" event -> ready.
- [APPROVE] LLR-262 -> the coordinator's session log names each session's phase and exact range; `scope_offenders` names every changed path but the REVIEW session's own round file; the loop stops needing a human on any offender right after the session; every reader takes a log as the commit that added it recorded it; the merge ladder refuses a modified or deleted log by name and re-derives the scope rule from every committed REVIEW log; leftovers after a REVIEW or CRITIQUE session fail the draw and are stashed under one named entry, a failed stash stopping the run; `read_verdict` reads the blob at HEAD in both arms; `logged_rounds` reads a round at the end of its range only when the range changed it; `done_when.items`/`changes` with the evidence grammar over the closed set LANDED, DONE, MET, VERIFIED, SHIPPED, PASSED, FIXED and COVERED; the claim warns by name on a missing Done-when; the review brief quotes each change; the intake mints one brief-less adjudication row per changed Done-when -> SR-154 and SR-156 both demand that the records the seam judges are not the judged lane's to rewrite; all twenty-one named symbols exist across the five modules the `module` cell lists; `done_when._EVIDENCE_TOKEN_RE` is exactly the eight words the cell now lists; TC-257 and TC-259 (approved in batch B) drive it, and `trace.py` raises the "Drafted but every citing TC is Approved" advisory on it today -> ready: batch B's return is answered — the open "such as" list is the closed set, and the flipped tree raises no requirement-form finding on the row. The row's width (five modules, one property) stands as batch B surfaced it; not returned on.
- [APPROVE] LLR-274 -> `absolute_advisories(needs, srs, llrs)` over the tier matrix `ABSOLUTE_CELLS` (need and acceptance with `why`; Requirement and AcceptanceCriteria with Rationale; Detail with Rationale), no test-case tier, `-000` and waivered rows skipped; `absolutes(cell)` cutting clauses at `;:()?!`, en or em dash, or a sentence-ending full stop, commas cutting segments and segments into lower-cased hyphen-joined words; a universal taking the next six words of its own segment, "at all" emphasis; a negative counting only as the first word of the clause's first segment and not before a comparative; a temporal taking its whole clause across commas; suppression by `CLOSED_DOMAIN_WORDS`, an adjacent `CLOSED_DOMAIN_PAIRS` pair or an id token; one advisory per row and cell naming the waiver's cell; `absolute_summary` one console line per tier, `absolute_report_lines` the report section; neither joins a failure set -> SR-157's acceptance names the never-gating advisories as in scope; every clause is true of `absolute_terms.py` (`_CLAUSE_RE`, `_segments`, `_domain`, `_closed`, `_WAIVER_RE`, `DOMAIN_WINDOW = 6`), rulings 12 and 16 are answered in the text, and the rationale argues the lexical-not-semantic choice, the negative rule's measured alternative and the test-case exclusion; TC-273 drives it -> ready.
- [APPROVE] TC-273 -> in-memory rows: THE MATRIX (an open-world absolute in each scanned cell one advisory, the same text in a reason cell nothing, no test-case tier, a placeholder nothing); THE PREDICATE (a declared set, registry, row noun, id or id token suppressed; open world or open time warned; `recorded waiver:` in the reason cell silencing the row while the marker in the scanned cell or a mention without it waives nothing); THE TOKENIZATION (hyphenated compound, clause-opening negative only, `no` before a comparative, `all` after `at`, the six-word window in its segment, temporal across commas, whole-word case-insensitive); THE OUTPUT (the quoted terms, the waiver cell, the summary line, the report section); THE CHECKER (a planted absolute through `trace.analyze` landing in `absolute_advis` alone, exit 0 under every flag) -> `tests/test_absolute_terms.py`, the module as its evidence, green (fast batch); Tier Smoke is true, the module is not slow; IF-252 exists -> ready.
- [APPROVE] LLR-275 -> `delivery_inventory()` returns (sources, exclusions, conditional, generated): every physical file under the kit less bytecode caches; the reasoned kit-only exclusions, a `this-repo` skill entered with its scope as the reason; the conditional copies (agent hooks, kit-scope skills once per agent's skills directory through `skill_copies`, knowledge packs); the generated outputs (the license and version stamps, the report, the open-items page, the `.gitkeep` directories) naming their generator source -> SR-163's universe must be independent of the declaration it grades or a deleted row is invisible; the rationale says so and why a generated output names its generator; every clause is true of `bootstrap.delivery_inventory`; Component CMP-009 -> ready: this closes batch B's finding that SR-163's checker had no design row.
- [APPROVE] LLR-276 -> `mapping_purpose_findings(entries, present, sr_by_id, sn_ids, declared_absences, delivery)` pure with the environment injected; given the delivery universe a source neither mapped, excluded nor conditional is `missing_file` and a classified source absent from the package or both mapped and excluded is `stale_entry`, then the generated and present conditional outputs join as entries carrying their source row's reference; a bare pair `unmapped_file`, an unresolved reference `unresolved_reference`, an absent undeclared destination `missing_file`, a present declared absence `stale_entry` unless its reason opens `LIFECYCLE:`; `MAPPING_FINDING_POLICY` gating the first two and warning the rest; `mapping_purpose_report` a count line per class and a line per finding; `gen_arch_map --mapping-purpose` exiting 1 on a gate-class finding -> every clause is true of `gen_arch_map.py` (`MAPPING_FINDING_POLICY`, `_delivery_source_findings`, `_inherited_delivery_entries`, the `LIFECYCLE:` test, `resolve_requirement_reference`); the rationale argues purity for one grading function and the gate/warn split; TC-204 and TC-274 drive it; Component CMP-006 beside LLR-204 -> ready.
- [APPROVE] TC-204 -> THE CELL (`mapping_entries` normalizing every row, a bare pair surviving as None), THE INDEPENDENT UNIVERSE (`delivery_inventory` classifying every physical source and enumerating generator outputs), THE CHECKER on one synthetic inventory with one defect per class and a clean control, THE POLICY (warn-first for the reference classes, gate for missing and stale), THE STANDING EVIDENCE over the live package census, MAPPING literal and this repository's spine -> ten named pointers in `tests/test_mapping_purpose.py`, each resolving and green (fast batch); Tier Smoke is now true, every pointer is in a fast module and the CLI bite batch B returned it for has moved to TC-274; the Expected now claims SR-163's acceptance through LLR-275 and LLR-276 -> ready.
- [APPROVE] TC-274 -> the real-row end-to-end bite: remove `process.toml.template -> docs/process.toml` from MAPPING in a child process with the source still in the package, drive `gen_arch_map.main()` through `--mapping-purpose`, require a gate-class `missing_file` naming the omitted source -> one named pointer in `tests/test_mapping_purpose_cli.py`, resolving and green (slow batch); Tier Full is true, the module is slow -> ready.
- [APPROVE] TC-275 -> `verification_coherence_advisories` on in-memory requirements: an Inspection row whose subject before its `shall` names a Critique acceptance record, with rubric and VERDICT prose, raising nothing; the same row under Test, Analysis or Demonstration raising one advisory naming the row, the cells and the method; an Inspection row about something else whose acceptance directs a fresh CRITIQUE session to return APPROVE raising one; one naming a Critique record only after its `shall`, one with no `shall`, one mentioning Critique without a record, each raising one -> `tests/test_verification_coherence.py`, the module as its evidence, green (fast batch); Tier Smoke is true; it verifies SR-157 directly, the advisory being one of the never-gating classes SR-157's acceptance names, and rulings 13 and 18's counterexamples are its arms -> ready.
- [APPROVE] TC-276 -> a registry row id as a declared input three ways: THE DECLARATION (an observation case naming SR-184, LLR-233, TC-055, SN-043 and DA-001, alone and beside a path, raising no failure and no advisory, the id no escaping path); THE SUPPORT PATHS (the checkpoint's support paths for an id being the registry directories and never a file named after it, a path input its own); THE DIGEST (over a two-row requirement registry, SR-184's digest differing from an unknown id's, unchanged when only the other row is edited, changed when SR-184 is) -> one named pointer in `tests/test_assumption_rules.py` and `tests/test_registry_id_inputs.py` whole, resolving and green (fast batch); Tier Smoke is true, both modules are fast; ruling 15's vacuity is answered by the support-path and digest arms; LLR-233's amended Detail (WI-690) states the rule it verifies -> ready.

## How the chain and the anchor were read

- Upward: the eight parent SRs as the brief printed them; SN-002, SN-007,
  SN-009, SN-012, SN-024, SN-026, SN-038 and SN-043 where a row's derivation
  depended on the need's words. Sideways: every approved sibling in the eight
  chains, read for overlap with the row under judgement; WI-694's LLR-272 and
  TC-270 read and left byte-exact. Downward: every evidence pointer resolved
  by test function; every code symbol located.
- Anchor: the record at 464dc7ac holds the six re-authored rows at `Drafted`
  (batch B's returns, copied as returned) and none of the seven new ones, so
  nothing here is a re-attest; the act names the LLR and TC registries.
- The flipped tree was driven through `trace.py --root . --strict` and
  `--strict-integrity`: no form or provenance finding on any of the thirteen
  (LLR-262's "such as" is gone); only the expected never-rode-a-copy findings
  the act clears.

Bar I produced (not claimed), on this tree with `python -m pytest -q -n 4 -p
no:cacheprovider`: the fast batch (`tests/test_kitlib_secret_classes.py`,
`tests/test_check_complexity.py`, `tests/test_absolute_terms.py`,
`tests/test_verification_coherence.py`, `tests/test_mapping_purpose.py`,
`tests/test_assumption_rules.py`, `tests/test_registry_id_inputs.py` among
fourteen modules): **448 passed, 1 skipped in 16.80s** (the skip is
`test_kitlib_secret_classes.py:214`, "generic bearer token had no pre-WI-520
scan pattern", by design); the slow batch (`tests/test_check_complexity_cli.py`,
`tests/test_mapping_purpose_cli.py` among eight modules): **372 passed, 1
skipped in 195.57s** (the skip is `test_dogfood_sync.py:189`, an empty
parameter set, unrelated). TC-257's and TC-259's modules were not re-run;
both cases are approved and their text is unchanged. No failures, no errors.

## Dispositions

None owed: every row is approved.

## Non-blocking findings (surfaced, not acted on)

1. **LLR-205's rationale still argues by precedent** ("the same test
   kitlib/spine.py was ruled into existence for ... nine equality pins") —
   an argument, not the row's history, and I did not return on it; a later
   clarity trim could state the rule without the precedent.
2. **TC-201 is Tier Full over a module that is not slow**, LLR-260's
   advisory class; re-tiering it to Smoke would cost milliseconds.
3. **LLR-262 remains the widest design row in the registry** (five modules,
   twenty-one symbols); batch B's split suggestion stands.
4. **TC-275 verifies SR-157 with no design row** for the verification-
   coherence advisory; OI-72's direct-TC state, honest as it stands.

OUTCOME: APPROVE rows=13
