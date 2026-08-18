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
context unconditionally, `PROCESS.md` is the load-bearing core we keep lean, and
`PROCESS_OPTIONS.md` is the expansion home that otherwise moves the bloat next
door silently. The 60-day evidence (2026-08-18 doc-size audit) is that **hard
caps hold and watch-only does not**: capped `AGENTS.template.md` came in at
−14%, watched `PROCESS.md` at +263% and `PROCESS_OPTIONS.md` at +1,092%. Check
before you edit and again before you commit.

## Budgets

**Capped** — a test fails past the number. Enforced by
`tests/test_bootstrap.py::test_always_loaded_docs_stay_within_byte_caps`
(plus `::test_agents_template_stays_within_size_budget` for AGENTS).

| File | Hard cap | Baseline | Stamped | Latest change |
|---|---|---|---|---|
| `project-trajectory/AGENTS.template.md` | **10,000** (≥2k headroom under Gemini's ~12k cap) | 9,994 | 2026-08-18 | `DevBar-*` → `DevStg-*` vocabulary rename |
| `CLAUDE.md` | **8,500** | 6,677 | 2026-08-18 | cap introduced (~27% headroom over the measured size) |
| `project-trajectory/skills/byte-budget-guard/SKILL.md` | **5,000** | 4,101 | 2026-08-18 | changelog evicted to `docs/log.md`; caps declared |

**Watched** — growth is allowed but must be flagged with a byte delta + reason
in the session/WI note. Enforced by convention + that report.

| File | Baseline | Stamped | Latest change |
|---|---|---|---|
| `project-trajectory/PROCESS.md` | 81,385 | 2026-08-18 | −114: the WI-455 merge — architecture.md references repointed to `docs/runtime-flows.md`/the dashboard |
| `project-trajectory/PROCESS_OPTIONS.md` | 173,374 | 2026-08-18 | −1: the WI-455 merge's token reconciliation |

`docs/status.md` is deliberately **not** here: its length is the kit's own
shipped warn-only S-1 line budget (default 120, `docs/status-lint` overrides) in
`check_docs.py` — a downstream-tunable check, not a meta-repo cap.

`ADOPTING.md`, `EXAMPLE.md` and `RESYNC_PACK.md` are the unbudgeted **expansion
homes**: push detail there instead of growing a capped file. `PROCESS_OPTIONS.md`
is an expansion home too, but — watched itself — its growth is flagged, not free.

## Procedure

1. **Record the before-size** of every listed file you will touch:

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
   nest the superseded stamp in a parenthetical — superseded stamps belong in
   `docs/log.md`, which is the history home.

4. **Confirm the tests still pass** whenever a capped file changed:

   ```
   python -m pytest tests/test_bootstrap.py -q -k "byte_caps or size_budget"
   ```

## Report shape (paste into the WI/session note)

```
Byte deltas, one line per touched file:
<file> <before> -> <after> (headroom left under its cap, or delta + reason).
```

Never report "within budget" without the actual `wc -c` number.
