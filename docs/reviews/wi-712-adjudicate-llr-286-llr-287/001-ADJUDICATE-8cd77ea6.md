# ADJUDICATE — WI-712 — first approval at 8cd77ea6

Independent adjudication of the five spine rows WI-618 authored `Drafted` on
merged trunk (the retirement record: a retired spine row leaves one record of
its own, found by its id), which the `human_approval_through =
"DevStg-Boundary"` dial releases to an adjudication session: SR-226 (a
labelled derived requirement), LLR-286, LLR-287, TC-299 and TC-300. The one
question: is each row ready to be APPROVED as it stands, or does it go back
with findings. `Approved` blesses the row's TEXT; the harness answers whether
its tests pass, and I ran them anyway, because a cell describing a mechanism
no module holds or a test the suite does not run is not blessable text.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chain of SR-226 in full; anchor
`docs/archive/last_approved` copied at e7fe487d for the SR, LLR and TC
registries). Every row was read upward (SN-010 from the needs registry; the
hats roster for MAINTAINER; B-09 and the rest of the crossings from
`external.toml`; IF-257 and IF-258 from `interfaces.toml`), sideways (SR-070,
SR-193, the B-01 rows SR-129, SR-144, SR-173, SR-174, SR-176) and downward
(every evidence pointer resolved by file and function name and read; every
named code symbol located in `retire.py`, `traj_views.py` and
`gen_trajectory.py`). The brief does not render the routed pointer cells, so
`SN-Refs`, `Boundary-Refs`, `SR-Refs` and `Verifies` were read from the live
registries and are ruled below. Disclosure: I read WI-712's queued spec for
its Context and the spine-authoring skill for rule (c); the arbitration file
(rulings 47, 48, 50) was context for why the lane built what it built, never
evidence that a row is true. HEAD stayed at 8cd77ea6; the worktree was clean
before this file was written.

CORRECTED after the first recording (4584cf8e): the flipped tree, driven
through `trace.py --strict` as the act requires, raised the kit's own
requirement-form gate (`trace_text.form_findings`, gating under `--strict`,
applied only to Approved rows, so a Drafted row is silent) on two of the four
rows I had approved. A row the kit's bar refuses the moment it is approved is
not blessable text, so LLR-287 and TC-300 are RETURNED on those cells and
stay `Drafted`; their readings otherwise stand. The same gate holds the
two-`shall` detector, which corroborates SR-226's first finding.

