# Sitting 3 — verify the adapted spine

**Status: PRECONDITIONS NOT YET MET.** This sitting runs **after** sitting 2's
rulings are executed — WI-451 both slices, WI-442, and whatever sweeps sitting 2
orders. Its subject is not the frame: it is whether **the re-stated system
requirements are functional**, and whether the re-attest windows that sitting 2
deliberately left open **close honestly**.

This document exists now, before it can be run, on purpose: **it defines the bar
so the executing sessions aim at it.** A builder re-stating 57 SRs should know
what will be asked of the result before they write the first row, and the
windows that must stay open should stay open deliberately rather than by
oversight.

Assembled 2026-08-13 alongside its sibling
[`2026-08-13-sitting-2-boundary-and-context.md`](2026-08-13-sitting-2-boundary-and-context.md),
which carries the rulings this one verifies. The carriers both were built from
are archived at
[`../archive/plans/2026-08-13-sitting-pack.md`](../archive/plans/2026-08-13-sitting-pack.md)
and
[`../archive/plans/2026-08-13-devstg-boundary-draft.md`](../archive/plans/2026-08-13-devstg-boundary-draft.md).

---

## 1. Preconditions — check these mechanically before convening

**Do not run this sitting on a partially executed set.** Each precondition below
names how to verify it without reading prose.

