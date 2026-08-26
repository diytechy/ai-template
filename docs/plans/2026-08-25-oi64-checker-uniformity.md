# OI-64 (c): do the shipped checkers honour ONE finding/severity/exit contract?

**The measurement OI-64's option (c) asks for, run and filed. Nothing was
edited: no checker, no registry cell, no severity.** The row stays `pending` —
this record answers the one question its recommendation calls decisive and
cheap to answer, and hands the ruling back with numbers instead of an estimate.

> The question, from OI-64's own option (c): *"measure whether the shipped
> checkers actually honour one contract — the severity words in use, whether
> every finding names a location, what each does with an absent optional
> input — and file the numbers."*

---

## The answer in one line

**The PROTOCOL is honoured; the VOCABULARY is not.** Every checker separates an
advisory from a gating finding and none lets an advisory reach the exit code;
89% of finding sites name their location and every exception is either
structural or enumerable. But the same four dispositions are spelled with
**12 different label words**, promoted by **6 differently-named flags** (with
four checkers carrying no promotion path at all), printed to stdout by some
checkers and stderr by others. A row stating the PROTOCOL would land green
today. A row stating a CLOSED SEVERITY VOCABULARY would land red on every
checker at once.

---

## Method, and what it is not

Two passes over the delivered harness, source and behaviour:

1. **Site census.** An AST walk over each module rendered every
   `x.append(<string>)` and `print(<string>)` call to its text shape (f-string
   and `.format` placeholders preserved, so a reader can see whether a location
   is interpolated). **430 sites** extracted. Every extracted site was then READ
   and classified; the classification's rules and its by-site exceptions are
   listed below, so the counts are auditable without re-running anything.
2. **Behavioural drive.** Every checker run twice — once on an EMPTY root (the
   absent-optional-input probe) and once on this repo — recording the exit code
   and what it printed.

<!-- fig: cmd="python project-trajectory/scripts/<checker>.py --root ." rev=fc8a0edc -->

**What this is not.** It is a read of THIS repo's shipped
`project-trajectory/scripts/`, on one box, at `fc8a0edc`. It measures what the
checkers DO, not whether each disposition is the RIGHT one — a WARN that ought
to be an ERROR reads here as a WARN honoured consistently. The site counts are
exact; the severity-word count is exact for label position
(`<script>: <TOKEN>`) and deliberately ignores the same words appearing inside
prose.

**Population: 14 shipped checkers**, plus the two rule libraries that feed
`trace` and own no exit code of their own (`coherence.py`, `trace_text.py`) —
counted for findings, not for exit policy. `check.py` is the composer, not a
checker, and is read here only for how it wires promotion.

---

## Axis 1 — the severity words in use

**12 distinct label tokens** carry what are, in every checker's own account,
four dispositions: passed / not applicable / advisory / gate.

| disposition | words in use |
|---|---|
| passed | `OK` (9 checkers), `clean` (4: `check_need_form`, `check_vocab`, `check_trajectory`, `check_privacy`) |
| not applicable | `SKIP`, `skipped`, and an unlabelled sentence (`check_vendored: no manifest at …`) |
| advisory | `WARN`, `WARNING (advisory)`, `ADVISORY`, `UNTRACED`, `note`, `hint` |
| gate | `FAIL` (6 checkers), `ERROR` (3), `FINDING (<class>)` (`trace`) |

Two checkers reason about this in their own source, which is why the split is
worth measuring rather than normalizing by fiat. `check_doc_refs` calls its
third word deliberate: *"A THIRD ink, because this module's other two both mean
something else: `WARN` gates under --strict, `UNTRACED` is hidden unless asked
for. An ADVISORY never gates and is never hidden."* `trace` uses a scheme no
sibling uses — `FINDING (integrity):` / `WARNING (advisory):` — because its
findings are CLASSED, not merely severed.

**Where a finding is printed is not uniform either.** Seven checkers never
write to stderr; `check_trajectory` writes 18 of its 21 prints there; `trace` 4
of 16, `check_privacy` 5 of 11, `check_doc_refs` 3 of 6.

**Exit alphabet: 0 and 1 everywhere.** The only `2` from a checker's own code is
`check_privacy`'s *"git diff --cached failed (not a git repo?)"*; the other `2`s
are argparse's.

## Axis 2 — does every finding name a location?

Of the 430 emission sites: **177** build an artifact or a data list (report
tables, approval briefs, mermaid, markdown blocks), **40** are renderers that
print a finding another site produced, **55** are summary or status lines —
leaving **158 per-finding emission sites**.

