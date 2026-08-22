## 2026-08-22 — WI-390: the concurrency-v2 program close finishes its deferred spine amendment, row CLOSES

Deferred open items: none — the row's two banked out-of-tier findings
(`IF-055`'s stale `SCHED_*` constants, `IF-080`'s stale "candidate worktree"
contract text) are recorded in the closed spec's Deliverable as a scope note
for the next interface-registry sweep, not deferred as an owner decision.

**Why.** Slice 1 (2026-08-20) closed three of this row's four surfaces
(connectivity, prose, stamps) and deferred the fourth — the spine amendment
replacing the retired two-intersecting-hoops render's prose in `LLR-056`/
`TC-056` — because amending an `Approved` cell was, at the time, ruled "the
sitting's act, not a builder's" (the `SR-006`/`LLR-014`/`TC-014` precedent).
That ground is superseded: `OI-53` ruled (b) on 2026-08-22
(`docs/log.d/2026-08-22-oi53-54-rule.md`) — a tracked repair row under the
ordinary review round may amend a stale-but-honestly-tagged `Approved` cell,
sanctioned by the `human_ratification_through = "DevStg-Needs"` dial (only
the Needs tier is human-held). `WI-501` executed the first batch under this
ruling the same day; this slice executes WI-390's own deferred cells in the
same dossier form.

**Re-measured today.** `SR-055` does not exist (zero grep hits — confirmed
gone by the unrelated WI-451 tombstone class, as this file's own 2026-08-18b
note already recorded; nothing to amend there). `LLR-056` and `TC-056` are
both live and `Approved`, and both still described the retired render: `.detail`
carried "(A) the intake loop ... (B) the human-decision loop ... two circular
working loops" with a shared `LLM_Agent` hub; `TC-056.method`/`.expected`
specified "two intersecting hoops" and the 6+5=11 edge count. `TC-056.evidence`
already cited only the live station-cycle tests — untouched, per the spec's
own recommendation. A full re-grep for the retired vocabulary
(`single-WI`, `SCHED_`, `candidate worktree`, two-hoop/`LLM_Agent`/11-edge
prose) across every SN/SR/LLR/TC row found no further live carrier in those
four tiers — three other `single-WI` hits (`LLR-131`, `LLR-151`, `TC-145`) use
the term for "one WI's own claim/classification" (contrasted with a *spine
batch*), the current vocabulary, verified clean against `schedule.classify`/
`kind_of` and `integrate.claim` before leaving them untouched. Two genuinely
stale hits turned up in the `Interfaces` tier instead — `IF-055` still names
`SCHED_*` classification constants absent from `schedule.py` (zero grep
hits), and `IF-080` still says "onto a candidate worktree", the exact phrase
slice 1 already fixed in `PROCESS_OPTIONS.md` — both outside this
instruction's SN/SR/LLR/TC scope and outside this row's already-closed
connectivity surface; banked in the closed spec's Deliverable rather than
fixed.

**What shipped.** Two cells amended, full dossier (`row | cell | old | new |
evidence`) in `docs/work/complete/WI-390-concurrency-v2-program-close.md`'s
`## Deliverable`:

- `LLR-056.detail` — replaced the two-loops/`LLM_Agent`-hub framing with the
  station-cycle description: the seven ring stations (Dispatcher tick ->
  Claim -> Lane build -> Station refresh -> Merge slot -> Trunk advance ->
  Intake mint) as one directed closed cycle, the three terminal-outcome cards
  fanning out of Lane build and back into Station refresh. Verified against
  `traj_panels._station_panel` (the shipped render) and
  `tests/test_traj_panels.py::test_process_tab_renders_the_station_cycle` +
  `::test_station_outcomes_derive_from_the_integrator` before writing.
- `TC-056.method`/`.expected` — replaced the two-hoop/11-edge claim with an
  assertion over the same ring: one closed cycle, 13 total edges (6 ring + 3
  fan-out + 3 fan-in + 1 dashed lost-race retry, `data-edge="slot-refresh"`),
  matching the pinning test's own counts exactly.