- [RETURN] SR-226 -> when a spine row is retired, the delivered harness leaves one record found by the retired id, written in the same change that deletes the row and naming the id, the date, the successor if any and the reason, and reports without failing a record changed after it landed and a spent id retired since the record began that has no record; the acceptance fixes the exact-row deletion, the refusal set with nothing written, survival of the log fold, the two warn-only reports and their silences, and the deleting commit read from history or reading unknown -> a labelled DERIVED requirement, judged by rule (c): (i) recorded where something reads it — `Hat-Refs` MAINTAINER, a roster name whose `listens_for` ("a requirement whose reason lives only in the session that wrote it") is the failure a deleted row's lost reason is, and the hat applies always; (ii) the rationale argues the lens, says why SN-010's text does not name what a reader finds at a spent id, and names the alternatives that lost (the watermark holds only marks; a forwarding map in the log is prose no tool reads; a record carrying its own commit is impossible); (iii) fed back upward in its last sentence. Routed pointers: `SN-Refs` SN-010 HOLDS — the nearest stated outcome (references a reader can follow and trust), honestly labelled derived from it; `Boundary-Refs` B-09 HOLDS — the record, the Retired tab and the console advisories are what EXT-006 reads. Downward the chain is complete: LLR-286 holds every mechanism, LLR-287 the one set-view, TC-299 drives every acceptance clause but the last and TC-300 the last, and all 45 cited cases pass at HEAD -> NOT ready, on three cells, none of which changes what the children implement or test. (1) `Requirement` carries TWO `shall`s ("shall write ... and shall report ..."): PROCESS.md §3 states "one requirement, one `shall`" and the Singular characteristic ("exactly one `shall`; no compound obligation"); none of the 117 approved SRs carries two, and the kit's own form gate (`trace_text.form_findings`, gating under `--strict` once a row is Approved) reports exactly this, so the row would fail the bar the moment it was flipped. The row states ONE decision — the record, and what keeps it standing — so the remedy is one `shall` over that decision with the reporting as the response's qualifier, never a split: the acceptance criteria and the four children decompose one decision, and TC-299's (e)-(g) arms verify the reporting clauses as this row's. (2) `Coincident` fails approved SR-193's test ("why its own specification ALONE delivers its needs"): the cell says the need asks for this outcome and this row is it, while the row's own rationale says SN-010's text does not name it — the two cells contradict each other, and SN-010 is in any case delivered jointly (the link check, the vision tag, every generated artifact's `--check`), the shape ruling 47 dropped the waiver on for SR-223 and SR-225. The honest state is unclassified, which the SR rung's gate reports without failing, until OI-97 gives the tier a vocabulary; that is a RETURN of the cell, not of the obligation. (3) `Boundary-Refs` omits B-01: the text's "write, in the same change that deletes the row" is a governed write from a session into a registry and a tracked record — B-01's crossing, the one the B-01 rows SR-174 (an identity allocated once) and SR-176 (a durable record of a finding) carry for the same reason — and ruling 27 requires a multi-valued cell to list every crossing the text names. Every other cell is blessable as it stands: the EARS `When` opening states the trigger, the voice names no file (the paths live at LLR-286's Module, IF-257 and IF-258), the rationale carries no citation frame and no vague or open-ended term, `Verification` Test and `Priority` S are true of the chain. Drafted in `## Dispositions` of WI-712's spec.
- [APPROVE] LLR-286 -> `retire.py` is the one home of the record: `retire` judges the whole retirement (a spine id with a nonzero number that is a live row of its tier's TOML registry, a non-blank reason, a real date defaulting to today, a successor that is another live spine id, no existing record) before the first write, `drop_row` cuts the row's table as text and refuses unless the result parses to the old document minus exactly that row, the record is created exclusively and the registry rewritten as working-tree changes for one commit; `fragment_text`/`parse_fragment` fix the four-cell `+++` front matter and refuse every departure from it; `seed_census`/`parse_exclusions` declare the ids spent before the record once, never an excluded id, replaceable only before landing; `missing_findings` is pure and capped at ten; `edited_findings` compares landing blobs from one `git log` against one `git hash-object`, reporting the shallow boundary as unverifiable and nothing off git; `retirement_findings` feeds `trace.py`'s advisories outside every exit code; `records` orders by tier then number and reads the deleting commit from history or unknown; `main` is the command with its exit protocol -> `SR-Refs` SR-226 HOLDS: every mechanism here decomposes a clause of that requirement or its acceptance, and nothing here answers an obligation the parent does not state. Every clause read against HEAD: `_judge`'s refusal order, `drop_row`'s parse-equality guard, `open("x")`, `_shape_problem` (`if body:` so whitespace after the fence is a body), `seed_census`'s `landings` check, `_CAP = 10`, `landings` letting the oldest `git log` chunk win, `shallow_boundary` reading the clone's `shallow` file, `records` reading `unknown` for a parentless landing, `_act` refusing `--exclude`/`--replace` without `--seed`; `trace.py` carries `findings.retired_advisories` from `retire.retirement_findings` and the exit-code test holds them at 0 under both strict flags. Fourteen code symbols, all present; Module resolves; CMP-006 lists `retire.py` in the derived component map. `Hat-Refs` empty is right: the parent carries MAINTAINER and this design row raises no hat of its own. The rationale says what breaks without each choice (a hand deletion without a record; a re-serialized registry losing every other row's bytes; a walk over every commit) and states the standing system; the form gate is silent on the row once flipped -> ready.
- [RETURN] LLR-287 -> `retired_panel(rows, before)` returns None with no record and otherwise the Retired tab and its table (id, date, successor or a dash, reason, deleting commit inside `<code class="retcommit" data-id>`), every cell escaped, under a caption naming lookup, render-time git and the census count when positive; `_retired_view` builds it from `retire.records` and `retire.read_census` as one-element or empty lists that `build_html` extends after the Process tab; `fresh_view(text, unresolved)` is what `--check` compares, the as-of stamp removed and the retcommit elements of `_unresolved(root)`'s ids emptied, every other commit held exactly -> `SR-Refs` SR-226 HOLDS: the parent's acceptance says the deleting commit is read from history when the record is shown and reads unknown where history cannot answer, and this is the one surface that shows it. Read at HEAD: `traj_views.retired_panel` (the dash, `esc` on every cell, the caption's two sentences, the `earlier` clause only when `before`), `gen_trajectory._retired_view` / the `extra_tabs += tabs` after `process_panel`, `RETCOMMIT_RE` + `fresh_view` + `_unresolved`, and the `--check` branch calling `fresh_view(current, unresolved) != fresh_view(generated, unresolved)`. Four code symbols, both modules, CMP-009 resolve; Detail and Title are clean under the form gate -> NOT ready on ONE cell: `Rationale` reads "a clone with less history, such as a shallow checkout in continuous integration, reads unknown", and "such as" is an open-ended enumeration the kit's form gate refuses on an Approved row (`FINDING (requirement form): LLR LLR-287 Rationale uses 'such as' — the scope cannot be closed, so the row cannot be completed — enumerate it`, gating under `--strict`; measured on the flipped tree). The argument is right and stays; the remedy is to close the set the row itself already knows — the checkouts that read unknown are the ones `records` names: an uncommitted record, a shallow clone, a squashed history — and say so without the escape phrase. Drafted in `## Dispositions` of WI-712's spec.
- [APPROVE] TC-299 -> over a temporary git repository holding the four registries, a watermark with two spent SR ids, a log and its fragment drop-box, drive the command through (a) the deletion writing its record for one commit, (b) eight refusals writing nothing, (c) the real `trunk_step.py --compile-log` leaving the record byte-identical, (d) the census with exclusions, runs and `--replace`, (e) the missing report and every unreadable-record shape, (f) the edited report through edit, commit, restore, removal, an uncommitted record, off git and a depth-one clone, (g) the findings outside both strict exit codes and `trace.py` over a scaffold printing the advisory -> twenty-one evidence pointers in `tests/test_retire.py`, every one resolving by function name and asserting exactly its Method arm (read at HEAD: the `repo` fixture is the Method's opening sentence; `test_each_refusal_writes_nothing`'s seven params plus `test_an_id_already_recorded_is_refused` are the eight refusals; `test_a_record_outside_the_declared_format_is_unreadable`'s seven params are (e)'s shapes, `_FENCED + "\n"`, spaces and a tab included and `test_the_final_newline_alone_is_not_a_body` the exception; `test_a_shallow_clone_says_the_record_is_unverifiable` names the record AND the census; `test_the_reports_never_change_the_exit_code` sets both strict flags). `Verifies` HOLDS: SR-226 (every acceptance clause but the shown-commit one has an arm), LLR-286 (its symbols are what the arms drive), IF-257 (the record and census shapes (e) and (d) hold the reader to) and IF-258 (the command's arm and exit protocol (b) and (d) drive) — both interface rows exist, owned by `scripts/retire`, and citing a seam a case drives is the kit's standing pattern. Expected states the condition, not the instrument; Level Integration true (real git, real `trunk_step.py`); Tier Full honest — `test_retire` is in `tests/conftest.py` `SLOW_MODULES`; Automated Yes; the form gate is silent on the row once flipped. Ran: 33 cases pass -> ready.
- [RETURN] TC-300 -> records read from temporary git repositories, a shallow clone included, and the real generator over the shared fixture project: (a) a landed record reads its landing short hash with its four cells, an uncommitted record, a root-commit record and a depth-one clone read unknown, tier-then-number order; (b) no record no tab whatever the census counts, two escaped rows with retcommit elements, a dash and a lookup caption, the census count stated only when positive; (c) the tab only once a record exists, `--check` failing on a fabricated commit or on unknown where history resolves, passing in a depth-one clone of a page rendered with full history, failing on a changed reason -> twelve evidence pointers in `tests/test_retire_dashboard.py`, each resolving and asserting exactly its arm (read at HEAD: `retired_panel([], 12) is None`; the `<badly>` escape; `<td>—</td>`; "108 ids retired before the record began"; `_rendered_history` committing sources, record and render; both `"0000000"` and `rt.UNKNOWN` forged; the depth-one clone's `--check` returning 0; `"Gone!"` returning 1). `Verifies` HOLDS: SR-226 (the acceptance's last clause), LLR-286 (`records`, arm (a)), LLR-287 (arms (b) and (c)), IF-257 (the record files the readers consume). Expected names the condition; Level Integration true; Tier Full honest — `test_retire_dashboard` is in `SLOW_MODULES`; Automated Yes. Ran: 12 cases pass -> NOT ready on ONE word of ONE cell: `Method` opens "the real generator run over the shared minimal project", and `minimal` is on the kit's vague-term list, which the form gate refuses on an Approved row (`FINDING (requirement form): TC TC-300 Method uses 'minimal' — no test can settle it — name the measurable`, gating under `--strict`; measured on the flipped tree). Here it is not a threshold but a fixture's nickname (`tests/traj_fixtures.make_repo`), which is exactly what the `Parameters` cell exists to carry: name the fixture there, and let Method say "the shared fixture project". Drafted in `## Dispositions` of WI-712's spec.

## How the chain and the anchor were read

- Upward: SR-226 as the brief printed it and as the live file holds it;
  SN-010 (`need`, `why`, `acceptance`) from `stakeholder-needs.toml`; the
  MAINTAINER hat's `applies_when`, `asks` and `listens_for` from `hats.toml`;
  every `B-` crossing from `external.toml`; SR-193 for the coincident test and
  SR-070 for the generator's own crossing set. Sideways: the B-01 rows named
  above, SR-223 and SR-225 (the derived rows ruling 47 left unclassified).
  Downward: all 33 pointers of TC-299 and TC-300 resolved by file and
  function and read; every code symbol of LLR-286 and LLR-287 located and
  read; `trace.py`'s `retired_advisories` wiring located.
- Routed pointer cells, ruled row by row above: SR-226 `SN-Refs` HOLD,
  `Boundary-Refs` B-09 HOLD and B-01 MISSING (part of the return); LLR-286 and
  LLR-287 `SR-Refs` HOLD; TC-299 and TC-300 `Verifies` HOLD.
- The form gate: every row was flipped and the tree driven through
  `trace.py --strict`; LLR-286 and TC-299 raise nothing, LLR-287 and TC-300
  raise the two findings quoted above, and their flips were reverted before
  the act. SR-226, LLR-287 and TC-300 were then scanned cell by cell with the
  gate's own patterns (`_SHALL_RE`, `_MODAL_RE`, `_ACTORLESS_RE`, `_VAGUE_RE`,
  `_ESCAPE_RE`): the three hits named in the verdict lines are the only ones,
  so the disposition below clears the gate in one pass.
- Approving LLR-286 and TC-299 under a returned parent: the parent's three
  findings are form (one `shall`), classification (the waiver) and one
  crossing; none changes the obligation set the children decompose, the
  disposition keeps that set and the children's `SR-Refs`/`Verifies`, and the
  kit already holds LLR-281 and TC-291 approved under Drafted SR-224. The
  chain-completeness claim belongs to the derived `Founded` state, not to a
  child's `Status`.
- Anchor: none of the five rows is `Approved` in the SR, LLR or TC copies at
  e7fe487d, and no approved row of those registries has drifted from its
  copy, so nothing here is a re-attest. The act names the LLR registry
  (LLR-286) and the TC registry (TC-299, with WI-714's TC-296); the SR token
  is dropped, since this act flips nothing there.
- Smoke-tier check: TC-299 and TC-300 are `Full`; both modules are in
  `SLOW_MODULES`, which is consistent. Every rationale and method states the
  standing system: no history, status or citation frame in any of the five.
- Advisories left standing, not findings: `trace.py` reports SR-226 "declares
  no Form" — no SR in the registry declares one; and 13 spent ids with no
  record (SR-222, LLR-266..270, TC-262..265, ...), the reservations WI-620
  still holds, which the census deliberately excluded.

## Bar I produced (not claimed)

On this tree, `python -m pytest -q -n 4 tests/test_retire.py
tests/test_retire_dashboard.py -p no:cacheprovider`: **45 passed in 31.73s**
(33 + 12), no failures, no errors. `python project-trajectory/scripts/trace.py
--root . --strict` at HEAD: rc 0, orphans=0 integrity=0; over the tree with
all five flipped: rc 1, `form-findings=2` (the two quoted above) beside the
expected pre-snapshot approval-record findings; over the tree with LLR-286,
TC-299 and TC-296 flipped: only the pre-snapshot approval-record findings.
`gen_trajectory.py --check`: "project-state dashboard up to date" (rc 0).

## Dispositions

Drafted in `docs/work/queued/WI-712-adjudicate-llr-286-llr-287.md` under
`## Dispositions` (one `toml` block, one lane, since the three rows are one
chain and the same gate): re-author SR-226's `Requirement` to one `shall`
over its one decision, drop its `Coincident` waiver, add B-01 to its
`Boundary-Refs`; close the enumeration in LLR-287's `Rationale`; name
TC-300's fixture in `Parameters` and drop `minimal` from its `Method`; every
status left `Drafted`, then the first-approval adjudication the merge's sweep
mints.

OUTCOME: RETURN rows=5
