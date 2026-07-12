---
name: byte-budget-guard
description: Use before and after editing this repo's budget-watched docs (AGENTS.template.md, PROCESS.md) to confirm they stay within their hard byte budgets and to report the delta.
stacks: [any]
domains: [any]
phases: [dev, gate]
tags: [byte-budget, agents-md, process-md, docs]
scope: this-repo
---

# Byte-budget guard (this template repo)

This repo's shipped guides have **hard byte budgets** because a downstream
`AGENTS.md` is truncated by Gemini near ~12k chars and `PROCESS.md` is the
load-bearing core we keep lean. Growing them silently is a recurring failure
mode here. Check before you edit and again before you commit.

## Budgets

| File | Budget | Enforced by |
|---|---|---|
| `project-trajectory/AGENTS.template.md` | **10,000 bytes** (≥2k headroom under Gemini's ~12k cap) | `tests/test_bootstrap.py::test_agents_template_stays_within_size_budget` |
| `project-trajectory/PROCESS.md` | **watched** (baseline **59,638** as of 2026-07-12/WI-095; keep flat — re-stamp this number, every tracked skill copy, when a flagged growth lands) | convention + the WI log's byte-delta report |

`PROCESS_OPTIONS.md`, `ADOPTING.md`, and `EXAMPLE.md` are the **expansion homes**:
push detail there instead of growing the two budgeted files.

## Procedure

1. **Record the before-size** of any budgeted file you will touch:

   ```
   wc -c project-trajectory/AGENTS.template.md project-trajectory/PROCESS.md
   ```

2. Make the edit. Prefer net-zero wording; if a rule must be added to
   `AGENTS.template.md`, **pay for it by tightening another** (the file's own
   *Customizing* note states this).

3. **Re-measure and compute the delta.** `AGENTS.template.md` must be
   `<= 10000`. If `PROCESS.md` grew, that is allowed but must be *flagged* with
   the byte delta and a reason in the session/WI note (the convention every late
   thread followed).

4. **Confirm the test still passes** whenever `AGENTS.template.md` changed:

   ```
   python -m pytest tests/test_bootstrap.py::test_agents_template_stays_within_size_budget -q
   ```

## Report shape (paste into the WI/session note)

```
Byte deltas: AGENTS.template.md 9976 -> 9976 (untouched, 24 B headroom preserved);
PROCESS.md 56230 -> 56230 (unchanged).
```

If a budgeted file grew, say by how much and where the paid-for tightening (or the
justification) is. Never report "within budget" without the actual `wc -c` number.
