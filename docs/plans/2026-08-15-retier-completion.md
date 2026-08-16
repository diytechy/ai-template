# What is preventing the re-tier from completing

> **RESOLVED (2026-08-15, same day): every blocker below was executed or ruled
> during the charge-through — WI-456/457/458/459/460 are all complete, OI-29
> and OI-30 are ruled, and the verification (second read + cross-family round
> 2) ran.** This document remains as the analysis of record; the live surface
> is [2026-08-15-review-package.md](2026-08-15-review-package.md).

**Written 2026-08-15, immediately after `WI-451` merged to trunk as `partial`.**
Asked for by the owner in session: *precisely* what stands between the merged
state and a finished re-tier — stated so it does not conflict with the sitting-3
plan, and naming anything that needs to pull forward.

**Nothing here is ruled.** Three follow-up work items are minted against it
(§5); the rulings they need are listed with each blocker.

---

## 0. What "complete" means, in the owner's own framing

> *"Reshuffling / grouping / tiering SRs/LLRs/Interfaces is the entire purpose
> of the re-tier exercise, and to make sure the new constraints properly can
> express this repository itself (and if not, where the gaps are)."*

That is **two** obligations, and only the first is normally tracked:

1. **The re-tiering itself** — every obligation at the altitude it belongs to,
   under the locked six-crossing frame. §2 and §3 are what remains.
2. **The constraint-fit question** — can the new frame *express this
   repository*? Where it cannot, the gap is a **deliverable of the exercise, not
   a failure of it** (owner, log `13s`). §4 is that answer, and it is the part
   no checker reports, because a constraint that cannot express something stays
   silent about it.

**§4 is the section to read if you only read one.** The re-tiering work in §2–§3
is bounded and known. The expressiveness findings are neither, and the sharpest
one is that **the frame does not partition the requirements at all**.

---

## 1. What is DONE — the baseline this measures against

Merged to trunk 2026-08-15 (`7674e4a1`), `WI-451 = partial`:

```
SN=27  SR=64  LLR=153  TC=148
orphans=0  integrity=0  component-findings=0  interface-findings=0
form-findings=2 (both recorded waivers: SR-140, SR-147)
full suite: 2492 passed, 10 skipped
```

The SR tier went **149 → 64**. `Boundary-Refs` is populated on all 64 rows. The
73 demotions needed **zero new design rows** — every obligation fit an existing
carrier, which is the census's "these were always LLRs" claim confirmed
mechanically rather than asserted.

Authoritative remainder: the close report's `## Not delivered` section,
[handbacks/WI-451-wi451-sr-retier-campaign.md](../handbacks/WI-451-wi451-sr-retier-campaign.md).
This document is that list, measured and grouped.

---

## 2. BLOCKER CLASS A — seven unruled authoring calls

Each is a mint / merge / re-classify decision of the **same class already
handled inline this month** (the SR-141 merge). None is a sitting. All seven are
`WI-458`.

| # | Call | Evidence | IF rows it moves |
|---|---|---|---|
| **H1** | The frame's own named B-05 observable — *"the package exists, is complete and consumable"*, the MAPPING manifest — **has no row**. 15 rows were minted and the one §1R.6 spelled out was not; `MAPPING` survives only in SR-163's *rationale*. Already pinned by `test_bootstrap`/`test_dogfood_sync`, so the obligation is real and merely unstated. | ledger line 330 | none |
| **H4** | **SR-148 / SR-153 / SR-059 all state (SN-025, loop work-selection)** — ordering twice, "no hand-maintained pointer" three times. Textually the same class as the SR-141 merge already performed. | ledger 331 | **6** — IF-053/054/071/085/088/089 via SR-153 |
| **H5** | **SR-031 and SR-137 both claim the tomllib-vs-sh observable, and have already DIVERGED** — only SR-031 names the fail-OPEN decoy. The act-2 partition note went into SR-031's rationale; the observable itself never moved. | ledger 332 | **2** — IF-032, IF-037 |
| **M1** | **Four rows escaped demotion against the campaign's own criterion** — SR-008, SR-021, SR-030, SR-133 (SR-133's rationale literally reads *"Decomposed from SR-006"*). **SR-008 and SR-133 are `Verified`.** | ledger 333 | **3** — IF-013/022 via SR-008, IF-015 via SR-030 |
| **M3** | **Three needs have zero textual coverage despite `orphans=0`** — SN-026's consent surface, SN-037's discrete/variable signal typing, SN-029's delegated-approval record. `orphans=0` proves each SN has ≥1 citing row, never that the row carries the whole need. | ledger 334 | none |
| **X1** | `SR-137` boundary refs revised `["B-01","B-02"]` → `["B-01","B-04"]` in act 7, **flagged for overrule**. | act 7 | none |
| **X2** | `SR-139` revised `["B-02"]` → `["B-02","B-05"]`, **flagged for overrule**. | act 7 | none |

