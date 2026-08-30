# Registry machinery reference — the SN → SR → LLR → TC spine and the derived stage

A **reference doc** (like `project-trajectory/EXAMPLE.md` and
`project-trajectory/ADOPTING.md`): not a working surface, not scaffolded, not a
registry. It describes what the kit's scripts *actually enforce* on the
traceability spine — every field, every rule, how the stage is derived from those
rows, and how the derived stage then decides which tests and coverage floors run.

Compiled 2026-08-01 by reading the scripts rather than the prose docs. Where a
claim is made, the enforcing file is named so it can be re-derived. Line numbers
are given as a reading aid and will drift; the function names will not.

**One axis, since WI-498 (2026-08-21).** The kit derived TWO values over these
rows — the eight-rung stage ladder and a three-value "bar" that selected checks.
The bar is deleted and this doc describes only the stage. Where a table below
still reads like a strictness selector, the value it names is a RUNG.

**Scope.** The four spine tiers in full, the stage derivation in full, the
harness's stage→tier→coverage path in full, and what sits outside the derived
range (`DevStg-Release`/`the owner's final read`, §9.5). The off-spine registries
(IF / PB / CMP / PART / ASSET / REPO) get a summary in §10. The **work-item**
registry (`docs/work/`) is a different machine with its own states and fields and
is deliberately not covered here.

---

## 1. The four tiers at a glance

| Tier | Home | Storage form | Id syntax | Owner hat |
|---|---|---|---|---|
| **SN** | `docs/requirements/stakeholder-needs.toml` | TOML, `[need.SN-###]` tables | `SN-<digits>` | Stakeholder |
| **SR** | `docs/requirements/system-requirements.toml` | TOML, `[requirement.SR-###]` tables | `SR-<digits>` | System Engineer |
| **LLR** | `docs/requirements/low-level-requirements.toml` | TOML, `[design.LLR-###]` tables | `LLR-<digits>` | Designer |
| **TC** | `docs/test/test-cases.toml` | TOML, `[test.TC-###]` tables | `TC-<digits>` | Test Engineer |

*(Carrier updated 2026-08-17 — the 2026-08-08 TOML cutover post-dates this
doc's compilation; an absent key IS the empty cell, and a duplicate id is a
parse error the carrier itself refuses.)*

Two engines read these rows and must never disagree:

- `project-trajectory/scripts/trace.py` **enforces structure** — it joins all
  four tiers and emits findings in six classes.
- `project-trajectory/scripts/spine_rules.py` **picks the rung** — it reads the
  same rows and computes which stage the repo has reached.

Shared rules USED to be duplicated between them per the retired F5
independently-copyable convention and pinned equal by `tests/test_rule_sync.py`.
Since WI-448 slice 3 they have ONE home — `project-trajectory/scripts/kitlib/spine.py`,
the spine ROW vocabulary — which both modules re-export under their existing
names, so a divergence between them (precisely the false-green the kit exists to
prevent) is now unrepresentable rather than pinned.

**Three cross-cutting conventions, stated once:**

- **`-000` is inert.** Any id ending `-000` is a template example row, skipped by
  every integrity, schema and orphan rule (`is_example`, in
  `project-trajectory/scripts/kitlib/spine.py`, re-exported by `trace_text.py`), so a fresh scaffold is vacuously
  clean. It is *not* skipped by the column-count structural check — a template
  row must still parse.
- **Multi-ref cells split on `;`, `,` or whitespace** (`refs()`, same file).
  Semicolon is the documented form; the other two are tolerated.
- **`Status` is a CLOSED vocabulary of exactly three values**, all matched
  case-insensitively: `Drafted`, `Approved`, `Founded`. Anything else is an
  **integrity finding on the always-on `--strict-integrity` floor** — not a
  legal-but-inert label. *(SR/LLR/TC only: the SN tier declares the same
  vocabulary and no live pipe reads it — §2.3.)* THE OPEN-VOCABULARY PROMISE IS
  RETIRED, in two acts:
  the closure landed 2026-08-15 (D-9 step 1) precisely because a word no
  predicate read — `Planned` was one, and `Bananas` would have read identically
  — sat in the registry announcing nothing; the rename to the ladder landed the
  same day (step 5), folding `Planned` into `Approved`. An adopter carrying
  `Implemented`/`In-Review`/… migrates the cells (`RESYNC_PACK.md`) rather than
  declaring them.

---

## 2. SN — Stakeholder Needs

The one tier stored as **prose**, which changes almost everything about how it is
validated.

### 2.1 Structure: section-as-state

There is **no Status column.** Maturity is the *heading the row sits under*:

| Section | State | Effect |
|---|---|---|
| any heading whose text contains **"draft"** (case-insensitive) | **Drafted** (DevStg-Below) | exempt from "every SN needs an SR"; **drops the derived gate to DevStg-Below** |
| any other heading (`## Core needs`, `## Edge-case expectations`) | **Approved** (DevStg-Reqs) | must have ≥1 SR referencing it — an uncovered approved SN is both an orphan finding (§6) **and caps the derived gate at DevStg-Below** (the WI-401 coverage rung, §8.1) |

Approving a need = **moving the table row up** in a reviewed commit. That commit
*is* the sign-off, and its date is the approval date — git-derived, no
column. Parsed by `sn_draft_ids` (a line-scanner that tracks the current heading
and collects `SN-###` tokens under draft ones). The id *universe* those states
partition is a **whole-text scrape** (`sn_all_ids`, one home in
`kitlib/spine.py` since WI-448 slice 3, re-exported by spine_rules and trace):
any `SN-###` token anywhere in
the file counts, tables and prose alike — so an SN id mentioned only in
approved *prose* and cited by no SR caps the derived gate at DevStg-Below (§8.1) exactly
as an uncovered table row does.

### 2.2 Fields

Two tables ship, with **different columns**.

**Core needs / Draft needs table:**

| Column | Vocabulary | Effect on the machinery |
|---|---|---|
| `SN-ID` | `SN-<digits>` | The join key. Duplicate across table rows = integrity finding. |
| `Need (plain language)` | free text | Read by the dashboard as the SN label; otherwise unvalidated. |
| `Why it matters` | free text | Read into the OKF bundle + approval view. Unvalidated. |
| `Priority` | `M` / `S` / `C` | **Never validated, never gates.** Documentation only. |
| `Acceptance intent` | free text | Read into the approval hierarchy view. Unvalidated. |

**Edge-case expectations table:**

| Column | Vocabulary | Effect |
|---|---|---|
| `SN-ID` | `SN-<digits>` | as above |
| `Lifecycle` | `Provision` / `Startup` / `Runtime` (a prompt, not an enum) | **Never validated.** Prompts the author to cover the whole product life. |
| `Scenario` | free text | — |
| `Expected behavior` | free text | — |

### 2.3 Rules that fire on SN

| Rule | Function | Class |
|---|---|---|
| SN id on >1 table row | `sn_integrity_findings` | **integrity** (wrong at any stage) |
| SN id under **both** a draft and a non-draft heading | `sn_integrity_findings` | **integrity** |
| `SN-###` with no SR referencing it (and not Drafted) | `analyze` | **orphan** (fails `--strict`) |
| leftover `SN-000` placeholder | `scan_sn_placeholders` | **placeholder** (fails `--no-placeholders`, on from DevStg-Tests) |

