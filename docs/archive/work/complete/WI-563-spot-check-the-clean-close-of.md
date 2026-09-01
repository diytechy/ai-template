+++
id = "WI-563"
title = "spot-check the clean close of WI-552 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

Spot-check of the GREEN close of WI-552 (the adjudicator's two exits, OI-70 as
refined by OI-73). One question asked: does what shipped answer what the row
asked for? **Verdict (corrected, round 2): the close STANDS WITH FINDINGS — a
successor is owed.** The first pass of this row answered "yes — the close
stands, no successor"; the supervisor-drawn REVIEW-A round
(`docs/reviews/wi-563-spot-check-the-clean-close-of/002-REVIEW-A-ef9f326-supervisor.md`,
CHANGES-REQUESTED findings=4) reversed that verdict, and this Deliverable is the
correction. Nothing about the WI-552 MERGE is reversed — a spot-check finding is
a successor row, never a reversal — but the finding is real and now carries one.

**THE MISS (why the verdict changed).** WI-552 arm 5 introduced an UNDECLARED
cross-component import, and `check_trajectory.py --strict` errors on it at this
lane's HEAD:

```
check_trajectory: ERROR - cross-component import scripts/schedule (CMP-008) -> scripts/trace (CMP-006) has no declared IF-### seam — declare the interface row in docs/requirements/interfaces.toml or retag the membership, or set docs/process.toml [checks] components_check = false
check_trajectory: 1 error(s) in docs/work.
```

