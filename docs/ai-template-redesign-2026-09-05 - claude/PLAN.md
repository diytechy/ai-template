# ai-template redesign — diagnosis, target shape, and an implementation breakdown

**Written 2026-09-05 for separate review, beside the repo and outside it.**
Refers to `ai-template` at trunk `a9bf6cee` (branch `contract_split`). Nothing
here is applied to the repo. Companion evidence files sit in this folder:

- [`A-spine-census.md`](A-spine-census.md) — every SN/SR/LLR/TC/IF classified as
  vision-bearing, loop mechanism, self-description, or rendering.
- [`B-module-map.md`](B-module-map.md) — all 82 modules mapped to the four-stage
  loop, with SLOC, test counts, fan-in/out, and the batch-lane code path.
- [`C-external-tools.md`](C-external-tools.md) — the 2025–26 tool landscape
  against each objective the kit developed on its own.

The owner's framing, which this plan takes as the requirement:

> At the end of the day it's a relatively simple high level loop: WI creation
> (potentially containing contradiction/consolidation from an adjudicator),
> scheduling according to WI, dispatching according to scheduler — one WI per
> lane — and controlled reviews / plan sessions with arbitration when necessary.

---

## 0. The verdict in one page

**The vision is sound and the core that carries it works. The mechanism built
around it has outgrown the vision by roughly an order of magnitude, and it is
now consuming most of the effort the kit exists to save.**

| What | Measured at `a9bf6cee` |
|---|---|
| Kit scripts | 82 modules, 76,337 lines; 38,995 SLOC of code once docstrings and comments are excluded (about half the source is prose) — all stdlib |
| Kit tests | 154 files, 87,679 lines, about 3,255 test functions (3,254 by AST; one is fixture text); 164,016 lines of Python in total |
| Mass by stage (appendix B) | rendering 20.6% · spine tracing 16.1% · the owner's four loop stages together 37.8% · checks 10.9% · merge 6.8% · scaffold 4.3% · migration 3.0% |
| Coupling | the seven loop modules' static import closure (deferred imports included) is 46 of 82 modules, 25,490 SLOC, 65% of the kit's SLOC — a possible-dependency measure, not a measured startup cost |
| Duplication | the `+++` frontmatter fence parsed 7 different ways · `process.toml` parsed raw in 4 places with 3 failure defaults · 7 prompt-composition mechanisms · 8 result/refusal conventions · 57 CLI verbs · 198 accepted complexity-debt rows |
| Spine | 27 SN · 76 SR · 192 LLR · 191 TC · 167 IF seams |
| Of the 192 LLRs (appendix A) | 47 vision-bearing · 63 loop mechanism · 44 self-description · 38 dashboard rendering |
| Of the 167 IF rows | 96 intra-kit function seams · 52 cross a boundary an adopter sees · 19 kit-to-repo-file |
| Of the 191 TCs | 27 assert something an adopter would observe; 164 test the kit's checkers on fixtures |
| Test SLOC vs kit SLOC | 59,966 vs 58,242 — the tests are larger than the product |
| Process prose | PROCESS.md 1,318 + PROCESS_OPTIONS.md 2,767 + RESYNC_PACK.md 4,950 lines |
| Harness plan at DevStg-Impl | 34 steps; 13 generated artifacts each with a freshness check |
| LLR churn since 2026-08-01 | 218 `detail` cells rewritten, 1 row removed; 18 ids ever retired against 192 live — rows are amended in place, not replaced, despite D-4 |
| Render test bill | about 340 tests / 10k lines for 8,036 SLOC that produce no decision; the suite's three slowest tests (68 s, 38 s, 23 s) are wire-routing geometry and run on every commit |
| Skills shipped | 31, of which 16 are domain skills (ROS 2, URDF, Gaussian splats, WebGPU, EKF…) with no relation to a process kit |
| Commits since 2026-06-04 | 3,510 — about 40 a day; kit-script churn Aug–Sep +61,305 / −22,174 lines |
| WIs merged since 2026-08-15 | 48 by category: 21 builds, 12 dispositions, 10 adjudications, 5 spot-checks — a count of kinds, not a measure of wasted effort (recorded cost: builds about $339, the other three about $304, with batched lanes double-counted) |

Three facts drive the recommendation:

1. **The loop feeds on itself.** More than half the work items the loop
   completes, by count, are judgements about its own previous work (amendment
   adjudications, disposition drafts, clean-close spot checks), and each mints
   successors. That is a category count, not a measured waste fraction — the
   recorded cost of the 27 is comparable to the 21 builds, not larger. What is
   measured is the review churn: the 2026-09-04 handoff counted twenty rounds
   in one day of which four were single-MINOR refusals and two were
   record-only reworks. Fixes for exactly that landed on 09-04 and 09-05 and
   have not yet been measured, which is why §5 now starts with a control
   period rather than a rebuild.
2. **The honesty devices have become the maintenance burden.** Ratchets
   (module size, complexity, smoke budget, coverage floors), allowlists
   (IF-TC coverage, orphans, provenance, kernel modules, declared absences),
   watermarks, seed counts, byte budgets — each was added to make a green
   honest, and each now needs re-stamping with a reasoned paragraph on nearly
   every kit change. The module-size baseline row for one file is a
   five-thousand-character justification. A supervising session spends its
   evening clearing "reds" that are the kit reporting on itself.
3. **The spine describes plumbing, not promises.** 96 of the 167 interface
   rows are seams between kit scripts (one module, `spine_carrier`, owns 19
   rows that are the same API listed once per importer); 44 LLRs describe
   retirements, migrations or "this helper now lives in kitlib"; every one of
   the 82 scripts has an LLR. An adopter cannot use these rows, a reviewer
   cannot judge them against a need, and every refactor of the kit amends
   approved requirement text, which drops the derived stage and mints another
   adjudication (see 1 above). Meanwhile the four founding Must needs of the
   vision (traced, gated, honest, stack-agnostic) carry a fifth of the LLR
   mass; the dashboard alone carries more.

**Recommendation: not a ground-up rewrite. A staged strangler rebuild in three
moves.** (a) Prune the spine to the promises an adopter can recognise, and move
mechanism description out of the requirement tier. (b) Rebuild the loop as a
small explicit state machine — one WI per lane, contradiction and consolidation
judged at intake before a row is queued, a typed verdict per round — under the
existing tracer and harness, which stay. (c) Cut the harness and the surfaces
to what the stage ladder needs. Target: roughly a fifth of the code, a fifth of
the tests, one process document, and a loop a new reader can hold in their head.
Section 5 gives the breakdown; section 6 gives the acceptance per phase and
what is deliberately lost.

---

## 1. What the vision actually requires

The `PROJECT-VISION:` tag and the 27 stakeholder needs reduce to five promises
an adopter can recognise. Everything the kit ships should be traceable to one
of them or be opt-in and cheap to ignore (SN-012, the proportionality need).

| Promise | Needs | What must exist |
|---|---|---|
| **P1 Traced.** Need → requirement → design → test, mechanically verified | SN-002, SN-007, SN-010, SN-036 | Registries in git; one tracer that computes orphans, coverage and integrity; an authoring guide |
| **P2 Gated.** Advance only through explicit gates whose bar is mechanical and honest | SN-004, SN-008, SN-009, SN-011, SN-029 | A stage derived from artifact state; a harness that fails rather than skips; human approval recorded on the row; a secrets floor |
| **P3 Adoptable.** Any stack, clean Python, no unargued dependencies, resync-able | SN-001, SN-003, SN-011, SN-033, SN-038, SN-039 | A scaffold; a declared stack file; a re-sync path; a guide |
| **P4 Self-directing.** An agent derives next work from tracked state, runs unattended, stops honestly | SN-005, SN-006, SN-025, SN-026, SN-027, SN-029 | A WI registry; a deterministic frontier; a coordinator; a review protocol; typed exits |
| **P5 Legible to the owner.** Progress, decisions owed, and connections from one place | SN-023, SN-028, SN-035, SN-037, SN-040 | A dashboard; an owner decision surface; one policy file |

