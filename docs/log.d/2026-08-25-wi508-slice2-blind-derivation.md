## 2026-08-25 — WI-508 slice 2: the blind derivation runs on two axes, and both teams disclose the same breach

**Summary.** The program's central instrument executed. Two agents derived the
minimal module map from a five-file input set — purpose statement, needs,
requirements, depth-0 frame, hat roster — with the design tier, the component and
interface registries, the process masters and the source tree all held out. The
brief was written and committed to a plan document **before** either ran. Team A
worked backwards from the declared boundary outputs and returned **24 modules**;
Team B clustered obligations by shared signal and failure mode and returned
**23**. They agree on **97.2%** of SR pairs, and the biggest result is one
neither axis could have produced alone. **Nothing is adjudicated against the live
layout here** — that is slice 3, and it is the only role permitted to read both
sides.

Deferred open items: none — a derivation commissions no act. The one thing it
DOES commission is a method correction, and it is this row's to carry, not the
owner's: see the disclosure below.

### The disclosure comes first, because the exercise's value depends on it

Neither agent read a byte of this repository, and both said so with the evidence:
every read confined to the pack by absolute path, and both noting that a
relative path would have landed inside the live repo since that is the working
directory. **Both then disclosed, independently and unprompted, the same
limitation:** the harness injected this repository's own instruction file — and
for Team B a memory index as well — into their context BEFORE the brief arrived,
naming directories and several script filenames.

That is a real weakening of the contract and it is recorded rather than
discovered later. What can be said precisely: the contamination is **names, not
structure**; both checked their module names against the injected material and
neither reproduced a filename as a module name; Team A additionally named four
places its map DIVERGES from what recall would have produced, each argued from
requirement text; and both recorded declining the same shortcut — the boundary
registry's `carries` cell enumerates delivered script names, and using it as the
module list was available to both and taken by neither.

**The method finding, owned by this program:** a future run of this instrument
must strip the harness context, not only the input set. Convergence between A and
B is slightly less independent than it looks. It is not worthless — a file list
is not a module map — but the claim must be stated at its true strength.

### What came back

| | Team A (outputs-backward) | Team B (obligations-clustered) |
| --- | --- | --- |
| modules | 24, in 6 layers | 23, in 4 bands |
| mean SRs per module | 3.1 (max 7) | 3.3 (max 8) |
| modules owning no SR | 1 | 1 |
| SRs resisting single ownership | 13 | 11 |
| requirement-level overlaps found | 13 | 14, plus 5 obligations with no SR subject at all |

Both defended their count against the same temptation — a smaller map is always
reachable by fusing — and both refused it in writing on the objective's own
terms. Team A: the six-way split the boundary registry hands over "reads better
and scores worse", because six carriers each consuming the same five foundation
signals is thirty implementations of five. Team B: its count is held DOWN by
three extracted shared stages rather than by fusion, and removing them yields "a
smaller module count and a strictly larger system". That is *calls, not lines*
applied by two agents who were told the phrase and then had to use it.

### Agreement, measured

Over all **2,775** unordered pairs of the 75 SR ids the two maps agree on whether
a pair shares a module in **97.2%** of cases (72 together in both, 2,626 apart in
both, 33 together only in A, 44 only in B). The best one-to-one module
correspondence pairs **22 of A's 24 with 22 of B's 23** and places **63 of 75
(84.0%)** identically.

fig: derived="pairwise co-membership over all 2775 unordered pairs of the 75 SR ids, plus a greedy best 1:1 module correspondence, computed from the two forward-assignment tables in the recorded returns; reproduction script in the record's §7"

**The headline convergence is invisible to that arithmetic**, because it cannot
be matched on SR overlap: Team A's `F5` and Team B's `M03` **own zero SRs each,
and are the same module** — one home for the shape of a finding, its severity
class, strict-mode escalation, vacuity, and how findings compose into an exit
code. Two opposite axes independently invented it, and independently found that
**no requirement states it** while eleven to thirteen rows each restate a
fragment. `SR-158`'s own acceptance concedes the hole in the corpus's words: *"A
class whose severity is stated at no declaration site is undeclared, and this row
is unsatisfied until it is declared there."*

**That is a missing requirement, not a layout defect**, and it must not be filed
as module work. Team B drafted the missing row's shape; the record carries it.

The one module with no counterpart at all is Team A's `F3` — every question
answered by reading version control, asked once. Team B distributed those reads.
Team A flagged its own thin ownership (one row, nine consumers) as a corpus
finding of the same shape as `F5`.

### `SR-163` split the two teams on exactly the seam slice 1 had just written

A assigned it to the spine-join checks; B to the package manifest. That is
`LLR-204` against `LLR-203` — the join against the inventory. Two agents that
could not see the registry cut along the same line the decomposition did, which
is the strongest available evidence that slice 1's two rows are a real boundary
rather than a convenient one.

### The twelve divergences are INPUTS, not findings

