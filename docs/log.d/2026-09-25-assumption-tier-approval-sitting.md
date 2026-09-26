## 2026-09-25 — The assumption tier's approval sitting: three adjudications, a re-anchor and the phase-6 act

An attended sitting on `refactor_again` after the owner returned and ruled the
[spine map](../plans/2026-09-25-assumption-tier-spine-map.md)'s D1, D11, D12 and
D28 ("Agreed"), then directed the handoff's order: WI-641, WI-601 and WI-603,
then the approval act WI-642. Reviews are codex Sol (medium). A Fable (medium)
agent arbitrates any disagreement between this session and a reviewer.

Deferred open items: none — the owner-reserved decisions stay numbered in the
spine map §6 (D8, D10, D14, D22, D29, D30), and none holds a gate or blocks a
queue.

### The three adjudications

- **Verdicts:** WI-641 `CLARITY rows=1` (SR-162: one stale clause dropped from
  its rationale); WI-601 `MEANING rows=1` (LLR-061: the multi-row assignment
  block); WI-603 `MEANING rows=1` (LLR-167: `amendment` routed, `conflict`
  retired, the consolidation assembler added). Each file is under
  `docs/reviews/wi-6NN-*/001-ADJUDICATE-f263118.md`. Both MEANING rows were
  judged blessable (within their parent SRs, true of the code, driven by
  named tests). Their re-attestation is the joint re-anchor below.
- **Sol review:** NOT YET SOUND, 1 blocker, 2 major, 2 minor. It confirmed
  every row call and the re-anchor's safety. Applied: the anchor now names each
  registry's own copy (27a30842 for requirements, 2e1197fd for design rows)
  rather than the brief's directory-wide stamp; "re-attested" now waits for the
  copy; the blessing wording is exact; LLR-253 is out of the collateral range.
  One correction to Sol: the requirements copy was last written at 27a30842,
  not the 580df781 it named.
- **Arbitration (the blocker):** Sol held that each verdict must rule all
  twenty rows its brief rendered. The Fable arbiter ruled for the scoped count,
  on WI-566's reviewed correction and WI-573. Nothing parses the `rows=` number,
  and ruling twenty rows three times would put MEANING on seventeen rows already
  ruled CLARITY three times. Each verdict now carries WI-566's "excluded from
  the count" section.
- **Filed by hand:** WI-645, WI-603's disposition under its drafted title
  (TC-061 and TC-161 lag their amended design rows, and two routed assemblers are
  named by no design row), needing WI-642; WI-646, the brief defect (whole-tree
  rendering, directory-wide stamp), needing WI-645. Watermark raised with
  `trace.py --bump-ids`.
- **Deviation:** the three rows were ruled in an attended sitting, not claimed
  through the integrator into lanes, since the loop is paused. Specs were
  closed with `spec_move.py` straight from `queued/`.
- **Commit bar for the adjudications:** smoke **1681 passed, 3 skipped** in
  164.8 s.
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=f2631182 -->
  Seconds **FAIL**: `check_smoke_budget.py --mode enforce` measured 164.7 s
  against the 60 s budget (spine map D10, this 8-core machine), recorded and not
  re-stamped. `check_docs --stale` OK (0 broken, 4 orphan warnings);
  `check_trajectory --strict` clean after clearing the closed specs' `specref`
  (its R-F rule caught the first close); `trace.py --strict-integrity` 0
  integrity, 0 orphans; the open-items view up to date.

### The re-anchor of LLR-061 and LLR-167

- **Act:** `intake.py snapshot --approves
  "docs/requirements/low-level-requirements.toml=WI-601+WI-603"`, in its own
  commit after both verdicts, as the amendment brief's aftermath requires for a
  released rung. The copy is scoped to the design-row record. Checked after the
  copy: the record equals the live registry, and the only attesting cells it
  absorbed are LLR-061's and LLR-167's `detail`, the two cells the verdicts
  ruled. The rest is file-scope collateral: 48 Drafted rows (not approvals) and
  traced `module` and `code_symbol` cells (non-attesting by ruling, §A5.1).
- **Commit bar for the re-anchor:** smoke **1681 passed, 3 skipped** in
  155.9 s; seconds **FAIL** at 156.6 s against 60 s (D10), recorded, not
  re-stamped. `check_docs --stale` OK (0 broken); `check_trajectory --strict`
  clean; `trace.py --strict-integrity` 0 integrity; `CURRENT.md` fresh; the
  open-items view up to date.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=71844466 -->

### The phase-6 approval act (WI-642)

