# Sitting 3 — verify the adapted spine

**Status: PARTIALLY MET — §0 is the measured scoreboard (2026-08-14).** The
build half of sitting 2's rulings is executed; **slice 2 of the re-tier is
deliberately parked on this sitting's census ratification**, so the sitting
opens with two ruling movements (§0.2) before its verification half can run.
Its subject is not the frame: it is whether **the re-stated system
requirements are functional**, and whether the re-attest windows that sitting 2
deliberately left open **close honestly**.

This document exists now, before it can be run, on purpose: **it defines the bar
so the executing sessions aim at it.** A builder re-stating 57 SRs should know
what will be asked of the result before they write the first row, and the
windows that must stay open should stay open deliberately rather than by
oversight. *(Preconditions re-worded 2026-08-14a to the final 13u rulings:
architecture derives, `counterpart` retires with the slimming, and the census
universe is all 148 SRs — the re-tier campaign, not the old 57-row
re-statement.)*

Assembled 2026-08-13 alongside its sibling
[`2026-08-13-sitting-2-boundary-and-context.md`](2026-08-13-sitting-2-boundary-and-context.md),
which carries the rulings this one verifies. The carriers both were built from
are archived at
[`../archive/plans/2026-08-13-sitting-pack.md`](../archive/plans/2026-08-13-sitting-pack.md)
and
[`../archive/plans/2026-08-13-devstg-boundary-draft.md`](../archive/plans/2026-08-13-devstg-boundary-draft.md).

---

## 0. State of play — measured 2026-08-14, after the mechanized tranche

