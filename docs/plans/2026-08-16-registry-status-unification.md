# Registry status unification — one vocabulary for "how approved is this row"

**Scope document, not an execution record.** Nothing here is applied. Written
`2026-08-16` on the owner's direction at the sitting-3 desk (item 6), for the
owner to approve, amend or decline before any cell moves. Its sibling
`2026-08-15-d9-migration-plan.md` is the shape to copy: a vocabulary migration
run in ordered steps, each independently revertible.

> **On the filename.** The owner asked for `spine-status-unification` *if other
> registries share the misalignment*. They do — and three of them
> (`interfaces`, `components`, `external`) are **off-spine** by this repo's own
> vocabulary, so `spine-` would name the document wrongly in a document about
> naming things correctly. Filed as `registry-` instead; rename if you disagree.

---

## 0. Scope — every registry, measured

The SN finding (§1) turned out to be one instance of a wider split. Across all
nine registries there are **four field names, three case conventions, and one
vocabulary that re-uses retired spine words for unrelated meanings**:

| registry | rows | field | vocabulary today |
|---|---|---|---|
| `system-requirements` · `low-level-requirements` · `test-cases` | 368 | `status` | `Drafted` \| `Approved` \| `Modified` — **the canonical one**: closed, Title-case, integrity-checked |
| `stakeholder-needs` | 27 | `kind` **+** `attestation` **+** `amended` | `core`\|`draft` + `pending` + a date (§1) |
| `interfaces` | 123 | `approval` | `drafted` (lowercase) |
| `external` (entity/boundary/relationship) | 14 | `approval` | `drafted` (lowercase) |
| `components` | 4 | `state` | `planned`\|`built`\|`verified`\|`has-gap`\|`deprecated` |
| `open-items` | 22 | `status` | `pending`\|`ruled` |
| `hats` · `agents` | 25 | — | none (config registries; out of scope) |

**Three findings beyond the SN one:**

**(a) `components.state` re-uses two RETIRED spine words for different
meanings.** Its declared vocabulary — stated in the shipped
`components.template.toml` — is `planned|built|verified|has-gap|deprecated`.
`Planned` and `Verified` were retired from the spine at D-9 (2026-08-15) and
folded into `Approved`, on the argument that near-synonyms get applied
inconsistently. They survive here in lowercase, in a different field, in a
different registry, meaning something else — and `check_vocab.py` cannot see it
because that checker guards only the retired `G*` gate tags. A reader who learns
"verified is retired" then meets `state = "verified"` has to discover that this
one is unrelated. **This is the retired-vocabulary regeneration `SR-149` exists
to prevent, in the one place the checker does not look.**

**(b) `approval` is a third spelling of the same axis** — different field name
*and* different case from the spine's `status`, so every cross-registry
question ("what is un-approved right now?") needs a per-registry special case.

**(c) The off-spine approval path has never been exercised.** All 123 interface
rows and all 14 external rows read `drafted`; nothing has ever been approved in
either. A state machine with one reachable state is a field, not a mechanism —
worth knowing before deciding whether these registries need the full vocabulary
or a simpler one.

**`open-items` is probably fine as-is** and is called out so its exclusion is
deliberate: `pending`/`ruled` describes a *decision*, not an artifact's
maturity. Different axis, legitimately different words. Confirm rather than
assume.

---

## 1. The SN finding (the instance that started this)

The SN tier encodes status across **three fields**, one of which carries
history. The other three spine tiers encode the same thing in **one**.

| axis | SR / LLR / TC | SN today |
|---|---|---|
| drafted | `status = "Drafted"` | `kind = "draft"` |
| approved | `status = "Approved"` | `kind = "core"` — the template defines it as *"a ratified need (the steady state)"* |
| amended | `status = "Modified"` | `attestation = "pending"` (17 rows, added `2026-08-16` at Sol F2) |
| **when it changed** | git · `docs/archive/` | **`amended = "<date>"`** (17 rows) |
| row TYPE | n/a | `kind = "edge"` |

Three defects, in the order they matter:

**(a) `amended` is history in a registry whose job is living truth.** A cell
recording *when a row changed* is provenance, and the repo already forbids that
class — `trace_text.provenance_findings` flags a spine row whose TEXT carries
its own history. It cannot see a FIELD, which is the only reason this passed.
Git and `docs/archive/` already hold the fact, hold it for every row rather
than seventeen, and cannot drift from it.