**Why X1/X2 cannot be left to a checker:** `trace.py` verifies that a crossing
reference *resolves*, never that it is the *right* crossing. Nothing mechanical
can catch a wrong answer here. They need eyes or they stand unexamined.

**M1's attestation objection is DISSOLVED, not deferred.** The owner ruled
2026-08-15 that overriding a historical attest is fine where it improves the
design — *"that is the entire purpose of this exercise."* So SR-008 and SR-133
being `Verified` is no longer a reason to leave them mis-tiered. The demotion
calls themselves are still owed.

**Also in class A, and smaller:** `SR-165` is `Draft` and **has no design row
and no test case**, so it cannot leave `Draft` by any route. Its verification
was flipped Inspection → Test in act 7, deliberately, which is what created the
obligation.

### The sequencing rule that must not be inverted

**Rule class A before any interface-registry work.** Measured: class A moves
**11 interface rows'** `sr_refs`. The ruled interface model (log `2026-08-15a`)
moves **zero** SR ids — its owner cell lands on the IF row. So the churn is
one-directional. Reversed, those 11 rows are re-pointed twice.

---

## 3. BLOCKER CLASS B — the verification the campaign declared it owed

Both are `WI-460`, and both must run **after** class A, on the settled state.

- **A second top-down read of the 64-row layer against the six crossings.** One
  read has run in each direction and closed the orphan set. The ledger names a
  second read of the layer *now that the layer exists to read* as the honest
  remaining check.
- **Adversarial round 2.** Round 1 is **spent** — it returned
  CHANGES-REQUESTED with 5 MAJOR findings, all confirmed and fixed, and the
  fixes postdate its verdict. A round is spent by the next commit, so round 2
  belongs last.

**Two defects that reached the merge bar are why this class is not optional.**
Both had the same cause — a bar that was not being run:

- `check_flows` refused the merge: the Runtime flows cited **eight ids the
  campaign had demoted** (SR-029/057/060/093/115/124/131/132). Nothing earlier
  caught it because the flows are hand-authored prose only `check_flows` reads,
  and the per-commit smoke tier does not run it.
- The lane worktree **had no `ruff`**, so every commit on that branch was made
  with `format` SKIPped, and two files carried unformatted code to the merge.

Act 4 already recorded "the smoke-only bar" as the cause of its five findings.
This is the third and fourth instance. **The lesson has not yet been converted
into a guard.**

---

## 4. BLOCKER CLASS C — where the new constraints CANNOT express this repository

The owner's second obligation. These are findings, not chores: each is a place
the frame is silent about something true of the repo.

### C1 — The six-crossing frame does not partition the requirements

Measured on merged trunk:

| Crossing | SRs referencing it | Interfaces realizing it |
|---|---|---|
| B-01 | 5 | **0** |
| B-02 | 2 | **0** |
| **B-05** | **55** | 7 |
| B-04 | 6 | 1 |
| B-06 | **1** | **0** |
| B-07 | **1** | **0** |

