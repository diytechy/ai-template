+++
id = "WI-332"
title = "Owner-raised 2026-07-27 at the re-attestation sitting: the open-items view showed WHICH CELLS MOVED and nothing else, so a rewritten Rationale arrived with no Requirement beside it - and the collapse checkbox implied a fuller reading that did not exist. gen_open_items now renders the rest of every row under the same control: for a changed row the cells the diff had no reason to show (empty cells dropped, changed cells NOT repeated - an unmarked second copy of the text under review is what an attestation must not carry), and for a section whose SR only flipped Status, the SR text the chain hangs from."
workstream = "docs"
needs = ["WI-322"]
buildtier = "quick"
priority = 2
safety_class = "ordinary"
order = 329
+++

## Deliverable

gen_open_items.py: _context_block() + the SR-level fallback in _attestation_cards (srs_by_id, sourced from the registries the renderer already loads - the attestation model in trace.py is untouched, so no second opinion about what changed). Toolbar label states BOTH halves and carries a hint line; the JS toggles one body class so the text collapse and the cell collapse cannot disagree; a <noscript> block reveals the context when the control governs nothing. Label-beside-value grid, because the stacked field shape pushed the next diff a screen down. Two guards in tests/test_gen_open_items.py, both mutation-proven (drop the block / drop the skip-set / drop the SR fallback -> each fails); runtime toggle verified in Chromium at 1280 light+dark, which the stdlib tests state they cannot drive. No spine amendment: LLR-118 already scopes this module as the RENDERER and enumerates no affordance (the collapse toggle is not in it either), so the row is unchanged and the open window is not enlarged.
