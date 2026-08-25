## 2026-08-25 — WI-508 slices 3 and 4: the alignment adjudicates, one WI is filed, and the biggest finding goes to the owner

**Summary.** The alignment pass ran — the only role permitted to read both sides
— and it spent most of its effort **refuting** the blind maps rather than
executing them. Twelve dispositions: ten keep with a recorded reason, two keep
with the reason absent from the row, **zero consolidations and zero requirement
gaps among the twelve**. The consolidation evidence lives where A and B agreed,
and a mechanical shared-stage test dissolved three of the four families there.
One survived having its original rationale read — and the reading made the
proposal *narrower*, not larger. `WI-519` filed. The zero-SR module both teams
derived went to the owner as `OI-64`, not to the queue as module work.

Deferred open items: OI-64.

### The one fact that governs every disposition

**The live map is ~3.5× finer than either derived map** — 83 modules named in
`Module` cells against 24 and 23. A derived module is a responsibility cluster;
a live module is a file; several files realize one cluster **with no duplication
at all** provided they call a shared stage. So the adjudication question is never
"do these live in one file" but:

> does each live home re-implement the behaviour, or do they all call one home
> for it?

That is *calls, not lines* used as an instrument rather than quoted, and it is
what kept this pass from filing three consolidations that would have been wrong.

### How the live side was read, and the three-way numbers

An LLR row's `module` cell is the traced home of a design decision and its
`sr_refs` name the obligation it decomposes, so `SR` → `{modules}` is a join the
registry already carries. **75 SRs · 186 LLRs · 83 distinct modules named · 76
source files · ZERO scripts named by no `Module` cell.**

Pair agreement over the 71 SRs comparable on all three sides (2,485 pairs):
**A↔live 94.6%, B↔live 94.8%, A↔B 97.0%.**

fig: derived="for each SR, the distinct module stems named by the `module` cells of the LLR rows whose `sr_refs` cite it; then pairwise co-membership over all 2485 unordered pairs of the 71 SRs present in all three partitions"

Both derived maps sit closer to each other than either sits to live, by about
the same margin — so neither is measurably the better description of the tree,
and **neither is a verdict on it**: at 3.5× the grain a live partition cannot
score 100% against a coarser one.

Four SRs have no live module and three of them legitimately: `SR-034`
(Analysis), `SR-036` (Inspection) and `SR-114` (Analysis) carry a verification
method that exempts them from decomposition — the absence IS the declared
method. They are the package-wide-property class both teams gave a module and
the boundary registry's own note calls a "sixth capability". `SR-181` is the
last orphan and is owned elsewhere.

### The twelve dispositions

Ten **KEEP — recorded**: `SR-006`, `SR-015`, `SR-019`, `SR-020`, `SR-043`,
`SR-111`, `SR-113`, `SR-163`, `SR-173`, `SR-174`.
Two **KEEP — reason not on the row**: `SR-024`, `SR-033`.
**Zero consolidate. Zero requirement gap.**

That result is not a shrug, and the reason is structural: the twelve are exactly
the set where the two blind maps DISAGREED — the record's own weak-evidence set,
where the requirements underdetermine the boundary — so a live choice cannot be
convicted against a derived answer that does not exist. Four of the twelve are
worth naming:

- **`SR-173` — B's prediction REFUTED by measurement.** B put the regeneration
  order with the artifact graph, arguing the seam would "duplicate the graph".
  The order is stated in exactly one place, `trunk_step.regen`, with `LLR-142`'s
  rationale carrying its reason. **There is no second copy to remove.**
- **`SR-174` — B's prediction REFUTED by reading the code.** B argued non-reuse
  would live away from the mark that proves it. `intake.next_wi_id` **calls**
  `trace.read_watermark` and deliberately does not catch its refusal — "a mint
  with no record of what has been allocated is the one operation that must not
  proceed on a guess". One stage, one caller.
- **`SR-043` and `SR-024`** sit at the alternative the deriving team had already
  **named and rejected in its own honesty section** — B offered "a spawn-gate
  module of its own", A offered "a standalone case generator". Live took each.
- **`SR-019`/`SR-020`.** Both maps wanted one module; live has two hook files —
  but `LLR-021`, the interpreter probe, is cited by **both** SRs. The shared
  stage the merge argued for already exists and is traced.

**The two thin ones are banked, not fixed.** `LLR-024` and `LLR-033` carry a
defensible module and no `Rationale` — the `MAINTAINER` failure class exactly,
and `MAINTAINER` is the lens on this program's own parent row. Both rows are
`Approved`, and writing a `Rationale` onto an `Approved` row is an amendment
that overrides an attestation: **the owner's act, not a worker's.**

### The consolidation evidence, and three refutations

Forty-seven dispersion pairs (A and B agree together, live splits). The
shared-stage test dissolved three families:

| family | verdict | what the tree actually shows |
| --- | --- | --- |
| declaration reading | **REFUTED** | **38 modules import `kitlib.config`; only `config.py` defines a declared-line reader.** The single declaration module is not missing — it is built. |
| measured-value vs baseline | **REFUSED** | Three genuinely different shapes. Merging `check_perf`'s gating engine with the WARN-FIRST-FOREVER duplication census puts the disposition behind one interface and leaves `D-7` one refactor from being undone. |
| derived-copy freshness | **REFUTED** | Team A's predicted "single largest saving". Each `--check` is `render() != read()` over the generator's own renderer — lines, not calls. A requirements-only derivation cannot see that the comparison is trivial once the renderer exists. |

