# Resume brief — the SR re-tier, the interface model, and the hardware crosscheck

**Written 2026-08-15 to be resumed from a cold session.** Everything needed to
pick up is here or pointed at precisely. Read this before touching anything.

---

## 0. WHERE THINGS PHYSICALLY ARE — read this first, it is the most common trap

Three git worktrees of the same repository exist on disk simultaneously:

| Path | Branch | State |
|---|---|---|
| `/Users/diytechy/Documents/ai-template` | `infra/mechanized-loop` | **TRUNK.** Still has **149 SR rows**, the retired `Area` column, `Boundary-Refs` empty on every row. Untouched by the re-tier. |
| `/Users/diytechy/Documents/ai-template-drive/wi451-sr-retier-campaign` | `wi451-sr-retier-campaign` | **THE WORK.** 64 SR rows, 9 commits, **unmerged**. Everything below about the re-tier lives here. |
| `/Users/diytechy/Documents/ai-template-drive/wi455-architecture-retirement` | `wi455-architecture-retirement` | Open. Holds the D-3 remainder (`direction`/`counterpart` shed). |

**If you open `system-requirements.toml` from the first path you are reading the
pre-campaign registry.** That has caused confusion once already.

Python for every script: `/Users/diytechy/Documents/ai-template/.venv/bin/python`.

---

## 1. What landed on the re-tier lane (9 commits, all green, WI-451 still OPEN)

The system-requirements tier went **149 → 64 rows**. Seven acts:

1. **26 supersession-bookkeeping rows deleted** (ids spent forever), with their
   validator, the `SupersededBy` column, 2 test cases and 6 pinning tests. One
   log entry is the forwarding map.
2. **The SR layer decided and reattached** — 34 held, 14 re-stated, SR-141
   merged into SR-148, **15 minted** (SR-151…SR-165), `Boundary-Refs` populated
   on all 64.
3. **73 rows demoted to the design tier.** Finding worth keeping: **zero new
   design rows were needed** — every obligation fit an existing carrier, which
   is the census's "these were always LLRs" claim confirmed mechanically.
4. **Adversarial round 1 (CHANGES-REQUESTED, 5 MAJOR)** — all confirmed, all
   fixed. See §5 for the lesson.
5. **`Area` retired for a closed `Aspect` vocabulary** (owner ruling
   2026-08-14h): six values, derivable values **dropped not remapped**, 21 of 64
   rows carry one, 42 carry none by design.
6. **Re-iteration pass** — two owed calls closed, the `Aspect` conversion
   finished in the shipped docs, an independent top-down read run.
7. **The top-down read's mechanical half closed** — 19 cells across 12 rows.

Final measured state on the lane: `SN=27 SR=64 LLR=153 TC=148`, `orphans=0
integrity=0 schema-findings=0 form-findings=2` (two recorded waivers), full
suite **2491 passed, 11 skipped**.

---

## 2. THE HARDWARE CROSSCHECK — largely ALREADY DONE, and it validated the model

**The Core project is on disk at `/Users/diytechy/Documents/Core`.** It is a real
mixed software-plus-physical adopter of this kit (the Gilbert/Adamah robot),
stamped `767487c` 2026-07-06, at `DevBar-Release`, 37 SN / 31 SR / 63 LLR / 70
TC, carrying a **283-line whiteboard, "AI-Template Fit and Hardware
Traceability"**, written expressly to test hardware fit, plus a ratified
glossary.

**Do not re-run the investigation from scratch — it was examined 2026-08-12 at
the owner's direction and its conclusions are recorded in `OI-14` in
`docs/requirements/open-items.toml`.** Carried here so a new session does not
have to re-derive them:

- **It reproduced this repo's central finding independently.** Core's ratified
  glossary defines `Module` as one of 8 swappable **assemblies** (BASE, TORSO,
  ARM-PROX, ARM-DIST, HAND, HEAD, PWR, HARNESS) while its actual `Module`
  *column* holds 63 source-file paths — two granularities under one column name,
  reached by a different project in a different domain.
- **The resolving definition, domain-neutral:** a COMPONENT is the coarse
  swappable boundary owning an interface contract, a test rig and a budget; a
  MODULE is the fine implementation home a requirement discharges into — a
  source file *or* a part source, interchangeably.
- **"One boundary, four views"** is Core's organizing principle and the reason
  no hardware component *type* is needed: cut the system so each assembly is
  simultaneously a mechanical unit, an electrical node, a software sub-graph and
  a registry `Module`.
- **The sharpest correction: the model breaks at MADE-versus-BOUGHT, not
  software-versus-hardware.** A *designed* part can BE code — Core's
  `hardware/parts/tendon_finger_rig.py` is parametric build123d Python, a design
  row binds to `build_rig`, and a test asserts joint travel and tendon path
  length.
