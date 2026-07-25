# 118-CRITIQUE — dashboard accessibility (SR-052), post-WI-293 render surface

**Trigger:** the WI-243 perceptual re-fire, second round this day. WI-293's A4 fix
touched `gen_trajectory.py` at `662bc87`, after 115/116/117, so
`check_trajectory --strict` returned to the fail-closed
`perceptual-stale SR-052;SR-053;SR-054`. This re-dates the perceptual evidence
past that render change and re-judges **SR-052** cold.

**Critic:** `OPENAI-SOL` (`gpt-5.6-sol`, OPENAI family) — a fresh,
family-heterogeneous **non-Anthropic** session per SR-084 / SN-024, dispatched by
hand through the `codex` CLI. The OpenCode-Go gateway that served 115/116/117 went
unresponsive mid-session (it stopped answering even a one-token probe), so the
OPENAI family carried this round; the requirement is *non-Anthropic*, which OPENAI
satisfies exactly as OpenCode did. Brief built to the SR-084 contract — rubric +
SN/SR intent + artifact recipe, **no build transcript and no implementer
self-assessment** — in an isolated sandbox holding only the artifact, an 11-shot
subset, and the rubric.

**Artifact:** `PROJECT_STATE.html` as generated at HEAD `662bc87` (byte-identical
to the copy judged), plus 11 renders — Process, landing, When, Knowledge and
How-SW across both themes, plus the 390px mobile fold.

**Rubric:** [dashboard-accessibility.md](../rubrics/dashboard-accessibility.md),
anchors `A1`–`A4`.

**Independent re-verification before recording.** Every A4 number reproduces
exactly: the focus ring at **1.00:1** on the phase-3 block (the ring is painted in
that block's own fill), **2.11:1** in dark, and the icicle amber ring at **2.49 /
2.22 / 2.55** on the SR / LLR / TC fills. WI-293's hub fix is confirmed landed at
**6.29:1**.

**Corroboration across critics.** The phase-3 focus-ring invisibility is now found
independently three times, at three severities: `OPENCODE-KIMI`
([117](117-CRITIQUE.md)) filed it MINOR under uniformity U5, `OPENCODE-GROK`
([116](116-CRITIQUE.md)) saw it and declined to file ("focus still updates the
detail pane"), and `OPENAI-SOL` files it MAJOR under A4 here. Three looks, one
defect — the strongest evidence this round produced.

**A recorded inconsistency, not resolved.** This session judged **A2 PASS**. The
sibling run against the composed WI-273 tree
(`docs/reviews/3-g3-WI-273-b45e/004-CRITIQUE-9b85f03.md`, same model, same rubric)
judged **A2 FAIL** on the unnamed `role="img"` containers. The evidence is
byte-identical — **41 of 43 unnamed in both artifacts**, verified directly — so
this is same-critic non-determinism, not a difference between the renders. It is
recorded here rather than reconciled, and it is why **WI-297** asks for an owner
ruling on A2 instead of another dispatch: a third opinion is not obviously worth
more than the two that already disagree.

---

## Anchor verdicts

**A1 — Keyboard reachability:** PASS — all five tabs are native buttons; Process nodes are native links; all 1,143 interactive SVG groups have `tabindex="0"`. Focus opens detail panels, and drill-down nodes handle Enter/Space. No `<details>` blocks are emitted.

**A2 — Accessible names:** PASS — tabs, links, and generated breadcrumb buttons have visible labels; all 1,143 focusable SVG groups have a direct `<title>`; scrollable views have `aria-label`, and the Process graphic has an explicit graphic label.

**A3 — No information by color alone:** PASS — statuses use visible text and glyphs (`✓`, `○`, `⊗`), phases print labels such as `1`, `3`, and `unphased`, and tier/type nodes expose prefixes, labels, legends, and titled names.

**A4 — Text contrast:** FAIL — sampled text passes in both themes, including light muted `#64748b` on `#ffffff` at 4.76:1, dark muted `#94a3b8` on `#0f172a` at 6.96:1, and hub white `#ffffff` on `#4f46e5` at 6.29:1. However, A4 also requires 3:1 for UI boundaries: the focused phase-3 block uses `#4f46e5` against the identical `#4f46e5` fill in light mode (1.00:1), and `#818cf8` against `#4f46e5` in dark mode (2.11:1).

## Findings

- [MAJOR] A4 -> `.drill .block:focus rect` uses the theme accent as its only focus boundary; it disappears on the phase-3 fill in light mode (1.00:1) and remains below 3:1 in dark mode (2.11:1). The icicle’s amber focus ring also misses 3:1 on SR `#0e7490` (2.49:1), LLR `#64748b` (2.22:1), and TC `#047857` (2.55:1) fills -> introduce a dedicated focus treatment, such as a contrasting two-layer ring, verified at ≥3:1 against every node fill in both themes -> @owner

## Notes

The eleven renders otherwise show readable light/dark text, explicit legends, and redundant textual status/type cues. The mobile render preserves readable content and signals horizontal overflow.

VERDICT: CHANGES-REQUESTED findings=1
