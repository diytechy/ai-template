# Registry status unification — one vocabulary for "how approved is this row"

**Execution plan. Nothing here is applied yet; everything here is RULED.**
Written `2026-08-16` as a scope document; **re-derived and promoted to an
execution plan `2026-08-17t`** on the owner's ruling of sitting-3 §0.4 item 6.
Its sibling `2026-08-15-d9-migration-plan.md` is the shape it copies: a
vocabulary migration run in ordered steps, each independently revertible.

> **The owner's ruling, verbatim (2026-08-17), which this document now serves:**
> *"update docs/plans/2026-08-16-registry-status-unification.md to ensure all
> attested / approved registries use the same enum (draft / approved / founded
> (when applicable)). There may be some out of date information in that md file
> as well that could use some cleanup."*
>
> That rules item 6's sub-call **(b)** — the off-spine half is **IN scope**, not
> a separable later step. Sub-call **(a)** (timing) is effectively ruled by the
> same directive: execution is dispatched ahead of the sitting, so this runs
> **before signing**. §6 states why that is the cheap order.

> **On the filename.** The owner asked for `spine-status-unification` *if other
> registries share the misalignment*. They do — and three of them
> (`interfaces`, `components`, `external`) are **off-spine** by this repo's own
> vocabulary, so `spine-` would name the document wrongly in a document about
> naming things correctly. Filed as `registry-` instead; rename if you disagree.

> **This is not new doctrine — it is the execution of standing decision 12.**
> `repo-lock.md:254` records the 2026-08-13 ruling that **D-9 and decision 12
> are one cross-registry vocabulary program with per-registry subsets**, and
> that *"the mapping here must be re-derived, not trusted"* — which is what §0
> and §4 below do. `trace.py:445-448` names D12 in its own words: *"one shared
> status vocabulary, per-registry subsets… the subset here is the two-value
> one; it is PROVISIONAL pending D-9's ladder."* The owner's
> **"(when applicable)"** and D12's **"per-registry subsets"** are the same
> rule; §3.2 states which subset each registry gets and on what evidence.

---

## 0. Scope — every registry, re-measured `2026-08-17t`

The SN finding (§1) is one instance of a wider split. Across all nine
registries there are **four field names, two case conventions, and one
vocabulary that re-uses retired spine words for unrelated meanings**:

| registry | rows | field today | vocabulary today |
|---|---|---|---|
| `system-requirements` · `low-level-requirements` · `test-cases` | 384 | `status` | `Drafted` \| `Approved` \| `Modified` — **the canonical one**: closed, Title-case, integrity-checked |
| `stakeholder-needs` | 27 | `kind` **+** `attestation` **+** `amended` | `core` (27/27) + `pending` (18) + a date (18) — §1 |
| `interfaces` | 123 | `approval` | `drafted` (lowercase, 123/123) |
| `external` (entity 4 · boundary 4 · relationship 3) | 11 | `approval` | `drafted` (lowercase, 11/11) |
| `components` | 4 | `state` | `planned` (4/4) \| `built` \| `verified` \| `has-gap` \| `deprecated` |
| `open-items` | 22 | `status` | `pending` \| `ruled` — a DIFFERENT axis; see §3.4 |
| `hats` · `agents` | 25 | — | none (config registries; out of scope) |

*Re-measured against the live registries at this commit. **Two figures in the
2026-08-16 revision of this table were stale:** `external` read **14** rows —
it is **11** since `2026-08-16q` deleted `EXT-004` + `B-06`/`B-07`; and the SN
`attestation`/`amended` sets read **17** — they are **18** since `2026-08-17h`
amended `SN-008`. The off-spine row total quoted in the old §6a (**141**) is
therefore **138** (123 + 11 + 4).*

**Three findings beyond the SN one, all re-confirmed:**

**(a) `components.state` re-uses two RETIRED spine words for different
meanings.** Its declared vocabulary — stated in the shipped
`components.template.toml` and pinned by `trace.ENUM_FIELDS["CMP"]["State"]`
(`trace.py:463`) — is `planned|built|verified|has-gap|deprecated`. `Planned`
and `Verified` were retired from the spine at D-9 (2026-08-15) and folded into
`Approved`, on the argument that near-synonyms get applied inconsistently. They
survive here in lowercase, in a different field, in a different registry,
meaning something else — and `check_vocab.py` cannot see it because that
checker guards only the retired `G*` gate tags. **This is the
retired-vocabulary regeneration `SR-149` exists to prevent, in the one place
the checker does not look.** §3.3 dissolves it rather than renaming around it.

**(b) `approval` is a third spelling of the same axis** — different field name
*and* different case from the spine's `status`, so every cross-registry
question ("what is un-approved right now?") needs a per-registry special case.

