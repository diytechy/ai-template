+++
id = "WI-430"
title = "Adopt a rule about what a comment may say — 'state the constraint, not its history' — and sweep the repo-lock citation sprinkle it outlaws. The kit had NO rule governing comment CONTENT before this (grepped; AGENTS.template.md ruled on comment DENSITY, freshness and the docstring contract, never on what a sentence may cite), so this is a new standard rather than enforcement of an old one. Part 1 adds the rule to AGENTS.template.md's Working agreement, paid for by tightening. Part 2 reads all 98 repo-lock citation sites in project-trajectory/scripts/**.py and tests/**.py, classifies each as CONSTRAINT (a reader could undo the rule without noticing) or PROVENANCE (the sentence survives deleting the parenthetical), deletes the provenance citations while KEEPING their sentences, and concentrates what remains into one header pointer per module. This is finding F-10 recurring: history sentences spend brief budget without constraining behaviour, and plan_briefs.IF_SURFACE_COLUMNS carries Contract cells verbatim into planning briefs, so the path from a sprinkled citation to a polluted prompt is real."
workstream = "scripts"
specref = ""
buildtier = "medium"
safety_class = "normal"
+++

## Deliverable

**DONE 2026-08-11.** Both parts executed. **98 citations → 15**, and the count
is the least interesting number here: *no sentence was deleted*, which was the
row's one hard constraint.

### Part 1 — the rule, and the honest note that it is NEW

Added to `project-trajectory/AGENTS.template.md`, **Working agreement**,
verbatim:

> - **State the constraint, not its history.** Cite a decision record only where
>   a reader could plausibly undo it — **at most once per module**, a header
>   pointer, never a per-site sprinkle. Provenance belongs in the archive.

