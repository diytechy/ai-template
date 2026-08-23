# Gate-authority deviation register — `autonomous`

**Status:** ACTIVE — owner directive 2026-07-15 (in-chat) flipped the declared
gate authority `single-approve` → **`autonomous`** to let phases iterate
through their gates without a human g2-close sitting. **Reversible / temporary:**
the owner may restore a lower level at any time. Keep in version control.

_Prior level:_ **`single-approve`** — APPROVED 2026-07-13 (OI-2; owner review of
the WI-107 enablement commit, [log.md](log.md) "GATE: DevStg-Impl re-attestation" +
Decisions). That level and its approval stand as history and may be restored
by raising `human_approval_through` in [process.toml](process.toml) + this
register.

**The posture is still named by the word; it is no longer STORED as one.**
SN-029 retired the `attended` / `single-approve` / `autonomous` enum for an
ordinal, because the enum could not express "TCs are human-held but LLRs are
not" and four tables each re-interpreted it. `bootstrap.py --gate-policy` still
takes the familiar word and TRANSLATES it, which is why this register keeps it
in the title. What the word now means here, read off
[process.toml](process.toml) `[attestation]`:

| dial | this repo | meaning |
|---|---|---|
| `human_approval_through` | `"DevStg-Below"` | nothing is human-held; the loop approves every rung itself |
| `keep_nondependent` | `false` | a paged round does not carry non-dependent work forward |
| `final_review` | `"always"` | the end-of-run review is never skipped — the fixed point below, as a dial |

**What this is:** this repo declares the `autonomous` gate authority (those
three `[attestation]` dials in [process.toml](process.toml); process.md §4).
The kit-owned process doc is never edited per-repo (a re-sync overwrites it);
this register amends it (process-options.md "Gate authority levels"). Where the two disagree, this file wins — **except the
fixed points at the bottom, which nothing overrides.**

**This repo (the ai-template META-repo):** the kit's own unattended layer,
self-applied (adopted via **WI-107**, `docs/archive/specs/WI-107.2026-07-20.md`). Under
`autonomous`, every gate **except the owner's final read** closes on an **independent
fresh-context LLM reviewer's recorded verdict** — no human batch sitting. This
is config-layer only: **no spine change**, so the flip does **not** move the
derived stage (`docs/stage` is always whatever `derive_stage.py` computes — the
level never moves the derived value; read `docs/stage` for the current stage
rather than this register). The level governs only WHO approves a gate,
not what the gate computes. _(The flip's reviewed commit is the owner's
in-chat directive + this register update, 2026-07-15.)_

## Deviation register

| process.md clause | Standard behavior | This repo (`autonomous`) |
|---|---|---|
| §4 acceptor, DevStg-Reqs+DevStg-Tests | a human approves each gate | an **independent fresh-context LLM reviewer's recorded verdict** approves the gate; no human sitting |
| §4 approval point | per-gate approval | each gate closes on its recorded reviewer verdict (LLM-gate); a human call is queued as a `Needs <human>` Open item only when a **fixed point** below forces it |
| §4 acceptor, DevStg-Impl→DevStg-Release | a human approves each gate | autonomous (LLM-gate verdicts) |
| §4 consistency review 'pause and ask' | solicit the human | route by revert-cost: LOW → decide + record (log.md Decisions log); MEDIUM/HIGH → the Blocked register; never a mid-run pause |

## Fixed points (nothing in this file overrides these)

- **the owner's final read is the human's.**
- **No un-run greens** — a verdict or test result that wasn't actually
  executed is a process violation regardless of tier. _(This is why a
  perceptual `Critique` — e.g. WI-144's rendered dashboard judgment — still
  needs a real rendered verdict under `autonomous`; the level never lets the
  loop fabricate an APPROVE it could not run.)_
- **The harness is still the bar** — LLM judgment supplements the checks; it
  never waives a red one.
- **Approved owner decisions are never re-decided by an agent** — flag a
  problematic one as Blocked instead.