**(c) The off-spine approval path has never been exercised.** All 123 interface
rows and all 11 external rows read `drafted`; all 4 component rows read
`planned`. Nothing has ever been approved in any of the three. A state machine
with one reachable state is a field, not a mechanism — which is precisely why
this migration is cheap to run now (§6): **no off-spine cell changes meaning,
only its spelling.**

---

## 1. The SN finding (the instance that started this)

The SN tier encodes status across **three fields**, one of which carries
history. The other three spine tiers encode the same thing in **one**.

| axis | SR / LLR / TC | SN today |
|---|---|---|
| drafted | `status = "Drafted"` | `kind = "draft"` (0 rows carry it) |
| approved | `status = "Approved"` | `kind = "core"` — the template defines it as *"a ratified need (the steady state)"* (27/27 rows) |
| amended | `status = "Modified"` | `attestation = "pending"` (**18** rows) |
| **when it changed** | git · `docs/archive/` | **`amended = "<date>"`** (**18** rows) |
| row TYPE | n/a | `kind = "edge"` (0 rows; retired at `2026-08-17j`) |

Three defects, in the order they matter:

**(a) `amended` is history in a registry whose job is living truth.** A cell
recording *when a row changed* is provenance, and the repo already forbids that
class — `trace_text.provenance_findings` flags a spine row whose TEXT carries
its own history. It cannot see a FIELD, which is the only reason this passed.
Git and `docs/archive/` already hold the fact, hold it for every row rather
than eighteen, and cannot drift from it.

**(b) `attestation` invents a second vocabulary for a word the spine had.**
`Modified` is the agreed name for amended-and-unsigned. A parallel
`pending` marker means a reader asking "is this row signed?" checks a different
field per tier.

**(c) `kind` conflates MATURITY with ROW TYPE.** `core`\|`draft` is a status
axis; `edge` is a row-shape axis. One field, two unrelated questions.

**Nothing reads `attestation` or `amended`.** Re-verified by grep across every
kit script: the only `attestation` hits are `docs/process.toml [attestation]`,
an unrelated config section. Both fields are inert documentation today, which
is why step 3 can delete them outright.

## 2. Why `kind` can die entirely (not merely be renamed)

The owner's direction is that `kind` goes, not that it is split. That is
mechanically available because **the edge/core half is already derived from the
row's field shape** — the legacy markdown reader does exactly this derivation
today, in `spine_carrier.needs_from_markdown` (`spine_carrier.py:745-793`):

```python
row_kind = kind or ("edge" if len(cells) - 1 == len(SN_EDGE) else "core")   # :782
...
if kind is None and any(n in SN_EDGE for n in names if n):                  # :785
    row_kind = "edge"
```

with `SN_CORE = (need, why, priority, acceptance)` (`:701`) and
`SN_EDGE = (lifecycle, scenario, expected)` (`:702`). The two shapes are
disjoint, so a row's type is a function of the keys it carries. Declaring it is
the **declared-where-derivable** pattern the repo is already retiring elsewhere
(re-tier v2 R4, `this_project`).

That leaves `kind = "draft"` as the only non-derivable thing the field carries —
and that is precisely what `status = "Drafted"` says.

So: **maturity → `status`; row type → derived from field shape.** `kind` has
nothing left.

> **The `edge` sub-question is CLOSED — it was open when this section was
> written on 2026-08-16, and the owner ruled it at `2026-08-17j`** (WI-471
> dispatch, verbatim: *"edge is dropped"*). The `edge` row kind, its
> `lifecycle`/`scenario`/`expected` fields and the standing edge-case checklist
> leave the kit surfaces; edge-case coverage is the hats mechanism's job. The
> boundary recorded with that ruling: *"`kind = core|draft` (maturity) STAYS
> until sitting-3 item 6's unification executes — only the `edge` row-type
> value dies."* **This plan is that execution.** The derivation above is
> therefore kept only as the LEGACY-markdown reader's business
> (`migrate_carrier`, `needs_from_markdown`); no live TOML path emits `edge`.

## 3. Target shape

### 3.1 The SN row

```toml
[need.SN-001]
status = "Approved"          # Drafted | Approved | Modified — the spine vocabulary
tags = ["templates", "scripts"]
need = """..."""
why = "..."
priority = "M"
acceptance = """..."""
```

Deleted: `kind`, `attestation`, `amended`. Added: `status`.

**The mapping, on the re-measured sets** (§0; the two sets agree exactly — 0
rows pending-without-amended, 0 amended-without-pending):

- the **18** rows carrying `attestation = "pending"` → `status = "Modified"` —
  `SN-001` `003` `005` `006` `008` `009` `011` `012` `023` `025` `026` `027`
  `028` `029` `034` `035` `038` `039`;
