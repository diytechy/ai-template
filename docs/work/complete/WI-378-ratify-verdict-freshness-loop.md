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

### The measurement (driven 2026-08-01; corrected at REVIEW-A round 1)

**The population is derived, not chosen** — this is the correction REVIEW-A
round 1 forced, and it is the row's own filed defect class (WI-392) one level
up: the first pass censused the four branches the session brief named, which is
a figure inherited rather than re-derived. The predicate has governed **every**
merge since the freshness comparison landed with `integrate.py`
(`git log --reverse -S"_verdict_gate" -- project-trajectory/scripts/integrate.py`
→ `e1cf5743`, and `37dfa9ee`, WI-386's peel, which only loosens it), and
`docs/review-policy` has read `1` since `274c64be`. So the population is:

```
git log --format="%H%x09%s" --grep="^integrate: merge"     # 20 merges
git merge-base --is-ancestor e1cf5743 <merge>              # true for all 20
```

`_verdict_gate`'s predicate — *the APPROVE's last commit must be no older than
the branch's last commit outside `docs/reviews/` and `docs/log.d/`* — was
replayed over all **20**, by walking each branch's own first-parent commits,
classifying the paths each touches, and attributing every extra review round to
the commit(s) that staled the APPROVE before it. A round only counts if the
verdict it invalidated was an **APPROVE**; a CHANGES-REQUESTED round was going
to be followed by more work regardless. **Thirteen of the 20 staled nothing;
these seven account for all 13 stalings** (13 + 7 = 20).

The `rounds` column counts **commits touching `docs/reviews/WI-<n>-REVIEW-A.md`** on the branch, which is what the predicate itself reads. It *undercounts* narrative rounds whenever one commit carried more than one round's verdict — WI-277 records three rounds in a file only two commits touched, and WI-280's rounds 1–2 both arrived in `8311c75`, the commit that also carried the ratify.

| Branch | rounds | APPROVEs staled | what staled them |
|---|---|---|---|
| WI-386 (`c2a9af1`) | 5 | 3 | `integrate.py` + tests, twice; `tests/test_wi_convert.py` |
| WI-384 (`979d8e0`) | 5 | 3 | `ADOPTING.md` + a queued spec; `docs/declared-absences`; `check_doc_refs.py` |
| WI-380 (`8c4d5f7`) | 3 | 1 | `c42e370` mutation-ledger correction (`docs/log.d/` + `docs/work/` only) |
| WI-374 (`8ffc6f8`) | 3 | 2 | `drive.py`; the LLR + TC registries |
| WI-277 (`8bde0a6`) | 2 | 1 | nine commits — a trunk merge plus six test-split slices |
| WI-371 (`4073a6d`) | 2 | 1 | `17d70468` `Deliverable` prose fix (`docs/work/` only) |
| WI-280 (`0fc58fb`) | 3 | 2 | `99a0596` close ceremony (`docs/work/` only); `ad2541d` hand trunk merge |

**13 staled APPROVEs. The census:**

- **9 — the gate working.** Each window contained a real change to shipping code
  or a declared doc. The verdict genuinely no longer described the tree;
  re-reviewing is the point.
- **1 — trunk moving under an open branch.** WI-280's `ad2541d` (the row's
  "firing #2"). WI-384, WI-386 and WI-277 also hand-merged trunk, but each of
  those windows already held real code changes, so the merge was not
  load-bearing for the refusal. **Structurally covered going forward** by
  WI-386's station protocol: `_verdict_gate` measures code-time at `_work_tip`,
  which peels the attested `refresh:` commit — and the lane no longer hand-merges
  trunk at all.
- **3 — a record edit that followed its own verdict.** WI-280's close ceremony,
  WI-380's mutation-ledger correction, and WI-371's `Deliverable` prose fix.
  These are the three an exclusion of `docs/work/` would have suppressed —
  **3 of 13, 23.1 %** (verified: every staling commit in those three windows
  touches nothing outside `docs/work/` + `docs/log.d/`; recomputing WI-380's
  `code_time` with `docs/work/` excluded gives `1785563826` against a
  `verdict_time` of `1785564586`, i.e. it would have passed).

**And 3-in-13 is the figure before this row's own advice is taken.** The two
ordering rules retire *both* of WI-280's stalings — the close ceremony by
closing first, the hand trunk merge by never hand-merging — leaving **11**, of
which the exclusion would buy back **2: 18.2 %**. That is the number describing
the world a successor actually lives in, and both of those two rounds caught a
false claim in the record (WI-380's stale mutation ledger, WI-371's `Deliverable`
naming a gitignored path). Credit where due: REVIEW-A round 2 derived this,
having disclosed that finding the population error gave it an interest in the
opposite conclusion — the ratio moved 0.9 points on a 44 % change in
denominator, so the decision never rested on the denominator, and the
*composition* moved against the exclusion.