**(b) `attestation` invents a second vocabulary for a word the spine had.**
`Modified` is the agreed name for amended-and-unsigned. A parallel
`pending` marker means a reader asking "is this row signed?" checks a different
field per tier.

**(c) `kind` conflates MATURITY with ROW TYPE.** `core`\|`draft` is a status
axis; `edge` is a row-shape axis. One field, two unrelated questions.

**Nothing reads `attestation` or `amended`.** Verified by grep across every kit
script: the only `attestation` hits are `docs/process.toml [attestation]`, an
unrelated config section. Both fields are inert documentation today.

## 2. Why `kind` can die entirely (not merely be renamed)

The owner's direction is that `kind` goes, not that it is split. That is
mechanically available because **the edge/core half is already derived from the
row's field shape** — the legacy markdown reader does exactly this derivation
today, in `spine_carrier.needs_from_markdown`:

```python
row_kind = kind or ("edge" if len(cells) - 1 == len(SN_EDGE) else "core")
...
if kind is None and any(n in SN_EDGE for n in names if n):
    row_kind = "edge"
```

with `SN_CORE = (need, why, priority, acceptance)` and
`SN_EDGE = (lifecycle, scenario, expected)`. The two shapes are disjoint, so a
row's type is a function of the keys it carries. Declaring it is the
**declared-where-derivable** pattern the repo is already retiring elsewhere
(re-tier v2 R4, `this_project`).

That leaves `kind = "draft"` as the only non-derivable thing the field carries —
and that is precisely what `status = "Drafted"` says.

So: **maturity → `status`; row type → derived from field shape.** `kind` has
nothing left.

> **Open sub-question for the owner.** Whether `edge` should stay derived-only
> or whether edge needs are better off as their own registry. This plan assumes
> derived-only (the smaller change). Zero edge rows exist in this repo today —
> all 27 are `core` — so the derivation is currently untested against live data
> and only the template's example exercises it. That is an argument for
> deciding it deliberately rather than by default.

## 3. Target shape

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
The 17 rows carrying `attestation = "pending"` become `status = "Modified"`;
the other 10 become `status = "Approved"`.

**The 17-vs-18 discrepancy is resolved by this change, not carried through it.**
Three places in prose say 18 amended rows; the registry carries the marker on
exactly 17 (`attestation` and `amended` agree with each other perfectly —
SN-001/003/005/006/009/011/012/023/025/026/027/028/029/034/035/038/039). Sol's
own F2 row says 17 and names them. **The prose "18" appears to be the error**,
but this must be confirmed against the actual amendment set before any row is
written as `Approved` — writing a genuinely-amended row as signed is the one
failure mode this whole change exists to prevent.

## 4. Blast radius — measured, not estimated

**Readers of SN `kind`** (every one, from grep):

| file | site | change |
|---|---|---|
| `spine_carrier.py` | `:938` drafted-id selector | `kind == "draft"` → `status == "Drafted"` |
| `spine_carrier.py` | `:782-787, :804, :860` markdown reader + edge branch | keep the derivation, stop emitting a `kind` key |
| `check_docs.py` | `:558` draft-need exemption | same selector swap |
| `derive_gate.py` | `:285` docstring + the drafted-SN rung | rung logic is unchanged; the SELECTOR and its docstring move |
| `trace.py` | `:1254` docstring | same |
| `migrate_carrier.py` | `SN_CORE`/`SN_EDGE`, `read_sn` | the legacy converter learns the new shape |

**Registries and docs:** `stakeholder-needs.template.toml` (the whole
"MATURITY IS A FIELD, NOT A SECTION" header block is rewritten),
`RESYNC_PACK.md` (a migration entry — this is a **downstream-visible schema
change**, so adopters need the note), this repo's own
`stakeholder-needs.toml` (27 rows), and **`spine_carrier.SPINE_TIER_KEYS`
gains its missing `"SN-ID"` entry** (owner ruling 2026-08-17, deliverable
added below as step 7).

**Tests:** 23 SN-specific `kind` assertions across 5 files —
`test_check_docs.py`, `test_check_need_form.py`, `test_migrate_carrier.py`,
`test_hats.py`, `test_rule_sync.py`. *(The raw grep for `kind` in `tests/`
returns 199, but most are unrelated senses — work-item `kind`, `REL-ID` `kind`,
`agent_common._coerce(value, kind)`. The 23 is the honest number.)*

