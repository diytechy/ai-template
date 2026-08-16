# The review package — everything the 2026-08-15 charge-through prepared, and the sitting that closes it

**For the owner.** This is the one document to run the review sitting from.
Written at the end of the 2026-08-15 charge-through (owner instruction: *"charge
through as much as possible until the updates to the spine are ready for me to
review and approve, with all related changes like vocabulary, wording, and
interfaces completed"*). Everything below is **provisional and overturnable**.
**No claim was ever strengthened**: the vocabulary rename moved words
value-for-value under your OI-30 rulings (`Planned`/`Verified` → `Approved` is
D1's fold, not a signing), no snapshot was seeded, and the signing acts are
all still yours.

---

## 1. What landed (the range `bb4ac776..HEAD` on `infra/mechanized-loop`)

| act | log entry | state |
|---|---|---|
| The re-tier merged to trunk, `WI-451 = partial` on your ruling | — | done |
| The seven class-A authoring calls + SR-165's chain (H1 mint SR-166 · H4 merge SR-153/SR-059→SR-148 · H5 one-home · M1 four demotions incl. two `Verified` rows · M3 three coverage extensions · X1/X2 confirmed) | `2026-08-15b` | done, overturnable per call |
| OI-29 ruled **(b)** — the B-05 concentration is real (your ruling, with the two riders recorded) | `2026-08-15c` | ruled by you |
| The snapshot directive — `archive/last_approved/` replaces the hash anchor (your ruling) | `2026-08-15d` | ruled by you |
| The interface rework, all 8 steps: IF schema tier (warn-first) · endpoint validation + `external:` marker · 8 rotted cells fixed · `sr_refs`→`req_refs` · the `owner` cell on all rows (21 judgement picks listed in the log) · flow/ownership split · `carried_by` prototyped on IF-102 · header re-based off dead SR-091 | `2026-08-15e` | done, picks overturnable |
| WI-459 crossing ownership (4 verdicts: B-01 realize/SR-019+020 · B-02 no-interface-today · B-06 realize/SR-151 · B-07 realize/SR-152) · WI-456's 16 amended cells adjudicated (14 scope-did-not-move, 2 deleted-by-ruled-demotion) · WI-457 close confirmed | `2026-08-15f` | done |
| D-9 migration steps 1–4b: Status enum closed at live truth `{Draft, Planned, Modified, Verified}` on the integrity floor · `is_planned` repairs the Planned blind spot · the `last_approved` snapshot mechanism built reader-first (module, mirror invariant, intake writer + `snapshot` subcommand, seed pinned out of every loop path) · the drift overlay · ~160 lines of git-walk baseline machinery deleted · the amendment adjudicator routed | `2026-08-15g` | done; boundaries held |
| LLR-158/TC-153 re-pointed onto the surviving mechanism; LLR-173/TC-167/IF-123–129 mint the snapshot module's spine coverage; dead `_rows_at`/`_toml_rows_text` deleted | `2026-08-15h` | done |
| The second top-down read (6 findings: 2 fixed, 4 recorded — §3) + the SKIP guard (built; the stronger refusal shape is yours to accept or decline — §3) | `2026-08-15i` | done |
| Adversarial round 2 — CHANGES-REQUESTED, 7 MAJOR (5 confirmed+fixed, 1 half-confirmed+fixed, 1 dispositioned — §4); `WI-460` CLOSED, the re-tier's verification COMPLETE | `2026-08-15j` | done, fixes overturnable |
| **D-9 migration step 5/5b — THE RENAME**: the Status enum narrows to `{Drafted, Approved, Modified}` (SR 15/22/22, LLR 17/59/79, TC 16/127/7) · `Planned` FOLDS into `Approved` per your D1 and `is_planned` is deleted in both homes · 136 off-spine `approval` cells `draft`→`drafted` · `drafts=`→`drafted=` and `planned=` gone from the basis line with `check._BASIS_RE` in the same commit · shipped prose + templates + ~185 test literals + 3 goldens. **The gate did not move: DevBar-Reqs, stage DevStg-Boundary.** | `2026-08-15m` | done, overturnable |
| **The `sr_bar` ceiling + its marker (your D2)** — `DevBar-Release` unreachable-by-cell, regression pin commented as deliberately deleted when the harness driver lands; the derived line renders `DevBar-Tests (Release: pending harness driver)` from one home. **§3 gains a measured finding: the ceiling's "loosens nothing" premise is FALSE for 11 harness steps** — read it before you accept the ceiling as ruled. | `2026-08-15m` | done; **one finding for you** |
| **Ladder-derived off-spine approval authority (your D3)** — `agent_common.APPROVAL_RUNGS` + `human_approves`, no new key and no new enum; the dispatcher seam + the writer-side contract, with the honest note that no WI kind carries a registry identity today | `2026-08-15m` | done |
| **The §3 judgement sweep on your rulings** — H1 confirm · M1 carve-out (the merge declined on a measured detail) · M3 inverted + the deeper-cut message sweep · L1 confirmed (no IF realizes B-06) · L2 `SR-167` minted — plus four 3.11-floor fixes forced by running the bar on the repo's own venv, and the honest note that the earlier full-suite greens were produced by an interpreter the record does not name | `2026-08-15n` | done, overturnable |

**Measured state (post-sweep):** `SN=27 SR=60 LLR=155 TC=150 orphans=0
integrity=0 component-findings=0 interfaces=122 interface-findings=0
form-findings=2` (the two recorded 13v waivers). Full suite at last run, **on
the repo's own `.venv` 3.11.9**: **2537 passed, 13 skipped, 4 failed — all
four pre-existing environment findings named in log `2026-08-15n`**, none of
the sweep's content. (The earlier "2544 passed" figure was produced by an
interpreter the record does not name — two 3.11-deterministic defects fixed at
the sweep made that run impossible on the declared floor.) Gate unchanged at
`DevBar-Reqs`.

---

## 2. OI-30 — **CLOSED, all three ruled** (owner, in session — log `2026-08-15k`/`l`) **and executed** (`2026-08-15m`)

The record, with the full analysis in
[2026-08-15-d9-migration-plan.md](2026-08-15-d9-migration-plan.md):

1. **`Planned`'s fate — RULED: fold out into `Approved`** at the rename.
   Your words: functionally equivalent — both fire the breakdown into expected
   children — and "approved" is clearer.
2. **The `sr_bar` ceiling — RULED: it stands** (log `2026-08-15l`), with the
   mitigation folded in: while it holds, the derived gate line reads
   `DevBar-Tests (Release: pending harness driver)` so the ceiling is never
   mistaken for a regression. Consumers were enumerated before the ruling —
   all monotone-stricter, `--gate DevBar-Release` stays invocable — and your
   framing is the recorded intent: the gate is computed by running the bar,
   not inferred from a cell. **OI-30 is CLOSED, fully ruled.**
3. **Off-spine approval authority — RULED, on your simpler shape:** it
   follows the **dev-stage ladder directly** — no new key, no new enum. The
   registry→rung association already exists in `derive_gate`
   (`boundary_incomplete` gates DevStg-Boundary on `external.toml`;
   `arch_incomplete` gates DevStg-Arch on components): `external.toml` is held
   at dial ≥1, `interfaces.toml`/`components.toml` at ≥2, an unmapped
   approval-carrying registry is held. At your dial of 4, identical effect to
   today — derived rather than declared.

---

## 3. The judgement items recorded for you (none blocks the wave)

From the second top-down read (`2026-08-15i`) — **SWEPT 2026-08-15 on your
rulings (log `2026-08-15n`); what each became:**

- **H1 — SR-166 vs SR-163 severity conflict: CONFIRMED, no act owed.** You
  accepted the recommendation; adversarial F7 had already executed the same
  shed convergently, so SR-166 states destination materialization + dogfood
  parity only and presence is SR-163's.
- **M1 — SR-159 vs SR-162: you asked to MERGE unless a detail was missing;
  the detail is real and measured** (log `2026-08-15n`): one shared observable
  of 6–7, zero shared requirement text, zero shared code symbols, independent
  vacuity regimes (at authority dial rung 1 — every adopter's normal state —
  SR-162 applies while SR-159 is vacuous); a merge either way is a mega-row
  (two vacuity regimes, three severity regimes, a phase-1/phase-5 conflict,
  a third 13v waiver), and dropping SR-159 costs ~19 citation edits besides.
  Executed instead: the carve-out on SR-159's by-default closer, widened to
  the TRIPLE claim the analysis found — endpoint-pair/Signal semantics are
  SR-162's, the generic required-field checker stays SR-157's (LLR-003).
  Overturnable like every authoring call.
- **M3 — INVERTED, then executed deeper than recommended.** The recorded
  recommendation ("evidence owed", not "invisible") died with the rename: the
  fold deleted `is_planned` and the advisory's claim is TRUE again — durably,
  by construction (`is_drifted` fires only on a row claiming approval, so a
  `Modified` child under an `Approved` parent is seen by NEITHER the marker
  arm nor the drift arm). The message now names that mechanism; your "deeper
  cut" question was answered YES and swept — six stale message/label fixes
  (the worst: three dashboard labels presenting `approved` counts as
  "verified", the exact double claim your D1 deleted) plus three `Drafted`
  LLR details. Full list: log `2026-08-15n`.
- **L1 — your "no interfaces satisfying B-06" is CORRECT, not a search gap:**
  zero IF rows realize B-06 — the recorded, owned gap from `2026-08-15f`
  (owner SR-151, execution the wi455 lane's). That fact is orthogonal to the
  `["B-06","B-05"]` attribution call, which stays open with the sweep's
  addendum: **SR-152/B-07's acceptance is the same package-alone shape, so X2
  applies to the pair or to neither** — flip both cells or leave both. Cells
  untouched.
- **L2 — the virtualized testing you asked about ALREADY EXISTS**
  (tests/test_check_perf.py: the regression arm end-to-end against a
  bootstrapped scaffold, plus unit, warn-tier, malformed, tier-scoping and
  harness-wiring arms); the gap was the SR statement alone. **`SR-167` minted
  `Drafted`** (both breach arms — one delivered exit contract, the SR-157
  one-verdict shape); IF-004/IF-031 `req_refs` gained it. **LLR-014.sr_refs
  and TC-014.verifies re-points are the sitting's** — both rows are `Approved`
  and amending an attested cell rides no sweep.

Carried from earlier in the session: **B-04's `carries` may need widening**
(X1's honest strain, `2026-08-15b`); **B-04 is only half realized** and no
advisory says so (`2026-08-15f`); **SN-037's review-obligation residual** is
stated on SR-162 rather than mechanized; the **`intake.py` singular-Disposition
defect** (`2026-08-15f` — an adjudication whose verdict is "nothing owed"
cannot say so under the contract's own heading); the **enum closure retires the
"Status is open vocabulary" promise** in three shipped docs (prose moves at the
rename; adopters covered by the RESYNC entry, but the sitting should confirm
rather than inherit it — `2026-08-15g`); the **SKIP guard refusal question**
(`2026-08-15i` — the built guard is a loud banner; making a declared-but-absent
tool a hard refusal breaks adopters and is yours to impose or decline).

The **21 interface owner picks** (`2026-08-15e`) and the **four crossing
verdicts** (`2026-08-15f`) are open to overrule item-by-item; the log entries
carry the reasoning.

## 4. Adversarial round 2 (cross-family, GPT-5.6 Sol via codex, read-only)

**Verdict: CHANGES-REQUESTED — 7 MAJOR.** Run on the settled tree after
`WI-458`, `WI-459` and the second read, so its findings do not postdate their
own fixes the way round 1's did. Every finding was re-verified by the author
before acceptance. Full text on the record:
[reviews/wi451-retier/ROUND-2-SOL.md](../reviews/wi451-retier/ROUND-2-SOL.md).
Detail and reasoning: log `2026-08-15j`.

| # | finding | disposition |
|---|---|---|
| F1 | `SR-140` still required the on-row digest anchor your `2026-08-15d` directive abolished — "never in a second registry", and same-commit anchoring an ERROR — while `LLR-173` claimed to implement it by copying whole files into a second tree in the approval commit | **FIXED.** Re-based onto the ruled contract; surviving obligations kept, the same-commit clause inverts (the copy MUST ride the approval), anti-laundering carried by the mirror invariant + seed rules. Held at 3 shalls |
| F2 | `unanchored_findings` was defined and **called by nothing** — an approval could bypass the record with no live check to say so; the mirror invariant also exited silently on a snapshot file *deleted* in the commit | **FIXED (both).** Wired into `trace.py` as an always-on advisory; deletion arm added. The ERROR promotion stays at migration step 7 **by design** (§B4/§B6). Wiring it found a further defect: the vacuum was keyed on the scaffolded directory, so it reported all eight tiers missing in every fresh adopter repo |
| F3 | `_claims_approval` read `Status` alone, so the four off-spine tiers snapshotted *because* their maturity cells are human-only were never drift-compared | **FIXED in the confirmed half** (tier-aware now, claimed sets derived from `derive_gate`'s ruled table). The SN half is **by design** — §B7, needs carry no maturity cell |
| F4 | No per-row before/after evidence for this sitting | **RECORDED DECISION, not fixed.** The wave is a full re-read (`2026-08-14e` / sitting-3 §2.1), and git-walk baselines are meaningless for rows the re-tier restructured. Raw diff: `git diff bb4ac776..HEAD -- docs/requirements docs/test`. Per-row before/after resumes from your first seed (step 5 below) |
| F5 | `SR-059`'s **migrated-repo** deletion obligation was dropped in the `WI-458` merge — only the fresh-scaffold half survived, so an adopter upgrade could keep the retired authority files and still pass | **FIXED.** Restored into `SR-148`'s acceptance; `LLR-060` names where each half discharges |
| F6 | `IF-004`/`IF-031` owners pointed at SRs that do not own the perf-verdict contract | **FIXED** — both → `LLR-014`, the polymorphic cell's first LLR owners. **The deeper gap stays open for you:** no SR states a perf-regression obligation at all (§3, L2). No row minted |
| F7 | `SR-163` and `SR-166` prescribed **conflicting outcomes** for the same manifest defects — an implementer could satisfy one only by violating the other | **FIXED.** `SR-166` sheds the two presence clauses (token-checked into `SR-163` first, so nothing vanished) and keeps destination materialization + dogfood parity |

**Nothing in this round moved a `Status`, an `approval` or an attestation cell.**

---

## 5. The sitting procedure, in order

> **⚠ Read the 10 ex-`Planned` rows even though no brief lists them.**
> D1's fold moved SR-137/138/139/140/144/146/147/148/149/150 to `Approved`, so
> they left the re-attest brief — and until your seed exists, the unanchored
> advisory is vacuous, so they sit on **no surface at all** while the seed
> will bless their text. They are the one set the surfaces cannot hand you;
> the sitting's read must include them deliberately (log `2026-08-15m`).

1. **Sweep §3's judgement items** — **DONE 2026-08-15 on your rulings** (log
   `2026-08-15n`; each disposition is in §3 above, every act overturnable).
   What §3 still hands you at the sitting: the L1 pair call
   (`SR-151`+`SR-152` boundary_refs, together or not at all), the dead
   red-TC-census rung (retire or re-arm), TC-123's retired-vocabulary method
   cell, the LLR-014/TC-014 re-points onto `SR-167`, and the three small
   naming calls (intake's "re-verify" verbs, bootstrap's `Status: DRAFT`
   header, the `--require-verified` flag name). (OI-30 is closed — §2.)
2. **Review the ratification brief** —
   [docs/ratify/2026-08-13-wi444.md](../ratify/2026-08-13-wi444.md)
   (regenerate first: `trace.py --ratify modified --out …`) and
   [open-items.html](../open-items.html) §2. The wave signs the `Modified`
   rows and ratifies the Draft ones — this is sitting-3's §2.1 window, and the
   status-vocabulary program rides it as one sequence (ruling `2026-08-14e`).
3. **Sign** — `intake.py`'s flip writer records your rulings; then **seed the
   snapshot**: `python project-trajectory/scripts/intake.py snapshot --seed`
   in the same reviewed commit. This is the first copy to
   `docs/archive/last_approved/` and the birth of drift detection.
4. **Step 7 executes** (mechanical follow-on, same reviewed act): retire
   `Modified` + the transitional predicate, narrow the enum to two, resolve
   `intake`'s `!= "Modified"` guard into a refusal, and arm the UNANCHORED rule
   as an ERROR on the integrity floor. (The `sr_bar` ceiling of your D2 is
   already landed — see §1 and its finding in §3.)
6. **`push = "human"` remains yours**, as does the merge-to-main call.

**THE RENAME IS NO LONGER A SITTING STEP.** Migration step 5/5b executed
2026-08-15 under your three OI-30 rulings (`2026-08-15m`); the brief in step 3
has been REGENERATED and its cells now read the new words. What changed for you:
the brief went from 47 SR sections to **37**, because the 10 SRs that read
`Planned` now read `Approved` and an approved row owes no re-attest. Those ten
are named in the log entry — **they are the rows the fold moved past you**, and
they are unanchored until the seed, so step 4 blesses their text whether or not
you read it here. Read them from the log's list, or overrule the fold. (The
sweep regenerated the brief once more — **38 sections now**, `SR-167` joining
the Draft-ratification set; log `2026-08-15n`.)

---

## 6. What was deliberately NOT done, and why

- **No status value renamed, no row signed, no snapshot seeded** — those are
  the sitting's acts (rulings `2026-08-14e`, `2026-08-15d`, repo-lock D-10's
  sequencing rule).
- **The interface schema inversion** stays dead (four measured blockers,
  [2026-08-15-interface-rework-plan.md](2026-08-15-interface-rework-plan.md)
  §2) — and after Q1/Q2 it is unmotivated, not merely blocked.
- **The `views` facet** (Q4) is ruled for the model, withheld from this repo's
  schema while nothing would populate it.
- **`dispatch._TC_NOT_RED`** deliberately did not gain `planned`
  (`2026-08-15g` — it would have made the red-census rung unreachable);
  re-decide at the rename if wanted.
- **WI-448** (one-home-per-behaviour), **WI-452**, **WI-390** and the
  **wi455-architecture-retirement lane** (D-3) are separate programs,
  untouched.