**The kit had no rule about what a comment may say.** Grepped before writing:
`AGENTS.template.md` ruled comment *density* ("comment generously and
deliberately"), comment *freshness* ("a comment is a promise — keep it true"),
and the *docstring contract* ("cite requirement ids instead of restating
constraints") — but nothing about whether a sentence may carry a decision id.
So this is a **new standard**, not the enforcement of an old one, and the sweep
below is its first application rather than a backlog of violations.

Note the one place it brushes an existing rule and does **not** contradict it:
"cite requirement ids instead of restating constraints" is about **live join
keys** (`SR-014` is a row a caller can look up and the harness validates);
this rule is about **decision records** (`D-5` is a settled argument). The kit
wants the first and not the second.

**The mirror into this repo: none is owed, and that is the dogfooded answer.**
This repo's `AGENTS.md` is a *stub* pointing at `CLAUDE.md` (the documented
inversion — the kit ships the opposite convention downstream), and
`CLAUDE.md`'s *Communication style* section is a digest that ends with an
explicit pointer: *"The shipped guide states the full version —
`project-trajectory/AGENTS.template.md` 'Working agreement'."* The rule landed
in that full version, so it already governs work here through a pointer rather
than a fifth paraphrase. `tests/test_dogfood_sync.py` was checked and **does
not govern `AGENTS.md` at all** (no reference to it anywhere in the file), so
there is no structural divergence to obey — the only AGENTS assertions in the
suite are `test_bootstrap.py`'s byte budget and its stubs-point-at-AGENTS.md
scaffold check, both unaffected.

### The byte budget — the rule was added at effectively net zero

`AGENTS.template.md` **9,989 → 9,991 bytes (+2)**, against a hard 10,000
budget: **9 bytes of headroom**. The file was at 9,989 *before* this WI, so the
rule (+235 bytes) had to be paid for in full. Where it was paid, all of it
meaning-preserving:

| tightening | saved |
|---|---|
| the subagent sentence — an *unmarked paraphrase of `PROCESS.md` §6*, which the same bullet already cites; the pointer stays, the three restated patterns go | ~135 |
| the gates bullet's `; default: pause for human approval` — a dial's default restated outside `docs/process.toml`, its one home | 35 |
| the contract prose (`keys read + …` → `keys + …`; `that already live in an SR (its …)` → `already in an SR (…)`) | ~24 |
| "the bar is that a reader never has to" → "a reader must never have to" | 17 |
| the session bullet's reflow (`the *Current State* header of` → `*Current State* in`) | ~16 |
| three one-word trims (`A small experiment` → `An experiment`; `markers, and never` → `markers; never`; `green, per` → `green per`) | 11 |

`PROCESS.md` **64,466 → 64,466 (unchanged)**. `PROCESS_OPTIONS.md`
**170,454 → 170,454 (unchanged)**. No baseline re-stamp owed.

### Part 2 — the sweep, and what reading 98 sites actually showed

**The 7/59 heuristic was wrong, and wrong in the direction that matters.** It
undercounted constraint by roughly half. Read site by site, the scripts split
**~12 constraint / 57 provenance** (not 7/59), because the heuristic keyed on
whether a *sentence* states a rule, and missed a class it has no signal for:
**obligation markers**. `intake.py`'s `# THE ANCHOR IS STILL OWED HERE`,
`spine_carrier.py`'s `(Owner ruling owed — …)` and `check_trajectory.py`'s
`RESERVED, NOT DEAD … has no writer yet` are not history and not constraints
either — they are **live unfinished business** parked at the line where it must
land. Deleting their citations as provenance would have been the real damage,
and a purely mechanical sweep would have done exactly that.

The 57 provenance sites were, as predicted, almost entirely one sentence
repeated: `# Through the CARRIER (repo-lock D-5): …` and
`# Sibling: the spine's registry CARRIER (repo-lock D-5/D-6) — …`. The second
form appeared in **11 module headers verbatim**. Every one of those sentences
names `spine_carrier.py` — the module whose own docstring holds the full
argument — so the citation was a second pointer to a place the sentence
already pointed.

**No sentence was deleted.** The row's hard constraint held: 98 parentheticals
removed, zero explanatory sentences lost. Six sites needed a small rewrite so
the sentence carried its constraint plainly once the id was gone (e.g.
`trace.py`'s `not for tidiness (repo-lock D-5, "the one thing that must not be
forgotten")` → `not for tidiness — this is "the one thing that must not be
forgotten"`, keeping the phrase that names the hazard).

#### Before → after, per file

| file | before | after | kept |
|---|---|---|---|
| `scripts/trace.py` | 11 | **1** | the `# --- the spine carrier (repo-lock D-5/D-6) ---` section banner |
| `scripts/check_trajectory.py` | 10 | **1** | the `# WHAT SURVIVED THE LEDGER (D-1)` banner over the reserved digest engine |
| `scripts/intake.py` | 9 | **1** | `# THE ANCHOR IS STILL OWED HERE (D-1)` — an open obligation, not history |
| `scripts/spine_carrier.py` | 4 | **1** | the module docstring header `(OI-12 / docs/repo-lock.md D-5)` |
| `scripts/gen_okf.py` | 4 | 0 | |
| `scripts/check_docs.py` | 3 | 0 | |
| `scripts/check_flows.py` | 3 | 0 | |
| `scripts/derive_gate.py` | 3 | 0 | |
| `scripts/migrate_carrier.py` | 3 | **1** | the module docstring's `(repo-lock Q11)` — what it deliberately does NOT do |
| `scripts/plan_artifacts.py` | 3 | **1** | the header `# both mints … never from max(live) (repo-lock D-4)` |
| `scripts/bootstrap.py` | 2 | 0 | |
| `scripts/check_doc_refs.py` | 2 | 0 | |
| `scripts/gen_release_checklist.py` | 2 | 0 | |
| `scripts/plan_coverage.py` | 2 | 0 | |
| `scripts/traj_parse.py` | 2 | 0 | |
| `scripts/traj_views.py` | 2 | 0 | |
| `scripts/agent_loop.py` · `gen_cases.py` · `integrate.py` · `plan_briefs.py` | 1 each | 0 | |
| **scripts total** | **69** | **6** | |
| `tests/test_module_size_ratchet.py` | 6 | **6** | **fenced** — see below |
| `tests/test_trajectory_staged.py` | 4 | 0 | |
| `tests/test_rule_sync.py` | 3 | **1** | the module docstring — this file *is* the F5 rule's live home (D-7) |
| `tests/test_attestation_digest.py` | 2 | **1** | the module docstring `(D-1)` — the subject of the file |
| `tests/test_check_docs.py` · `test_dogfood_sync.py` · `test_spine_carrier.py` · `test_trace_rules.py` | 2 each | 0 / 0 / **1** / 0 | `test_spine_carrier.py`'s docstring header `(D-5/D-6, SR-147)` |
| `tests/conftest.py` · `test_dual_plan_round.py` · `test_gen_cases.py` · `test_intake.py` · `test_plan_artifacts.py` · `test_trace.py` | 1 each | 0 | |
| **tests total** | **29** | **9** | |
| **TOTAL** | **98** | **15** | |

Every survivor is a **module docstring, a section banner, or an obligation
marker** — none is a per-site sprinkle, which is the shape the rule asks for.

#### The four keeps that are not module headers, and why each earned it

1. **`plan_artifacts.py:57`** — `both mints below count from the MARK, never
   from max(live) (repo-lock D-4)`. This session watched `plan_artifacts` get
   "simplified" back to `max(live)+1`; the citation is the evidence that stops
   the next override. The two per-site D-4 repeats beneath it were dropped —
   their sentences ("`max(live) + 1` re-issues the number of any round that has
   been DELETED") already defend themselves.
2. **`intake.py:1398`** — the anchor is *owed*, at the line that owes it.
3. **`check_trajectory.py:3075`** — the digest engine has no writer yet and a
   dead-symbol sweep must not delete it. A record that a thing is deliberately
   unfinished is not provenance.
4. **`migrate_carrier.py:27`** — the module docstring's list of what the
   converter deliberately does NOT do. "Finishing the job" here would launder
   38 rows' re-blessing; the id is the record that not-finishing was ruled.

### The hard fences — obeyed, and accounted for

**`docs/requirements/*.toml` — the three spine registries, untouched.** Editing
ratified row text is a spine amendment, which is sitting territory. Exactly
**one citation each**, all left in place:

| file | site |
|---|---|
| `system-requirements.toml:1686` | inside `SR-…`'s `rationale` (the attestation-ledger retirement) |
| `low-level-requirements.toml:1689` | inside `LLR-…`'s `rationale` (None-vs-`{}`, absent-vs-empty) |
| `stakeholder-needs.toml:2` | the file's **header comment** naming the carrier it replaced |

The third is a header comment rather than row text and so was *technically*
sweepable, but it sits in a fenced file and moving it buys nothing — left with
the other two rather than reaching across the fence for one byte.

**`docs/requirements/interfaces.csv` — DEFERRED TO OI-14, counted not swept.**
**11 rows** of 110 carry a `repo-lock` citation, and here they are so OI-14
inherits the work rather than re-deriving it:

```
IF-102  IF-104  IF-105  IF-106  IF-107  IF-108  IF-109  IF-110  IF-111
IF-116  IF-117
```

Not edited. OI-14 is going to rewrite what a `Contract` cell *contains*, so
sweeping now would mean sweeping twice — and these 11 are the F-10 path
itself: `plan_briefs.IF_SURFACE_COLUMNS` carries `Contract` verbatim into
planning briefs, which is where a decision reference becomes prompt text.

**`tests/test_module_size_ratchet.py` — all 6 kept, and the reason is
categorical.** Its citations are ratchet **reason** fields: each records that a
specific size bump was reviewed and what authorised it. **The reason IS the
record** — the file is an explicitly dated changelog whose entire content is
provenance, so the rule ("provenance belongs in the archive") does not apply to
a file that *is* the archive. Deleting the ids there would destroy the only
evidence that a threshold move was sanctioned.

One honest wrinkle, recorded rather than fixed: its line 945 says
`current_digests` *"carries the repo-lock D-1 pointer"*. That per-site pointer
was swept from `check_trajectory.py`'s `current_digests` docstring — but the
module still carries D-1 at its section banner (line 3075, ~80 lines above), so
the ratchet's claim remains true **at module scope**, which is the scope the
new rule operates at. Left alone under the fence.

**`docs/log.md`, `docs/archive/**`, `docs/work/complete/**`** — untouched, per
the `check_doc_refs` doctrine: a historical document naming a decision is
accurate history. **`docs/repo-lock.md`, `docs/plans/**`,
`OWNER_SCRATCHPAD.md`** — not this row's. **`docs/status.md`,
`docs/architecture.md`, `docs/okf/**`** — generated, regenerated rather than
hand-edited (below).

### Generated surfaces — regenerated, because docstrings moved

`gen_arch_map.py` harvests the **first line** of every docstring, which is
precisely where several of these citations sat, so the sweep is visible in the
map. `trunk_step.py --regen` re-derived all six document families; the moved
surfaces are `docs/architecture.md` (3 summary cells), `PROJECT_STATE.html`
(1 line), and `docs/gate` (its `as-of` stamp only — **the gate itself is
unchanged at G1**, and the basis counts `SN=29 SR=146 LLR=149 TC=146` are
identical, which is the point: a comment sweep must not move the gate).
`docs/okf/` and `docs/status.md`'s generated block came back byte-identical.
Every `--check` mode left fresh.

### Verification — and one failure that is NOT mine

```
$ pytest -q -n auto
1 failed, 2257 passed, 5 skipped in 382.77s (0:06:22)
```
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=4d0b3470 -->

**Reconciling against the stated baseline (2258 passed, 5 skipped).** The
population is identical — `2257 + 1 + 5 = 2263 = 2258 + 5`. One test flipped
pass → fail, and it is
`test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans`:
`docs/spine-restructure-2026-08-08.md` has no path from an entry root.

**Proven pre-existing rather than argued.** The test was run on a **detached
worktree at clean `HEAD` (4d0b3470)**, with none of this WI's changes present:

```
$ pytest tests/test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans -q
1 failed in 0.51s          # detached worktree @ 4d0b3470, clean
```
<!-- fig: cmd=".venv/bin/python -m pytest tests/test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans -q" rev=4d0b3470 -->

The cause is commit **`81bf474b`** ("repo-lock: perform the collapse-to-a-pointer
step it always prescribed"), which removed the **only** inbound link to that
doc — `git show 81bf474b~1:docs/repo-lock.md` matches it once, `git show
81bf474b:docs/repo-lock.md` zero times. The two surviving mentions are both
under `docs/work/`, which this test explicitly `--ignore`s. **Surfaced as a
finding, not fixed inline**: the repair is either a re-link from
`docs/repo-lock.md` (not this row's file) or an `docs/orphans-allow` entry
(declaring an absence is an act of acceptance, not a green-making edit). The
stated baseline was measured before `81bf474b` landed.

**Everything else green:**

```
Traceability: SN=29 SR=146 LLR=149 TC=146 orphans=0 integrity=0
              components=5 component-findings=0 interfaces=110 interface-findings=0
```
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/trace.py --root . --strict" rev=4d0b3470 -->

`trace.py --root . --strict` **rc 0**. `check_trajectory.py --root . --strict`
**rc 0** ("clean — 427 work item(s), 405 done (95%), 21 cancelled, graph
acyclic"). `check_docs.py --root . --stale` **rc 0** (0 broken links).
`check.py --jobs 0` → **RESULT: PASS** (gate G1, tier all; the four FAIL rows
are all marked *advisory — not gating* and all pre-existing).
`ruff format --check` → **168 files already formatted**; the single
`ruff check` error is the pre-existing `E741` in `tests/test_id_watermark.py`,
the same one WI-429's entry records, unchanged by this row.

**One measured side-effect worth recording.** `check_doc_refs --strict` reports
**27 dangling at HEAD and 27 after** — the sweep created no dangling pointer,
which is the property that matters. But *untraced* references fell
**1261 → 1237 (−24)**: that is the sweep removing `docs/repo-lock.md` mentions
from code, measured rather than asserted.
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_doc_refs.py --root . --strict" rev=4d0b3470 -->

### Deviations from spec

**One, and it is a placement judgement worth flagging.** The row asked for the
rule "in the file's own voice and keep it tight" — done — but the topical home
for a rule about *what a comment may say* is arguably the file's
**"Comment for humans — and the map"** section, not the Working agreement. It
went in the **Working agreement as instructed**, because the rule's reach is
wider than code comments (it governs docs and spec prose too, and the F-10
finding that motivated it was about **`Contract` cells in a registry**, not
about comments). Recording the alternative rather than silently taking it.

Nothing else deviated: no fence was crossed, no sentence deleted, no file
outside the two declared globs edited except the budgeted guide and the
regenerated surfaces.

## Context

**The owner's mandate, which is the whole of the row's authority:** *"If
someone wants to know the history and the rationale, they should look in the
archive, otherwise it's probably not necessary to sprinkle these everywhere, it
just makes it harder to read."* The specific fear named with it is an LLM
**chasing a citation to a decision that was already made**, and documentation
getting clobbered with decision references.

**Why this is evidence, not taste.** It is finding **F-10 recurring**. F-10
measured the IF `Contract` cells — 27% naming a WI, history outnumbering
everything else in the longest cells — and concluded that history sentences
*"spend brief budget without constraining behaviour, and mix narrative with
normative statement in a prompt."* The mechanism is not hypothetical:
`plan_briefs.IF_SURFACE_COLUMNS` carries `Contract` verbatim into planning
briefs, so a citation written into a cell is a citation read by the next
planner.

**The care point that makes this more than a `sed`.** A citation often sits in
the *only* sentence recording why non-obvious code is shaped the way it is.
This session already watched `plan_artifacts` get "simplified" back to
`max(live)+1` — the exact failure mode — so the row's binding instruction was
**never delete a sentence because it contains a citation**, and where removing
the id would leave a sentence meaningless, rewrite the sentence to carry the
constraint plainly. That is why the sweep was performed by reading all 98
sites rather than by pattern, and why the constraint/provenance split came back
different from the heuristic that scoped it.

**Where the history still lives, undisturbed:**
[`docs/archive/repo-lock-decisions-2026-08.md`](../../archive/repo-lock-decisions-2026-08.md),
and every `D-n` still resolves in [`docs/repo-lock.md`](../../repo-lock.md).
Nothing was made unfindable — it was made un-sprinkled.
