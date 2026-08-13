# The `Status` ladder migration — a measured checklist

**What this is.** The execution checklist for **D-9** ([`repo-lock.md`](../../repo-lock.md)
§2): `Draft`/`Verified`/`Modified` → **`Drafted` → `Approved` → `Founded`**,
uniform across SN · SR · LLR · TC. It exists so the migration lands as one
reviewed act rather than a discovery exercise at the end of a sitting.

**Nothing here is executed.** Q11 holds the 470-row rewrite behind the P0
sitting: the 38 `Modified` rows must be resolved there first, or retiring the
word launders the re-blessing they owe.

**Figures measured 2026-08-11 at `bc6315d9`.** Commands are given inline so
each is reproducible (the repo's declared-figure convention).

---

## 0. THE FINDING THAT CHANGES THE PLAN — `Status` is open-vocabulary, checked nowhere

D-9's recorded safety property is that deleting the pass rung means *"a stray
`Verified` anywhere is unambiguously an un-migrated row."* **That property has
no enforcer today, and the migration must build one.**

Measured — `trace.ENUM_FIELDS` covers exactly two columns, and `Status` is not
among them:

```
SR: ['Verification']      TC: ['Tier']
Status enum-checked anywhere? False
```

Driven directly, an invented value produces **no finding and no true
predicate**:

```
row = {"SR-ID": "SR-999", "Status": "Bananas"}
is_draft: False   is_verified: False   is_modified: False
```

Every predicate is a case-insensitive match against a magic string, and the
docstrings say so on purpose — *"Status is open-vocabulary; `Verified` is the
value the G3 `--require-verified` criterion and the gate derivation act on."*

**Why this is the plan's first item rather than a footnote.** In a
half-applied migration the failure directions are not symmetric:

| half-migrated row | consequence | loud? |
|---|---|---|
| `Approved` read by OLD predicates | not draft, not verified → row drops out of G3 credit, and loses the Draft exemption from child-completeness rules | **loud** — gate drops, orphan findings appear |
| `Verified` read by NEW predicates | same shape, opposite side | **loud** |
| **`Modified` unmigrated, read by a new `is_drifted`** | `is_modified` False → **the row silently vanishes from the re-attest brief** | **SILENT — this is the laundering direction Q11 exists to prevent** |

So the migration's **first commit** must close the vocabulary: add `Status` to
`ENUM_FIELDS` for SN/SR/LLR/TC with exactly `{Drafted, Approved, Founded}`.
Without it, D-9's self-announcing property is a claim with no mechanism, and
the one failure mode that stays quiet is the one that costs a sitting.

---

## 1. Blast radius, counted

| surface | sites | command |
|---|---|---|
| literal `"Draft"`/`"Verified"`/`"Modified"` in **scripts** | **8** | `grep -rn '"Draft"\|"Verified"\|"Modified"' project-trajectory/scripts/*.py \| wc -l` |
| the same literals in **tests** | **96** | same, over `tests/*.py` |
| shipped **templates + docs** naming the vocabulary | **8 files** | `registries/{system-requirements,test-cases}.template.toml`, `PROCESS.md`, `PROCESS_OPTIONS.md`, `ADOPTING.md`, `EXAMPLE.md`, `README.md`, `KICKOFF_PROMPT.md` |

**Only eight literal sites in the scripts** — because the vocabulary is
centralized in three predicates. The predicates are the migration; the tests
are the bulk of the diff.

### Rows to migrate — 470

| tier | `Draft`→`Drafted` | `Verified`→`Approved` | `Modified`→(sitting)→`Approved` | total |
|---|---|---|---|---|
| SR | 11 | 110 | 25 | 146 |
| LLR | 13 | 130 | 6 | 149 |
| TC | 12 | 127 | 7 | 146 |
| **SN** | 1 (`kind="draft"`) | 28 (18 core + 10 edge) | 0 | 29 |

SN carries **no `status` key at all** — its state is `kind`. See §3.

---

## 2. The predicates — the migration's safety rail

Not symmetrically duplicated, which matters when editing:

| predicate | defined in | note |
|---|---|---|
| `is_draft` | `trace_text.py:45`, `derive_gate.py:132` | `trace.py` re-exports |
| `is_verified` | `trace.py:133`, `derive_gate.py:137` | |
| `is_modified` | `trace.py:142`, `derive_gate.py:233` | docstring: *"recognized for SURFACING, not gate arithmetic"* — so retiring it has **limited gate impact**, its real consumer is the re-attest brief |

`tests/test_rule_sync.py` pins all three equal across modules
(`test_is_draft_agrees` / `test_is_verified_agrees` / `test_is_modified_agrees`,
each over a casing/whitespace/None battery). **That pin is the rail: it must be
updated in the same commit as the predicates, and it must keep testing by
VALUE** — an equality-only pin was already proved vacuous once in this repo
(§7, the SN reader twin: all three copies were byte-identical *and all three
wrong the same way*).

**After migration it must assert:** the three predicates agree, `is_drifted`
(the derived overlay) agrees where duplicated, and — new — that **no predicate
recognizes a retired word**. A pin that only proves the new words work would
let a stale copy keep honouring `Verified` silently.

---

## 3. The SN tier — `kind` splits

Today `kind` conflates two facts: the **tier** (core vs edge-case, which
selects the row's field shape) and the **state** (draft). Measured: 18 core ·
10 edge · 1 draft.

The migration adds `status` and leaves `kind` holding **only** the tier
distinction — one fact, one home. Note this is the *second* time this fact has
moved: D-5 already retired section-as-state (a heading containing "draft")
into `kind = "draft"`, killing a live sharp edge where a prose mention under
the draft heading silently re-drafted an attested need.

**SN readers to update** — the tier with the most parsing code and the least
enforcement (F-6): `trace.sn_all_ids` · `trace.sn_draft_ids` ·
`derive_gate`'s twins of both · `sn_normative_text` ·
`check_docs._registry_needs` · `traj_parse._sn_rows` · `gen_okf.sn_rows` ·
`check_flows`'s inline SN regex · `spine_carrier.folded`.

---

## 4. The traps, by `file:line`

**`derive_gate`'s per-artifact ladder** (docstring §17-38, `sr_gate` ~209-218).
Today: SR `Draft`→G0, ratified-not-decomposed→G1, decomposed→G2, *decomposed
AND `Status=Verified`*→G3. Under a **monotone** ladder that last rung is
simply **"at `Founded`"** — the conjunction disappears, because `Founded` is
above `Approved` by construction. Also owed: the `ex-draft` counterfactual and
the `drafts=` / `modified=` / `uncovered=` basis counters. `modified=` becomes
a **drift** counter and must be renamed with the value, or the basis line
reports a word the vocabulary no longer contains.

**`trace.reattest_model` (`trace.py:1617`)** — signature
`statuses=("modified",)`. Under D-9 that selection becomes a **drift
computation**, which does not exist until D-1's anchor half ships. **Interim
answer owed:** until `TextHash`/`HashedOn` exist there is nothing to compute
from, so either the brief keeps selecting a retired literal (contradicting the
closed enum in §0) or the migration waits on the anchor. **This is the hard
coupling in the plan** — see §5.

**`intake.py:1548`** — `if status != "Modified"` guards the writer that flips
a cell. Under D-9 **nothing authors drift**, so this arm has no successor
value; it either becomes a refusal or the writer's purpose changes. Decide
before touching it; `intake` is also the module that already re-entered the
1500-line monolith threshold.

**The WI vocabulary is SEPARATE and untouched** — `check_trajectory.py:206-219`
declares `OPEN_STATUSES`/`TERMINAL_STATUSES`/`BACKLOG_STALE_STATUSES`
(`draft`/`queued`/`active`/`deferred`/`blocked`/`done`/`cancelled`/`partial`),
mirrored in `agent_common.py:1115-1120`. That is the **directory-as-state**
vocabulary for work items, it is already *closed* (unknown dir = loader
refusal), and a work item is not a requirement. D-9 does not apply. Note the
word `draft` appears in both vocabularies meaning different things — a
pre-existing collision the ladder makes slightly worse, worth a comment at
minimum.

---

## 5. Proposed order, with what blocks what

| # | step | blocked on |
|---|---|---|
| 1 | **Close the vocabulary** — `Status` into `ENUM_FIELDS` with the three values, SN/SR/LLR/TC (§0) | nothing — but it must land *with* step 3, since the enum and the data must agree at every commit |
| 2 | Resolve the 38 `Modified` rows | **the P0 sitting** (Q11) |
| 3 | The atomic act: 470 rows + the three predicates + `test_rule_sync`'s pin + `derive_gate`'s rungs + the basis counters + the SN `kind`/`status` split | step 2 |
| 4 | Prose: `PROCESS.md`, `PROCESS_OPTIONS.md`, the reference doc, `EXAMPLE.md`, `KICKOFF_PROMPT.md` | **must move IN step 3's commit** — changing it earlier makes live documentation false |
| 5 | Templates + `ADOPTING` migration note | step 3 (every adopting repo migrates too) |
| 6 | `reattest_model` / `intake`'s drift arms | **D-1's anchor half** — no `TextHash`, nothing to derive |
| 7 | `Founded` computation wired per tier | SN/SR/TC free today; **LLR's discharge test is its own WI**, in flight |

**The coupling to state plainly:** steps 3 and 6 want to be one commit and
cannot be, because drift-as-derived needs an anchor that does not exist yet.
The honest interim is that after step 3 the repo has **no drift detector at
all** — the 38 rows are resolved and `Approved`, and nothing watches for the
next amendment until D-1's anchor half lands. That is a *regression in
coverage* between step 3 and step 6, and it should be recorded as a known gap
with an owner-visible marker rather than discovered later.

---

## 6. What I could not determine

- **Whether `Founded` is written into the cell or layered at read time.**
  D-9 leaves it open; it decides whether the migration writes one value or two
  per row, and whether `Founded` needs to be in the closed enum at all (if it
  is never authored, an authored `Founded` should arguably be an *error*).
- **What `intake` does instead of writing `Modified`** — needs the step-6
  design.
- **Whether the 96 test literals are behavioral or spelling.** Not classified
  row by row; a sample suggests most pin spelling, but the migration should
  treat each as behavioral until read, because a test that pins spelling is
  free to change and a test that pins *behavior through* a spelling is not.
