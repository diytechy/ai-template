# 004-CRITIQUE — dashboard accessibility (SR-052), composed WI-273 + WI-293 render

**Scope:** the COMPOSED tree `9b85f03` (train `3-g3-WI-273-b45e` merged onto the
WI-293 baseline) — *not* branch HEAD. It judges the render that would exist if
this train integrated, which is the render SR-052 acceptance must be measured
against.

**Critic:** `OPENAI-SOL` (`gpt-5.6-sol`, OPENAI family) — a fresh,
family-heterogeneous **non-Anthropic** session per SR-084 / SN-024, dispatched by
hand through the `codex` CLI after the OpenCode-Go gateway stopped responding
mid-session. The builder was `opus` (Anthropic), so OPENAI gives real cross-family
independence. Brief built to the SR-084 contract: rubric + SN/SR intent + artifact
recipe, and **no build transcript and no implementer self-assessment**. It worked
in an isolated sandbox holding only the artifact, an 11-shot subset, and the
rubric.

**Artifact:** the composed `PROJECT_STATE.html` + 11 renders (Process, landing,
When, Knowledge, How-SW across both themes, plus the 390px mobile fold).

**Rubric:** `docs/rubrics/dashboard-accessibility.md`, anchors `A1`–`A4`.

**Independent re-verification (by the composing session, before recording).** Every
checkable number reproduces: `--border` at **1.23 / 1.18 / 1.22 / 1.29** against
its four adjacent surfaces (floor 3:1), and **41 of 43** `role="img"` SVGs carry no
container-level accessible name (SOL counted 42; the difference is lookahead
window, not substance). The 4 focusable `.view` regions *do* each carry an
`aria-label` — SOL's A2 finding is about the inner SVGs, not those.

**Disagreement with [116-CRITIQUE](../116-CRITIQUE.md), recorded not resolved.**
`OPENCODE-GROK` saw both of these and passed them: the unnamed `role="img"` SVGs
as a Note ("parent `.view` aria-labels and per-node `<title>`s cover interactive
naming for A2 as written"), and the sub-3:1 borders via WCAG 1.4.11's
"identifiable by other means" exception. SOL calls both MAJOR because the `.view`
regions and Process-stage rectangles are themselves focusable controls. Two
independent non-Anthropic critics, two defensible readings of the same evidence.
The composing session did not adjudicate in its own favour; the stricter verdict
stands and the anchor remains unsatisfied.

**Note:** WI-293's hub fix is confirmed landed — SOL measured white on the Process
hub at **6.29:1** and passed it. Neither finding below is about WI-273 or WI-293;
both are pre-existing whole-document defects.

---

## Anchor verdicts

**A1 — Keyboard reachability:** PASS — the five native tab buttons implement roving `tabindex` with Arrow/Home/End handling; all 1,143 interactive SVG groups have `tabindex="0"`, focus opens their detail panel, and all 38 drill-down nodes handle Enter/Space. Process stages are native SVG links.

**A2 — Accessible names:** FAIL — all 1,143 focusable SVG nodes have immediate `<title>` elements, tabs have visible labels, and Process links are titled; however, 42 of 43 meaningful `role="img"` SVG containers have neither `aria-label`/`aria-labelledby` nor a direct `<title>`. Only the Process-loop SVG names its graphic.

**A3 — No information by color alone:** PASS — status nodes use redundant glyphs (`✓`, `○`, `⊗`) and textual legends; phase nodes display their phase labels; tier/type nodes carry visible abbreviations or names and corresponding text legends. The cues remain apparent across the eleven renders.

**A4 — Text contrast:** FAIL — sampled text passes in both themes: light muted `#64748b` on `#f8fafc` is 4.55:1, dark muted `#94a3b8` on `#0f172a` is 6.96:1, white on the LLR fill `#64748b` is 4.76:1, and white on the Process hub `#4f46e5` is 6.29:1. However, graphical/UI boundaries miss the rubric’s 3:1 floor: light `#e2e8f0` against `#ffffff` is 1.23:1 and against `#f8fafc` is 1.18:1; dark `#1e293b` against `#0f172a` is 1.22:1 and against `#0b1120` is 1.29:1.

## Findings

- [MAJOR] A2 -> 42 drill/icicle SVGs declare `role="img"` without a container-level accessible name, despite becoming meaningful visible graphics as layers are opened -> give each SVG a direct `<title>` or `aria-labelledby` tied to its visible layer heading; for SVGs containing independently interactive nodes, consider a named group role instead of an unnamed image role -> @owner
- [MAJOR] A4 -> `--border` supplies sub-3:1 boundaries for focusable `.view` regions, detail cards, and linked Process-stage rectangles in both themes -> introduce theme-specific boundary colors that reach 3:1 against every adjacent surface, or provide another persistent boundary cue meeting the same threshold -> @owner

## Notes

No actual expandable `<details>` control is emitted; the two textual occurrences are registry data, so that A1/A2 category is vacuous for this artifact.

VERDICT: CHANGES-REQUESTED findings=2