**Note the asymmetry:** SN gets *no* required-field check and *no* enum check —
`--strict-schema` covers SR/LLR/TC only. An SN row with an empty
`Why it matters` and a blank `Acceptance intent` passes every gate. Prose tier,
prose enforcement; the DevStg-Reqs consistency review is the human backstop.

---

## 3. SR — System Requirements

**12 columns.** The **grouping row** of the re-attest surfaces: the sitting,
the pending-owner-actions projection and the `--approve modified` brief all key
off the SR row — presentation, never attestation scope (a row's `Status`
answers for its own cells; a child amendment never flips the parent SR — owner
ruling 2026-08-17).

| Column | Required¹ | Vocabulary / default | Effect on the machinery |
|---|---|---|---|
| `SR-ID` | ✔ | `SR-<digits>` | Join key. Duplicate → integrity; malformed → integrity; **a row with content but a blank id** → integrity ("a live requirement that just vanished from every join"). |
| `Title` | ✔ | free text | Node label in the outline / mermaid / HTML views. |
| `SN-Refs` | ✔ | `;`-joined SN ids | **Upward join.** Empty (when real SNs exist) → orphan; unknown target → orphan. *Traced, not approved* (§9). |
| `Requirement` | ✔ | one testable shall-statement, on an EARS pattern | Approved prose — amending it opens a re-attest window. Two rules read the text: `form_findings` **gates** the decidable half of singular/unambiguous (one `shall`, no non-obligation modal, no unfalsifiable term, no open-ended clause, no actorless passive), and `ears_advisories` **warns** when the opening states a condition outside `When`/`While`/`If`/`Where` (process.md §3). |
| `Rationale` | ✔ | free text | **Required**, unlike the LLR's. Guards zero-to-zero (every row already carries one). |
| `AcceptanceCriteria` | ✔ | measurable condition | Approved. Fed to the critique brief as SR intent. A **warn-only** testability advisory flags comparative/absolute claims that name no predicate. |
| `Permutations` | ✘ | the `gen_cases.py` grammar² | Optional test-design dimensions, lifted verbatim into `gen_cases.py --spec`. Never validated by `trace.py`. |
| `Priority` | ✔ | **open** (`M`/`S`/`C` by convention) | Required non-empty under `--strict-schema`; the *value* is never checked. |
| `Verification` | ✔ | **closed**: `Test`, `Demonstration`, `Manual`, `Analysis`, `Inspection`, `Attest`, `Critique` | The highest-leverage cell — §3.1. |
| `Status` | ✔ | **closed**: `Drafted`, `Approved`, `Founded` | Drives the gate — §3.2. |
| `Phase` | ✘ | bare integer (`2`) on approved rows once armed | Optional delivery phase — §3.3. |
| `Aspect` | ✘ | closed: `process` \| `trajectory` \| `unattended-loop` \| `connectivity` \| `perf` \| `portability` | The ruled CROSS-CUTTING review grouping (sitting-2 decision 10, executed by the WI-451 re-tier; replaced the 31-value free-text `Area`, whose 25 component-derivable values were dropped rather than remapped). Blank is normal — a non-cross-cutting row carries none, and that is never a finding; a non-empty out-of-vocabulary value IS a `--strict-schema` finding. `trace.py` emits per-aspect SR counts and never gates on the count. |

¹ under `--strict-schema` (DevStg-Impl). ² `name=range[min..max]`; `name=set{a,b,c}`;
`name=bool`; `@full|@pairwise|@boundaries`.

Plus two **optional extension columns** not in the shipped template:

| Column | Effect |
|---|---|
| `Lifecycle` | Recognised in the traced/approved split; validated nowhere. |

### 3.1 `Verification` — what it changes

Three separate mechanisms read this cell.

1. **LLR exemption.** `Analysis`, `Inspection`, `Attest` (`LLR_EXEMPT`)
   decompose to a TC but **no LLR** — there is no code to write, only its
   acceptance to analyse — so the "SR has no LLR" orphan rule stands down.
   `Critique` is deliberately *not* exempt: its artifact is produced by code,
   only its acceptance is subjective. The set is mirrored byte-for-byte in
   `spine_rules.LLR_EXEMPT`.
2. **The verification-basis split** — always reported, never gates:
   - **mechanized** = `Test` — rests on a runnable check.
   - **attested** = `Attest` — rests on a named human's recorded judgment.
   - **demonstrated/observed** = everything else — a human observed an outcome:
     repeatable, but not a runnable check.
   A blank or unrecognised method falls to *demonstrated* — the conservative
   bucket, so an unknown method is never counted as a runnable check.
3. **`--strict-schema`** rejects any value outside the closed set.

**Important:** `--require-verified` (the DevStg-Impl bar) applies to **every approved SR
regardless of method**. It was once Test-only, which let a `Demonstration` SR
sitting at `Implemented` pass `trace.py` while `spine_rules` refused it DevStg-Impl — the
two scripts disagreeing about the gate.

### 3.2 `Status` — the three magic values

