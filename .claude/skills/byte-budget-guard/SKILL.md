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
| `project-trajectory/PROCESS.md` | **watched** (baseline **68,197** as of 2026-08-13/WI-443 (+829 on the 67,368 stamp: §8 gains the ruled OI-14 part B INTERFACE-ONLY contract — `Contract` states only what crosses plus its `Signal` (`discrete`/`variable`), the why moves to `Rationale`, the four warn-first form rules (no WI id, no decision citation, no rationale connective, a 500-character ceiling) are named, and `Stability` is declared the row's ONE maturity field now that `Status` retires; the field list and the machine-consumed paragraph re-worded in place (`Status` dropped from the `plan_briefs` surface); earlier 67,368 as of 2026-08-13/WI-440 (+311 on the 67,057 stamp: §8 gains one paragraph stating that `plan_briefs.IF_SURFACE_COLUMNS` feeds the IF row's surface — `Contract` and `Status` included — VERBATIM into the dual-plan LLM planning briefs, so a cell is consumed as authority rather than merely read (OI-14's first do-not-wait); earlier 67,057 as of 2026-08-12/stage-gate ruling (+2,591 on the 64,466 stamp: §4 gains the ruled **"Stages and gates — state vs. certified boundary"** subsection — the 0–5 stage ladder with the gates between its rungs, the uniform next-gate rule, the kept "a gate is not a pure function of stage" caveat, and the floor-not-achievement reading of the derived value; the §4/§7 gate-as-state sentences reworded in place. Owner ruling 2026-08-12, `docs/archive/plans/2026-08-11-stage-gate-semantics.md`; earlier 64,466 as of 2026-08-11/WI-432 (unchanged by that WI, which did not touch this file; the number is RECONCILED to what the tree actually carries — the 64,451 stamp had drifted +15 un-flagged. Historical reasons kept: −9 on the 64,460 stamp: −9 on the 64,460 stamp: §4's gate-authority and §7's push-authority pointers moved from the retired one-word files to their `docs/process.toml` dials, which reads shorter; earlier +141 on the 64,319 stamp: the §4 phased-delivery note tightened to numeric-only Phase and gained the ruled phase-boundary sentence (confirmed scope change, never the raw gate drop) + the `--next-phase` pointer)); keep flat — re-stamp this number, every tracked skill copy, when a flagged growth lands) | convention + the WI log's byte-delta report |
| `project-trajectory/PROCESS_OPTIONS.md` | **watched** (baseline **171,289** as of 2026-08-13/WI-437+WI-440 (+316: the OI-25 sweep — the ten instructional lines that taught the RETIRED `gate_policy` enum rewritten onto the live vocabulary (`human_ratification_through`, the `human-held`/`loop-held` SESSION HOLD); the `--gate-policy` flag and `docs/gate-policy.md` keep their names — live interface, not residue; plus +355: the "Component layer" cross-CMP paragraph states the new WI-440 multi-membership overlap ADVISORY — warn-only, never the exit code — so the new WARN an adopter sees is documented in the layer that emits it; both on the 170,618 stamp, composed at the serial merge; earlier 170,618 as of 2026-08-12/stage-gate ruling (+9 on the 170,609 stamp — net flat: the "Derived gate model" section stops calling itself "the working summary", repoints its dead `docs/specs/derived-gate-model.md` deference at the archived spec AND at process.md §4 as the ruled authority, and its applies-when row stops claiming an always-on layer; the false "the repo is at gate G iff" claim is gone, and four now-duplicated restatements were trimmed to pay for the additions. Owner ruling 2026-08-12; earlier 170,609 as of 2026-08-11/WI-433 (+212 on the 170,397 stamp: the "Unattended operation" blackout sentence now states the ruled SHIPPED-DISABLED default and the asymmetry that decided it, replacing one clause that named a value; earlier −62 on the measured 170,459 at WI-432: −62 on the measured 170,459 this file actually carried: the "Where the dials live" note and five layer opt-out sentences re-point from the six one-word files to `[checks] <key> = false`, which reads shorter. NOTE the stamp it replaced said 170,452 while the tree held 170,459 — a +7 drift that landed un-flagged before this WI, reconciled here rather than carried; earlier +1,314 on the 169,138 stamp: +1,314 on the 169,138 stamp: the "Where the dials live" note — the one policy home `docs/process.toml`, its keyed-pure-sh shape, the `--migrate-config` conversion and the refusal of a mixed config, plus the three kinds of declared file that deliberately stay outside it — and the per-dial rewrites from the retired one-word files to their `[section] key` names; earlier +13 on the 169,125 stamp: the layer table gained its row for the dispatcher split; earlier +115 on the 169,010 stamp: the "Signed measurements" *Grammar* sentence narrowed to whole-token placeholders — a metacharacter inside a longer value is command text and the marker is judged, closing the silent over-approximation of WI-392 REVIEW-A round-2 finding 4; earlier +788 on the 168,222 stamp: "Phased delivery" — the numeric-only rule with its literal-join rationale and grandfathering note replacing the free-form-string blessing, plus the ruled phase-boundary paragraph and the `--next-phase` helper; earlier +1,908 on the 166,314 stamp: +1,570 for "Signed measurements" part 3 — the opt-in `fig:` declared-figure marker grammar with the population and derived-figure bars, the truth/presence enforcer split, and rung 2 recorded as deliberately not built — plus +338 at the REVIEW-A rework: the *Grammar* sentence (placeholder values declare nothing, per-marker judgment, bare-or-quoted rev=) and two fig-ok exemptions so the convention text ships scaffold-clean); growth is allowed but must be *flagged* with a delta + reason — re-stamp this number, every tracked skill copy, when a flagged growth lands) | convention + the WI log's byte-delta report + the doc's own *Applies-when index* note |

`ADOPTING.md`, `EXAMPLE.md` and `RESYNC_PACK.md` are the unbudgeted
**expansion homes**:
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
