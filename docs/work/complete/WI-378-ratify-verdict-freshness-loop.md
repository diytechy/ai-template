+++
id = "WI-378"
title = "Resolve the ratification/verdict-freshness loop: under gate-policy `autonomous` a reviewer's recorded verdict is what RATIFIES a re-attest window, but performing that ratification is a commit on a non-excluded path, so it immediately stales the verdict that authorized it and the queue refuses. Fired TWICE on WI-280 - the second time on a merge that altered no WI content at all - so the rounds a WI owes are bounded by trunk's commit rate, not its own risk. REFRAMED 2026-07-31 by owner direction and now DEPENDS on the concurrency-v2 design: with spine WIs serialised (WI-381) and the amendment detector corrected to ignore traced-not-ratified cells (WI-380), firing 2 cannot happen and most windows never open, so the option that would have weakened the fail-closed gate drops out entirely. What remains is the ordering documentation, which was always free - and possibly nothing else. Do not build before WI-380; measure what still fires first. The considered-and-set-aside options are kept in the spec as the record."
workstream = "process"
needs = ["WI-380"]
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

**Documentation only, and the measurement is the deliverable.** The row was
scoped to measure first and it measured: the freshness gate mostly fires
*correctly*, the class worth removing is small and removable by ordering rather
than by exclusion, and so `integrate._verdict_gate` ships **unchanged in
behaviour**. Three text changes and one filed row.

### The measurement (driven 2026-08-01)

`_verdict_gate`'s predicate — *the APPROVE's last commit must be no older than
the branch's last commit outside `docs/reviews/` and `docs/log.d/`* — was
replayed over the four merged branches that exercised it, by walking each
branch's own first-parent commits, classifying the paths each touches, and
attributing every extra review round to the commit(s) that staled the APPROVE
before it. A round only counts if the verdict it invalidated was an **APPROVE**;
a CHANGES-REQUESTED round was going to be followed by more work regardless.

| Branch | rounds | APPROVEs staled | what staled them |
|---|---|---|---|
| WI-280 (`0fc58fb`) | 4 | 2 | `99a0596` close ceremony (`docs/work/` only); `ad2541d` hand trunk merge |
| WI-380 (`8c4d5f7`) | 3 | 1 | `c42e370` mutation-ledger correction (`docs/log.d/` + `docs/work/` only) |
| WI-384 (`979d8e0`) | 5 | 3 | `ADOPTING.md` + a queued spec; `docs/declared-absences`; `check_doc_refs.py` |
| WI-386 (`c2a9af1`) | 5 | 3 | `integrate.py` + tests, twice; `tests/test_wi_convert.py` |

**Nine staled APPROVEs. The census:**

- **6 — the gate working.** WI-384 ×3 and WI-386 ×3, each window containing a
  real change to shipping code or a declared doc. The verdict genuinely no
  longer described the tree; re-reviewing is the point.
- **1 — trunk moving under an open branch.** WI-280's `ad2541d` (the row's
  "firing #2"). WI-384 and WI-386 also hand-merged trunk, but both windows
  already held real code changes, so the merge was not load-bearing for the
  refusal. **Structurally covered going forward** by WI-386's station protocol:
  `_verdict_gate` measures code-time at `_work_tip`, which peels the attested
  `refresh:` commit — and the lane no longer hand-merges trunk at all.
- **2 — a record edit that followed its own verdict.** WI-280's close ceremony
  and WI-380's mutation-ledger correction. These are the only two an exclusion
  of `docs/work/` would have suppressed (verified: every staling commit in both
  windows touches nothing outside `docs/work/` + `docs/log.d/`; recomputing
  WI-380's `code_time` with `docs/work/` excluded gives `1785563826` against a
  `verdict_time` of `1785564586`, i.e. it would have passed).

**Two corrections to the record this row inherited.**

1. The spec's firing-#1 narrative said the ratifying flip and the close ceremony
   were "real spine commits". Only the close ceremony was load-bearing:
   `8311c75` carried `docs/reviews/WI-280-REVIEW-A.md` *in the same commit* as
   the flip, so `verdict_time == code_time` and the predicate (strict `<`) let
   it pass. `99a0596`, touching `docs/work/` only, is what refused.
2. The session brief attributed the `docs/work/` limb to WI-380 round 3, WI-384
   rounds 4–5 and WI-386 round 5 — four rounds. Measured, it is **one**: WI-384
   rounds 4 and 5 were staled by `docs/declared-absences` and
   `check_doc_refs.py`, WI-386 round 5 by `tests/test_wi_convert.py`. Those
   commits also touch `docs/work/`, but excluding it would not have suppressed
   any of them.

**WI-380's contribution to this count is zero, and that is the expected shape.**
None of the nine stalings came from a spurious re-attest window; the
ratified/traced split acts upstream, on how often a window opens at all.

### What was built, and what deliberately was not

- **`PROCESS_OPTIONS.md`, "The LLM-gate verdict protocol"** — a new paragraph
  stating the freshness rule, the two ordering rules that retire the avoidable
  class for free (**close before the final verdict round**; **never hand-merge
  trunk on a work branch**), the census above, and that `docs/work/` is
  deliberately inside the window.
- **The `session-protocol` skill, §4** — the same ordering as an operational
  bullet, where a closing session actually meets it, linking rather than
  restating the rule.
- **`integrate._verdict_gate`'s docstring** — the reason `docs/work/` is not
  excluded, recorded at the predicate a successor would edit, with the numbers.
  **No behaviour change**; `docs/log.d/`'s different treatment is explained in
  the same place.
- **NOT built: option (b), widening the exclusion.** It buys back 2 of 9 rounds
  (1 of 7 after the ordering was adopted) and costs a real hole: a spec's
  `safety_class`, `needs` and `Deliverable` could then change after the APPROVE,
  unseen. WI-380's round 3 is the case that settles it — the correction it
  bought a round for carried a *newly driven* figure nobody else had checked, so
  the exclusion would have shipped un-reviewed evidence.
- **NOT built: option (c).** Unnecessary for the same reason, as the reframing
  predicted.
- **NOT filed: capping a record-only review round** (WI-386's reviewer's
  proposal, bias disclosed). The class is 2 of 9; capping it addresses ~22 % of
  the cost while weakening a fail-closed gate. Its durable half — making the
  class cheap — was filed instead.
- **FILED: WI-392** (`docs/specs/WI-392.md`) — a driven figure carries the
  command and revision that produced it, and a check verifies that provenance.
  Three false figures in this one session (WI-380's `2 failed, 7 passed`,
  WI-391's `109 links`, WI-384's self-falsifying "two false positives") were
  caught by reviewers rather than by machine, and two of them cost a full round.

### Evidence that ordering is the right remedy

The close-before-verdict ordering was adopted informally during the 2026-08-01
session: WI-380, WI-384 and WI-386 all closed (spec moved, `Deliverable` filled)
*before* their round-1 verdict. **Zero close-ceremony stalings resulted** — the
class that cost WI-280 a round disappeared without any gate change. It was
tribal knowledge from WI-280's log until this row; now it is written where a
session reads it.