- the other **9** → `status = "Approved"` — `SN-002` `004` `007` `010` `024`
  `033` `036` `037` `040`.

> **`Modified`, not `Founded`, and deliberately so.** `Modified` is
> TRANSITIONAL: it is the live spine enum today and it retires at **D-9 step
> 7**, POST-sign, when snapshot comparison replaces it (owner ruling
> `2026-08-17m`: *"modified means nothing because it is caught by comparing to
> the snapshot"*). Writing these 18 rows as `Modified` now puts SN on exactly
> the vocabulary the other three tiers already speak, and they resolve the way
> every other tier's `Modified` rows do — the sitting signs them to `Approved`,
> the snapshot seeds, then the word retires. §5B holds everything that waits
> for that.

**The former "17-vs-18 discrepancy" is CLOSED, and it closed the other way.**
The 2026-08-16 revision of this section reasoned that three places in prose
said 18 while the registry carried 17, and concluded *"the prose 18 appears to
be the error."* **That conclusion is now wrong and must not be executed.**
`2026-08-17h` amended `SN-008` (its `need` cell moved from the hue metonym to
*"a reader can believe a pass verdict"*), which set that row's first
`attestation = "pending"` and `amended = "2026-08-17"`. The live count is
**18**, measured this session, with `attestation` and `amended` in exact
agreement and `SN-008`/`SN-027` the only two dated `2026-08-17`. Step 1 still
runs — but as a confirmation of 18, not an adjudication of 17-vs-18.

### 3.2 The one enum, and which subset each registry gets

**The field name unifies onto `status`. The vocabulary unifies onto the spine's
Title-case closed set.** The per-registry subset is the owner's *"(when
applicable)"* and D12's *"per-registry subsets"*:

| registry | field after | subset after | is `Founded` applicable? |
|---|---|---|---|
| `stakeholder-needs` (SN) | `status` | `Drafted` · `Approved` (+ `Modified`, transitional) | **later** — arms with the spine at D-9 step 8 |
| `system-requirements` (SR) | `status` *(unchanged)* | same | **later** — same |
| `low-level-requirements` (LLR) | `status` *(unchanged)* | same | **later** — same |
| `test-cases` (TC) | `status` *(unchanged)* | same | **later** — same |
| `interfaces` (IF) | `approval` → `status` | `Drafted` · `Approved` | **NO — never** |
| `external` (EXT · B · REL) | `approval` → `status` | `Drafted` · `Approved` | **NO — never** |
| `components` (CMP) | `state` → `status` **+ new `standing`** | `Drafted` · `Approved` · `Founded` | **YES — today** |

**"When applicable" is not a judgement call — it is a test the code already
answers: `Founded` is available exactly where a DISCHARGE PREDICATE exists.**
`Founded` means "settled AND demonstrated" (`derive_gate.py:606-608`), so a row
can only reach it if something computes whether its children answer it.

- **Off-spine, IF/EXT/B/REL: no predicate, and the reason is already written
  down.** `derive_gate.py:626-628`, on `BIF_MATURITY`: *"NOT Founded on
  `approved`… an approval says the crossing is agreed, it says nothing about
  the crossing having been demonstrated."* These four tiers get the two-value
  subset permanently. **A row here never reaches `Founded`** — say so in the
  templates rather than leaving a reader to wonder.
- **Off-spine, CMP: a predicate exists and is live.**
  `CMP_MATURITY` (`derive_gate.py:639-656`) already maps `verified → FOUNDED`,
  and `arch_incomplete` (`:750-767`) gates rung 3 on it. **CMP is the one
  registry where `Founded` is reachable TODAY** — which is why the word enters
  its enum in this pass and not at D-9 step 7. No live row takes the value (all
  4 are `planned` → `Drafted`), so the word becomes legal without any cell
  moving to it.
- **Spine: four predicates exist but are not yet wired to the word.** D-9 C4
  records all four discharge tests as built (`check_doc_refs.symbol_findings`;
  SN = the coverage rung; SR = `derive_gate._decomposed_sr_ids:569`; TC = the
  `Evidence` existence half) — *"`Founded` is computable for all four tiers
  today"* — but `SPINE_MATURITY` deliberately omits it
  (`derive_gate.py:606-608`: *"unreachable from the spine today by design"*).
  **Arming it is D-9 step 8, POST-sign. This plan does not touch it** (§5B).

### 3.3 `components.state` — adjudicated: it is CONFLATED, and the split dissolves the collision

The question the brief poses is whether `state` is an attestation field or a
domain lifecycle field. **Measured, it is both — and that conflation is the
same defect as SN's `kind`.**

Evidence that it IS the attestation/maturity field for rung 3:

1. `CMP_MATURITY` maps it onto the ladder semantics and `arch_incomplete`
   (`derive_gate.py:750-767`) gates the architecture rung on the result.
2. `agent_common.APPROVAL_RUNGS` (`agent_common.py:582-586`) lists
   `"components"` beside `"external"` and `"interfaces"` — the repo already
   classifies CMP as an approval-carrying registry, at `DevStg-Arch`.
3. `baseline_snapshot._STATE_CELL_CLAIMED` (`baseline_snapshot.py:184-187`,
   read at `:279`) derives "does this row claim approval?" from `CMP_MATURITY`
   — the snapshot layer treats a `State` cell as an approval claim.

Evidence that it ALSO carries a second axis: `has-gap` and `deprecated` are not
maturity values. They are lifecycle facts *folded onto* maturity
(`has-gap → DRAFTED`, `deprecated → APPROVED`), exactly as `kind = "edge"` was
a row-type fact sharing a field with maturity.

**The call: SPLIT it, the way SN's `kind` is being split.**

```toml
[component.CMP-001]
status = "Drafted"        # Drafted | Approved | Founded — the one enum
standing = "active"       # active | has-gap | deprecated  (omit = active)
```

| `state` today | → `status` | → `standing` |
|---|---|---|
| `planned` | `Drafted` | *(omit)* |
| `built` | `Approved` | *(omit)* |
| `verified` | `Founded` | *(omit)* |
| `has-gap` | `Drafted` | `has-gap` |
| `deprecated` | `Approved` | `deprecated` |

**Why this beats the 2026-08-16 §6a proposal (rename `planned`→`designed`,
`verified`→`implemented`).** The rename leaves three spellings of one axis
standing and merely swaps two colliding words for two others that must then be
defended forever. The split **dissolves finding (a) by construction**:
`planned` and `verified` cease to exist as CMP values, so there is nothing left
to collide with the retired spine words, and no new vocabulary is invented —
every word in the result is either the one enum or a word CMP already used.
It also makes the round-trip `PROCESS.md:773` documents (`verified → has-gap →
verified`) *more* legible, as `Founded → Drafted+has-gap → Founded`: a
demonstrated partition that regressed and was re-demonstrated.

> **On the name `standing`, and why NOT `lifecycle`.** The obvious word for the
> second axis is `lifecycle` — and it is **rejected**, by this plan's own
> finding (a) applied to itself. `lifecycle` is already a live key: it is the
> first field of `SN_EDGE` (`spine_carrier.py:702`, `migrate_carrier.py:545`)
> **and it has an entry in the SHARED carrier header map**
> (`spine_carrier.py:136` `"lifecycle": "Lifecycle"`, `:723`;
> `migrate_carrier.py:144`) — a map that is global across registries, so a CMP
> `lifecycle` key would route through the same entry as a dying SN edge field.
> That is a MECHANICAL collision, not merely a semantic one, and it is exactly
> the retired-vocabulary regeneration §0(a) is about. `condition` and
> `disposition` are also taken (`hats.py:256+`; the WI registry). **`standing`
> and `health` are the only unused candidates measured; `standing` is chosen**
> because it covers both `has-gap` (the partition does not hold) and
> `deprecated` (it has been retired), where `health` covers only the first.

**Live cost: 4 rows, all `planned` → all `status = "Drafted"`, zero `standing`
cells written.** `CMP_MATURITY` collapses to the identity mapping over the one
enum (`drafted→DRAFTED, approved→APPROVED, founded→FOUNDED`), which is
`SPINE_MATURITY` minus the transitional row — see step 7c for whether to
collapse the two tables or leave them distinct.

### 3.4 `open-items` — deliberately NOT unified, and the collision it leaves

`open-items` already spells its field `status`, over `pending`\|`ruled`. That
describes a **decision**, not an artifact's maturity — a different axis,
legitimately different words. It does not join the enum.

**But the field-name unification creates a name collision with it**, and this
repo's D-3 doctrine is one name for one meaning. Stating it rather than
discovering it later: after this change, `status` means "attestation maturity"
in seven registries and "has this been ruled on" in one.

**Recommendation: accept it in this pass, and file the rename as its own
call.** `open-items` is a generated surface (`gen_open_items.py`) whose rows
are tooling output rather than attested artifacts, so the collision misleads
much less than `planned`/`verified` did — nobody reads an OI row asking whether
it is signed. If the owner wants it closed, the move is
`status` → `disposition` over the same two words; it is ~22 rows plus
`gen_open_items.py` and the OI schema entry, and it is **independent of every
step below**. Do not fold it in without a ruling.

## 4. Blast radius — re-measured `2026-08-17t`, not estimated

