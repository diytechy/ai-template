+++
id = "WI-1004"
title = "The policy duplicates the OI-130 re-score found disagreeing each get one home, with the disputed inputs pinned"
workstream = "process"
sr_refs = ["SR-147", "SR-157", "SR-189", "SR-220", "SR-166", "SR-156", "SR-146", "SR-158"]
specref = "docs/plans/2026-11-11-oi130-rescore/README.md#one-home-per-behaviour-still-a-code-obligation"
buildtier = "strong"
safety_class = "ordinary"
priority = 4
planmode = "single"
+++

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
- **A bare string in a list key (`sr_refs = "SR-1"`)**: both read it
  character by character; they agree, so it is not this row's (reported as
  found).
- **Adopter-visible:** `check_trajectory` names a spec carrying a non-string
  title as malformed, and the scheduler skips it, where it read `'5'`;
  `wi_convert --to-csv` refuses a spec whose filename does not carry its id,
  or whose `adjudicates` value the registry refuses. RESYNC entry.

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

- [ ] Each of the 11 has one implementation that every former copy calls, and
      the copies are deleted; or, for §13.14, the spec says why it is not a
      disagreeing duplicate on today's tree. One commit per behaviour, in the
      order above, each with its pinning test.
- [ ] Where copies disagreed, the kept answer is the one stated above for each
      input, pinned by a test naming that input. A choice that changes what an
      adopter sees is named in the Deliverable, with a RESYNC entry where a
      shipped script's output changes.
- [ ] The two pins that check nothing are repaired: `value_to_cell` gains the
      `None` case, and the `need_ids` pin runs on a TOML needs file.
- [ ] `consolidate` finds every OI edge `split_pred_edges` finds (B10).
- [ ] The `[dupes-census]` baseline is re-stamped downward if the count drops.
- [ ] The new design and test-case rows are Drafted, and the component view
      and the other generated views are regenerated for them.
