## 2026-08-01 — WI-378: the verdict-freshness loop, measured — documentation only

**One line:** the row was scoped to *measure first and possibly deliver nothing
else*, and that is what it delivered — replaying `integrate._verdict_gate`'s
predicate over **every** merge it has governed found the gate is mostly firing
**correctly**, so the fail-closed gate ships unweakened and what lands is the
ordering that shrinks the avoidable class.

**The population, derived rather than chosen.** The first pass censused the four
branches the session brief named; REVIEW-A round 1 was right that this is a
sample, not a population, and the corrected numbers below supersede it. The
predicate has governed every merge since the freshness comparison landed with
`integrate.py` (`git log --reverse -S"_verdict_gate" -- .../integrate.py` →
`e1cf5743`, plus `37dfa9ee`, WI-386's peel, which only loosens it), and
`docs/review-policy` has read `1` since `274c64be`. So:

```
git log --format="%H%x09%s" --grep="^integrate: merge"     # 20 merges
git merge-base --is-ancestor e1cf5743 <merge>              # true for all 20
```

**The measurement.** `_verdict_gate` refuses when the APPROVE's last commit is
older than the branch's last commit outside `docs/reviews/` and `docs/log.d/`.
Replayed over all 20 by walking each branch's own first-parent commits,
classifying the paths each touches, and attributing every extra round to the
commit(s) that staled the APPROVE before it (a CHANGES-REQUESTED round does not
count — more work was coming regardless). **Thirteen staled nothing; these
seven account for all 13 stalings** (13 + 7 = 20).

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

**13 staled APPROVEs: nine the gate working** (a real change to shipping code or
a declared doc — the verdict genuinely no longer described the tree), **one
trunk moving under an open branch** (WI-280's firing #2, now structurally
covered: `_verdict_gate` measures code-time at `_work_tip`, which peels the
attested `refresh:` commit, and under WI-386's station protocol the lane does
not hand-merge trunk at all), and **three a record edit that followed its own
verdict** — WI-280's close ceremony, WI-380's mutation-ledger correction and
WI-371's `Deliverable` prose fix. Those three, **3 of 13 (23.1 %)**, are what an
exclusion of `docs/work/` would have suppressed; recomputing WI-380's
`code_time` with `docs/work/` excluded gives `1785563826` against a
`verdict_time` of `1785564586`, i.e. it would have passed.

**Three corrections to the record**, the first two found by the replay and the
third by the reviewer:

1. WI-280's firing #1 was **not** caused by the ratifying spine commits. `8311c75`
   carried `docs/reviews/WI-280-REVIEW-A.md` in the same commit as the flip, so
   `verdict_time == code_time` and the strict `<` let it pass. The close
   ceremony `99a0596` — `docs/work/` only — is what refused.
2. The session's working belief was that the `docs/work/` limb cost four rounds
   (WI-380 r3, WI-384 r4–r5, WI-386 r5). Measured, *within those four branches*
   it cost **one**: WI-384's rounds 4 and 5 were staled by
   `docs/declared-absences` and `check_doc_refs.py`, WI-386's round 5 by
   `tests/test_wi_convert.py`. Those commits touch `docs/work/` too, but
   excluding it suppresses none of them.
3. **This WI's own first census was wrong about its population** — four branches
   where the predicate had governed 20 — and stated a *universal* over that
   sample ("the only two an exclusion would have suppressed"), which WI-371's
   `17d70468` falsifies. It is the same defect one level up from the two figures
   this row had already refused to inherit, and it is exactly what WI-392 exists
   to catch: the command that derives the population would have enumerated 20.
   The correction makes the decision **better** supported, not worse — the added
   case is a `Deliverable` prose fix, the precise field this row argues a
   reviewer must re-read after an APPROVE.

4. **And the correction itself carried an underived figure.** The round-1 fix
   restated the census as "Twelve staled nothing; these seven" — 12 + 7 = 19
   against a population of 20; it is **thirteen**. Nobody re-derived a number
   that fell out of a number they had just re-derived. It is worth recording
   plainly rather than quietly fixing: this is the third occurrence of one
   defect class in one row — a brief's figures (refused), a brief's population
   (inherited), and now a restatement of my own corrected population — and the
   third happened *while writing the paragraph explaining the second*. That is
   the strongest argument available for what WI-392 is meant to build, and it
   is why that row's constraint now sits in its Done-when rather than only in
   its prose.

**The figure after this row's own advice is taken: 2 of 11 (18.2 %).** The two
ordering rules retire both of WI-280's stalings — the close ceremony by closing
first, the hand trunk merge by never hand-merging — leaving 11, of which the
exclusion buys back 2, and both of those rounds caught a false claim in the
record. REVIEW-A round 2 derived that, having disclosed that finding the
population error gave it an interest in the opposite conclusion; the ratio moved
0.9 points on a 44 % change in denominator, so the decision never rested on the
denominator, and the composition moved *against* the exclusion.

**WI-380 contributed zero to this count, as expected** — none of the 13 came
from a spurious re-attest window. The ratified/traced split acts upstream, on
how often a window opens at all, which is exactly why this row was told to
measure rather than to assume.

**Deliverables.**

- [`project-trajectory/PROCESS_OPTIONS.md`](../../project-trajectory/PROCESS_OPTIONS.md),
  "The LLM-gate verdict protocol" — the freshness rule, the census plus the
  command that derives its population, the two ordering rules (**close before
  the final verdict round**; **never hand-merge trunk on a work branch**) stated
  as *necessary but not sufficient*, and that `docs/work/` is deliberately
  inside the window.
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

**Deliberately not built.** Option (b), widening the exclusion: it buys back
**3 of 13** rounds (23.1 %) and lets a spec's `safety_class`, `needs` and
`Deliverable` change after the APPROVE unseen. Two of the three settle it —
WI-380's round 3 paid for a correction carrying a *newly driven* figure nobody
else had checked, and WI-371's paid for a `Deliverable` prose fix, so the
exclusion would have shipped un-reviewed evidence in one case and an un-reviewed
shipped claim in the other. Option (c) is unnecessary for the same reason. Also
**not filed**: capping a record-only review round (WI-386's reviewer's proposal,
bias disclosed by him) — the class is 3 of 13 (23.1 %) and **two of those three
rounds caught a false claim**, which is the argument against capping them; its
durable half became WI-392 instead.

**Ordering is necessary, not sufficient — at its real strength.** WI-380, WI-384
and WI-386 all closed — spec moved, `Deliverable` filled — *before* their round-1
verdict this session, and no close ceremony staled an APPROVE on any of them;
that was worth writing down, since the class cost WI-280 a round and lived only
in its log. But an earlier draft here read that as "zero close-ceremony
stalings", which is literally true and **masked, not clean**. WI-384's
`dba18f2a` and WI-386's `1329bd4e` *are* post-APPROVE record edits inside
staling windows, costing nothing only because a code change shared the window;
and **WI-371 closed before its verdict and still bought a record-only round**,
because its round-1 APPROVE carried the MINOR that forced the `Deliverable`
fix — a finding that did not exist when the close was made. Ordering removes the
anticipatable half of the class and no more.

**Deviations from spec:** none in scope. The spec's Done-when box "This spec is
archived to `docs/archive/specs/`" is met
([`docs/archive/specs/WI-378.2026-08-01.md`](../archive/specs/WI-378.2026-08-01.md),
with the firing-#1 correction noted at its head).

**Byte deltas:** `AGENTS.template.md` 9,991 → 9,991 (unchanged; 9 bytes of
headroom under 10,000). `PROCESS.md` 64,319 → 64,319 (unchanged).
`PROCESS_OPTIONS.md` 164,003 → **166,314** (+2,311 — the verdict-freshness
paragraph, grown at REVIEW-A round 1 by the derived population, its command and
the necessary-not-sufficient qualifier, and at round 2 by the post-ordering
2-in-11 figure). The `byte-budget-guard` baseline is
re-stamped to 166,314 and now records that **+846 of the +3,157 gap to the old
163,157 stamp was inherited unstamped** — attributed at round 1 to
"WI-380/384/386", which the reviewer refuted and the file sizes settle: 163,157
at the wi-380 merge, 164,003 at wi-384, 164,003 at wi-386, so WI-380 and WI-386
moved this file by **0 bytes and the whole +846 is WI-384's**. That is the
silent growth the skill exists to catch.

**Tests.** The full suite was driven **four times** across the row — twice before
REVIEW-A round 1, once after its corrections, once after round 2's — reading
`1 failed, 1744 passed, 12 skipped` every time (331.63 s / 344.97 s / 409.43 s /
446.85 s; wall varies with sibling worktrees, the counts do not). The reviewer
independently reproduced the same counts. `pytest -q -n auto -m smoke` →
`1 failed, 560 passed, 4 skipped`, run six times with stable counts (wall
12.5–33.0 s). The one red is
`test_check_lane.py::test_this_repo_is_not_a_work_branch`, which asserts the
checkout it runs in holds no `docs/work/active/<branch>/` claim — false by
construction in a lane worktree, so it reds on every claimed branch and is not
this row's. It is **not** a permanent standing red: it is fixed on trunk ahead
of this branch (`5f292892`) and clears when the lane refreshes.
`ruff check .` → `All checks passed!`; `ruff format --check .` →
`146 files already formatted`; `check_trajectory.py --root . --strict` → `clean
(390 work item(s), 366 done (94%), 16 cancelled, graph acyclic)`;
`check_doc_refs.py --root . --strict` → `OK - no dangling path or sym:
references`; `check_docs.py --root . --stale` → `OK - 341 doc(s), 974 intra-repo
link(s), 0 broken` (341 rather than the 340 recorded at round 1: the verdict
file itself is now on the branch).
