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
| `project-trajectory/PROCESS.md` | **watched** (baseline **64,460** as of 2026-08-02/WI-402 (+141 on the 64,319 stamp: the §4 phased-delivery note tightened to numeric-only Phase and gained the ruled phase-boundary sentence (confirmed scope change, never the raw gate drop) + the `--next-phase` pointer); keep flat — re-stamp this number, every tracked skill copy, when a flagged growth lands) | convention + the WI log's byte-delta report |
| `project-trajectory/PROCESS_OPTIONS.md` | **watched** (baseline **170,032** as of 2026-08-08/mechanized-loop P13 docs half (+894 on the 169,138 stamp: the `NEEDS-HUMAN`→`NEEDS-JUDGEMENT` label migration (decision D-6), carrying the ruling that **exit code 7 does not move** and that the open-items *bucket* keeps the old spelling because there an owner call genuinely is the point; plus `partial/` — the third terminal (decision D-2) — added to the work-item layer's lifecycle bullet, its directory statement, its `Status ∈ {…}` set and its terminal prose (an attempt's judgement is an immutable outcome event outside `docs/work/`, and its remaining scope a newly minted successor, never the same row revived); earlier +13 on the 169,125 stamp: the layer table gained its row for the dispatcher split; earlier +115 on the 169,010 stamp: the "Signed measurements" *Grammar* sentence narrowed to whole-token placeholders — a metacharacter inside a longer value is command text and the marker is judged, closing the silent over-approximation of WI-392 REVIEW-A round-2 finding 4; earlier +788 on the 168,222 stamp: "Phased delivery" — the numeric-only rule with its literal-join rationale and grandfathering note replacing the free-form-string blessing, plus the ruled phase-boundary paragraph and the `--next-phase` helper; earlier +1,908 on the 166,314 stamp: +1,570 for "Signed measurements" part 3 — the opt-in `fig:` declared-figure marker grammar with the population and derived-figure bars, the truth/presence enforcer split, and rung 2 recorded as deliberately not built — plus +338 at the REVIEW-A rework: the *Grammar* sentence (placeholder values declare nothing, per-marker judgment, bare-or-quoted rev=) and two fig-ok exemptions so the convention text ships scaffold-clean); growth is allowed but must be *flagged* with a delta + reason — re-stamp this number, every tracked skill copy, when a flagged growth lands) | convention + the WI log's byte-delta report + the doc's own *Applies-when index* note |

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