Two observations about this table matter for the redesign:

- **P4 is opt-in in the needs (priority S), but it is where the churn lives
  and it is not separable today.** The four loop stages are 38% of the code
  directly, and by static reachability (deferred imports included) the loop
  can reach 46 of 82 modules, 65% of the kit's SLOC — the tracer, the
  trajectory checker, the architecture map and the dual-plan machinery. That
  is possible dependency, not measured load (`check_trajectory` tolerates a
  missing `check_docs`, for one), but it means nothing enforces the boundary
  the needs describe when they call the loop a layer that "costs a repo that
  doesn't use it nothing."
- **The heavy needs are not the founding ones.** By fractional LLR mass the
  top four are SN-023 (dashboard, 21.5), SN-012 (right-sizing, 16.5), SN-006
  (unattended, 16.1) and SN-024 (perceptual acceptance, 15.8); traceability
  itself is fifth. Appendix A argues each candidate: SN-027 (parallel lanes)
  is the most defensible cut — 26 LLRs and 24 TCs buying throughput, not
  trust, while every gate works identically at one lane; SN-024 is a process
  invention no adopter has asked for; SN-023 should keep its need and lose the
  acceptance clause that mandates the interface graph. The late needs SN-035,
  SN-037, SN-039 and SN-040 are cheap (ten LLRs between eight of them) and
  should be left alone, except that SN-040's mechanism is write-only and can
  become prose.

---

## 2. Diagnosis — how a simple loop became this

### 2.1 The loop turned inward

The unattended loop was built to implement the kit's own backlog. That is the
right dogfood, but it created a feedback path nothing bounds: every merge that
touches approved text mints an amendment adjudication; every early close mints
a disposition; every fourth clean close mints a spot check; every overlapping
pair of queued rows mints a consolidation. Each of those is a WI, claims a
lane, draws review rounds, and often mints more. Of 48 merges since 2026-08-15,
27 were this class by count (a category count, not a cost share — §0). The frontier at the time of writing holds nineteen queued
rows of which nine are adjudications of earlier adjudications.

The owner's instinct — "consolidation and contradiction checks at WI creation"
— is the structural fix: judge a row ONCE, when it is proposed, before it is
queued. The current design judges after the fact (a census over the queue at
idle ticks; an adjudication after a merge), which is why the same scope is
judged repeatedly.

### 2.2 Multi-WI lanes

Only one kind of WI batches: every ready spine row is admitted together into
one branch and one session (`dispatch._kind_action`). The record is clear
about why — not throughput (that knob, the "traincar", was killed after 19
reservations produced 0 gate-verified merges) but **atomicity of the human
re-attestation window**: one window over the whole spine means an amendment
cannot land half-attested. Appendix B sizes what that bought and cost. The
batch-only code is about 100 code-only SLOC (314 with docstrings, which is the
figure appendix B first quoted against a docstring-free denominator; corrected
in review round 1), a quarter of one percent of the kit, plus about 360 test
lines. Two of the fourteen functions — the verdict peel for the mechanical
close — also exist because the single-row WI-586 lane staled its own round, so
they go for a different reason (close-before-round, §4.4), not because of
cardinality.
It caused four of the six stranding defects measured on 2026-09-03: a walk
that skipped a built-but-unclosed row and stranded the lane for ten sessions,
a close that read a spec already moved and exited the whole loop, a preflight
that refused three of four rows because the lane itself had closed them, and
a legacy rollup compiled once per row. Telemetry attributes one lane's cost to
four rows, and a reviewer judged four rows with one empty findings body
(round 010). One WI per lane removes the class. What the batch protected — a shared
premise and the amendment that depends on it approving in ONE window — is
recovered by a rule, not by scheduling: related spine amendments are authored
as ONE work item (a WI may amend several rows), so atomic approval is
preserved per WI, and `exclusive` only serialises execution. What is genuinely
lost is atomicity across amendments an author chose to split, and the
component-scoped design in `concurrency-v2.md` §A4.4 is the recovery if a
spine ever grows large enough to need it. **The owner's
suspicion is right about causation and wrong about magnitude:** batches are
not where the complexity mass lives (appendix B §B.7).

### 2.3 The spine describes the kit to itself

The kit applies its own process to itself (SN-007). That is right. But the
process asks for an LLR per design decision and an IF row per seam, and the
kit has been refactored continuously for three months, so the spine now
records the kit's internal call graph: which module calls which, which helper
owns which regex, which allowlist a checker reads. Three consequences:

- **Every refactor is a requirement amendment.** Moving a function amends an
  approved LLR, which drops the derived stage, mints an adjudication, and
  needs a human or delegated approval to climb back. The stage has oscillated
  between DevStg-LLReqs and DevStg-Tests for weeks while the code was stable.
- **The tests test the tester.** Most TCs are "the checker reports X on a
  scaffold." Necessary for a checker, but they are unit tests of tooling
  wearing the clothes of requirement verification, and there are 3,255 of
  them taking ten minutes.
- **167 interface seams, 151 cited by no test, held on a 118-row allowlist
  with a seed count and a hygiene report.** This is a coverage number nobody
  can act on, so it is managed rather than closed.

### 2.4 Honesty devices without a budget

The kit's best idea is that a green must be honest: no silent skips, no
laundering by list edit, every exception carries a reason. But each device
was added without a cap on how many devices there may be. Today a routine
change to one script can red: the module-size ratchet, the cognitive
complexity ratchet, the smoke-time budget (under machine load, on untouched
commits), the IF-TC allowlist hygiene, the doc-refs checker (for a path named
in prose that does not exist yet), the orphan check, the backlink coverage
floor, the generated-artifact freshness for up to thirteen files, the
approval-brief freshness, the status budget, the vocabulary check, and the
figures provenance marker. Each red is defensible alone. Together they mean
the honest cost of any change is dominated by explaining the change to the
kit. The 2026-09-04 handoff §5 records the smoke budget red on every
measurement that day, on untouched commits, with nothing re-stamped — the
device was measuring the laptop.

### 2.5 The review protocol judges wording

Reviews are drawn from a second model family and escalate on failure. Good.
But the measured churn (handoff 09-04 §4) is prose: single-MINOR refusals,
record-only reworks, dispositions re-litigated for phrasing. The verdict
grammar admits a CHANGES-REQUESTED with no MAJOR; the reviewer brief for
adjudication rows asked for wording quality until 2026-09-05. Appendix to
`decisions-for-review-2026-09-05.md` §2 shows round count now measures the
reviewer's threshold, not the worker.

### 2.6 Three owner surfaces, and the owner still needs a handoff

`docs/status.md` (forward-only, byte-budgeted), `docs/open-items.html`
(generated briefs), `docs/ratify/CURRENT.md` (the approval brief),
`PROJECT_STATE.html` (the dashboard), `docs/log.md` (52k lines, compiled from
fragments), and a hand-written `docs/handoff-<date>.md` every day the loop
runs. The last item is the tell: the generated surfaces do not give a resuming
human or agent the picture, so a person writes one. The open-items mint
produced bare questions (five keys, no options) until this week.

### 2.7 Eight ways to say "no", seven ways to fill a prompt