| Value | Predicate | Stage effect | Rule effect |
|---|---|---|---|
| `Drafted` | `is_drafted` | **DevStg-Below — drops the repo gate** | Exempt from *child-completeness*: needs no LLR, no TC. SN linkage and all integrity rules still apply. Exempt from `--require-verified`. |
| `Approved` | `is_approved` | doesn't hold a rung open (`is_drafted` is what does) | The row's TEXT is blessed. It makes NO claim that tests passed: the 2026-08-15 ruling (OI-30 D2) carried onto the stage axis at WI-498 slice 3. **No cell reaches DevStg-Release**, and since WI-500 that is structural rather than vacuous — the rung's one input is `spine_stage`'s `evidence_passed` parameter, fed only by `kitlib.stage.evidence_verdict` over the harness-written `docs/test/evidence` record, and the pin demands that return be guarded by the bare parameter so a row-computed guard is unrepresentable. |
| `Founded` | `is_founded` | same as `Approved` (settled, never caps) | `Approved` PLUS a demonstration: the artifacts the row calls for EXIST. **COMPUTED, not typed** — the four discharge tests are the SN coverage rung, SR decomposition, `check_doc_refs`' LLR anchor rule and the TC `Evidence` half. Armed for the spine 2026-08-20 (D-9 step 8); no live cell takes it. Nothing WRITES it — whether a tool ever will is D-9 consequence 2's still-open half — but whether an AGENT-authored `Founded` is itself an error is answered: OI-45 (ruled 2026-08-20) sanctions it for spine content past the declared human-approval level (`agent_common.human_holds`). |
| anything else | — | (an integrity finding — see §3.2's closure) | Not inert: reported. |

**There is no value for a post-approval amendment.** A transitional `Modified`
carried that state until 2026-08-20 (D-9 step 7), feeding a `modified=N` basis
count and the `--approve modified` brief. It retired once the snapshot-backed
drift rule had run live beside it through the signing act: an amended row now
stays `Approved`, and what marks it is the DIFFERENCE from its copy in
`docs/archive/last_approved/` — a property of two files, for every row rather
than the ones somebody remembered to mark. Blessing an amendment is a reviewed
commit that re-reads the changed cells and runs `intake.py snapshot`.

### 3.3 `Phase` — optional phased delivery

- Parsed by `phase_num` — **the first digit run wins**, so `v2`, `2` and
  `phase-2` all parse to `2`. The lenient parse is **grandfathering** (owner
  ruling 2026-08-01, WI-402): historical labels keep filtering and deriving,
  but a live approved cell must be a bare integer — next bullet.
- **The rule arms itself, and is NUMERIC-ONLY.** `phase_approved_findings` is
  vacuous until ≥1 spine row is phased (digit-parse arming — a `v2` cell arms
  it too); once *anything* is phased, **every approved SR/LLR/TC `Phase` must
  be a full-cell bare integer** — digits only, no prefix — under
  `--strict-schema` (DevStg-Impl, where the schema tier already bites). A Drafted row may
  always leave it blank. Numeric-only is a correctness rule, not a style: two
  joins match the cell **literally**, never by parse — the `--phase`/`--approve`
  scope filters (`in_phase`/`_scope_srs`) and check_trajectory's phase-drop
  join of `docs/stage`'s `per-phase-live=` labels against phase-anchor WI titles
  — so a reformatted `P1`/`v2` cell went silently vacuous there, disarming the
  warn without telling anyone. (Legacy `[v3]`-style title anchors in
  `docs/archive/work/complete/` (WI-504 relocated the terminal directories
  under the archive, 2026-08-22) are history — never rewritten; the rule bites live
  registry cells only. The anchor's own vocabulary changed at WI-498 slice 4:
  a new title takes `[<phase>]-[DevStg-<Rung>]`, and the retired
  `[g1|g2|reqs|tests]` spellings are translated on read — `reqs`/`g1` to
  `DevStg-LLReqs`, `tests`/`g2` to `DevStg-Impl`, by MEANING rather than by the
  spelling each shares with a different rung.)
- `--phase 1,2` scopes `--require-verified`. A blank Phase is always in scope
  (downstream compatibility), and the **foundation phase** — `min()` over all SR
  phases — is never deferred. The `tag in phases` match itself stays literal
  (CLI label-agnostic) — which is exactly why the cells must be numeric.
- **The phase boundary is a confirmation event** (owner ruling 2026-08-01). The
  current phase is derived — `max()` over non-draft spine rows, the `phase = N`
  field in `docs/stage` (§8.3) — and it increments only when
  re-opened scope is **confirmed**: an adjudication verdict that scope moved,
  or a new draft-SN batch approved into scope — **never on the raw derived-stage
  drop**. A spurious re-attest window must not burn a phase number (WI-280 is
  the counterexample: 19 traced cells, 11 SRs flipped, no scope moved).
  `derive_stage.py --next-phase` prints that max + 1 — the one derived call
  every agent and the intake mint helper (WI-388) use for a newly confirmed
  phase's number (an unphased spine is the implicit foundation `1`, so it
  prints `2`; a Drafted row's phase is not yet scope and never bumps the answer).

---

## 4. LLR — Low-Level Requirements

**11 columns.** The decomposition tier: *how* an SR is met, in named code.

| Column | Required | Vocabulary / default | Effect |
|---|---|---|---|
| `LLR-ID` | ✔ | `LLR-<digits>` | Join key; the same three integrity rules as SR. |
| `SR-Refs` | ✔ | `;`-joined SR ids | **The canonical SR↔LLR link.** Empty → orphan ("no SR parent"); unknown target → orphan; citing a **superseded** SR → integrity. |
| `Title` | ✔ | free text | Node label. |
| `Module` | ✔ | repo path | Doubles as a **join target**: the set of `Module` values is added to the PB back-link target set and to the IF-endpoint advisory join. Normalised by stripping a leading `project-trajectory/` segment and any of `.py .sh .ps1 .ts .js .go .rs .cmd`. |
| `CodeSymbol` | ✔ | function/type name | Required non-empty, and **resolved against real code** — `check_doc_refs.py`'s `symbol_findings` is the LLR tier's *discharge* test (§4.2). Also read by `gen_okf.py` for the knowledge bundle. |
| `Detail` | ✔ | decomposition detail, **not** an SR paraphrase | Approved prose. |
| `Rationale` | ✘ | free text | **Deliberately not required** — "a short decomposition row's why IS its parent SR's, so requiring one everywhere would manufacture the restatement the column exists to prevent." Approved when present. |
| `TestRefs` | ✘ | `(see TC)` | **Inert** — see §12.1. |
| `Status` | ✔ | closed, as SR | `Drafted` HOLDS THE `DevStg-LLReqs` RUNG OPEN (`spine_stage`: `any(is_drafted(r) for r in llrs)`) and exempts the row from "no TC". Otherwise **does not move the stage** — §4.1. |
| `Component` | ✘ | `CMP-###` | Optional membership tag, validated against the CMP registry only when that registry is non-empty. |
| `Phase` | ✘ | digit-parseable | = the parent SR's Phase by convention. Same arming rule. |

### 4.1 LLR Status does not gate — on purpose

`spine_stage` in `spine_rules.py`: an LLR holds its rung open **only** when
`is_drafted` reads it as DRAFTED (the new-phase signal). Once
present, its own Status is irrelevant — the SR's `Approved` drives the SR rung,
matching `--require-verified`, which checks SRs and not children. A downstream
repo whose LLRs all read `Implemented` is unaffected here (that value defaults
to APPROVED for this rule deliberately; the closure names it on the integrity
floor instead, so one fault is not punished twice).

There is a **warn-only** lint for the resulting readout drift
(`llr_status_advisories`): an LLR below `Approved` while *every* citing TC is
already `Approved`. Never promoted to an error, "because making LLR status gate
would re-introduce the exact LLR-status coupling the derived-stage model dropped."
A `Founded` LLR is exempt — it reads ABOVE `Approved`, so there is nothing to
lift and the nag would push it DOWN the ladder. (The exemption named the
transitional `Modified` until that value retired, 2026-08-20.)

### 4.2 `CodeSymbol` must BIND — the discharge test, and what the cell may name

`symbol_findings` in `check_doc_refs.py` (WI-429; approved as built by owner
ruling **OI-20**, 2026-08-13). A live LLR row must carry **at least one**
identifier-shaped `CodeSymbol` token that binds at module scope in one of the
`.py` modules its `Module` cell names — `CodeSymbol` supplies the tokens,
`Module` supplies the **search scope**, and the `;`-joined module list is read
as a **union**, never as a positional pairing. Warn-first; **hard under
`--strict`** at the `[step:doc-refs]` DevStg-Impl step.

**The grammar, ruled with the approval.** ADMISSIBLE in `CodeSymbol`:

- a **resolvable code symbol** — function, class, method or module constant.
  Private `_`-names and constants count: the oracle is
  `gen_arch_map.module_bindings`, not the rendered public-API module map, which
  drops exactly what 41 of this repo's live rows name;
- a **module path** — the module itself is the realization artifact;
- a designed **PART SOURCE** — a physical part authored as parametric code. It
  binds like any other symbol. (A *bought* part never reaches this tier: it is a
  `PART` row owned by an `IF` row.)

NOT admissible: a **generated artifact** (its generator is the realization) or a
**prose contract** (a description of behaviour is not a name). Four live rows
are therefore **honestly unfounded** rather than founded by widening the grammar
to fit them — the cell names a function local, a label that never existed, or an
HTML attribute that merely looks like an identifier.

**Why anchor and not per-token.** A per-token rule reds 31 of 149 rows on
arrival, 18 for tokens that were never symbol claims — enforcing a grammar no
ruling had given the cell. Per-token misses file as *untraced* and are counted
every run, so a later tightening stays available rather than hidden. Same trade
ruling **R2** made on the sibling `Evidence` cell: validate the coarse claim,
rule the fine one prose.

**This rule is the decomposition FLOOR.** Under OI-21's ladder, rung 4
terminates where a token binds: a requirement that still needs allocating to
sub-parts is an SR for that sub-scope; one that binds to code is the bottom. An
*advisory* version would make D-9's `Founded` rung vacuous for one of four
tiers, which is why it gates.

**The non-`.py` skip is REPORTED, never silent** (the OI-28 guard, WI-449). A
row naming only non-Python modules — a hook, a shell template — has no Python
name to bind, so discharge is not computed for it. That skip is correct and
unchanged, but it used to produce **no output at all**, which is a fail-open now
that template paths are ruled admissible in `Module` as realization artifacts.
Each such row now prints one `ADVISORY -` line naming the row and its modules
(folding to a single counted line past 15 rows). Advisory is a **third ink**
with its own meaning here: `WARN` gates under `--strict`, `UNTRACED` never gates
and is hidden without `--show-untraced`, `ADVISORY` never gates and is never
hidden.

---

## 5. TC — Test Cases

**11 columns.** The evidence tier.

| Column | Required | Vocabulary / default | Effect |
|---|---|---|---|
| `TC-ID` | ✔ | `TC-<digits>` | Join key; the same three integrity rules. |
| `Verifies` | ✔ | `;`-joined **SR / LLR / IF** ids | The downward join. Empty → orphan ("verifies nothing"); unknown token → orphan; **only IF ids** → orphan (a seam citation *supplements*, never replaces, the spine citation). |
| `Level` | ✔ | **open** (`Unit`, …) | Required non-empty; the value is never validated. |
| `Method` | ✔ | **open** | Required non-empty; the value is never validated. |
| `Tier` | ✔ | **closed**: `Smoke`, `Full`, `Release` | The only closed TC vocabulary. Wrong value → schema finding. Selects release-checklist items (§9.5); **not** joined to the pytest marker that selects tests — see §12.2. |
| `Parameters` | ✘ | `param=a; other=x` | Read as the artifact recipe in the critique brief. Not validated. |
| `Expected` | ✔ | cite the AcceptanceCriteria **by id** | Approved prose. |
| `Automated` | ✔ | `Yes` / `No` (open) | **Conditional rule:** `Yes` + empty `Evidence` → schema finding ("a claimed-automated test with no cited location is a soft false-green"). |
| `Evidence` | ✘* | pytest node / path / procedure link | *Required only when `Automated=Yes`. |
| `Status` | ✔ | closed, as SR | `Drafted` → DevStg-Below. Otherwise does not gate (same as LLR). |
| `Phase` | ✘ | digit-parseable | = the max Phase of what it verifies. Same arming rule. |

### 5.1 The SR/LLR/TC triangle rule

A TC may cite an SR *and* an LLR together, so one test discharges both the "SR
needs a TC" and "LLR needs a TC" rules. `triangle_findings` keeps that honest:
**when a TC cites both, each cited LLR's `SR-Refs` must intersect the SRs the
same TC cites.** Citing `LLR-1` beside `SR-2` when `LLR-1` decomposes `SR-1` is
incoherent at any stage — so it joins the **integrity** floor, not the
gate-scoped orphan set.

---

## 6. The join / orphan rules, consolidated

| # | Rule | Exempt when | Class |
|---|---|---|---|
| 1 | every approved **SN** has ≥1 SR | SN is Drafted (section-as-state) | orphan |
| 2 | every **SR** links ≥1 SN | the SN registry has no real ids yet | orphan |
| 3 | every **SR** SN-Ref resolves | ditto | orphan |
| 4 | every **SR** has an LLR | SR is Drafted **or** `Verification ∈ {Analysis, Inspection, Attest}` | orphan |
| 5 | every **SR** has a TC | SR is Drafted | orphan |
| 6 | every **LLR** has ≥1 SR parent | — (never) | orphan |
| 7 | every **LLR** SR-Ref resolves | — | orphan |
| 8 | every **LLR** has a TC | LLR is Drafted | orphan |
| 9 | every **TC** verifies something | — | orphan |
| 10 | every **TC** ref resolves (SR/LLR/IF) | — | orphan |
| 11 | a **TC** citing only IF ids also names a spine id | — | orphan |
| 12 | an SR/LLR pair in one TC shares the LLR's recorded parent link | — | **integrity** |
| 13 | no LLR grounds on a superseded SR | — (Drafted LLRs are **not** exempt) | **integrity** |

Rules 1–11 are **gate-scoped** — they fail `--strict`, which the harness runs
from DevStg-Tests. Rules 12–13 are **always wrong** and sit on the integrity floor the
pre-commit hook runs on every commit.

Rule 1 also has a **gate-input twin** since WI-401: an uncovered approved SN
caps the *derived gate* at DevStg-Below (§8.1) — same cited set, same Drafted exemption, so
the itemized listing and the cap can never disagree on one registry state.

---

## 7. Finding classes, flags, and exit codes

`trace.py` sorts findings into a bag; `exit_code` decides what is fatal.

| Class | Fails `--strict` | Fails `--strict-integrity` | Contents |
|---|---|---|---|
| `integrity` | ✔ | ✔ | dup/malformed/blank ids, triangle incoherence, CSV column-count mismatch |
| `orphans` | ✔ | ✘ | rules 1–11 |
| `status_findings` | ✔ | ✘ | `--require-verified` misses |
| `placeholders` | ✔ | ✘ | leftover `-000` rows (collected only under `--no-placeholders`) |
| `schema` | ✔ | ✘ | empty required fields, bad enums, `Automated=Yes` without Evidence, approved-phase misses (only under `--strict-schema`) |
| `budget` / `module` / `component` / `interface` | ✔ | ✘ | off-spine back-link failures |
| **advisories** | ✘ | ✘ | LLR-status drift, AcceptanceCriteria testability, EARS statement pattern, paraphrase, artifact-naming, fan-out, verification coherence, knowledge-pack refs, IF endpoint join |

**Advisories never join the exit code, even under `--strict`** — "a warn-tier
checker feature mints no SR and gates nothing."

---

## 8. How the gate is DETECTED

The gate is **computed from the registry rows, never declared.** You do not set
it; you approve artifacts and regenerate.

### 8.1 The per-artifact rules

`spine_rules.py` asks each in-scope artifact what level it has reached.

| Tier | DevStg-Below | DevStg-Reqs | DevStg-Tests | DevStg-Impl |
|---|---|---|---|---|
| **SN** | under a "draft" heading, **or approved with no covering SR** (the WI-401 coverage rung) | — | — | approved **and cited by ≥1 SR `SN-Refs`**: such an SN owes nothing past DevStg-Reqs, so it contributes DevStg-Impl and **never caps** |
| **SR** | `Status=Drafted` | approved, **not decomposed** | **decomposed** = has its required LLR (unless `Verification ∈ LLR_EXEMPT`) **AND** a TC — **and this is the ceiling** (OI-30 D2) | *unreachable by cell*: the release bar is the harness's answer, not a Status value |
| **LLR / TC** | `Status=Drafted` | — | — | once present, contributes DevStg-Impl and **never caps** |

A below-`Approved` SR needs no rule of its own: it is decomposed-but-not-approved, so
it reads **DevStg-Tests**. That is the deliberate gate pull that makes a pending re-attest
visible.

The SN column's two DevStg-Below rungs are deliberately disjoint (WI-401, owner ruling
2026-08-01). A **Drafted** SN fires only the draft rung — it is exempt from the
coverage rung exactly as it is exempt from trace.py's orphan rule, so one fact
never fires two findings at once. An **approved** SN cited by zero SR `SN-Refs`
is an unanswered need: DevStg-Reqs is not earned, so it caps the raw level at DevStg-Below. The
split of labor with `trace.py` is the module pair's usual one — this rung is
the *gate input*; the itemized `SN … has no SR` listing stays trace.py's orphan
finding at DevStg-Tests strictness — and both read the **same cited set**
(`sn_cited_ids`, which since WI-448 slice 3 has ONE home in `kitlib/spine.py`
that both modules re-export — it was an F5 duplicate pinned equal by
`test_rule_sync`, and the pin retired with the copy), so the gate
and the listing cannot contradict on one registry state. The cited set is
built from the rows in scope: in the raw view a Drafted SR's citation counts
(the draft itself already drops the gate), while the `ex-draft` counterfactual
rebuilds it over the non-draft subset — so removing a draft answer never
fabricates coverage.