| # | Precondition | How to verify |
|---|---|---|
| 1 | **The frame is adopted and RECORDED.** Sitting 2 decision 1 ruled; decision 8 requires the record *"kept with the architecture, not in session prose"* (SN-040's ratified acceptance) | `grep -n "boundary\|external entit\|operational context" docs/architecture.md` returns a real hand-authored section, not the three generated function-summary rows it returns today |
| 2 | **The registry shape is executed per sitting 2 decision 5.** Either `external.toml` (or whatever name won) exists with entity rows and a resolvable `counterpart` in `interfaces.toml`, or the ruling explicitly chose not to mint it | the file exists and loads; `python project-trajectory/scripts/trace.py --strict` is clean on it; or the log's Decisions entry records the no-mint |
| 3 | **The port list is adopted** (decision 2), including the IF-080/IF-081 disposition | those two rows' `counterpart` no longer claims `downstream adopter`, **or** the ruling records why it still does |
| 4 | **WI-451 slice 1 (CENSUS) is done** — each of the 75 script-naming SRs classified port / internal / mixed against the adopted inventory, with the re-statement sized per row | the WI's `## Deliverable` is filled and the row sits in `docs/work/complete/` |
| 5 | **WI-451 slice 2 (RE-STATEMENT) is applied under the WI-444 token-verification bar** — no obligation weakened; every re-stated cell token-compared to its predecessor | the slice's own ledger reproduces the WI-444 method: per-row token multiset comparison, with the count of rows passing stated as a real number |
| 6 | **WI-442 has landed** — SN-037…SN-040 gain their first coverage | `docs/gate`'s basis line shows **`uncovered`** below 8; the `sn_refs` of the new SRs name which need each covers |
| 7 | **The 2.4-sweep window and the decision-6 window are still open — deliberately.** Sitting 1's rationale sweep flipped rows `Modified` and called it *"a deliberately re-opened window, sitting 2's to close"*; sitting 2 rules structure and does not sign a spine | those rows are still `Modified` at this sitting's start, and the log records that as intent rather than as drift |
| 8 | **Area→aspect is executed IF sitting 2 ruled it rides WI-451's window** | the `Area` column is gone from `system-requirements.toml` and the six aspect values are a closed vocabulary — or the ruling records that it does not ride |
| 9 | **SN-007's ruled strike — or the owner's 2026-08-13 proposed replacement text, if sitting 2 confirmed it — is applied INSIDE this window** (sitting 2 housekeeping item 1) | `stakeholder-needs.toml` SN-007's `need` no longer contains *"a change to a script is covered by a test exercised end-to-end against a real scaffold"*, and — if the replacement was confirmed — reads *"it stays traceable and tested through every change"* |

**On precondition 9, specifically.** The strike was ruled 2026-08-11 and was
supposed to land with the prose batch; it did not, and sitting 1 then ratified
the SN registry. A lone edit to a ratified need **opens a re-attest window
outside a batched one** — which is exactly what its own ruling said to avoid. It
must ride **this** window. Do not let a tidy-up session apply it alone.

---

## 2. What you are signing

**The signing surface is [`../open-items.html`](../open-items.html)**, per the
standing pattern — it carries the per-cell before/after word-level diffs with the
baseline revision printed on every section, plus the toolbar box that reveals the
untouched cells. A diff says what moved; an attestation asks whether the evidence
still verifies what the row now *says*. It cannot be honestly reproduced in
markdown, which is why it stays a pointer.

### 2.1 The window as of assembly — **regenerate before the sitting**

Measured 2026-08-13 against the live registries. **These lists will have moved by
the time this sitting runs** — WI-451's re-statement alone touches up to 57 SR
rows. Re-derive; do not sign from this table.

| Tier | Total | Verified | Modified | Draft | Planned |
|---|---|---|---|---|---|
| SN | 27 | — | — | 0 | — |
| SR | 148 | 105 | 30 | 0 | 13 |
| LLR | 151 | 122 | 14 | 14 | 1 |
| TC | 148 | 127 | 7 | 13 | 1 |

*(The SN registry has no `status` field at all — its fields are `acceptance ·
kind · need · priority · why`, and maturity is `kind`. All 27 rows are
`kind = "core"` since sitting 1.)*

**The 30 `Modified` SRs** — SR-003, SR-006, SR-021, SR-023, SR-025, SR-026,
SR-027, SR-028, SR-029, SR-030, SR-040, SR-050, SR-055, SR-070, SR-071, SR-072,
SR-079, SR-080, SR-081, SR-082, SR-083, SR-085, SR-089, SR-090, SR-091, SR-092,
SR-108, SR-112, SR-122, SR-125.

**The 14 `Modified` LLRs** — LLR-002, LLR-018, LLR-034, LLR-040, LLR-081,
LLR-118, LLR-132, LLR-136, LLR-140, LLR-144, LLR-145, LLR-149, LLR-150, LLR-153.

**The 7 `Modified` TCs** — TC-031, TC-034, TC-084, TC-085, TC-098, TC-138,
TC-147.

**The 14 `Draft` LLRs to ratify** — LLR-155, LLR-156, LLR-157, LLR-158, LLR-159,
LLR-160, LLR-161, LLR-162, LLR-163, LLR-164, LLR-166, LLR-167, LLR-168, LLR-169.

**The 13 `Draft` TCs to ratify** — TC-150, TC-151, TC-152, TC-153, TC-154,
TC-155, TC-156, TC-157, TC-158, TC-159, TC-161, TC-162, TC-163.

That is the **LLR/TC draft ratification** sitting 1 deferred: **14 + 13 = 27
rows**, and it reconciles exactly to `drafts=27` in the current basis line.
The 13 `Planned` SRs (SR-137…SR-149) and the two `Planned` rows LLR-165 /
TC-160 were lifted at sitting 1 and are not in this window.

### 2.2 The chain-integrity fix this sitting owes — TC-159

**Pack §2.3 lifted SR-147, LLR-165 and TC-160. It never lifted TC-159 — the TC
that actually verifies LLR-165.** Measured live:

| row | status | what it points at |
|---|---|---|
| **TC-159** | **`Draft`** | `verifies = ["SR-147", "LLR-165"]` |
| TC-160 | `Planned` | `verifies = ["SR-147", "LLR-166"]` |
| **LLR-165** | `Planned` | `test_refs = "TC-159"` |
| LLR-166 | `Draft` | `test_refs = "TC-160"` |

So LLR-165 is a `Planned` row whose only verification is a `Draft` test case,
while the `Planned` test case verifies a `Draft` design row. **The 2.3 execution
left the chain internally inconsistent in both directions.** WI-452 part (2)
(*"confirm … that TC-159/TC-160 still exercise the path"*) will walk straight
into it.

**Two honest resolutions, and this sitting must pick one deliberately rather than
letting a builder pick:** lift **TC-159** to `Planned` alongside the rows it
verifies (the reading that 2.3 simply missed a row), or **re-point** LLR-165's
`test_refs` and accept TC-159 stays `Draft` (the reading that TC-160 was always
meant to be the carrier). Do not let it be resolved silently in a slice.

---

## 3. The D-9 status-ladder decision

**The migration is UNEXECUTED.** D-9 renames `Draft` / `Verified` / `Modified` →
**`Drafted` → `Approved` → `Founded`**, uniform across SN · SR · LLR · TC. The
three target words exist today only as unused constants in `derive_gate.py`. Its
**only** checklist is archived at
[`../archive/plans/2026-08-11-status-ladder-migration.md`](../archive/plans/2026-08-11-status-ladder-migration.md),
whose own header sentence — *"Nothing here is executed"* — is still true.

**⚠ Stale-figures warning.** Every number in that document was measured
**2026-08-11 at `bc6315d9`**, which is *before* the OI-18 edge dissolution, the
prose batch, and sitting 1. Its **470-row per-tier migration table** is
therefore wrong on counts while right on **shape**. Re-derive every figure before
executing; the plan is the structure, not the arithmetic.

The essentials, carried here so the decision is self-contained:

### 3.1 The asymmetric-failure table — the row that decides the whole plan

Verbatim from §0:

| half-migrated row | consequence | loud? |
|---|---|---|
| `Approved` read by OLD predicates | not draft, not verified → row drops out of G3 credit, and loses the Draft exemption from child-completeness rules | **loud** — gate drops, orphan findings appear |
| `Verified` read by NEW predicates | same shape, opposite side | **loud** |
| **`Modified` unmigrated, read by a new `is_drifted`** | `is_modified` False → **the row silently vanishes from the re-attest brief** | **SILENT — this is the laundering direction Q11 exists to prevent** |

And the finding underneath it, driven rather than reasoned:

```
SR: ['Verification']      TC: ['Tier']
Status enum-checked anywhere? False
```
```
row = {"SR-ID": "SR-999", "Status": "Bananas"}
is_draft: False   is_verified: False   is_modified: False
```

> So the migration's **first commit** must close the vocabulary: add `Status` to
> `ENUM_FIELDS` for SN/SR/LLR/TC with exactly `{Drafted, Approved, Founded}`.
> Without it, D-9's self-announcing property is a claim with no mechanism, and
> the one failure mode that stays quiet is the one that costs a sitting.

### 3.2 The hard coupling — `trace.reattest_model` and D-1's anchor

Verbatim from §4:

> **`trace.reattest_model` (`trace.py:1617`)** — signature
> `statuses=("modified",)`. Under D-9 that selection becomes a **drift
> computation**, which does not exist until D-1's anchor half ships. **Interim
> answer owed:** until `TextHash`/`HashedOn` exist there is nothing to compute
> from, so either the brief keeps selecting a retired literal (contradicting the
> closed enum in §0) or the migration waits on the anchor. **This is the hard
> coupling in the plan.**

The sibling trap, same section: **`intake.py:1548`** guards its cell-flipping
writer with `if status != "Modified"`, and under D-9 **nothing authors drift**, so
that arm has no successor value — it becomes a refusal, or the writer's purpose
changes. Decide before touching it.

### 3.3 The declared coverage regression between steps 3 and 6

Verbatim from §5:

> **The coupling to state plainly:** steps 3 and 6 want to be one commit and
> cannot be, because drift-as-derived needs an anchor that does not exist yet.
> The honest interim is that after step 3 the repo has **no drift detector at
> all** — the 38 rows are resolved and `Approved`, and nothing watches for the
> next amendment until D-1's anchor half lands. That is a *regression in
> coverage* between step 3 and step 6, and it should be recorded as a known gap
> with an owner-visible marker rather than discovered later.

**Ruling that gap is part of this decision.** A migration that silently removes
the only drift detector is exactly the class of change this repo's process exists
to refuse doing quietly.

### 3.4 OI-21 execution question 5c — the ONE-sequence coupling

OI-21's fifth execution question, sub-decision (c), verbatim from
[`../requirements/open-items.toml`](../requirements/open-items.toml):

> (c) SEQUENCING against the D-9 ladder migration (repo-lock section 5 step 7),
> which rewrites the same `is_draft`/`is_verified`/`is_modified` predicates in
> the same file - the two programs must land as one sequence or the insert
> hazard this brief records fires in the gap between them.

So D-9 is not a standalone tidy-up: **the rung-predicate work and this migration
are one program**, and scheduling either alone re-opens the other.

### 3.5 ⚠ The new fact: `Planned` is already live, outside D-9's ladder

Sitting 1 introduced a **fourth** status value — **`Planned`** — when it lifted
the 13 Draft SRs, LLR-165 and TC-160. Measured live: 13 SRs, 1 LLR and 1 TC carry
it. **D-9's target vocabulary has exactly three values** (`Drafted`, `Approved`,
`Founded`), and §0's first commit is to close the enum to precisely those three.