- **Who approved what.** The four needs, SN-041 to SN-044, are on the rung
  the owner holds (`human_approval_through = "DevStg-Needs"`). They were signed
  by the owner's **stand-in**, a Fable (medium) agent reading the phase-6
  brief at this sitting, as the owner directed. They are not the owner's own
  signature. The 33 requirements, 47 design rows and 40 test cases sit on
  released rungs and are approved on the LLM verdicts: codex Sol's per-tier
  reviews and the earlier stand-in's per-tier approvals (spine map §5),
  confirmed at this sitting. Stand-in verdict: `SITTING: APPROVE`, every need
  approved and the chains confirmed. Every SR cites one of the four needs or an
  approved need; every SR has a design row and a test case; every design row
  has a test case.
- **Owed by the owner (re-attestation):**
  - **D6/D20, SN-042's acceptance, first.** As the owner accepted it (the C1
    package): "…the project record shows that order for every requirement;
    …". As approved: "…the project record shows that order for every
    requirement approved after the project adopts this rule; …". A one-line
    ruling keeps or reverts the narrowing.
  - **D2:** SN-043 and SN-044 are new needs no owner has signed.
  - **D5:** SN-041's first acceptance sentence is answered by a later
    assumption row, not by an SR.
  - Still reserved: D8, D14, D22 (spine map §6).
- **D3, stated plainly:** the needs flip without `stakeholder_refs` or
  `source`. SN-044's own acceptance is met only once the C1 sitting commit
  (WI-643) writes them, after the build ships the keys.
- **The act.** One commit flips 124 rows (`status` only; each row's other
  cells compared equal before and after). The dated brief
  `docs/ratify/2026-09-25-phase6-assumption-tier.md` is minted from the fresh
  `CURRENT.md` at the act's parent. The stand-in read the `trace.py --approve
  6` rendering, and that rendering is byte-identical at the act's parent. The
  snapshot copies the four spine records. The design-row and test-case records
  are authorised by their Status moves. The requirements and needs records are
  named with `--approves`, because the tool refuses to absorb drifted approved
  text that a Status flip alone does not cover, and it never infers a needs
  approval. Checked after the copy: each record equals live. The only moved
  cells on existing rows are the 124 status flips and 18 SR `rationale` cells:
  the seventeen ruled CLARITY at WI-547, WI-593 and WI-599, and SR-162 ruled
  CLARITY at WI-641. LLR-061 and LLR-167 were re-anchored in the previous
  commit. Collateral rows (SR-183..SR-186, TC-208..TC-211) arrive Drafted,
  not as approvals.
- **Stage:** the headline stays **DevStg-Tests** (settled), and phase 6 reads
  DevStg-Impl; the derived current phase is now 6.
  <!-- fig: cmd="python project-trajectory/scripts/derive_stage.py --root ." rev=f537fc53 -->
- **Deviation, `test_first_since`: not set by this act.** WI-642 asked for
  "this commit", which a commit cannot name. SR-217 judges requirements
  "approved after" the start, so the right value is the act's **parent**,
  f537fc53 (the stand-in flagged this). The key cannot be declared yet:
  `tests/test_rule_sync.py` holds this repo's `[checks]` keys equal to the
  shipped template's, and the template gains the key only with WI-640. A first
  attempt declared it and the smoke tier failed on exactly that rule, so the
  value is recorded in WI-640's spec instead, and WI-640 sets it when it ships
  the key.
- **README:** the four approved needs gained inventory bullets, marked
  commissioned rather than shipped. `check_docs` fails an approved Must/Should
  need no README bullet cites.
- **Sol review of the staged act:** NOT YET SOUND, 2 blockers (close WI-642
  in the act and leave a truthful next-work surface; the README bullets) and 1
  minor (the snapshot stamp now says which verdict covers which rows). All
  applied. It also confirmed the flip, the record's absorption and the needs'
  `--approves`. It judged the `test_first_since` key acceptable; the test
  above overrules that.
- **Closed:** WI-642, in the act commit. The status bullet, the handoff's
  resume map and the spine map §6 (the owner's rulings) point at the build.
- **Commit bar for the act:** smoke **1681 passed, 3 skipped** in 178.1 s
  (with the `test_first_since` key removed; with it, one failure in
  `test_rule_sync`, above); seconds **FAIL** at 178.9 s against 60 s (D10),
  recorded, not re-stamped. `check_docs --stale` OK (0 broken);
  `check_trajectory --strict` clean; `trace.py --strict-integrity` 0
  integrity; `CURRENT.md` fresh; `approval-immutable` ok; `derive_stage
  --check` up to date at DevStg-Tests; the open-items view up to date.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=f537fc53 -->
