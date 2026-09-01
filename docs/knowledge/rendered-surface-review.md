# Rendered-surface review: layout priority, robustness, and accessibility of this repo's generated owner surfaces — DRAFT

> **DRAFT (agent-authored, WI-546, 2026-08-30).** Drafted by the unattended lane so the `hat.UX-DESIGNER`, `hat.UX-ENGINEER` and `hat.ACCESSIBILITY` roster entries have a shared `knowledge` value to point at; the owner reviews and cuts at RETURN, per the `hats.toml` header's own rule. This distills THIS repo's accumulated perspective from its own decisions and surfaces — it is not retrieved external research, and its claims are the drafter's reading, not a settled finding.

This pack is shared because three hats review the same objects from three angles.
The objects are this repo's **generated, owner-facing surfaces**: the root
`PROJECT_STATE.html` dashboard and the SVG views emitted by
`project-trajectory/scripts/gen_trajectory.py` (the `arch`/icicle, `dag`, and
software/how tabs); the owner decision surface `docs/open-items.html` from
`gen_open_items.py`; and the console reports the checkers print. In THIS repo the
two UX hats are ruled `always` (the `hats.toml` VALUES-DIVERGE note, lines 63–66)
because these are real pages a session reads to decide what to do next — not a
hypothetical adopter's UI. The bar for all three is written down: SR-052
(accessibility), SR-053 (cross-view uniformity), SR-054 (task-level usability) in
`docs/requirements/system-requirements.toml`.

## What each hat looks for here

### UX-DESIGNER — does the layout put the reader's decision first?
The charter asks who reads a surface and what decision they make on it, and
listens for "a surface that renders every fact it has instead of the one the
reader came for." Ground it in the two surfaces that already made this choice.
`gen_open_items.py` orders its output by what an owner needs to rule (pending
decisions, then approvals/re-attests, then pending actions — docstring "in the
order an owner needs it"), and it exists *because* the prior surface handed the
reader a pointer ("run `trace.py --approve modified`") they could not act from.
The dashboard starts panels collapsed past the greater-than-3 rule (the
`_know_panel` note near `gen_trajectory.py:934`) so density does not bury the
next step — SR-054's "start-collapsed" clause. When reviewing a new view, ask:
is there ONE reader and ONE decision named, and is the thing they came for above
the fold, or is the view a faithful dump of the registry it reads?

### UX-ENGINEER — does it hold at real widths, themes, volumes, and bad data?
The charter listens for "a view verified only by reading its generator, never by
looking at it rendered." This repo has a named cure: the `render-dashboard-critique`
skill (`project-trajectory/skills/`) screenshots `PROJECT_STATE.html` across a
declared width × theme × tab matrix (including the 390px mobile landing and the
graph-heavy `sw`/`dag` tabs) and reads the PNGs — because critiques historically
judged ~790 KB of markup, never pixels. Use it; do not accept "the generator
looks right." The data-state failures this repo has actually hit are the test
set: the EMPTY case is handled by rendering nothing and passing vacuously for an
absent/placeholder-only registry (`gen_trajectory.py` docstring ~:58/:85, guard
near :1040) — SR-070's "omit the view, never emit an empty one"; the HUGE case is
SR-054's "over the real registry volumes rather than a trimmed fixture, no label
clipped or overlapping"; the MALFORMED/edge case is why `_splice_flows_into_panel`
raises instead of silently truncating under `python -O` (the L-02 fix,
~:783–786). Note also the view-fallback trap at ~:863–872, where an empty node
set let a promised view silently go unmet (117-CRITIQUE). Robustness here means
verified rendered, at real volume, with the empty/huge/malformed branch exercised.

### ACCESSIBILITY — is keyboard / screen-reader / low-vision a stated bar?
The charter listens for "a surface whose acceptance names only how it looks to a
sighted mouse user." SR-052 is that bar made explicit and mechanical: every
interactive element keyboard-reachable and carrying an accessible name, no
information by colour alone, a readable contrast floor, swept over EVERY emitted
view (not a sample). The generator already carries the scaffolding to check
against — roving-tabindex tab keyboard nav with Arrow/Home/End
(`gen_trajectory.py:744–773`), `role`/`aria-selected`/`aria-controls` on the
tablist and panels (~:564–600), and `role="img"` + `aria-label` on the progress
meters (:541, :548). A review wearing this hat confirms those against SR-052's
acceptance rather than trusting they exist: is any focusable element hidden in a
container AT skips, does any status/phase/type encoding read through text or shape
with colour removed, does every text-and-fill pair clear the floor. The
listens-for failure is acceptance that says "renders cleanly" and nothing about
the keyboard or the screen reader.

## Application

- **Look at it rendered.** For any dashboard-appearance change, run
  `render-dashboard-critique` and read the PNGs across the matrix; file rendered
  defects as their own WIs (the skill builds eyes, it is not a redesign).
- **Name the reader and the decision** before judging layout; SR-054's findability
  clause is "each core reading task within one tab switch."
- **Exercise empty / huge / malformed**, not just the happy fixture: absent
  registry (omit, don't empty — SR-070), real registry volume (SR-054), and the
  degenerate branch that silently truncates (L-02) or renders the wrong view
  (117-CRITIQUE).
- **Check accessibility against SR-052's acceptance**, element by element, over
  every emitted view — keyboard reach, accessible name, colour-independent
  encoding, contrast floor.
- **Watch cross-view coherence (SR-053).** The same status word, colour, and
  interaction idiom must read the same across the dashboard, `open-items.html`,
  and the console — its charter is CONSISTENCY, but all three review hats meet at
  the seams between these surfaces.

## Open questions / bounded here

- **What is mechanically enforced today is not fully settled.** SR-052/053/054
  are Approved and phase-3 (aspect `trajectory`); each states its acceptance as a
  child-LLR chain, and SR-054 records one clause — a first-time reader in fact
  finding the entry points usable — that rests on a **recorded human judgement**,
  not a standing check. Treat that clause as owner-attested, not auto-verified.
- **The critique matrix is declared in `shoot.mjs`, not here.** Widths, themes and
  tabs are that file's constants; this pack does not restate them (single source).
  The runner is meta-only (Playwright is never shipped downstream).
- **Line locators are the drafter's reading at 2026-08-30** and drift as
  `gen_trajectory.py` changes; re-locate by the named symbol/comment, not the
  number, if it has moved.
- **SR-053's owning hat is CONSISTENCY, not one of these three** — included here
  because cross-view drift is what a reader of these surfaces experiences as
  untrustworthiness, and the three hats are where it surfaces.
