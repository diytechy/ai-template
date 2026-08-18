# Sitting 3 — verify the adapted spine

> **RE-STAMPED 2026-08-16 — READ THIS BANNER, THEN §0.4.** Everything in §0.1,
> §0.2 and §2.1 was measured on **2026-08-14**, before the re-tier merged and
> before re-tier v2 ran; **none of those figures survived the day** — re-derive
> at convening from [`../gate`](../gate)'s basis line and the regenerated brief,
> never from a table here. What changed structurally: **the decision ledger
> (§0.3) is 9 of 9 RULED**, so this sitting is owed no ledger ruling at all.
> What it is owed is the **ATTESTATION** — the LLR/TC draft ratifications, the
> re-attest window, and the status-vocabulary sequence's remainder (§3, whose
> steps 1–5b are executed) — plus the calls that arrived *after* this ledger was
> written. **[§0.4](#04-what-the-2026-08-16-work-adds-to-this-desk) is the desk:
> what today's work put on it, which calls are genuinely open, and which the
> sitting only countersigns.** The procedure that runs the sitting is
> [`2026-08-15-review-package.md`](2026-08-15-review-package.md) §5.

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
> Re-measure this table at convening rather than reading it — and see the log's
> `2026-08-15*`/`2026-08-16*` Decisions for what actually changed. (The resume
> brief this note used to point at was archived 2026-08-16 as superseded:
> [`../archive/plans/2026-08-15-resume-brief.md`](../archive/plans/2026-08-15-resume-brief.md).)

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

> **SUPERSEDED BY EXECUTION 2026-08-15/16 — this sitting no longer ratifies the
> census; it reads the result.** Both "census calls only this sitting can make"
> below were **RULED 2026-08-14b/c** (ledger rows 1–3); slice 2 executed and
> **merged to trunk** (`2026-08-15b`…`f`), and re-tier v2 then re-tiered the
> surviving layer again under R1/R2 (`2026-08-16c`…`i`). Kept whole for the
> reasoning and the per-row ledger it points at — **not for its arithmetic**.

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

> **RECONCILED 2026-08-16 — ALL NINE ARE RULED; each row carries its closing
> id.** Rows 1–4 and 9 closed at the 2026-08-14 sitting-adjacent rulings, rows
> 6–7 at the OI-30 rulings (`2026-08-15k`/`l`, executed `2026-08-15m`), row 8
> re-landed and **left this sitting entirely** (`2026-08-15f`), and row 5's
> program is executed through its step 5b (`2026-08-15g`/`m`) with only the
> signing half outstanding. **Nothing is deleted from this table** — a ruled row
> is the record of what was ruled and by which entry. **The consequence for the
> sitting: it owes no ledger ruling.** What it owes is the attestation (§2.1's
> window, re-derived) plus the calls in **§0.4**, which arrived after this
> ledger was written and therefore appear nowhere in it.

| # | Decision | Recommendation on record | Depth |
|---|---|---|---|
| 1 | **Ratify the census** — the 148-row classification (34 / 15 / 73 / 26) as the shape slice 2 executes | **RULED 2026-08-14b — RATIFIED** (owner: iteration expected at this scope; overhead direction approved) | §0.2 · [the ledger](2026-08-14-wi451-slice1-sr-census.md) |
| 2 | **The 26 tombstones** | **RULED 2026-08-14b — DELETE per D-4**; follow-through named in §0.2, executed by slice 2 | §0.2 call 1 |
| 3 | **The four package-wide B-05 properties** — SR-031 (policy readers agree) · SR-034 (stdlib + ledger) · SR-035 (stack-agnostic) · SR-114 (cross-OS): each is a property of EVERY delivered capability at once, so none fits a single one of B-05's five ruled buckets | **RULED 2026-08-14c — option A**: the decomposition axis gains the declared sixth bucket *package-wide property*; each stays ONE SR (the 13p invariant's own "crossing-or-**delivered-property**" wording admits it). Re-statement across the five groups passed over | §0.2 call 2 |
| 4 | **TC-159** — lift to `Planned` beside the rows it verifies, or re-point LLR-165's `test_refs` | **RULED 2026-08-14f — LIFTED, both halves**: the §2.3 lift had CROSSED the subject pairs (converter TC-159↔LLR-165, reader TC-160↔LLR-166); re-pointing would have forged a converter-requirement→reader-test edge. TC-159 and LLR-166 both `Draft`→`Planned`; drafts 29→27 | §2.2 |
| 5 | **The D-9 + D12 vocabulary program** — execute, sequence, or defer | **RULED 2026-08-14e — ONE SEQUENCE with the ratification wave**, right after slice 2's drafts land: the signing acts ARE the transition (first commit closes the enum; §3.3 gap recorded owner-visibly; rung-predicate work in the same sequence per §3.4). **STEPS 1–5b EXECUTED** (`2026-08-15g`, `2026-08-15m`): the enum closed at live truth, the `last_approved` snapshot mechanism built reader-first, then the rename narrowed it to `{Drafted, Approved, Modified}` with `Planned` folded out — **and the gate did not move**. What is left of this row IS the sitting: sign → seed → **step 7** (retire the transitional `Modified` — the enum lands at `{Drafted, Approved, Founded}`, drift = snapshot comparison — resolve `intake`'s `!= "Modified"` guard into a refusal, arm UNANCHORED as an ERROR) = review-package §5 steps 3–4 | §3 |
| 6 | **`Planned`'s fate** under the three-word ladder (16 live rows) | **RULED 2026-08-15 (OI-30 D1, log `2026-08-15k`) — FOLDED OUT into `Approved`, and EXECUTED at the rename (`2026-08-15m`)**: functionally the same rung, "approved" clearer; the fourth-rung option died with its `CMP_MATURITY` collision | §3.5 |
| 7 | **Authority over the off-spine approval elements**, and the dial's form | **RULED 2026-08-15 (OI-30 D3, log `2026-08-15k`) — the dial's form does NOT change**: authority follows the dev-stage ladder directly (`APPROVAL_RUNGS` + `human_approves` beside `DIAL_HOLDS`, unmapped = held), EXECUTED `2026-08-15m` | §3.6 |
| 8 | **Crossing ownership — restated in the locked frame's terms** (sitting-2 D6's own text still says "31 BIF rows"; that is the superseded v1 frame — the live question is over the SIX crossings): for each of B-01/02/04/05/06/07, which SRs and IFs realize it, and who owns closing each gap. The lists are mechanical but EMPTY today — SR-side `Boundary-Refs` sits at 0 of 149 and `trace.py`'s SN-037 advisory says verbatim *"the re-tier campaign is what moves this number"*; the IF tie-back re-key is the retirement lane's held remainder | **RULED 2026-08-14d — DEFERRED**, re-lands by name after slice 2 populates `Boundary-Refs` + the D-3 re-key (owner expects it may effectively dissolve in the full re-tier — recorded so it re-lands either way); B-06/B-07's missing SR already delegated to slice 2. **RE-LANDED AND CLOSED 2026-08-15 — this sitting no longer carries it.** It did NOT dissolve: the table was regenerated (B-05 = 50 of 65 refs, 77%; B-01/B-02/B-06/B-07 realized by no interface row), the B-05 half was ruled by the owner as `OI-29` option (b) — the concentration is real because the template package IS the product — and each unrealized crossing got a named owner (B-01 → SR-019/SR-020, B-06 → SR-151, B-07 → SR-152) or a recorded statement that none should realize it (B-02, conditional on SR-140 shipping). The IF-side re-key stays D-3's. Record: `WI-459`, log `2026-08-15f` | [sitting-2 Decision 6](2026-08-13-sitting-2-boundary-and-context.md#decision-6--the-15-missing-crossings--6-partial-ones-who-owns-them) |
| 9 | **The human-agent entity follow-on** — only the deliberate CONFIRMATION is open: 13k already ruled human-vs-loop *"survives as policy and record, never as an entity split"*, and the frame is LOCKED at five entities; decision 2's applied text asks the sitting to *say so deliberately* rather than let it stand by omission (reversing would mint a sixth entity and re-open the locked frame) | **RULED 2026-08-14d — CONFIRMED**: the human stays inside EXT-001, REL-002 carries the surfacing, the frame stays at FIVE entities | [sitting-2 Decision 2](2026-08-13-sitting-2-boundary-and-context.md#decision-2--adopt-or-amend-the-port-list-and-its-discriminator-self-contained) |

**Delegated unless you pull them up:** the census-surfaced authoring calls —
a dedicated SR for B-06/B-07, the SR-141/SR-148 overlap, the
migration-history strikes (sitting-2 §6 items 2/5/7 ride this window), and
SR-060's dead clause — ride slice 2 under the WI-444 token-verification bar;
the builder executes them row-by-row against decisions 1–3 above.

### 0.4 What the 2026-08-16 work adds to this desk

*(Added 2026-08-16. **Pointers only — nothing here is restated**, because every
item has a home that carries it in full and a second copy would be the next
thing to drift. Everything named below is **provisional and overturnable**; no
row is signed, no snapshot is seeded, and `docs/archive/last_approved/`
deliberately does not exist yet.)*

**Four things to have open beside the brief:**

| what | where | what it is |
|---|---|---|
| the **regenerated ratify brief** | [`../ratify/2026-08-13-wi444.md`](../ratify/2026-08-13-wi444.md) | the signing surface, regenerated through the day — `SR-148`'s section is in it as of `2026-08-16i`. **The ten ex-`Planned` rows still owe their deliberate read** (`2026-08-15m`): they sit on no surface at all until the seed exists |
| the **standards memo** | [`2026-08-16-tiering-research-memo.md`](2026-08-16-tiering-research-memo.md) | what published practice says about artifact names across requirement → acceptance → trace. **R2's absolute form is stricter than every body surveyed**; its §1/§3 leave one live question — whether the S3/S5 "current carrier" filenames move down to the trace tier or become registry-id anchors — which the memo recommends riding THIS sitting, because ruling it later re-touches every reworded row once more. Owner-approved `2026-08-16j` |
| the **alignment map**, including **§4** | [`2026-08-16-derivation-alignment.md`](2026-08-16-derivation-alignment.md) | the blind re-derivation's output (`2026-08-16j`) and its hat-aware extension (`2026-08-16k`): matched / orphaned-in-legacy / orphaned-in-fresh, the ranked top-10, and §4.4's revised ranking after the hat pass. **A validation instrument only — it moved no registry cell**; every orphan is a finding for you |
| the **v2 cursor** | [`2026-08-15-retier-v2-one-decision-tiering.md`](2026-08-15-retier-v2-one-decision-tiering.md) §0 | the six slices, each with its closing log id, reading **"DONE except the sitting"** |

**STATE AT THE DESK — measured `2026-08-16r`, RE-DERIVE AT CONVENING.** A
snapshot with its command attached, not an authority: this document's
§0.1/§0.2/§2.1 tables went stale in a day once and the banner at the top says
so. Re-run the command; if it disagrees, it wins.

| what | measured | note |
|---|---|---|
| spine | `SN=27 SR=63 LLR=155 TC=150` · `orphans=0 integrity=0` | the shape you are signing |
| pending signature | **147 `Modified` + 52 `Drafted`** (SR 40/19 · LLR 83/17 · TC 24/16) | every row awaits a **first** approval |
| derived bar | `DevBar-Reqs`, stage `DevStg-Boundary` (1 of 8) | unchanged across the whole program |
| baseline | **`docs/archive/last_approved/` does not exist** | the brief renders full text, not diffs — you read cold, and signing is what seeds it |
| **frame** | **4 entities · 4 crossings · 3 relationships** | `EXT-004`/`B-06`/`B-07` **CUT** `2026-08-16q`; ids SPENT |
| off-spine | 123 IF · 4 CMP · 11 frame rows · 22 OI | IF rows are **all `drafted`** — that approval path has never been exercised |
| gating reds | `traceability`, `trajectory` | see below — **only one clears by signing** |
<!-- fig: cmd="python project-trajectory/scripts/trace.py --root . && cat docs/gate" rev=e2ec44c1 -->

**The two gating reds, and which one signing fixes:**

- **`traceability`** — mostly `--require-verified` firing on the 147 `Modified`
  rows, which **is** the open window and clears when you sign. But `trace.py
  --strict` alone still exits 1 on **`SR-140`/`SR-147`**'s multi-`shall`
  findings: both carry the 13v waiver, and `form_findings` **deliberately does
  not suppress on it**, so the waiver is recorded and the finding still gates.
  Signing does **not** green this step — splitting those two rows does, which
  is item 13.
- **`trajectory`** — a real ERROR unrelated to the sitting:
  `scripts/hats → scripts/spine_carrier`, a cross-component import with no
  declared IF seam, from the 2026-08-16 hats work. Not yours to rule; one
  interface row or a membership retag clears it.

**WHAT MOVED SINCE THIS DESK WAS WRITTEN** — the 2026-08-16/17 session, so a
reader does not have to reconstruct it from the log:

| ruling | what changed | log |
|---|---|---|
| `SR-053` **RETAINED**, `hat.CONSISTENCY` ruled `always` | the "retire unless mechanically testable" condition was found ALREADY MET (8 LLRs → 8 TCs, 11 automated tests, green); both rosters flip identically | `2026-08-16p` |
| retired-rubric acceptance **CORRECTED** on `SR-052`/`053`/`054` | acceptance restated as the decomposed chain, no artifact named; the three `Rationale` cells reworded off the retired method | `2026-08-16p` |
| the **verification-coherence lint** shipped | `trace_text.verification_coherence_advisories`, warn-only — a row whose prose claims an instrument its `Verification` contradicts. Two narrowings measured, not assumed | `2026-08-16p` |
| the advisory critique **NOT re-armed** | an LLM critic on an any-change trigger would fire on nearly every spine change; `SR-054`'s residue recorded as a stated Prose gap | `2026-08-16p` |
| **L1 pair ruled on DESIGN CONTROL** | `SR-151` **and** `SR-152` → `["B-05"]`; a hosted runner is an ADOPTER's boundary | `2026-08-16q` |
| **frame CUT** | `EXT-004`, `B-06`, `B-07` deleted; the locked-frame test went red and was updated with the ruling | `2026-08-16q` |
| two kit skills carried **retired vocabulary** | `gate-advance`/`registry-hygiene` taught `Status=Verified` and `Modified → Planned`, both retired at D-9; fixed. `check_vocab` guards only the retired `G*` tags | `2026-08-16p` |
| item 3 **RULED AND APPLIED** | 19 `Consumes` `owner` cells re-pointed SR→LLR; `WI-469` filed for the 27 file-endpoint rows; the three `external:` rows stand | `2026-08-17c` |
| the four Sol-mint SRs **DECOMPOSED** | `SR-171`/`172` gain `LLR-174`/`175` + `TC-168`/`169`; `SR-173` gains `TC-170`; `SR-174` measured already-carried — see the re-written signing note below the Sol table | `2026-08-17d` |
| three flagged defects **FIXED** | `LLR-153`'s mint detail states the watermark floor; `TC-135` tier `Full`→`Smoke`; `trace_text` `;`-split asymmetry fixed (advisories 114→113, `IF-088` cleared — `IF-128`'s survivor is a REAL owner-vs-endpoint disagreement, now item 18) | `2026-08-17e` |
| **adversarial round 2 ran** (Sol + Terra via codex, hostile brief, author re-verified) | 6 CONFIRMED · 2 in-part · 1 refuted over `47234903^..HEAD`; nothing applied — the surviving calls are **item 18** | `2026-08-17f` |
| item 8 **RULED AND APPLIED** | all four WI-468 recommendations adopted: `SR-175`/`176`/`177` minted as labelled derived rows under SN-026/009/027 (+ `LLR-176`/`177`, `TC-171`/`172`); `SN-008`'s hue metonym + `SN-027`'s `why` amended on the open window; C-ACC-2 matched-to-`SR-052`, remainder filed `WI-470` — contrast at the option doc §6 | `2026-08-17h` |

