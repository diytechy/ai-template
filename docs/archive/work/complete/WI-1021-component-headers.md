+++
id = "WI-1021"
title = "Each code file declares its one component in a Component header, and component membership is read from the headers"
workstream = "process"
sr_refs = ["SR-159", "SR-165", "SR-049"]
specref = ""
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1021`, cut from `refactor_again` at
`1aa6c439a`, with the commit hooks on. The specref (the pointer rules) is
cleared at close, as a terminal row's is. The lane built on its own picks;
the operator ruled the one-component table on 2026-11-21, accepting every
pick, before the review (Done-when 4; Context, "The table, ruled").

- `5e13999ca`: the plan ([plan](../../../plans/WI-1021/plan.md)) and the
  one-component table ([table](../../../plans/WI-1021/component-table.md)).
- `458724024`: the reader, the census, membership read from the headers, the
  advisory retired, the 167 headers, the interface and spine rows, the
  documents, the RESYNC entry, the tests and the regenerated views.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.
- The commit after the close-out, before the review (the coordinator): the
  operator's ruling recorded, and the declaration's batch and PowerShell
  carriers narrowed to Done-when 1's (Deviations).

**The table** (Done-when 4). Each of the 34 files with design rows tagged to
several components, its tags with the rows behind them, the pick and the
reason, with three flags at the top: eight near-even files (the leading
component under two thirds of the tags: `acceptance_record`, `check`,
`gen_open_items`, `census`, `check_doc_refs`, `held_status`, `id_carrier`,
`kitlib/authority`), two files doing two components' work
(`acceptance_record`, `check_doc_refs`), and the picks against the tag
majority (`hooks/pre-commit` CMP-007 by CMP-007's row and IF-134;
`kitlib/config` and `kitlib/git` CMP-006 by the kernel rule). The 22
in-scope files no design row names get a lane pick each, listed there too.
`scripts/dev-setup.sh` and `.ps1` (this repository's copies) are outside the
scope and carry no header.

**The grammar and its one reader** (Done-when 1; LLR-396). In
`gen_arch_map.py`, beside `module_contracts` and `header_lines`:
`file_component(path)` returns `(component, problem)` over a Python module's
docstring (read off its first statement's tokens) or any other file's
`header_lines` over the grammar's own carriers (`_COMPONENT_FORMS`: the
contract header's forms, with a batch file's narrowed to `REM` lines and a
PowerShell script's to `#` lines); `component_declaration` judges the lines: exactly
`Component: CMP-NNN`, else absent, doubled or malformed (a malformed line
voids the file even beside an exact one).

**The scope and the census** (Done-when 1 and 2; LLR-397).
`arch_inputs.component_headers(root)` walks every file under `[paths] src`
of a grammar type (`README.md`, hidden parts and `__pycache__` excluded) and
every non-directory file owner `gen_arch_map.owner_files` reads, and returns
the valid declarations and one finding per file absent, doubled, malformed or
naming no live component row; a file of another type stating a
`Contract IF-NNN:` body is a finding naming its suffix. Vacuous with no live
component row. The findings ride `component_findings`: WARN plain, ERROR
under `--strict`, the `components_check` opt-out.

