# Gate-authority deviation register — `single-ratify`

**Status:** RATIFIED 2026-07-13 — owner review of the enablement commit (OI-2;
the sitting record + ruling: [log.md](log.md) "GATE: G3 re-attestation" +
Decisions log). Keep in version control.
**What this is:** this repo declares the `single-ratify` gate authority (`docs/gate-policy`; process.md §4). The kit-owned process doc is never edited per-repo (a re-sync overwrites it); this register amends it (process-options.md "Gate authority levels"). Where the two disagree, this file wins — except the fixed points at the bottom, which nothing overrides.

**This repo (the ai-template META-repo):** the kit's own unattended layer, self-applied. Adopted via **WI-107** (`docs/specs/WI-107.md`) so `agent-resume.*` boots a managed, consent-explicit run with **one human attestation point per phase batch**. Config-layer only — no spine change, so **WI-107 itself did not move the derived gate** (`derive_gate.py`); this level governs only WHO makes the ratifying Status-change commit, not what the gate computes. _(The gate value is always whatever `derive_gate.py` computes — `docs/gate` is authoritative, not this register. It read G3 at adoption; a later, unrelated change — the `[v3]-[g2]` decomposition, log.md 2026-07-14 — decomposed phase v3, so the derived gate is now **G2** while that phase is open. status.md's live G2 and this file are consistent: `single-ratify` still governs only the ratifying authority.)_ The landing commit that flipped `docs/gate-policy` to `single-ratify` was itself the reviewed commit the owner accepts (the single attest) — that review landed 2026-07-13 (the OI-2 acceptance; see the Status line above).

## Deviation register

| process.md clause | Standard behavior | This repo |
|---|---|---|
| §4 acceptor, G1+G2 | a human approves each gate | LLM-gate review; every human call queued as a `Needs <human>` Open item (+ provisional decision where the driver proceeded) |
| §4 ratification point | per-gate approval | one human sitting at **G2 close** ratifies/amends the queue; ratified decisions move to docs/log.md (relocating the point = amending this register) |
| §4 acceptor, G3→G-Release | a human approves each gate | autonomous rules after ratification (LLM-gate verdicts) |
| §4 consistency review 'pause and ask' | solicit the human | route by revert-cost: LOW → decide + record (log.md Decisions log); MEDIUM/HIGH → the Blocked register; never a mid-run pause |

## Fixed points (nothing in this file overrides these)

- **G-Final is the human's.**
- **No un-run greens** — a verdict or test result that wasn't actually
  executed is a process violation regardless of tier.
- **The harness is still the bar** — LLM judgment supplements the checks; it
  never waives a red one.
- **Ratified owner decisions are never re-decided by an agent** — flag a
  problematic one as Blocked instead.