**WORK OWED BEFORE THE BRIEF REGENERATES — two items, pointers only**
*(reconciled `2026-08-17l`; re-reduced `2026-08-17r` — the draft-TC pins are
EXECUTED; each survivor is stated in full elsewhere on this desk).*
Clearing these first means the brief the sitting reads is the text it signs,
with no re-touch after: **(1) the `SR-140` split** — the one row still holding
the `traceability` step red (the gating-reds note above; signing does not
green it, splitting does); **(2) the `SR-173` wording decision** — item 18's
residue: reword the shall toward its acceptance, or attest the stronger
reading deliberately. *(The former item (2), the three draft-TC pins on
`TC-168`/`169`/`170`, was executed `2026-08-17r` — five new mutation-proved
tests, evidence cells updated, rows still `Drafted` for the sitting.)*

**STILL OPEN — the calls this sitting actually makes.** Each carries its
**impact** and a **recommendation** inline, so a call can be made from this
page; the linked homes hold the full evidence for the ones you want to go
deeper on. A recommendation is a starting position, never a ruling taken in
advance.

> **SCOREBOARD — re-stamped `2026-08-17s`, the current truth of this list.**
> OPEN: **item 6** (two sub-calls: run the SN migration before signing?
> and the off-spine vocabulary half) — the last open call. Plus the two
> **work items in the block above** (`SR-140` split · `SR-173` wording).
> Everything else is struck, ruled, or countersign-only: items 1 · 1a · 3 ·
> 7 · 8 · 15 · 16 · 17 · 19 · 20 and the Sol rows 9–14; item 18's owner-cell
> half executed on investigation `2026-08-17p`, its pins half executed
> `2026-08-17r` (five mutation-proved tests on `TC-168`/`169`/`170`); item
> 19 ruled and executed `2026-08-17s` (the behavioral fit-criterion form —
> 50 acceptance cells re-worded, `SR-150` flagged as the one Approved
> holdout, ledger at
> [`2026-08-17-acceptance-form-ledger.md`](2026-08-17-acceptance-form-ledger.md)).
> **On the numbering:** item numbers are STABLE IDS — log entries cite
> them — so closed items keep their numbers and are struck, never removed
> or renumbered. Gaps (no 2, 4, 5) are items closed and removed in desk
> revisions that predate this list's freeze; rows 9–14 live in the Sol
> table above rather than in this list. Do not count visible entries;
> read the ids.

