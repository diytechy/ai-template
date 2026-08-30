+++
id = "WI-537"
title = "check_complexity.py: a stdlib cognitive-complexity and SLOC census with a TSV baseline, report-only (OI-68 phase 1)"
specref = "docs/plans/2026-08-29-complexity-sensor-plan.md#phase-1--the-sensor-report-only"
workstream = "process"
sr_refs = ["SR-183"]
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Context

**What this row builds.** `project-trajectory/scripts/check_complexity.py`: a
stdlib-`ast` census of every function in the declared source surface, reporting
**cognitive complexity** (SonarSource rules) and **SLOC** per function, plus a
per-module **public-symbol count** that is REPORTED and never gated. The baseline
is a central TSV at `docs/complexity-baseline`. Modes: `--report` (print the
census, always exit 0), `--restamp` (write the current census), `--mode warn`
(the default: compare, report a divergence, still exit 0) and `--mode enforce`
(exit nonzero on any divergence).

**Posture in THIS phase: report-only.** No `[step:]` row, no gate, no arming in
`docs/stack.ini`. The script ships with the enforce capability (exercised by its
own tests) but nothing in this repo runs it as a gate; arming is the opt-in
phase-2 act. The census lands in the log as the measurement the OI-68 ruling is
answered with, re-derived by the shipped script rather than borrowed from the
research prototype.

**Why cognitive and not cyclomatic.** `tests/test_complexity_ratchet.py` already
runs ruff `C901` per function. Cognitive complexity charges an increment per
level of NESTING, which cyclomatic cannot express — the kit's coordinators are
deeply nested rather than widely branched, so the two axes score a population of
functions far apart. The count and worked examples land in the log at close,
measured by THIS script.

**Why stdlib and not a linter.** A shipped check that needs a linter forces every
adopter to install it (`docs/dependencies.md`, the `shipped` tier's own bar). The
C901 ratchet is the demonstration of the cost: it `skipif`s away without ruff and
its baseline is coupled to ruff's counting rules. This script pins its counting
rules in its own docstring, which is what makes its baseline a property of the
code rather than of a tool version.

**The two correctness traps, each owed a test.** (a) `elif` is parsed as a nested
`If` in `orelse`: a naive recursion both double-counts and over-nests every
`elif` ladder — flatten it, and treat the else-branch as +1 flat with no nesting
increment. (b) A `BoolOp` scores **runs of like operators**, not operators:
`a and b and c` is +1, `a and b or c` is +2. A third, kit-specific: a nested
`def` takes a nesting increment and no base increment, so decomposing OUTWARD is
rewarded and nesting inward is not — said in the docstring.

**The baseline file.** `docs/complexity-baseline`, TSV, one row per
over-threshold function, sorted, LF-only, with a header that states its own
stance. TSV rather than TOML/JSON for one reason: minimum merge-conflict surface
when two concurrent sessions each re-stamp. Header columns:
`path`, `function`, `cognitive`, `sloc`, `reason`. **The seeded baseline is a
DEBT STATEMENT, NOT AN APPROVAL** — the same stance `test_module_size_ratchet.py`
took, and the file's own header says so.

**NOT in scope.** Arming (`[step:complexity]` in `docs/stack.ini`) — phase 2.
Retiring any existing sensor (the line ratchet) — phase 2. Shipping downstream
(the `bootstrap.MAPPING` row, the `stack.ini.template` step, the RESYNC entry) —
phase 3. The relative-churn sensor — separate, and unfiled.

**Spine landed (Drafted, owner to approve):** `SR-183` (the requirement),
`LLR-206` (the design), and — because the tests split by tier — `TC-202` (Smoke,
the in-process metric) and `TC-203` (Full, the CLI drives). The census seed reads
179 functions over cognitive 15 across `project-trajectory/scripts/**/*.py`.

**REVIEW-A re-affirmation.** SR-183's acceptance was tightened during rework —
its threshold boundary now reads strictly OVER (`>`), aligning it with LLR-206,
the implementation, and the baseline (see the log fragment's REVIEW-A section).
This WI still answers SR-183 as amended: the boundary was always exclusive in the
built code and the seeded baseline; the amendment only makes the SR say what the
LLR and code already said. Scope and deliverable are unchanged.

**REVIEW-A Round 6 clarification.** LLR-206 now names the implementation boundary
exactly: `census()` returns every source-function row, while `main()` selects the
strictly-over (`>`) rows for baseline comparison. This is a contract correction,
not a behavior change. The Round 3/4 iteration records also have their four
reviewer-named trailing spaces removed; the identical empty-field whitespace in
the later Round 5/6 records is removed so the next review range is clean too.