### 8.2 Aggregation

**The repo gate = `min()` over every in-scope artifact.** One Drafted row anywhere
therefore drops the whole repo to DevStg-Below. Phase gates are the min over that phase's
artifacts, reported per-phase alongside the repo number.

Two floors keep the answer honest:

- A repo with **no real SRs yet** (a fresh scaffold) is **DevStg-Reqs** — the
  requirements-drafting start — never a vacuous DevStg-Impl.
- The **cached selection value is floored at DevStg-Reqs**, so a repo below the
  floor still selects its integrity checks. The unfloored reading, DevStg-Below
  drops included, is recorded beside it (`settled-stage`, `live-stage`) so
  nothing hides.

### 8.3 The cache: `docs/stage`

The computed record is written to `docs/stage`, a `key = value` file whose
`stage =` field is the rung the repo is IN. Comment lines carry the header;
every fact is a field:

```
stage = DevStg-Arch
stage-ord = 3
stage-of = 8
floored = no
settled-stage = DevStg-Arch
live-stage = DevStg-Reqs
phase = 5
per-phase = 1=DevStg-Arch;3=DevStg-Arch;4=DevStg-Arch;5=DevStg-Arch
per-phase-live = 1=DevStg-Arch;3=DevStg-Arch;4=DevStg-Arch;5=DevStg-Reqs
drafted = 15
fingerprint = sha256:0ead5927…
```