1. ~~**The L1 pair**~~ — **RULED AND APPLIED IN FULL `2026-08-16p`.** Both
   rows now read `boundary_refs = ["B-05"]`.

   The owner ruled on **design control**, which is a better criterion than the
   package-alone acceptance shape this entry previously argued from — the
   acceptance shape was evidence, design control is the reason. In the owner's
   words: *"the kit is providing a method for the CI runner to activate, but
   this template has no design control over an external CI respecting
   configurations… all it can do is provide a method within the pack for CI to
   run."* `SR-151` first, then `SR-152` on the same argument (option (a),
   symmetric rather than the `["B-05","B-04"]` variant that was on offer).

   **This is a consistency fix, not new doctrine** — the frame already reasons
   this way twice:
   - `REL-002` — the generators ship as **B-05 content** while the workflow
     running them is *adopted*; those outputs are "NOT system outputs (13u)".
   - `REL-003` — the model-provider surface lands its obligation on *"delivered
     loop content (B-05), exercised session-side"* and mints **no crossing**
     for `EXT-005`. An uncontrollable external was already handled by keeping
     the obligation on the package.

   **Recorded consequence, so it is never read as an oversight:** the hosted
   re-run — the second half of the honest-limit pair `SR-019` states from the
   local side — now has **no crossing of its own** in this frame. Both rows'
   rationales say so in their own words rather than leaving the frame to imply
   it.

1a. ~~**Can `B-06`/`B-07` simply be cut?**~~ — **RULED AND EXECUTED
   `2026-08-16q`.** Owner: *"Agreed cut B-06/B-07/EXT-004."* Done: the two
   crossings and the `EXT-004` (Hosted CI) entity are deleted from
   `external.toml`, on the design-control reading item 1 established — a hosted
   runner is an **adopter's** boundary, this system holds no authority over
   whether an external runner honours the workflow it is handed, and what it
   delivers is a METHOD for one to invoke. The frame already applied that
   reasoning to the model provider at `REL-003`; `EXT-004` was the
   inconsistency.

   **The frame answered:** the finding item 1 created —
   *"boundary crossing(s) named by NO requirement: B-06, B-07"* — is **gone**,
   and *"realized by NO interface row"* drops from **four crossings to two**
   (`B-01`, `B-02`). The frame is now **4 entities · 4 crossings · 3
   relationships**, `orphans=0 integrity=0` unchanged.

   **Preserved, per the recommendation:** the statement the cut would otherwise
   have destroyed now lives in **`B-04`'s own `notes`** — the honest-limit pair
   (a local hook floor is bypassable, so the guarantee rests on the verdict at
   the moment of the act *plus* a re-run away from that bypass), followed by
   why the re-run is **not a crossing of this system**. Stated as a ruling
   rather than left as an absence, which is the whole point.

   **Ids are SPENT — never re-mint `B-06`, `B-07` or `EXT-004`** (the D-1/D-4
   doctrine: a registry states what IS, git is the history, and this entry plus
   log `2026-08-16q` are the forwarding pointer). **FINDING, not fixed:**
   `B`/`EXT` are **not watermark spaces** — `WATERMARK_SPACES` covers
   `ASSET CMP DP IF LLR MOD OI PART PB REPO SN SR TC WI` and nothing else — so
   unlike an SR or an IF, nothing mechanically stops a future session
   re-minting a cut crossing id at a different thing. That is the exact
   vacuous-space class the `IF-121/122` mint hit. See item 17.