*(Added 2026-08-14 so the sitting can open from one document. Everything below
was measured on trunk at the basis line `SN=27 SR=149 LLR=152 TC=149 drafts=27
modified=51 uncovered=7` (drafts moved 29 → 27 by the 2026-08-14f carrier-pair
lifts); re-derive at convening per §2.1's own rule.)*

**What landed since assembly (all through adversarial verdict rounds):** the
schema row is merged — `external.toml` live, `interfaces.toml` slimmed to the
approval schema (`stability` retired), the SR-side `Boundary-Refs` field and
SN-037's SR→boundary checker live, both sharp hazards held in-commit. SN-033's
need-form checker is live warn-first with its chain (SR-150 · LLR-170 ·
TC-164 — three NEW rows in the draft window, which is why `drafts` reads 29,
not §2.1's 27). The hats roster is executed per decision 11. `architecture.md`
is retired **through the deletion on the still-open retirement lane** (flows
moved to `docs/runtime-flows.md`, obligation never lapsed; the dashboard's
How-SW tab renders the architecture and embeds the flows) — the lane holds the
measured **D-3 `direction`/`counterpart` shed** (115 rows each; ~85
consumption-shaped IF re-authorings) and the `external.toml` context view as
its honest remainder, sequenced behind this sitting's census ruling.

### 0.1 Preconditions scoreboard (§1's table, measured)

> **STALE AS OF 2026-08-15 — read this first.** This table was measured before
> the re-tier executed. Rows **5, 7 and 8 are now false in substance and true
> only of trunk**: slice 2 is no longer parked (its layers landed on an unmerged
> lane), the `Modified` rows have been touched, and `Area` is retired for the
> closed `Aspect` vocabulary there. They flip the moment that lane merges.
> Re-measure this table at convening rather than reading it — and see
> [2026-08-15-resume-brief.md](2026-08-15-resume-brief.md) for what actually
> changed.

| # | State | Measured fact |
|---|---|---|
| 1 | **PARTIAL** | derived view + flows landed on the retirement lane, not yet merged; `check_flows` disposition = **moved**, never lapsed |
| 2 | **MET** | `external.toml` live on trunk; `trace.py --strict` clean |
| 3 | **MET in letter** | IF-080/IF-081 carry no boundary tie-back field; `direction`/`counterpart` themselves still live — their shed is the retirement lane's held remainder |
| 4 | **MET** | the census is complete — §0.2 below; the WI's Deliverable fills at campaign close, the census doc is the ledger |
| 5 | **OPEN, deliberately** | slice 2 is parked on this sitting's census ratification — no row edited before it (owner-held spine, `human_ratification_through = 4`) |
| 6 | **MET** | `uncovered` 8 → **7** (SN-033 covered); the remaining 7 are the campaign's to supply |
| 7 | **OPEN, deliberately** | the `Modified` rows are untouched since sitting 1 — intent, not drift |
| 8 | rides slice 2 | `Area` still live on 148/149 rows |
| 9 | **MET** | SN-007's `need` reads *"it stays traceable and tested through every change"* — verified verbatim 2026-08-14 |

### 0.2 The census — what this sitting ratifies FIRST

Full per-row ledger: [`2026-08-14-wi451-slice1-sr-census.md`](2026-08-14-wi451-slice1-sr-census.md)
(all 148 rows: crossing · classification · reason class · B-05 capability ·
flags). Headline, re-derived from scratch (13q's ~100 was sizing, and the
prior session's shall-shape stats did **not** reproduce — the census's own
figures govern):

- **HOLDS 34 · RE-STATES 15 · DEMOTES 73 · supersession-tombstones 26** — 88
  rows change text in slice 2; the demotion splits **27 harness-verdict · 30
  unattended-loop · 16 generators** on the B-05 delivered-capability axis
  (scaffold/MAPPING and hook-floor rows hold or re-state).
- Findings the census surfaces as deliverables (13s): **B-06/B-07 have no
  dedicated SR** (the CI-mirror obligation rides SR-019's acceptance cell);
  the migration-history class is ~10 rows larger than the known
  SR-040/059/131; SR-141/SR-148 overlap; SR-049 lacks `area`.

**Two census calls only this sitting can make** (they change slice 2's row
math, so they are ruled BEFORE slice 2 dispatches):

1. **The 26 tombstones — DELETE per the D-4 precedent (recommended;
   census §5-F2's class-waiver framing is superseded by this).** The owner
   challenged the waiver framing (2026-08-14) and the record agrees: the
   D-1/D-4 doctrine — *"a registry states what IS; git is the history"* — was
   performed on 2026-08-11 (`SR-039 → LLR-036 → TC-039` **deleted, not
   marked**, the log entry the forwarding pointer, ids spent forever, citing
   IF rows deleted with their rows, watermarks untouched). The 26 tombstones
   are the OLDER mark-in-place pattern from before D-4 was first performed;
   under the doctrine they are history wearing row ids. Deleting them takes
   SR 149 → 123 and removes 26 waivers from slice 2's math. The mechanical
   follow-through slice 2 owes if ruled so: one log entry as the forwarding
   home for all 26; their citing IF rows go with them (the SR-039 rule);
   `sn_refs` coverage re-checked against the replacement rows; and
   `trace.py`'s supersession machinery (`sr_supersession_findings` et al.)
   plus **TC-099** (inspects the frozen migration map) shrink or retire with
   the class — by ruling, not by lapse. Keep-with-class-waiver remains the
   alternative only if an in-registry pointer is wanted over the log's.
2. **The four package-wide B-05 properties** (SR-031/034/035/114, e.g.
   stdlib-only/cross-platform) — a declared sixth bucket, or forced into the
   five-capability split each carries only partially.

**Movement order for the sitting:** ratify the census + rule the two calls
(and §2.2's TC-159 pick) → dispatch slice 2 under the WI-444 bar → reconvene
on §2's signing surface once slice 2's ledger exists. §2.1 is re-measured
2026-08-14 (the WI-454 mints included, the census's slated exits as its last
column) — regenerate once more at convening, per its own rule.

**Slice 2 runs LAYER-BY-LAYER (ruled `2026-08-14g`; method recorded in the
WI-451 spec's `## Context`).** SN→SR decides what the SR layer *should* be
and reattaches the 49 holding/re-stating rows (the 26 tombstones delete, not
descend); SR→LLR decomposes and lands the 73 demotions under the parent each
obligation belongs to; LLR→TC re-points; then **re-iterate — top-down again,
and bottom-up for dangling/unattached TCs**, against `trace.py`'s orphan
count (9 on the live spine today) rather than judgment. The row-centric
reading — a parent minted per demotion — was rejected as producing ~73 thin
ad-hoc parents. The **D-9/D12 migration stays out of the layers** (`14e`):
per-layer interleaving was weighed and rejected on the global row predicates
and §3.1's silent direction; the order is layered re-tier → one atomic
migration → one signing wave.

### 0.3 THE DECISION LEDGER — every ruling this sitting owes, in one table

*(The sitting-2 §4.0 pattern. Rule top-down: 1–3 unblock slice 2; 4–7 are the
vocabulary/verification program; 8–9 are sitting-2 re-lands whose conditions
are now met. Signing the §2.1 window is an ATTESTATION, not a decision, and
comes only after slice 2's ledger exists.)*

| # | Decision | Recommendation on record | Depth |
|---|---|---|---|
| 1 | **Ratify the census** — the 148-row classification (34 / 15 / 73 / 26) as the shape slice 2 executes | **RULED 2026-08-14b — RATIFIED** (owner: iteration expected at this scope; overhead direction approved) | §0.2 · [the ledger](2026-08-14-wi451-slice1-sr-census.md) |
| 2 | **The 26 tombstones** | **RULED 2026-08-14b — DELETE per D-4**; follow-through named in §0.2, executed by slice 2 | §0.2 call 1 |
| 3 | **The four package-wide B-05 properties** — SR-031 (policy readers agree) · SR-034 (stdlib + ledger) · SR-035 (stack-agnostic) · SR-114 (cross-OS): each is a property of EVERY delivered capability at once, so none fits a single one of B-05's five ruled buckets | **RULED 2026-08-14c — option A**: the decomposition axis gains the declared sixth bucket *package-wide property*; each stays ONE SR (the 13p invariant's own "crossing-or-**delivered-property**" wording admits it). Re-statement across the five groups passed over | §0.2 call 2 |
| 4 | **TC-159** — lift to `Planned` beside the rows it verifies, or re-point LLR-165's `test_refs` | **RULED 2026-08-14f — LIFTED, both halves**: the §2.3 lift had CROSSED the subject pairs (converter TC-159↔LLR-165, reader TC-160↔LLR-166); re-pointing would have forged a converter-requirement→reader-test edge. TC-159 and LLR-166 both `Draft`→`Planned`; drafts 29→27 | §2.2 |
| 5 | **The D-9 + D12 vocabulary program** — execute, sequence, or defer | **RULED 2026-08-14e — ONE SEQUENCE with the ratification wave**, right after slice 2's drafts land: the signing acts ARE the transition (first commit closes the enum; §3.3 gap recorded owner-visibly; rung-predicate work in the same sequence per §3.4) | §3 |
| 6 | **`Planned`'s fate** under the three-word ladder (16 live rows) | **RULED 2026-08-15 (OI-30 D1, log `2026-08-15k`) — FOLDED OUT into `Approved`, and EXECUTED at the rename (`2026-08-15m`)**: functionally the same rung, "approved" clearer; the fourth-rung option died with its `CMP_MATURITY` collision | §3.5 |
| 7 | **Authority over the off-spine approval elements**, and the dial's form | **RULED 2026-08-15 (OI-30 D3, log `2026-08-15k`) — the dial's form does NOT change**: authority follows the dev-stage ladder directly (`APPROVAL_RUNGS` + `human_approves` beside `DIAL_HOLDS`, unmapped = held), EXECUTED `2026-08-15m` | §3.6 |
| 8 | **Crossing ownership — restated in the locked frame's terms** (sitting-2 D6's own text still says "31 BIF rows"; that is the superseded v1 frame — the live question is over the SIX crossings): for each of B-01/02/04/05/06/07, which SRs and IFs realize it, and who owns closing each gap. The lists are mechanical but EMPTY today — SR-side `Boundary-Refs` sits at 0 of 149 and `trace.py`'s SN-037 advisory says verbatim *"the re-tier campaign is what moves this number"*; the IF tie-back re-key is the retirement lane's held remainder | **RULED 2026-08-14d — DEFERRED**, re-lands by name after slice 2 populates `Boundary-Refs` + the D-3 re-key (owner expects it may effectively dissolve in the full re-tier — recorded so it re-lands either way); B-06/B-07's missing SR already delegated to slice 2. **RE-LANDED AND CLOSED 2026-08-15 — this sitting no longer carries it.** It did NOT dissolve: the table was regenerated (B-05 = 50 of 65 refs, 77%; B-01/B-02/B-06/B-07 realized by no interface row), the B-05 half was ruled by the owner as `OI-29` option (b) — the concentration is real because the template package IS the product — and each unrealized crossing got a named owner (B-01 → SR-019/SR-020, B-06 → SR-151, B-07 → SR-152) or a recorded statement that none should realize it (B-02, conditional on SR-140 shipping). The IF-side re-key stays D-3's. Record: `WI-459`, log `2026-08-15f` | [sitting-2 Decision 6](2026-08-13-sitting-2-boundary-and-context.md#decision-6--the-15-missing-crossings--6-partial-ones-who-owns-them) |
| 9 | **The human-agent entity follow-on** — only the deliberate CONFIRMATION is open: 13k already ruled human-vs-loop *"survives as policy and record, never as an entity split"*, and the frame is LOCKED at five entities; decision 2's applied text asks the sitting to *say so deliberately* rather than let it stand by omission (reversing would mint a sixth entity and re-open the locked frame) | **RULED 2026-08-14d — CONFIRMED**: the human stays inside EXT-001, REL-002 carries the surfacing, the frame stays at FIVE entities | [sitting-2 Decision 2](2026-08-13-sitting-2-boundary-and-context.md#decision-2--adopt-or-amend-the-port-list-and-its-discriminator-self-contained) |

**Delegated unless you pull them up:** the census-surfaced authoring calls —
a dedicated SR for B-06/B-07, the SR-141/SR-148 overlap, the
migration-history strikes (sitting-2 §6 items 2/5/7 ride this window), and
SR-060's dead clause — ride slice 2 under the WI-444 token-verification bar;
the builder executes them row-by-row against decisions 1–3 above.

---

## 1. Preconditions — check these mechanically before convening

**Do not run this sitting on a partially executed set.** Each precondition below
names how to verify it without reading prose.

| # | Precondition | How to verify |
|---|---|---|
| 1 | **The frame is adopted and RECORDED as a DERIVED view.** Decision 1 CLOSED (13o); decision 8 (13u) rules `architecture.md` dies and the record renders from the registries in `PROJECT_STATE.html` — which SATISFIES SN-040 (*"kept with the architecture, not in session prose"*) | the dashboard's architecture tab renders the entities/boundary/relationship rows from `external.toml` (the WI-455 program or its context-view slice landed), and `check_flows`'s obligation has an explicit disposition — moved or retired by ruling, never lapsed |
| 2 | **The registry shape is executed per sitting 2 decision 5.** Either `external.toml` (or whatever name won) exists with entity rows and a resolvable `counterpart` in `interfaces.toml`, or the ruling explicitly chose not to mint it | the file exists and loads; `python project-trajectory/scripts/trace.py --strict` is clean on it; or the log's Decisions entry records the no-mint |
| 3 | **IF-080/IF-081's ruled-internal disposition is executed** (decision 2, 13u; `counterpart` itself retires with the slimming) | under the slimmed schema the two rows carry **no boundary tie-back** (`interface_from_external`/`interface_to_external` absent) — or the schema row's ledger records why one does |
| 4 | **The re-tier census (slice 1) is done** — every one of the 148 SRs classified holds / demotes / re-states against §1R.2's six crossings, the demotion sized per row (13q: the ~100 figure is sizing, never a target) | the campaign row's census ledger exists with all 148 rows dispositioned; the WI's `## Deliverable` records the totals |
| 5 | **The re-tier execution (slice 2) is applied under the WI-444 token-verification bar** — no obligation weakened; every re-stated cell token-compared; every demoted row parented under a surviving SR, its LLR minted, TCs re-pointed, `sn_refs` re-homed; one-shall waivers recorded per row (13v) | the slice's ledger reproduces the WI-444 method with real counts: rows held / demoted / re-stated, LLR ids minted, waivers recorded |
| 6 | **WI-442 has landed** — SN-037…SN-040 gain their first coverage | `docs/gate`'s basis line shows **`uncovered`** below 8; the `sn_refs` of the new SRs name which need each covers |
| 7 | **The 2.4-sweep window and the decision-6 window are still open — deliberately.** Sitting 1's rationale sweep flipped rows `Modified` and called it *"a deliberately re-opened window, sitting 2's to close"*; sitting 2 rules structure and does not sign a spine | those rows are still `Modified` at this sitting's start, and the log records that as intent rather than as drift |
| 8 | **Area→aspect is executed IF sitting 2 ruled it rides WI-451's window** | the `Area` column is gone from `system-requirements.toml` and the six aspect values are a closed vocabulary — or the ruling records that it does not ride |
| 9 | **SN-007's re-word STILL HOLDS** — executed 2026-08-13 by owner ruling in session, *before* sitting 2, superseding the ride-this-window disposition (sitting 2 housekeeping item 1) | `stakeholder-needs.toml` SN-007's `need` reads *"it stays traceable and tested through every change"* and no later edit re-introduced the per-change coverage clause |

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

### 2.1 The window — **re-measured 2026-08-14; regenerate again before the sitting**

Measured 2026-08-14 against the live registries (assembly figures of
2026-08-13 superseded). **The last column is the census's slated exits** —
rows that will LEAVE the tier once §0.2's rulings execute in slice 2; the
status columns describe today's registry, the exits column describes the
pending structural change, and signing happens only after the exits are real
rows-moved. Re-derive at convening; do not sign from this table.

| Tier | Total | Verified | Modified | Draft | Planned | Slated exit (census · pending §0.2) |
|---|---|---|---|---|---|---|
| SN | 27 | — | — | 0 | — | — |
| SR | 149 | 105 | 30 | 0 | 14 | **−26 deleted** (D-4, if ruled) · **−73 demoted** to LLR → ~50 SRs remain |
| LLR | 152 | 122 | 14 | 14 | 2 | +~73 inbound demotion mints (plus parent-SR joins) |
| TC | 149 | 127 | 7 | 13 | 2 | re-points only (demoted rows' TCs follow their LLRs; TC-099 retires with the tombstones — D-4 ruled 2026-08-14b) |

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
LLR-160, LLR-161, LLR-162, LLR-163, LLR-164, LLR-167, LLR-168, LLR-169,
and **LLR-170** (the need-form checker, minted 2026-08-14).

**The 13 `Draft` TCs to ratify** — TC-150, TC-151, TC-152, TC-153, TC-154,
TC-155, TC-156, TC-157, TC-158, TC-161, TC-162, TC-163, and **TC-164**
(the need-form dirty-cell case, minted 2026-08-14).

That is the **LLR/TC draft ratification** sitting 1 deferred plus the two
2026-08-14 mints: **14 + 13 = 27 rows**, reconciling exactly to `drafts=27`
in the current basis line. The 14 `Planned` SRs — SR-137…SR-149 lifted at
sitting 1, plus **SR-150** (the need-form checker SR, minted 2026-08-14) —
and the four `Planned` rows LLR-165 / LLR-166 / TC-159 / TC-160 (the carrier
pairs, aligned by the 2026-08-14f ruling) are not in this window.

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

### 3.6 ⚠ The authority dial does not speak for the new approval elements (2026-08-14a)

`human_ratification_through` is defined over **the four spine tiers plus
"nothing"** (`dispatch._kind_action`: *"implementation is not a ratification
tier"*; the comparison is the OI-21 declared lookup over the stage rungs). The
D4/D12 rulings just commissioned approval elements **off-spine** — on
`interfaces.toml` as `stability` retires, and on `external.toml` from its
first commit — and **no value of the dial declares who may flip those**. This
program (D-9 + D12, this section's decision) must extend the authority
declaration to every registry that gains the shared vocabulary — and this is
also where the dial's FORM is worth re-opening if needed: a tier-set (e.g. a
declared list of held registries) covers the off-spine expansion naturally,
where the 0–4 ordinal cannot. (Owner asked 2026-08-14 whether a string-form
item exists: none does — the int ordinal was itself the ruled replacement of
the retired three-word enum. If the form changes, it changes HERE, as one act
with the vocabulary.) Until then, the schema row states `external.toml`'s
flip authority in prose from the first commit.

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
