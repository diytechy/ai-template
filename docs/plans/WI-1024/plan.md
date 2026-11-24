# WI-1024 (F-4): the plan

The constrains cells, the derived interface coverage and its population.
Branch `maint/wi-1024`, cut from `refactor_again` at `bba30552f`. Spec:
`docs/work/queued/WI-1024-constrains-coverage.md` (it moves at close); its
specref is the review-churn plan's
[pointer rules](../2026-10-11-review-churn/pointer-rules.md).
This file is phase 1 of `planmode = "single"`: nothing below is built until
the coordinator confirms it, and section 16 lists the calls to confirm.

Every count here was measured on this branch at `bba30552f` with tomllib over
the registries, `arch_inputs.implements_index` (the back-link index),
`arch_interfaces.contract_homes` (the file stating each contract body) and the
harvested `docs/interface-reference.md`. The per-interface first pass is
[candidates.md](candidates.md).

## 1. The cells and their class

**Schema.** `kitlib.spine.SPINE_TIER_KEYS` gains `constrains` on `SR-ID`, and
`constrains`, `dimensions` and `out_of_domain` on `LLR-ID`; `spine_carrier`'s
`SPINE_COLUMN` maps them to `Constrains`, `Dimensions` and `OutOfDomain`, and
`migrate_carrier.KEY` gains the inverses (`tests/test_rule_sync.py` pins the
pair). Since WI-1023 the loader refuses an undeclared key, so the cells must
be declared before any row carries one, and a `dimensions` cell on an SR stays
refused by the same rule.

**Cell shapes** (Done-when 1). `constrains` is a list of one or more `IF-###`
ids, written like `sr_refs`. `dimensions` is one string in the permutation
grammar (`name=range[a..b]`, `name=set{...}`, `name=bool`, an optional
`@full|@pairwise|@boundaries`). `out_of_domain` is one sentence.

**Templates and headers.** The LLR template's example row sets all three keys
with guidance (`constrains = ["IF-000"]` with a trailing comment, a
`dimensions` example that parses, and a one-sentence `out_of_domain`), and its
`detail` guidance says placement is derived from the interfaces the row
constrains and those its verifying cases name. The SR template's example row
sets `constrains` (the system boundary only) and its `permutations` guidance
says the SR cell holds system-boundary dimensions and an LLR constraining an
interface states its own input set in `dimensions`. The interface registry's
header, live and template, gains one paragraph: a row states its form; the
behaviour across it is stated by each LLR or SR whose `constrains` names it;
every live interface reaches an executable test case through such a row or a
case whose `verifies` names it. (The live LLR and SR registries carry no
header.)

**The grammar check.** The grammar's one parser moves from
`gen_cases.parse_spec` into `kitlib.spine` as a function raising `ValueError`;
`parse_spec` calls it and turns the error into the same `SystemExit` text, so
`gen_cases` behaves as before (its tests stay unchanged). The dimensions rule
calls the kernel parser, so the cell refuses exactly what the generator
refuses.