3. ~~**The `Consumes` owner-side reading**~~ — **RULED AND APPLIED
   `2026-08-17c`.** The recommendation adopted verbatim: **`owner` points at
   the DESIGN tier wherever a design row exists for the owner-side
   endpoint**, and the mechanism stands as re-measured — `owner` = LLR makes
   the endpoint derivable (`owner` → LLR → `module`); `owner` = SR means the
   IF cell is the single home for it and stays.

   **Applied:** the population, re-derived independently at the ruling
   session, reproduced the desk split exactly — 49 SR-owned `Consumes` rows
   → **19 converted / 27 file-endpoint / 3 `external:`**. The 19 `owner`
   cells re-pointed to the design tier: `IF-039`, `IF-040`, `IF-043`,
   `IF-055`, `IF-056`, `IF-071`, `IF-075`, `IF-082`, `IF-083`, `IF-084`,
   `IF-085`, `IF-088`, `IF-089`, `IF-093`, `IF-101`, `IF-116`, `IF-117`,
   `IF-127`, `IF-130` — the per-row picks, the one-owner call on the WI-280
   sibling seam, and the three candidate-LLR-gap judgment calls are recorded
   in `2026-08-17c`. No status flipped, no contract text moved. The three
   `external:` rows (`IF-032` git, `IF-036` upstream docs, `IF-041` agent
   CLI) stand untouched.

   **The READING stands; four of the 19 picks are CONTESTED.** Adversarial
   round 2 (`2026-08-17f`) confirmed that on `IF-043`, `IF-117`, `IF-127` and
   `IF-130` the mechanical module-match diverges from the row's own recorded
   answerability judgement — the same class as `IF-128`, the one advisory
   survivor. Those five owner cells are **item 18**; the other 15 re-points
   were not contested (Sol's all-19-are-name-matches framing was refuted with
   row evidence).

   **The 27 mis-authored rows are FILED, not edited:**
   [`WI-469`](../work/queued/WI-469-consumes-names-the-medium.md)
   (queued) carries the full 27-row population, the owner's correction
   (*"the file itself is the actual interface"* — they name the MEDIUM where
   they should name whom the medium serves), and the two sub-shapes, kept
   here because they are the executing session's fork:

   | shape | fix |
   |---|---|
   | low fan-out — e.g. `coverage.json` read by check/check_coverage only; `docs/declared-absences` by five checkers | name the actual consumer; the endpoint becomes derivable |
   | published contract, high fan-out — `docs/stack.ini` (17 readers), `docs/architecture.md` (12) | the file IS the interface: name the consumer class, tie back to `B-05` per the `IF-013`…`IF-018`/`IF-048` pattern |

   WHICH consumer each of the 27 names is per-row judgement, deliberately
   NOT done at the ruling (the mechanical attribution attempt stem-matched
   and was discarded as unsound). **CONSEQUENCE FOR `wi455` (unchanged):**
   `counterpart` cannot be dropped as a COLUMN until `WI-469` re-authors —
   re-author first, then drop what has become derivable.

6. **The SN tier's status vocabulary** — RE-FRAMED `2026-08-16p`, and the
   earlier framing ("no `Status` cell") understated it. The tier encodes
   status across **three** fields: `kind` = `core`\|`draft` (the ratified and
   drafted halves, mixed into the same field as the `edge` ROW-TYPE value),
   plus `attestation = "pending"` and `amended = "<date>"` added at Sol's F2.
   Two defects, both owner-named: the pair invents semantics the agreed
   vocabulary already had a word for, and `amended` puts **history in a
   registry whose job is living truth** — the class `provenance_findings`
   already forbids in prose but cannot see in a field, and which git and
   `docs/archive/` hold better. **Owner direction (`2026-08-16p`): SN gains
   `status` on the closed spine vocabulary; `attestation`, `amended` AND
   `kind` all die.** Scope + blast radius:
   [`2026-08-16-registry-status-unification.md`](2026-08-16-registry-status-unification.md)
   — whose §5 gained step 7 by owner ruling `2026-08-17k`: the execution also
   closes the SN schema census (`spine_carrier.SPINE_TIER_KEYS` gains
   `"SN-ID"`, wiring SN into the dogfood drift check it alone sits outside).

   **WHAT IS ACTUALLY OPEN HERE — restated `2026-08-17q` after the owner
   could not tell from this item's text (the direction above is RULED;
   these two sub-calls are not):**
   - **(a) TIMING — run the SN migration BEFORE signing?** No snapshot
     exists, so today it costs **zero re-attestation**; after signing, the
     same edit re-opens every touched SN row. Everything to execute is
     already specified (the unification plan §5 steps 1–7, census
     included). **Recommendation: yes, run it before the sitting.**
   - **(b) THE OFF-SPINE HALF — genuinely undecided.** The survey found
     the split is NOT SN-only (that doc §0): four field names across the
     registries (`status`, `kind`+`attestation`, `approval`, `state`), and
     `components.state`'s shipped vocabulary re-uses `planned` and
     `verified` — two words D-9 retired from the spine — for unrelated
     meanings, where `check_vocab.py` cannot see them. Unify (and to what
     vocabulary), or leave — a separable step, deferrable past the
     sitting.
7. ~~**The two remaining provisional hat charters**~~ — **RULED `2026-08-17`.**
   Owner: *"keep both, as long as they can be opted out of downstream users I
   tend to think default always is fine. Easy to change later."*
   `INTEGRITY-RECOVERABILITY` (R-5) and `PRODUCT-FITNESS` (R-6) are ruled
   `always` in **both** rosters and the provisional block is closed — the
   roster is now **sixteen hats, all ratified owner text, 10 `always` / 6
   conditional**. Ruled on their own findings, not on R-4's precedent.

   **THE CONDITION WAS VERIFIED, not assumed.** `hats.toml` is seeded from the
   shipped template ONCE (`bootstrap.copy_if_new` is write-once) and then
   **preserved** — `RESYNC_PACK`'s "Preserve always" class covers every
   registry — so an adopter's edits survive a kit upgrade. Downstream opt-out
   today is *narrow the `applies_when` predicate* or *delete the block*; both
   persist. That statement now lives in both rosters so a downstream reader
   finds it without this document.
   **Measured:** ruling them IN moved no count and no test pin (both were
   already `always` as drafts); no SR rationale changed either, because **zero
   SR rows cite either charter** — they were drafted as ROSTER findings (the
   lens was missing), not to justify an existing row. They are preventive, and
   the first decomposition they touch will be a future one.
   **Residual, not fixed:** the opt-out is real but blunt — deleting a block
   destroys the charter text and the reason it was cut. A `never` token in the
   `applies_when` grammar would give "off, but keep the text"; see the config
   discussion at `2026-08-16p`. Unfiled and unruled.

