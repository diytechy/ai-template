## 2026-09-01 — WI-563 rework: the spot-check verdict re-opened

Round 2 on the WI-563 adjudication lane, driven by the supervisor-drawn verdict
`docs/reviews/wi-563-spot-check-the-clean-close-of/002-REVIEW-A-ef9f326-supervisor.md`
(CHANGES-REQUESTED findings=4). The verdict record stands as written and is not
edited here; this fragment records what the rework did about it.

**The corrected verdict.** The first pass closed WI-563 as "the close STANDS —
no successor". That is withdrawn. The close of WI-552 now reads **STANDS WITH
FINDINGS — successor owed**. Nothing about the WI-552 merge is reversed (a
spot-check finding is a successor row, never a reversal), but the finding is
real: WI-552 arm 5 introduced a live `--strict` ERROR that the first pass did
not detect.

**The missed ERROR.** `project-trajectory/scripts/schedule.py:445` — the lazy
`import trace as _trace` inside `schedule.load_oi_status` — creates an
undeclared cross-component import `scripts/schedule` (CMP-008) ->
`scripts/trace` (CMP-006). `check_trajectory.py --strict` exits 1 on it:

```
check_trajectory: ERROR - cross-component import scripts/schedule (CMP-008) -> scripts/trace (CMP-006) has no declared IF-### seam — declare the interface row in docs/requirements/interfaces.toml or retag the membership, or set docs/process.toml [checks] components_check = false
```

Attribution verified two ways: the import arrives with `b2b06898` ("WI-552 arms
5+6"), and `git show b6e155d3^1:project-trajectory/scripts/schedule.py | grep
'import trace'` finds nothing — trunk immediately before the WI-552 merge has no
such import and no ERROR. Not fixed here: this is an adjudication lane, and the
repair is the successor's work.

**The false Bar claim, withdrawn.** The first pass declared "the environment
here has no pytest toolchain; the spot-check is a read-level attestation" and
skipped the checks on that basis. The claim was wrong — `check_trajectory.py`
needs no pytest, the venv exists, and the station's own refresh trailer at
`ef9f3268` attests `bar PASS (11 steps, tier all)` on this tree — and it is the
direct cause of the miss. Replaced with real output, run in this worktree today:

- `check_trajectory.py --strict` -> exit 1, the single ERROR above (non-strict
  exit 0). That red is the finding, not a defect of this rework.
- `pytest -q -n auto -m smoke` -> 1449 passed, 8 skipped in 22.45s
- `check_smoke_budget.py --mode enforce` -> 20.6s vs 60s budget -> within
- `check_docs.py --root . --stale` -> OK - 1152 doc(s), 1570 intra-repo link(s),
  0 broken (1 orphan warning(s))

**The exits, taken through the kit's own machinery.** Two successors are DRAFTED
in WI-563's `## Dispositions` section (the spec re-opened in
`docs/archive/work/complete/`, `## Deliverable` still ahead of `## Context`,
filename unchanged) for `intake._disposition_drafts` to mint at this row's merge
— a lane never mints a WI or OI id. Draft 1: declare the IF-### seam for the
`schedule -> trace` crossing (or retag membership) and record the strict-ERROR
miss against the WI-552 close. Draft 2 carries an `open_item` cell, so
`intake._inject_open_item` raises a `pending` OI for the human-owed
`intake._SPEC_NEEDS_RE` no-DOTALL ruling and lands that OI id in draft 2's
`needs`, parking it `waiting:open-item-pending` until the owner rules; the two
cosmetic WI-552 leftovers (dead `intake._OI_ID_RE`; the
`check_trajectory.validate` docstring vs the `known_ois=None` coercion) ride the
same row's text. Both blocks parse clean through `intake.parse_dispositions` and
`intake._mint_shape_refusal`.

Deferred open items: none nameable from a lane — the OI is DRAFTED as the `open_item` cell of WI-563's second `## Dispositions` block and is minted with its id at merge by `intake._inject_open_item`; no lane may allocate an OI id.

No product code changed on this lane. Bar: smoke tier + budget + docs (this
rework's declared bar); the full unfiltered suite was deliberately not run.