`stage` is the SELECTION value: the rung the SETTLED spine has earned, folded as
the min over the phases that have earned one, then floored. `settled-stage` is
that same fold before the floor, `live-stage` the honest reading over ALL rows —
drafts included and unfloored — and `drafted` is how far the two are allowed to
differ. `per-phase` / `per-phase-live` break both out per phase, with
`DevStg-Below` as the has-nothing-settled-yet sentinel (never a rung).

`fingerprint` is a SHA-256 over the LF-normalized content of the declared
derivation inputs (`DECLARED_INPUTS` in
[`scripts/kitlib/stage.py`](../project-trajectory/scripts/kitlib/stage.py)) — the
six spine registries and, since WI-500, `docs/test/evidence`. **When that record
is PRESENT the fold also covers the declared `[paths]` source and test trees**,
because otherwise a recorded `DevStg-Release` would ride an unchanged evidence
file over an edited tree with the fingerprint still matching; a repo with no
record pays none of that walk. A reader recomputes it
and trusts the recorded values ONLY on a match, deriving fresh in memory
otherwise — so no **selection or approval** consumer can read a stale stage,
on any lane. **The display surfaces are the named exception**, by design:
`traj_parse._stage_value` and `traj_status._stage_facts` parse the recorded file
directly, without the fingerprint check, so a generated artifact describes the
commit it ships with. On a tree whose declared inputs have moved,
`PROJECT_STATE.html` and the generated status block therefore render the
recorded rung while `check.py` and `human_holds` derive fresh. Only three call
sites reach `read_stage` — `check.py`, `agent_common.py`, `check_trajectory.py`
— and those are exactly the deciding ones.

- `check.py` reads `stage` and runs every step whose declared `from-stage`
  threshold sits at or below it. An out-of-vocabulary value is a hard exit, not
  a fallback.
- **No file → the `derived-stage` step FAILS**, naming the command to run. A repo
  that deleted the record never gets a silently weaker bar.
- Freshness is guarded by `derive_stage.py --check`, wired as the `derived-stage`
  step at **every** rung and in the pre-commit hook. It recomputes and fails on
  drift. A file still in `stage.template`'s comment-only placeholder form counts
  as "not yet in derived form" and passes with a note, so a not-yet-migrated repo
  stays green.

### 8.4 The suppressed-gate window

Because the gate is a `min()`, a single Drafted row **drops the gate,
and the harness then drops every step tagged for the higher gate.** `lint` and
`--require-verified` simply stop running for the duration. That is
not a relaxed bar — it is a blind spot, and it has bitten this repo: twelve
commits went green over those steps during the 2026-07-26/27 window, and the debt
surfaced in one lump when the window closed. (The debt of record was the
duplication census's; that census was torn down later, D-7/WI-426. The blind
spot is the point, not which step fell into it.)

`window_open` in `check.py` detects it and warns. Its two signals are not equally
good evidence, which is the subtlety:

- **`modified>0` is conclusive on its own** — a COMPATIBILITY arm since D-9
  step 7 retired the value: this kit no longer emits the field, and
  `check._basis_counts` reads its absence as 0, but a gate file written by an
  older kit (or by a repo mid-migration) still carries one and still trips it.
  `Modified` was *defined* as a
  post-attestation amendment, so the row can only exist in a spine that has
  already been approved. A window by construction.
- **`drafted>0` is ambiguous** — a `Drafted` row reads DevStg-Below in a mature repo starting a new
  phase *and* in a project that has never approved anything. The `ex-draft` basis
  figure disambiguates: it is the level the same arithmetic computes with the
  draft rows removed. If that clears DevStg-Tests and sits above the level the drafts
  produced, the spine has demonstrably climbed and the drafts alone are holding
  it down.

Since WI-401 an **uncovered approved SN** opens the same kind of window (the
gate drops to DevStg-Reqs, the DevStg-Tests/DevStg-Impl steps stop running), with `uncovered>0` on the
basis line naming the cause. `window_open` does **not** read that field — its
signals remain `drafts`/`modified` — an honest gap: the warn is absent, but the
drop itself and its count are on the basis line in plain sight.

---

