# ADJUDICATE — WI-705 — first approval at 126cf5f2

Independent adjudication of the seven spine rows WI-557 authored `Drafted` on
merged trunk (the delegated-decisions record, OI-74 and OI-75), which the
`human_approval_through = "DevStg-Boundary"` dial releases to an adjudication
session: SR-225 (a labelled derived requirement), LLR-282, LLR-283, LLR-284,
TC-292, TC-293 and TC-294. The one question: is each row ready to be APPROVED
as it stands, or does it go back with findings. `Approved` blesses the row's
TEXT; the harness answers whether its tests pass, and I ran them anyway.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chain of SR-225 in full; anchor
`docs/archive/last_approved` copied at 464dc7ac for the SR registry and
eecd656d for the LLR and TC registries). Every row was read upward, sideways
and downward, every evidence pointer resolved by file and function name, and
every named code symbol located and read in its module. Disclosure: I read
WI-705's queued spec for its Context and the spine-authoring skill for rule
(c); the arbitration file (rulings 39 to 43) was context for why, never
evidence. HEAD stayed at 126cf5f2; the worktree was clean before this file was
written.

- [APPROVE] SR-225 -> where the declared decision-recording dial asks for a record, the delivered loop content judges a closing lane against that run's decisions record: refusing to integrate the lane when the record is absent, naming where it belongs, and reporting without refusing each entry of a present record that omits a required disclosure field or leaves one blank; the acceptance fixes the off/undeclared vacuity, the refusal by path for a complete, cancelled or partial close, the pass for a lane carrying its record, each malformed shape reported by entry and none refusing, unjudged extra keys and the inert -000 entry, the dial value outside its three refused as configuration before the record is read (trimmed and case-folded), and the session note handed to a build or adjudication session and not to a review session -> a labelled DERIVED requirement under SN-029, judged by the skill's rule (c): (i) `Hat-Refs` UNATTENDED-OPS, a roster name whose `listens_for` ("a failure that pages nobody ... a green that is green because nothing looked") is the failure the rationale names in those words, and SN-029 carries the `unattended`/`loop` tags that reach it; (ii) the rationale argues the lens, says why SN-029's text (a record of each approval on a released tier) does not itself name the other calls a run makes, and names the alternative that lost (a prose instruction, which degraded as soon as nothing read it) and each design call's reason (why the dial, why every close, why report-not-refuse for a malformed entry, why configuration is judged first, why the record is never a route for work); (iii) fed back upward in its last sentence. One `shall` under a `Where` opening (ruling 43 answered), refusal and report as its two responses. Voice: no file or symbol named at the SR — the path, the keys and the module live at the LLRs and IF-255/IF-256. No citation frame. Sideways: SR-144 owns the per-close report the same rung reads first, SR-209 the provenance trailer, SR-215 the merge checkpoint; none decides what a delegated run discloses. Downward: LLR-282/283/284 decompose the dial, the record and the merge rung, and TC-292/293/294 drive every acceptance clause (each mapped below) -> ready. No `Coincident` waiver and no `da_refs`: honestly unclassified under SR-193's third state (ruling 47).
- [APPROVE] LLR-282 -> `agent_common.decision_recording(docs)` reads `[attestation] decision_recording` through `process_config` and returns one of `DECISION_RECORDING_MODES` (= `kitlib.decisions.MODES`): `off` when undeclared, the value's `mode_word` when that is a mode, and `record` for any other declared value, a wrong-typed one included; `mode_word` is the one normalization (trim, lowercase; `None` for non-text); the key is registered in `PROCESS_ONLY_KEYS` as str and in `PROCESS_KEY_VOCAB` as the three modes, and `config_conflicts` compares through the same `mode_word`, refusing in the dial's own words -> every clause true at HEAD (`agent_common.py`: `DECISION_RECORDING_MODES = _kitdecisions.MODES`, `PROCESS_KEY_VOCAB[("attestation","decision_recording")]`, `decision_recording` returning `"off"` / `declared if declared in ... else "record"`, `mode_word` at its own definition, `_mode_vocab_findings` naming the three values); the row adds the design SR-225 does not state (undeclared -> off, unrecognized -> record, one normalization, the alphabet's one home) and its rationale says what breaks under each alternative; Module and Component (CMP-008, the loop's) resolve; own `Hat-Refs` empty, correctly — the parent carries the lens -> ready.
- [APPROVE] LLR-283 -> `kitlib/decisions.py`, importing nothing and reading no file, git or environment: `record_path(run)` = `docs/decisions/<run>.toml` with `/` -> `-`; `record_findings(text)` one finding when the text does not parse, else one per defect (a `decision` key that is not a table; an entry id not `D-<digits>`; an entry not a table; each `REQUIRED_KEYS` key absent or not a string; one of the first four blank after trimming; a `high_risk` absent or not a list of strings; each hoisted id the table lacks), `-000` ids skipped wherever they appear, extra keys unjudged, never raising; `owed(mode, outcomes)` true under `record`/`escalate-first` with at least one outcome whatever it is; `session_note(mode, run)` empty under `off`, else the instruction naming the path, the keys, the hoist and the not-an-exit rule, with one more sentence under `escalate-first` -> every clause read true in the module at HEAD (`_ENTRY_ID_RE`, `_inert`, `_entry_findings`, the `high_risk` arm returning before the hoist check, `owed`'s `MODES[1:]`, the note's text); IF-255 (file) and IF-256 (call) exist with the contracts the module's docstring carries; the row decides the record's shape and the obligation's population (every close) and its rationale argues report-not-refuse and no-outcome-word; own `Hat-Refs` empty, correctly -> ready.
- [APPROVE] LLR-284 -> `integrate._decision_record_refusal(root, branch, outcomes)` is a rung of `_merge_refusal` reached through `_close_record_refusal` directly after the per-close report rung; reads the dial from the trunk's docs and returns `None` under `off`; returns the first `config_conflicts` finding first, so a dial value outside its alphabet is refused as configuration before any record is read; reads `record_path(branch)` off the branch's tree with `git show`, refusing naming branch, path and dial when absent and `owed`, and printing one line per `record_findings` finding when present; `docs/decisions/` joins the surfaces an adjudication-only lane may touch; `agent_loop.session_body` appends `session_note` for the lane's branch to a build or adjudication session's body, and `reviewer_prompt` composes the review brief apart from that fork -> every clause read true at HEAD (`integrate.py` 2802-2855: `ac.decision_recording`, `ac.config_conflicts(docs)` before the `git show`, the refusal text naming `branch`, `rel` and `mode`, the `print("integrate: decisions record ...")` per finding; line 1888-1890 the `docs/decisions/` surface; `agent_loop.py` 886-889 `kdecisions.session_note(mode, worker["train"])`); the row's rationale argues the placement (beside the report rung, before the bar rung, configuration inside the rung) and why the note is appended at the one fork; Module and CMP-008 resolve; own `Hat-Refs` empty, correctly -> ready.
- [APPROVE] TC-292 -> a policy file under a temporary directory: (a) the three values read as themselves with no conflict; (b) an attestation section without the key, and no policy file, read `off`; (c) a padded value and two mixed-case values read as their word with no conflict, and `mode_word` trims, lowercases and answers `None` for a number; (d) a misspelled value yields exactly one conflict naming the key and the three values and not the rung message, and reads `record`; a boolean is refused by name and reads `record`; (e) the template declares `off` and this repository's policy file `record` -> seven named pointers in `tests/test_decision_record.py`, each resolving by function name (lines 86-143) and passing; every LLR-282 clause has an arm and every SR-225 dial clause (off/undeclared, the three values trimmed and case-folded, the refusal where the policy file is checked, unrecognized -> record) is driven; Verifies SR-225 and LLR-282; Tier Smoke honest — `test_decision_record` is not in `tests/conftest.py` `SLOW_MODULES` and the module runs in-process on tmp_path; Level Unit true; Expected states the condition -> ready.
- [APPROVE] TC-293 -> the `kitlib.decisions` call surface over record texts planted in memory, clause by clause: sound records (two entries, one hoisted; no entries and an empty hoist); each required key absent, non-text (number, boolean, list, table), blank (empty, spaces, whitespace) for the first four and nothing for `review`; the shapes (non-table entry, non-table `decision`, id outside `D-<digits>`, unparseable text); the hoist (string, list with a number, mixed, table, missing, naming an absent entry); extra keys; nine hostile texts never raising; the inert -000 entry and the shipped template; the path with `/` -> `-`; `owed` under each mode for complete, cancelled, partial and mixed closes and not for `off` or no outcomes; the note empty under `off`, naming path, keys and hoist under `record`, one more sentence under `escalate-first`, appended by `session_body` to a build and to an adjudication session under `record` and to neither under `off`, absent from `reviewer_prompt`'s brief -> twenty-two named pointers in `tests/test_decision_record.py`, each resolving (lines 153-349) and passing; every LLR-283 clause and every SR-225 record and session-note clause has an arm (ruling 42's coverage, confirmed by reading); Verifies SR-225, LLR-283 and IF-256 (exists: the call seam owned by `scripts/kitlib/decisions`); Tier Smoke honest (not a `SLOW_MODULES` module, in memory); Level Unit true -> ready.
- [APPROVE] TC-294 -> a claimed lane in a temporary git repository closed into a terminal folder, its record committed on the lane's branch when present, the trunk's policy file declaring the dial: (a) under `record` and `escalate-first`, complete and cancelled closes without a record are refused by the merge ladder naming the path, and a partial close by the rung naming the path; (b) under `off` and undeclared, no refusal names the record and the rung returns nothing; (c) a complete and a partial close carrying a sound record pass the rung with nothing reported; (d) an entry lacking its `alternative` passes the rung and the report names path, entry and key; (e) a misspelled dial makes the ladder refuse naming key and value, not the path; a padded and two mixed-case dials read as their word -> eight named pointers in `tests/test_decision_record_merge.py`, each resolving (lines 78-131) and passing (16 collected: the module parametrizes the two recording modes); every LLR-284 clause and SR-225's refusal, pass, report and configuration-first clauses have an arm, the partial close included (ruling 39); Verifies SR-225, LLR-284 and IF-255 (exists: the file seam); Tier Full honest for a case driving real git repositories through the merge ladder; Level Integration true -> ready.

