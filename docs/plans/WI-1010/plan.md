# WI-1010 plan: the page shows the assumptions owed, then every requirement states its argument

Planned on branch `maint/wi-1010` at `1ee58e149`, a maintenance branch cut
from trunk `refactor_again` at `1cb2e8680`. Read in full: the row and its
scope critique; SR-193, SR-194, SR-203, SR-205, SR-211, SR-212; the 21
requirements and SR-235 with their needs, siblings and design rows; DA-001 to
DA-020 and SUR-001 to SUR-003; the frame (`external.toml`); IF-074, IF-075,
IF-080, IF-226 and the coordinator's interface rows (IF-271 to IF-290);
`check_assumption_gate.py` and the gate's rules in `assumption_rules.py`;
`trace.assumption_brief_lines` and `assumptions_owing`; section 2 of
`gen_open_items.py`; `acceptance_record`'s cell split.

## Construction

### 1. The page

1. **One model** (`trace.py`). `assumption_owing_model(root, srs, tcs,
   ids=None)` returns `[(id, why, moved cells, chain)]`: each assumption and
   surrogate `assumptions_owing` reports (or each id `ids` names), with the
   chain `assumption_rules.assumption_chain` builds for it. An id the
   registry does not declare refuses, as the brief does today.
   `assumption_brief_lines` renders that model and no longer gathers its own.
   The brief's text does not change.
2. **The cards** (`gen_open_items.py`). `_need_cards`' card body becomes
   `_owing_card(rid, why, cells, row, after="")`: moved cells before and after
   with the rest of the row as context, or every cell whole. `_need_cards`
   and the new `_assumption_cards(model)` both call it, so a need and an
   assumption read alike. An assumption's card adds "Relied on by" (each
   citing requirement's id, title and text); a surrogate's adds "Named by"
   (each assumption naming it, with its text). The block's heading is the
   brief's own, "Assumptions and surrogates owing an acceptance".
3. **The page around it.** `render` calls the model once. §2 is SR chains,
   then needs, then assumptions; the empty message prints only when all
   three are empty and names the assumptions registry as checked. The header
   counts the assumptions and surrogates owing, and its drifted count takes
   in a drifted one. The module docstring's section list and the
   `Contract IF-074:` block say it; `trace.py`'s `Contract IF-075:` names the
   new function.
4. **Size.** `gen_open_items.py` measures 938 code lines by the ratchet's own
   `module_sloc` (the brief's 996 did not reproduce). The cards add about 40
   and the shared card body takes some of `_need_cards`' lines back, so it
   stays under the 1000-line threshold with no baseline entry. `trace.py` is
   pinned exactly; its re-stamp names this row.

### 2. The arguments

Registry rows, plus two contract blocks in docstrings.

- **Coincident waivers** where the requirement's own behaviour is the outcome
  the reader meets, with no party between: SR-024, SR-129, SR-226, SR-231,
  SR-232, SR-234, SR-236, SR-238, SR-241, SR-242, SR-245.
- **Existing assumptions** where one truly carries the argument: SR-247 on
  DA-014 (an adopter upgrades by the documented route, which names the
  migrator); SR-246 on DA-004 (the hook floor is not bypassed, for its staged
  arm) and DA-013 (work reaches trunk only through the gated path, for its
  lane arm); SR-243 on DA-016 (a codex runner serves its default provider,
  which its usage record names); SR-235 on DA-007 (the independent reviewer
  adds evidence, which its record keeps).
- **New assumptions**, `Drafted`, from DA-021: the agent CLI keeps its hook
  contract (SR-229, SR-230, SR-237); its transcripts record the session as it
  ran (SR-229, SR-244); the recorded and built Claude Code records the guard's
  tests use are faithful, a fidelity assumption on B-10 realized by a new
  surrogate SUR-004 (SR-229, SR-230); a coordinating session acts on the
  coordination instructions the kit publishes and injects (SR-237, SR-243,
  SR-244); an agent chooses a skill by its description (SR-224); a CLARITY
  ruling rules as the operator would (SR-228); the kit runs in the normal
  working environment the review threat model names, and the sessions ruling
  findings apply its directions (SR-233).
- **Interfaces.** IF-080's `bridged_by` gains the two agent-CLI assumptions.
  IF-275 ties back to B-04, bridged by the hook assumption. IF-289 ties back
  to B-05, coincident. New rows: IF-321 (the verdict file an adjudicator
  writes at the path `coordinator_adjudicate` reserved, from B-10) and IF-322
  (the dispute verdict in `kitlib.dispute`'s grammar, from B-10), each
  coincident, each with its `Contract` block in its owner's docstring.
  `tests/test_frame_context.py`'s pin of the untied rows and of B-10 moves
  with them. SR-235's crossing is re-pointed from B-05 to B-09.

Checked in memory before writing a row: with these cells,
`crossing-allocation` and `interface-allocation` report 0, and every
`assumption-gate` line is a `Drafted` assumption or surrogate (79 lines).

## Files

`project-trajectory/scripts/trace.py`, `gen_open_items.py`,
`coordinator_adjudicate.py` (docstring), `kitlib/dispute.py` (docstring);
`project-trajectory/RESYNC_PACK.md`; `tests/test_open_items_assumptions.py`
(new), `tests/test_frame_context.py`, `tests/test_module_size_ratchet.py`;
`docs/requirements/assumptions.toml`, `system-requirements.toml`,
`low-level-requirements.toml`, `interfaces.toml`; `docs/test/test-cases.toml`;
`docs/status.md`; the regenerated views.

## The arms the tests pin (TC-448)

- A `Drafted` assumption, a `Drafted` fidelity assumption, its `Drafted`
  surrogate and a lone `Drafted` surrogate each get a card; an `Accepted`
  assumption that has not moved gets none. A first-acceptance card shows each
  cell whole, past the page's clip, and no diff marks; an assumption's card
  names each requirement relying on it with its text, and a surrogate's names
  the assumptions naming it.
- An accepted assumption whose text moved after the snapshot gets a card
  marked DRIFTED with the moved words before and after, and the header's
  drifted count takes it in.
- The page's assumption cards are exactly the rows the brief's model returns,
  in its order, and the header counts them; with only assumptions owing, §2
  does not print its empty message.
