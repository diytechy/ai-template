---
name: byte-budget-guard
description: Use before and after editing this repo's budget-watched docs (AGENTS.template.md, PROCESS.md, PROCESS_OPTIONS.md) to confirm they stay within their byte budgets and to report the delta.
stacks: [any]
domains: [any]
phases: [dev, gate]
tags: [byte-budget, agents-md, process-md, docs]
scope: this-repo
---

# Byte-budget guard (this template repo)

This repo's shipped guides have **byte budgets** because a downstream
`AGENTS.md` is truncated by Gemini near ~12k chars, `PROCESS.md` is the
load-bearing core we keep lean, and `PROCESS_OPTIONS.md` (the opt-in expansion
home) will otherwise bloat the adopter's reading cost silently — the growth
just moves next door. Growing any of them silently is a recurring failure mode
here. Check before you edit and again before you commit.

## Budgets

| File | Budget | Enforced by |
|---|---|---|
| `project-trajectory/AGENTS.template.md` | **10,000 bytes** (≥2k headroom under Gemini's ~12k cap) | `tests/test_bootstrap.py::test_agents_template_stays_within_size_budget` |
| `project-trajectory/PROCESS.md` | **watched** (baseline **63,249** as of 2026-07-27/WI-328 (+1,425 on the 61,824 stamp: §3's stand-alone rule corrected to its real scope — every spine registry, not the `SR` alone — and its real severity, gating under `--strict`; plus §4's rule that requirement-text work sequences INTO an open re-attestation window rather than after it; plus the §2 tier table naming the LLR's new `Detail`/`Rationale` split — the prose for it went to ADOPTING.md §6 and EXAMPLE.md, which are unwatched on purpose; plus the two §3 rules the WI exists to state — one requirement/one `shall` in decidable terms, and a rationale that carries its own reason — which belong beside the stand-alone rule they complete, not in an options doc a downstream adopter may never open); keep flat — re-stamp this number, every tracked skill copy, when a flagged growth lands) | convention + the WI log's byte-delta report |
| `project-trajectory/PROCESS_OPTIONS.md` | **watched** (baseline **165,000** as of 2026-07-28/WI-342 (+1,887 on a tree that was ALREADY 163,113: the "Signed measurements" section + its applies-when row. Note the 1,342 between the previous stamp of 161,771 and the tree it was stamped against — WI-322 and the 127-REVIEW-A commit grew this file without re-stamping, which is why the procedure says `wc -c` FIRST and never trusts this number as the before-size); growth is allowed but must be *flagged* with a delta + reason — re-stamp this number, every tracked skill copy, when a flagged growth lands) | convention + the WI log's byte-delta report + the doc's own *Applies-when index* note |

`ADOPTING.md` and `EXAMPLE.md` are the unbudgeted **expansion homes**:
push detail there instead of growing `PROCESS.md` / `AGENTS.template.md`.
`PROCESS_OPTIONS.md` is also an expansion home, but — watched itself now — its
growth is flagged too, not free.

## Procedure

1. **Record the before-size** of any budgeted file you will touch:

   ```
   wc -c project-trajectory/AGENTS.template.md project-trajectory/PROCESS.md project-trajectory/PROCESS_OPTIONS.md
   ```

2. Make the edit. Prefer net-zero wording; if a rule must be added to
   `AGENTS.template.md`, **pay for it by tightening another** (the file's own
   *Customizing* note states this).

3. **Re-measure and compute the delta.** `AGENTS.template.md` must be
   `<= 10000`. If `PROCESS.md` or `PROCESS_OPTIONS.md` grew, that is allowed
   but must be *flagged* with the byte delta and a reason in the session/WI
   note (the convention every late thread followed), and the grown file's
   baseline in the Budgets table above must be **re-stamped** — source plus
   every tracked skill copy — in the same commit.

4. **Confirm the test still passes** whenever `AGENTS.template.md` changed:

   ```
   python -m pytest tests/test_bootstrap.py::test_agents_template_stays_within_size_budget -q
   ```

## Report shape (paste into the WI/session note)

```
Byte deltas: AGENTS.template.md <before> -> <after> (state the headroom left under 10,000);
PROCESS.md <before> -> <after> (unchanged, or delta + reason);
PROCESS_OPTIONS.md <before> -> <after> (unchanged, or delta + reason).
```

If a budgeted file grew, say by how much and where the paid-for tightening (or the
justification) is. Never report "within budget" without the actual `wc -c` number.
