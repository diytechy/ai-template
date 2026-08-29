---
name: byte-budget-guard
description: Use before and after editing this repo's byte-capped or byte-watched docs (AGENTS.template.md, CLAUDE.md, this skill, PROCESS.md, PROCESS_OPTIONS.md) to confirm they stay within their limits and to report the delta.
stacks: [any]
domains: [any]
phases: [dev, gate]
tags: [byte-budget, agents-md, process-md, docs]
scope: this-repo
---

# Byte-budget guard (this template repo)

Some files here cost every reader on every session: a downstream `AGENTS.md` is
truncated by Gemini near ~12k chars, `CLAUDE.md` and this skill load into agent
context unconditionally, `PROCESS.md` is the core we keep lean, and
`PROCESS_OPTIONS.md` is the expansion home that otherwise takes the bloat
silently. The evidence (2026-08-18, one 48-day
window, all three files present; derivation in
`docs/knowledge/instruction-file-adherence.md`) is that **hard caps hold and
watch-only does not**: capped `AGENTS.template.md` +2.6% and still
under cap; watched `PROCESS.md` +91% and `PROCESS_OPTIONS.md` +1,101%. Check
before you edit and again before you commit.

## Budgets

**Capped** — a test fails past the number. Enforced by
`tests/test_bootstrap.py::test_always_loaded_docs_stay_within_byte_caps`
(plus `::test_agents_template_stays_within_size_budget`).

| File | Hard cap | Baseline | Stamped | Latest change |
|---|---|---|---|---|
| `project-trajectory/AGENTS.template.md` | **10,000** (≥2k under Gemini's ~12k cap) | 9,980 | 2026-08-22 | +39: WI-507 — the dedup bullet gains the consolidation pointer (0→A→B) |
| `CLAUDE.md` | **8,500** | 7,827 | 2026-08-23 | -4: WI-499 — the `human_ratification_through` mention in the repo-map paragraph re-keys to `human_approval_through` |
| `project-trajectory/skills/byte-budget-guard/SKILL.md` | **5,000** | 4,883 | 2026-08-29 | WI-532 re-stamped both watched rows below (−367 / +449) and this row |

**`AGENTS.template.md` and this file are parked at their caps** (~1% free
each); `CLAUDE.md` holds ~8%. Those two are what you hit first, and the DOC is
what gives — a cap is load-bearing (AGENTS reserves ≥2k for the adopter's own
section under Gemini's truncation) and is not to be raised. Adding a sentence
means cutting one, in the same edit. Each `Baseline` is pinned to its file's
real size by `test_capped_doc_baselines_match_the_real_sizes`.

**Watched** — growth is allowed but must be flagged with a byte delta + reason
in the session/WI note. NOTHING PINS THESE: both had drifted un-flagged before
WI-498 slice 5 measured them, so re-stamp on the way past.

| File | Baseline | Stamped | Latest change |
|---|---|---|---|
| `project-trajectory/PROCESS.md` | 87,651 | 2026-08-29 | **−367** FLAGGED: WI-532 (OI-67) — §8 rewritten for the one-owner row (owner, far side, channel, data; the definition beside the code; mint header-first). Absorbs WI-527's unflagged +1,342 (86,676 → 88,018) |
| `project-trajectory/PROCESS_OPTIONS.md` | 179,209 | 2026-08-29 | **+449** FLAGGED: WI-532 (OI-67) — the intra-repo seam model becomes owner / far side / channel, and the risk paragraph moves the rot to the header where it is checked |

`docs/status.md` is deliberately **not** here: its length is the kit's shipped
warn-only S-1 line budget (default 120, `docs/status-lint` overrides) in
`check_docs.py` — a downstream-tunable check, not a meta-repo cap.

`ADOPTING.md`, `EXAMPLE.md` and `RESYNC_PACK.md` are the unbudgeted **expansion
homes**: push detail there rather than grow a capped file. `PROCESS_OPTIONS.md`
is one too, but — watched itself — its growth is flagged, not free.

## Procedure

1. **Record the before-size** of every listed file you touch:

   ```
   wc -c project-trajectory/AGENTS.template.md CLAUDE.md project-trajectory/PROCESS.md project-trajectory/PROCESS_OPTIONS.md project-trajectory/skills/byte-budget-guard/SKILL.md
   ```

2. Make the edit. Prefer net-zero wording; if a rule must be added to a capped
   file, **pay for it by tightening another** (`AGENTS.template.md`'s own
   *Customizing* note states the same rule for downstream editors).

3. **Re-measure and compute the delta.** Every capped file must be at or under
   its cap. Flag any watched file's growth with the delta and a reason, then
   **re-stamp** the changed row — source plus every tracked skill copy, in the
   same commit. A re-stamp **replaces** the row's baseline, date and reason; never
   nest the superseded one in a parenthetical — history lives in `docs/log.md`.

4. **Confirm the tests pass** whenever a capped file changed:

   ```
   python -m pytest tests/test_bootstrap.py -q -k "byte_caps or size_budget"
   ```

## Report shape (paste into the WI/session note)

```
Byte deltas, one line per touched file:
<file> <before> -> <after> (headroom left under its cap, or delta + reason).
```

Never report "within budget" without the actual `wc -c` number.