fig: cmd="grep -l 'kitlib.config' over the declared src root, against grep -l 'def read_declared\|def first_declared_line' over the same root" rev=64e9bf2a

The third one is this pass doing its job in the direction that protects the live
tree: the blind map was confidently wrong, and only both-sides reading could
show it.

### The one that survived — and the rationale made it SMALLER

**Declared exception lists.** Five files, five parsers, four modules. The naive
consolidation is "merge five parsers", and reading the original rationale first
is what stopped it — because each parser differs in a way its own docstring
argues: a `# seed-count:` migration baseline on one; a per-entry reason on
another stated **by contrast** with the first; a ruled required open-item id as
the FIRST TOKEN of the reason on a third; two separators and a `LIFECYCLE:`
marker on a fourth; a reason deliberately discarded on the fifth. Five recorded
decisions. A blanket extraction flattens all five to buy a few lines.

What the reading *did* surface is narrower and is a defect the repo already
diagnosed in writing. Two of the five return `(entries, unparsed)` and report a
malformed **declaring** line; three drop it silently. And
`read_provenance_allow`'s own docstring says why silence is wrong:

> "the other half of 'declares nothing' is that it also COUNTS as nothing, and
> the arms that reason about how many exceptions stand were reading that silence
> as an empty surface."

Argued once, adopted twice (`_parse_kernel_allow` names its source — "the
`docs/provenance-allow` split"), **missing three times.**

### Filed, and declined

- **`WI-519`** (`medium` / `ordinary`, no `needs`) — carry the parse-honesty arm
  to the three readers that lack it, each keeping its own grammar, required
  fields and fail-safe direction. Its spec carries an explicit **MUST NOT**
  section against the merge, a Done-when that requires a real CONSUMER for each
  new signal (an unwired report is the original gap with a better name), and the
  two call-site hazards. **On the destination, honestly:** the program's spec
  said consolidations feed the `wi448`/`wi483` lanes and both are
  closed-archived, so there is no parent lane — the row stands on its own and
  does not wait on `WI-508`.
- **Declined:** the three refuted families above; the **48 fusion pairs** (A and
  B agree apart, live fuses — `agent_loop` 14, `check_trajectory` 13,
  `agent_common` 10, `bootstrap` 5), which are the module-size ratchet's
  existing debt seen from the requirements side and are recorded as corroboration
  rather than filed as a rival program; and the remaining dispersion families,
  which have NOT had their rationale read and so are named but not filed —
  filing them without that reading is precisely what the standing directive
  refuses.

### A finding about the INSTRUMENT, recorded and deliberately not built

The standing duplication census reads **0 groups / 0 redundant copies / 0
redundant lines** on this tree, while this pass confirmed a real repeated
behaviour.

fig: cmd="python project-trajectory/scripts/check_dupes_census.py --root ." rev=64e9bf2a

No fault in the census: it hashes function **bodies**, so it measures *textual*
duplication, and every family here is *structural* — the same behaviour written
differently in three to five places, which body-hashing cannot see by
construction. **That is the blind derivation's measurable value over the standing
instrument**, and it is worth knowing before anyone reads a zero census as "no
duplication". Not filed as a WI: the remedy is not obvious, and the census's own
header routes changes through the owner on `D-7`'s strength, where an over-eager
duplication gate was torn down after 93% of its findings proved to be accepted
idioms. Proposing a mechanism here would be design-by-speculation on a surface
the owner has already burned once.

### `OI-64` — the requirement gap goes to the owner, not to the queue

The zero-SR module both teams derived is the one bucket-3 finding, it is not
among the twelve, and it is not a layout question. The
finding/severity/strict-escalation/vacuity/exit-composition contract is restated
in 11–13 rows and stated by none — with `SR-158` declaring itself unsatisfied
for want of a declaration surface no row owns. Two adjacent restatements are
folded into the same row so a ruling does not produce three partial ones:
"naming the at-fault row and cell" (15 phrasings) and "every degrade is named,
never silent" (8 rows, SN-008's honesty property), plus vacuity (8 rows).

Four options; recommended **(c) then (a)** — measure whether the shipped
checkers honour ONE contract before minting a row that might land red, since
that is (a)'s single unanswered question and it is cheap to answer in the
already-twice-run measure-don't-rewrite shape. **No module work was filed
against it**, and the row says so explicitly, so a later reader cannot mistake
it for a deferred refactor.

### Gates

```
python -m pytest -q -n auto -m smoke        -> 1327 passed, 5 skipped
python scripts/check_smoke_budget.py --mode enforce
                                            -> within the 60s budget
python project-trajectory/scripts/check_docs.py --root . --stale   -> 0 broken
python project-trajectory/scripts/check_trajectory.py --root . --strict -> clean
python project-trajectory/scripts/trace.py --root . --strict       -> integrity=0
the generated-artifact --check gates        -> all fresh
```
fig: cmd="each command as written above, run in this order on this tree" rev=64e9bf2a-dirty

**Registry-and-docs slice, and the full unfiltered suite is NOT claimed.**
Nothing executable changed: the diff is one open-item row, one queued WI spec,
one plan document, the program spec's slice block, this fragment, the working
surface and the watermark. No script, no test and no spine cell was touched.
Watermarks `OI` 63 → 64 and `WI` 518 → 519 via `trace.py --bump-ids`.

### Scope honesty

`WI-508` is **not complete** and is not claimed to be. What remains is named on
the row: the un-read dispersion families, routing the fusion set to the
size-ratchet debt rather than re-deriving it, `OI-64`'s ruling, and the two
inherited items (the ratchet's debt pointer still names this row; M-06's four
test monoliths are still unsplit).