**These cannot both stand.** The sitting must either:

- **re-scope D-9's target vocabulary** to admit `Planned` (or its successor) as a
  fourth rung — which changes the enum, the predicates, and every figure in the
  §1 table; or
- **rule `Planned` out** before this window closes — deciding what those 15 rows
  become under the three-value ladder.

Whichever way it goes, it must be ruled **before** the window closes, because
after the window every one of those rows is a ratified row and moving it costs a
new window.

---

## 4. Close mechanics

Adapted from the sitting pack §5, corrected for the current state.

1. **You sign in [`../open-items.html`](../open-items.html)** — that is where the
   per-cell evidence lives, with the baseline revision printed per section.
2. **The signed rows' `Status` moves in a reviewed commit**: `Modified` →
   `Verified`, `Draft` → `Planned`. **[`../gate`](../gate) is DERIVED, never
   hand-set.**
3. **`python project-trajectory/scripts/derive_gate.py`** regenerates the bar; the
   `drafts` / `modified` / `uncovered` counts fall and the bar rises on its own
   arithmetic. Freshness `--check` is a commit-bar step, so a stale `docs/gate`
   is a red.
4. **Regenerate the dependent surfaces** — `trunk_step.py --regen` covers
   arch-map, okf, derived-gate, trajectory, status and open-items. **If sitting 2
   minted an external-entity registry, confirm its generated context view is in
   that set** rather than a hand-maintained block.