`intake.py snapshot` refused first, naming exactly the two amended cells as
ratified text with no authorising act in the tree (the expected refusal, not
a defect); re-run as `intake.py snapshot --approves "OI-53 (b), 2026-08-22 --
docs/log.d/2026-08-22-oi53-54-rule.md"` — 7 registry files copied to
`docs/archive/last_approved`, no fabricated warrant.

**Banked findings disposed.** The `gen_arch_map.module_contracts`
Contracts-grammar false-quiet (a negative statement naming the id it denies
is misread as a declaration) had no home outside this spec — given one at
[`docs/enforcement-audit.md`](../enforcement-audit.md), "Findings from this
audit" item 5. The two provide-only-leaf advisories (`scripts/lane`,
`scripts/handback` "declares no Consumes seam") already had a durable home —
`docs/log.md:2989` records the identical `kitlib/station` precedent this
class follows — re-confirmed still live by `check_trajectory.py --strict`;
no new home needed.

**Gates**, real output, Windows, `.venv` Python 3.11.9, `-n auto`:

- `check_trajectory.py --root . --strict`: **identical WARN/FINDING set**
  before and after the two cell edits (87 lines both sides, `diff` empty),
  and identical again after the `--approves` snapshot refresh. After the
  close move (spec to `docs/work/complete/` + regen): WI-390 drops out
  cleanly — no more oversized-title or stale-SpecRef WARN naming it, done
  count 470 -> 471 (507 total, 21 cancelled, graph acyclic), zero new
  findings introduced.
- `trace.py --root . --strict --strict-integrity`: `integrity=0` unchanged
  before/after; zero citation-frame findings from the new prose (no WI/OI/date
  tokens in either cell). `Traceability: SN=27 SR=74 LLR=176 TC=172 orphans=7
  integrity=0 verified-mechanized=71 verified-demonstrated=3
  verified-attested=0 drafts=6 ...`.
- `python -m pytest -q tests/test_module_size_ratchet.py`: **3 passed**.
- `check_stubs.py --root .`: `OK - no source directory at src` — re-confirmed
  vacuously clean here, as slice 1 recorded.
- `python -m pytest -q tests/test_rule_sync.py`: **42 passed**.
- `python -m pytest -q -n auto -m smoke`: **1397 passed, 5 skipped** — 57.19s
  on the pre-close run, 65.87s on the post-close re-run; both within this
  box's already-measured 54.9-64.0s+ range (CLAUDE.md), one machine is one
  data point, not moved by this registry-only change.
- `python project-trajectory/scripts/check_docs.py --root . --stale`: `OK -
  1013 doc(s), 1346 intra-repo link(s), 0 broken` (only pre-existing
  non-blocking staleness hints, none naming this slice's files).
- `python project-trajectory/scripts/trunk_step.py --regen`: `derived-stage
  ok`, `trajectory ok`, `status ok`, `open-items ok` (`okf` skipped — no
  `docs/okf/` in this repo). `docs/stage`'s fingerprint/as-of moved to the
  current commit as expected; `docs/status.md`'s generated frontier block
  drops WI-390 and promotes the next ready WI in its place — the only touch
  to that file, and it is the generated block, not hand prose (grepped: no
  hand-authored `docs/status.md` reference to WI-390 or concurrency-v2
  existed to begin with).

Registry-and-docs-only change (no executable code touched), so the full
unfiltered suite is not owed by CLAUDE.md's own rule; not run.

**Close.** All four surfaces this row owns are now done — (1) the spine
amendment (this slice), (2) connectivity, (3) prose, (4) stamps (slice 1,
2026-08-20). `SpecRef` cleared, spec moved from `docs/work/active/` to
`docs/work/complete/WI-390-concurrency-v2-program-close.md`, the now-empty
`active/wi390-concurrency-v2-program-close/` directory removed.