The import is `project-trajectory/scripts/schedule.py:445`, the lazy `import
trace as _trace` inside `schedule.load_oi_status` (the REVIEW-A finding names
the enclosing concern `_open_item_states`; the function as shipped is
`load_oi_status`, which wraps `trace.open_item_states`). It is attributable to
the work under review: it arrived with `b2b06898` ("WI-552 arms 5+6: typed OI
edges in needs + dead-dep extends to partial") and the same command on trunk
immediately before the WI-552 merge (`b6e155d3^1`) is ERROR-free — that revision
of `schedule.py` contains no `import trace` at all. The first pass of this
spot-check concluded arm 5 "Present" and the close "STANDS" without detecting
it. This is exactly the class a sample attestation exists to catch, and it is
caught now.

**THE CAUSE OF THE MISS.** The first pass declared its Bar as "the environment
here has no pytest toolchain; the spot-check is a read-level attestation". That
claim was FALSE and is withdrawn: `check_trajectory.py` needs no pytest at all,
the trunk venv exists, `docs/status.md` standingly requires an unfiltered
`check_trajectory.py --strict` before anything is claimed done, and the station's
own refresh trailer at `ef9f3268` attests `bar PASS (11 steps, tier all)` on this
tree. An environment claim excused a check the environment could run and the repo
mandates — that is the direct cause of the missed ERROR, recorded here as its own
finding against the first pass, not against WI-552.

**Bar (real output, this worktree, 2026-09-01).**
- `check_trajectory.py --strict` -> **exit 1**, 1 ERROR (quoted above) + WARNs.
  Non-strict is exit 0. That red IS the finding; it is deliberately NOT fixed on
  this adjudication lane — the fix belongs to the drafted successor.
- `pytest -q -n auto -m smoke` -> **1449 passed, 8 skipped in 22.45s**.
- `check_smoke_budget.py --mode enforce` -> **smoke wall-clock budget: 20.6s vs
  60s budget -> within** (exit 0).
- `check_docs.py --root . --stale` -> **OK - 1152 doc(s), 1570 intra-repo
  link(s), 0 broken (1 orphan warning(s))** (exit 0).

**What still holds from the first pass.** Each of the seven Done-when arms was
located in the merged tree and matched the ask: arm 1 mechanical close
(`handback.close_adjudication` + `dispatch._close_done_adjudication`); arm 2
OI-mint (`intake._mint_open_item`/`_inject_open_item`); arm 3 refusal invariant
at both close and merge, extended to the cancelled arm; arm 4 inbound-edge
replacement (`intake._replace_inbound_edges`); arm 5 typed OI edges
(`kitlib.spine.split_pred_edges`, `waiting:open-item-pending`,
`validate(..., known_ois)`); arm 6 `dead_dependency_findings` extended to
`partial`; arm 7 the widened brief + PROCESS_OPTIONS prose. Each arm carries a
covering test. The arms are present — arm 5 simply shipped an undeclared seam
alongside them.

**Residuals, now queued rather than merely named.** `intake._SPEC_NEEDS_RE`
(intake.py:1344) lacks `re.DOTALL`, so `_replace_inbound_edges` silently skips a
dependent whose `needs` is written as a MULTI-LINE TOML list — arm 4's "becomes
unrepresentable" guarantee holds only under the single-line-`needs` invariant. It
does not bite today: the machine writers emit single-line `needs` and a tree-wide
scan finds no multi-line `needs` list. Two further round-4 APPROVE MINORs (dead
`intake._OI_ID_RE`; `check_trajectory.validate` docstring vs `known_ois=None`
coercion) are cosmetic and confirmed present. The first pass left all three on no
queue at all; they now ride the `## Dispositions` drafts below.

**Exits taken.** Two successors are DRAFTED in `## Dispositions` (below), for
`intake._disposition_drafts` to mint at this row's merge — a lane never mints an
id. Draft 1 declares the IF-### seam (or retags membership) for the
`schedule -> trace` crossing and records the strict-ERROR miss against the WI-552
close; draft 2 carries the `open_item` cell, so the mint raises a `pending` OI for
the human-owed DOTALL ruling (the two cosmetic leftovers ride its text) and lands
that OI id in draft 2's `needs`, parking it `waiting:open-item-pending` until the
owner rules. No fix to `schedule.py` or `interfaces.toml` was made here: this is
an adjudication row, and the repair is the successor's work.

No spine rows minted or re-statused (adjudication row, no SR-Refs), so no
approval-brief regeneration. Read-only audit: no product code changed.

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-552-adjudicator-two-exit-close.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.

## Dispositions

```toml
title = "Declare the IF-### seam for schedule.py's lazy import of trace, clearing the strict ERROR WI-552 introduced"
workstream = "process"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
```

WI-552 arm 5 added `import trace as _trace` inside `schedule.load_oi_status`
(`project-trajectory/scripts/schedule.py:445`), creating a cross-component
import `scripts/schedule` (CMP-008) -> `scripts/trace` (CMP-006) with no
declared IF-### row. `check_trajectory.py --strict` errors on it (exit 1); the
same command at `b6e155d3^1` — trunk immediately before the WI-552 merge — is
ERROR-free, so the red is attributable to that work and not pre-existing.
IN SCOPE: choose ONE of the two exits the checker itself names — declare the
interface row in `docs/requirements/interfaces.toml` (the likely right answer:
the OI readiness gate really is a seam between the scheduler and the registry
reader, and a declared seam wants a covering TC per process.md §8) or retag the
component membership if the two modules genuinely belong to one component. Then
re-run `check_trajectory.py --strict` and show exit 0 on the ERROR line.
EXPLICITLY NOT IN SCOPE: the pre-existing WARN population (undeclared
connectivity, IF-without-TC, LLR CodeSymbol drift) — those long predate WI-552
and are their own burn-down; do not green them here. Also record, in this row's
Deliverable, the process finding this successor exists for: the WI-563
spot-check first passed the WI-552 close as clean because it declared a false
no-toolchain Bar and skipped the mandated `--strict` run. Setting
`[checks] components_check = false` is NOT an acceptable exit — that is
sanctioning the check to green a step.

```toml
title = "Rule and apply the intake._SPEC_NEEDS_RE no-DOTALL residual, and clear the two cosmetic WI-552 leftovers"
workstream = "process"
buildtier = "quick"
safety_class = "ordinary"
priority = 3
open_item = "intake._SPEC_NEEDS_RE (intake.py:1344) has no re.DOTALL, so _replace_inbound_edges silently skips a dependent whose `needs` is a MULTI-LINE TOML list: WI-552 arm 4's 'the WI-541 strand becomes unrepresentable' guarantee in fact holds only under the single-line-`needs` invariant the machine writers happen to keep (a tree-wide scan finds no multi-line `needs` today, so it does not bite). Rule which the kit means: (a) tighten the regex to DOTALL (or a real TOML read) so the guarantee is unconditional, (b) keep the regex and DECLARE the single-line-`needs` invariant, enforced by a check so a hand-written multi-line `needs` is refused rather than silently skipped, or (c) accept the narrowed guarantee and amend WI-552's claim to match."
```

Gated on the owner's ruling by construction: the `open_item` cell above makes
`intake._inject_open_item` mint a `pending` OI at this row's merge and land its
id in THIS row's `needs`, so the successor parks
`waiting:open-item-pending` until the ruling lands (OI-73 exit (B) — there is no
standalone OI exit; the OI is always a dependency of a queued successor).
Riding along, because they are one small pass over the same two files and were
also left on no queue by the first spot-check pass: (i) `intake._OI_ID_RE`
(intake.py:304) is dead — `next_oi_id` reads the watermark and
`trace.live_max_ids`, nothing uses the regex; delete it or use it. (ii)
`check_trajectory.validate`'s docstring disagrees with the shipped
`known_ois=None` coercion at check_trajectory.py:812 (`known_ois = known_ois if
known_ois is not None else frozenset()`); fix the docstring to state what the
code does. Both are cosmetic and neither needs the ruling — but do them in the
same commit range so the residual list from the WI-552 review closes out whole.