> **Every line number below was re-verified this session.** Four rows of the
> 2026-08-16 table had drifted or were wrong; each correction is marked.

### 4.1 Readers of SN `kind`

| file | site | change |
|---|---|---|
| `spine_carrier.py` | **`:938`** `draft_need_ids` — `n.get("kind") == "draft"` *(holds exactly; it is the file's LAST line, so any insertion above shifts it)* | → `n.get("status") == "Drafted"` |
| `spine_carrier.py` | **`:871`** `draft_ids_from_text` — the second, distinct drafted selector *(row missing from the old table)* | dispatches to the above; docstring only |
| `spine_carrier.py` | **`:782-787`** `needs_from_markdown` edge derivation *(holds byte-for-byte)* | keep the derivation, stop emitting a `kind` key |
| `spine_carrier.py` | **`:795-824`** `needs_from_toml` (`:804` emits `{"id": rid, "kind": "core"}`) + `needs_from_text` — **CORRECTED**: the old table's `:804` named the markdown call site, which is now at `:824` and `:839` (two call sites, not one) | stop emitting `kind`; read `status` |
| `spine_carrier.py` | **`:849-868`** `folded` — edge branch at `:860`, core projection **`:861`** *(was `:860`, drifted +1)* | drop the edge arm per `2026-08-17j` |
| `check_docs.py` | **`:558`** `n.get("kind") != "draft"` *(holds exactly)* | same selector swap |
| `derive_gate.py` | **`:281-301`** `sn_draft_ids` docstring (`:285` carries the `kind = "draft"` sentence — *holds*) | docstring only; delegates to the carrier |
| `derive_gate.py` | **`:436-449`** `sn_bar` — the actual drafted-SN rung, called from `:945` — **NEW ROW**: the old table folded this into `:285`, conflating a docstring with the rung logic | rung logic UNCHANGED; it consumes `draft_ids` |
| `trace.py` | **`:1192-1212`** `sn_draft_ids` docstring (the sentence at `:1196`) — **CORRECTED**: the old table said `:1254`, which is now `return out` in the duplicate-id finder, an unrelated legacy-markdown scan | docstring only. **It is the F5-duplicated twin of `derive_gate.py:285` and `test_rule_sync` PINS THEM EQUAL — they must change in the same edit** |
| `migrate_carrier.py` | `SN_CORE` `:544`, `SN_EDGE` `:545`, `read_sn` `:548` (heading-kind `:569`, shape fallback `:586`, emit `:588`), `sn_to_toml` writes `kind` at `:596` | the legacy converter learns the new shape |

**Not affected:** the derived gate's arithmetic (the SN rungs read
*drafted-ness*, which survives under a new name), `hats.py` (reads `tags`, not
`kind`), and the `attestation`/`amended` deletion (no reader at all).

### 4.2 Readers of the off-spine `approval` / `state`

| file:line | reads | what the rename/re-case costs |
|---|---|---|
| `trace.py:354, :359, :360, :361` | `"Approval"` in the IF/EXT/B/REL REQUIRED-column lists | rename the key |
| `trace.py:356` | `"State"` in the CMP required list | rename the key; add `standing` as OPTIONAL |
| `trace.py:461, :470, :474, :476` | `ENUM_FIELDS` `{"drafted","approved"}` for IF/EXT/B/REL | → `"Status": {"Drafted","Approved"}` |
| `trace.py:463` | `ENUM_FIELDS["CMP"]["State"]` (five words) | → `"Status": {"Drafted","Approved","Founded"}` + `"Lifecycle": {"active","has-gap","deprecated"}` |
| `derive_gate.py:747` | `r.get("Approval")` via `_maturity(…, BIF_MATURITY)` — `boundary_incomplete`, rung 1 | → `r.get("Status")` |
| `derive_gate.py:767` | `r.get("State")` via `_maturity(…, CMP_MATURITY)` — `arch_incomplete`, rung 3 | → `r.get("Status")` |
| `derive_gate.py:633-636` `BIF_MATURITY` | lowercase-keyed table | keys UNCHANGED — `_maturity` lowercases before lookup (`:659`), so a Title-case cell still resolves |
| `derive_gate.py:639-656` `CMP_MATURITY` | ditto | keys become the one enum; `has-gap`/`deprecated` rows LEAVE (they move to `standing`) |
| `baseline_snapshot.py:278, :279` | `row.get("Approval")` / `row.get("State")` against `_APPROVAL_CELL_CLAIMED` / `_STATE_CELL_CLAIMED` (derived `:184-187`) | → `r.get("Status")`; the derived sets follow the tables automatically |
| `check_trajectory.py:954` | `load_ifs` normalizes `r.get("Approval")` | rename; **no comparison** — nothing keys on the value (reasoning at `:1718-1732`) |
| `gen_okf.py:484` | emits `Approval` as a one-pager tag | rename; presentation only |
| `gen_release_checklist.py:268` | renders `Approval` into the contract line | rename; presentation only |
| `traj_views.py:1146` | `"State"` in the CMP panel column tuple | rename; presentation only |
| `spine_carrier.py:210, :244` | header maps `"approval"→"Approval"`, `"state"→"State"` | rename both |
| `spine_carrier.py:363, :372, :384, :385, :386` | `OFFSPINE_KEYS` schema keys for IF/CMP/EXT/B/REL | rename; add `standing` to `CMP-ID` |
| `migrate_carrier.py:198, :207` | header maps `"Approval"→"approval"`, `"State"→"state"` | rename both |
| `agent_common.py:625-658` `human_approves` | **keyed on the registry STEM via `APPROVAL_RUNGS`, NOT on the field name** | **LOGIC UNCHANGED.** Docstring only (it says "an `approval` cell" five times). This is materially smaller than the 2026-08-16 table implied |