The conventions a reader must hold to follow one call chain (appendix B §B.4):
results come back as `(value, refusal)` tuples in 19 modules, as a bare
refusal string or None in 12, as `(ok, msg)` in 6, as lists of finding
strings from 95 functions in 31 modules, as six custom exception classes, as
stdlib raises, as `main()` integers of which only two modules use the declared
`EXIT_*` vocabulary, and as 109 `sys.exit` sites of which 78 sit in library
code. The declared prompt contract (`prompts.fill`) has one caller; the
worker, reviewer and critique prompts it was written for use six other
mechanisms, one of which silently ignores a missing slot. The `+++`
frontmatter fence that every WI spec opens with is parsed by seven different
functions with seven different failure behaviours, and one of them documents
keeping itself in sync by hand. `process.toml`, the "one home for every dial",
is read raw in four places with three different defaults on failure. None of
this is a requirement, a need or a gate. It is what happens when 82 modules
grow in a flat namespace with a leaf `kitlib` that holds 4% of the code. Two
cautions the review round added: the seven fence parsers do different jobs
(one masks metadata, one preserves editable text, one needs fence positions on
a CRLF checkout), and the four `process.toml` readers encode different
consumer decisions on purpose (error, enable-check, ask-a-human). The fix is
one parser that returns a typed result — absent, malformed, valid — while each
consumer keeps its documented decision; not one failure behaviour for all.

### 2.8 Rows are amended, never uprooted — and the machinery makes that the cheap path

The owner's concern (2026-09-05): LLRs mostly describe implementation-level
decompositions, and agents may be working AROUND a design an LLR describes
rather than replacing the row when the need changes. The record supports it,
and it names the cause.

| Measured since 2026-08-01 (`docs/requirements/low-level-requirements.toml`) | |
|---|---|
| Commits touching the LLR registry | 126 |
| `detail` cells rewritten | 218 |
| LLR rows removed | 1 |
| LLR ids ever retired over the kit's lifetime (watermark 210, live 192) | 18 |

The owner ruled the opposite policy a month earlier (D-4, 2026-08-09:
"if something is superseded, it should just get removed"; ids are never
reused). Practice did not follow the ruling because the machinery prices the
two moves differently. Amending a row in place keeps its id, its `Approved`
status frame, its TC, its `Implements:` back-links in code and its allowlist
entries; it costs one amendment adjudication. Replacing the row means a new
`Drafted` id, a new TC, re-pointed back-links, the stage dropping, AND the
same adjudication. Faced with that, an agent — or a human — rewrites the
`detail` cell to describe the new mechanism in the old row's frame. The 44
"self-description" rows in appendix A are the residue: six rows whose text
records their own retirement, eight that say "this now lives in kitlib", one
that says "the seam described here is not yet extended". Those are rows that
should have been deleted and were amended instead. The second-order effect is
the one the owner fears: a row whose `detail` is a paragraph about a specific
helper reads, to the next worker, as a constraint on how the helper must
work, and the worker builds around it.

### 2.9 Rendering is the heaviest test bill and the least gate-bearing code

The renderer family (`gen_trajectory`, `traj_*`, `gen_open_items`,
`gen_arch_map`, `gen_components`, `gen_okf`) is 16 modules and 8,036 SLOC that
produce no decision (appendix B). Its tests: about 340 test functions and
roughly 10k lines in the render modules proper (plus another 240 tests for
`check_trajectory`, which shares the `test_trajectory*` prefix). The three
slowest tests in the whole suite are render geometry —
`test_traj_graph.py`'s wire-routing tests at 68 s, 38 s and 23 s, plus a 7 s
panel render — and `test_traj_graph` is NOT in the smoke tier's slow-module
exclusion, so those three run on every commit; the per-commit bar clears its
60 s budget only because xdist spreads them across cores. Every change to the
scheduler, the tracer or the merge slot pays for the dashboard's tests, and
nothing about a dashboard render can red a gate.

### 2.10 Migration tail and shipped sprawl

The CSV registry carrier, `wi_convert`, `migrate_carrier`, legacy rollups,
retired vocabulary aliases and the RESYNC pack (4,950 lines of prose
migration recipes) serve adopters that, as far as the record shows, number
one or two inside the owner's own sphere. Sixteen domain skills (robotics,
rendering, web UI) ship in a process kit. The scaffold copies about 150
files.

---

## 3. The gaps — what the vision needs that the kit does not yet give

These are gaps against P1–P5, not against the current implementation.

1. **A trustworthy green below the top stage.** The station refresh at
   DevStg-Tests runs fourteen steps and zero tests; the merge slot's "bar
   green" attests a suite that never ran (memory note, 2026-09-04). A gate
   that can pass with no tests executed violates P2 regardless of how many
   ratchets surround it.
2. **A coordinator that knows what code it is running.** A nine-hour process
   executes the modules it imported at launch (OI-83); it produced a false
   BLOCKER. A resumed single-checkout worker scans an empty range (OI-84).
   P4 requires the loop to be right about its own state before it is right
   about anything else.
3. **Telemetry that can answer the owner's questions.** No artifact records
   which tier a session ran at (the two Anthropic tiers are one model). Per-WI
   cost is unrecoverable for batched lanes. `est_tokens` is declared and set
   by nothing. The owner asked "should this have been a stronger worker" and
   the data cannot say. The record to write once per session (the codex plan's
   list, adopted): WI id, attempt, role, provider and model, roster row, tier,
   policy revision, timestamps, review outcome, terminal result.
4. **A review threshold.** CHANGES-REQUESTED must require a MAJOR or BLOCKER;
   a rework must move the non-record tree; adjudication reviews must judge
   scope and driven claims, not wording. Items 1–2 of the churn program
   landed on 2026-09-04; the reviewer brief on 09-05. Not yet measured.
5. **Judgement at intake, once.** Contradiction with the spine, overlap with
   an open row, and "already answered" are asked after a row exists and
   sometimes after it merged. They should be asked when the row is proposed,
   with the answer recorded on the row.
6. **An adopter path that is exercised.** The kit's tests bootstrap a scaffold,
   but there is no continuously exercised downstream repo, no adoption
   metric, and the guides are long. P3 is asserted, not demonstrated.
7. **Requirements that a stakeholder recognises.** SN-033 asks that each need
   be recognisable as the outcome the stakeholder asked for. The LLR/IF tiers
   fail that test for most rows; appendix A quantifies it.
8. **Bounded self-work.** Nothing caps the share of the loop's throughput
   spent on adjudicating its own closes. P4's "gets as far as it honestly can"
   needs a definition of "far" that excludes running in place.

---

## 4. Target shape

### 4.1 Three products, separated

Today one folder holds three things with different owners, cadences and
adopters. Separate them so each can be small.

```
project-trajectory/
  spine/       P1+P2: registries, tracer, stage, approval, harness     (always shipped)
  queue/       P4a:   work items, frontier, intake judgement           (shipped; loop-independent)
  loop/        P4b:   dispatch, lanes, sessions, review, merge         (opt-in layer)
  surfaces/    P5:    dashboard, owner briefs, status, log             (shipped; thin)
  scaffold/    P3:    bootstrap, resync, templates, guides             (tool, not copied)
  skills/      process skills only; domain skills move to their own repo
```

Dependency direction is one-way downward: `loop` imports `queue` and `spine`;
`queue` imports `spine`; `surfaces` reads all three and is imported by none.
`tests/test_import_layers.py` already exists to enforce a layering; give it a
layering worth enforcing.

**Eight modules inside those packages** (appendix B §B.7 derives the same
list from the code): `spine/registry.py` (one carrier, one row vocabulary, one
reader — absorbing `spine_carrier`, `kitlib.spine`, `kitlib.registry`,
`kitlib.ladder`, `trace_text` and the sixteen private parsers),
`spine/trace.py` (the join and the orphan report only, under 1,000 SLOC),
`spine/check.py` (the harness, with the ten `check_*` leaves as steps),
`queue/work.py` (minting, intake judgement, the frontier — absorbing
`intake`, `consolidate`, `census`, `check_trajectory`, `schedule`),
`loop/loop.py` (dispatcher, lane, session — absorbing `dispatch`, `lane`,
`agent_loop`, `agent_common`, `agent_session`, `agent_route`, minus the batch
code), `loop/merge.py` (claim, refresh, merge slot, handback — absorbing
`integrate`, `handback`, `spec_move`, `trunk_step`, `kitlib.station`),
`loop/review.py` (verdict, scoring, briefs, arbitration — absorbing
`kitlib.verdict`, `score_reviews`, `adjudicate_brief`, `acceptance_record`,
`hats`, `gen_verdict_rollup` and the five `plan_*` modules), and
`surfaces/render.py` (one generator with pluggable views, replacing sixteen
modules).