| | sites | share |
|---|---|---|
| **names a location** (row id, `file:line`, file, or module path) | **141** | **89.2%** |
| **population-level** — no single location exists by construction | 11 | 7.0% |
| **thin** — a location exists and the finding does not name it | 6 | 3.8% |

| checker | names | population | thin |
|---|---|---|---|
| `trace.py` | 59 | 2 | 0 |
| `check_trajectory.py` | 30 | 7 | 3 |
| `trace_text.py` | 18 | 0 | 0 |
| `coherence.py` | 8 | 0 | 0 |
| `check_doc_refs.py` | 7 | 1 | 0 |
| `check_docs.py` | 5 | 0 | 2 |
| `check_flows.py` | 5 | 0 | 1 |
| `check_need_form.py` | 2 | 0 | 0 |
| `check_vendored.py` | 2 | 0 | 0 |
| `check_figures` / `check_perf` / `check_privacy` / `check_stubs` / `check_vocab` | 1 each | 0 | 0 |
| `check_dupes_census.py` | 0 | 1 | 0 |

**The 11 population-level sites, enumerated** — each is a count or a set over
the whole corpus, so there is no at-fault row to name: `trace`'s SR→boundary
coverage and hat coverage; `check_trajectory`'s uncited-IF-seam count, its three
`if-tc-coverage-allow` hygiene lines, its uncontained-module and top-view
breadth findings, and its phase-drop stand-down; `check_doc_refs`' non-Python
`Module` advisory; `check_dupes_census`' baseline-vs-measured line.

**The 6 thin sites, enumerated** — a location exists and the finding does not
name it: `check_flows.py:194` (*"diagram {n} cites no SR/LLR id"* — the ordinal,
never the doc path), `check_trajectory.py:512` (malformed WI id, no file/line),
`check_trajectory.py:2341` (the phase, not the anchor row),
`check_trajectory.py:1916` (the import edge, not the importing `file:line`),
`check_docs.py:591` and `:596` (the README/registry inventory findings name the
file, never the line).

**This is the axis a stated contract could hold today**, provided it carves out
population-level findings. Without that clause the row lands red on 11 sites
that cannot be fixed, only re-worded.

## Axis 3 — an absent optional input

Every checker driven on an EMPTY root:

<!-- fig: cmd="for f in check_*.py trace.py; do python $f --root .; done  # run in an empty directory" rev=fc8a0edc -->

| behaviour | count | checkers |
|---|---|---|
| **exit 0 and NAMES the absence** | **12** | `check_coverage` (*"no per-module coverage floors declared"*), `check_doc_refs` (*"no symbol inventory … the sym: tier is skipped"*), `check_docs`, `check_dupes_census`, `check_figures`, `check_need_form`, `check_perf`, `check_privacy` (`--repo`), `check_stubs`, `check_trajectory` (*"vacuously clean"*), `check_vendored`, `check_vocab` |
| **exit 1 on the absence** | 1 | `check_flows` — *"FAIL - docs\runtime-flows.md does not exist"*. Declared, not accidental: the doc is REQUIRED from `DevStg-Tests` and this checker has no warn tier at all |
| **exit 0, but not vacuously clean** | 1 | `trace` — emits `FINDING (integrity): docs/id-watermark is missing` on an empty tree, exits 0 without `--strict`, exits 1 with it |

**Vacuity is the best-honoured axis: 12 of 14 pass vacuously AND say so**, which
is the harder half of the clause — a silent vacuous pass is the fail-open the
corpus warns about everywhere else. Two further observations from the same
drive, neither of which any row today would catch: `check_privacy` in its
default staged-diff mode exits **2** in a non-git directory where `check_docs`
prints *"staleness check skipped (git unavailable or not a git work tree)"* and
continues — one class of environment absence, resolved three ways (fatal /
named skip / named skip); and `trace` WRITES `docs/test/report.md` into the tree
as a side effect of a plain check invocation.

## Axis 4 — strict-mode escalation

**Six spellings, four checkers with none, and two per-row mechanisms.**

| mechanism | checkers |
|---|---|
| `--strict` promotes warn → gate | `check_doc_refs`, `check_figures`, `check_need_form`, `check_stubs`, `check_vendored`, `check_vocab`, `check_trajectory`, `trace` |
| `--strict` accepted and **inert by declaration** | `check_dupes_census` — *"accepted for the [step:] convention's uniform shape; never changes the exit code — this check is warn-first forever (D-7)"* |
| a differently-named flag | `check_docs --strict-orphans` (one class only), `trace --strict-integrity` / `--strict-schema`, `gen_arch_map --strict-backlinks` |
| **no promotion path** | `check_coverage`, `check_flows`, `check_perf`, `check_privacy` — each gates by default instead |
| **per-row declared severity** | `check_perf`'s `Gate=fail`/`warn` per budget; `check_trajectory`'s per-rule `hard` flag (`if hard or args.strict`) |

