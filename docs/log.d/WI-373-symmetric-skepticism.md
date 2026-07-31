## 2026-07-30 — WI-373: the finding lifecycle, reversal evidence, and sanctioned rework

Owner-directed (the moth-balled-work post-mortem: parked changes had been
scrubbed by sessions that never read the record justifying them, and review
findings were being acted on unverified). Documentation-only; no new checks —
the 2026-07-28 audit's enforcement-layer-growth warning applied deliberately.

**What shipped.** (1) PROCESS_OPTIONS' "The LLM-gate verdict protocol" gains
**the finding lifecycle**: a finding names a concrete, falsifiable failure
scenario; its owner **confirms** it by reproducing that scenario or
**refutes** it *before* changing code; a refutation is a legitimate recorded
outcome charged to the reviewer's confirmed-finding rate, never the owner's
standing; a **re-review round verifies fixes landed — it does not hunt fresh
findings in them** (the 127→131 fix-aimed recursion measurement is the
reason); the mid-build **design-escalation case** (what was found / why the
current shape cannot reach the requirement / both paths' costs) closes the
paragraph; the reviewer-independence bullet routes per-WI rounds through the
lifecycle. (2) AGENTS.template's working agreement carries three austere
clauses: finding-is-a-claim as a *pointer* to the lifecycle, undo-takes-
evidence ("read the record behind landed work before reverting it"), and
wrong-design-escalates-as-a-written-case in the now "No sunk-cost shipping,
keeping, or blind retries" bullet — paid per the file's own Customizing rule
(the decision-dial tail, the stronger-approach sentence folded into
sanctioned-rework, the `--flow` parenthetical, one contract-example line,
three micro-trims). (3) The enforcement audit records the honest tiers —
confirm-or-refute (Reviewer+Prose, symmetric to the signed-measurements row),
reversal evidence (Prose), no-sunk-cost-keeping (Prose, the restructure named
as the worked precedent) — and its finding 3 lists the additions.

**Deviations from spec.** The spec named *two* AGENTS clauses; a third
(finding-is-a-claim) shipped as well — the always-loaded surface was the
directive's whole point — but as a pointer, not a restatement, after round-1
finding 3 caught the first cut duplicating the lifecycle. The escalation-case
shape moved from the AGENTS clause (austerity) into the PROCESS_OPTIONS
lifecycle paragraph (round-1 finding 4) so it ships somewhere durable.

**Review round record ([WI-373-REVIEW-A](../reviews/WI-373-REVIEW-A.md)).**
Round 1: CHANGES-REQUESTED, findings=5 (1 MAJOR, 4 MINOR) — every finding
**confirmed by reproduction before any fix**, none refuted: the lifecycle's
own first dogfooding. The MAJOR (close bookkeeping must precede the
merge-triggering APPROVE, house precedent WI-370/371) produced this close;
finding 2 caught a `git add -A` sweeping an uncommitted **OWNER_SCRATCHPAD.md
hunk** into the build commit — confirmed by `--stat` alone (owner-only
surface, content unread), the commit recut without it, the owner's edits left
on disk. Standing lesson: **never `git add -A` in this repo — stage by
name.** Findings 3/4/5 fixed as above (5 = the audit row now states the
score_reviews scoreboard has been dark since 2026-07-15; feed-or-delete
stays the open owner call, audit rec #8).

**Byte deltas on budgeted files.** AGENTS.template.md **9,975 → 9,991** (9
bytes headroom under 10,000; size test green). PROCESS.md **64,301
unchanged**. PROCESS_OPTIONS.md **161,117 → 162,601** (+1,484, flagged: the
finding lifecycle + escalation-case shape; baseline re-stamped in all three
skill copies).

**Bars (real output).** Full unfiltered suite at the close tree: **1690
passed / 7 skipped / 2 failed (617s)** — one failure the standing
work-branch conditional `test_this_repo_is_not_a_work_branch` (red for the
whole branch by WI-357's design, the WI-366/367 precedent); the other,
`test_meta_repo_has_zero_unexplained_orphans`, was this close's own defect —
archiving the spec moved it a directory deeper and broke its two relative
links (`../log.md`/`../status.md`) — fixed in the close commit and the test
re-run green (`1 passed`). Smoke `-m smoke` at close: **555 passed /
1 failed** (the same standing conditional). `check_docs.py --stale`:
0 broken. `check_trajectory.py --strict`: clean — **354 done**.
