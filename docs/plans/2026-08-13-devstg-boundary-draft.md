# The DevStg-Boundary draft — the kit's depth-0 frame, for sitting 2

**Status: DRAFT FOR RULING, not a decision.** Written after sitting 1 ratified
SN-037…SN-040 and ruled decision **2.7(a)** — *an SR may name an artifact only
where that artifact is a **declared boundary crossing***
([sitting-pack §2.7](2026-08-13-sitting-pack.md)) — which queued
[`WI-451`](../work/queued/WI-451-sr-boundary-conformance-pass.md). That pass
re-states ~50 SRs *against the boundary*, so the boundary has to exist first.
This document proposes it. Every figure names the command that produced it.

---

## 0. Provenance — where DevStg-Boundary came from, and where boundaries live

**The owner's question:** *"I don't recall how that even appeared, do those
appear in interfaces.toml or was a new registry proposed?"*

**Short answer: `interfaces.toml` is the one home. No new registry was ever
proposed — not in any plan, WI spec, open item or log entry.** (Searched:
`grep -rn "boundary registry\|boundaries.toml\|boundary.toml\|actors.toml\|new
registry" docs/plans docs/requirements docs/log.md docs/work project-trajectory`
— the only hits are two dual-plan assumptions about a WI-registry *column* and
WI-399's scope guard, none about boundaries.) The rung's own predicate reads the
IF registry and nothing else (`derive_gate.boundary_incomplete`, line 574).

**How the rung appeared, in three steps:**

1. **2026-08-11** — [`2026-08-11-stage-gate-semantics.md`](2026-08-11-stage-gate-semantics.md)
   argued *a gate is a moment, the repo uses it as a state*, and shipped a
   six-rung ladder. **No boundary rung in it** (its header now records it as
   superseded in part). The companion
   [`status-ladder-migration.md`](2026-08-11-status-ladder-migration.md) is D-9's
   `Status` rewrite and is unrelated — it mentions boundaries nowhere.
2. **2026-08-12/13 — OI-14 part A-prime is what minted the rung.** OI-14 asked
   *"whether `DevBar-Reqs` must require a declared system boundary first"*
   (`open-items.toml#OI-14.one_line`), because *"SRs are blessed today against a
   frame nobody declared"* (`OI-14.recommendation`). Ruled **(A6): require the
   declared system boundary, WITH AN APPLIES-WHEN AND WARN-FIRST**
   (`docs/log.md` Decisions, 2026-08-13 batch ruling).
3. **2026-08-13 — OI-21 gave it a rung.** The eight-rung `DevStg-<Label>` ladder
   inserted `DevStg-Boundary` at position 1, between Needs and Reqs; OI-14's
   own row records the consequence: *"naming 'system boundary interfaces' as its
   own stage makes the ORDERING obligation ladder-borne for every project, so
   A5/A6/A7 now decides only the ENFORCEMENT half."* Shipped in **WI-445**
   (`docs/log.md` §2026-08-13c, "the gate vocabulary retires").

**What the rung requires.** `PROCESS.md` §4 line 396: *"the system's frame: what
is outside, what crosses, each crossing typed. HAPPENS ONCE."* The boundary is
the one level that does **not** recurse — every boundary below it is *produced
by* a partition (PROCESS.md §4, "The boundary happens once"). The bar
(`gate-advance/SKILL.md` L128-131): *"If the repo declares an `interfaces`
registry, the boundary inventory is settled — every declared crossing typed,
none left at `Stability = Experimental` — or `DevStg-Boundary` honestly holds the
ladder down."*

**The honest current state — and it is weaker than it sounds.**
`boundary_incomplete`'s own docstring (`derive_gate.py` L586-590) says the quiet
part: *"NOTE WHAT THIS DOES NOT CLAIM. It does not verify that every external
crossing is covered — nothing in the schema types a crossing as external today,
and inventing that field is OI-14 part B's business, not this rung's."* Part B
shipped (WI-443) **without** adding that field: `interfaces.toml`'s fields are
`direction · this_project · counterpart · contract · signal · signal_note ·
sr_refs · version · stability · component · notes` — there is no `external`
flag. So the rung today checks only that the *declared* rows are settled, never
that the frame is complete.

**The five rows holding the rung down** (`Stability = Experimental`, 5 of 113;
`python3 -c` over `tomllib.load(interfaces.toml)['interface']`):

| IF | Gist | Why still Experimental |
|---|---|---|
| **IF-057** | `plan_coverage` reads `interfaces.toml` + SR ids to resolve a dual-plan's per-WI cites | its consumer seam (`agent_loop`) was never declared — "WI-197's to declare" |
| **IF-103** | `migrate_carrier.py` — the one-shot CSV→TOML spine converter | *"Stability is PROVISIONAL on purpose: migration scaffolding with a defined end"* |
| **IF-118** | `gen_open_items` reads the decision registry through `spine_carrier` | minted by the batch-2 carrier sweep, never re-reviewed |
| **IF-119** | `agent_route` reads the model registry through `spine_carrier` | same sweep |
| **IF-120** | `trunk_step` asks the carrier which carrier of a registry is live | same sweep; was `Provisional` until WI-443 |

Note what they are: **four of the five are internal carrier seams, not external
crossings.** The rung that is supposed to certify *the system's frame* is
currently held down by module-to-module plumbing. That is a finding for §4.

**Where the 34-crossing inventory actually lives — and it is not a registry.**
[`2026-08-13-part-a-data-pack.md` §1](2026-08-13-part-a-data-pack.md) (WI-441,
measured at rev `81a142c2`), whose own header says **"analysis input, not a
decision."** §1a lists 15 crossings the registry carries (X-01…X-15), §1b lists
19 it misses (M-01…M-19), §1c declares the set **complete to the author's best
reading** with six stated uncertainties. WI-441's deliverable records the same:
*"the 34-crossing boundary inventory … (19 crossings have no IF row — Part B's
intake)."*