**Git hooks read neither field.** Verified across `.githooks/` and the shipped
`project-trajectory/hooks/`: the only matches are the English word "state(d)"
in `pre-commit` comments. The 2026-08-16 note that hooks were in the blast
radius is **withdrawn**.

> ### ⚠ Two traps an execution agent MUST NOT walk into
>
> **(i) A rename silently disarms a guard.**
> `tests/test_ratification_level.py:725-753` greps every
> `project-trajectory/scripts/*.py` with the regex
> `approval["'\]]*\s*[:=]\s*["']approved["']` to prove **no kit script writes an
> approval cell**. Rename the field without re-keying that regex and the guard
> passes vacuously forever — the exact failure class this whole change exists
> to prevent. **Re-key it in the same commit as step 7.**
>
> **(ii) Two tests pin the maturity tables EQUAL to trace's vocabulary, by raw
> set comparison.** `tests/test_ratification_level.py:495`
> (`set(dg.BIF_MATURITY) == trace.ENUM_FIELDS["B"]["Approval"]`) and `:496`
> (the CMP twin). The tables stay lowercase-keyed while `ENUM_FIELDS` goes
> Title-case, so **these comparisons break by construction** and must become
> case-normalized (`{v.lower() for v in …}`). A green run here is only
> meaningful once they are re-keyed — do not "fix" them by lower-casing the
> registries.

### 4.3 Registries, templates and docs