8. ~~**The four hat-exposed obligation candidates**~~ — **RULED AND APPLIED
   `2026-08-17h`** (the closing block below) — provider egress of commit
   authorship, the privacy finding-record's retention bound, SN-027's
   undeclared throughput budget, and the colour-only signal. Filed as an intake
   row that **mints nothing**; the disposition of each — new need, amendment,
   labelled derived requirement, or refused — is yours (alignment map §4.3,
   `2026-08-16l`). Carried by `WI-468` (`queued`, `safety_class = "spine"`),
   whose Title states all four candidates in full with their charter clause
   ids, so the WI row is the one place to read them.
   **Impact:** up to 4 new SN rows or 4 amendments, each of which then owes an
   SR decomposition — the largest potential ADDITION to the spine on this desk.
   Two are data-protection (C-DPR-3 commit-authorship egress to an external
   model runner, already drawn at `REL-003`; C-DPR-2 the privacy finding
   record's own retention), one is SN-027's undeclared throughput measure
   (unfalsifiable as written), one is SN-008's colour-only "believe a green".
   **Recommendation:** rule the two DATA-PROTECTION ones this sitting and defer
   the others if time is short — those two describe personal data crossing a
   boundary the frame already draws, which is the class where "no need states
   it" is a real exposure rather than a tidiness finding. C-ACC-2 is the
   cheapest (a wording amendment to SN-008, no new row); C-PRF-1 is the one
   that most needs your judgement, since declaring a throughput measure
   commits the repo to measuring it.
   **The intake proposals now EXIST** (`WI-468` closed complete
   `2026-08-17g`): one section per
   candidate, grounding measured in the code, all four options costed, the
   refusal case stated honestly, in
   [`2026-08-17-wi468-obligation-intake-options.md`](2026-08-17-wi468-obligation-intake-options.md).
   Its recommendations in one line: **C-DPR-3** a hat-derived SR under SN-026
   (the brief-assembly discipline is real but undeclared; the runner's pull
   channel is consent-shaped, and no outbound redaction exists anywhere);
   **C-DPR-2** a hat-derived SR under SN-009 narrowed to
   value-never-persists (the durable finding copy is the committed session
   transcript, which redacts credentials but not PII); **C-PRF-1** a modest
   derived SR under SN-027 reporting fan-out utilisation, no numeric target
   (nothing measures today — and the repo in fact runs `lanes=1`, with no
   instrument that would say so); **C-ACC-2** no new row — the SN-008
   wording amendment plus record-as-matched to `SR-052`, whose `Approved`
   text already states no-colour-alone with the mechanized A3 chain behind
   it (the §4.3 "carried by neither" premise is measurably overstated for
   this one candidate).

   **RULED AND APPLIED `2026-08-17h` — all four recommendations adopted as
   proposed.** Owner: *"You can break down the spine as you recommend… I
   want to see how it contrasts with what is available."* Applied: `SR-175`
   (under `SN-026`), `SR-176` (under `SN-009`, narrowed to
   value-never-persists) and `SR-177` (under `SN-027`,
   Drafted-**undecomposed**, no numeric target) minted as labelled derived
   rows, each `Rationale` naming its deriving charter(s) per the 2026-08-16l
   form; `LLR-176`/`TC-171` and `LLR-177`/`TC-172` pin what exists (plus a
   new standing authorship-egress sweep,
   `tests/test_brief_egress_conventions.py`); `SN-008`'s hue metonym and
   `SN-027`'s `why` amended as deliberate rides on the open window (both rows
   `attestation = "pending"`); C-ACC-2 recorded **matched-to-`SR-052`** at
   the alignment map (§4.3) and the remainder filed as `WI-470`. **The
   contrast the owner asked for is the option doc's §6** — each new row
   against what already existed, row-cited. What this sitting still owes
   here: the countersign — the three Drafted rows ride the LLR/TC
   draft-ratification sweep, and the two amended needs join the re-attest
   window.

**THE SIX SOL ROW-CALLS — FIVE APPLIED `2026-08-17b`, F11 DECLINED.** Owner:
*"apply all of SOL's queued recommendations except for F11, adapting any as
you need."* Verdicts and Sol's original wordings remain in
[`../reviews/retier-v2/ROUND-SOL.md`](../reviews/retier-v2/ROUND-SOL.md).

| # | id | disposition |
|---|---|---|
| 9 | **F11** | **DECLINED** — `SR-040` split not taken. Its support had already evaporated (the tripwire clause gained two lenses at option (b); fan-out 1 of a bound of 7; one `shall`), so no orphan and no detector stood behind it |
| 10 | **F12** | **APPLIED, adapted** — `SR-026`'s acceptance carried backoff and stall-abort, which its shall never stated. Sol offered *delete or mint*; **minted**, because both describe live behaviour: **`SR-171`** (bounded retry on a declared transient limit) and **`SR-172`** (a stalled session ends at its declared limit), split in two because they fail for opposite reasons |
| 11 | **F14** | **APPLIED** — `SR-046` was a menu specification (numbered menu, direct launch, machine listing, empty-declaration text, exit passthrough, declaration grammar). Now one capability-level decision: every declared capability reachable, the same way, from one declaration, by three kinds of caller |
| 12 | **F15** | **APPLIED** — `SR-129` shed the spec-folder layout, the retired CSV and the drained-stop mechanics from its shall; they sit at `LLR-136` and in acceptance |
| 13 | **F16** | **APPLIED — and it cleared a gating finding.** `SR-147`'s shall carried the migration history and a second obligation; re-voiced to one. **`trace.py`'s `form-findings` drops 2 → 1**, so `SR-140` is now the only row holding the `traceability` step red. The recorded 13v waiver is SPENT and says so |
| 14 | **F18** | **APPLIED** — `SR-170` split three ways. It keeps the EXCLUSIVE-WRITER contract; **`SR-173`** takes ordered-and-no-partial-result, **`SR-174`** takes identity allocation. `LLR-142` → `SR-173`; `LLR-153`/`154` → `SR-174`; `TC-135` → `SR-173`; `TC-147`/`148`/`158` → `SR-174`; `IF-090`/`091`/`101` re-pointed and `IF-101`'s owner with them. The jargon (*shared authority surface*, *mint*, *composed tree*, *serial integration seam*) is gone |

**Spine after:** `SN=27 SR=67 LLR=155 TC=150`, `orphans=0 integrity=0`,
`drafted` 52 → **56** (the four mints land `Drafted`, so they are exempt from
the decomposition rules and the gate is unmoved at `DevBar-Reqs`). Id
watermark bumped `SR 170 → 174`.