- **One mechanism already spans both domains at zero cost:** "grams and N·m
  budget exactly like milliseconds." Where a rule is defined over numbers with a
  direction, hardware needs no special case.
- **THE HONEST LIMIT, and it is load-bearing:** Core's hardware half is
  **DESIGNED, NOT EXERCISED** — `procurement.csv` has zero rows,
  `hardware/assemblies/` and `tests/hardware/` are empty, `electrical/` is a
  README, no mass budget row exists. **Validate against Core's REASONING, which
  is battle-tested against this kit; do NOT treat its hardware registries as
  proof the model survives contact, because it has not been contacted.**

### What the crosscheck still genuinely owes

The 2026-08-12 examination answered **the component/module question** (OI-14
Part A). It did **not** answer the question raised 2026-08-15: **does a
`provides`/`serves` interface model fit *physical* interfaces?** That is new.

Specific things to look for in Core's whiteboard and registries:

1. How does Core express an interface between two **assemblies** (a connector, a
   harness, a mounting) — one row or two? Who owns it?
2. Does anything in Core's registries have a **mutual** interface with no
   natural provider? That is the case the proposed model handles worst.
3. Core lacks the `Component` column (its kit version predates it) — so check
   whether its interface rows carry endpoint fields, and whether dropping
   `this_project`/`counterpart`/`direction` would cost it anything it uses.
4. The `HARNESS` assembly is the interesting one by name — a harness *is* an
   interface. See how it is modelled.

The owner's expectation is that this surfaces no blocking issue. The evidence
above supports that; the open risk is confined to item 2.

---

## 3. THE INTERFACE AUDIT — scoped, prototyped, not shipped

Full proposal: [2026-08-15-interface-model-proposal.md](2026-08-15-interface-model-proposal.md)
(committed to trunk, explicitly **unruled**). Headline measurements, already
taken, reproducible against trunk's `interfaces.toml`:

- `direction` is **`Provides` (41) / `Consumes` (74)** — already provider/consumer
  shaped, not in/out.
- **115 distinct (provider, consumer) seams; zero with more than one provider.**
- **74 of 115 consumed with NO declared provider** — 32 sourced from a file
  (legitimate; needs a source/sink concept), **42 from a script that declares no
  output at all**. `spine_carrier` is consumed by **14** modules and declares
  nothing; `trace` and `check_trajectory` by 5 each.

**The audit is the migration's work list, not just diagnostics:** those 42 need
provider rows minted *before* any schema inversion has somewhere to put their
consumers.

**What "scoping the audit" means concretely:**

1. Turn the prototype into a real read-only check producing the 74-row table,
   each row classified file-source / script-source-needs-provider / covered.
2. Decide its **home** — a new script, or a rule inside `check_trajectory`.
3. Decide **severity: warn-first**, with the count visible. A gating check is
   red on day one against a known backlog (see §6).
4. Resolve the coupling in §6 before `direction` is shed by D-3.

---

## 4. THE RE-TIER, CONTINUED — and how the field changes hit it

**Five findings remain open, all needing an owner ruling.** None is mechanical.
Full detail is in the lane's ledger at
`docs/plans/2026-08-14-wi451-slice2-ledger.md`:

| # | Finding |
|---|---|
| H1 | The frame's own named B-05 observable — "the package exists, is complete and consumable", the MAPPING manifest — **has no row**. 15 were minted and the one the frame spelled out was not. |
| H4 | **SR-148 / SR-153 / SR-059 all state (SN-025, loop work-selection)** — the same class as the SR-141 merge already performed. |
| H5 | **SR-031 and SR-137 both claim the tomllib-vs-sh observable** and have already diverged — only SR-031 names the fail-OPEN decoy. |
| M1 | **Four rows escaped demotion** against the campaign's own criterion — SR-008, SR-021, SR-030, SR-133 (SR-133's rationale literally reads "Decomposed from SR-006"). |
| M3 | **Three needs have zero textual coverage** despite `orphans=0`: SN-026's consent surface, SN-037's discrete/variable signal typing, SN-029's delegated-approval record. |

**Plus two crossing attributions revised in act 7 and flagged for overrule** —
nothing mechanical can catch a wrong answer here, since the checker verifies a
crossing *resolves*, never that it is the right one:

- `SR-137` `["B-01","B-02"]` → `["B-01","B-04"]`
- `SR-139` `["B-02"]` → `["B-02","B-05"]`

**Also owed on the lane:** `SR-165` needs a design row + test case before it
leaves `Draft` (its verification flipped Inspection → Test in act 7,
deliberately). Round 2 of the adversarial review is owed before merge — round 1
is spent, because the fixes postdate its verdict.

### The interaction that decides sequencing

