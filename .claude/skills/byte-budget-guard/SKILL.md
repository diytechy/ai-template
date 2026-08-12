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
| `project-trajectory/PROCESS.md` | **watched** (baseline **64,466** as of 2026-08-11/WI-432 (unchanged by that WI, which did not touch this file; the number is RECONCILED to what the tree actually carries — the 64,451 stamp had drifted +15 un-flagged. Historical reasons kept: −9 on the 64,460 stamp: −9 on the 64,460 stamp: §4's gate-authority and §7's push-authority pointers moved from the retired one-word files to their `docs/process.toml` dials, which reads shorter; earlier +141 on the 64,319 stamp: the §4 phased-delivery note tightened to numeric-only Phase and gained the ruled phase-boundary sentence (confirmed scope change, never the raw gate drop) + the `--next-phase` pointer); keep flat — re-stamp this number, every tracked skill copy, when a flagged growth lands) | convention + the WI log's byte-delta report |
| `project-trajectory/PROCESS_OPTIONS.md` | **watched** (baseline **170,397** as of 2026-08-11/WI-432 (−62 on the measured 170,459 this file actually carried: the "Where the dials live" note and five layer opt-out sentences re-point from the six one-word files to `[checks] <key> = false`, which reads shorter. NOTE the stamp it replaced said 170,452 while the tree held 170,459 — a +7 drift that landed un-flagged before this WI, reconciled here rather than carried; earlier +1,314 on the 169,138 stamp: +1,314 on the 169,138 stamp: the "Where the dials live" note — the one policy home `docs/process.toml`, its keyed-pure-sh shape, the `--migrate-config` conversion and the refusal of a mixed config, plus the three kinds of declared file that deliberately stay outside it — and the per-dial rewrites from the retired one-word files to their `[section] key` names; earlier +13 on the 169,125 stamp: the layer table gained its row for the dispatcher split; earlier +115 on the 169,010 stamp: the "Signed measurements" *Grammar* sentence narrowed to whole-token placeholders — a metacharacter inside a longer value is command text and the marker is judged, closing the silent over-approximation of WI-392 REVIEW-A round-2 finding 4; earlier +788 on the 168,222 stamp: "Phased delivery" — the numeric-only rule with its literal-join rationale and grandfathering note replacing the free-form-string blessing, plus the ruled phase-boundary paragraph and the `--next-phase` helper; earlier +1,908 on the 166,314 stamp: +1,570 for "Signed measurements" part 3 — the opt-in `fig:` declared-figure marker grammar with the population and derived-figure bars, the truth/presence enforcer split, and rung 2 recorded as deliberately not built — plus +338 at the REVIEW-A rework: the *Grammar* sentence (placeholder values declare nothing, per-marker judgment, bare-or-quoted rev=) and two fig-ok exemptions so the convention text ships scaffold-clean); growth is allowed but must be *flagged* with a delta + reason — re-stamp this number, every tracked skill copy, when a flagged growth lands) | convention + the WI log's byte-delta report + the doc's own *Applies-when index* note |

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