5. **Record the attestation as a row in [`../log.md`](../log.md) `## Sittings`** —
   a named human, the date, and **the rung range the sitting certifies** (OI-21
   ruled sittings stay their own axis: fewer sittings than boundaries, each
   naming its range). The table's existing rows preserve the retired `G*`
   vocabulary verbatim under the OI-21 attestation carve-out; the header note
   carries the translation.
6. **Run the full unfiltered suite and `check.py` at the derived gate**, and paste
   the real output. The per-commit bar is the smoke tier; a sitting close is not a
   commit — it takes the full tier.
7. **Merge-to-main and push stay yours.** Everything is committed locally on
   `infra/mechanized-loop`; this repo runs `push = "human"`.

**The basis line as of assembly** ([`../gate`](../gate), computed 2026-08-13) —
**it will have moved by the time you close, and that movement is the point:**

```
# basis: SN=27 SR=148 LLR=151 TC=148 drafts=27 modified=51 uncovered=8 computed=DevBar-Below ex-draft=DevBar-Below phase=5 per-phase=1=DevBar-Tests;2=DevBar-Tests;3=DevBar-Tests;4=DevBar-Below;5=DevBar-Below stage=DevStg-Boundary stage-ord=1 stage-of=8
# computed 2026-08-13 (as-of 94408245)
DevBar-Reqs
```

Read it honestly: the value is the bar that must next be **CLEARED**, the MIN
over every in-scope row's own bar floored to `DevBar-Reqs`. `drafts=27` +
`modified=51` are the window this sitting closes; `uncovered=8` is the coverage
WI-451 and WI-442 are supposed to have supplied; `stage=DevStg-Boundary` is what
sitting 2's rulings were meant to clear. **If `stage` has not advanced past
`DevStg-Boundary` when you convene, precondition 1 has not really been met** —
whatever the prose says.