**Three capability sets, expressed where the scaffold already declares
files.** The codex plan's framing (cross-reference §2.8): a manual core, the
managed loop, and advanced planning/architecture/reporting are three sets in
the existing bootstrap mapping — no second manifest or schema — and the
adoption tests prove each promise is available and verified when its set is
enabled and absent from the core's imports when it is not.

**Three conventions, adopted before any merge of modules**, because they are
where a reader currently holds eight contracts to follow one call: one result
type (a `Findings` record with severity, and typed exit codes only at the CLI
edge — no `sys.exit` in library code); one prompt fill (`prompts.fill`, strict
on missing slots, with every template in one catalogue); one registry read
(one frontmatter parser, one `process.toml` reader, one failure behaviour).

### 4.2 The spine, pruned

- **Keep** SN, SR, TC as the promise tiers. Keep LLR only where it records a
  design decision an adopter could disagree with (a mechanism choice, a
  boundary, a format). A helper's existence is not a requirement.
- **Interface rows** describe seams that cross a boundary an adopter or a
  human sees: CLI contracts, file formats read by two parties, git hook
  contracts, the LLM CLI contract, the harness plan. Intra-kit function
  seams are documented in module docstrings and derived into the
  architecture map, not held as requirement rows. Expected: 167 → the 52
  boundary-crossing rows plus the 19 kit-to-repo-file rows, then one row per
  SURFACE for the intra-kit seams that carry a contract an import cannot
  express (error semantics, required cells, fail-closed defaults — review
  round 1 sampled five and all five did) with their consumer guarantees kept
  as contract tests — about 60. The target is one declaration per surface,
  not zero `call` rows.
- **One approval mechanism.** `Status` on the row plus the byte-for-byte
  baseline snapshot. Delete the parallel attestation ledgers and the
  approval-ledger helpers that the D-1/D-9 program already ruled dead.
- **Stage derivation stays, unchanged.** An earlier draft proposed that an
  LLR amendment could not drop the stage below DevStg-Tests; review round 1
  showed that contradicts SN-029's acceptance text ("an AMENDED requirement
  drops the derived stage exactly as a newly introduced one does") and would
  hide a human-held amendment while the approval dial covers the LLR tier.
  The honest lever is the distinction the kit already draws: a relocation
  edit to a traced cell (`Module`, `CodeSymbol`, `TestRefs`) never drops the
  stage, a normative-cell edit does. Refactors stop re-litigating the gate
  because the pruned spine (above) no longer holds a normative row per
  helper — not because the gate is clamped. If the owner wants more than
  that, the route is an explicit amendment to SN-029 (§7).
- **Test cases verify outcomes.** A TC says what an adopter observes. The
  checker's own unit tests are pytest, tagged to the TC they support, and
  not rows.

### 4.3 The queue, with judgement at intake

- **Status is the directory** — keep it; it is the best idea in the queue.
  Terminal rows under `archive/work/`, one home, no tolerance for a second.
- **A row has a lifecycle with one judgement point:**
  `proposed → (intake) → queued → active → done|cancelled|partial|restructured`.
  Intake runs when a row is proposed (by a human, by a close's dispositions,
  by a census) and answers three questions with a typed record on the row:
  does it contradict the spine, does it overlap an open row (absorb, extend,
  or edge), is it already answered. The mechanical pre-filter (shared
  spec-of-record, shared touched modules, title similarity, shared SR) runs
  first and is cheap; an LLM adjudication is drawn only when the pre-filter
  finds something, and it judges the PROPOSAL, not a merged row. A proposal
  that extends an existing queued row appends a Done-when to it instead of
  minting. This is the owner's "consolidation at WI creation." It is the EARLY
  filter and the one place overlap is judged; it does not replace the check
  that only a merge can make. A proposal is judged on intended scope against
  the queue of that moment; what it actually amends, and what the trunk looks
  like when it lands, are known only at merge. So: the post-merge validation
  of actually-changed approved cells against the snapshot stays for every
  approved row (promise or mechanism tier); the queue relation is rechecked on
  the composed trunk in the merge slot; and the intake record carries the
  queue digest it judged, so a later merge that moves the digest invalidates
  it rather than leaving a stale verdict standing. What intake retires is the
  idle-tick census as a separate row-minting mechanism and most disposition
  drafting.
- **The intake record is precise about what it judged.** Following the codex
  plan and its Fable review (cross-reference §2.4): the decision records the
  affected queued IDs it derived from structured references — requirement rows,
  dependency closure, declared shared or exclusive resources, the proposal's
  normative scope — and a missing or ambiguous scope means a global hold, not
  a guess at independence; transaction staleness (the snapshot revision, for
  apply-time preconditions) is kept separate from semantic reuse (a
  fingerprint over the adjudicated scope and acceptance text, deliberately
  excluding Deliverable, telemetry and routing-only tier changes, which is the
  existing four-field `queue_digest` rationale kept); repeated proposals from
  one source event are deduplicated against the accepted decision so a
  dismissed finding cannot mint work forever; and the legacy queue is
  reconciled ONCE by an explicit exclusive WI, after which intake reconciles
  new or changed proposals only, never every idle tick.
- **The scheduler is the sole admission authority.** Today `schedule.order_key`
  and `dispatch._judgement_first` give two answers to "what runs next" and the
  dashboard shows the first while the dispatcher executes the second (codex
  plan README §2.1). One pure scheduling result — the selected assignments plus
  the reason every other row waits — is consumed identically by the CLI
  (`next --explain`), the dashboard and the dispatcher; the dispatcher may
  refuse a stale decision or an unavailable resource, never re-order. Needs
  edges, priority, exclusivity and class barriers stay; batch admission and
  the dispatcher-side override go.
- **Spot checks and post-merge adjudications** survive only for rows that
  amended a promise-tier requirement, and they are sampled by a declared
  rate, not minted per merge.

### 4.4 The loop, as a state machine one reader can hold

```
   ready WI ──claim──▶ LANE(worktree, branch, one WI; the claim records its integration base)
                          │ build session (worker brief = spec + spine context + diff)
                          ▼
                       CLOSE (by the worker, before any round): spec → archive/work/<terminal>/,
                       Deliverable written, proposals drafted
                          ▼
                       REVIEW round r on the closed tree (second family; verdict file:
                       APPROVE | CHANGES(MAJOR+) | BLOCKED; the round names the governing identity)
                          │ CHANGES → rework session (must move the non-record tree) → r+1,
                          │           escalate tier at r=3, page at r=5
                          ▼
                       MERGE SLOT (serial): refresh onto trunk (the peelable refresh commit),
                       run the stage bar INCLUDING tests, ff-merge, regenerate, telemetry row
                          │ fail → back to lane with the red as a finding
                          ▼
                       INTAKE of the close's proposals (4.3) and the post-merge cell check, then next tick
```

Rules that make it small:

- **One WI per lane, always.** Related spine amendments are authored as one
  WI, which is what preserves atomic approval; the `exclusive` key and a class
  barrier (spine rows one at a time) give the serialisation the batch gave.
- **The verdict is a file with a grammar, and the grammar has a threshold.**
  CHANGES-REQUESTED needs a MAJOR. A rework that changes only records is not
  a rework. A round is drawn on the kit's existing **governing identity** —
  the tree with the record paths (`docs/reviews/`, `docs/log.d/`,
  `docs/iteration/`) removed and the station's refresh commit peeled
  (`kitlib/verdict.py`) — so a round file can name the tree it judged without
  moving it, and a refresh after review does not stale it. That identity and
  that one peel stay. What goes is the SECOND peel, for machine-authored
  close commits, because the worker closes BEFORE the final round rather than
  the machinery closing after it; the merge slot verifies the round names the
  governing identity of the tree it is about to merge.