**Two things to know before signing these** *(re-measured and re-written
`2026-08-17d` — this note used to say all four owned no LLR or TC, which was
never true of the F18 pair: the F18 row above lists the children re-pointed to
them at the same sitting)*: the four are **`Drafted` and now DECOMPOSED** —
`SR-171` carries `LLR-174` + `TC-168` and `SR-172` carries `LLR-175` +
`TC-169` (minted `2026-08-17d` against the live `agent_loop.py` behaviour,
evidence the existing loop suite plus one new stall-window test); `SR-173`
keeps `LLR-142` + `TC-135` and gains `TC-170` (two new regen tests: executed
dependency order, regen-never-commits); `SR-174` was already fully carried by
`LLR-153`/`154` + `TC-147`/`148`/`158`, so nothing was minted there. The
`TC-135`/`147`/`148` `expected` cells, still reading "Satisfies SR-170" after
the re-point, were corrected in the same act. And `SR-174` states the
non-reuse clause that used to live only in `SR-170`'s acceptance, which was
the same acceptance-mints-a-requirement defect Sol raised at F12. *(Round 2
then audited this decomposition and confirmed pin debt on the new draft TCs —
item 18's RECOMMENDED half — without contesting the decomposition itself.)*

**TWO VOCABULARY CALLS RAISED `2026-08-16p`** — both spine-wide, neither
SN-specific, and both cheap now and expensive after signing. **Both closed
`2026-08-17m` — see the items.**

15. ~~**Does a chain change flip its attestation unit?**~~ — **RULED
    `2026-08-17m` — THE CELL READING.** Owner verbatim: *"No a child flipping
    does not impact the parent, please update both this item, process.md, and
    any other documentation."* A row's attestation covers its OWN cells: a
    `Status` flips only when the row's own text changes, and a child (LLR/TC)
    amendment never flips the parent SR — child changes surface through the
    snapshot-drift arm and the gate, never by invalidating the parent's
    signature. APPLIED same-day: `docs/process.md` §4 rewritten;
    `modified_chain_advisories` (the warn-tier enforcer this item named)
    RETIRED with its tests and ratchet entries; the staged amend-without-flip
    guard's owning-SR exemption removed (the amended row itself must flip);
    the skills, the machinery reference and the SR-keyed surfaces reworded —
    grouping by SR is presentation, never attestation scope. The `SR-144`
    history reads consistently under the ruling: it flipped at `2026-08-16l`
    on its own rationale change, not on its children (item 20). The
    chain-completeness claim moves to the `Founded` state per item 16's
    correction — the two rulings are one design: attest cells, derive
    chain-completeness.
16. ~~**The third status word.**~~ — **CLOSED `2026-08-17m` — NEVER OPEN: a
    relitigation artifact.** Owner verbatim: *"the plan was always the three
    units: drafted, approved, and founded — modified means nothing because it
    is caught by comparing to the snapshot. I don't understand why things are
    being relitigated."* The record proves it: the LIVE
    [d9-migration-plan](2026-08-15-d9-migration-plan.md) step 7 states
    verbatim *"Retire the transitional word: delete `is_modified`; enum →
    `{Drafted, Approved, Founded}`"*, and its C4 note records that all four
    `Founded` discharge tests already exist — `Founded` was the standing
    target all along, never a floated fourth word. The corruption mechanism:
    later re-stamp banners paraphrased step 7 as *"narrow the enum to two"*
    (silently dropping `Founded`), and this document's §3 pointer aimed at the
    ARCHIVED 2026-08-11 checklist (header: "nothing is executed") instead of
    the live plan — this item then recast `Founded` as a new proposal and
    invoked OI-30 D1 against it. OI-30 D1 folded `Planned` out and never
    touched `Founded`; that ruling is UNTOUCHED by this closure. `Modified` is
    TRANSITIONAL and retires at step 7; post-seed, drift is caught by
    comparison against `docs/archive/last_approved/`.

17. ~~**Should `B` and `EXT` become watermark spaces?**~~ — **RULED
    `2026-08-17n` — YES, AND `REL` WITH THEM.** Owner: *"Yes add them."*
    Raised by the `2026-08-16q` cut, which spent three ids the watermark did
    not protect: `WATERMARK_SPACES` was derived from `ID_PATTERNS` plus
    `SN`/`WI`/`OI`/`DP`, the frame tiers were never added, so deleting a
    crossing freed its number in the live tree. APPLIED same-day: the three
    frame spaces joined `WATERMARK_SPACES`, `external.toml` joined the
    live-id sweep, and the marks stand at the highs EVER allocated —
    `B = 7` (seeded above the live max of 5, because `B-06`/`B-07` were cut
    before the space was guarded; a new space's first mark is a seed, and
    `trace.py` now accepts one above `max(live)` exactly once), `EXT = 5`,
    `REL = 3` (both equal to their live maxima, verified against the
    registry's full git history). `REL` was included on this item's own
    reasoning — the frame tiers were the only id spaces exempt, and `REL`
    is the same locked-frame class with the same delete-by-ruling exposure;
    nothing distinguishes it. The pin in `tests/test_id_watermark.py`
    extends to all three; the shipped `id-watermark.template` gains the
    rows; the adopter-facing consequence (a resync goes red until one
    `--bump-ids`) is a `RESYNC_PACK.md` §3 entry.

18. **The adversarial round-2 desk** — what survived author re-verification of
    the Sol + Terra round over the three `2026-08-17` spine commits
    (`2026-08-17f`; full findings, evidence and verdicts in
    [`../reviews/retier-v2/ROUND-2-SOL-TERRA.md`](../reviews/retier-v2/ROUND-2-SOL-TERRA.md)).
    Nothing is applied; every disposition here is yours.

    **Five contested `owner` cells — the OWNER-CALL half — EXECUTED ON
    INVESTIGATION `2026-08-17p` (owner directive: verify each seam's
    information against the code at BOTH endpoints, then correct; the
    never-both-standing discipline applied to every row). Countersign-only
    now; per-row evidence in the log entry:**
    - `IF-127` — **REVERTED `LLR-001` → `SR-140`**: adjudicate_brief lazily
      imports trace and calls `load_registries` + `reattest_model` exactly as
      contracted; no trace design row names either symbol (`LLR-001`'s
      code_symbol is `main`), so the recorded `2026-08-15h` exception stands
      and the note records the re-affirmation.
    - `IF-130` — **RESOLVED `LLR-050` → `SR-049`**: `bar_label` is a
      module-scope derive_gate function `_stage_line` genuinely calls, still
      named by none of derive_gate's four LLRs; the note's false "req_refs
      carries SR-070" claim corrected (the live cell carries `SR-168`).
    - `IF-043` — **KEPT `LLR-017`, the split RECORDED in notes**: the code
      shows ONE engine — `check_privacy.Scanner` (LLR-017's own code_symbol)
      compiles BOTH leak classes and produces the one `--range` verdict both
      branches of the hook read; `LLR-018` answers for the identity/PII class
      content behind "gated identity".
    - `IF-117` — **REVERTED `LLR-023` → `SR-147`** (the req_refs SR): no
      gen_arch_map design row names `module_bindings`, and `LLR-023`'s
      artifact is exactly what the contract disclaims. RESIDUE FLAGGED for
      this sitting: no SR states the CodeSymbol-anchor obligation itself
      (SR-147 states the carrier; SR-158's acceptance names only the verdict
      shape) — a candidate-gap the owner has not ruled.
    - `IF-128` — **RE-POINTED `LLR-173` → `LLR-166`** (the counterpart's one
      design row, which DEFINES both refusals the contract names — IF-129's
      the-definer-answers rule); the standing owner-vs-endpoint advisory
      cleared (113 → 112), and the contract dropped `OFFSPINE_TABLE` from its
      consumed-symbol list (comment-only in baseline_snapshot — a false
      consumption claim; the other seven symbols verified in code).
    **Impact:** five cells, all `drafted`/unattested — the corrections cost
    no re-attestation; the ratify brief renders the corrected rows, and the
    sitting countersigns or overturns them like any other provisional act.

    **The RECOMMENDED half — EXECUTED `2026-08-17r` (owner directive
    2026-08-17): five new tests, every one mutation-proved, evidence cells
    updated, rows still `Drafted` for the sitting.** `TC-168`: the `min` cap
    is now load-bearing (a fallback-above-ceiling case; deleting the cap
    fails it while the old evidence stayed green under the same mutation,
    confirming F5), the parsed-reset retry branch and the 3600 default are
    pinned via a `time.sleep`-recording driver (the wall-clock waits are
    observed, never served); `TC-169`: the default of 3 pinned — no flag
    passed, the third no-commit session exits `EXIT_STALL`, the second does
    not; `TC-170`: the failure-path sentence is now an executed check — a
    later step's failure after green steps leaves HEAD unmoved and the green
    output uncommitted. No claim-vs-code divergence surfaced: the code does
    exactly what the rows state.

    **Two CONFIRMED-IN-PART residues, recorded not urgent:** `LLR-153`'s new
    refusal wording slightly overstates (`next_wi_id` uses `.get("WI", 0)`,
    so a watermark file missing its WI line mints from the sweep — mitigated
    by the always-on integrity floor); and `SR-173`'s shall ("no partial set
    behind") reads stronger than its acceptance ("not left committed") — a
    tension that PRE-DATES this stack (minted at `4cf98e4f`) and rides the
    signing window like any other row-text question.

19. ~~**The acceptance-cell / current-carrier question**~~ — **RULED AND
    EXECUTED `2026-08-17s`, with a THIRD form superseding both options
    below.** The owner, verbatim: *"can you formulate the acceptance
    criteria in terms of the exact boundaries, pass/fail conditions, and
    edge cases for when the work is finished with respect to the behavior
    the system requirement asks for?"* — and, recalling `SR-052/053/054`:
    acceptance-as-chain-closure is not the wanted form either. So: an SR
    acceptance cell states the **behavioral fit criterion**, naming neither
    concrete artifacts nor the row's own decomposition chain; artifact
    bindings live at the design/trace tier (LLR `module`/`detail`, TC
    `evidence`); chain-completeness is the `Founded` state's claim
    (`2026-08-17m`). Executed under the WI-444 token-verification bar: the
    population re-derived at **40 of 70** (the +1 over the table below is
    `SR-112`), 50 cells re-worded, every stripped token's trace-tier home
    verified first and 8 LLR details + 2 rationale lines re-homed in the
    same commit; `SR-150` (`Approved`, outside the window) is the one
    flagged holdout for the sitting's own re-attestation act. Per-row
    ledger:
    [`2026-08-17-acceptance-form-ledger.md`](2026-08-17-acceptance-form-ledger.md);
    log `2026-08-17s`.

    *(The question as it stood, kept for the record — the two options both
    superseded by the ruling above.)* The standards
    memo ([`2026-08-16-tiering-research-memo.md`](2026-08-16-tiering-research-memo.md)
    §1/§3, owner-approved `2026-08-16j`) leaves ONE live question from the
    R2 rewording: requirement cells no longer name concrete artifacts, but
    acceptance cells still name **"current carrier" filenames** — the
    `2026-08-16h` read counted eight redundant current-carrier clauses. Do
    those filenames move DOWN to the trace tier (LLR/TC name the artifact,
    acceptance states the fit criterion), or become **registry-id anchors**
    in place?
    **Impact:** every reworded row's acceptance cell. This is the "cheap
    now, expensive after" shape at its purest: ruling it after signing
    re-touches — and re-attests — every one of those rows a third time.
    **Recommendation (the memo's, on record):** ride THIS sitting.

    **The population, measured at the desk (`2026-08-17o`; superseded by
    the executed ledger above — filename/path tokens in SR
    `acceptance_criteria` cells):** **39 of 70 SRs** name a concrete
    artifact; **34 cells** use the literal "current carrier" idiom. The
    rows the ruling re-touches, with what each names:

    | SRs | artifacts named in acceptance |
    |---|---|
    | SR-006/007 | `check.py`; + `docs/stack.ini` |
    | SR-009/010/011 | `bootstrap.py` |
    | SR-022 · SR-024 · SR-033 | `check_vendored.py` · `gen_cases.py` · `gen_release_checklist.py` |
    | SR-026/027/028 | `agent_loop.py` |
    | SR-034 · SR-035 | `docs/dependencies.md` · `trace.py` |
    | SR-036 · SR-111 | `ADOPTING.md`, `docs/kit-version`; + `bootstrap.py` |
    | SR-040 · SR-043 | `docs/process.toml`, `status.md`; + `docs/subagent-gate` |
    | SR-046 | `docs/stack.ini`, `scripts/run_menu.py` |
    | SR-049 | `derive_gate.py`, `docs/gate` |
    | SR-070 | `gen_arch_map.py`, `gen_okf.py`, `gen_trajectory.py` |
    | SR-129 | `docs/work/` (+ the retired `work-items.csv` as history) |
    | SR-137/138 | `docs/process.toml`; + `bootstrap.py` |
    | SR-147 · SR-149 · SR-150 | `migrate_carrier.py` · `check_vocab.py` · `check_need_form.py` |
    | SR-151 | `docs/stack.ini`, `tests/test_ci_tier_declaration.py` |
    | SR-154 | `docs/agents-enabled`, `docs/agents.toml` |
    | SR-156 | `agent_common.py`, `integrate.py`, `lane.py` |
    | SR-157 | `trace.py`, `trace_text.py`, `check_trajectory.py`, `docs/process.toml` |
    | SR-158 | `check.py` + four checker modules, `docs/declared-absences`, `docs/orphans-allow`, `docs/stack.ini` |
    | SR-159 | `check_trajectory.py`, `gen_arch_map.py`, `trace.py`, `docs/architecture.md`, `docs/process.toml` |
    | SR-166 | `tests/test_bootstrap.py`, `tests/test_dogfood_sync.py` |
    | SR-167 | `check_perf.py`, `docs/test/perf-baseline.json`/`perf-metrics.json`, `tests/test_check_perf.py` |
    | SR-168/169 | `PROJECT_STATE.html`, `gen_trajectory.py` |
    | SR-170 · SR-173 | `trunk_step.py`; + `check.py` |
    | SR-174 | `intake.py`, `integrate.py` |

20. ~~**The `SR-144` flip**~~ — **CLOSED BY SUPERSESSION; nothing to rule.**
    Recorded so it stops circulating: the `2026-08-16h` flag was that
    `SR-144` sat `Approved` while the M4 correction had flipped its child
    `LLR-144` + `TC-138` `Modified` — flipping the owning SR is an
    attestation act the plan holds for the human, but while it stayed
    `Approved` the correction was invisible to the brief and gate. The
    question died the next day, mechanically: `2026-08-16l`'s hat-derived
    labels touched `SR-144`'s rationale and flipped it
    `Approved` → `Modified` as a named, rationale-only amend consequence
    (one of four: SR-144/146/147/149). Verified at this desk: all three
    rows read `Modified` today, the M4 correction is in the brief, and
    `SR-144` re-attests with the window like every other row. No separate
    flip call exists.

**CLOSED TODAY — the sitting only countersigns these.** They are owner rulings
already executed; listed so the sitting knows it is reading a settled state
rather than an open one, and so an overrule is a deliberate act.

- **`SR-053` RETAINED and `hat.CONSISTENCY` ruled `always`** (`2026-08-16p`) —
  the "retire unless it can be tested mechanically" condition was found
  **already met** (8 LLRs → 8 TCs, 11 automated tests, all green); the row's
  only dependence on a retired rubric was its AC cell, corrected in the same
  ruling. What stays open on the row is **provenance, not verification**, and
  it is now answered by a lens rather than a need — the narrower finding (no
  need states cross-view coherence) is recorded in the row's `Rationale`, so
  cutting the charter later re-opens the right question. R-5/R-6 unmoved.
- **The retired-rubric acceptance corrected on `SR-052`/`SR-053`/`SR-054`**
  (`2026-08-16p`) — acceptance restated as the decomposed LLR/TC chain with no
  artifact named. Two residues named and **not** ruled: the three `Rationale`
  cells still assert the retired method, and `trace.py` has no
  AC-vs-`Verification` coherence lint.
- **The hat roster CLOSED at sixteen, all ratified** (`2026-08-17`) —
  `INTEGRITY-RECOVERABILITY` and `PRODUCT-FITNESS` ruled `always`, no
  provisional block remains in either roster. The ruling's condition
  (downstream opt-out) was verified against `bootstrap.copy_if_new` +
  `RESYNC_PACK`, not assumed.
- **Option (b) — hat-derived labels over SN amendment** for the quality family;
  16 rows labelled, `SR-155` alone left lens-less (`2026-08-16l`).
- **ACCESSIBILITY and PERFORMANCE ruled `always`** — the switched-off-hat
  residue dissolves and the four stale "switched-off" labels are reworded to
  state the dependency CLOSED; the silence taxonomy now names only
  SAFETY/LEGAL/DATA-PROTECTION as silent-by-design (`2026-08-16n`).
- **The SN `tags` wiring** — 17 needs tagged by the charter-subject rule, 10
  left untagged deliberately; this is what makes a governing hat reach its own
  need at all (R-2, `2026-08-16l`), with `hats.py audit` as its standing sweep
  (`2026-08-16m`).
- **`SN-006`'s safety half moved out of `why` into the normative need text**,
  which makes `SR-043`'s parentage text-derivable (`2026-08-16l`).

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

> **DO NOT READ THE TABLE BELOW AS STATE — 2026-08-16.** Every figure in it is
> pre-merge and pre-v2, and its **vocabulary is retired**: `Verified`, `Draft`
> and `Planned` no longer exist as values (the rename narrowed the enum to
> `{Drafted, Approved, Modified}` and folded `Planned` into `Approved` —
> `2026-08-15m`). The window itself is unchanged in KIND: the `Modified` rows
> re-attest and the `Drafted` rows ratify, as one sequence with the
> status-vocabulary program (`2026-08-14e`). **Read the live window off
> [`../gate`](../gate)'s basis line and the regenerated brief**; the table stays
> as the record of what the window looked like when this sitting was assembled.

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

> **CLOSED — RULED `2026-08-14f`, ledger row 4: LIFTED, both halves.** The pick
> below was made deliberately rather than left to a slice, and it turned out to
> be a third reading neither option named: **the §2.3 lift had CROSSED the
> subject pairs** (converter TC-159↔LLR-165, reader TC-160↔LLR-166), so
> re-pointing would have forged a converter-requirement→reader-test edge. Kept
> for the reasoning; nothing here is owed.

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

> **RULED AND LARGELY EXECUTED — re-stamped 2026-08-16.** The decision this
> section was written to force is **ledger row 5, RULED `2026-08-14e`**: one
> sequence with the ratification wave. Steps 1–5b then executed (`2026-08-15g`,
> `2026-08-15m`) — the enum closed at live truth, the `last_approved` snapshot
> mechanism replaced D-1's hash anchor on your `2026-08-15d` directive, and the
> rename narrowed the vocabulary to **`{Drafted, Approved, Modified}`** with
> `Planned` folded out, **without moving the gate**. §3.5 and §3.6 below are
> **closed** (OI-30 D1 and D3, `2026-08-15k`/`l`). §3.2's hard coupling
> **dissolved** with the anchor it depended on. What is left of this section is
> the sitting's own act: **sign → seed → step 7** (review-package §5 steps 3–4).
> The subsections stay as the argument that produced the sequence; read §3.1 and
> §3.3 in particular, because the asymmetric-failure row and the recorded
> coverage gap are what step 7 is arming against.

**The migration is PART-EXECUTED** (steps 1–5b landed 2026-08-15,
`2026-08-15g`/`2026-08-15m`; the sitting owes sign → seed → step 7). D-9
renames `Draft` / `Verified` / `Modified` → **`Drafted` → `Approved` →
`Founded`**, uniform across SN · SR · LLR · TC. The **checklist of record is
the LIVE** [`2026-08-15-d9-migration-plan.md`](2026-08-15-d9-migration-plan.md)
(step 7 verbatim: retire the transitional word; enum →
`{Drafted, Approved, Founded}`; drift = snapshot comparison). The earlier
checklist survives as history at
[`../archive/plans/2026-08-11-status-ladder-migration.md`](../archive/plans/2026-08-11-status-ladder-migration.md)
— its header's *"Nothing here is executed"* was true when written, false since
2026-08-15; this §'s old pointer at it is the mis-aim item 16 records.

**⚠ Stale-figures warning.** Every number in that archived document was measured
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
2. **The signed rows' `Status` moves in a reviewed commit** — under the renamed
   vocabulary (`2026-08-15m`) that is `Modified` → **`Approved`** and `Drafted`
   → **`Approved`**, both rungs landing on the same word; the retired
   `Verified`/`Planned` targets this step originally named no longer exist.
   **[`../gate`](../gate) is DERIVED, never hand-set.** **Then seed the snapshot
   in the same reviewed commit** (`intake.py snapshot --seed`) — the copy must
   ride the approval, and it is the birth of drift detection.
3. **`python project-trajectory/scripts/derive_gate.py`** regenerates the bar; the
   `drafted` / `modified` / `uncovered` counts fall and the bar rises on its own
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