## 9. How the gate determines TEST COVERAGE

"Coverage" means three different things here, and the gate touches all three.
Keeping them apart is most of the value of this section.

| Sense | Question | Enforcer |
|---|---|---|
| **Requirement coverage** | does every requirement have a test at all? | `trace.py` orphan rules 4/5/8 (§6) |
| **Test-suite scope** | *which* tests run this time? | `check.py` tier selection |
| **Code coverage** | how much of the source did they execute? | `pytest --cov` global floor + `check_coverage.py` per-module floors |

### 9.1 Gate → which steps run at all

`check.py` builds a plan of `(name, requires, command, gates, layer)` tuples and
keeps only the steps whose `gates` set contains the resolved gate.

| Step | Gates | Layer | Notes |
|---|---|---|---|
| `format` | **DevStg-Impl** | product | |
| `lint` | **DevStg-Impl** | product | |
| `tests+coverage` | **DevStg-Impl** | product | the whole test run is DevStg-Impl-tagged |
| `registry-integrity` | **DevStg-Reqs** | process | `trace.py --strict-integrity` — the always-valid floor, so a broken CSV cannot hide until DevStg-Tests |
| `derived-stage` | DevStg-Reqs, DevStg-Tests, DevStg-Impl | process | the freshness guard on `docs/stage` (the effective-stage cache, WI-498 slice 1) |
| `privacy` | DevStg-Reqs, DevStg-Tests, DevStg-Impl | process | a leak is wrong at any stage |
| `doc-navigability` | DevStg-Reqs, DevStg-Tests, DevStg-Impl | process | |
| `traceability` | **DevStg-Tests, DevStg-Impl** | process | `trace.py --strict --no-placeholders --html` |
| `design-flows` | **DevStg-Tests, DevStg-Impl** | process | |
| `trajectory` | **DevStg-Tests, DevStg-Impl** | process | gains `--strict` here |
| `perf-budgets` | **DevStg-Impl** | process | |
| declared `[step:*]` | per section | product | this repo declares `doc-refs`, `figures`, `module-coverage`, all at **DevStg-Impl** |

Two consequences worth internalising:

- **The entire product bar — format, lint and the test suite — is DevStg-Impl-only.** At
  DevStg-Reqs and DevStg-Tests the harness runs process checks and does not run the tests.
- `--stage` on the command line wins (the retired `--gate` spelling is still
  accepted); a *defaulted* stage for `--run-step` / `--run-steps` resolves to
  `all`, never `docs/stage`, so the pre-commit hook's floor stays warn-first.

### 9.2 Tier → which tests run

Tier selection is **orthogonal to the gate**: `--tier` picks the subset, and the
tiers map to pytest marker expressions.

| Tier | Marker expression | Measures coverage? |
|---|---|---|
| `smoke` | `-m smoke` | **no** |
| `full` | `-m "not release"` | yes |
| `release` | *(none — everything)* | yes |
| `all` | *(none — everything)* | yes |

The default is **opt-out**: an **unmarked test runs in `full` and above**, so a
forgotten marker can never silently drop a test from the pre-merge suite.
Marking a test `release` is what opts it *out* of pre-merge. `docs/stack.ini`
`[tiers]` overrides the built-in map with stack-native expressions.

This repo additionally budgets the smoke tier in `[smoke-budget]`: a wall-clock
`seconds` target (enforced by `check_smoke_budget.py`) and a deterministic,
machine-independent `max-tests` membership ceiling (enforced by
`tests/test_smoke_budget.py`). Both are **growth sensors with headroom**, not
freezes — a ratchet stamped at current+1 bites on the first legitimate addition.

### 9.3 Coverage floors, and how the tier gates them

Coverage instrumentation is appended to the test command **only when the tier is
in `COVERAGE_TIERS` = (`full`, `release`, `all`)**. The smoke subset alone is not
expected to meet a full-suite threshold, so holding it to one would fail the
cheap gate for the wrong reason.

Two layers, deliberately:

1. **Global floor** — `docs/stack.ini` `[coverage] threshold` (85 here) passed to
   `pytest --cov-fail-under`. One aggregate number, the backstop.
2. **Per-module floors** — `check_coverage.py` compares each file's
   `summary.percent_covered` in `coverage.json` against `docs/coverage-floors`,
   because one aggregate number lets a heavily-tested generator subsidize thin
   coverage in a security or process boundary while the headline still passes.

`check_coverage.py` fails when any declared module is below its floor, **or is
absent from the report** (a declared floor whose module vanished from measurement
must fail, never quietly pass), or the floors file is malformed, or the report is
corrupt. It exits 0 when every floor holds, when none are declared, when the
report is absent, or when the selected tier does not measure coverage.

Two independent defences stop a **stale** report being graded as a current pass:

- `check.py` **run-scopes** `coverage.json` — it clears a stale copy before any
  plan that runs `tests+coverage`, so a smoke run leaves no previous full-tier
  file behind.
- `check_coverage.py --skip-tiers smoke` makes the comparator SKIP *without
  reading the report at all*, giving an honest tier-named skip even where the
  file lingers.

The step also declares `lane = tests+coverage` so that under `check.py --jobs 0`
(parallel, as CI runs it) it cannot race the producer, find no JSON, and SKIP —
silently not enforcing the floors.

### 9.4 The trunk-lane exemption

Generated-artifact freshness is the **trunk lane's** job. On a claimed work
branch — one with a `docs/work/active/<branch>/` spec directory — the steps in
`_TRUNK_FRESHNESS_STEPS` (`derived-stage`, `trajectory-map`,
`status-map`, `open-items`, `okf`, `approval-fresh`) are reported SKIP with their
reason instead of running. Gating a branch on freshness would red every branch
for drift it is forbidden to fix.

It is **fail-closed**: off git, on a detached HEAD, or unclaimed, the full bar
applies. `--trunk-lane` forces them back on, which is what the station refresh
uses — that tree *is* the tree that becomes trunk, so the branch stands in the
trunk lane for exactly that one run.

**The practical consequence:** a work branch runs a genuinely weaker bar than
trunk, including the `derived-stage` freshness check. The stage a branch reports
is the value as-of-base.

### 9.5 What sits OUTSIDE the derived range: DevStg-Release and the owner's final read

DevStg-Reqs–DevStg-Impl are the derivable gates. `DevStg-Release` and `the owner's final read` are **not derived, not
cached, and not known to the harness at all** — `check.py`'s vocabulary is
`GATES = ["DevStg-Reqs", "DevStg-Tests", "DevStg-Impl", "all"]`, so there is no `--gate DevStg-Release` to run.
They are release milestones recorded separately.

The distinction is one of kind, not of degree: **DevStg-Impl is a state the spine reaches
and holds; DevStg-Release is an event performed per release** (and skipped entirely
for a one-off deliverable). A repo can sit at DevStg-Impl indefinitely without ever
performing one.

Four things separate them, only the first of which is a test run:

1. **The `release` test tier runs** — the marker filter is dropped, so
   release-marked tests execute. DevStg-Impl's own exit criteria name the **full** tier.
2. **The generated release checklist is completed and signed** —
   `gen_release_checklist.py` harvests what no automated test covers: every
   `Demonstration`/`Manual`/`Inspection` SR, every TC with `Tier=Release` or
   `Automated` not-yes, the SN acceptance intents, provided IF contracts, and the
   PB budgets. The ticked copy, filed under `docs/releases/`, IS the sign-off
   artifact.