**Not affected:** the derived gate's arithmetic (the SN rungs read *drafted-ness*,
which survives under a new name), `hats.py` (reads `tags`, not `kind`), and the
`attestation`/`amended` deletion (no reader at all).

## 5. Sequencing

Steps, each independently revertible, in the `2026-08-15-d9-migration-plan.md`
shape:

1. **Confirm the amendment set** — resolve 17 vs 18 against git before anything
   is written as `Approved`. Blocking; everything else waits on it.
2. **Add `status` beside the existing fields**, dual-read in the selectors
   (`status` wins, `kind` is the fallback). Nothing breaks; both shapes parse.
3. **Migrate the 27 rows** — write `status`, delete `attestation`/`amended`.
4. **Drop the `kind` fallback** from the selectors; derive `edge` from field
   shape at the one site that needs it.
5. **Delete `kind`** from the 27 rows and the template; rewrite the template
   header.
6. **`RESYNC_PACK.md` entry** + the tests + the goldens.
7. **Close the SN schema census** (owner ruling 2026-08-17, log
   `2026-08-17k`; the guard gap behind the template's missing `tags`, found
   at the shipped-docs audit — log `2026-08-17j`). Add the `"SN-ID"` entry to
   `spine_carrier.SPINE_TIER_KEYS` with the POST-unification key set
   (`status · tags · need · why · priority · acceptance`), and wire the SN
   tier into `test_dogfood_sync`'s three-leg template ↔ live ↔ schema
   comparison — SN is today the ONE spine tier outside it, which is exactly
   how the template shipped without `tags` while the live registry gained it.
   The need table's `[need.SN-###]` shape differs from the row tiers, so the
   test side may need a small reader addition — that wiring is part of this
   step, not a follow-on. Sequenced HERE deliberately: adding the census
   before the unification would pin the dying `kind`/`attestation`/`amended`
   set and force the census to be edited twice.

## 6. The timing argument

**Run this BEFORE signing.** No `docs/archive/last_approved/` snapshot exists,
so every SN row awaits a *first* approval and the brief renders current text
rather than a diff. Changing the field shape today costs **zero
re-attestation**. After the sitting it costs a re-attest of every touched row —
and the owner would have signed 17 rows carrying a field pair already rejected.

This is the same argument that made the `2026-08-16p` acceptance-criteria
correction free, and it expires at the sitting.

## 6a. The off-spine half — a second, separable step

§4–§5 scope the SN change only. The off-spine registries (§0) are a **separate
decision and a separate step**, deliberately not folded in: SN is 27 rows in the
tier a sitting is already reading, while the off-spine change is 141 rows in
registries nobody is signing this week.

The call to make, per registry, is *which* alignment:

- **Rename to `status` and adopt the closed vocabulary** — one word everywhere,
  one cross-registry query. Costs 141 rows plus every reader of `approval`/
  `state`, and forces `Modified` onto tiers that may have no re-attest concept.
- **Keep a separate field, fix only the collision** — leave `approval`, and
  re-word `components.state`'s `planned`/`verified` to values that do not
  collide with retired spine words (`designed`, `implemented`). Much smaller;
  leaves three spellings of one axis standing.
- **Decide `components.state` is a different axis entirely** — it arguably
  describes *build progress*, not *approval*, in which case the fix is to
  RENAME the field to say so (`build_state`) and the collision is the only
  defect. Note this reading makes finding (a) sharper, not weaker: two axes
  sharing a word is exactly why the collision misleads.

**Whichever is chosen, (a) is worth fixing on its own** — a shipped template
declaring a vocabulary containing two words this kit retired last week is a
downstream-visible contradiction, independent of any unification.

## 7. What this plan does NOT decide

- Whether `edge` becomes a derived shape or its own registry (§2's sub-question).
- Whether the SN `status` should then be WIRED — nothing reads the current
  marker, and a `status` field nobody checks is the same defect with a better
  name. Candidates: `trace.py` refusing to treat a `Modified` need as ratified,
  and the ratify brief grouping by it. Sizing that is a separate pass.
- The third status word. The owner floated *"drafted, approved, and founded (or
  decomposed to its dependencies)"* — a possible replacement for `Modified`
  whose meaning is "this row's children exist and answer it". That is a
  **spine-wide vocabulary question**, not an SN one, and it should not ride this
  change.
