## 2026-08-24 — WI-513 widens `owes()` past the SR-only test, and OI-62 files the (b) go/no-go

Two owner-directed acts (2026-08-24, in-session: *"Yes that sounds suitable"*),
against the blind spot the 2026-08-23 sitting stopped on rather than resolved
(`docs/log.d/2026-08-23-oi61-rule-and-spine-approval.md`, "THE DISCREPANCY —
nineteen `Drafted` spine rows the owner surface does not enumerate"). The
owner's chosen path, verbatim: *"fix the surface first, approve from a
corrected brief."*

Deferred open items: OI-62 — the (b) go/no-go on the contract generalization's
second stage. A pending brief, not a decision this sitting owed.

### Act 1 — `WI-513`: the `owes()` widening, executed and closed

**The mechanism gap, restated from the finding.**
`trace.reattest_model`'s `owes(sr)` tested `is_drafted` on the **SR row
only**: `is_drafted(sr) or sr_chain_drifts(...)`. A `Drafted` LLR or TC under
an `Approved`, undrifted SR reached no surface — `sr_chain_drifts` cannot see
it either, since a row below approval has made no claim to fall from the
snapshot, and one absent from the snapshot is unanchored rather than drifted.
The function's own docstring already stated the wider contract it did not
implement: *"a row now owes an act when it is `Drafted`"* — a row, not the SR.

**The widening.** `owes()` now also asks the question of every row in the
SR's chain:

```python
def owes(sr):
    if is_drafted(sr):
        return True
    chain = chain_of(sr.get("SR-ID", ""), srs, llrs_by_sr, tcs_by_ref)
    if any(is_drafted(row) for _kind, _rid, row in chain):
        return True
    return sr_chain_drifts(sr.get("SR-ID", ""), chain, snapshot)
```

Kept honest at three more points, so the two renderers that share this model
(`gen_open_items.py`'s `open-items.html`, `trace.py`'s markdown brief) stay
coherent:

- **The pill answers for the whole chain, not the SR alone.** `_entry_kind`
  now takes `(sr_drafted, chain_has_drafted)` — a card wears "approval owed"
  if the SR or ANY chain row is `Drafted`, "re-attest owed" only for pure
  drift. Before, an `Approved` SR with a `Drafted` child wore "re-attest
  owed", which named the wrong act.
- **A `Drafted` row with no cell diff still renders.** The old loop appended a
  chain row only `if cells:` — a `Drafted` row copied byte-identical into the
  snapshot (`intake.py snapshot` copies every registry wholesale, not only
  approved rows) produced an empty diff and was silently dropped. Both
  renderers now show it with a `drafted` state / tag and the reason ("Drafted
  — never approved", or "No cell differs from the approved snapshot… its own
  `Status` asks for a human").
- **Every row dict carries a `drafted: bool`**, independent of `state`
  (`added`/`changed`/`removed`/`current`/`drafted`), so a renderer can say WHY
  a row owes even when its state is `added` because of drift-adjacent timing
  rather than because it is `Drafted`.

**Driven by tests** (`tests/test_gen_open_items.py`,
`tests/test_trace_briefs.py`): a `Drafted` LLR under an `Approved`, undrifted
SR owes and surfaces (`test_drafted_child_under_approved_undrifted_sr_owes`,
`test_reattest_brief_owes_a_drafted_llr_under_an_approved_undrifted_sr`); an
`Approved` LLR under an `Approved` SR does not
(`test_approved_child_under_approved_sr_does_not_owe`,
`test_reattest_brief_stays_silent_for_an_approved_undrifted_chain`); a
`Drafted` row present in the snapshot byte-identical still owes
(`test_drafted_child_unchanged_since_snapshot_still_owes`); and a dynamic
census test asserts, against THIS repo's own live spine (not a literal),
that every unique `(kind, id)` the model marks `drafted` equals the live
`is_drafted` count over `srs + llrs + tcs`
(`test_reattest_model_owed_row_count_matches_the_live_drafted_llr_tc_census`).
Two pre-existing tests were updated rather than left contradicting the fix
they described: `test_empty_attestation_state_names_only_what_it_checked`
(122-REVIEW-A) used to assert the SR-only-scoping caveat text and a fixture
that, post-widening, no longer reaches the vacuous branch at all — repointed
to the truly-vacuous case and the caveat's corrected wording (it used to claim
a chain row reaches this view "through the snapshot-drift arm… and through
nothing else", which the widening makes false).

**The surfaces, before/after, on the live registries (no approval act taken):**

- `docs/open-items.html` —
  before: *"0 pending decision(s) · 1 spine row(s) owing a approval or a
  re-attest, across 1 chain row change(s); 1 row(s) drifted from the approved
  snapshot."*
  after: *"1 pending decision(s) · 10 spine row(s) owing a approval or a
  re-attest, across 20 chain row change(s); 10 row(s) drifted from the
  approved snapshot."*
  (the `1 pending decision(s)` in the after-line is `OI-62`, filed in Act 2
  below — unrelated to the widening itself.)
<!-- fig: cmd="python project-trajectory/scripts/gen_open_items.py --root ." rev=c54ddd10 -->
- `docs/ratify/CURRENT.md` regenerated (`trace.py --approve modified --out
  docs/ratify/CURRENT.md`) against the same widened model; the approval-fresh
  gate demands this on any registry/surface change.
- The ten owing SRs and their twenty chain rows, confirmed by direct
  inspection of `reattest_model`'s output: `SR-070`(2), `SR-146`(1),
  `SR-157`(2), `SR-159`(1, the one pre-existing drift — `LLR-041`, unrelated
  to this widening), `SR-160`(2), `SR-161`(2), `SR-162`(2), `SR-164`(2),
  `SR-168`(4), `SR-177`(2). The nineteen `Drafted` rows the 2026-08-23 sitting
  named (`LLR-187/193/194/196/198/199/200/201/202`,
  `TC-182/188/189/191/192/194/195/196/197/198`) are exactly the nineteen
  `drafted: True` rows in the regenerated model — each appears once, under its
  real owning SR.
<!-- fig: cmd="python -c \"import sys; sys.path.insert(0,'project-trajectory/scripts'); import trace as tr, spine_rules; from pathlib import Path; reg=tr.load_registries(Path('docs')); print(sum(1 for rows in (reg.srs,reg.llrs,reg.tcs) for r in rows if spine_rules.is_drafted(r)))\"" rev=c54ddd10 -->

**Not done, deliberately:** no row's `Status` was flipped. The corrected
brief is what the owner approves FROM next — approving under the OLD,
under-counted brief would have been exactly the laundering the mechanism
exists to prevent, which is why the 2026-08-23 sitting stopped rather than
guessed at a fix.

**Close.** Spec moved to
[../archive/work/complete/WI-513-owes-widening-drafted-chain.md](../archive/work/complete/WI-513-owes-widening-drafted-chain.md),
`specref` cleared, `## Deliverable` filled before `## Context`.

### Act 2 — `OI-62` filed: the (b) go/no-go, pending

A pending brief in the house form, at
`docs/requirements/open-items.toml#OI-62`. `wi_refs` unset (no ruling yet).

**THE NUMBER**, quoted from `WI-512`'s close
(`docs/log.d/2026-08-24-wi512-contract-generalization.md`): the 27 CLI-family
`contract` cells thinned from 7,385 to 2,613 characters (−64.6%); of the
survivors, 908 characters over 11 of the 27 rows is the irreducible remainder
— **87.7% of the family's prose was restatement, 12.3% (908/7,385 characters,
one row in seven, 11/27 rows) was not.** Alongside it, (d)'s named-symbol
tripwire is live and reporting **7 findings over 5 rows** (`IF-055` real rot,
`IF-038`/`IF-072`/`IF-061`/`IF-132`/`IF-143` judgement calls), none of them
among the 27 rows the pass touched.

**Options carried, each FOR/AGAINST:** (a) proceed now as one 108-row campaign
row; (b) proceed in tranches by row family (non-CLI `Provides` first, then
`Consumes`); (c) hold until the 7 tripwire findings are triaged; (d) decline —
the CLI family was the outlier (provably uniform, single boundary tie), not
necessarily representative of the other 108 rows.

**Recommendation, shaped honestly** (the WI-512 close's own reading: "(b) is
worth running… because one row in seven carried something real" — a
recommendation to run it, not a claim about how much it will find): lean (b),
tranched by row family, because the measured 40.7% keep-rate is over a
UNIFORM population and the honest way to learn whether it generalizes to a
heterogeneous one is to re-measure on the next tranche rather than commit all
108 rows to one pass on an extrapolated number. Fold the 5 ambiguous tripwire
findings' triage into the first tranche rather than gating on them
separately — the finding list is already fully enumerated and does not sharpen
by waiting.

### Gates

- `python -m pytest -q -n auto -m smoke` → **1321 passed, 5 skipped in
  21.76s**; `check_smoke_budget.py --mode enforce` re-ran it standalone at
  **26.34s, 26.7s vs 60s budget → within**.
- `check_docs.py --root . --stale` → 1055 docs, 1376 links, **0 broken** (pre-
  existing "possibly stale" hints on unrelated archived docs, none of them
  touched here).
- `check_trajectory.py --root . --strict` → clean, exit 0 (pre-existing WARNs
  only — the 4 `SR-163`/`SR-181` orphans, the `LLR-197` provenance finding,
  none introduced here).
- `trace.py --root . --strict-integrity` → `SN=27 SR=75 LLR=184 TC=181
  orphans=4 integrity=0 drafts=19 interface-findings=0
  provenance-findings=1` — unchanged from HEAD; the widening touches
  attestation rendering, not the integrity/orphan rules.
- `python -m pytest -q -n auto --basetemp=D:\pytest-tmp-owes` → **3010
  passed, 14 skipped in 1013.27s (0:16:53)**.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=c54ddd10 -->
<!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-owes" rev=c54ddd10 -->

**Two ratchets re-stamped, both reviewed bumps, reasons recorded in their own
entries:** `tests/test_module_size_ratchet.py` (`trace.py` 5553 → 5621, +68 —
the chain-wide `Drafted` arm, the re-signatured `_entry_kind`, the `drafted`
flag threaded through every row branch, and the markdown renderer's new
`"drafted"` state arm) and `tests/test_complexity_ratchet.py` (`trace.py:
reattest_model` 18 → 19, one new branch; `trace.py:reattest_lines` NEW entry
at 11, the same `"drafted"`-state branch crossing the threshold in the
renderer). `tests/test_generated_newlines.py`'s pinned LF-write site in
`gen_open_items.py` moved 1156 → 1183 (comment updated, not just the number —
churn from code added above the site, not a new site). `docs/id-watermark`
re-stamped via `trace.py --bump-ids` (`WI 512 -> 513`, `OI 61 -> 62`). One
R-D catch, fixed rather than worked around: `check_trajectory.py --strict`
refused a first draft of the `docs/status.md` bullet for naming `WI-513` by
id after its close (status.md is forward-only; a closed WI's id is history) —
reworded to describe the act without the token.
