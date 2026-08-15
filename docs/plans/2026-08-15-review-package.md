# The review package — everything the 2026-08-15 charge-through prepared, and the sitting that closes it

**For the owner.** This is the one document to run the review sitting from.
Written at the end of the 2026-08-15 charge-through (owner instruction: *"charge
through as much as possible until the updates to the spine are ready for me to
review and approve, with all related changes like vocabulary, wording, and
interfaces completed"*). Everything below is **provisional and overturnable**;
nothing was flipped toward `Verified`/`Approved`; no snapshot was seeded; the
signing acts are all still yours.

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

**Measured state:** `SN=27 SR=59 LLR=155 TC=150 orphans=0 integrity=0
component-findings=0 interfaces=122 interface-findings=0 form-findings=2` (the
two recorded 13v waivers). Full suite at last run: **2525 passed, 10 skipped**.
Gate unchanged at `DevBar-Reqs`.

---

## 2. The three rulings the sitting must make first — **OI-30**

All three are surfaced on [open-items.html](../open-items.html) /
`docs/requirements/open-items.toml` OI-30, with the full analysis in
[2026-08-15-d9-migration-plan.md](2026-08-15-d9-migration-plan.md):

1. **`Planned`'s fate** — recommendation: fold out into `Approved` at the
   rename (it is the same rung; a fourth rung collides with `CMP_MATURITY`'s
   `"planned"` and re-opens the uniformity ruling).
2. **The `sr_bar` ceiling** — recommendation: ceiling at `BAR_TESTS` with a
   regression pin until the harness driver lands (otherwise the migration
   silently collapses DevBar-Tests into DevBar-Release).
3. **Off-spine approval authority** — recommendation: keep the 0–4 ordinal
   untouched; add `[attestation] human_approval_registries = ["interfaces",
   "external", "components"]`, unlisted-means-held, enforced by a new
   `human_approves()` read by the dispatcher and every approving writer.

---

## 3. The judgement items recorded for you (none blocks the wave)

From the second top-down read (`2026-08-15i`):

- **H1 — SR-166 vs SR-163 severity conflict:** both report the
  manifest-completeness observables, one warns where the other fails.
  Recommendation: SR-166 sheds the two shared clauses, cross-references SR-163.
- **M1 — SR-159 vs SR-162** both claim the IF endpoint/Signal declaration
  site. Recommendation: SR-162 keeps (SN-037's words), SR-159 gains the
  carve-out.
- **M3 — the llr-status advisory message** is now false seven times over
  (the Planned repair discharged what it warns about). Recommendation: correct
  the message ("evidence owed", not "invisible to the sitting"), keep the warn.
- **L1 — SR-151 `["B-06"]`** should probably read `["B-06","B-05"]` (the X2
  precedent decides it).
- **L2 — no SR states that a perf-budget regression fails** (vacuous here, the
  template ships the layer).

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

<!-- ROUND2-VERDICT -->

---

## 5. The sitting procedure, in order

1. **Rule OI-30** (§2, three calls). Everything after step 2 is shaped by them.
2. **Sweep §3's judgement items** — each is a one-line confirm/overrule; the
   log entries carry the detail.
3. **The rename (migration step 5/5b) executes** — mechanical, ~30 min of
   agent work once OI-30 D1 is ruled: `Draft→Drafted`, `Verified→Approved`,
   `Planned→` per your D1 ruling, predicates, templates, shipped prose, the
   basis-line + `_BASIS_RE` in one commit, the `--ratify` scope rename. The
   complete touchpoint table is
   [2026-08-15-d9-migration-plan.md](2026-08-15-d9-migration-plan.md) §B.
4. **Review the ratification brief** —
   [docs/ratify/2026-08-13-wi444.md](../ratify/2026-08-13-wi444.md)
   (regenerate first: `trace.py --ratify modified --out …`) and
   [open-items.html](../open-items.html) §2. The wave signs the `Modified`
   rows and ratifies the Draft ones — this is sitting-3's §2.1 window, and the
   status-vocabulary program rides it as one sequence (ruling `2026-08-14e`).
5. **Sign** — `intake.py`'s flip writer records your rulings; then **seed the
   snapshot**: `python project-trajectory/scripts/intake.py snapshot --seed`
   in the same reviewed commit. This is the first copy to
   `docs/archive/last_approved/` and the birth of drift detection.
6. **Steps 7–8 execute** (mechanical follow-on, same reviewed act): retire
   `Modified` + the transitional predicates, arm the UNANCHORED rule on the
   integrity floor, apply the `sr_bar` ceiling per your D2 ruling.
7. **`push = "human"` remains yours**, as does the merge-to-main call.

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