3. **Warn-tier perf budgets meet a human.** A PB row's `Gate` column
   (`fail`/`warn`) is independent of its `Tier`; noisy runtime metrics default to
   `warn` and therefore fail no gate at any tier. The checklist is the only place
   they are confirmed.
4. **Release admin and different sign-offs** — version bump, changed `Approved`
   interface versions communicated to counterparts, changelog. DevStg-Impl signs off
   System Engineer + Test Engineer; DevStg-Release adds the active domain hats and the
   **Human**.

**How a Release-tier TC is authored** — two populations, built nothing alike:

- **Slow / hardware / long-running automated tests.** Structurally an ordinary
  test carrying the `release` pytest marker. Because tiering is opt-out, marking
  `release` is specifically the act of removing a test from the pre-merge suite.
- **Procedure records for human-verified requirements.** Every SR owes ≥1 TC
  *regardless of method*, so a `Demonstration`/`Manual`/`Inspection` SR's TC is
  **not a test function at all** — it is a written procedure with
  `Automated=No`, usually `Tier=Release`, its `Expected` citing the SR's
  AcceptanceCriteria by id and its `Evidence` naming a procedure doc rather than
  a pytest node. `Automated=No` also means the conditional Evidence rule (§5)
  does not fire, so a manual TC may legally cite nothing.

One deliberate detail in the harvester: a **blank** `Automated` cell counts as
manual. An unclassified test lands on a human's checklist rather than being
assumed covered.

---

## 10. The traced-vs-approved cell split

Owner ruling 2026-07-31 (`docs/concurrency-v2.md` §A5.1, WI-380). The newest
layer, and the one behind a lot of historical accidental gate churn.

When an **`Approved`** spine row is amended, `staged_spine_amendments` in
`check_trajectory.py` sorts each changed cell into two halves. Only an
**approved** cell change warns that a re-attest is owed.

| Registry | **Traced** (amend freely) | **Approved** (opens a re-attest window) |
|---|---|---|
| SR | `SN-Refs`, `Boundary-Refs`, `Hat-Refs`, `Phase`, `Aspect`, `Lifecycle` | `Title`, `Requirement`, `Rationale`, `AcceptanceCriteria`, `Permutations`, `Priority`, `Verification` |
| LLR | `Module`, `CodeSymbol`, `TestRefs`, `Component`, `Phase`, `SR-Refs`, `Hat-Refs` | `Title`, `Detail`, `Rationale` |
| TC | `Verifies`, `Evidence`, `Automated`, `Phase` | `Method`, `Expected`, `Parameters`, `Level`, `Tier` |

**Why it exists:** WI-280 moved code, 19 LLR `Module` cells followed it, 11
owning SRs flipped off `Approved`, the gate dropped, and it cost an approve
brief and four review rounds — for a change that altered no requirement.

**The residual rule fails safe:** a column in *neither* set is treated as
**approved**, so a newly-added column can only ever be too loud, never silently
un-approved. `tests/test_trajectory_staged.py` pins both halves.

**Chain-consistency warns — RETIRED** (owner ruling 2026-08-17, the cell
reading): `modified_chain_advisories` told an author to flip the owning SR
whenever a child read the retired `Modified` marker, asserting the retired
chain reading. An amended LLR/TC under an `Approved` SR is a legitimate state — a row's
`Status` answers for its own cells — and an UNMARKED child amendment is the
snapshot-drift arm's find once `docs/archive/last_approved/` is seeded.

---

## 11. Off-spine registries (summary)

All optional; all vacuous when absent or `-000`-only.

| Registry | Id | Back-link cell | Rule |
|---|---|---|---|
| `docs/requirements/interfaces.toml` | `IF-###` | `Owner` (a path or `external:` party), `Requestors` / `Consumers` (exactly one), `interface_from_external` / `interface_to_external` | An id-shaped or multi-endpoint `Owner` joins the `--strict` failure set (OI-67), and so does a directional tie-back naming a crossing `external.toml` does not declare. **Warn-only**: a row naming both far sides or neither; a module-shaped owner that no LLR `Module` names and whose header declares no `Implements:` (the seam reaches no requirement); an endpoint that resolves to nothing in the tree (WI-455: the cell is present only where `Owner`→LLR→`Module` cannot derive it). Citable from a TC's `Verifies`. A row still carrying a RETIRED cell (`Contract`, `Provider`, `Req-Refs`, `Signal`, `SignalNote`) joins the `--strict` failure set (OI-67 slice 6). The `Data` cell carries FIVE warn-first rules: the four FORM rules (no work-item id, no `D-<n>` citation, no rationale connective, a 160-character ceiling) plus a CONTENT rule — a `SCHED_*` / `Foo.bar` / `CONSTANT_NAME` token must resolve in the declared source surface and a named path must exist, vacuous where there is no surface (`[arch-map] mode = files`) and silent on a path `docs/declared-absences` declares. **The definition gate** is `check_trajectory.contract_body_findings` (WARN plain, ERROR under `--strict`, sharing `[checks] interfaces_check`): the owner must declare the row on its `Contracts:` marker AND state a `Contract IF-###:` body there; an `external:`-owned row is stated by the kit module on its far side; a source declaring another in-tree owner's row is a finding. The optional `VerifiedBy` cell (a `TC-###` or an `LLR-###`; empty = "verified in its own right") is checked for RESOLUTION only, warn-first. |
| `docs/requirements/external.toml` — the depth-0 FRAME (WI-442) | `EXT-###` (entities), `B-##` (boundary crossings), `REL-###` (relationships) | crossing `Entity`; relationship `From`/`To` | THREE tiers on ONE path, keyed by id column. Every reference must resolve to a declared entity, joining the `--strict` failure set — **and crossings or relationships declared with NO entity at all are a finding of their own**, not a vacuous pass. Required fields per tier: EXT `Name`/`Class`/`Description`/`Status`; B `Entity`/`Direction`/`Carries`/`Status`; REL `From`/`To`/`Kind`/`Flow`/`Status`. `Status` (`Drafted`\|`Approved`) is the one maturity field, shared with the IF tier, and **rung 1 of the stage ladder reads it** — `spine_rules.boundary_incomplete` caps the repo at `DevStg-Boundary` while any crossing is `Drafted`. Realization coverage (a crossing with no realizing IF row) is REPORTED and never gated: decision 6, deferred by ruling. An SR names its crossing(s) in `Boundary-Refs` — resolution hard, coverage advisory (SN-037). |
| performance budgets | `PB-###` | `Refs` | Must resolve to a real SR id, LLR id, **or LLR `Module` path**. Empty `Refs` → finding. |
| `docs/requirements/components.toml` | `CMP-###` | `PartOf`, `SupersededBy` | Must name real CMP ids. When non-empty, every `Component` tag on LLR/IF/PART/ASSET must resolve. `Knowledge` refs under `docs/knowledge/` are **warn-only**. |
| procurement | `PART-###` | `Component` | membership only |
| assets | `ASSET-###` | `Component` | membership only |
| `docs/requirements/hats.toml` — the declared perspectives | hat NAME (`[hat.SECURITY]`; no numeric space, so no `-000` row) | SR/LLR `Hat-Refs` | Resolution is HARD: a `Hat-Refs` naming a hat the roster does not declare joins the `--strict` failure set (class `hat`). Coverage is warn-only FOREVER — one advisory counting rows attributable to no perspective, one naming hats no row is attributable to, and BOTH are suppressed entirely until at least one row fills the cell, so adopting the kit is quiet. Coverage counts **effective** sets (`trace.effective_hats`: a row's own refs unioned with its `SR-Refs` parents'), never cells — an LLR's cell holds only what its own decomposition raised, and copying a parent's hats down is the staleness this derivation exists to forbid. Vacuous with no roster (absence is opt-out for the whole layer); `trace.py` reads NAMES only and `scripts/hats.py` remains the sole validator of roster content. |
| repos | `REPO-###` (legacy `MOD-###`) | `DelegatedSRs` | Must name real coordinator SRs; empty is allowed. Cross-repo reconciliation is deferred. |