`SR-006`, `SR-015`, `SR-019`, `SR-020`, `SR-024`, `SR-033`, `SR-043`, `SR-111`,
`SR-113`, `SR-163`, `SR-173`, `SR-174`. Each marks a place the requirements
underdetermine the boundary — is the hook the module or the classifier; does an
invariant live with its checker or with what it measures; does the scaffold write
a value it did not compute. The record states the question under each. The
instruction they carry into slice 3: **a live divergence where A and B AGREED is
stronger evidence than one at a point where they split.**

### What both teams found about the REQUIREMENTS

Convergent, reached from both axes: the finding/severity/exit contract has no
subject; derived-copy currency is stated seven or eight times under five names;
refuse-rather-than-default is stated five to eleven times with only the fail-safe
direction genuinely varying; the interpreter probe is duplicated **by explicit
ruling**, `SR-160` saying so in its own text; sensitive-class scanning has
**already diverged in the field** and `SR-176` records it; measured-value-versus-
baseline is one pipeline with four postures; and two rows state one provenance
record shape, `SR-165` calling itself "the `SR-161` form applied to the partition
instead of the perspective set".

Team B's axis additionally surfaced what a per-capability decomposition
systematically misses — a clause everywhere and a subject nowhere: "every degrade
is named, never silent" (8 rows), vacuity of an absent optional input (8 rows),
all-or-nothing durable writing (5 rows, 5 mechanisms), and the pair-level claim
the local floor and the hosted re-run make only together. It also lists five
obligations stated in a need or the frame with no SR subject at all.

### Deliverables

- [`docs/plans/2026-08-25-blind-minimal-map-brief.md`](../plans/2026-08-25-blind-minimal-map-brief.md)
  — the question, recorded before the answers: the objective in the owner's
  words, the research grounding, the closed input set with a per-file reason for
  every inclusion AND exclusion, the two axes, the required return shape, and
  what the derivation is NOT.
- [`docs/plans/2026-08-25-blind-derivation-a-outputs.md`](../plans/2026-08-25-blind-derivation-a-outputs.md)
  and
  [`-b-obligations.md`](../plans/2026-08-25-blind-derivation-b-obligations.md)
  — both returns verbatim, unedited.
- [`docs/plans/2026-08-25-blind-minimal-map-derivation.md`](../plans/2026-08-25-blind-minimal-map-derivation.md)
  — the record: the disclosure, the two maps at a glance, the measured agreement
  with its reproduction script, the twelve divergences with the question under
  each, the convergent requirement-level findings, what is NOT concluded, and
  two instructions for the alignment pass.

### Gates

```
python -m pytest -q -n auto -m smoke        -> 1327 passed, 5 skipped in 60.46s   [--basetemp=D:\tmp\pytest-wi508]
python scripts/check_smoke_budget.py --mode enforce
                                            -> 1327 passed, 5 skipped in 25.89s
                                               26.3s vs 60s budget -> within      [the declared command]
python project-trajectory/scripts/check_docs.py --root . --stale
                                            -> OK, 1085 docs, 1417 links, 0 broken
python project-trajectory/scripts/check_doc_refs.py --root .
                                            -> 200 dangling, IDENTICAL to the count
                                               measured on a stashed tree at HEAD
python project-trajectory/scripts/check_trajectory.py --root . --strict
                                            -> clean
the five generated-artifact --check gates    -> all fresh
```
fig: cmd="each command as written above, run in this order on this tree; the check_doc_refs baseline by `git stash -u` at 0f8cb9a7, re-run, `git stash pop`" rev=0f8cb9a7-dirty

**A measured environment finding, because it nearly cost a false budget breach.**
The two readings above are the SAME tier on the SAME tree minutes apart, and the
only difference is `--basetemp`. Redirecting pytest's temp root to D: took the
smoke tier from **25.89 s to 60.46 s** — 2.3x, and across the 60 s budget line.
The redirect is a documented workaround for disk pressure on C:, and the pressure
is gone: C: measures **41 GB free**, against the ~1.6 GB the working surface
recorded. Both facts are corrected on `docs/status.md`, because a session that
reaches for the workaround by habit will read a breach that is an artifact of the
workaround rather than of the tier. **The budget was NOT touched in either
direction**; the declared command is what it is calibrated against, and it
measures 26.3 s.

fig: cmd="python scripts/check_smoke_budget.py --mode enforce ; python -m pytest -q -n auto -m smoke --basetemp=D:\tmp\pytest-wi508 ; df -h /c" rev=0f8cb9a7-dirty

**Docs-only slice.** Four plan documents, the WI spec's slice block, this
fragment and the working surface. No registry cell, no script and no test was
touched, so no generated artifact moved and no full-suite run is owed.

### One warn accepted knowingly rather than silenced

`check_figures` warns that this fragment's `fig:` markers carry a DIRTY rev, and
so do slice 1's. They are correct as written: those figures WERE driven on a
working tree, which is what `<sha>-dirty` says. Re-stamping them with a clean sha
to clear the warn would put a false provenance in the record to quiet a check —
the one trade this repo does not make. The checker's advice (commit first, then
re-drive) is right in general and unavailable for a figure that gates the commit
carrying it; 127 of the 429 declared figures in the tree already sit in the same
position.