`trace` is the outlier in the other direction: **nothing** gates without
`--strict` — an integrity finding on a live registry exits 0 unless the caller
asked for the promotion. `check.py` is what makes this coherent in practice,
wiring the promotion per step and per rung; nothing but `check.py` knows the
whole map.

## Axis 5 — declared carve-out markers

Three shapes, and the only axis that was recently MADE uniform:

- **5 declared allow-FILES** — `docs/orphans-allow`, `docs/need-form-allow`,
  `docs/provenance-allow`, `docs/kernel-modules-allow`,
  `docs/if-tc-coverage-allow` — in 3 grammars (` — `-separated token+reason;
  glob lines; seeded burn-down list).
- **In-line markers**, one spelling each: `check_vocab: allow` /
  `check_vocab: allow-file`, `privacy-ok`, `<!-- sn-inventory: off -->`,
  `source`/`sink` in an IF row's `Notes`, `<actor>` on an endpoint.
- **Config dials**: `docs/process.toml [checks]` per-layer off switches.

**PARSE HONESTY IS UNIFORM ACROSS ALL FIVE FILES** — WI-519 finished that, and
it is the strongest evidence in this measurement that a shared protocol is
already understood: every reader reports the FIRST unreadable declaring line
with the count and the grammar, located at `file:lineno`, instead of dropping it
silently. The SEVERITY differs per host and each states why in its own
docstring — `trace`'s is integrity-class *"because … the always-on floor is the
only pipe that runs at every gate"*, while `check_trajectory`'s kernel-allow
rides `components_check` *"rather than the always-on floor"*. **One protocol,
per-row disposition** — precisely the shape OI-64's recommendation argues is
statable.

## Axis 6 — how findings compose into an exit code

**No advisory reaches an exit code anywhere in the harness.** `trace.exit_code`
composes from named finding classes only, and the advisory bags are absent from
it by construction; `check_trajectory` routes `(rule, hard, msg)` triples and
prints anything neither hard nor promoted; `check_doc_refs`, `check_docs`,
`check_dupes_census`, `check_trajectory`, `trace`, `trace_text` and
`gen_open_items` carry the phrase *"never the exit code"* (or *"never
gating"*) **25 times** across 7 modules.

<!-- fig: cmd="grep -rhoE 'never the exit code|never gating|never changes the exit code|never joins a failure' project-trajectory/scripts/*.py | wc -l" rev=fc8a0edc -->

That phrase, repeated across seven modules written at different times, IS the
unwritten contract OI-64 says has no subject.

---

## What this means for the four options

**It answers the one question OI-64 called decisive**: (a) would NOT mint a
requirement the delivered harness fails — on three of its four clauses. Stated
clause by clause, as a row would have to state them:

| the clause | lands |
|---|---|
| a finding names its location | **green**, with an explicit carve-out for population-level findings (11 sites) and 6 thin sites to fix — enumerated above, each a one-line edit |
| an advisory never reaches the exit code | **green**, unanimously, and already stated in the corpus's own words 25 times |
| an absent optional input is vacuous and says so | **green** for 12 of 14; `check_flows`' hard failure is a DECLARED gate obligation rather than a defect and would be named as one; `trace`'s empty-tree integrity finding is a true finding, not a vacuity breach |
| a severity class comes from a closed vocabulary | **RED on every checker** — 12 words for 4 dispositions, before any question of which word is right |

So the honest report is neither "green" nor "ragged" but **three green and one
red, and the red is the cheapest kind**: no behaviour has to change to satisfy
it, only spellings, and the vocabulary a row would close over does not exist
yet because no row has ever had to name it. That is a fact about authoring, not
about the harness being wrong.

**What the measurement does NOT settle, deliberately.** The owner's direction of
2026-08-25 puts the mint target at the INTERFACE tier — *"either the interface
contract (wherever it lives) defines the interface expectations, or the LLR
does"* — and **where interface contracts live is itself unruled**, sitting in
OI-63's re-ask after that row's (d) cleanup. A protocol contract minted before
that re-ask would be minted into a home the owner may move. Whether that
sequencing matters, or whether the protocol is statable independently of where
contracts end up living, is the owner's call and is not prejudged here.

**Filed, not ruled.** OI-64 stays `pending`.
