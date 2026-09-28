# ADJUDICATE — WI-704 — first approval at 126cf5f2

Independent adjudication of the two spine rows WI-701 authored `Drafted` on
merged trunk (the dashboard's de-emphasis contrast check, usability anchor
T5), which the `human_approval_through = "DevStg-Boundary"` dial releases to
an adjudication session: LLR-285 and TC-296. The one question: is each row
ready to be APPROVED as it stands, or does it go back with findings.
`Approved` blesses the row's TEXT; the harness answers whether its tests pass,
and I ran them anyway.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chain of SR-054 in full; anchor
`docs/archive/last_approved` copied at eecd656d for the LLR and TC
registries). Both rows were read upward (SR-054, SN-023, SN-024), sideways
(the nine approved T-anchor LLRs and their TCs) and downward (the one evidence
pointer resolved and read; the named symbols and the `--mute` token located in
`gen_trajectory.py`, `traj_render.py` and `traj_panels.py`). Disclosure: I
read WI-704's queued spec for its Context and the spine-authoring skill; the
arbitration file was context, never evidence. HEAD stayed at 126cf5f2; the
worktree was clean before this file was written.

- [APPROVE] LLR-285 -> the rules that de-emphasise a label-bearing node (the drill's trace-muted block, the hover dim of the icicle cell, the flat-roadmap work item and the knowledge concept) set one declared page token, `--mute`, a partial desaturation, and nothing else, so a node's label ink and fill are not blended toward one another and the label and the descend arrow clear the body-text floor 4.5:1 against the de-emphasised fill in both themes; a connector keeps its opacity fade; scope: a de-emphasis rule sets opacity or a filter and nothing else, shorthand filters modelled as colour matrices; an engine ignoring the filter loses the emphasis, not the contrast; whether what remains reads as a selection stays perceptual under LLR-055/TC-055 -> SR-054 asks that labels stay readable and that detail is revealed without losing context, and the ACCESSIBILITY lens (own `Hat-Refs`, earned: no parent carries it, and its `listens_for`, "a surface whose acceptance names only how it looks to a sighted mouse user", is exactly the low-vision failure a 1.6:1 muted label is) is the row's own; the rationale says what breaks under the obvious alternative (opacity collapses ink against fill; a .35 fade measured 1.6:1 to 2:1; clearing 4.5:1 by opacity needs .98) and which second alternative lost (a precomputed muted fill per node, doubling every emitter's fills and markers). Every clause true at HEAD: `gen_trajectory.py` declares `--mute:saturate(.2)` at `:root` and `.cell.dim, .wi.dim { filter:var(--mute); }`; `traj_render.py` DRILL_STYLE `.drill[data-focused-trace] .block.trace-muted{filter:var(--mute);}` with the wire keeping `opacity:var(--o-muted)`; `traj_panels.py` `_know_panel` `#knowgraph .knode.dim{filter:var(--mute);}` — the four shapes, one token, no other property. Sideways it takes T5's de-emphasised state, which LLR-105 (the ring and arrow against the host fill) does not claim, and says where the residue stays; Module and CMP-009 resolve -> ready.
- [RETURN] TC-296 -> sweep every fresh emitter document, one fixture per emitter, derive from each stylesheet every rule putting a de-emphasis state class on a labelled node shape, model the paint as the browser applies it (shorthand filters as sRGB colour matrices, then opacity over the page surface, refusing any other property or an unmodelled function), resolve each reached node's fill, label ink and per-node ring ink or accent fallback in both themes over both surfaces, and assert 4.5:1; assert the sweep reached block, cell, wi and knode with the arrow among them -> the one evidence pointer resolves (`tests/test_traj_render_sweeps.py::test_t5_a_deemphasised_node_keeps_body_text_contrast_in_both_themes`, line 906) and does exactly this, passing (13 collected in the module); Tier Full is honest for a `SLOW_MODULES` module; Level Unit, Verifies SR-054 and LLR-285, and the non-vacuity thresholds (four shapes, >= 100 label checks, >= 10 arrow checks) all hold -> NOT ready on one sentence of `Method`: "(the committed dashboard is an older renderer's markup, so it is left out)". That parenthetical states the row's own status at the moment it was written, not the standing system — and it is already false at HEAD: `python project-trajectory/scripts/gen_trajectory.py --check` reports "project-state dashboard up to date", so the committed dashboard IS the current renderer's markup, while the test still leaves it out. A reader with no history reconstructs the correction ("so the committed file used to lag") and, worse, reads a false premise for the exclusion. The standing reason is that this case asserts the CURRENT emitter, which only a document rendered now can evidence, whereas the committed artifact evidences whichever renderer last wrote it (its freshness is SR-070's contract, not this case's); the sibling sweeps that include the shipped artifact (TC-122, TC-125) judge a property the artifact must hold as shipped, which is a different claim. The remedy is one clause: keep the exclusion, state that reason. Every other cell is blessable as it stands. Drafted in `## Dispositions` of WI-704's spec.

## How the chain and the anchor were read

- Upward: SR-054 as the brief printed it (approved, re-attested at act seq 4);
  SN-023 and SN-024 from the needs registry; the hats roster for ACCESSIBILITY.
  Sideways: LLR-055, LLR-099, LLR-100, LLR-105, LLR-115, LLR-116, LLR-117,
  LLR-119, LLR-120 and their TCs, each an anchor's mechanized core, none
  claiming the de-emphasised state. Downward: the one evidence pointer read in
  full, `_deemphasis_rules` / `_deemphasis_paint` / `_reached_nodes` /
  `_node_inks` located beside it; `_every_emitter_document` located in
  `tests/traj_fixtures.py` as the `Parameters` cell says.
- Anchor: neither row is in the LLR/TC copies at eecd656d, so nothing here is
  a re-attest. The act names the LLR registry for this row (LLR-285 is
  approved); the TC registry token this row would have contributed is dropped
  for WI-704 — TC-296 stays `Drafted` inside the TC copy that WI-705 and
  WI-709 carry, which is what it is.
- Smoke-tier check: TC-296 is `Full`; its module is in `SLOW_MODULES`, which
  is consistent.

## Bar I produced (not claimed)

On this tree, `python -m pytest -q -n 4 -p no:cacheprovider` over the six
modules batch D's rows cite: **166 passed in 51.26s**;
`tests/test_traj_render_sweeps.py` collects 13. No failures, no errors.
`gen_trajectory.py --check`: "project-state dashboard up to date" (rc 0).

## Dispositions

Drafted in `docs/work/queued/WI-704-adjudicate-llr-285-tc-296.md` under
`## Dispositions` (one `toml` block): re-word TC-296's `Method` parenthetical
to the standing reason for excluding the committed artifact, then the
first-approval adjudication the merge's sweep mints.

OUTCOME: RETURN rows=2