**Membership reads the headers** (Done-when 3).
`kitlib.spine.module_components(declared)` keys the declarations by
`norm_module`; `arch_components.component_top_view`, `arch_seams` and
`gen_components` (seam placement and each component's `modules`) read it.
Under the Trust ruling an import edge touching an undeclared file is
reported as unclassified before the seams and the kernel are read, and an
edge is internal only inside one component, so a key two files share
(`check.py`, `check.sh`) silences nothing. `derive_stage` reads no
membership (the DevStg-Arch rung reads only the component rows' status and
standing), so it is unchanged; the plan records the reading. No check
compares a design row's `component` cell with a header.

**No new silence** (Done-when 5). The multi-membership advisory is retired
(`cross_component_advisories`, its re-export and its warn-loop line). The
picks make three uncovered crossings, and `gen_components` reading
`arch_inputs` a fourth; each is covered: **IF-326** (new, `Drafted`, `call`,
owner `kitlib/done_when`, requestor `acceptance_record`: the digest width
`_DIGEST_CHARS`, with its `Contract IF-326:` body and TC-461), and the
requestor added to the `Drafted` rows whose `data` already names the call:
`agent_policy` to IF-195, `id_carrier` to IF-194, `gen_components` to IF-316
(whose `data` and body gain `component_headers`). IF-319's `data` drops the
advisory. CMP-006's `notes` are rewritten in header terms.

**Every in-scope file carries its declaration** (Done-when 6): 167 files
(136 Python modules and 18 other files under `[paths] src`, 13 file owners
outside it), written by a scratch script that is not shipped: CMP-006 42,
CMP-007 27, CMP-008 59, CMP-009 39. The census over the live tree reads 167
declared, 0 findings. `docs/kernel-modules-allow` is unchanged.
<!-- fig: cmd="arch_inputs.component_headers(root) over the worktree" rev="458724024" -->

**Documents** (Done-when 7). `PROCESS.md` §8 states once where the header
goes and what an undeclared file means. `PROCESS_OPTIONS.md` "Component
layer" reads software membership from the header, names the unclassified
edge and retires the advisory. `RESYNC_PACK.md` gains "Each file declares
its one component in a `Component:` header, and membership is read from it
[since 1aa6c439a]", the first of variant F's entries.

**Spine rows.** New, `Drafted`, phase 6: LLR-396 and LLR-397 (SR-159,
CMP-006), TC-457 to TC-461, IF-326. `trace.py --root . --bump-ids` moved the
watermark IF 325 -> 326, LLR 395 -> 397, TC 456 -> 461. No status moved, and
`intake.py snapshot` was not run.

**Acts owed** (text-only amendments of `Accepted` rows, drifting for
automated adjudication; and the new rows' first acceptance):

- LLR-373 (the join's input is the declarations), LLR-067 (membership from
  the headers; the unclassified edge; internal only inside one component),
  LLR-199 (the view's modules and seam placement read the headers);
- TC-435 (method, expected and evidence follow the join's input), TC-067
  (method drops the advisory; evidence drops the retired advisory test),
  TC-195 (the modules come from the headers), TC-436 ("tag" becomes
  "declare");
- CMP-006's `notes`;
- first acceptance of LLR-396, LLR-397, TC-457 to TC-461 and IF-326; the
  requestor additions on IF-194, IF-195 and IF-316 and IF-319's `data` are
  on `Drafted` rows and owe none.

Read and left unamended, since no sentence of theirs names the membership
source: LLR-374, LLR-049, LLR-172 (the spec's S5 named them as likely
re-cuts), TC-049.

**Deviations from the plan and the spec.**

- TC-436 is amended, where the plan left it: its "Tag one importer into one
  component" read as a design-row tag.
- The scope walk lives in `arch_inputs` (the census's input home), not in
  `gen_arch_map`, to keep the reader's module's growth to the reader.
- `gen_arch_map.py`'s size-ratchet baseline is re-stamped up, 1599 -> 1655
  SLOC (the reader, where the spec places it), with the reason in the
  ratchet's entry; `check_trajectory.py`'s down, 1659 -> 1657.
- SR-159 now has 9 direct LLR children, over the warn-only fan-out bound of
  7 (`trace.py` advisory, not the exit code); LLR-396 and LLR-397 sit there
  by the spec's `sr_refs`.
- `docs/kernel-modules-allow`'s header comment still mentions the retired
  advisory; Done-when 6 holds the file unchanged, so it is left for a later
  row.
- An empty `__init__.py` under `[paths] src` owes a one-line docstring (the
  scope is every Python file); the RESYNC entry says so.
- Before the review (the coordinator, 2026-11-21): the reader first read
  the declaration through every form `header_lines` reads for the
  `Contracts:` marker, a batch file's `::` lines and a PowerShell `<# #>`
  help block included: looser than Done-when 1, which names a `REM` line
  and a `#` line, and, for `::`, than LLR-396. It now reads only those two;
  LLR-396 and TC-457 (both `Drafted`) follow, and `gen_arch_map.py`'s size
  baseline moves 1655 -> 1657, a reviewed bump with its reason in the
  ratchet's entry. Every written header already used those lines, so the
  census still reads 167 declared, 0 findings.
- Done-when 3 names the DevStg-Arch derivation among membership's readers;
  `derive_stage` reads none (the DevStg-Arch rung reads only the component
  rows' status and standing), so the clause is met with no change to it, as
  the plan records.

**Tests.** Red before the code: `tests/test_component_headers.py`, `37
failed in 1.46s` as first written (each carrier, each finding class, the
scope, vacuity, the unclassified edge, membership from headers), then
restructured into loops to spare the smoke tier, `14 failed in 0.58s`;
green, `14 passed in 0.83s`.
<!-- fig: cmd="python -m pytest tests/test_component_headers.py -q" rev="the worktree before the code, then after it" -->

- Red before the code: `tests/test_component_headers.py` as first
  written, `37 failed in 1.46s` (each carrier, each finding class, the scope,
  vacuity, the unclassified edge, membership from headers); folded into loops
  to spare the smoke tier's membership, `14 failed in 0.58s`; green with the
  code, `14 passed in 0.83s`.
  <!-- fig: cmd="python -m pytest tests/test_component_headers.py -q" rev="the worktree before the code, then after it, ahead of 458724024" -->
- The modules whose fixtures moved from design-row tags to headers, each
  green after its edit: `test_trajectory_arch` `169 passed in 16.31s` (six
  advisory tests retired, the unmapped-endpoint test inverted to the
  unclassified edge); `test_gen_components`, `test_components_registry` and
  `test_component_headers` `44 passed in 18.38s`; `test_seam_import_forms`
  `18 passed in 0.68s`; `test_traj_views` `64 passed in 45.93s`.
  <!-- fig: cmd="python -m pytest -q -n auto <each module listed>" rev="the worktree ahead of 458724024" -->
- The full unfiltered suite, every module importing a changed module among
  them: `2 failed, 8268 passed, 31 skipped, 18 warnings in 5206.14s
  (1:26:46)`. The two: `test_generated_newlines`' pinned line in
  `gen_open_items.py` moved with its header (1670 -> 1672, the pin and its
  chain updated), and `test_derive_stage`'s committed stage was stale after a
  later registry edit (regenerated). Those two modules again: `41 passed in
  17.83s`. After the suite, `gen_components._add_members` was decomposed
  (the complexity ratchet) and the stale complexity row dropped:
  `test_gen_components`, `test_complexity_ratchet` and
  `test_module_size_ratchet` `21 passed in 3.93s`.
  <!-- fig: cmd="python -m pytest -q -n auto" rev="the worktree ahead of 458724024" -->
- `run_menu.py smoke` over the committed build tree: `trace.py --strict`
  `orphans=0 integrity=0`, `component-findings=0 interfaces=270
  interface-findings=0`; `check_trajectory.py --strict` clean;
  `check_resync: OK, 155 shipped path(s) changed`; the tier `3713 passed, 3
  skipped, 18 warnings in 83.29s (0:01:23)`, under `max-tests = 3720`.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="458724024 (its tree before the commit)" -->
- The commit hook over `458724024`: `RESULT: PASS`. Its readability step
  WARNs that the flag-axis reading of several touched modules is above
  `docs/flag-axis-baseline`; their readings equal their readings at
  `5e13999ca` (`adjudicate_act.py` 0 functions, 1 site; `session_keep.py` 1
  and 8; `gen_arch_map.py` 0 and 6), so the baseline was stale before this
  row touched them (report-only).
- Before the review: the outside-the-carrier test gains a PowerShell help
  block and a batch `::` line (the help block left the carrier list), `1
  failed, 12 passed in 6.97s` on the old reader, whose `::` case read
  `CMP-001` too; with the narrowed carriers, every test module importing
  `gen_arch_map` plus `test_import_layers` and `test_dogfood_sync`, `667
  passed, 1 skipped in 215.22s (0:03:35)`; `trace.py --strict` `orphans=0
  integrity=0`, `component-findings=0`.
  <!-- fig: cmd="python -m pytest -q -n auto <each module listed>" rev="the worktree after fa057410d, before the review" -->

**Byte deltas.** `PROCESS.md` 101,623 -> 101,950 (+327, watched);
`PROCESS_OPTIONS.md` 202,180 -> 202,304 (+124, watched); the byte-budget
skill 4,742 -> 4,631 (cap 5,000; its two watched rows re-stamped, three
copies); `RESYNC_PACK.md` 734,651 -> 737,613 (unbudgeted).

## Context

Variant F's first row (F-1), filed on trunk on 2026-11-21 after the operator
chose to build F before WI-1015 (queue-drill HANDOFF §3.1 Q1 (a), §3.3).
F point 1, ruled in revision 35: component membership has one home, the
realization. A code file declares its component in its header; the LLR's
`component` cell stops being the membership source (it leaves the schema in
WI-1023).

Today no file declares a component. Membership is derived by
`kitlib.spine.module_components` (LLR-373, "the join's one home", WI-1005):
a file belongs to every component its LLRs' `component` cells name. 34 files
carry LLRs tagged to more than one component, so the cross-component rule
(LLR-067) treats their edges as multi-membership advisories. That is
WI-1015's loophole 2, which this row dissolves (WI-1015 is restructured into
F's rows; HANDOFF §3.3 N1).

**One component per file (operator, 2026-11-21, §3.3 N3).** A file is
ascribed to one component. Reuse keeps one owner: the eight files on
`docs/kernel-modules-allow` are owned by CMP-006 and imported across
components without a seam (OI-48). Configuration keeps one owner: other
components read it through a `file` interface. Most of the 34 have a clear
majority (`trace.py` 25 to 1, `integrate.py` 17 to 1); a minority LLR is
placed later through the interface it constrains (WI-1024), not by the
file. The real calls are the near-even splits: `check.py` (9/4/1),
`acceptance_record.py` (8/5/1) and the files at 1 to 1 (`check_doc_refs.py`,
`census.py`, `held_status.py`, `kitlib/authority.py`, `id_carrier.py`). A
file doing two components' work is evidence about the partition (OI-14); it
is flagged and filed as its own row, never split here.

**The table, ruled (operator, 2026-11-21, queue-drill HANDOFF §3.5).** Every
pick in `docs/plans/WI-1021/component-table.md` stands as proposed: the
eight near-even files (R1); the three picks against the tag majority,
`hooks/pre-commit` CMP-007 and `kitlib/config` and `kitlib/git` CMP-006 by
the kernel rule (R3); and the 22 in-scope files no design row names (R4).
Of the two files doing two components' work (R2), `acceptance_record.py`
keeps CMP-006 and WI-1045 is filed on trunk to move its CMP-008 landing
rules into a CMP-008 module behind an interface; `check_doc_refs.py` keeps
CMP-007 and gets no row until WI-1023 lands, since its symbol-binding
oracle's spine role retires there.

**Where the header goes (F point 1, revision 16).** In the same header that
holds the file's `Contracts:` marker, by the file's comment syntax (Done-when
1). Not built here: the inventory-entry form for a file type with no comment
syntax; no file in this row's scope lacks one, so it is filed when an
adopter needs it.

**The component registry's prose.** CMP-006's `notes` describe membership by
LLR tags and the multi-membership advisories this row retires; this row
rewrites those sentences. Removing the file names component rows still carry
is WI-1028's (no code in row text).

**Downstream.** Adopters gain the header grammar. This row writes its own
RESYNC entry, the first of variant F's (each F row writes its own entry,
apply in landing order; the operator: re-sync need not be one entry). Items
4 and 10 of the review-churn plan are not bundled with F.

## Scope answers

- **S1.** One deliverable: the header grammar, its reader and check, the
  headers written, and membership switched to them. They land together:
  headers without the switch are a second home, and the switch without
  headers empties every component.
- **S2.** The headers become the membership input to strict checks and the
  DevStg-Arch derivation, so a `## Trust` section follows.
- **S3.** The grammar, its carriers and the scope are closed (Done-when 1
  and 2); anything else is a finding or outside the rule, as stated there.
- **S4.** `single`: several script families (`kitlib/spine.py`,
  `arch_components.py`, `arch_seams.py`, `gen_components.py`,
  `derive_stage.py`, `gen_arch_map.py`) and a grammar over file headers.
- **S5.** No state, domain value or boundary is added; membership changes
  its input. Re-cut LLRs (text only, drifting): LLR-373 (the join), LLR-067
  and LLR-374 (the cross-component rule and its import resolution), LLR-199
  and LLR-049 (the component views), LLR-172 (the derivation record); the
  lane's plan completes the list from the code. The ruled table may move
  edges across a boundary; each is covered (Done-when 5).
- **S6.** `needs` is empty: nothing this row reads is unbuilt. No new
  package, tool or service.
- **B4.** The one-component table is the operator's ruling (Done-when 4).

## Trust

The header becomes the authority on a file's component, which strict checks
and the stage derivation read (PROCESS.md §3, "When a guard is owed").

- **Producer.** A person or model editing the file in a lane (the supported
  route), and this row's migration. No script writes a header.
- **Failed write.** A header left absent, doubled, malformed or naming no
  live CMP row. Each is a finding (Done-when 1); no kit route half-writes a
  header.
- **Consumers.** The one header reader (beside
  `gen_arch_map.module_contracts`), read by the membership home in
  `kitlib/spine.py`, `arch_components.py`, `arch_seams.py`,
  `gen_components.py` and `derive_stage.py`.
- **Ruling, shared by every consumer.** A file whose declaration is absent
  or invalid belongs to no component: it is reported, and every import edge
  touching it is reported as unclassified, never treated as internal or
  exempt.

## Done-when

- [ ] **Grammar.** A declaration is one line reading exactly
      `Component: CMP-NNN` (digits as the id space spells them), placed by
      file type: a Python module docstring; a `#` line in the top-of-file
      comment block for `.sh`, `.command`, `.ps1`, `.toml`, `.ini`, `.csv`
      and files with no suffix (the hooks, `docs/agents-enabled`); a `REM`
      line in the top-of-file comment block for `.cmd`; a line inside the
      opening `<!-- ... -->` comment of a `.md` file (`docs/runtime-flows.md`,
      `docs/status.md`). One reader, beside the existing `Contracts:` header
      reader, returns each in-scope file's component. A file with no
      declaration, two declarations, a malformed one or an id no live CMP
      row has is a finding; warn-first, failing `--strict` from DevStg-Arch
      upward, like the cross-component rule it feeds.
- [ ] **Scope, closed.** Every file under `[paths] src` of a type the
      grammar lists (`README.md` excluded as documentation), and every file
      the contract scan reads as a file owner today
      (`arch_interfaces._owner_files`: 13 non-directory paths, the hooks,
      configuration files and registries among them). A file of another
      type under `[paths] src` is outside the rule unless it states a
      `Contract IF-NNN:` body, which is then a finding naming its type. A
      file outside the scope may carry a declaration, judged by the same
      grammar.
- [ ] **Membership reads the headers.** `kitlib.spine.module_components`'s
      callers (`arch_components`, `arch_seams`, `gen_components`) and the
      DevStg-Arch derivation read file membership from the one header
      reader, under the Trust ruling. No check compares an LLR's
      `component` cell with a header. The LLRs in S5 are amended to the
      header source (Accepted: text only, drifting for adjudication).
- [ ] **The table, ruled by the operator.** The lane's plan lists each of
      the 34 files with LLRs tagged to several components: its candidate
      components with LLR counts, the pick and its reason, and a flag where
      the file does two components' work. The lane commits the table and
      stops; the coordinator puts it to the operator. The reader and the
      headers for every other file may be built meanwhile. The lane goes
      to review only once the ruling is recorded in this spec's Context.
      Each flagged file keeps the ruled header and gets a queued row filed
      on trunk.
- [ ] **No new silence.** Every import edge the ruled headers turn into a
      crossing is covered by an existing interface row naming both files,
      shown inside one component, or covered by a new `Drafted` `call` row
      from the lane's id range. The multi-membership advisory retires, and
      CMP-006's `notes` stop describing it (drifting for adjudication).
      `trace.py --strict` and `check_trajectory --strict` are clean.
- [ ] Every in-scope file carries its declaration; the kernel allowlist is
      unchanged.
- [ ] A RESYNC entry tells adopters the grammar, that headers are owed from
      DevStg-Arch upward, and that it is the first of variant F's entries.
      PROCESS.md §8 states where the header goes, once.
- [ ] Tests: red-before for each finding class, each carrier syntax, the
      Trust ruling (an unclassified edge) and membership from headers;
      every test module importing a changed module runs green.