**Three corrections to the record this row inherited.**

1. The spec's firing-#1 narrative said the ratifying flip and the close ceremony
   were "real spine commits". Only the close ceremony was load-bearing:
   `8311c75` carried `docs/reviews/WI-280-REVIEW-A.md` *in the same commit* as
   the flip, so `verdict_time == code_time` and the predicate (strict `<`) let
   it pass. `99a0596`, touching `docs/work/` only, is what refused.
2. The session brief attributed the `docs/work/` limb to WI-380 round 3, WI-384
   rounds 4–5 and WI-386 round 5 — four rounds. Measured, **within those four
   branches** it is **one**: WI-384 rounds 4 and 5 were staled by
   `docs/declared-absences` and `check_doc_refs.py`, WI-386 round 5 by
   `tests/test_wi_convert.py`. Those commits also touch `docs/work/`, but
   excluding it would not have suppressed any of them.
3. **My own first pass was wrong about the population**, and the reviewer caught
   it. Censusing four branches, I wrote "these are the *only* two an exclusion
   would have suppressed" — a universal claim over a sample. WI-371's
   `17d70468` falsifies it. The corrected figure is 3 of 13, and it makes the
   decision *better* supported, not worse: the added case is a **`Deliverable`
   prose fix** — precisely the field this row argues a reviewer must re-read
   after an APPROVE.

**WI-380's contribution to this count is zero, and that is the expected shape.**
None of the 13 stalings came from a spurious re-attest window; the
ratified/traced split acts upstream, on how often a window opens at all.

### What was built, and what deliberately was not

- **`PROCESS_OPTIONS.md`, "The LLM-gate verdict protocol"** — a new paragraph
  stating the freshness rule, the two ordering rules (**close before the final
  verdict round**; **never hand-merge trunk on a work branch**) as *necessary
  but not sufficient*, the census above with the command that derives its
  population, and that `docs/work/` is deliberately inside the window.
- **The `session-protocol` skill, §4** — the same ordering as an operational
  bullet, where a closing session actually meets it, linking rather than
  restating the rule.
- **`integrate._verdict_gate`'s docstring** — the reason `docs/work/` is not
  excluded, recorded at the predicate a successor would edit, with the numbers.
  **No behaviour change**; `docs/log.d/`'s different treatment is explained in
  the same place.
- **NOT built: option (b), widening the exclusion.** It buys back **3 of 13**
  rounds (23.1 %) and costs a real hole: a spec's `safety_class`, `needs` and
  `Deliverable` could then change after the APPROVE, unseen. Two of the three
  settle it between them — WI-380's round 3 bought a correction carrying a
  *newly driven* figure nobody else had checked, and WI-371's bought a
  `Deliverable` prose fix, so the exclusion would have shipped un-reviewed
  evidence in one case and an un-reviewed shipped claim in the other.
- **NOT built: option (c).** Unnecessary for the same reason, as the reframing
  predicted.
- **NOT filed: capping a record-only review round** (WI-386's reviewer's
  proposal, bias disclosed). The class is 3 of 13; capping it addresses 23.1 %
  of the cost while weakening a fail-closed gate — and two of those three rounds
  caught a false claim, which is the argument against capping them. Its durable
  half — making the class cheap — was filed instead.
- **FILED: WI-392** (`docs/specs/WI-392.md`) — a driven figure carries the
  command and revision that produced it, and a check verifies that provenance.
  Three false figures in this one session (WI-380's `2 failed, 7 passed`,
  WI-391's `109 links`, WI-384's self-falsifying "two false positives") were
  caught by reviewers rather than by machine, and two of them cost a full round.

### Ordering is necessary, not sufficient — stated at its real strength

The close-before-verdict ordering was adopted informally during the 2026-08-01
session: WI-380, WI-384 and WI-386 all closed (spec moved, `Deliverable` filled)
*before* their round-1 verdict, and no close ceremony staled an APPROVE on any
of the three. That was worth writing down — the class that cost WI-280 a round
was tribal knowledge from its log until this row.

But an earlier draft of this Deliverable read that as "zero close-ceremony
stalings", which is literally true and **masked, not clean**, and REVIEW-A round
1 was right to say so. Two things it hid:

- WI-384's `dba18f2a` and WI-386's `1329bd4e` **are** post-APPROVE record edits
  sitting inside staling windows. They cost nothing only because a code change
  shared the window and would have bought the round anyway.
- **WI-371 closed before its verdict and still bought a record-only round.** Its
  round-1 APPROVE carried a MINOR; fixing it meant editing the `Deliverable`
  (`17d70468`), which no ordering could have placed earlier because the finding
  did not exist yet.

So ordering removes the *anticipatable* half of the class and nothing more. The
irreducible remainder is a verdict demanding a record change — and that round is
the gate working, since two of the three record-only rounds in the census caught
a false claim.
