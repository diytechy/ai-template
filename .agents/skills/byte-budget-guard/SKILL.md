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
| `project-trajectory/AGENTS.template.md` | **10,000** (≥2k under Gemini's ~12k cap) | 9,948 | 2026-08-20 | −5: WI-486's back-link re-word onto its dial, paid by dropping an example |
| `CLAUDE.md` | **8,500** | 7,147 | 2026-08-20 | +166: the stale ~17.6 s smoke figure replaced by three warm readings, one past the ceiling |
| `project-trajectory/skills/byte-budget-guard/SKILL.md` | **5,000** | 4,975 | 2026-08-21 | -7: the row had drifted 57 low (4,925 stamped, 4,982 real); every Baseline cell is now test-pinned |

**Two files are parked at their caps: `AGENTS.template.md` 52 bytes free (0.5%)
and this one under 1%;** `CLAUDE.md` holds ~16%. Those two are what you hit
first, and the DOC is what gives — a cap is load-bearing (AGENTS reserves ≥2k
for the adopter's own section under Gemini's truncation) and is not to be
raised. Adding a sentence means cutting one, in the same edit.

Each `Baseline` is pinned to the file's real size by
`test_capped_doc_baselines_match_the_real_sizes`: a stale baseline is how this
procedure produces the overrun it exists to prevent.

**Watched** — growth is allowed but must be flagged with a byte delta + reason
in the session/WI note. Enforced by convention + that report.

| File | Baseline | Stamped | Latest change |
|---|---|---|---|
| `project-trajectory/PROCESS.md` | 84,383 | 2026-08-20 | **+303** FLAGGED: WI-484 — §1's derived-SR clause re-pointed onto the `Hat-Refs` cell, carrying the two rules a column name cannot give (blank = *not recorded*; an LLR's effective set is own + parents') |
| `project-trajectory/PROCESS_OPTIONS.md` | 176,601 | 2026-08-21 | **+1,070** FLAGGED: WI-488 (OI-43 (a)) — seam-TC coverage promotes WARN to ERROR under `--strict` at DevStg-Tests+, with a migration allowlist |

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
