# WI-542 adjudication (002) — the close of WI-521 (lane wi521-decomposition-debt-owner)

Independent second pass. The lane closed `WI-521` **partial**, reason "worker
exit 4", and left the keep/discard split explicitly OWED (`split_decided_by =
"adjudicator"`) — correct for a lane whose worker died before it could judge its
own work. A prior adjudication (`001-ADJUDICATE-1058868.md`, commit `9cc57286`)
already ruled PARTIAL / KEEP-all / one successor and drafted that successor in
this row's `## Dispositions`. I re-derived the four answers from the commit range
`efcde754aa..378e90005b`, the review telemetry, and the live tree — not from
either report's prose — and I **concur**. The disposition already drafted at 001
stands; I do **not** duplicate it (a second block would double-mint a standing
debt owner).

## 1 — Is the claimed outcome right? YES, PARTIAL.

`WI-521` is a **standing debt owner** by its own scope ("THIS ROW IS A STANDING
DEBT OWNER … closed only when the debt below is paid or re-homed"). Slice 3 — the
IF-seam tier of `test_trace.py` split to `tests/test_trace_interfaces.py` —
landed clean, and substantial debt remains. So the close is neither COMPLETE (the
debt is not paid) nor CANCELLED (real, verified work survives on trunk). PARTIAL
is right.

Independently verified the slice is clean, not merely claimed clean:
- **Node-id set equality** vs the pre-split file at `56e7e52b`: 92 collected ids
  each side, empty symmetric difference — nothing renamed, dropped or merged.
- **Sizes match the record**: `test_trace.py` 1370, `test_trace_interfaces.py`
  978 (was 2323 pre-split); the two untouched monoliths `test_trajectory_arch.py`
  2290 and `test_agent_loop.py` 1640 stand.
- **Green**: `pytest tests/test_trace.py tests/test_trace_interfaces.py` exits 0
  on trunk.
- **Spine clean**: `check_trajectory.py --strict` exits 0; every WARN is
  pre-existing and unrelated to the split (gen_trajectory/pending CodeSymbol
  warns, shared-spec-of-record warns on other open WIs, the SR-181 orphan owned
  elsewhere).

## 2 — Is the keep/discard split honest? It was OWED; I decide it: KEEP ALL, DISCARD NONE.

The build committed (`e3c820cc` BUILD COMMITTED); slice 3's two work commits
(`c9203f47` split, `adfc1204` full-suite record) are behaviour-preserving by the
node-id-equality proof above and green on trunk. The three REVIEW-A ERROR/TIMEOUT
sessions (002/003/004) are an **external infrastructure failure**, not a defect
in the diff: the Codex reviewer returned "You've hit your usage limit … try again
at 8:34 AM" twice (sessions 002, 004) and the coordinator timed session 003 out
at 7200s after it had already reached full collection (smoke 1384). A review that
never ran is not a review that rejected. Nothing in the range is unsafe — the
remainder is the station refresh (`56e7e52b`), the log fragment, and session
telemetry. Whole range `56e7e52b..378e90005b` is KEEP; discard none.

## 3 — Should a successor exist? YES, one — already drafted at 001; it stands, un-duplicated.

The standing-owner role cannot ride a disposed row: `WI-521`'s spec now lives in
`docs/work/partial/WI-521-decomposition-debt-owner.md` (confirmed) and a closed
row is never revived. The successor in this row's `## Dispositions`
(`supersedes = "WI-521"`) carries the un-paid debt: the three remaining fusion
heads (`agent_loop`, `agent_common`, `bootstrap`), the rest of `check_trajectory`
(4,327 lines, `main` at complexity 24), and M-06's two remaining monoliths
(`test_trajectory_arch.py` 2,290, `test_agent_loop.py` 1,640). It correctly does
NOT carry §3's sensor/axis question — OI-68 re-homed that to `WI-537`/`WI-538` on
2026-08-30. I re-verified that block is accurate and complete; I add nothing to
it, so exactly one successor mints at close.

## 4 — What does the successor cost? buildtier = strong, planmode single.

The remaining heads are the harder ones — `agent_loop` (already decomposed
twice), `agent_common`, `bootstrap`, and `check_trajectory.main` at complexity 24
— each slice re-measuring a blind derivation and touching the spine on module
moves. `strong` (the predecessor's tier) is right. The work is a build
(decomposition slices), not a design fork, so `planmode` stays single.

## Findings

- [MAJOR] the module-size ratchet still names the disposed owner -> `tests/test_module_size_ratchet.py` names `WI-521` as the debt owner (docstring lines 9 and 87 "THE DEBT OWNER … IS `WI-521`", the `"decompose (WI-521)"` finding message at line 2035, and the baseline-entry comments), but `WI-521` is now terminal in `docs/work/partial/` — a growth sensor whose commentary names a terminal item is the exact dead-owner defect this row was filed to make unreachable -> when the machinery mints the drafted successor, move the pointer (docstring, finding message, and baseline-comment references) to the successor id in that same commit, per the rule this row inherited ("if this row closes, move the ratchet pointer in the same commit") -> @owner
- [MINOR] the keep/discard split was empty at close and is resolved here, not by the lane -> a dispatcher closing a crashed worker has no view of the work, so `keep=[]`/`discard=[]` was correctly deferred (`split_decided_by = "adjudicator"`); left unresolved it would leave unjudged commits on trunk, the defect this rung exists to catch -> ruling of record: KEEP all of `56e7e52b..378e90005b`, DISCARD none — slice 3 is independently re-verified behaviour-preserving (node-id set equality, green, `--strict` clean) and the REVIEW-A failures are external infra (Codex usage-limit / 7200s timeout), not code -> @owner
- [MINOR] two adjudications now carry a `WI: WI-542` trailer for one disposition -> this is the independent second pass (002); session 001 already committed a valid verdict and the successor is drafted once in the spec's `## Dispositions` — I confirm it rather than re-author it, so no second successor is introduced -> at WI-542's close mint exactly the one drafted successor; the two verdict files are the recorded reasoning of two passes reaching the same ruling, not two dispositions -> @owner

OUTCOME: PARTIAL successors=1