`stakeholder-needs.template.toml` (the whole "MATURITY IS A FIELD, NOT A
SECTION" header block is rewritten), `interfaces.template.toml:67-68, :85` and
`external.template.toml:24-27, :38, :46, :55` (both declare the
`drafted | approved` vocabulary in prose — rewrite to the one enum **and state
that `Founded` is not applicable to these tiers**, §3.2),
`components.template.toml` (the `state` line + the `State = planned|built|…`
sentence inside `notes`), `PROCESS_OPTIONS.md:2254` (the CMP vocabulary
sentence), `PROCESS.md:763, :773` (the `has-gap → verified` flow diagram and
its prose), and `RESYNC_PACK.md` — **downstream-visible schema changes**, so
adopters need entries (§5A step 9; the precedent entry is *"The `Status` ladder
RENAME"* `[since 3771c003]`).

### 4.4 Tests

**The 2026-08-16 figure of "23 SN-specific `kind` assertions" does not
reproduce under any defensible counting rule and is withdrawn.** The **file set
was right** (no sixth file carries an SN `kind` literal); the count was not.
Re-measured:

| file | lines mentioning SN `kind` | real `assert`s on it |
|---|---|---|
| `tests/test_check_docs.py` | 3 (`:21, :459, :470`) | 0 |
| `tests/test_check_need_form.py` | 5 (`:27, :93, :113, :244, :257`) | 0 |
| `tests/test_hats.py` | 11 (`:157-168, :267-273, :583, :591, :602`) | 4 |
| `tests/test_migrate_carrier.py` | 5 (`:280, :281, :284, :292, :301`) | 2 |
| `tests/test_rule_sync.py` | 4 (`:663, :678, :700, :701`) | 0 |
| **total** | **28** | **6** |

The 22 non-assertion sites are **TOML fixture strings** — they feed real
parsers, so they break just as hard as an assertion would and are fully in the
blast radius. State both numbers; neither alone is honest.

> **A coverage hole to know about before moving any of this.**
> `tests/test_spine_carrier.py` contains **zero** occurrences of the string
> `kind` — the module that owns `draft_need_ids`, `folded`, `SN_CORE`/`SN_EDGE`
> and the whole field has no direct test of it. Step 4's selector swap is
> therefore proved only indirectly, through `test_check_docs` /
> `test_rule_sync`. **Step 4 owes a direct `test_spine_carrier` case** for
> `draft_need_ids` over a `status`-carrying need set; this is the one place the
> migration would otherwise move untested code.

Off-spine test sites are listed inline in §4.2; the concentrated ones are
`tests/test_baseline_snapshot.py:303, :322, :337, :344-347`,
`tests/test_ratification_level.py:393, :394, :484, :495-502, :686-753`,
`tests/test_migrate_carrier.py:164, :175`, `tests/test_trajectory_arch.py:166`.

## 5. Sequencing

**The two lists below are not one list.** §5A runs NOW, before the sitting
signs anything, at zero re-attestation cost. §5B runs at **D-9 steps 7-8**,
after the sitting has signed AND seeded `docs/archive/last_approved/`.
**Nothing in §5B is runnable today and nothing in it is done.**

### 5A — RUNS NOW (pre-sign). Nine steps, each independently revertible.

Each step names its files, its verification and its rollback boundary. The bar
for every step is the **commit bar**: `python -m pytest -q -n auto -m smoke`
plus `python project-trajectory/scripts/check_docs.py --root . --stale`.

| # | step | files | verify | rollback boundary |
|---|---|---|---|---|
| **1** | **Confirm the amendment set is 18** against git — §3.1 lists the ids. Blocking; everything waits on it. *(No longer an adjudication of 17-vs-18: §3.1 closed that. This is a confirmation that no row was amended after this plan was measured.)* | — (read-only) | `git log` over `stakeholder-needs.toml` since `2026-08-16`; the 18 ids must match §3.1 exactly | nothing written |
| **2** | **Add `status` beside the existing fields**, dual-read in both selectors (`status` wins, `kind` is the fallback) | `spine_carrier.py:871, :938`; `check_docs.py:558` | full suite green with BOTH shapes parsing; `trace.py --strict` counts unchanged | one commit; `kind` still authoritative |
| **3** | **Migrate the 27 rows** — write `status` per §3.1, delete `attestation` and `amended` | `docs/requirements/stakeholder-needs.toml` | 18 `Modified` + 9 `Approved`; zero `attestation`/`amended` keys; `check_docs --stale` clean | registry-only; step 2's dual-read still accepts the old shape |
| **4** | **Drop the `kind` fallback** from the selectors; **add the missing direct test** (§4.4) | `spine_carrier.py:871, :938`; **new** `tests/test_spine_carrier.py` case | the new test fails against the pre-step-2 selector (mutation-proved) | selectors only |
| **5** | **Delete `kind`** from the 27 rows and the template; rewrite the template header block; drop the `edge` arm per `2026-08-17j` | `stakeholder-needs.toml`; `stakeholder-needs.template.toml`; `spine_carrier.py:782-787, :849-868`; `migrate_carrier.py:544-596` | `grep -c '^kind' docs/requirements/stakeholder-needs.toml` → 0; `test_dogfood_sync` green | the legacy markdown reader keeps its own derivation |
| **6** | **Off-spine ENUM → the one vocabulary** (Title-case). 123 IF + 11 EXT/B/REL cells `drafted` → `Drafted`; 4 CMP `planned` → `Drafted`. **Re-key the two set-equality pins (§4.2 trap ii) in this commit.** | the three registries; `trace.py:461-476`; `tests/test_ratification_level.py:495, :496` | `derive_gate` basis line **byte-identical** before/after — no cell changed meaning, only spelling | registries + enum tables; field names untouched |
| **7** | **Off-spine FIELD → `status`**, and **split `components.state`** into `status` + `standing` per §3.3. **(a)** rename `approval` → `status` across IF/EXT/B/REL; **(b)** CMP split; **(c)** decide whether `CMP_MATURITY` collapses into `SPINE_MATURITY` or stays a distinct row — *recommend STAYS distinct*: the two tables will differ again at D-9 step 7 when `Modified` leaves the spine's. **Re-key the no-writer guard regex (§4.2 trap i) in this commit.** | every §4.2 row; `tests/test_ratification_level.py:725-753` | basis line byte-identical again; the no-writer guard **proved still live** by a deliberate temporary violation | the widest step — keep it its own commit |
| **8** | **Close the SN schema census** (owner ruling `2026-08-17k`). Add `"SN-ID"` to `spine_carrier.SPINE_TIER_KEYS` (`:268-307`) with the POST-unification key set — `status · tags · need · why · priority · acceptance` — and wire the SN tier into `test_dogfood_sync`'s three-leg template ↔ live ↔ schema comparison. Also add `"SN": {"Status": STATUS_VALUES}` to `trace.ENUM_FIELDS` — the correct home, though its enforcement is advisory at today's gate (D-9 C1). | `spine_carrier.py:268`; `tests/test_dogfood_sync.py:326`; `trace.py:394` | the three-leg check green for SN | schema + test only |
| **9** | **`RESYNC_PACK.md` entries** (one for the SN shape, one for the off-spine field/enum — both downstream-visible) + remaining tests + goldens + the §4.3 prose surfaces | `RESYNC_PACK.md`; `PROCESS.md:763, :773`; `PROCESS_OPTIONS.md:2254`; the four templates | **full unfiltered suite** `pytest -q -n auto`; `check_docs --root . --stale`; landing-order test green on the new entries | docs + tests |

> **Step 8 is sequenced HERE deliberately** (owner ruling `2026-08-17k`, owner
> verbatim *"Yes add in"*): adding the census before the unification would pin
> the dying `kind`/`attestation`/`amended` set and force it to be edited twice.
>
> **Precondition step 8 must handle:** `SN-008` is the ONE live need missing a
> `tags` key (10 rows lack `tags` in total: the 9 never-amended rows plus
> `SN-008`). The three-leg check compares template ↔ live ↔ schema, so decide
> before wiring whether `tags` is REQUIRED or OPTIONAL in the SN key set. It is
> the guard gap that let the template ship without `tags` in the first place
> (`2026-08-17j`), so **optional-with-a-census-entry** is the honest answer
> unless the owner wants all 10 rows tagged.

### 5B — RUNS AT D-9 STEPS 7-8 (POST-sign AND POST-seed). NOT NOW.

**Precondition for every line below: the sitting has signed, and
`docs/archive/last_approved/` has been seeded in the same reviewed commit.**
Until then the snapshot does not exist and none of this is decidable. This
section is a pointer, not a task list — `2026-08-15-d9-migration-plan.md` rows
7 and 8 are the spec of record.

- **`Modified` retires** — delete `is_modified`; the spine enum narrows to
  `{Drafted, Approved, Founded}`; `test_rule_sync` gains the **negative**
  assertion that no predicate honours a retired word; `intake.py:1591`'s
  `if status != "Modified": continue` resolves into a refusal;
  `SPINE_MATURITY`'s transitional `"modified": APPROVED` row leaves. **The 18
  SN rows §5A step 3 writes as `Modified` are cleared by the SIGNING, not by
  this step** — D-9 step 7's own precondition is *"step 6 clears the last
  `Modified`"*.
- **The UNANCHORED rule arms** as an ERROR on the `--strict-integrity` floor.
- **`Founded` is computed** for the four spine tiers (D-9 step 8), and `sr_bar`
  ceilings at `BAR_TESTS`. This is where the spine's `Founded` column in §3.2
  turns from *later* into *live*. CMP's `Founded` is already live and is
  untouched by this step.

## 6. The timing argument — and why it is now a ruling, not a recommendation

**Run §5A BEFORE signing.** No `docs/archive/last_approved/` snapshot exists,
so every SN row awaits a *first* approval and the brief renders current text
rather than a diff. Changing the field shape today costs **zero
re-attestation**. After the sitting it costs a re-attest of every touched row —
and the owner would have signed 18 rows carrying a field pair already rejected.

The off-spine half is even cheaper, and §0 finding (c) is why: **all 138
off-spine rows sit in their vocabulary's first state.** No cell changes
meaning; only its spelling. Step 6's verification — *the `derive_gate` basis
line is byte-identical before and after* — is available precisely because
nothing semantic moves.

This is the same argument that made the `2026-08-16p` acceptance-criteria
correction free, and it expires at the sitting. **The owner has effectively
ruled it** by dispatching execution ahead of the sitting; item 6 sub-call (a)
is answered *yes*.

## 7. What this plan does NOT decide

- **Whether the SN `status` should then be WIRED beyond drafted-ness.** Nothing
  reads the current marker, and a `status` field nobody checks is the same
  defect with a better name. Candidates: `trace.py` refusing to treat a
  `Modified` need as ratified, and the ratify brief grouping by it. Sizing that
  is a separate pass. *(Step 8's `ENUM_FIELDS` entry gives it a home; it does
  not give it teeth at today's gate.)*
- **Whether `open-items.status` renames to `disposition`** (§3.4). Recommended
  as a separate call; independent of every step above.
- **When the spine's `Founded` arms** — that is D-9 step 8's business (§5B),
  not this plan's.

*(Two items this section used to carry are now CLOSED and have moved into the
body: the `edge` sub-question, ruled `2026-08-17j` — §2; and "the third status
word", ruled `2026-08-17m` — the enum's end state is `{Drafted, Approved,
Founded}`, stated in §3.2.)*
