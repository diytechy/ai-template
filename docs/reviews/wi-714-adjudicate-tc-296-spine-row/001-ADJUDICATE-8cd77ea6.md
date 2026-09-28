# ADJUDICATE — WI-714 — first approval at 8cd77ea6

Independent adjudication of the one spine row WI-711 re-authored `Drafted` on
merged trunk (the dashboard's de-emphasis contrast check, usability anchor
T5), which the `human_approval_through = "DevStg-Boundary"` dial releases to
an adjudication session: TC-296, returned by WI-704's adjudication on one
sentence of its `Method` and amended in that one cell. The one question: is
the row ready to be APPROVED as it stands, or does it go back with findings.
`Approved` blesses the row's TEXT; the harness answers whether its test
passes, and I ran it anyway.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chain of SR-054 in full; anchor
`docs/archive/last_approved` copied at e7fe487d for the TC registry). The
row was read upward (SR-054 and LLR-285, both approved, act seq 4 and 6),
sideways (the nine approved T-anchor LLRs and their TCs, TC-122 and TC-125 in
particular as the sweeps that keep the shipped artifact) and downward (the one
evidence pointer resolved and read in full; `_every_emitter_document` located
in `tests/traj_fixtures.py` as the `Parameters` cell says). The brief does not
render the routed `Verifies` cell, so it was read from the live registry and
is ruled below. Disclosure: I read WI-714's queued spec for its Context, the
WI-704 verdict for what was returned, the spine-authoring skill, and the
arbitration file (ruling 52) as context only. HEAD stayed at 8cd77ea6.

- [APPROVE] TC-296 -> sweep every fresh emitter document, one fixture per emitter, leaving the committed dashboard out for a standing reason; derive from each stylesheet every rule putting a de-emphasis state class on a node shape that document draws with a label; model the paint as the browser applies it (shorthand filter functions as sRGB colour matrices, then opacity over the page surface), refusing a rule that sets any other property or names an unmodelled function; resolve each reached node's fill, label ink (inline, else the most specific stylesheet rule) and, where it carries a descend arrow, its per-node ring ink or the accent fallback, in both themes over both surfaces, and assert 4.5:1; assert the sweep reached block, cell, wi and knode with the arrow among them -> the one evidence pointer resolves (`tests/test_traj_render_sweeps.py::test_t5_a_deemphasised_node_keeps_body_text_contrast_in_both_themes`, line 906) and does exactly this at HEAD: `if label == "shipped": continue`; `_deemphasis_rules` deriving rules from `DEEMPHASIS_STATES` against the nodes the page draws with `<text`; `_deemphasis_paint` asserting `set(props) <= {"opacity", "filter"}` and `_filter_matrix` asserting `saturate`/`grayscale` only; `_label_ink` inline-else-most-specific; `_node_inks` reading `--ring` or `--accent`; `THEME_SURFACES` over both themes and `--surface`/`--bg`; the floor `T5_BODY_FLOOR = 4.5`; and the non-vacuity floors `{"block", "cell", "wi", "knode"} <= shapes`, `kinds["arrow"] >= 10`. `_every_emitter_document` builds exactly seven fresh fixtures (flat-dag, knowledge-tiered, knowledge-flat, tiered-drill, how-sw-drill, how-sw-flat, process), as `Parameters` says. The returned sentence is now the standing reason and nothing else: "the case asserts the current emitter, which only a document rendered now evidences, and the committed artifact's freshness is SR-070's contract" — true of the system whatever the committed file's state (it is up to date at HEAD and the sentence no longer claims otherwise), a registry id as its only anchor, no history or status a reader could reconstruct a correction from, and consistent with TC-122 and TC-125 keeping the shipped artifact for a different claim (a property the artifact must hold as shipped). `Verifies` HOLDS: SR-054 (labels readable at default zoom — the legibility clause this case holds at the body-text floor in the de-emphasised state) and LLR-285 (the row whose Detail this case verifies clause by clause, its `--mute` token the one declared property the modelled rules set). Expected names the condition and its non-vacuity floors; Level Unit matches its siblings TC-122 and TC-125; Tier Full honest — `test_traj_render_sweeps` is in `tests/conftest.py` `SLOW_MODULES`; Automated Yes; every other cell byte-identical to the text WI-704 found blessable. Ran: 13 cases pass in the module -> ready.

## How the chain and the anchor were read

- Upward: SR-054 as the brief printed it (approved, re-attested at act seq
  6); LLR-285 (approved at act seq 6). Sideways: LLR-055, LLR-099, LLR-100,
  LLR-105, LLR-115, LLR-116, LLR-117, LLR-119, LLR-120 and their TCs, none
  claiming the de-emphasised state. Downward: the evidence pointer and its
  helpers (`_deemphasis_rules`, `_deemphasis_paint`, `_reached_nodes`,
  `_node_inks`, `_deemphasised_pairs`) read in full; the fixture list read.
- The one cell that changed since WI-704's return is `Method`, and only its
  parenthesis (the diff at 78fd8fcd shows nothing else), so WI-704's readings
  of every other cell stand and were re-checked, not assumed.
- Anchor: TC-296 is `Drafted` in the TC copy at e7fe487d, so this is a first
  approval, not a re-attest. The act names the TC registry, shared with
  WI-712's rows in the one batch-E snapshot.

## Bar I produced (not claimed)

On this tree, `python -m pytest -q -n 4 tests/test_traj_render_sweeps.py -p
no:cacheprovider`: **13 passed in 14.82s**, no failures, no errors.
`gen_trajectory.py --check`: "project-state dashboard up to date" (rc 0).

OUTCOME: APPROVE rows=1
