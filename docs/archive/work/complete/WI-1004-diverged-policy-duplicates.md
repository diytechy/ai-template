+++
id = "WI-1004"
title = "The policy duplicates the OI-130 re-score found disagreeing each get one home, with the disputed inputs pinned"
workstream = "process"
sr_refs = ["SR-147", "SR-157", "SR-189", "SR-220", "SR-166", "SR-156", "SR-146", "SR-158"]
specref = ""
buildtier = "strong"
safety_class = "ordinary"
priority = 4
planmode = "single"
+++

## Deliverable

Ten of the eleven behaviours now have one home, which every former copy
calls; the copies are deleted. The eleventh, rolling review §13.14, is not a
disagreeing duplicate on today's tree and left scope at the dispositions (its
entry below). Built on the maintenance branch `maint/wi-1004` from
`426f88f60`, one commit per behaviour in the spec's order, each with its
pinning tests, rows and RESYNC entry. The spec of record is "One home per
behaviour" in
[`docs/plans/2026-11-11-oi130-rescore/README.md`](../../../plans/2026-11-11-oi130-rescore/README.md).
The row's SpecRef cell was cleared at close, as R-F asks of a terminal row.

| # | Behaviour | Home | Copies deleted | Kept answer on each disputed input | Test (TC) | Commit |
|---|---|---|---|---|---|---|
| 1 | B3 value to cell | `kitlib.spine.value_to_cell` | `migrate_carrier.value_to_cell`, `spine_carrier.value_to_cell` | `None`: the empty cell | `test_rule_sync.py::test_the_carrier_value_cell_has_one_home_and_reads_none_as_empty` (TC-438) | `47438070f` |
| 2 | B12 module key | `kitlib.spine.norm_module` | `migrate_carrier._short_module` | `pkg/__init__.py`: `pkg`; `hooks/x.sh`: `hooks/x` | `test_policy_one_home.py` (TC-439) | `956377922` |
| 3 | Id number | `kitlib.spine.id_number` | `kitlib.decisions._id_number`, `kitlib.registry.spec_id_number`, `wi_convert._id_number` | `X2-5`: 5; `WI-12a`: 0 (digits after the last dash) | `test_policy_one_home.py` (TC-440) | `24e9ae0d7` |
| 4 | B5 SN-id universe | `kitlib.spine.sn_all_ids` | the whole-file scrapes in `check_docs._registry_needs` and `check_flows.load_ids` | an id only in a TOML comment or stakeholder description: no need; `SN-000`: excluded | `test_policy_one_home.py`, `test_rule_sync.py` (TC-441) | `0aabe35c0` |
| 5 | B10 ref split | `kitlib.spine.refs`, `split_pred_edges` | the `;`-only splits in `consolidate` (five), `adjudicate_brief._cited_spine` (two), `intake._owning_srs`; `agent_common._refs`'s body | `,`- or space-separated cell: its ids; `OI-5x`: no open-item edge | `test_policy_one_home.py` (TC-442) | `35336c150` |
| 6 | B8b spec parse | `kitlib.registry.parse_spec_row` | `wi_convert`'s `split_spec`, `parse_deliverable`, `status_from_location`, `_scalar`, `_text` | `title = 5` (any non-text value but an integer `priority`): refused; id the filename does not carry: refused; `adjudicates = ["a;b"]` or `"a"`: refused; `["a;b"]` in any other list key: refused | `test_policy_one_home.py` (TC-443) | `eab83e5cd`, review fix below |
| 7 | Queued-spec lookup | `kitlib.registry.queued_spec` | `handback._queued_spec`, `consolidate._archive_plan`'s glob, `integrate._queued_spec`'s glob | two queued specs of one id: refused (none: refused, in each caller's words) | `test_policy_one_home.py` (TC-444) | `07fc4f676` |
| 8 | §13.13 spec precedence | `kitlib.registry.governing_spec` | `agent_policy._spec_home_rank` (and `agent_common`'s re-export), `done_when._copy_at`'s folder-index choice | archive and legacy `docs/work` copy: the archive's; active beside closed: the closed; two terminal copies, or two in one folder: the first by path | `test_policy_one_home.py` (TC-445) | `4a4e66432` |
| 9 | §13.22 command tokenizer | `kitlib.config.split_cmd` (moved from `agent_session`, which imports it) | `check._split_template` | unquoted `#`: a word; JSON array: its elements | `test_policy_one_home.py` (TC-446) | `c81c86f14` |
| 10 | §13.16 declared-file grammar | `kitlib.config.declared_entries`, `declared_absences` | the walks in `check_need_form.read_need_form_allow`, `trace.read_provenance_allow`, `trace._declared_absences`, `trajectory_arch._parse_kernel_allow`, `check_doc_refs.read_declared_absences` | byte-order mark: stripped; undecodable byte: replaced; `path - reason` and `path—reason`: unparsed (the spaced em dash only); `dir/`: `dir` | `test_policy_one_home.py` (TC-447) | `4e0bcf9e0` |
| 11 | §13.14 freshness arm | none: out of scope | none | the four arms agree on every verdict; the missing-output postures are deliberate per generator, and the STALE line's stream decides nothing | none | `b09b33fed` |

**What an adopter sees change** (each named in its RESYNC entry, all anchored
`[since 426f88f60]`):

- `check_docs`' README inventory and `check_flows` fail a citation of an SN
  id that exists only in a TOML comment or a stakeholder description (B5).
- `check_trajectory` names a spec whose front matter holds a non-text value
  (`title = 5`), or a list element carrying `;` (`sr_refs = ["SR-1;SR-2"]`),
  as malformed, and the scheduler skips it; `wi_convert --to-csv` refuses
  those, a spec whose filename does not carry its id, and an `adjudicates`
  value the registry refuses (B8b).
- Handback's edge and return writes and the consolidation close refuse, and
  write nothing, on two queued specs of one id (queued-spec lookup).
- `check.py` runs a `stack.ini` step command carrying a bare `#` whole, and a
  JSON-array command as its elements (§13.22).
- A hyphen-separated or unspaced line in `docs/declared-absences` is reported
  unparsed and declares nothing; a BOM'd file's first entry counts (§13.16).
- `migrate_carrier --if-shape` folds an owner on `__init__.py` or a non-`.py`
  module to its normalized key (B12); malformed ids sort differently (id
  number); `consolidate`, `adjudicate_brief` and `intake` widen three
  advisory signals (B10). B3 and §13.13 change no output on any input a kit
  route writes.

**Dispositions and plan.** `b09b33fed`: the critique's two BLOCKERs and
three MAJORs adopted (S1 by the operator's 2026-11-19 ruling: one row, walked
in series), with copies, home, SR and kept answer per input stated before any
code, and a Trust and an architectural-delta section. `40a74a817`: the plan.

**The two vacuous pins** are repaired: the `value_to_cell` pin has the `None`
case (TC-438), and the `need_ids` pin reads the live TOML needs file (TC-441).
**B10's Done-when:** `consolidate._commissioning_docs` returns exactly
`split_pred_edges`' open-item edges over a nine-cell battery (TC-442).
**`[dupes-census]`** reads 2/2/32 before and after: every deleted copy had a
body unlike its home's, which the census does not count, so no re-stamp.

**At review** (Sol): a list element carrying `;` was refused only for
`adjudicates` and flattened into two references for every other list key.
The stricter answer now holds for every list key the parse reads
(`kitlib.registry.spec_list_element`), pinned per key by
`test_a_list_element_carrying_the_cell_join_is_refused`; no spec on the tree
wrote one.

**Rows.** New and Drafted: LLR-382 to LLR-388 and TC-438 to TC-447.
Traced cells changed on Accepted rows: LLR-197 `test_refs` gains TC-439,
LLR-215 gains `test_refs` TC-441, LLR-210 `test_refs` gains TC-442, LLR-163
`code_symbol` drops `split_cmd`. Drafted interface rows IF-112 and IF-072
have their notes corrected. Module sizes re-stamped down: `agent_common.py`
1093 to 1090, `integrate.py` 1795 to 1793, `check.py` 1344 to 1339,
`trace.py` 3854 to 3836, `trajectory_arch.py` 1128 to 1117. The complexity
baseline drops `wi_convert.parse_spec`'s row.

## Context

Filed by hand on 2026-11-15 (attended, at the owner's request) from the OI-130
re-score record's "One home per behaviour" section, the second of the three
rows the 2026-11-11a handoff left unfiled (its owner item 3). Its scope
critique is owed before a claim.

WI-448's consolidation stopped short: 19 policy behaviours still have more
than one independent home, and 11 of them disagree on some input. This row
takes those 11. The 8 that agree, and the 18 plumbing duplicates, stay out
unless the critique folds them in. `PROCESS.md` §3's 0→A→B rule applies:
extract the shared stage and delete the copies.

The 11, as the record lists them:

- **B3 `value_to_cell`:** `None` becomes `''` in `migrate_carrier` and
  `'None'` in `spine_carrier`. The pin has no `None` case.
- **B5 SN-id universe:** on a TOML needs file, `check_docs` and `check_flows`
  scrape ids from comments and descriptions, and `check_flows` also counts
  SN-000. The `need_ids` pin returns early on TOML, so it checks nothing.
- **B8b spec parse:** `wi_convert.parse_spec` and
  `kitlib.registry.parse_spec_row` disagree on `title = 5`, on an id that does
  not match its filename, and on `["a;b"]`.
- **B10 ref split:** `adjudicate_brief`, `consolidate` and `intake` split on
  `;` only, so `consolidate.py:451` misses OI edges `split_pred_edges` finds.
- **B12 module key:** `migrate_carrier._short_module` differs from
  `kitlib.spine.norm_module` on `__init__.py` and on non-`.py` paths.
- **Queued-spec lookup:** given two matching specs, `handback` takes the
  first, `integrate` refuses, and `consolidate` takes the first.
- **Id number from an id:** `kitlib.spine` and `kitlib.decisions` take the
  digits after the last dash; `wi_convert` and `kitlib.registry` take the
  first run of digits.
- **Rolling review §13.13, §13.14, §13.16 and §13.22** (unmerged
  `origin/rolling_review`, `04488d5cd`): spec precedence, the generator
  freshness arm, the declared-file grammar and the command tokenizer.

No SR is named here: each behaviour sits under its own requirement. The
critique attaches them, and splits this row per behaviour if one row is too
large to review.

**Operator ruling, 2026-11-19, on the critique's S1:** the row stays ONE work
item, walked in series ("It could still be walked in series as a single work
item, but agreed if it's separate behavior it can be broken up"). Each
behaviour below lands as its own commit, in the order given, with its pinning
test, so any one of them can be split out later without re-deciding the rest.

## Critique dispositions

Scope critique round 1, `docs/reviews/2026-11-19-scope-critiques/WI-1004.md`.

- **S1 (BLOCKER), eleven landable consolidations bundled with no order:
  adopted, by the operator's ruling above.** One row, walked in series. "The
  eleven, in landing order" below fixes the order; each behaviour is one
  commit carrying its test, so the row splits along those commits if a later
  reader wants it split.
- **S3 (BLOCKER), the kept answer on each disputed input undecided:
  adopted.** Each behaviour below names its copies, every input on which they
  disagree on today's tree, the answer kept on each, and one sentence of
  reason. The rule used to choose: the answer correct for inputs a supported
  route produces; then the one an accepted test already pins; then the
  stricter. A strict check is never loosened.
- **S5 (MAJOR), no architectural delta: adopted.** See "Architectural
  delta": every home sits in the shared kernel the seam check exempts
  (`docs/kernel-modules-allow`), so no component boundary moves and no
  interface row is added; IF-112's and IF-072's notes are corrected where
  they describe a copy this row deletes. The component view regenerates for
  the new design rows, and that is in the Done-when.
- **S2 (MAJOR), authority over holds, acts and gates unstated: adopted.** See
  "Trust": per behaviour, whether a hold, act or gate reads a different answer
  afterwards, and on which inputs. Every change in what a gate refuses is a
  tightening, and each is named.
- **B1 (MAJOR), requirement linkage and the four review items unenumerated:
  adopted.** `sr_refs` now names each behaviour's requirement, found through
  the design row that binds the home or the copy where the disagreement acts.
  The four rolling-review items are stated below in full (copies, inputs,
  kept answers), read from `04488d5cd`, so the row no longer depends on the
  unmerged branch (the critic's S6 anchor). One of the four, §13.14, is not a
  disagreeing duplicate on today's tree and leaves scope, with the reason.

## The eleven, in landing order

Each entry: the copies on today's tree (trunk `426f88f60`), the one home,
the requirement, the inputs on which the copies disagree, and the kept answer
on each. "Adopter-visible" names what a shipped script's output changes.

### 1. B3 `value_to_cell` (SR-147, via LLR-165 and LLR-166)

- **Copies:** `migrate_carrier.value_to_cell(col, value)` (the migration's
  round-trip self-check, `compare`) and `spine_carrier.value_to_cell(value)`
  (the TOML reader every consumer goes through, `rows_from_toml`).
- **Home:** `kitlib.spine.value_to_cell(value)`, a cell rule beside
  `refs`; both callers already import `kitlib.spine`.
- **`None`:** `''` against `'None'`. **Kept: `''`.** TOML has no null, so the
  reader never meets `None`; the only route that produces it is the
  migration reading an absent key, and every consumer reads an absent cell as
  empty.
- **Adopter-visible:** none: each caller's output on the inputs it receives is
  unchanged.

### 2. B12 module key (SR-157, via LLR-197)

- **Copies:** `kitlib.spine.norm_module` and `migrate_carrier._short_module`
  (the IF-row shape migration folding an id-typed owner through its LLR's one
  module).
- **Home:** `kitlib.spine.norm_module`.
- **`pkg/__init__.py`:** `pkg` against `pkg/__init__`. **Kept: `pkg`.**
- **A non-`.py` source path (`hooks/x.sh`):** `hooks/x` against `hooks/x.sh`.
  **Kept: `hooks/x`.** For both: the endpoint check compares an IF owner
  through `norm_module`, so an owner folded by the other rule names no module
  the check resolves.
- **Adopter-visible:** `migrate_carrier`'s IF-shape migration writes the
  normalized owner for those two inputs. RESYNC entry.

### 3. Id number from an id (SR-157, via LLR-197)

- **Copies:** `kitlib.spine._id_number` and `kitlib.decisions._id_number`
  (digits after the last dash, 0 otherwise); `kitlib.registry.spec_id_number`
  and `wi_convert._id_number` (first run of digits).
- **Home:** `kitlib.spine.id_number`, public.
- **`X2-5`:** 5 against 2. **`WI-12a`:** 0 against 12. **Kept: digits after
  the last dash, 0 when that tail is not all digits.** Every id a supported
  route mints (`WI-###`, `OI-###`, `D-###`) reads the same either way; the
  open-item coverage rule in `kitlib.spine` matches covered numbers through
  this answer, and the first-digit-run answer would read `OI-35abc` as OI-35.
- **Adopter-visible:** only the order a malformed id sorts in
  (`read_spec_rows`, `wi_convert --to-csv`); no supported route produces one.

### 4. B5 SN-id universe (SR-189, via LLR-215)

- **Copies:** `kitlib.spine.sn_all_ids(text, carrier)` (the need tables only
  under TOML, `-000` excluded), and two whole-file scrapes: the existence
  half of `check_docs._registry_needs` and `check_flows.load_ids`' SN set.
- **Home:** `kitlib.spine.sn_all_ids`, the carrier taken from the file's
  suffix.
- **An SN id written only in a TOML comment or a stakeholder description:**
  the copies count it as a need; the home does not. **Kept: not a need** (the
  rule SR-189 states: the needs file's stakeholder list names needs without
  being one, and trace.py's gate derivation already reads the home).
- **`SN-000`:** `check_flows` counts it; the home does not. **Kept:
  excluded.** `check_flows` skips a cited `-000` id before the lookup, so the
  answer reached no finding.
- **Adopter-visible:** a README or a runtime-flows section citing an id that
  exists only in a comment or a stakeholder description now fails
  `check_docs`' inventory and `check_flows` (a tightening). On this repo's
  registry the three readings are equal. RESYNC entry.
- **The vacuous pin is repaired:** the `need_ids` agreement test runs on the
  TOML needs file.

### 5. B10 ref split (SR-220, via LLR-210; home under LLR-197)

- **Copies:** `kitlib.spine.refs` (`;`, `,` or whitespace) and
  `split_pred_edges` over it, `agent_common._refs` (an agreeing copy of the
  same body), and the `;`-only splits of a ref cell in
  `adjudicate_brief._cited_spine` (a work item's and an LLR's `SR-Refs`),
  `consolidate` (`_superseded`'s `Supersedes`, `_commissioning_docs`'
  `Predecessors`, and the `SR-Refs` reads in the module signal,
  `_llr_modules` and `_model`) and `intake._owning_srs`.
- **Home:** `kitlib.spine.refs`; `split_pred_edges` for a `Predecessors`
  cell's open-item edges.
- **A ref cell separated by `,` or whitespace (`SR-1, SR-2`, `WI-1 OI-5`):**
  the copies read one token that names nothing; the home reads two ids.
  **Kept: two ids**, the reading the scheduler, the validator and the
  dashboard already take of the same cell.
- **`OI-5x` in `Predecessors`:** `consolidate` counts an open-item edge
  (`startswith("OI-")`); `split_pred_edges` reads a hard work-item token.
  **Kept: not an open-item edge**, the scheduler's reading.
- **Out of B10:** `;`-joined list cells whose entries may hold a space or a
  comma (`Adjudicates` tokens, `Module` paths, interface endpoints, a verdict
  line's counters) keep their `;`-only read; that is a different grammar, not
  a ref split.
- **Adopter-visible:** the consolidation clusters, the adjudication brief's
  spine context and intake's owning-SR hint read hand-written `,`- or
  space-separated cells as ids. All three are advisory. RESYNC entry.

### 6. B8b spec parse (SR-166, via LLR-181; the copy under SR-129, LLR-136)

- **Copies:** `kitlib.registry.parse_spec_row` (every registry reader) and
  `wi_convert.parse_spec` (the converter's own fence split, body parse,
  status lookup and scalar rules).
- **Home:** `kitlib.registry.parse_spec_row`. `wi_convert.parse_spec` keeps
  only what is the converter's: it refuses an `active/` claim (a conversion is
  a drained-stop operation), then calls the home and re-raises its refusal as
  a `ConvertError`.
- **`title = 5`, and any non-string scalar or list element** (`priority`
  excepted, which may be an integer): the home wrote `'5'`; the converter
  refused. **Kept: refused.** No supported route writes one, no spec on this
  tree carries one (measured over `docs/work` and `docs/archive/work`), and it
  is the stricter answer.
- **An id the filename does not carry:** the home refused; the converter
  accepted. **Kept: refused** (the stricter; the id has two homes, compared).
- **`adjudicates = ["a;b"]`, or `adjudicates = "a"`:** the home refused
  (`adjudicates_tokens`, the one parser of that value); the converter joined
  it. **Kept: refused.**
- **`["a;b"]` in any other list key (`sr_refs`, `needs`, `adopted`,
  `authoring_tags`, a list-form `supersedes`)**, a disagreement with the
  `adjudicates` rule inside the home itself: both parses joined the element
  into the cell, so one element read downstream as two references. **Kept:
  refused, for every list key** (added at review): it is the answer
  `adjudicates` already had, the stricter, and no spec on this tree writes one
  (measured over `docs/work` and `docs/archive/work`). A bare-string
  `supersedes = "WI-1;WI-2"` is unchanged: it is the converter's own written
  form of a several-id cell.
- **A bare string in a list key (`sr_refs = "SR-1"`)**: both read it
  character by character; they agree, so it is not this row's (reported as
  found).
- **Adopter-visible:** `check_trajectory` names a spec carrying a non-string
  title as malformed, and the scheduler skips it, where it read `'5'`;
  `wi_convert --to-csv` refuses a spec whose filename does not carry its id,
  or whose `adjudicates` value the registry refuses; and both refuse a list
  element carrying `;`. RESYNC entry.

### 7. Queued-spec lookup (SR-156, via LLR-151; SR-220, via LLR-312 and LLR-210)

- **Copies:** `integrate._queued_spec` (claim, the Done-when notice),
  `handback._queued_spec` (the edge and return writes), and the inline glob in
  `consolidate._archive_plan` (the consolidation close).
- **Home:** `kitlib.registry.queued_spec(work_dir, wi_id)`: the one queued
  spec of the id, or a `ValueError` naming how many matched.
- **Two queued specs carrying one id:** `integrate` refused; `handback` and
  `consolidate` acted on the first. **Kept: refused.** Each caller writes or
  moves the file; acting on one copy leaves the other standing as a live
  queued row of the same id, and the claim already refused.
- **None:** all three refuse today; each keeps its own wording.
- **Adopter-visible:** handback's edge and return writes and the consolidation
  close refuse, writing nothing, on a tree carrying two queued specs of one
  id. RESYNC entry.

### 8. Rolling review §13.13: spec precedence (SR-156, via LLR-307)

- **Copies:** `agent_policy.authoritative_spec` (sorts the candidates by home,
  `docs/archive/work` before `docs/work`, then by path; read by the merge
  slot's verdict-owed check, the worker brief and `review_brief`), and
  `kitlib.done_when._copy_at` as `spec_at` drives it (the copy in the last of
  `active/<branch>`, `archive/complete`, `work/complete`, `archive/partial`,
  `work/partial`, `archive/cancelled`, `work/cancelled`; read by the Done-when
  hold, the adjudication brief, `review_brief`, `review_set` and the plan
  pass). `review_brief` reads one spec through both.
- **Home:** `kitlib.registry.governing_spec(paths)`, one precedence key:
  a copy in a terminal folder before an active one before any other, then
  `docs/archive/work` before `docs/work`, then the path.
  `authoritative_spec` binds it; `_copy_at` chooses among its hits with it.
- **The same id under `docs/archive/work/complete` and
  `docs/work/complete`:** archive against work. **Kept: archive.**
  `spec_move` closes into the archive; `docs/work/<state>` is the legacy home
  (TC-325's own wording).
- **An active copy beside a closed copy under `docs/work`:** the alphabetical
  tie-break picked the active copy; `spec_at` the closed one. **Kept: the
  closed copy**, which is `authoritative_spec`'s stated reason ("the branch
  has moved the spec to its terminal folder and filled it") and the case its
  accepted test pins.
- **Two terminal copies (`complete` and `partial`), or two copies in one
  folder:** path order against the later folder or path. **Kept: path order
  (the first).** No route writes either; the answer a reader can predict from
  the paths alone.
- **Not a copy:** `adoption_record._spec_at` refuses when more than one spec
  carries the id. It is a strict check and stays as it is.
- **Adopter-visible:** none on a tree a kit route wrote. RESYNC entry (the
  helper moves into `kitlib.registry`).

### 9. Rolling review §13.22: the command tokenizer (SR-146, via LLR-163; the copy under SR-006, LLR-006)

- **Copies:** `agent_session.split_cmd` (agent `CmdTemplate`s and the
  product test command) and `check._split_template` (every `docs/stack.ini`
  step command `check.py` runs).
- **Home:** `kitlib.config.split_cmd`, moved from `agent_session` (which
  binds it under its name); `check.py` must stay runnable on `kitlib` alone,
  so the home cannot stay in `agent_session`.
- **An unquoted `#` token:** `check.py` dropped it and every token after it
  (shlex's default comment character); `split_cmd` keeps them. **Kept: kept.**
  `configparser` takes a `stack.ini` value whole (no inline comments), so
  `check.py` ran a shorter command than the one declared and than the one the
  loop runs.
- **A JSON-array template:** `check.py` split the text as shell words;
  `split_cmd` reads the array. **Kept: the array**, which no supported
  `stack.ini` value is.
- **Adopter-visible:** a `stack.ini` step command carrying a bare `#` now runs
  whole under `check.py`. RESYNC entry.

### 10. Rolling review §13.16: the declared-file grammar (SR-158, via LLR-038)

- **Copies:** five line walks over `<key> — <reason>` files, each reading
  blank and `#` lines as nothing and a line with no separator as unparsed:
  `check_need_form.read_need_form_allow`, `trace.read_provenance_allow`,
  `trajectory_arch._parse_kernel_allow`, and the two readers of
  `docs/declared-absences`, `check_doc_refs.read_declared_absences` and
  `trace._declared_absences`.
- **Home:** `kitlib.config.declared_entries(path)`, the one walk: `utf-8-sig`
  with replacement, `\n` lines, the em dash separator. Each reader keeps only
  what its own file's key means (a token, three key fields, a module key, a
  path).
- **A file saved with a byte-order mark:** `check_doc_refs` and
  `trace._declared_absences` read the mark into the first key, hiding the
  first entry; the other three strip it. **Kept: stripped.**
- **An undecodable byte:** `check_doc_refs` raised, `trace._declared_absences`
  read no entries at all; the others replace it. **Kept: replaced.**
- **`docs/declared-absences`, `path - reason` (a hyphen):** `check_doc_refs`
  declared the path; `trace` did not. **`path—reason` (no spaces):** `trace`
  declared it; `check_doc_refs` reported it unparsed. **Kept: neither; the
  em dash with a space each side only**, which is the file's own header, its
  interface row's data cell (IF-072: "path then em dash then reason") and
  the grammar of the other four files; the stricter.
- **`docs/declared-absences`, `dir/ — reason`:** `check_doc_refs` strips the
  slash; `trace` kept it. **Kept: stripped**, the reader of record
  (`gen_arch_map` and `test_dogfood_sync` already read the file through it).
- **Out of §13.16:** `trajectory_arch`'s `docs/if-tc-coverage-allow` parse
  has a different grammar (the reason is optional, and a `# seed-count:`
  comment is read), so it keeps its own walk.
- **Adopter-visible:** a hyphen-separated declared absence stops declaring
  its path and is reported as an unparsed line (a tightening); a BOM'd file's
  first entry starts counting. RESYNC entry.

### 11. Rolling review §13.14: the generator freshness arm: out of scope

Read on today's tree, the four copies (`gen_arch_map`'s three arms,
`gen_components`, `gen_open_items`, `gen_skills_index`) agree on the verdict
for every input: exit 1 exactly when the newline-normalized output differs
from the render. What differs is (a) a missing output, which each generator
answers by a posture it documents as deliberate (an opt-in host document is
"nothing to check", a required view is stale, a hand-authored map host is an
error), as the review's own verifier found ("a deliberate opt-in posture for
optional docs, so the helper needs a per-generator missing policy"); and
(b) the stream the STALE line goes to, which `check.py` merges
(`run_step_captured`) or streams whole, and which decides nothing. So it is a
duplicated arm of plumbing, not a disagreeing policy duplicate, and this row
does not take it. The review's proposal (one `check_or_write` and one
generator table) stays where the review left it.

## Architectural delta

- Every home is in the shared kernel (`kitlib/spine.py`, `kitlib/registry.py`,
  `kitlib/config.py`, each listed in `docs/kernel-modules-allow`), so an edge
  into one is not a cut. The callers already import `kitlib`, except
  `handback`, which gains `kitlib.registry`. No component boundary moves; no
  interface row is added or retired.
- IF-112's note (that `check_docs` keeps its own whole-file scrape) and
  IF-072's note (that names `trace._declared_absences` as a reader of its own
  grammar) are corrected to the one home. Both rows are Drafted.
- New design rows for the new homes (`value_to_cell`, `id_number`,
  `queued_spec`, `governing_spec`, the moved `split_cmd`,
  `declared_entries`), each Drafted; a design row that named a deleted
  function drops it from its traced `code_symbol` cell.

## Trust

`PROCESS.md` §3 "When a guard is owed". What changes for a file with
authority over a hold, an act or a gate:

- **Queued-spec lookup** governs three acts (claim, handback writes, the
  consolidation close) over `docs/work/queued/`. Two now refuse an input
  they used to act on; none acts on an input it used to refuse.
- **B8b** governs how every registry reader reads `docs/work/`. A spec with a
  non-string value, which the readers read, is now reported malformed and
  skipped by the scheduler; nothing the readers refused is now read. The
  converter now refuses two shapes it accepted.
- **§13.13** governs which copy of a spec the merge slot's verdict-owed check
  and the Done-when hold read. They change only on trees no kit route writes,
  and both now read the same copy. `adoption_record`'s refusal is unchanged.
- **B5 and §13.16** govern what `check_docs`, `check_flows`, `check_doc_refs`
  and `trace` accept. Each change is a tightening (an id or a declaration that
  named nothing stops counting), apart from a BOM'd file's first entry, which
  starts counting as its reader intended.
- **§13.22** changes which command `check.py` runs, on an input carrying a
  bare `#`, to the command the file declares.
- B3, B12, B10 and the id number govern no hold, act or gate. B10 widens three
  advisory signals.

## Done-when

- [x] Each of the 11 has one implementation that every former copy calls, and
      the copies are deleted; or, for §13.14, the spec says why it is not a
      disagreeing duplicate on today's tree. One commit per behaviour, in the
      order above, each with its pinning test.
- [x] Where copies disagreed, the kept answer is the one stated above for each
      input, pinned by a test naming that input. A choice that changes what an
      adopter sees is named in the Deliverable, with a RESYNC entry where a
      shipped script's output changes.
- [x] The two pins that check nothing are repaired: `value_to_cell` gains the
      `None` case, and the `need_ids` pin runs on a TOML needs file.
- [x] `consolidate` finds every OI edge `split_pred_edges` finds (B10).
- [x] The `[dupes-census]` baseline is re-stamped downward if the count drops.
- [x] The new design and test-case rows are Drafted, and the component view
      and the other generated views are regenerated for them.