**The findings** (all fail `trace.py --strict`; none runs in the commit
hook's `--strict-integrity`):

| Finding | Where |
|---|---|
| a `constrains` id that is no live interface row (a retired, unknown, non-interface or example id), on an LLR or an SR | `coherence.constrains_findings` |
| an empty list | already refused when the registry is read (`spine_carrier.empty_value_findings`); a test pins it for the new cell |
| a `dimensions` cell the grammar refuses | `coherence.constrains_findings` |
| an `out_of_domain` cell that is not one sentence: one line, ending in a full stop, no interior sentence end (decision D14) | `coherence.constrains_findings` |
| either companion cell on an LLR with no `constrains` | `coherence.constrains_findings` |

**The warn-first missing-cell report** (operator, 2026-11-21, recorded in the
queue-drill hand-off §3.6 and the spec's Context). One advisory line: the LLRs
carrying `constrains` without `dimensions`, and without `out_of_domain`,
counted by the channel of each interface they constrain, the first ten named.
It never changes an exit code. Its output at the last slice's tip is the
Deliverable's evidence for the later strictness call.

**The class** (`acceptance_record.SPINE_TRACED_CELLS` /
`SPINE_ACCEPTED_CELLS`, `intake.ROUTED_TRACED_CELLS`):

- **`constrains` is traced (SR and LLR) and routed.** It is a pointer, the
  same shape as `SR-Refs` and `Verifies`: it names a row in another registry
  and carries no prose. Classed accepted (the residual), it would arm a
  re-accept window on every one of the roughly 120 populated rows for a
  change that moves no accepted text. It is routed, like `SR-Refs`,
  `Verifies`, `SN-Refs` and `Boundary-Refs`, because a changed `constrains`
  moves what the row claims: it is the coverage relation, it places the row,
  and it sets the blast radius. Whether the row's text states the behaviour
  across the named interface is a judgement on the row, the one the pointer
  rules give the sitting ("does the named interface carry what this row
  constrains?"). Silent, the whole population would land unjudged. Under
  WI-1060's rule, a routed link on a row an act does not name waits for that
  row's own act, so every populated row is owed a sitting.
- **`dimensions` and `out_of_domain` are accepted** (LLR). Each is a
  statement the row makes, the one home of the behaviour's input set, as the
  SR `Permutations` cell is accepted today. On an accepted row either is an
  amendment of accepted text, judged against the three row rules like any
  other: no code name in a dimension's name or values, every value and the
  out-of-domain behaviour driven by a test the row's TC names, and nothing
  beyond the parent SR.

`ROUTED_TRACED_CELLS` moves to `record_rows.py` in WI-1060, which lands first;
see D16. The registry machinery reference's traced-versus-accepted table
gains the three cells.

## 2. The two checks

**The derived coverage check** (Done-when 2 and 5) lives in `coherence.py`,
the module of row joins (`coherence.interface_coverage`), reading one new
derivation in the shared kernel, `kitlib.spine.interface_reach(ifs, srs,
llrs, tcs)`, which is the blast radius:

- an interface's **rows** are the LLRs and SRs whose `constrains` names it,
  and the LLRs a case naming it verifies (observed at it, per pair, as
  placement reads it);
- its **cases** are the cases naming it, the cases verifying any of its rows,
  and, for a constraining SR, the cases verifying the LLRs whose `sr_refs`
  name that SR (D4; WI-1027's tree walk replaces this one step when it lands);
- a case is **executable** unless its `automated` cell reads `No`, the kit's
  one observation marker (`assumption_rules.is_observation_tc`, LLR-233). The
  spec's "Inspection, Analysis or Attest evidence" is that set (D3).

An interface whose cases hold no executable case is reported, naming it; one
whose cases are all observation cases is reported on its own line as reached
by observation alone. Example rows are not read; with no live interface row
the check is vacuous, and the `[checks] interfaces_check` opt-out silences it
(D5). A count line in `trace_text` (`coverage_line`, beside the existing
`placement_line`) counts the interfaces reached through a constraining LLR,
through a constraining SR, through a naming case alone, by observation alone,
and not at all: interface coverage counts LLR and SR `constrains` alike.

**The per-pair repeat check** (Done-when 3) lives in `coherence.py`
(`coherence.repeat_findings`). For each interface a case's `verifies` names,
the name is redundant for a verified LLR or SR whose `constrains` includes
that interface. It is a finding only when it is redundant for every LLR and
SR the case verifies; a case verifying no LLR or SR is never a finding. It
runs under `trace.py --strict` and not under `--strict-integrity`, so the
commit hook never runs it (F-call 3).

Measured consequence (D2). 131 of 427 cases name an interface; 125 of those
also verify an SR, and no SR carries `constrains` today. Read as written, a
verified SR without `constrains` keeps the name, and after the scripted
population the check fires on 8 names over 4 cases (TC-253, TC-301, TC-308,
TC-309). Read for LLRs only, it would fire on 147 names over 102 cases, each a
routed `Verifies` change on an accepted case. This plan builds the reading as
written.

**Warn-first, then strict.** Both checks land warn-first: their lines go to
the interface advisories, never an exit code. The last slice (section 4)
moves both into the failing set in one commit, red first, together with the
case strips the repeat check asks for and OI-43's retirement. The strips wait
for that slice because, under the scripted picks, three of the names they
remove (IF-176, IF-264, IF-265) are their interface's only case citation and
are not on OI-43's allowlist, so stripping them earlier fails
`check_trajectory --strict` while OI-43's check stands.

`trace.py` only wires: one new failing `Findings` field, the calls in
`analyze`, `exit_code` and the console/report renderers, about 16 code lines
against its ratchet of 3784 (a reviewed re-stamp; WI-1027 also touches the
file). `coherence.py` grows by about 150 lines from 220.

## 3. Population, measured before it is planned

**Live interfaces: 239.** 235 owned by a component, 4 by an `external:`
party.

| Channel | Component-owned | `external:` | Total |
|---|---:|---:|---:|
| call | 103 | 0 | 103 |
| file | 53 | 0 | 53 |
| exit-code | 39 | 0 | 39 |
| cli | 22 | 1 | 23 |
| stdout | 13 | 0 | 13 |
| bytes | 3 | 1 | 4 |
| env | 1 | 1 | 2 |
| git | 1 | 1 | 2 |

By owner: CMP-006 98, CMP-008 76, CMP-007 38, CMP-009 23, `external:` 4.
50 realize a boundary crossing (B-05 43, B-04 4, B-10 2, B-01 1). 19 are
constituents riding a bundle (`carried_by` IF-102 or IF-123); each needs its
own reach (D19). 238 have a contract body in exactly one file.

**Already named by a case: 130** (131 cases, of 427), every one by an
executable case. Under the derived rule these 130 are reached today; the
other 109 are not, and no row carries `constrains`. (OI-43's allowlist holds
128 entries, 127 live; 18 of them are now cited by a case.)

**Obvious constraining LLR from today's evidence.** One rule, applied by a
script over the registries, the back-link index and the contract bodies,
takes the strongest evidence tier that yields a candidate:

| Tier | Evidence | Interfaces |
|---|---|---:|
| 1 | a case naming it verifies the LLR, and the LLR's back-link sits in the file stating its contract (both agree) | 92 |
| 2 | (`call` rows) the function the interface names carries the LLR's back-link | 13 |
| 3 | a case naming it verifies the LLR (no back-link in the contract's file) | 30 |
| 4 | the contract body cites the LLR by id | 5 |
| 5 | exactly one LLR is back-linked in the contract's file | 18 |
| 6 | several LLRs are back-linked in the contract's file | 50 |
| 7 | no evidence (mostly registry, configuration and document formats, whose body sits in a README or header that carries no back-link) | 31 |

So 92 interfaces have an obvious candidate (69 of them a single LLR), 66 more
a scripted one (tiers 2 to 5), and 81 are judged (tiers 6 and 7). Tiers 1 to
5 name 118 distinct accepted LLRs; a greedy cover of the same sets needs 93.
By channel, `cli` sits mostly in tier 1 (16 of 23) and `call` in tiers 1 to
3 (79 of 103), while 26 of the 31 tier-7 interfaces are `file` rows.

**The method.** The script's tiered pick is a proposal, never a link. Each
interface is then judged row by row: read the candidate LLR's text, the
interface's form (its `data` cell and contract body) and the tests the
LLR's TC names, and keep the link only where the LLR's text states the
behaviour across that interface. A link that fails that test is dropped.
Where no existing LLR states the behaviour, a new `Drafted` LLR does, under
the SR it serves, with a new `Drafted` TC naming the existing tests that
drive it (tagged in those files). The rules the judgement follows:

- one constraining row per interface is enough; prefer the LLR that already
  constrains a sibling interface of the same surface (a script's `cli`,
  `exit-code` and `stdout` rows), so the number of touched accepted rows
  stays near the cover, not the candidate count;
- prefer an LLR whose text carries no code name when two state the same
  behaviour;
- an LLR constraining interfaces of several components gets all its links in
  the slice of the first, so no row is touched twice;
- an SR carries `constrains` only where its own requirement states the
  behaviour across a system-boundary interface and no LLR does;
- `dimensions` and `out_of_domain` are written only where the behaviour's
  input is a closed set the grammar states and every value, and the
  out-of-domain behaviour, is driven by a test the LLR's TC names (D21);
  otherwise both stay absent and the warning counts them.

The judged table, one line per interface with its link, the reason and the
evidence, replaces [candidates.md](candidates.md) in each population slice,
so the reviewers and the sittings read the reasoning beside the registry
diff.

**Estimates** (ranges; the Deliverable records the actuals):

| What | Estimate |
|---|---|
| accepted LLRs gaining `constrains` | about 120 (95 to 150) |
| of those, carrying code names that rule 1 scrubs (measured: 82 of the 118 scripted candidates) | about 85 |
| LLRs gaining `dimensions` and `out_of_domain` (mostly `exit-code`, `cli` and enumerable `call` rows) | about 40 (25 to 60) |
| SRs gaining `constrains` | 0 to 5 |
| new `Drafted` LLRs (mostly the tier-7 formats) | about 20 (10 to 35) |
| new `Drafted` TCs for them | about 20 (at most 27 left after the mechanism's six) |
| accepted TCs whose `verifies` loses a redundant name | 4 (last slice) |

**The four `external:` rows** each get the LLR stating our reading of the far
side: IF-032 (`git`: the staged diff, the commit message, the outgoing range)
judged among LLR-017, LLR-018 and LLR-031 (the secrets scan reads it);
IF-036 (upstream document bytes) LLR-022; IF-041 (the agent CLI's headless
invocation) judged between LLR-026 and LLR-163; IF-277 (the agent CLI's
environment variables) LLR-300. A new `Drafted` LLR only where none of these
states the reading. None realizes a crossing, so none takes an SR.

## 4. The adjudication load

Every amended accepted row and every new row goes to a sitting:

| Rows | Count |
|---|---:|
| accepted LLRs gaining `constrains` (with scrubs and companion cells) | about 120 |
| re-cut accepted rows (section 7): LLR-042, LLR-199, LLR-244, LLR-403, SR-211, SR-249, TC-080, TC-195, TC-480 | 9 |
| SRs gaining `constrains` | 0 to 5 |
| accepted TCs losing a redundant name | 4 |
| new rows: the mechanism's six LLRs and six TCs; the population's LLRs and TCs | about 52 |
| **total** | **about 190 (160 to 230)** |

**Brief size.** The second sitting judged 57 rows on a 398K-character brief
(Neon, 488 s); the third 38 rows on 275K (444 s): about 7K characters a row.
190 rows are about 1.3M characters, four to five times the largest sitting
yet. Each sitting's bundle also carries, once, the form of every interface its
rows constrain (the `data` cell and contract body, about 1.1K characters
each).

**Batching.** By the owner component of the interfaces the rows constrain,
at most about 40 rows a sitting (near the third sitting's size), six
sittings: A (the mechanism but the two check rows, the re-cuts but LLR-042
and TC-080, the four `external:` rows, CMP-009: about 37), B (CMP-007: about
33), C1 and C2 (CMP-008: about 63), D1 and D2 (CMP-006: about 74), E (the last
slice: LLR-042, TC-080, the coverage and repeat rows with their TCs, the four
strips: about 10, foldable into D2).

**Slices: yes.** Five merges of this branch, the spec staying in `queued/`
until the last closes it (D10):

1. the mechanism: schema, templates and headers, class tables, grammar,
   findings, the warn-first report, both checks warn-first, placement and
   reach, the readers, PROCESS.md §4's dimensions text, the slice's RESYNC
   entry, the mechanism's six LLRs and six TCs, the re-cuts but LLR-042 and
   TC-080, and the CMP-009 and `external:` population (sitting A);
2. the CMP-007 population (sitting B);
3. the CMP-008 population (sittings C1, C2);
4. the CMP-006 population (sittings D1, D2);
5. **the strictness**: both checks fail `--strict`, the four case strips,
   OI-43's retirement (section 6), LLR-042 and TC-080, the coverage LLR's
   strict wording, the second RESYNC entry, the Deliverable's channel counts,
   the close-out (sitting E).

Slice 5 carries the strictness and lands after sitting D2's act, so no link a
sitting returned is what holds coverage strict. Slicing keeps each review
diff and each sitting bounded, lets a sitting's returns correct the next
slice's population before it repeats the mistake, and keeps trunk green
throughout: the population slices touch registries only and both checks stay
advisory until every interface is reached. The coverage and repeat LLRs
(LLR-421, LLR-422) and their TCs stay `Drafted` and out of sittings until
slice 5, so their warn-first text is never accepted and then amended (D11).

## 5. The readers, by function

| Reader | Change |
|---|---|
| `kitlib.spine.llr_placement(tcs, ifs, llrs=())` | places each LLR at the component owner of each interface its `constrains` names, unioned with the per-pair case placement; an `external:` owner places nothing; `llrs` defaults empty, and every caller below passes it |
| `kitlib.spine.interface_reach` (new) | the blast radius (section 2); its first reader is the coverage check; WI-1029's component context and WI-1030's audit reuse it, and WI-1027's walk replaces its SR-to-LLR step |
| `trace_text.placement_line` | passes `llrs` |
| `trace_text.coverage_line` (new) | the interface coverage counts |
| `gen_components.build` | passes `llrs`; the component view places rows through `constrains` (LLR-199) |
| `traj_parse.placed_llrs` | passes `llrs`; the dashboard's architecture view (the What-tab icicle) shows a design row's placement through `constrains` in its detail |
| `intake._placement` | loads the design rows and passes them; the build brief's code map and its packs and seams follow |
| `check_trajectory._placed_sr_components` | passes the rows it loads; the knowledge-pack advisory follows |
| `assumption_rules.component_srs` | passes `llrs`; the interface-form gate's no-source fallback reach follows, with LLR-244's clause re-cut to cite LLR-403 (D8) |
| `arch_interfaces.interface_findings` | its "IF seam(s) are cited by no TC" total line retires (slice 5): the coverage line replaces the count, and the direct relation is no longer owed |

The SW containment drill (`rendering/traj_views.sw_containment`) draws seams
between components from the interface rows and reads no requirement, so it is
unchanged. An SR is not placed, so an SR's `constrains` feeds reach and
coverage and never placement.

## 6. OI-43's retirement (slice 5)

- **The direct check.** `arch_interfaces.if_tc_coverage_findings`,
  `if_tc_allow_hygiene_findings`, `if_tc_allow_parse_findings`,
  `read_if_tc_allow`, `parse_if_tc_allow`, `_parse_if_tc_allow_full`,
  `if_tc_allow_growth`, `IF_TC_ALLOW` and `IF_TC_SEED_RE` are deleted, with
  `trajectory_arch`'s and `check_trajectory`'s re-exports and
  `check_trajectory`'s two call sites. The `docs/complexity-baseline` entry for
  the hygiene function goes; the size ratchet re-stamps `check_trajectory.py`
  and the arch modules downward.
- **The allowlist.** `docs/if-tc-coverage-allow` is deleted (128 entries,
  seed 98). The comments naming it as a precedent (`arch_seams`,
  `arch_components`, `docs/kernel-modules-allow`, `tests/test_bootstrap.py`)
  say "the retired seam-TC allowlist". `PROCESS_OPTIONS.md`'s seam-TC
  paragraph is rewritten to the derived rule; PROCESS.md §8's "Every interface
  is backed by a contract/fixture test cited from a TC's Verifies" becomes the
  derived rule (a watched-file delta, restamped in the byte-budget skill).
- **LLR-042** loses its uncited-seams clause (section 7), and `TC-080` its
  seam-citation case; `tests/test_trajectory_arch.py`'s
  `test_seam_tc_citation_warn` flips to assert the check reports no uncited
  seam, and the allowlist tests (`SEEDED_IF_TC_ALLOW` and the promotion,
  hygiene and parse tests, none tagged to a TC) are deleted.
- **OI-43's record.** A dated clause appended to OI-43's `decision` cell, the
  original left as written (the precedent of OI-72's correction): the direct
  interface-to-test-case check and its allowlist retired at WI-1024, under
  the review-churn plan's variant F, once every interface reached an
  executable test case through a constraining requirement or a naming case
  (D13).

## 7. The re-cut accepted rows, with their amendments

Each is text-only, keeps `Accepted` and shows as drift. Inherited code names
are scrubbed (rule 1). Every clause kept is checked against the tests its TC
names before the commit, and a clause with no driving test is cut.

**LLR-199** (SR-070; TC-195; sitting A). It restated the placement rule, so
it now cites LLR-403, and its code names go.
- `detail`: "The component view is derived from the component, design-row,
  system-requirement, interface and test-case registries and the files'
  component headers. The component registry declares the components, and each
  file's header places that file in one. Each design row is placed where
  LLR-403 places it, and a system requirement reaches the components its
  placed design rows sit in. The interface registry gives each seam's owner and
  far side. The view is written to the generated component file, which a
  freshness check compares with a regeneration, failing when they differ.
  For each component the view lists its member design rows, the requirements
  they decompose, the perspectives in effect on those members, its files, and
  its seams split into internal and boundary. A requirement reaching no
  component appears once in the counted unplaced table. A requirement in
  several components appears in each and in each component's shared list. A
  seam appears in each component its endpoint cells name: internal to the
  lowest component enclosing every endpoint through the part-of chain,
  internal to none when an endpoint is an external party or no component
  encloses them all, and boundary to every other; a seam naming no declared
  component stays in the unplaced table. No acceptance or maturity cell
  appears in the view. With no real component row and no view on disk, the
  generator exits 0 and writes nothing."
- `rationale`: "The column this replaces promised a prose home the kit never
  created and no script ever read, which is the weakest form a design record
  can take: its staleness was undetectable by construction. A derived view
  inherits every check the spine already carries, since the rows it joins
  have to be correct for the gate to pass, and the same freshness check the
  other generated views carry reports it stale. The cost is accepted rather
  than hidden: a requirement list says what a component is obliged to do and
  nothing about how its parts fit, so the artifact that stays true is bought at
  the price of the artifact that showed mechanism. The coverage edges are
  answered in the emitted file rather than in the generator's head, because a
  view that silently drops rows is indistinguishable from one with a bug."
- `title` unchanged. The unplaced design-row clause moves out: LLR-403 states
  it and TC-480 drives it.

**TC-195** (verifies SR-070, LLR-199; sitting A). `method`: the JOIN sentence
becomes "THE JOIN: assert the design rows are placed where the derived
placement puts them, through an interface a design row constrains and through
the interfaces its verifying test cases name, and the requirement tier is
reached through them, while the files come from their component headers.";
"--check passes on a fresh view" becomes "the freshness check passes on a
fresh view"; "the inert -000 example" becomes "the inert example row". The
rest unchanged. A new test in `tests/test_gen_components.py` drives the
`constrains` half.

**LLR-403** (SR-249; TC-480; sitting A).
- `title`: "A design row sits where the interfaces it constrains or its
  verifying test cases name are owned, and one placed nowhere is counted"
- `detail`: "A design row is placed at the owner of each interface its
  constrains cell names, and, for each pair of a test case and a design row
  its verifies cell names, at the owner of each interface the same case
  names, where that owner is a component; an interface owned by an external
  party places nothing, and a row placed at several components is placed at
  each. Example rows are not read. A row placed by neither is unplaced. The
  generated component view lists each placed row in its components and each
  unplaced row in its unplaced table, counted in its census; the state view's
  design-row detail shows a placed row's components and the word unplaced for
  the rest; and the strict check's report prints one line counting the placed
  and unplaced rows, naming the first ten unplaced and counting the rest.
  Being unplaced does not change the strict check's exit code."
- `rationale`: "A row that named its component restated by hand a fact the
  interfaces it constrains and the cases verifying it already hold, and the
  copy drifted when the code moved; deriving it leaves one home. Counting
  rather than refusing keeps a decomposition whose interface is not yet named
  legal while keeping the gap visible."

**TC-480** (verifies SR-249, LLR-403; sitting A).
- `method`: "Place design rows over test cases naming interfaces: one case
  naming two interfaces owned by two components, a second naming one of them
  for two rows, a case naming an interface an external party owns, a case
  naming no interface and an example case; and place a design row that
  constrains an interface a component owns and is verified by a case naming
  none, and one that constrains an interface an external party owns. Count the
  unplaced rows, then count twelve unplaced rows; build the component view,
  and render it, from the same rows; and read the state view's design-row
  detail for them. Then run the strict check over a project whose one design
  row is verified by a test case naming no interface."
- `expected`: "The first row is placed at both components and the second at
  the one its case names; the row constraining the component's interface is
  placed at that component; the external owners and the interface-free case
  place nothing, and the example case is not read. The two unplaced rows are
  counted and named on one line, and of twelve the line names ten and counts
  two more. The component view holds each placed row and its requirement in
  its components, lists the unplaced rows and counts them in its census; the
  state view shows each placed row's components and the word unplaced for the
  others. The project's check passes with its row unplaced, its report
  counting that row as unplaced."

**SR-249** (sitting A). Rule 3 needs it: LLR-403 now places through
`constrains`, which the SR did not allow.
- `title`: "Where a design row sits is derived from the interfaces it
  constrains and those its verifying test cases name"
- `requirement`: "The delivered harness shall derive the components each
  design-tier row sits in from the interfaces it constrains and those its
  verifying test cases name, counting a row placed in none as unplaced rather
  than refusing it."
- `rationale`: "Realizes SN-002 and SN-023. Where a row sits follows from the
  interfaces whose behaviour it states and those it is verified at, each owned
  by a component, so placement is derived and never restated on the row. A row
  that named its component restated by hand a fact the interfaces and the
  cases verifying it already hold, and the copy drifted when the code moved;
  deriving it leaves one home. A row placed nowhere is a decomposition whose
  interface is not yet named, which is legal and visible, so it is counted and
  listed rather than refused, and the views a reviewer reads to see how the
  parts connect show it as unplaced."
- `acceptance_criteria`: "A design row is placed at the owner component of
  each interface it constrains and of each interface that a test case
  verifying it names, once per component; an interface owned by an external
  party places nothing, and a row placed at several components is placed at
  each. The generated component view lists each placed row in its components
  and each unplaced row in its unplaced table, the state view shows each
  design row's components or that it is unplaced, and the strict check's
  report counts the placed and the unplaced rows; a row's being unplaced does
  not change the strict check's exit code."

**SR-211** (sitting A; `rationale` only). Its last sentence says the
requirement a seam answers "stays derived through the interface's owner",
which `constrains` makes false. New last sentence: "A requirement stating the
behaviour a seam carries names that seam in its own constrains cell, and the
relation is never recorded on the interface, so it keeps one home." Its
`requirement` and `acceptance_criteria` are unchanged ("no requirement
reference is recorded on the interface" stays true).

**LLR-244** (SR-212; sitting A; D8). One clause: "Where no source is scanned,
an interface instead reaches the requirements of the design rows placed in its
owner component, a design row placed through the interfaces its verifying test
cases name." becomes "Where no source is scanned, an interface instead reaches
the requirements of the design rows placed in its owner component, each placed
as LLR-403 places it." The rest is unchanged; its column and stage names are
registry terms, not code.

**LLR-042** (SR-159; TC-080; slice 5, sitting E).
- `detail`: "Emits warn-first findings that never change the exit status: one
  for each component holding an inventory file by its header that no
  interface row names, that owns no row, or that is on no row's far side, and
  one for each contract declaration in a file naming no interface row. A
  source note on a row marks its owner deliberate and a sink note its far
  side, each suppressing that direction's finding. The process
  configuration's interface-check opt-out silences them all, and an absent
  inventory or one of a single file is vacuous. Whether an interface reaches a
  test case is not this row's finding."
- `title` unchanged; no `rationale`.

**TC-080** (verifies SR-159, LLR-042, IF-316; slice 5, sitting E).
- `method`: "Run the per-component connectivity cases, the source and sink
  note cases, the contract-declaration case, the opt-out case and the strict
  non-gating case, and run the connectivity check over an interface no test
  case names."
- `expected`: "Each component gap and each contract declaration naming no
  interface row warns without failing the strict check; each note-suppressed
  direction and the opted-out run stay silent; and the interface no test case
  names draws no finding from this check."

## 8. The new rows (the mechanism)

`Drafted`, phase 6 (the F rows' precedent: LLR-404 sits under SR-157 at 6).
Each TC verifies its SR and LLR and names no interface.

- **LLR-417** (SR-157) "A design or system-requirement row names the
  interfaces it constrains, each a live interface". "A design row or a
  system requirement may carry a constrains cell listing one or more
  interface ids, written as its other reference lists are. Each id must name a
  live interface row, the example row excluded; one that does not is a finding
  that fails the strict check, naming the row and the id. An empty list is
  refused when the registry is read, as any explicit empty cell is." TC-527.
- **LLR-418** (SR-157) "A design row's input-set and out-of-domain cells
  parse, and sit only beside a constrains cell". "A design row carrying a
  constrains cell may carry a dimensions cell, one string in the permutation
  grammar of ranges, sets and booleans with an optional combination strategy,
  and an out-of-domain cell, one sentence saying what the interface does with
  an input outside those dimensions. A dimensions cell the grammar does not
  parse, an out-of-domain cell that is not one sentence, and either cell on a
  design row with no constrains cell are each a finding that fails the strict
  check, naming the row and the cell." TC-528.
- **LLR-419** (SR-157) "A design row constraining an interface without its
  input-set or out-of-domain cell is reported without failing the strict
  check". "Each design row carrying a constrains cell but no dimensions cell,
  or no out-of-domain cell, is counted on one warning line by the channel of
  each interface it constrains, the first ten named; the warning does not
  change the strict check's exit code." TC-529.
- **LLR-420** (SR-178) "The constrains cell is traced and routed to
  adjudication, and the input-set and out-of-domain cells are accepted text".
  "A requirement or design row's constrains cell is a traced cell: changing it
  on an accepted row moves no accepted text, and the change is routed to
  adjudication as a changed requirement or verifies reference is. A design
  row's dimensions and out-of-domain cells are accepted cells: changing either
  on an accepted row amends its accepted text." TC-530.
- **LLR-421** (SR-157) "An interface whose reach through the rows
  constraining it and the cases naming it holds no executable test case is
  reported". "An interface's reach is
  the design rows and system requirements whose constrains cell names it, the
  design rows a test case naming it verifies, and every test case naming it or
  verifying one of those rows, a requirement's cases including those of the
  design rows decomposing it. Each live interface whose reach holds no test
  case the harness runs is reported, naming it, and one whose reach holds only
  observation cases is reported as reached by observation alone; a count line
  gives the interfaces reached through a constraining design row, through a
  constraining requirement, through a naming case alone, by observation alone
  and not at all." Slice 1 adds "These findings do not change the strict
  check's exit code"; slice 5 replaces it with "Each reported interface is a
  finding that fails the strict check." TC-531. Held out of sittings until
  slice 5 (D11).
- **LLR-422** (SR-157) "A test case naming an interface that every row it
  verifies already constrains is reported". "For each interface a test case's
  verifies cell names, the name repeats a verified design row or system
  requirement whose constrains cell includes that interface. The name is
  reported, naming the case and the interface, only when it repeats every
  design row and system requirement the case verifies; a case verifying none
  is never reported, and a case verifying one row that constrains the
  interface and one that does not is not reported. The integrity check the
  commit hook runs does not report it." Slice 1 adds "The report does not
  change the strict check's exit code"; slice 5 replaces it with "Each
  reported name is a finding that fails the strict check." TC-532. Held out
  of sittings until slice 5 with LLR-421 (D11).

## 9. How the rows stay inside the three row rules

- **No code names.** Before each commit a scratch scan lists every token
  shaped like a file, flag, function, symbol, constant or call signature in
  each row the commit adds or changes; the commit carries none, inherited
  ones included (D9). Registry and cell names stay (`constrains cell`,
  `verifies cell`, the component registry); the contract terms used are "the
  strict check", "the integrity check", "the component view", "the freshness
  check". A dimension's name and values name inputs ("findings",
  "state=set{current,stale,missing}"), never a flag or a parameter.
- **One obligation, every clause tested.** Each new LLR above states one
  obligation; a clause-to-test table per new or amended row is kept in the
  slice's population table and in the Deliverable, and a clause with no
  driving test is cut, never left. `dimensions` is written only where each
  value is driven (D21). SR-249 keeps one `shall` and its criterion bounds
  its absolutes ("does not change the strict check's exit code").
- **A child within its parent.** Each amended LLR is re-read against its SR
  after the rewording, and each TC against the rows it verifies; SR-249 is
  amended because LLR-403 would otherwise exceed it. A `constrains` link
  adds no clause to the row's text, so it cannot exceed the parent, but the
  link is kept only where the text already states the behaviour.

## 10. Tests (red first where new), by module

| Module | Test | Done-when |
|---|---|---|
| `tests/test_constrains.py` (new, in-process, smoke) | a dead id on an LLR, and on an SR, is a finding and `--strict` exits 1 (red first) | 1 |
| same | a non-interface id and the example id are findings (red first) | 1 |
| same | an empty `constrains` list is refused at read (a pin of the carrier rule, green at once; stated) | 1 |
| same | an unparsable `dimensions` cell is a finding (red first) | 1 |
| same | an `out_of_domain` cell of two sentences is a finding (red first) | 1 |
| same | each companion cell on an LLR without `constrains` is a finding (red first) | 1 |
| same | an LLR with `constrains` and no companion cells is counted on the warning line by channel and `--strict` still exits 0 (red first: the line is absent) | 1 |
| same | the kernel grammar parser accepts and refuses exactly what `gen_cases` does | 1 |
| same | an interface no row or case reaches is reported; one reached through an LLR's `constrains`, through an SR's `constrains` and one of its LLRs' cases, and through a naming case is not; one reached only by an observation case is reported as such (red first) | 2 |
| same | the coverage count line counts each route | 2, 6 |
| same | the opt-out silences the coverage check; no interface row is vacuous | 2 |
| same | `interface_reach` returns the constraining and observed rows and their cases | 6 |
| same | the repeat check: a name redundant for every verified LLR and SR is a finding under `--strict` and not under `--strict-integrity`; the mixed case (one verified LLR constrains the interface, another does not) is not, asserted beside its all-redundant twin so the test is red first; a verified SR without `constrains` keeps the name | 3 |
| same | slice 5: an unreached interface and a repeated name each make `--strict` exit 1 (red first against the warn-first build) | 3, 5 |
| `tests/test_llr_trace_cells.py` | placement through `constrains` (a component owner places, an external owner places nothing, the union with case placement), and the state view shows it (red first) | 6 |
| `tests/test_gen_components.py` | the component view places a row through `constrains` (red first) | 6 |
| `tests/test_trace.py` | the placement line counts a `constrains`-placed row | 6 |
| `tests/test_llr_trace_cells.py` | the build brief's context block names a `constrains`-placed row's component | 6 |
| `tests/test_if_owner_component.py` | the interface-form gate's no-source fallback reach follows `constrains` placement (D8) | 6 |
| `tests/test_cell_classes.py`, `tests/test_trajectory_staged.py` | `Constrains` traced on both tiers, `Dimensions` and `OutOfDomain` accepted, every template column classified | 1 |
| `tests/test_intake_held_act.py` | a `constrains`-only change on an accepted row is a routed amendment (red first) | 1, 4 |
| `tests/test_rule_sync.py`, `tests/test_dogfood_sync.py` | the column map and its inverse, and the templates, declare the three keys | 1 |
| `tests/test_trajectory_arch.py` | slice 5: the allowlist tests deleted; the uncited-seam test flipped | 5 |
| `tests/test_gen_cases.py` | unchanged, green (the grammar moved) | 1 |
| `tests/test_trace_golden.py` | the report gains the coverage section; golden updated | 2 |
| `tests/test_bootstrap.py` | a fresh scaffold passes `trace.py --strict` with the new template rows | 1, 7 |
| `tests/test_module_size_ratchet.py`, `tests/test_complexity_ratchet.py`, `tests/test_import_layers.py`, `tests/test_dogfood_sync.py` | re-stamped where a module grew or shrank, with the reason | 8 |

Each population slice adds the new TCs' tags to the existing test files that
drive the new LLRs, and runs `trace.py --root . --strict`,
`check_trajectory.py --root . --strict` and the test modules holding every
touched TC's tests. Every importer of a changed module runs per builder rule
5 (measured: `trace` 49 test modules, `spine_carrier` 33, `check_trajectory`
31, `intake` 27, `acceptance_record` 21; the union is most of the suite, much
of it in `SLOW_MODULES`).

## 11. The RESYNC entries

Two, since the strictness lands in its own slice (D20), both after WI-1023's:

- **Slice 1:** "Requirement rows name the interfaces they constrain, with the
  behaviour's input set, and interface reach is reported warn-first [since
  <base>]". What changed: the three cells, their findings and the warning;
  the class (`constrains` traced and routed, the companions accepted); the
  grammar's one parser; placement through `constrains`; the coverage and
  repeat reports. What to do: run `trace.py --strict` and read the coverage
  line; for each unreached interface add `constrains = ["IF-###"]` to the
  LLR (or, at the system boundary, the SR) that states its behaviour, or name
  it in a case's `verifies`; add `dimensions` and `out_of_domain` where the
  input is a closed set; each `constrains` added to an accepted row is
  routed to adjudication, and each companion cell re-opens the row.
  Kit-owned files: every script, the LLR, SR and interface templates,
  `PROCESS.md`, `PROCESS_OPTIONS.md`, the skills.
- **Slice 5:** "Every interface reaches an executable test case through a
  constraining row or a naming case, under `--strict`; the direct
  interface-test check and its allowlist retire [since <base>]". What to do:
  clear the coverage line first (it now fails `--strict`), drop each case
  name the repeat check reports, then delete `docs/if-tc-coverage-allow`.

## 12. Documents

`PROCESS.md` §4 (Dimensional coverage: the SR cell for system-boundary
dimensions, the LLR's `dimensions` and `out_of_domain`) and §8 (the derived
rule); `PROCESS_OPTIONS.md` (the seam-TC paragraph); the spine-authoring and
registry-hygiene skills and their dogfood copies; the spine questions (the
sitting's question for a `constrains` link); `docs/registry-machinery-reference.md`
and `docs/enforcement-audit.md`; the byte-budget skill's restamp. Each states
the rule once and links to PROCESS.md.

## 13. Merge notes

- **WI-1060** (lands first) moves `ROUTED_TRACED_CELLS` to `record_rows.py`
  and reworks `acceptance_record.py` and `intake.py`. This branch rebases
  onto trunk once it merges, before slice 1's class commit, so `Constrains`
  joins the moved table directly (D16).
- **WI-1027** (F-7, either order) touches `trace.py`, `coherence.py`,
  `kitlib/spine.py` and the registries. Whichever lands second moves the
  reach's SR-to-LLR step onto the tree walk, and a parent's coverage counts
  its descendants' cases.

## 14. Ids

Mechanism: LLR-417 to LLR-422, TC-527 to TC-532. Population: LLR-423 up
(57 left), TC-533 up (27 left). The TC range is the tight one: about 20
population TCs are expected; a TC verifying sibling new LLRs is used where
one set of tests drives them, and if the population needs more than 27 the
build stops and asks (D17). `trace.py --root . --bump-ids` after each mint.

## 15. Risks

- Rule 1 on every touched row (D9) makes this row rewrite about 85 accepted
  LLRs' text, a third of the 239 that carry code-shaped tokens and F-8's
  work done early. WI-1025 then moves contract-body prose into these same
  LLRs, so each is re-accepted again there either way.
- A sitting reads a touched legacy row whole, so a clause no test drives is
  exposed; the clause-to-test check before each commit is the guard, and a
  clause is cut rather than left.
- Six sittings and five merges are the critical path; the strict slice
  cannot land before the last population act.

## 16. Decisions for the coordinator to confirm

1. **D1.** `constrains` is traced and routed on both tiers; `dimensions` and
   `out_of_domain` are accepted (section 1).
2. **D2.** The repeat check as the spec words it: a verified SR without
   `constrains` keeps the name (8 names over 4 cases strip), not an LLR-only
   reading (147 names over 102 cases).
3. **D3.** Executable means `automated` is not `No`; "Inspection, Analysis or
   Attest" is the observation set; an interface reached only by observation
   fails `--strict` in slice 5 like an unreached one, on its own line.
4. **D4.** A constraining SR's cases include those of the LLRs decomposing it
   (WI-1027's walk later).
5. **D5.** The coverage check honours `[checks] interfaces_check`, the one
   opt-out OI-43's check honoured, so an adopter who opted out is not newly
   failed.
6. **D6.** The rules live in `coherence.py`, placement and reach in
   `kitlib/spine.py`, the grammar in `kitlib/spine.py` behind `gen_cases`; no
   new shipped module.
7. **D7.** The blast radius is `kitlib.spine.interface_reach`, read first by
   the coverage check; no new command-line surface in this row.
8. **D8.** Every placement reader reads `constrains`, the interface-form
   gate's fallback included, with LLR-244's one clause re-cut to cite
   LLR-403; the alternative leaves that reader on case placement and LLR-244
   untouched.
9. **D9.** Rule 1 applies to every row touched, so about 85 accepted LLRs gain
   a text rewrite beside `constrains`; the alternative leaves a
   `constrains`-only row's inherited code names to F-8, with the sitting's
   preface exempting them.
10. **D10.** Five slices, merged in turn, the spec closing at the last, with
    both checks warn-first until slice 5 (Done-when 3 and 5 hold at slice 5,
    the repeat check included); the alternative is one merge after all six
    sittings' worth of population.
11. **D11.** Sittings by owner component, at most about 40 rows, six in all;
    the coverage and repeat LLRs (LLR-421, LLR-422) and their TCs stay out of
    sittings until slice 5; slice 5 lands after sitting D2's act.
12. **D12.** SR-249 and SR-211's rationale are re-cut beside LLR-199,
    LLR-403, TC-195 and TC-480 (section 7).
13. **D13.** OI-43's record gets a dated clause appended to its `decision`
    cell, the original as written; not a `follow_up` cell, which is for a
    ruling no work item carries.
14. **D14.** "One sentence" for `out_of_domain` is one line ending in a full
    stop with no interior sentence end; an `out_of_domain` without
    `dimensions` is only the missing-cell warning, not a finding.
15. **D15.** The "cited by no TC" total line retires with LLR-042's clause
    and TC-080's case; the coverage line is the one count.
16. **D16.** This branch rebases onto trunk after WI-1060 merges, so
    `Constrains` joins `record_rows`' routed table; if slice 1 must go first,
    it edits `intake.ROUTED_TRACED_CELLS` and the merge moves the line.
17. **D17.** Ids: mechanism LLR-417 to 422 and TC-527 to 532; the build stops
    and asks if the population needs more than 27 TCs.
18. **D18.** New rows take phase 6, as LLR-404 does under SR-157.
19. **D19.** Each of the 19 bundle constituents needs its own reach.
20. **D20.** Two RESYNC entries, one per shipped slice.
21. **D21.** `dimensions` and `out_of_domain` are written only where every
    value and the out-of-domain behaviour are driven by a test the LLR's TC
    names; elsewhere both stay absent and the warning counts them.