**B-05 carries 55 of 70 references — 79%.** B-06 and B-07 carry one row each.
A partition in which one cell holds four fifths of the population is not
classifying anything; it is a default with five exceptions.

This is the single most important open question about the re-tier, and it is
genuinely open in both directions:

- **Either B-05 is under-decomposed** — it already needed a *sixth* bucket
  minted at ruling `2026-08-14c` (the "package-wide property" class) to absorb
  four rows that fit none of its five, which is evidence the bucket set was
  already straining; or
- **the frame is correct and the imbalance is real** — this repo's product
  genuinely is one package crossing one boundary, and the other five crossings
  are thin because the repo is thin there.

**Nothing in the registry distinguishes these two readings**, and the difference
decides whether the re-tier is done or half-done. Raised as `OI-29`.

### C2 — Four of six crossings have no realizing interface

B-01, B-02, B-06 and B-07 are declared crossings that **no interface row
realizes**. This is the *second* condition on sitting-3 decision 8, and the
first (`Boundary-Refs` populated) is now **met**. See §5.1 — this is the
pull-forward.

### C3 — The interface tier has no schema tier at all

Re-verified: `trace.py`'s required-field and enum dictionaries carry keys for
SR, LLR and TC **only**. There is no IF key. On an interface row **nothing is
required, nothing is enum-checked, and nothing bounds a cell's content.**

So the re-tier tiered SR and LLR against real constraints and tiered IF against
**none**. "Reshuffling SRs/LLRs/**Interfaces**" is only two-thirds mechanized.
This is OI-14 Part B's own ruled direction (*"ADDING A SCHEMA TIER, not writing
more prose"*) and it is step 1 of
[the interface rework plan](2026-08-15-interface-rework-plan.md).

### C4 — The consequences of C3, measured

- **24 of 115 endpoint cells do not resolve.** 10 are genuine rot (four name
  `docs/requirements/system-requirements.csv`, a file that became TOML; plus
  `agents.csv`, `open-items.csv`, `stakeholder-needs.md`,
  `performance-budgets.csv`, `subagent-gate`, `coverage.json`). 14 are
  legitimately external (`downstream adopter` ×8, `git`, `agent CLI`,
  `upstream docs`, `run.* launchers`) but **carry no marker saying so**, which
  is precisely why they are indistinguishable from the rot.
- **`IF-097`'s counterpart holds three endpoints in one scalar cell**
  (`scripts/agent_loop;scripts/plan_briefs;scripts/plan_runner`), so any
  per-seam count is approximate.
- **110 of 115 seams are cited by no test case**, against PROCESS §8's
  "every interface is backed by an SR and a contract/fixture test."
- **Seven arch-map modules are named by no interface row at all**
  (`check_vocab`, `handback`, `hats`, `lane`, `spec_move`, `traj_graph`,
  `traj_render`).

`trace.py` already warns on the unresolvable endpoints — that check exists and
is advisory. **The plan's step 2 is therefore already half-built**, which is
worth knowing before anyone scopes it.

### C5 — Ownership and flow are still one column

Ruled 2026-08-15 (Q2): *"a 'provide' … implies directionality, but does not mean
it is actually directional."* Today `direction` fuses both. Until they separate,
the registry cannot say "X owns this seam, and nothing flows either way" — the
form every physical/mutual interface takes. This repo has no physical seams, so
**nothing here will ever surface the gap**; it is real for adopters only.

### C6 — One home per behaviour is unsatisfiable against today's tree

**12 duplicated behaviours across 39 (behaviour, home) pairs in 16 modules.**
The primary constraint of the whole partition — a behaviour owned by two
components makes a partition *invalid, not merely expensive* — does not hold on
the current tree. `WI-448` (the common-module program) owns deleting the copies.
Nothing in the re-tier can close this, and **any provider-uniqueness check
shipped before WI-448 lands is red on day one against a backlog it does not
own.**

### C7 — `cross_component_findings` is vacuous for 46 of 113 rows

