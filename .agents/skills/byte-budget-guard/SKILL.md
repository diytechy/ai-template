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
door silently. The doc-size evidence (2026-08-18, re-derived over one 48-day
window with all three files present; derivation and withdrawn figures in
`docs/knowledge/instruction-file-adherence.md`) is that **hard
caps hold and watch-only does not**: capped `AGENTS.template.md` +2.6% and still
under cap; watched `PROCESS.md` +91% and `PROCESS_OPTIONS.md` +1,101%. Check
before you edit and again before you commit.

## Budgets

**Capped** — a test fails past the number. Enforced by
`tests/test_bootstrap.py::test_always_loaded_docs_stay_within_byte_caps`
(plus `::test_agents_template_stays_within_size_budget` for AGENTS).

| File | Hard cap | Baseline | Stamped | Latest change |
|---|---|---|---|---|
| `project-trajectory/AGENTS.template.md` | **10,000** (≥2k headroom under Gemini's ~12k cap) | 9,953 | 2026-08-18 | WI-455's architecture retirement — **and see the parked-at-the-cap note below** |
| `CLAUDE.md` | **8,500** | 6,981 | 2026-08-18 | +176: the mandated-token rule — what the kit writes into an adopter's cell must mean something in their repo |
| `project-trajectory/skills/byte-budget-guard/SKILL.md` | **5,000** | 4,968 | 2026-08-20 | +136: WI-485's two re-stamps (the 4,882 baseline was stale — the file measured 4,832) |

**`AGENTS.template.md` is parked at its cap: 47 bytes free (0.5%).** Every other
capped file holds 2–18%, so this is the one you will hit first, and it is the DOC
that must give — the cap is load-bearing (it reserves ≥2k for the adopter's own
section under Gemini's truncation) and is not to be raised. Adding a sentence
there means cutting one there, in the same edit.

**Watched** — growth is allowed but must be flagged with a byte delta + reason
in the session/WI note. Enforced by convention + that report.

| File | Baseline | Stamped | Latest change |
|---|---|---|---|
| `project-trajectory/PROCESS.md` | 83,486 | 2026-08-20 | **+987**: WI-485 (OI-41) — §5 gains the always-shipped owner-decision-surface clause and its three deferral mechanisms. FLAGGED growth, not a displacement: nothing in §5 became redundant, and what moved came out of `PROCESS_OPTIONS.md` |
| `project-trajectory/PROCESS_OPTIONS.md` | 174,309 | 2026-08-20 | +148: WI-485 (OI-41) — the owner-decision-surface paragraph loses its *where it lives* half (now `process.md` §5) for the pointer, and S-3's escape is corrected: an absent registry is the finding |

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
