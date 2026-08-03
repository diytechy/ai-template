# WI-412 — REVIEW-A (2026-08-02)

**Reviewer:** OPENAI-SOL (`gpt-5.6-sol`) via the `codex` CLI — cross-family,
fresh context, independent of the builder. Charter:
[code-review-adversarial](../rubrics/code-review-adversarial.md). The reviewer
was given the code diff and the requirement surface (WI-381 REVIEW-A findings
1/3/4) and **not** the builder's Deliverable, log fragment, or commit messages,
per the rubric's leaked-self-assessment clause.

**Rounds:** 2. Round 1 **REWORK** (1 BLOCKING, 2 MINOR); round 2 **APPROVE**
(0 findings).

## Round 1 — REWORK

1. **BLOCKING — the implementation counted merged BRANCHES, not integrated
   WIs.** Driven: a residue branch, a two-WI exclusive batch and one ordinary
   branch landed four WI specs while the banner reported three. `_poll`
   incremented once per lane and the residue credit used
   `len(finished_branches)`. The round-1 fix therefore closed the *symptom* the
   original finding named while leaving the contract ("count every WI
   integrated in the tick, whatever admission path merged it") unmet.
2. **MINOR — the two-source rejection was a rationalization.** Separate
   labelled counts are not double-counted unless summed; the exclusive-arm form
   hid two surfaced rows whenever one unrelated card existed (driven).
3. **MINOR — a false invariant comment.** "a drain that failed merged nothing
   to claim" is untrue: `integrate.integrate` merges in sequence and stops at
   the first refusal, so a red drain can have merged some. The reviewer
   confirmed no banner misreports today (both arms print no count on nonzero),
   so the defect was the stated invariant, not the behavior.

Also caught by the builder's own mutation check rather than by review: the
round-1 banner unit test passed against the OLD code and pinned nothing.

## Round 2 — APPROVE

Full verdict as returned by the reviewer:

## Subject framing

This diff changes dispatcher reporting, not merge mechanics:

- Counts integrated WI ids across ordinary lanes, exclusive batches, and residue drains.
- Separately labels pending owner cards and queued attestation rows.
- Documents sequential, partially successful drains.
- Re-stamps the watched `PROCESS_OPTIONS.md` byte count across three skill copies.

Blast radius includes drained, pause, and admission-path banners; parked/handback accounting; owner-facing surface guidance; and malformed residue handling.

## Failure classes hunted

- Silent undercount, overcount, and branch-vs-WI confusion.
- Double-counting or suppression between the two banner sources.
- Pre-credit when a sequential drain merges one branch then refuses another.
- Regressions through ordinary, exclusive, parked, and handback paths.
- Hand-made claim directories, absent branches, and unclaimed branch specs.
- Tests remaining green against old arithmetic.
- Incorrect byte stamps or divergent skill copies.

## Round-1 finding closure

1. Prior BLOCKING branch-count defect: closed.

The real five-WI flow landed two residue WIs, two exclusive-batch WIs, and one ordinary WI:

```text
dispatch: queue drained - no ready work items; 5 WI(s) integrated this run.
REVIEW_PROBE rc=0
REVIEW_PROBE landed=WI-401-widget.md,WI-501-alpha.md,WI-502-beta.md,WI-777-residue.md,WI-778-second.md
```

Mutating both counters back to branch/lane counting made the new test fail with:

```text
dispatch: queue drained - no ready work items; 3 WI(s) integrated this run.
1 failed in 2.89s
MUTATION_RC=1
```

2. Prior MINOR two-source suppression: closed.

A real run with one pending card and two surfaced gate rows printed:

```text
dispatch: queue drained - 1 ratification(s) waiting in open-items.html; 2 queued attestation row(s) on the frontier (the two reads may name the same row)
REVIEW_PROBE cards=1
REVIEW_PROBE worker_calls=[]
REVIEW_PROBE rc=0
```

The old `max(...)` behavior produced two test failures. The exclusive-arm mutation that hid surfaced rows produced:

```text
AssertionError: queue drained - 1 ratification(s) waiting in open-items.html
1 failed
EXCLUSIVE_ARM_MUTATION_RC=1
```

3. Prior MINOR false transactional comment: closed.

I drove two residue branches where the first merged and the second failed the minted-ID refusal:

```text
REVIEW_PROBE predrain_residue_wis=2
REVIEW_PROBE rc=1 state_merged=0 good_on_trunk=True bad_on_trunk=False
```

No success count was printed. This confirms `dispatch.py` `_drain` (line 174 at review time) now describes the actual sequential, non-transactional behavior.

## Fresh probes

Admission-path counts:

```text
ORDINARY: ... 1 WI(s) integrated this run. rc=0
PARKED:   ... 2 WI(s) integrated this run. rc=0
HANDBACK: PAUSED ... 1 WI(s) integrated before the stop. rc=8
```

Requested malformed branch shapes:

```text
NO_BRANCH finished=[] residue_count=0
UNCLAIMED finished=['foreign'] residue_count=0
UNCLAIMED rc=1 state_merged=0 foreign_landed=False
```

The unclaimed branch was loudly refused with `trunk holds no claimed specs for foreign`.

I also challenged duplicate WI ids. The lightweight stub bar could permit a duplicate, but the real shipped scaffold rejected it before merge:

```text
gen_trajectory: ERROR - duplicate work-item id WI-777
REAL_DUP residue_count=2
REAL_DUP rc=1 landed=[]
```

Therefore I could not reproduce a production double-count defect.

## Tests actually run

All ran in the specified lane worktree:

```text
4 passed, 1 warning in 5.17s
153 passed in 36.12s
667 passed, 2 skipped in 14.09s
1965 passed, 6 skipped in 326.16s (0:05:26)
```

Pytest warned that the sandbox prevented its CPU-cap operation; the tests themselves completed normally. Final worktree status remained clean:

```text
## wi-412-dispatcher-banner-counts
```

## Byte and copy verification

After confirming LF working-tree content:

```text
169138 project-trajectory/PROCESS_OPTIONS.md
```

All three tracked copies stamp `169,138`, compare byte-identical, and hash identically:

```text
8d77e7bc80b1e97f9d70c5fc68ac227f3570339a6edf088bf0b7ebacb065adbf
COPY_CMP_RC=0
```

## Numbered findings

None. I reproduced no BLOCKING, MAJOR, or MINOR defect.

## F1/F3/F4 coverage map

| Spec item | Coverage | Result |
|---|---|---|
| F1 — honestly name both banner sources | Zero-card real-flow test, mixed-source real drive, old-`max` and exclusive-arm mutations | Covered |
| F3 — count every WI integrated through barrier-open residue and all admission paths | Five-WI drive, ordinary/parked/handback probes, partial-failure probe, branch-count mutation | Covered |
| F4 — re-stamp 169,138 across all tracked skill copies | `wc -c`, stamp search, SHA-256, and pairwise `cmp` | Covered |

VERDICT: APPROVE