Deliberately so, for any endpoint carrying no component tag. `component-findings=0`
honestly means *"no findings among the 67 classifiable rows."* Confirming the
other 46 are covered by the containment rule was owed when the partition was
ruled and has not been done.

### C8 — `Aspect` describes 21 of 64 rows

43 carry none. That is the **ruled** end state (`2026-08-14h`: derivable values
dropped, not remapped), so it is not a defect — but it means the vocabulary
classifies a third of the tier, and it is worth stating plainly rather than
reading `Aspect` as a partition.

---

## 5. Relationship to sitting 3 — no conflict, one pull-forward

**Sitting 3 keeps everything it owns.** Nothing in §2–§4 duplicates or
pre-empts it:

| Sitting-3 scope | Status | This document |
|---|---|---|
| Decisions 1–4 | RULED (`14b`/`c`/`f`) | consumed, not re-opened |
| Decision 5 — the D-9 + D12 vocabulary program | RULED `14e`: **ONE SEQUENCE with the ratification wave** | **untouched.** No WI here flips a Status or closes an enum. |
| Decision 6 — `Planned`'s fate (16 live rows: 10 SR, 2 LLR, 2 TC + 2) | SCHEDULED into #5 | **untouched** |
| Decision 7 — off-spine approval authority | SCHEDULED into #5 | **untouched** |
| The 27 LLR/TC draft ratifications | sitting 3's | **untouched** |
| Signing the §2.1 window | an attestation, sitting 3's | **untouched** |
| Decision 9 — human-agent entity | RULED `14d` CONFIRMED | consumed |

**The one thing that should pull forward: DECISION 8, crossing ownership.**

It was ruled `2026-08-14d` as **DEFERRED**, re-landing by name *"after slice 2
populates `Boundary-Refs` + the D-3 re-key"*, and it asks exactly this: *"for
each of B-01/02/04/05/06/07, which SRs and IFs realize it, and who owns closing
each gap."*

- **Condition 1 is now MET** — `Boundary-Refs` is populated on all 64 rows.
- **Condition 2 is not** — the IF tie-back re-key is D-3's, still unexecuted on
  the `wi455-architecture-retirement` lane.
- **The owner expected it "may effectively dissolve in the full re-tier."
  It has not.** §4 C1/C2 is the measured answer, and it is a *finding*: one
  crossing holds 79% of the rows, and four crossings have no realizing
  interface.

**Why it should move rather than wait:** it is a **tiering and grouping**
question — the re-tier's own purpose — not a vocabulary or ratification
question, which is what the rest of sitting 3 is. Leaving it in sitting 3 files
the sharpest re-tier finding under a sitting about status words. It is minted as
`WI-459`, and pulling it forward **removes** work from sitting 3 rather than
adding any.

---

## 6. The work items minted

| WI | Scope | Depends on | Needs a ruling? |
|---|---|---|---|
| **WI-458** | Class A — the seven authoring calls (H1, H4, H5, M1, M3, X1, X2) plus SR-165's missing design row and test case | — | **Yes**, seven of them; each carries a recommendation |
| **WI-459** | Class C1/C2 — crossing ownership, decision 8 pulled forward: the B-05 79% imbalance and the four crossings no interface realizes | WI-458 (it moves boundary refs) | **Yes** — is B-05 under-decomposed, or is the imbalance real? (`OI-29`) |
| **WI-460** | Class B — the second top-down read and adversarial round 2, on the settled state | WI-458, WI-459 | No |

**Already queued, not re-minted:** `WI-456` (adjudicate the 16 ratified/routed
SR cells the merge amended), `WI-457` (dispose the close), `WI-448` (the
common-module program that C6 waits on), `WI-452`.

**Deliberately NOT minted:** the interface schema tier (C3/C4/C5). It is
[the interface rework plan](2026-08-15-interface-rework-plan.md)'s steps 1–8,
whose model is ruled and whose execution is not. Minting a WI for it here would
give one program two homes — the exact defect this repo keeps correcting.