If the interface model lands, **every one of the 64 SR rows gains a `provides`
field**. The ratification wave — 15 Draft + 23 Modified SRs, 15 Draft + 72
Modified design rows, 14 Draft tests — is ruled to execute as ONE sequence with
the status-vocabulary migration. **Signing those rows before they gain
`provides` means signing them twice.**

That is the single most important scheduling fact in this document. Options,
for the owner:

- **(a) Merge and ratify now, accept a second touch later.** Gets the re-tier
  banked; costs a second signing pass on the same rows.
- **(b) Hold ratification, land the interface model first, sign once.** Costs a
  longer-open lane — and it has already gone 46 commits stale once.
- **(c) Merge the lane now but hold the ratification wave** until the interface
  field lands. Banks the work, avoids double-signing, keeps the lane short.
  **This is the author's recommendation** and it is not yet ruled.

---

## 5. PROCESS TRAPS — every one of these actually bit this session

- **RUN THE FULL SUITE, not smoke.** `pytest -q -n auto -m smoke` was green
  through a destroyed code map, a stale schema assertion and a broken phase
  contract. The full run (`pytest -q -n auto`, ~7 min) caught all three. Smoke
  is the per-commit bar; **full is required before claiming anything done**.
- **`gen_arch_map.py` must be run with `--src project-trajectory/scripts`.**
  With default args it scans a non-existent `src/`, emits an EMPTY map behind a
  warning, and **destroys 1,413 lines** of committed content. This happened.
- **Never name `WI-451` in `docs/status.md`'s hand-authored prose** — an id in
  that prose is refused at claim time, making the open lane unclaimable. The
  generated frontier block is exempt and names it there.
- **Measure, do not report intent.** Four of five reported counts were wrong
  because they came from what the change manifests *intended* rather than from
  the applied diff. Re-derive from `git show <base>:<file>` versus the tree.
- **Assert `old` before replacing a cell.** The applier pattern used here
  (assert the current cell matches the draft's `old`, then substitute) caught a
  stale draft and refused it rather than overwriting.
- **Closed work-item specs carry `sr_refs` too.** Deleting 100 rows left 111
  dangling pointers across 81 specs in `complete/` and `cancelled/`; the first
  sweep only covered the open folders.
- **Log fragments, not `docs/log.md`.** On a work branch write
  `docs/log.d/<WI-id>-<slug>.md`; the merge compiles them. **7 fragments are
  currently pending on the lane.**

---

## 6. FACTS NOT TO RE-DERIVE

- **One-home-per-behaviour is unsatisfiable against today's tree:** 12
  duplicated behaviours across **39 (behaviour, home) pairs in 16 modules**. A
  separate program (WI-448, the common-module program) owns deleting the copies.
  Any provider-uniqueness check is therefore red on day one against a backlog it
  does not own — ship it warn-first.
- **`cross_component_findings` is deliberately vacuous** for endpoints with no
  component tag — **46 of 113 rows** — so `component-findings=0` honestly means
  "no findings among the 67 classifiable rows."
- **OI-14 is already `ruled`, and its Part B is literally "what an interface row
  must say."** The 2026-08-15 proposal is an **amendment to a ruled item**, not
  a fresh design, and must be raised as one.
- **The partition method is ruled to be N2/DSM literally, not by analogy**
  (`docs/knowledge/system-decomposition-methods.md`). In N2, direction is encoded
  by matrix position and the matrix belongs to the containing block — so
  "orientation owned from a parent" is the convention, not an accommodation.
  That doc also records that physical components are a **non-structural
  constraint** that may override a lower-cost cut, and that **signal
  granularity** (one row per contract, or per field/flag/exit-code) is an unmade
  modeling choice that decides the row count.
- **D-3 coupling:** D-3 sheds `direction`, but the §3 audit *depends* on
  `direction` to know which end provides. Shed it before the provider concept
  lands and the check loses its input. Re-scope D-3 to be the inversion rather
  than running both against the same 115 rows.
- **Crossing realization today:** only B-04 (1 row) and B-05 (7 rows) have any
  realizing interface. **B-01, B-02, B-06 and B-07 have none.** That is the
  second, unmet condition on the deferred crossing-ownership decision — the
  first (`Boundary-Refs` populated) is now met on the lane.

---

## 7. SUGGESTED ORDER

1. **Rule the five re-tier findings** (§4) — they are mint/merge/re-classify
   calls of the same kind already handled inline this month, not a sitting.
2. **Decide the ratification/merge sequencing** (§4, options a/b/c). This
   unblocks everything else.
3. **Read Core's whiteboard** for the four physical-interface questions in §2 —
   cheap, and it is the only primary evidence on the new question.
4. **Ship the audit warn-first** (§3) — read-only, touches no lane.
5. **Then** the schema inversion, folded into D-3, after the re-tier lane merges.

Round 2 of the adversarial review goes **last**, on the settled state — a round
is spent by the next commit, so taking it early wastes it.