**Reconciliation with the live registry, honestly.** The 15 X-rows all still
exist and still name an external counterpart today. A filter for
non-repo-path counterparts returns **16** rows — the extra is `IF-019`
(`skills/INDEX.csv`), an internal generated file, not an actor. Of the 19
M-rows, **13 have no IF row at all** (M-01, M-02, M-04, M-05, M-07, M-09, M-11,
M-12, M-13, M-14, M-15, M-17, M-19) and **6 have a partial/adjacent row that
names the file rather than the actor** (M-03/IF-048, M-06/IF-014, M-08/IF-074,
M-10/IF-037, M-16/IF-032, M-18/IF-070). **`docs/architecture.md` carries no
boundary section at all** (`grep -n "boundary\|external\|actor"` returns only
three generated function-summary rows) — which is a live gap against SN-040's
acceptance: *"the record is kept with the architecture, not in session prose."*

---

## 1. The depth-0 frame — what is OUTSIDE, what CROSSES

**The system** = the kit: `project-trajectory/` scripts + hooks + templates,
verified by `tests/`, self-applied to this repo (`docs/architecture.md`, "Shape
of the product"). Direction is stated from the kit's point of view: **IN** = the
kit consumes; **OUT** = the kit provides. Signal typing is OI-14 part B's ruled
vocabulary (`PROCESS.md` §8): **discrete** = finite enumerable alphabet;
**variable** = unbounded content.

| # | External party | Crossings (typed) | IF today |
|---|---|---|---|
| **E1** | **Adopting team / contributor** | `dev-setup.*` invoke + toolchain probe (discrete) · `run.*` capability menu OUT (discrete) · terminal report OUT (variable) | M-01 **MISSING** · IF-048 (menu side only) · M-19 **MISSING** |
| **E2** | **Human owner** (this repo, and every adopter's) | `agent-resume.*` trigger IN (discrete) · `docs/process.toml` dial surface IN (discrete) · ratifications / `Status` flips IN (discrete) · `docs/status.md` IN/OUT (variable) · `PROJECT_STATE.html` OUT (variable) · `open-items.html` OUT (variable) | M-02, M-11, M-09 **MISSING**; IF-037 / IF-074 name the *file*, not the reader |
| **E3** | **Agent CLI (direct session)** — OI-28 seed 1 | instructions IN (variable) · artifact edits OUT, admitted only through the git hook floor (variable gated by discrete) · headless invoke + result (IF-041) · `PreToolUse` allow/deny (IF-020) | IF-020, IF-041 exist; M-12/M-13 **MISSING** |
| **E4** | **Model provider API** behind every CLI | rate limit · auth expiry · retired model (discrete error class) | M-15 **MISSING** (the pack cites "SN-020's failure modes"; SN-020 was dissolved at OI-18, so **no live SN owns this crossing** — SR-026's backoff clause is its only home) |
| **E5** | **External reviewer CLI** (codex; `sol`/`terra`) | hostile brief OUT, findings IN (variable) | M-14 **MISSING** (`docs/agents.csv` declares families via IF-045; no provider row) |
| **E6** | **git** — the mutation floor | staged/outgoing content IN (IF-032) · commits, merges, pushes, advisory locks (discrete ref state + variable diff) · hook exit as the enforcement gate (discrete) | IF-032 read side only; M-16 otherwise **MISSING** |
| **E7** | **GitHub / hosted CI** | push·PR·schedule trigger + OS×Python matrix IN (discrete) · job verdict + step log OUT (discrete + variable) | M-04, M-05 **MISSING** |
| **E8** | **OS · filesystem · Python ≥3.11** | path semantics · encoding · kernel advisory lock · interpreter presence (discrete) | M-17 **MISSING** (SN-011 + SR-034/035/114 depend on it; the pack also cites SN-013, dissolved at OI-18) |
| **E9** | **Test/coverage toolchain** (pytest, coverage) | results feeding the tier floors (discrete) · `coverage.json` percents (IF-070, variable) | IF-070 partial; M-18 otherwise **MISSING** |
| **E10** | **Downstream adopted repo (tree)** | scaffold write + re-sync diff OUT (variable + discrete stamp) · harness verdict OUT (IF-013) · generator outputs OUT (IF-017, IF-018) · vendored-drift verdict (IF-016) · upstream source IN (IF-036) | IF-013…IF-018, IF-036; M-06 (the template→`docs/` **mapping**) **MISSING** |
| **E11** | **The shipped template set as product** — OI-28 seed 2 | `*.template.*` + `registries/*` OUT as a traced artifact class (variable) | M-07 **MISSING** — one SR anchor owed, `test_dogfood_sync` as its verification |

**Two rows that need re-reading, not re-typing.** `IF-080` (`integrate.py`) and
`IF-081` (`trunk_step.py`) declare `downstream adopter` as counterpart but are
the unattended station's *internal* serialization seams. They are counted in the
data pack's 15 external rows; under §2's discriminator they read internal.
Sitting 2 should say which.

**The data pack's six stated uncertainties (§1c) stand and are the ruler's, not
mine:** is `downstream adopter` one actor or three (team / tree / their CI)? is
git one crossing or three (read / write / hooks)? is the terminal an actor at
all? is the skills fan-out into a third-party agent's config namespace its own
crossing? is a `docs/knowledge/` pack an input? and `MULTI_REPO.md`'s cross-repo
rung was deliberately not audited.

---

## 2. The boundary set the SRs get written against

**The discriminator, stated as a rule WI-451 can apply mechanically:**

> An artifact may be named in SR text **iff** it is the *this-project* side of an
> IF row whose `counterpart` is an **external party from §1** — i.e. it is a
> **port**. Everything else is an **internal seam**: it belongs to the LLR tier
> (or is re-stated against the IF row that types the seam).

**Depth-0 PORTS — the proposed list.**

- **Harness entry** — `check.py` (IF-013); **scaffold/re-sync** —
  `bootstrap.py` (IF-014, incl. `--agents`/`--sync`).
- **Unattended entry** — `agent_loop.py` (IF-015) + root
  `agent-resume.{cmd,sh,command}` (M-02, no row). **Contributor launchers** —
  `run.*`/`run_menu.py` (IF-048), `dev-setup.{sh,cmd,command}` (M-01, no row).
- **Agent-harness contract** — `subagent_gate.py` PreToolUse (IF-020).
- **The git hook floor** — `pre-commit`, `pre-push`, `commit-msg` (M-13, no row).
  Ports *because they are the only thing standing between E3 and the tree*
  (OI-28: SR-019's rationale is already written as a boundary statement).
- **Adopter-invoked generators** — `gen_cases.py` (IF-017),
  `gen_release_checklist.py` (IF-018), `check_vendored.py` (IF-016).
- **Declared surfaces a human reads or edits** — `docs/process.toml` (the dial
  surface), `docs/status.md`, `docs/gate`, `PROJECT_STATE.html`,
  `open-items.html`, `docs/architecture.md`. **The surface is the port; its
  generator is not.**

**Internal seams — the LLR/architecture tier.** The W1–W4 component boundaries
(`components.toml`: CMP-006 Registry & conformance · CMP-007 Gatekeeper ·
CMP-008 Autonomy · CMP-009 Human & adopter surfaces, all `State = planned`,
provisionally adopted warn-first — sitting-pack §3). Under the recursion these
are *depth-1* boundaries produced by the P5 partition; the ladder is explicit
that a partition **is** the next level's boundary declaration, so they are not
depth-0 frame and SRs must not name their modules.

**Worked examples of each class:**

| SR | Names | Class | Why |
|---|---|---|---|
| SR-006 | `check.py` | **PORT** | IF-013's this-project side; an adopter types this string |
| SR-034 | `scripts/*.py` (as a set) | **PORT-ish** | names the *shipped set*, not a module — a property of E10's crossing |
| SR-026 | `agent_loop.py` | **PORT** | IF-015 |
| SR-137 | `docs/process.toml` | **PORT** | E2's dial surface |
| — | `gen_trajectory.py` (11 SRs) | **INTERNAL** | the *dashboard* is the port; the generator is CMP-009 realization |
| — | `check_trajectory.py` (9 SRs) | **INTERNAL** | a lint inside CMP-007; the adopter invokes `check.py`, never this |
| — | `trace.py` (10 SRs) | **INTERNAL** | same; its verdict reaches the outside only through IF-013 |
| — | `schedule.py` (5 SRs) | **INTERNAL** | CMP-008 frontier machinery, no external counterpart |

**Measurement, and where it differs from the pack.** `75 of 148` SRs name a
`.py` in `requirement` text — the pack's figure reproduces exactly. Splitting
them on the *ten declared-external-port scripts* (`check`, `bootstrap`,
`agent_loop`, `check_vendored`, `gen_cases`, `gen_release_checklist`,
`subagent_gate`, `run_menu`, `integrate`, `trunk_step`) gives **18 SRs naming
only ports** and **57 naming at least one internal module** — not the pack's
~25/~50 estimate. The delta is definitional (the pack's "entry-point-class" was
a looser reading), and it moves the re-statement program *up*, not down. The
per-row census is WI-451 slice 1's job; this figure only sizes it.

<!-- fig: cmd="python3 - <<'EOF' … tomllib over system-requirements.toml, re
r'\b([A-Za-z_][A-Za-z0-9_]*\.py)\b' over requirement text, ports set as listed",
rev=4295dea4 -->

---

## 3. The SR↔SN duplication question

**The owner's concern, verbatim:** *"If a system requirement is defined at the
boundaries of the system, it can't refer to its implementation and it also can
feasibly be 1 SR per SN, and then implementation specific details drop into
LLRs. My main concern is how much duplication might exist between SR and SNs."*

**The quantification** (`tomllib` over `stakeholder-needs.toml` +
`system-requirements.toml`, counting `sn_refs`):

- 27 SNs, 148 SRs, **232 (SR→SN) edges**.
- **19 SNs are covered; 8 are not** — and the uncovered eight are exactly
  SN-033…SN-040, *including all four boundary needs ratified at sitting 1*.
  All 27 rows now read `kind = "core"` (the sitting-1 ratification commit,
  4295dea4), so **SN-037…SN-040 are ratified needs with zero SRs.** They are
  not "young rows waiting for decomposition" — they are the commissioning
  authority for WI-451, and WI-451's output is their first coverage.
- Across the 19 covered: **min 2, median 8, mean 12.2, max 30**.
  **No SN has exactly one SR.** The thinnest are SN-028 (2), SN-011 (3),
  SN-029 (3); the fattest are SN-006 (30), SN-025 (28), SN-002 and SN-010 (24).
- **82 of 148 SRs cite more than one SN** — so the graph is not even a tree,
  let alone 1:1. A 1:1 tier would have to *cut* 84 of the 232 edges.

<!-- fig: cmd="python3 - <<'EOF' … collections.Counter over sn_refs; median via
statistics.median", rev=4295dea4 -->

**Chain 1 — SN-008 → 19 SRs: the SN is one word, the SRs are the mechanism.**
SN-008 is *"a reader can believe a green: gates are honest, and a green never
hides a skipped check, a stub, or an unmet criterion."* Restated at the boundary
it fans out across **different ports**: SR-006 types IF-013's verdict
(`--gate <bar>` runs that bar's steps; a missing tool **fails**, `--lenient`
degrades to SKIP); SR-016 is the stub detector; SR-133 the freshness skip;
SR-093…098 the loop's own honesty. **The SR tier is not duplicating SN-008 —
it is naming which port each promise is measurable at.** One need, many ports:
this is the healthy case and it is the majority.

**Chain 2 — SN-006 → 30 SRs, via SR-026: signal typing and error paths.**
SN-006 says *"an agent can run unattended and resume from repo text alone; such
a run never blocks on a prompt and fails clearly."* SR-026 adds what the port
contract must say: *which* text is authority (claimed assignment + committed
trailer evidence, **not** `docs/status.md`, which SR-059 makes a *generated*
surface), that stdin is closed, that a rate limit **backs off** rather than
fails, that a stall aborts to protect budget. Everything after the semicolon is
**error-path obligation the SN does not carry** — and the acceptance cell
records that the backoff clauses were folded in at the 2026-08-13 dissolution
*because the review round found no SR carried them*. That is the tier earning
its keep in the record.

**Chain 3 — SN-028 → 2 SRs: the honest near-echo.** SN-028's need cell already
names `docs/process.toml`, bare `[section]` headers, the dual-reader pin and the
`--migrate-config` refusal — because its *acceptance* cell does. SR-137 restates
the one-home-plus-refusal rule; SR-138 adds the migration. **Read SN-028's need
sentence against SR-137's requirement sentence and they say the same thing.**
The delta lives entirely in the acceptance cells (SR-137 enumerates *at every
guarded entry point*: the dispatcher's pre-claim preflight, intake's
adjudication arm, the integrator's verdict gate). SN-011 → SR-034/035/114 is the
same shape: SR-035's whole text is *"the process and ID scheme shall be
stack-agnostic"* with acceptance *"the ID scheme is language-neutral"* — an SR
that adds **nothing** over its SN.

**The options where the echo is real:**

1. **Tolerate the echo, the acceptance cell carries the delta.** Cheapest; keeps
   the tiers uniform; but SN-033's ratified rule (*a stakeholder reads the need
   without knowing how the repo is built*) is violated in the other direction —
   SN-028's need cell is echoing *downward* into implementation vocabulary.
2. **Merge** — delete the SR, point LLRs at the SN. Breaks the join
   (`trace.py` walks SN→SR→LLR→TC); refuted on machinery grounds alone.
3. **Split the roles: the SN carries the OUTCOME, the SR carries the PORT
   CONTRACT.** SN-028 becomes *"the owner can find and change every policy dial
   in one home, and a repo declaring a dial twice is refused"* — no filename;
   SR-137 keeps `docs/process.toml`, the line grammar and the refusal points.

**Recommendation: option 3, and note it is already the ratified direction.**
SN-033 (ratified) forbids internal paths in `need` cells; decision 2.7(a)
permits them in SR cells *at declared ports*. `docs/process.toml` is a port
(§2), so SR-137 keeps its name and SN-028 loses it. The two rules compose into
one sentence: **the need names the outcome, the requirement names the port.**
Do **not** target 1:1 — 82 of 148 SRs are genuinely multi-need, and forcing 1:1
would either merge unrelated ports into one row or duplicate one port's contract
across several. The right invariant is *one SR per (need, port)* pair, which the
current 232 edges are already a rough approximation of.

**One flag for the ruler:** SR-035 as written adds nothing to SN-011 and is a
real merge candidate — but it is `Modified`, so touching it costs a re-attest.
Bundle it into WI-451's window rather than opening a second one.

---

## 4. What sitting 2 must rule

1. **Adopt or amend the depth-0 frame (§1)** — the eleven external parties
   E1…E11 and their crossings, including the six stated uncertainties from the
   data pack §1c (is `downstream adopter` one actor or three? is git one
   crossing or three? is the terminal an actor?). Adopting also means adopting
   the **completeness declaration** — the claim that this set is the whole
   frame — which is what the rung actually certifies.
2. **Adopt or amend the port list (§2)** and its discriminator rule. The two
   rows to decide explicitly: **IF-080/IF-081** (`integrate.py`,
   `trunk_step.py`) declare `downstream adopter` but read as internal;
   and whether a **generated surface** is a port while its generator is not.
3. **The five Experimental rows.** They hold the rung down today, and four of
   the five (IF-118/119/120 + IF-057) are internal carrier plumbing, not frame.
   Three dispositions: promote to `Stable` (the carrier sweep has converged);
   leave and accept the rung stays down; or rule that **only external-counterpart
   rows should gate rung 1** — which requires the `external` field
   `derive_gate.boundary_incomplete` says nobody has built yet. **IF-103**
   (`migrate_carrier`) is deliberately provisional and should stay Experimental
   until the conversion program ends.
4. **The 13 missing crossings + 6 partial ones.** WI-442 (queued) owns OI-28's
   two seeds; the other ~17 need an owner. Ruling scope here decides whether
   rung 1 can honestly close at all.
5. **The duplication policy for the re-statement pass** — §3's option 3, or an
   alternative — stated as a rule WI-451 slice 2 can apply per row, plus whether
   SR-035's merge rides that window.
6. **Where the boundary record LIVES once ruled.** SN-040's acceptance requires
   it *"kept with the architecture, not in session prose"*, and
   `docs/architecture.md` has no boundary section today. The frame belongs there
   (prose + a table); the typed crossings belong in `interfaces.toml`. **No new
   registry.**