---

## 12. Drift and gotchas

Findings from compiling this, ordered by how likely each is to be behind a
recurring issue. These are observations, not filed work — none has a WI.

### 12.1 `LLR.TestRefs` is fully inert

It ships in the template, it is classified in the traced/approved split, it is
named in the required-fields exclusion comment — and **no code reads its value**.
The LLR↔TC link is carried entirely by the TC's `Verifies`. Anyone filling this
column is doing unverified bookkeeping; anyone trusting it is reading a cell
nothing maintains. The template already hints at this by shipping the literal
`(see TC)`.

### 12.2 `TC.Tier` and the pytest marker are unreconciled

`TC.Tier` is genuinely load-bearing in one place: `gen_release_checklist.py`
selects checklist items on `Tier == "Release"` **or** `Automated` not-yes, so the
cell decides what reaches a human at DevStg-Release (§9.5). It is also required
non-empty, enum-checked against `{Smoke, Full, Release}`, and emitted into the
OKF bundle.

What it does **not** do is select tests. `check.py`'s docstring says "the `Tier`
field in test-cases.toml is the registry source of truth" for tiering, but what
actually runs a test is the **pytest marker** on the test function, and nothing
compares the two. They are independent declarations of the same fact.

The asymmetry matters in one direction. A TC row reading `Release` whose test
lacks the marker merely runs earlier than declared — harmless. But a test marked
`release` whose TC row reads `Full` **silently drops out of the pre-merge
suite** while the registry still reads as pre-merge-covered. Same for a TC
declared `Smoke` whose test carries no `smoke` marker: absent from the cheap
gate, covered on paper.

### 12.3 The entire product bar is DevStg-Impl-only

`format`, `lint` and `tests+coverage` are tagged `{"DevStg-Impl"}`. Combined with §8.4,
this is the sharp edge: **one Drafted row drops the gate below DevStg-Impl and
the test suite stops running in the gated plan.** `window_open` warns about
exactly this, but the warning is the only thing between a window and a silently
untested stretch.

### 12.4 `LLR.CodeSymbol` was required but never resolved — CLOSED, with a residue

The finding as compiled: `--strict-schema` demanded the cell be non-empty and
nothing checked it named a symbol that existed, while its neighbour `Module`
genuinely *was* a join target (PB back-links, IF endpoints) — so the two looked
equally load-bearing and were not.

**Closed by WI-429's anchor rule and OI-20's ruling — see §4.2**, which also
gave the cell the grammar it never had. Two residues remain, both deliberate:
the rule is **coarse** (one binding token founds the row, and the per-token
misses are counted *untraced* rather than gated), and four live rows are
**unfounded with a stated reason** rather than guessed at.

### 12.5 SN has no schema tier at all

Every CSV tier gets required-field and enum checks; SN gets duplicate-id and
draft/approved-collision only. An SN row with `Priority`, `Why it matters` and
`Acceptance intent` all blank passes DevStg-Impl.

### 12.6 Required-but-unvalidated cells

`SR.Priority`, `TC.Level` and `TC.Method` are all required non-empty under
`--strict-schema` with **open** vocabularies. `M`/`S`/`C` is a convention
enforced by nobody. Only `SR.Verification` and `TC.Tier` are closed sets.

### 12.7 The phase rule arms globally from one row

Phase a single SR anywhere and *every* approved SR, LLR and TC across the repo
instantly owes a bare-integer `Phase` or `--strict-schema` reds. Intended, but a
cliff rather than a ramp — worth knowing before someone phases one row to try it.

### 12.8 `refs()` splits on whitespace

A cell reading `SN-001 and SN-002` parses to three tokens, and `and` becomes an
"unknown reference" orphan. The finding is correct but names the token, not the
cause.

### 12.9 `SupersededBy` (SR tier) — RETIRED

The SR-tier supersession column and its ~80-line validator retired with the
tombstone-class deletion (D-4 ruling 2026-08-14b; the log's forwarding entry
is the map). The CMP registry's own `PartOf`/`SupersededBy` rule is separate
and still live.

### 12.10 `LLR.SR-Refs` is approved only by the residual

The code says so explicitly: §A5.1 never named it, and it is "the same shape of
pointer as the ruled-traced `SN-Refs` / `Verifies`." Flagged in-code as WI-388's
question rather than a defect — but it means re-pointing an LLR at a different
parent SR opens a re-attest window while re-pointing an SR at a different SN does
not.

---

## 13. Command reference

```bash
# integrity floor only (what the pre-commit hook runs)
python project-trajectory/scripts/trace.py --strict-integrity

# the DevStg-Tests bar
python project-trajectory/scripts/trace.py --strict --no-placeholders --html

# the DevStg-Impl bar
python project-trajectory/scripts/trace.py --strict --no-placeholders --html \
    --require-verified --strict-schema [--phase 2]

# what stage do the registries derive to, and on what basis
python project-trajectory/scripts/derive_stage.py --print
python project-trajectory/scripts/derive_stage.py --check     # freshness guard
python project-trajectory/scripts/derive_stage.py --next-phase  # the number a newly
                                                # confirmed phase takes (§3.3)

# the whole harness at a chosen gate/tier
python project-trajectory/scripts/check.py --gate DevStg-Impl --tier full
python project-trajectory/scripts/check.py --list             # show the plan only

# per-module coverage floors (needs a coverage.json from a covered tier)
python project-trajectory/scripts/check_coverage.py --tier full --skip-tiers smoke

# the approval hierarchy for a batch, and the re-attest brief
python project-trajectory/scripts/trace.py --approve SR-052,SR-053
python project-trajectory/scripts/trace.py --approve modified --out docs/ratify/CURRENT.md
python project-trajectory/scripts/trace.py --approve modified --check   # freshness gate (approval-fresh)

# mint the sitting's dated, IMMUTABLE record from CURRENT.md (WI-503) — the
# only sanctioned writer of a docs/ratify/<date>-*.md; check.py's
# approval-immutable step refuses any other commit that touches one
python project-trajectory/scripts/trace.py --mint-approval-brief wi052-wi053

# expand an SR's Permutations cell into concrete cases
python project-trajectory/scripts/gen_cases.py --spec "size=range[0..2GiB]; enc=set{utf8,utf16}"
```