- **The coordinator is stateless between ticks** except for git. Every tick
  re-derives the frontier, the lane table and the merge queue from the tree
  (which `finished_branches()` already does). It records the digest of its
  own scripts at launch and exits with a typed code when they move (OI-83).
  A claim records its integration base (OI-84).
- **Sessions are one function**: build argv from the model row, deliver the
  prompt on stdin, capture, write telemetry with the routed tier and row id.
  Prompts are five templates: worker, reviewer, intake-adjudicator,
  planner, arbiter. The dual-plan round becomes the planner + arbiter pair
  drawn when a WI carries `planmode = "dual"`.
- **Escalation stays fixed-policy** (the doc already says no learned router;
  the 09-05 analysis confirms there is no signal to learn from).
- **Authority is evaluated against current trunk policy, not the claim.**
  The claim records the policy revision as execution provenance only;
  approval authority, holds and required evidence are re-evaluated at every
  phase boundary and at promotion, so a mid-flight tightening of
  `human_approval_through` applies to in-flight work and a relaxation is never
  inferred from an old claim (codex plan, Fable F-04).
- **Human holds drain, they do not race.** Under `keep_nondependent = false`
  a held candidate stops new admission and waits for active work to drain,
  then is prepared on the settled trunk so the owner is never asked to
  re-approve against a trunk that moved. Artifact attestation names normative
  content and survives unrelated trunk motion; candidate approval names the
  exact tree and is never carried to a different one (codex plan, Fable F-02).
- **One review envelope, typed payloads.** Plans, implementation reviews,
  consolidation judgements and subjective critiques share only provenance,
  findings with stable ids and severity, and disposition; their criteria stay
  subject-specific payloads, not one universal optional-field schema.
  Arbitration of a disputed finding gets one attempt against the same
  candidate before it becomes a human decision.
- **A bounded experiment, not the default: the exact-tree integration turn.**
  The codex plan proposes serialising final candidate preparation, checks,
  final review and promotion in one reserved turn on a frozen composed tree
  with a same-tree acceptance receipt, which would remove the refresh peel as
  well as the close peel (cross-reference §2.1). It costs every lane's
  independence during the turn, and the repo's review-round distribution
  (about 3.2 per build, up to 12) means the serial section is rounds ×
  (compose + check + review). Phase 3 runs it as a stop/go experiment under
  codex's own conditions — a latency budget predeclared at the configured lane
  count against the historical round distribution, and a ledger counting the
  receipt schema, candidate-branch retention and recovery export added
  against the peeling deleted. Pass, and it replaces the governing identity;
  fail, and the design above stands.

### 4.5 The harness and the surfaces, cut to the ladder

- **One harness (`check.py`) over one `stack.ini`.** Steps per stage. The
  stage bar at DevStg-Tests and above ALWAYS runs the tests (gap 1).
- **Ratchets: three, not seven.** Coverage floor, complexity ceiling, and
  test wall-clock — each with a baseline file whose rows are one line and a
  one-line reason, re-stamped only by an explicit reviewed commit (the kit's
  never-green-by-list-edit rule stands; an earlier draft's automatic
  re-baseline on untouched commits was a laundering path and is withdrawn).
  The wall-clock budget is measured as the median of three controlled runs,
  and a breach on an untouched commit is REPORTED as environment noise with
  the three readings — never re-stamped by the machine. Module-size, IF-TC
  allowlist, backlink floor, dupes census, figures markers, status byte
  budget: delete or demote to a report the dashboard shows.
- **Generated artifacts: four.** Dashboard, open-items page, stage file,
  approval brief. Each regenerated by the merge slot, never a commit-time
  freshness step for a reader-facing document. `status.md` becomes a
  generated page with one hand-authored `## Notes` block, and that block is
  the authored operational channel — provider outages, quota resets, which
  code a long-running coordinator loaded — which no tree-derived field can
  infer. The dashboard's "Resume" panel derives the rest (pause state,
  frontier, lanes, last merges, owed decisions), regenerates at every tick end
  and on pause rather than only at merge, and every field names its source,
  its freshness and what it shows when unknown. The daily handoff is retired
  only after a resume from a paused and a failed run has been driven from the
  panel plus the Notes block alone.
- **The log**: keep fragments compiled at merge. Cap the compiled log by
  rotating yearly into the archive.
- **Docs**: one PROCESS.md under 800 lines with the opt-in layers as
  sections; AGENTS.template.md unchanged in spirit; RESYNC_PACK replaced by a
  versioned `CHANGELOG.md` plus `bootstrap.py --sync` doing the mechanical
  half (the pack's own §5 names the promotion trigger; treat this redesign as
  that trigger).

### 4.6 Replace, don't amend — and make replacement no costlier than amendment

For mechanism-tier rows (LLRs, and the surviving IF rows), the rule becomes
the one D-4 already states, made cheap enough to follow:

- **A mechanism change rewrites the design, and the id follows the
  responsibility.** When the mechanism an LLR describes changes, its `detail`
  is rewritten wholesale to describe the new design — never patched around
  the old text — and the row keeps its id while it still names the same
  design responsibility (the codex plan's position, cross-reference §2.6;
  this plan's first draft minted a new id on every change, which is what made
  replacement expensive). A successor id is minted only when obligations
  split, combine or disappear, with `supersedes` lineage; ids are never reused
  for a different meaning (D-4). A worker brief states this in one line; `check_trajectory` gets a
  detector for the residue — a `detail` cell containing "retired", "now lives
  in", "no longer", "not yet" or a date stamp is a row that was amended when
  it should have been replaced (warn-first, as every new detector here is).
- **Price the two moves the same.** Today replacement costs a stage drop plus
  a Drafted row's approval plus re-pointing, while amendment costs one
  adjudication. Two mechanisms close the gap without touching SN-029: (a) the
  new row is minted with `supersedes = <old id>` and the merge-slot intake
  treats a supersession that keeps the parent SR, the TC set and the
  back-links as ONE adjudication, the same brief the amendment gets today —
  the judge sees old text, new text and the diff, and approves or returns; (b)
  where a successor id IS minted, `Implements:` back-links and TC `verifies`
  cells are re-pointed by the replacement tooling (`spec_move`'s link-aware
  ritual already does this for WI specs; extend it to spine ids), so a
  replacement is one command, not a sweep. Keeping the id in the common case
  makes (b) the exception rather than the rule. The stage still drops, as SN-029 requires, and climbs back on the
  same adjudication.
- **LLRs describe decisions, not helpers.** The pruned spine (§4.2) keeps an
  LLR where an adopter could disagree with a design choice. A row whose
  subject is one function's placement is a docstring, and a worker who finds
  such a row should be told to delete it, not honour it.

### 4.7 Rendering as a separately tested module

- **Own package, own tests, own step.** `surfaces/` (§4.1) holds the render
  code; its tests live under `tests/surfaces/` and run as their own harness
  step, `[step:render-tests]`, not inside `tests+coverage`.
- **Path-triggered in the merge slot, always-on in CI.** The step declares the
  paths that can change its result: the render package itself, and its
  INPUT contracts — the registry readers (`spine/registry.py`) and the
  registry templates, since a schema change is the one way non-render code
  can break a render. The merge slot runs the step when the composed diff
  against trunk touches any declared path, and records "render-tests: not
  triggered (paths unchanged)" otherwise — a stated selection, never a
  silent skip, which keeps the honest-harness doctrine intact. CI on push
  runs it unconditionally, so a wrong trigger list is caught on the next
  push rather than never.