## How the chain and the anchor were read

- Upward: SR-225 as the brief printed it and as the live file holds it; SN-029
  from `docs/requirements/stakeholder-needs.toml`; the hats roster from
  `docs/requirements/hats.toml` for UNATTENDED-OPS. Sideways: SR-144 (the
  per-close report the same rung reads first), SR-209, SR-215; no sibling
  decides what a delegated run discloses. Downward: every evidence pointer of
  TC-292, TC-293 and TC-294 resolved by file and test function; every named
  symbol of LLR-282, LLR-283 and LLR-284 located and read.
- Anchor: none of the seven rows is in the SR copy at 464dc7ac or the LLR/TC
  copies at eecd656d, so nothing here is a re-attest of this row's rows. The
  act names all three registries.
- Smoke-tier check (batch D's standing rule): TC-292 and TC-293 are `Smoke`
  and cite `tests/test_decision_record.py`, which is not in `SLOW_MODULES`.
  TC-294 is `Full`.
- Method and Rationale cells state the standing system. SR-225's rationale
  names a prose instruction "tried and measurably degraded" — that is the
  alternative that lost, stated as an argument, not a changelog entry; no
  work-item, ruling or date is cited in any of the seven rows.

## Bar I produced (not claimed)

On this tree, `python -m pytest -q -n 4 -p no:cacheprovider` over the six
modules batch D's rows cite: **166 passed in 51.26s**; `tests/test_decision_record.py`
collects 89 and `tests/test_decision_record_merge.py` 16. No failures, no
errors.

## The derived requirement: recommendation to the owner

SR-225 passes rule (c) as written. Keep it derived; SN-029's acceptance could
carry "and a record of the delegated calls a run made beside the record of
its approvals" (the row's own proposed sentence), at which point the row reads
as realized rather than derived.

## Outside this act, noted for the coordinator

This repository's policy file declares `decision_recording = "record"`, so
under SR-225's own rule a lane closing through the merge slot owes
`docs/decisions/build-batch-d.toml`. This adjudication worktree is driven by
the coordinator rather than a claimed loop lane and the assignment's commit
sequence names no such file, so none is written here; whoever lands
`build/batch-d` decides whether the merge path reads that rung.

OUTCOME: APPROVE rows=7
