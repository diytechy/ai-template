## 2026-08-01 — WI-378: the verdict-freshness loop, measured — documentation only

**One line:** the row was scoped to *measure first and possibly deliver nothing
else*, and that is what it delivered — replaying `integrate._verdict_gate`'s
predicate over the four merged branches that exercised it found the gate is
mostly firing **correctly**, so the fail-closed gate ships unweakened and what
lands is the ordering that retires the avoidable class for free.

**The measurement.** `_verdict_gate` refuses when the APPROVE's last commit is
older than the branch's last commit outside `docs/reviews/` and `docs/log.d/`.
Replayed by walking each branch's own first-parent commits, classifying the
paths each touches, and attributing every extra round to the commit(s) that
staled the APPROVE before it (a CHANGES-REQUESTED round does not count — more
work was coming regardless):

| Branch | rounds | APPROVEs staled | what staled them |
|---|---|---|---|
| WI-280 (`0fc58fb`) | 4 | 2 | `99a0596` close ceremony (`docs/work/` only); `ad2541d` hand trunk merge |
| WI-380 (`8c4d5f7`) | 3 | 1 | `c42e370` mutation-ledger correction (`docs/log.d/` + `docs/work/` only) |
| WI-384 (`979d8e0`) | 5 | 3 | `ADOPTING.md` + a queued spec; `docs/declared-absences`; `check_doc_refs.py` |
| WI-386 (`c2a9af1`) | 5 | 3 | `integrate.py` + tests, twice; `tests/test_wi_convert.py` |

**Nine staled APPROVEs: six the gate working** (a real change to shipping code
or a declared doc — the verdict genuinely no longer described the tree), **one
trunk moving under an open branch** (WI-280's firing #2, now structurally
covered: `_verdict_gate` measures code-time at `_work_tip`, which peels the
attested `refresh:` commit, and under WI-386's station protocol the lane does
not hand-merge trunk at all), and **two a record edit that followed its own
verdict** — WI-280's close ceremony and WI-380's mutation-ledger correction.
Those two are the *only* ones an exclusion of `docs/work/` would have
suppressed; recomputing WI-380's `code_time` with `docs/work/` excluded gives
`1785563826` against a `verdict_time` of `1785564586`, i.e. it would have
passed.

**Two corrections to the record the row inherited**, both found by the replay:

1. WI-280's firing #1 was **not** caused by the ratifying spine commits. `8311c75`
   carried `docs/reviews/WI-280-REVIEW-A.md` in the same commit as the flip, so
   `verdict_time == code_time` and the strict `<` let it pass. The close
   ceremony `99a0596` — `docs/work/` only — is what refused.
2. The session's working belief was that the `docs/work/` limb cost four rounds
   (WI-380 r3, WI-384 r4–r5, WI-386 r5). Measured, it cost **one**: WI-384's
   rounds 4 and 5 were staled by `docs/declared-absences` and
   `check_doc_refs.py`, WI-386's round 5 by `tests/test_wi_convert.py`. Those
   commits touch `docs/work/` too, but excluding it suppresses none of them.

**WI-380 contributed zero to this count, as expected** — none of the nine came
from a spurious re-attest window. The ratified/traced split acts upstream, on
how often a window opens at all, which is exactly why this row was told to
measure rather than to assume.

**Deliverables.**

- [`project-trajectory/PROCESS_OPTIONS.md`](../../project-trajectory/PROCESS_OPTIONS.md),
  "The LLM-gate verdict protocol" — the freshness rule, the census, the two
  ordering rules (**close before the final verdict round**; **never hand-merge
  trunk on a work branch**), and that `docs/work/` is deliberately inside the
  window.
- [`project-trajectory/skills/session-protocol/SKILL.md`](../../project-trajectory/skills/session-protocol/SKILL.md)
  §4 (+ both materialized copies) — the same ordering as an operational bullet
  where a closing session meets it, linking rather than restating.
- [`project-trajectory/scripts/integrate.py`](../../project-trajectory/scripts/integrate.py)
  `_verdict_gate` docstring — **no behaviour change**; the reason `docs/work/`
  is excluded from the exclusion, with the numbers, recorded at the predicate a
  successor would edit, plus why `docs/log.d/` is genuinely different.
- **WI-392 filed** ([`docs/specs/WI-392.md`](../specs/WI-392.md)) — a driven
  figure carries the command and revision that produced it, and a check verifies
  that provenance. Three false figures landed in this one session's records
  (WI-380's `2 failed, 7 passed`, WI-391's `109 links`, WI-384's self-falsifying
  "two false positives"); two cost a full review round.

**Deliberately not built.** Option (b), widening the exclusion: it buys back 2
of 9 rounds and lets a spec's `safety_class`, `needs` and `Deliverable` change
after the APPROVE unseen. WI-380's round 3 settles it — the correction that
round paid for carried a *newly driven* figure nobody else had checked, so the
exclusion would have shipped un-reviewed evidence. Option (c) is unnecessary for
the same reason. Also **not filed**: capping a record-only review round (WI-386's
reviewer's proposal, bias disclosed by him) — the class is 2 of 9, so it
addresses ~22 % of the cost while weakening a fail-closed gate; its durable half
became WI-392 instead.

**Evidence the ordering is the remedy, not a consolation.** WI-380, WI-384 and
WI-386 all closed — spec moved, `Deliverable` filled — *before* their round-1
verdict this session, and **zero close-ceremony stalings resulted**. The class
that cost WI-280 a round disappeared with no gate change. It was tribal
knowledge from WI-280's log until now.

**Deviations from spec:** none in scope. The spec's Done-when box "This spec is
archived to `docs/archive/specs/`" is met
([`docs/archive/specs/WI-378.2026-08-01.md`](../archive/specs/WI-378.2026-08-01.md),
with the firing-#1 correction noted at its head).

**Byte deltas:** `AGENTS.template.md` 9,991 → 9,991 (unchanged; 9 bytes of
headroom under 10,000). `PROCESS.md` 64,319 → 64,319 (unchanged).
`PROCESS_OPTIONS.md` 164,003 → **165,557** (+1,554 — the verdict-freshness
paragraph). The `byte-budget-guard` baseline is re-stamped to 165,557 and now
records that **+846 of the +2,400 gap to the old 163,157 stamp was inherited
unstamped** from WI-380/384/386, which is the silent growth the skill exists to
catch.

**Tests** (all driven at this fragment's own revision, so the counts include it):
`pytest -q -n auto -m smoke` → `1 failed, 560 passed, 4 skipped in 24.23s`
(counts stable across three runs this session; wall time 12.5–24.2 s); full
`pytest -q -n auto` → `1 failed, 1744 passed, 12 skipped in 331.63s (0:05:31)`.
The one red is the standing
`test_check_lane.py::test_this_repo_is_not_a_work_branch` (this checkout *is* a
work branch). `ruff check .` → `All checks passed!`; `ruff format --check .` →
`146 files already formatted`; `check_trajectory.py --root . --strict` → `clean
(390 work item(s), 366 done (94%), 16 cancelled, graph acyclic)`;
`check_doc_refs.py --root . --strict` → `OK - no dangling path or sym:
references`; `check_docs.py --root . --stale` → `OK - 340 doc(s), 974 intra-repo
link(s), 0 broken`.