- **Selection by affected capability, with a broad fallback** (the codex
  plan's table, cross-reference §2.7): a core change proven independent of the
  renderer and its snapshot inputs runs core tests only; routine registry
  value changes run one generation-and-freshness check plus a cheap renderer
  boundary smoke; emitter, layout, style, template, asset or fixture changes
  run the full rendering family; snapshot-schema, shared-parser, vocabulary
  or shared-fixture changes run the shared contracts plus the affected
  rendering suite; test-selection changes, broad refactors, unknown impact or
  an unavailable comparison base run the broad suite and say why; phase close,
  release and a declared periodic run always run everything. Selection
  compares the whole change against its recorded base (renames and deletions
  included), local and CI use the same result, and a required check is never
  left pending by a workflow-level path skip. **Precondition:** SN-007's
  full-suite acceptance is amended, as a reviewed change, before any narrowing
  is enabled; until then the existing full run stands.
- **The geometry tests leave the per-commit bar.** The three wire-routing
  tests move to the render step's own slow tier; the per-commit smoke bar
  keeps one render smoke test (the dashboard generates and validates) so the
  build of the page itself stays covered.
- **Coverage floor per package.** The render package carries its own coverage
  floor in `docs/coverage-floors`, so pulling it out of `tests+coverage` does
  not lower the kit's global number silently.

### 4.8 Where external tools take over

Detail and evidence in appendix C. The short list the redesign should adopt
or study before building:

- **Nobody ships lane-claim-plus-gated-merge as a library, but one CLI ships
  the merge station.** A survey of about twenty worktree orchestrators
  (appendix C §C.1) found the field converged on worktree isolation and
  packaged it as desktop apps, TUIs or CLIs; the three projects that model
  the kit's whole stack are single-author, abandoned or sunsetting.
  **Worktrunk** (MIT/Apache, ~6,800 stars, released weekly, Windows via
  Winget, no daemon, state as real git) implements the same SEQUENCE as the
  station the kit hand-built: `wt merge` commits, rebases onto the target,
  runs blocking pre-merge hooks declared in a TOML file, fast-forward merges
  and cleans up. Two documented behaviours cut against the kit: its default
  squash and rebase rewrite the history that carries the kit's commit-bound
  review evidence, and a conflict leaves an open rebase where the kit's
  refresh restores the last work commit. An adapter would run
  `--no-commit --no-rebase`, which leaves the preparation with the kit, and
  must be prototyped against the station contract — evidence preservation,
  tested-tree identity, trunk races, regeneration order, recoverable failure —
  before any saving is claimed. It is a `system`-tier dependency an adopter
  installs, not a shipped-check dependency. Claude Code's own `isolation: worktree` covers lane creation
  for one vendor only.
- **Requirements-in-git tools exist and none fits the constraints.** Doorstop
  (LGPL, 16 deps) is the only one that binds approval to content — a
  fingerprint on each item and on each parent link, so a parent edit marks
  children suspect — and it stops at a binary review state. StrictDoc pulls
  86 packages including a browser driver; Sphinx-Needs means adopting Sphinx.
  Keep the TOML spine; borrow Doorstop's fingerprint-on-the-link, OFT's
  defect vocabulary (orphaned / outdated / predated / ambiguous / unwanted /
  duplicate) and sphinx-needs' declarative schema validation; emit ReqIF as a
  free export.
- **Agent-native issue trackers do not keep plain text in git.** Beads moved
  to Dolt (canonical changes sit outside source-branch diffs unless exported
  and committed); gastown inherits that and needs a daemon fleet. The plain-text ones (ticket, Backlog.md, ticket-rs)
  are bash, Node or unlocatable. Status-as-directory stays; copy their
  `ready` semantics and nothing else. GitHub Issues, whose dependencies are
  now GA, is a viable one-way mirror for human visibility.
- **Bernstein is the one library-shaped loop** (Python, Apache-2.0,
  deterministic planner-free coordination, per-worktree agents, a Janitor
  gate, file-based state, Windows in its classifiers) — a solo-maintained
  beta today. Watch it as the alternative to Phase 3's `loop/merge.py`.
- **Nothing commits a typed verdict.** Deliberation tools return chat,
  judge frameworks emit run records, review bots hold their state on the
  vendor's servers. `check-jsonschema` could validate the verdict file as a
  ledger row; the conflict detection stays in the kit.
- **The pre-commit framework is not a zero-install base**: five packages plus
  a Python, network on first run, no offline mode, and `stages:` are git hook
  types, not project phases. No runner implements a stage ladder; Nox gets
  out of the way of the Python the kit already has. lychee (links and
  anchors, Windows binary) and lizard (26-language complexity, one CSV row per
  function) are the two optional steps worth offering polyglot adopters.
- **Agent Skills is an open standard** adopted by every major vendor;
  conforming the kit's process skills costs a frontmatter check and makes
  them portable unchanged. AGENTS.md is cross-vendor with Claude Code the
  holdout, which validates the kit's thin-stub import pattern.
- **A suppression ratchet** (`cleat`'s escapes check) is the one gate worth
  adding — it watches the hatches the other ratchets are evaded through.
- **Two owner-surface shapes to copy**: blurb's log algorithm (compiled-ness
  as directory location, never deletion) and TC39's forward-only status by
  filtering a generated table, which retires the "scrub every done id" rule.

What has no good substitute, where the kit's investment is justified
(appendix C §C.8): the spine with per-cell approval, the byte-exact baseline
and the stage derived from spine health; typed, committed, CI-gated verdicts
and the "recommendation awaiting a ruling" brief; the heterogeneous-family
review with fixed escalation and the fail-never-skip harness doctrine.

---

## 5. Implementation breakdown

Strangler pattern: the new shape grows beside the old inside the same repo,
each phase leaves the trunk green and shippable, and the old path is deleted
only when its replacement has run the kit's own backlog for a stated period.
Every phase is a small number of hand-built commits with adversarial rounds
(the out-of-band pattern the owner already uses), not loop WIs — the loop
should not rebuild itself while running.

Effort is given in supervised working days for one strong agent with a human
reviewing at phase ends. Numbers are estimates and should be re-derived after
Phase 0.

### Phase 0 — Freeze and measure (2 days)

- Tag `v1-final`. Record the measured baseline: SLOC per module, test count
  and wall time, spine counts, harness steps, the 48-row telemetry table.
- Land the four correctness items that do not wait for the redesign because
  they are wrong today: the stage bar runs tests at DevStg-Tests and above
  (gap 1); the coordinator exits on script drift (OI-83); the claim records
  its base (OI-84); the routed tier and row id land in telemetry (gap 3).
- Stop the loop minting work about itself while the rebuild runs: set
  `complete_review = "off"`, `adjudication_review = "when-minting"` stays,
  and pause the consolidation census. Record the dial changes.
- **Then a two-week CONTROL PERIOD (added in review round 1).** The churn
  fixes of 2026-09-04/05 (MINOR-only verdicts do not block; identity-unchanged
  reworks page; the adjudication reviewer brief) have never been measured, and
  the smallest intake improvement — the `{open_rows}` slot and an `EXTEND`
  outcome on the disposition brief, drafted in
  `docs/decisions-for-review-2026-09-05.md` §4 — is a few days' work. Land
  that, run the loop as it stands on the real backlog for two weeks, and
  record per merge: rounds, CHANGES-REQUESTED count, supervisor interventions,
  adjudication share, escaped defects. **Decision gate:** if the control
  period alone brings rounds per merge under 2.0, adjudication share under
  20% and supervisor interventions under one a day, Phases 3 and 4 are
  re-scoped to the harness cuts only and the loop is NOT rebuilt. The
  spine prune (Phase 1) proceeds either way; it is justified by appendix A,
  not by churn.
- **Done when:** the baseline table is committed; the four fixes have tests;
  the frontier holds only build rows; the control-period table is committed
  and the gate decision is recorded as an owner ruling.

### Phase 1a — Preservation mapping (4–5 days, human-heavy)

Review round 1's BLOCKER 4 established that appendix A's class (c) means
"the ROW is self-description", not "the BEHAVIOUR is dispensable": of ten
sampled rows, five carry contracts an adopter would miss (the flow-doc
structure, vendored-source drift, the launcher's exit codes and EOF safety,
the kitlib completeness check, the complexity ratchet itself). So nothing is
deleted until every clause has a home.

- Produce a **clause-level disposition manifest** for every LLR, IF and TC
  row, using six dispositions (the codex plan's vocabulary, adopted): keep
  (enduring observable contract); consolidate (same obligation stated once,
  every acceptance condition preserved); move to design decision (internal
  organisation, reviewable without pretending it is a stakeholder outcome);
  move to optional capability (still promised when enabled); migration-only
  (with an explicit retirement release); retire (owner-approved, successor
  mapping where applicable). For each row's clauses: for each normative clause, where it lives afterwards
  (a surviving row, a module docstring plus a named test, or retired with the
  reason), and which TC or pytest test carries it. This is also the
  reproducible classification manifest appendix A lacks.
- Merge the LLR-005/LLR-015 duplicate into one row that keeps LLR-005's
  additional obligations. For the intra-kit IF rows, one row per surface,
  with each consumer's guarantee (error semantics, required cells,
  fail-closed defaults) carried as a contract test.
- Stand up the adopter fixture from Phase 5 EARLY, in its minimal form, so
  the prune has an external oracle.
- **Done when:** the manifest is committed and reviewed; every retained clause
  names its test; the fixture is green before any row moves.

### Phase 1b — Spine prune (4–5 days)

- Execute the manifest. Targets: LLR 192 → about 70 (the 47 vision-bearing
  rows plus a minimal loop layer of about 20, the dashboard's 22
  per-rubric-anchor rows collapsed to two); IF 167 → about 60; TC 191 →
  about 90 (retired TCs become pytest tests tagged to the surviving row).
- Stage derivation is NOT changed (review round 1, BLOCKER 1). If the owner
  wants refactors to stop dropping the stage, that is an explicit amendment
  to SN-029 taken in §7, not a clamp.
- Delete the IF-TC coverage allowlist and its hygiene check; every surviving
  seam gets a real contract test or a `VerifiedBy`.
- Keep the pre-prune baseline snapshot as the comparison oracle until the
  manifest has been checked against it; re-seed the snapshot once, afterwards,
  as a signed owner act.
- **Rollback trigger and rehearsal:** the prune lands as a small number of
  reviewed commits behind a tag; a red on the fixture or a manifest clause
  with no home reverts to the tag. Rehearse the revert once before the first
  real commit.
- **Done when:** `trace.py` is green with orphans=0 and no allowlist; every
  manifest clause resolves; the fixture passes its own gates; a kit refactor
  commit that moves a helper between modules touches no normative cell and
  therefore leaves the stage where it was (the test of 2.3).

### Phase 2 — Queue with intake judgement (5 days)

- First, the three conventions from §4.1: one frontmatter parser returning
  a typed result (absent / malformed / valid) that the seven current sites
  consume for their different jobs (masking, text preservation, fence
  positions on CRLF); one `process.toml` reader with the same typed result
  while the four consumers keep their documented decisions (error,
  enable-check, ask-a-human); one result type and no `sys.exit` outside
  `main()` (78 library-code sites today); one prompt fill (the worker,
  reviewer and critique prompts move onto `prompts.fill`). Each site's
  failure direction is characterised (malformed fence, BOM, CRLF, missing key,
  security default) BEFORE it is replaced — this is not a find-and-replace.
- Introduce the `proposed/` directory and the intake step
  (`queue/intake.py`): mechanical pre-filter, typed record on the row
  (`intake = {verdict, overlaps, contradicts, judged_at}`), optional LLM
  adjudication drawing the intake-adjudicator template. Add the `EXTEND`
  verdict that appends a Done-when to an existing queued row.
- Route every producer of rows through it: human mint, close dispositions,
  gap census. Delete the post-merge amendment adjudication for non-promise
  rows and the idle-tick consolidation census once intake has judged a
  week's proposals.
- One terminal home (`archive/work/`), integrity error on a spec anywhere
  else — this is the WI drafted in `decisions-for-review-2026-09-05.md` §5.
- **Amend the approved contracts that mandate the old runtime BEFORE Phase 3
  enables any changed behaviour** (the codex plan's P1A, added here after
  the cross-reference; this plan's own reviewer missed it). SR-148 approves
  the current admission partition, LLR-149 the multi-WI batch, SR-144 and
  SR-156 the partial close and lane lifecycle, SR-157/LLR-210/TC-208 the
  census consolidation, LLR-159/LLR-182 the admission and terminal vocabulary.
  A new runner enabled against those rows either fails the gates or runs
  outside them. The amendment set is the smallest reviewed, version-scoped
  change to those rows and their TCs, approved through the stage mechanism,
  with old-format and old-runner tests scoped to their supported version. No
  red gate is waived to fit the pilot.
- **Done when:** a proposal that duplicates a queued row is refused or
  extends it at intake, driven on a scaffold and on the live queue; the
  adjudication share of merges over the following two weeks is under 20%.

### Phase 3 — Loop rebuild, one WI per lane (8 days)

- New `loop/` package: `dispatch.py` (tick: frontier → claim → lanes → merge
  queue), `lane.py` (worktree + one session), `review.py` (round, verdict
  grammar with the MAJOR threshold, fixed escalation), `merge.py` (rebase,
  bar with tests, ff-merge, regenerate, close), `session.py` (argv from the
  model row, stdin prompt, telemetry). Target about 6k SLOC replacing
  `agent_loop`, `dispatch`, `lane`, `integrate`, `handback`, `intake`'s mint
  half, `agent_route`, `agent_session`, `kitlib/verdict`, `kitlib/station`,
  `score_reviews`, `gen_verdict_rollup`, `acceptance_record`, `pending`,
  `plan_*` (about 12k SLOC today across the dispatch, merge, review and
  arbitrate stages; target 5–6k).
- Close-before-round ordering removes the verdict peel and the legacy
  rollup path. Batch admission and `mechanical_close_order` are not ported.
- Run both loops against the kit's backlog for two weeks in alternation;
  the new loop must merge every class of row the old one merges, with fewer
  rounds per merge and no supervisor-drawn rounds.
- Runs only if Phase 0's decision gate said so.
- **Rollback trigger:** the old loop stays runnable behind a flag until the
  soak ends; any class of row the new loop cannot merge, or any supervisor
  intervention the old loop would not have needed, stops the soak and reverts
  the flag.
- **Done when:** the old loop's modules are deleted; the run log shows two
  weeks with no hand intervention beyond the pause file and rulings; the
  retained tests from Phase 1a all pass against the new loop.

### Phase 4 — Harness and surfaces (4 days)

- Ratchets cut to three with one-line baselines and auto re-baseline on
  untouched commits. Generated artifacts cut to four, regenerated at merge.
- `status.md` becomes generated plus a Notes block; the handoff document is
  retired in favour of the dashboard's derived Resume panel; the open-items
  mint writes a full brief (title from the first sentence, options and a
  recommendation required — WI-570's scope).
- Skills: domain skills move to a sibling repo; the kit ships process skills
  only.
- Rendering becomes its own package and harness step per §4.7; the three
  wire-routing tests leave the per-commit bar; `[step:render-tests]` carries
  a declared path trigger and runs unconditionally in CI.
- The replace-don't-amend rule (§4.6) lands as one line in the worker brief,
  a warn-first residue detector, and the `supersedes` single-adjudication
  path plus id-aware re-pointing.
- **Done when:** the pre-commit floor runs under ten seconds; every ratchet
  red names the guarantee it protects and how to re-stamp it by a reviewed
  commit; a resume from a paused run AND from a failed run has been driven
  from the Resume panel plus the Notes block alone, after which the handoff
  document is retired.

### Phase 5 — Scaffold, docs, and the adopter test (4 days)

- `bootstrap.py --sync` performs the mechanical half of a resync from a
  `CHANGELOG.md` with `since` SHAs; RESYNC_PACK.md is archived.
- PROCESS.md rewritten under 800 lines with the opt-in layers as sections;
  PROCESS_OPTIONS.md folded in or archived.
- A downstream fixture repo (a small real project, not a scaffold) is
  adopted and re-synced in CI on every kit change — P3 becomes demonstrated.
- **Done when:** the fixture repo passes its own gates on a clean Python
  3.11 on Windows and POSIX in CI; a new adopter can go from empty repo to a
  green DevStg-Reqs gate following only the README.

### Totals

| | Today | Target after Phase 5 |
|---|---|---|
| Kit SLOC (code only) | 38,995 in 82 modules | ~10–12k in about 8 modules |
| Loop import closure | 65% of the kit | the `loop` package and what is below it |
| Tests | 3,255 / ~10 min | ~700 / under 3 min full, under 30 s smoke |
| Result / prompt / registry conventions | 8 / 7 / 7 | 1 / 1 / 1 |
| LLR / IF / TC | 192 / 167 / 191 | ~70 / ~60 / ~90 |
| Harness steps at top stage | 34 | ~14 |
| Generated artifacts | 13 | 4 |
| Process prose | ~9k lines | ~1.5k |
| Supervised effort | | ~36 days plus a two-week control period and a two-week soak — **indicative only**; re-estimate after the Phase 1a manifest and the Phase 3 exact-tree experiment exist (the codex plan declines to estimate before those, and is right that the number is not credible until then) |

---

## 6. What is deliberately lost, and the risks

- **Fine-grained requirement history of the kit's internals.** Deleted LLR
  and IF rows are history in git and in the archived log. A future reader who
  wants to know why a helper exists reads its docstring, not a row.
- **Some honesty devices.** The module-size ratchet, the IF-TC allowlist and
  the backlink floor go. The argument is that they measured the kit's
  description of itself; the coverage and complexity ratchets and the
  no-skip harness carry the honesty that matters.
- **Batch merges.** Spine rows merge one at a time. If spine WIs become
  frequent again that is a signal the spine is describing plumbing again,
  not a reason to bring batches back.
- **Risk: the rebuild is itself a big change to a repo whose process punishes
  big changes.** Mitigation is the strangler order and the Phase 0 freeze of
  self-minting. The owner's out-of-band pattern (hand commits, Opus/Sol
  adversarial rounds, no loop WIs) is the right vehicle.
- **Risk: adopters mid-resync.** There appear to be none outside the owner's
  sphere; Phase 5 makes that explicit with a fixture rather than a pack.
- **Risk: the loop's soak finds classes of row the new loop cannot merge.**
  Two weeks in alternation is the cheapest honest test; extend rather than
  shortcut it.
- **Risk: the prune retires a behaviour with its row.** Review round 1 found
  five of ten sampled "self-description" rows carrying adopter-visible
  contracts. The Phase 1a manifest and the early fixture exist for this; if
  either is skipped, the prune should not run.
- **Risk: the plan's own measurements.** Two figures in the first draft were
  wrong in the plan's favour (batch SLOC counted with docstrings; "27 of 48"
  read as effort). They are corrected in this version and the corrections are
  recorded in `review-01-dispositions.md`; treat any remaining single-source
  number as a claim to re-derive before it drives a decision.

---

## 7. Decisions the owner should take before Phase 1

1. Confirm the five promises in §1 as the frame. Rule on the two needs
   appendix A names as the cheapest cuts: SN-027 (parallel lanes — keep the
   one-WI-per-lane loop, drop the fan-out as a stakeholder need and let it be
   a `lanes` dial with no requirement rows of its own) and SN-024 (perceptual
   acceptance — retire, or keep as an opt-in layer with its 39 LLRs moved out
   of the core registry). Rule SN-023's acceptance clause down to "one file a
   reviewer can open."
2. Decide whether SN-029's acceptance ("an amended requirement drops the
   derived stage exactly as a newly introduced one does") should be amended
   so that a mechanism-tier (LLR) amendment on a stage already past
   DevStg-Tests is adjudicated without dropping the stage — or left as it is,
   with the pruned spine doing the work. Review round 1 showed the plan's
   first draft would have clamped the stage in contradiction of that text;
   only an explicit amendment to the need is honest.
3. Rule one WI per lane and the retirement of batch admission.
4. Rule the intake point (`proposed/` + judgement) as the one place
   contradiction and consolidation are asked.
5. Choose the ratchet set (three proposed) and the auto-re-baseline rule.
6. Decide the fate of the sixteen domain skills.
7. Decide whether Phase 3's merge station is rebuilt in the kit or delegated
   to Worktrunk as a system-tier dependency (appendix C §C.1), after a
   prototype against the station contract (evidence preservation under
   `--no-commit --no-rebase`, tested-tree identity, trunk races, regeneration
   order, recoverable failure). The trade is one external binary and a TOML
   hook file against part of the refresh/merge code — how much is what the
   prototype measures. Either way the claim, the verdict gate, intake and the
   review protocol stay in the kit — nothing external models those.
8. Rule the replace-don't-amend policy for mechanism-tier rows (§4.6): D-4
   already says superseded rows are removed; the decision is whether a
   supersession that keeps the parent, the TC set and the back-links is one
   adjudication (the amendment's price) so the ruling becomes the cheap path.
9. Rule rendering as a path-triggered harness step (§4.7): the merge slot
   runs render tests only when the render package or its input contracts
   changed, recorded as a stated selection; CI on push runs them always.
10. Accept or reject the Phase 0 control period and its decision gate.
11. Run the exact-tree integration-turn experiment (the codex plan's P5) in
    Phase 3, or skip it and keep the governing-identity design as the end
    state. The experiment is cheap to define and expensive to run; its budget
    must be declared before it starts. It is
   the round-1 reviewer's strongest structural point: the churn fixes already
   landed have not been measured, and a rebuild decided before measuring them
   cannot be evaluated afterwards.

---

## 8. Review record

This plan is under adversarial review by a second model family, on the kit's
own cross-family doctrine. Each round's brief, findings and the author's
per-finding dispositions are kept beside the plan:

- Round 1 (codex, `gpt-6-astra`, effort high, 2026-09-05):
  [brief](review-01-brief-codex-astra.md) ·
  [findings](review-01-codex-astra-findings.md) ·
  [dispositions](review-01-dispositions.md). Verdict: diagnosis partly,
  target partly, breakdown not executable. Four BLOCKERs and ten MAJORs;
  every finding accepted in full or in part, none rejected. The material
  changes: the stage clamp withdrawn (contradicted SN-029); automatic
  ratchet re-baselining withdrawn (a laundering path); a clause-level
  preservation manifest before any row is retired; a two-week control period
  with a decision gate before any loop rebuild; corrected figures (batch
  code is about 100 code-only SLOC, not 383; the loop's closure is 46
  modules by static reachability; "27 of 48" is a category count).
- Round 2 (cross-reference against the owner's independent codex plan,
  2026-09-05, branch `redesign-crossref-2026-09-05`):
  [comparison and dispositions](review-02-crossref-codex-plan.md). The two
  plans converge on the loop shape, one WI per lane, intake before
  eligibility, the LLR replacement route and rendering isolation. Ten codex
  elements adopted — amend-the-contracts-before-enabling (a defect this plan
  shared and its reviewer missed), the scheduler as sole admission authority,
  intake affected-scope and staleness rules, current-policy authority and
  human-hold drain, the review envelope, capability sets in the bootstrap
  mapping, the telemetry record, the six-way disposition vocabulary, the
  rendering selection table with the SN-007 precondition, and the codex id
  policy for LLR replacement. The exact-tree integration turn is taken as a
  bounded experiment, not the default.
