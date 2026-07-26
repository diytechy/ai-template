# Mechanizing the dashboard's "perceptual residue" (WI-309…WI-312)

**Status: queued** (filed 2026-07-25, owner-directed: *"ideally we can get to the
point where critiques are not required — if the test and render methods produce
quality graphics with considerations for these aspects as mechanical tests,
critiques can be retired."*)

A shared effort doc, one section per WI. The spec-of-record for each row.

## Why these four exist

WI-300's option (f) decomposes each rubric anchor into a child LLR + automated
TC. Nine children landed. **Six of them end by handing a leftover back up to
their coarse parent** — `LLR-102` "near-duplicate but non-identical hues",
`LLR-103` "spacing, exact visual weight", `LLR-104` "whether the sizes read as
visually uniform", `LLR-101` "whether each control READS as well-named". By the
ruling's own rule (`Verification=Critique` only while a perceptual child
remains) that pins SR-052 and SR-053 to the critique indefinitely.

**Measured against the shipped artifact 2026-07-25, none of the four is
perceptual. They are UNMEASURED.** Three are ordinary arithmetic or set
membership; the fourth is ~90% mechanical. And each would **fail today**, which
is the real finding: quality defects were sitting behind the word "perceptual".

These four WIs mechanize them — *fix + the check that owns the anchor*, the
standing pattern. When they land, SR-052 and SR-053 flip to `Verification=Test`
with an **empty** residue rather than accepted losses.

**They do not retire critiques outright.** SR-054's four clauses (is the entry
point *obvious*, does the reader stay *oriented*, does a truncation read as
*more-available*, are crossings *tolerable*) are about a reader's experience, not
the artifact's properties, and `perceptual-stale` fires while **any** SR is
`Critique`. That boundary is a separate question — see "What stays" below.

## WI-309 — U1: one declared type scale, no raw font-size literals

**Measured:** 18 raw `font-size` literals against 5 declared tokens.
`.7rem`/`.75rem`, `.9rem`/`.95rem`/`.98rem`, `1.05rem`/`1.1rem`, `8.5px`/`9px`
are near-duplicate steps for the same role — 3–7% apart, which no reader
distinguishes and no rule justifies. Two of the literals (`.85rem`, `.8rem`)
are *byte-identical to an existing token* and simply weren't using it.

**Core.** Declare the scale, then assert every emitted `font-size` resolves to a
declared step. Two families, documented as two because they genuinely are:

- a **page** scale in `rem` (prose, cards, tiles — scales with the root size);
- a **node** scale in `px` (SVG labels, whose geometry is fixed px, which is why
  `--nlabel` was already px while `--small` was rem);
- one **relative** step in `em` for text that must size against its parent
  (`code`, a table sub-line).

Near-duplicate steps merge into the nearer declared one. Claiming "one scale"
across rem and px would be false, so the LLR states two-plus-one.

**Done-when:** every `font-size` in every rendered document is `var(--…)`; the
declared set is small and each step names its role; a test asserts it over the
full emitter sweep.

## WI-310 — U3: one declared token set for stroke, opacity and corner radius

**Measured:** 8 distinct `stroke-width`, 7 `opacity`, 5 `border-radius`, 4 `rx`.
That is drift, not a system — and it is exactly what `LLR-103`'s residue
("spacing, exact visual weight") gestures at without measuring.

**Core.** Same shape as WI-309: declare the set, assert membership. Same
merge rule for near-duplicates (`1.2`/`1.4`/`1.5` stroke widths are one weight).

**Done-when:** every emitted stroke-width / opacity / radius resolves to a
declared token; a test asserts it over the full emitter sweep.

## WI-311 — U5: extend the pairwise ΔE floor across vocabularies

**Measured:** the repo already computes pairwise ΔE — but only *within*
`PHASE_ACCENTS`. Across vocabularies (260 pairs, excluding the declared
tier↔type mirror) **seven land under the existing ΔE ≥ 15 floor**:

| ΔE | pair |
|---|---|
| 9.5 | `SR` `#0e7490` vs `phase[3]` `#155e75` |
| 10.5 | `Interface` `#7c3aed` vs `phase[7]` `#7e22ce` |
| 12.5 | `Process Guide` `#9a3412` vs `phase[2]` `#991b1b` |
| 12.7 | `LLR` `#64748b` vs `sw-node[component]` `#475569` |
| 14.2 | `sw-node[component]` `#475569` vs `phase[3]` `#155e75` |

and *within* `sw-node`, `external #334155` vs `component #475569` is **8.6** —
the closest pair in the document. `120-CRITIQUE` reported this class
independently, so it is confirmed live rather than merely computable.

**The floor is a judgement and must be recorded as one.** 15 is the phase-accent
precedent, chosen because every phase swatch can sit beside every other in one
legend. Two colours from *different* vocabularies meet less often, so a lower
cross-vocabulary floor is defensible — but `#0e7490` vs `#155e75` at 9.5 is the
pair a critic actually conflated. **Recommendation: keep 15 within a vocabulary,
and adopt 12 across vocabularies**, which clears the confirmed conflations
without forcing a wholesale re-hue. State the number and its reason in the LLR.

**Done-when:** a pairwise floor holds within *and* across every declared
vocabulary, with the two floors and their justification recorded; the ~5 offending
values are re-hued; the check runs on the constants (no fixture needed).

## WI-312 — A2: accessible-name quality, not merely presence

**Measured:** 0 empty names — but **57 bare-id-only** names (`IF-001` with no
description) and **14 duplicated names across 74 nodes**, worst
`'contains → descend'` **×39**. A screen-reader user hearing that thirty-nine
times cannot tell those controls apart. All three are regex-decidable.

**Core.** A name must be present *and*: not a bare registry id alone; unique
among its siblings; and, for a control with visible text, containing that text
(WCAG 2.5.3 label-in-name).

**Done-when:** the three rules hold over the full emitter sweep; the ~57 IF nodes
carry a real description; the `contains → descend` markers are disambiguated or
made presentational.

**Residue that genuinely stays:** given a name that is present, unique and
descriptive — is it the *right* description? That is small, and it belongs to
SR-054's judgement rather than to A2's structure.

## What stays perceptual after all four

`SR-054` keeps `Verification=Critique` on four clauses. Two of them (**T4**
truncation-affordance, **T7** viewport fit) are mechanizable with a browser
harness measuring bounding boxes and `scrollWidth` — a real but separate build.
Two (**T1** "the entry point is obvious", **T3** "the reader stays oriented")
describe a reader's experience and cannot be asserted about an artifact without
redefining them as proxies. **Retiring critiques entirely is a decision about
those two**, not a test-authoring problem — and until it is taken,
`perceptual-stale` keeps firing on every render commit.
