## 2026-09-24 — The owner's rulings on the review pack, and Part C filed

An attended owner session that took the
[owner review pack](../plans/2026-09-24-owner-review-pack.md) one item at a
time. Each answer is in its plan's decision table and was committed as it was
given. Documentation and work-registry filing only: no script, test, spine row
or template changed.

**Owner decisions recorded.**

- **Assumption-tier plan §12.1:**
  - **Q16** (pack A1): bundle `system = "operation" | "delivery"`, which
    means the same thing in an adopter's repo; "kit" names the operation frame
    only in this repo's prose.
  - **Q6** (pack A4): rig rows become `[surrogate.SUR-##]` rows; `emulates`
    lists one or more external parties; surrogates for an adopter's own parts
    wait for the design-tier assumption space. Two naming fixes ride with it:
    SR `form` `package-wide` → `cross-cutting`, and the derived evidence ladder
    is the "evidence level", leaving `standing` to validity.
- **Sister plan §5:**
  - **S4** (pack A2): retirement fragments live in `docs/log.d/retired/`,
    which the non-recursive log fold skips.
  - **S2** (pack A3): "design expectation" kept, plus a glossary line;
    "design specification" was weighed and not taken, because "spec" already
    names a work item's scope document.
  - **S11** (pack B1): the direction is an actual single trunk commit per
    work item (option d), with a dedicated plan before any ruling: the claim
    from lane branches, batching, in-lane adjudication in the merge slot,
    rows on held rungs, held partials, the folded mint, kept lane refs, and
    the amendments.
  - **S9** (pack B2): the check keys on the coordinator's recorded session
    phase and range; it runs after each review session and again in the merge
    ladder; a dirty tree fails the draw; the merge ladder makes the final pass
    on build lanes.
  - **S13** (pack B3): every claimable work item has a Done-when written
    before claim; a change to it by merge is flagged.
  - **S6** (pack B4): the checkpoints are work-item merge and release; the
    check is a mechanical hash of each TC's declared inputs, and a due TC
    mints one deduplicated re-judge item.
  - **S3** (pack B5): phased. The sitting adds a provenance column on needs
    and the vision's two headline needs; the census of the remaining prose
    constraints is ruled later.
  - **S8** (pack B6): the OTel GenAI usage names, pinned, in inclusive form,
    with raw usage kept verbatim. OpenInference, the OpenAI/LiteLLM usage
    shape and Langfuse's usage model were not compared, and are noted.
  - **S5** (pack B7): an inner loop using a spine-derived test map; the 41
    tier disagreements become a separate item, priced later.
  - **S14** (pack B7): pursued, re-scoped from cycles to structure. A
    flag-axis count now; duplicated-stage detection is researched and
    validated against past consolidation findings first.

**Work items filed.** Pack Part C's seven defects are WI-605 to WI-611, each
with a Done-when.

**Finding, not fixed (surfaced to the owner).** `intake._bookkeeping_commit`
stages with `git add -A` and restores with `git reset --hard HEAD` on a
refusal. Run from a primary checkout holding the owner's uncommitted edits, it
would commit them into a mint, or discard them. Part C was therefore filed
through intake's own checks, id allocation and spec writer, with explicit
staging instead of that commit.

**Deviations.**

- The seven work items share the pack as their spec of record (R-E needs
  one), so `check_trajectory.py --strict` reports 21 advisory shared-spec
  pairs; it is otherwise clean.
- The depth-0 mockup (`docs/plans/mockups/`) still renders `system = "kit"`.
  Its renderer rebuilds from the live registries, so it was not regenerated.

**Byte deltas on budgeted files:** `docs/status.md` shrank by 4 lines; no
other capped file was edited.

**Checks run before this commit.**

- `check_trajectory.py --strict`: **clean** (608 work items; 85 warnings: the
  64 already present plus the 21 shared-spec pairs above).
- `check_docs.py --root . --stale`: **OK**, 1479 docs, 0 broken links, 3
  orphan warnings, all present before this session.
- Commit bar (smoke + `check_smoke_budget.py --mode enforce`): still
  running when `4c4a91ae` was committed at the owner's request; its result
  is recorded below.

**Commit bar, on this machine.**

- Results: smoke **1681 passed, 3 skipped** (264.6 s, then 236.3 s on the
  budget check's own run).
- Seconds: **FAIL**. `check_smoke_budget.py --mode enforce` measured 237.7 s
  against the 60 s budget. This box has 8 logical cores, and a codex review
  was running alongside the second run. The changes are documentation and
  registry filings only and cannot move the tier's timing; one machine is one
  data point, so the budget was not re-stamped.

<!-- fig: cmd="python -m pytest -q -n auto -m smoke; python scripts/check_smoke_budget.py --mode enforce" rev=4c4a91ae -->

**Cross-provider review.** A codex Sol review (reasoning effort medium, the
read-only sandbox, 225,090 tokens) of `d8998c27..4c4a91ae` verified all six
claims the session added (the S11 claim and batching facts, the mint's title
dedupe, the census's whole-body hashing, the intake staging hazard, the
providers' cached-token semantics, the S13 precedent) and returned 7
findings (5 MAJOR, 2 MINOR), all applied:

- the sister plan's §3.5 recommendation of (i) and §2.3's phase-close
  checkpoint are marked superseded by the S11 and S6 rulings;
- WI-606 captures raw codex and opencode usage without mapping it, and Claude's
  two parse defects move to S7's adapter (the S8 ruling), so there is one
  mapping, not two;
- WI-541 now waits on WI-605, so the retention check reads corrected
  occupancy;
- this fragment records the bar's result instead of promising it;
- WI-608's citation and WI-607's over-length title are corrected.
