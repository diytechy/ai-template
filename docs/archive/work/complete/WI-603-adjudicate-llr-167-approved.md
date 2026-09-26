+++
id = "WI-603"
title = "adjudicate: LLR-167 - approved/routed cell(s) amended on merged trunk 3b004c4..f395907 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
+++

## Deliverable

Ruled in an attended sitting on `refactor_again` (the loop is paused), from the
before/after cells, against the design-row record last written at 2e1197fd:

    VERDICT: MEANING rows=1

LLR-167's `detail` moves in three places: `amendment` is now routed, `conflict`
is retired rather than shipped unrouted, and a consolidation assembler joins
with its own all-or-none rule and dissolved-overlap refusal. The traced
`code_symbol` gains `consolidate_values`. The verdict is
`docs/reviews/wi-603-adjudicate-llr-167-approved/001-ADJUDICATE-f263118.md`.

The design-row tier is released to the adjudicator, so the re-attestation is
this row's. The new text was judged blessable: it sits within SR-144, SR-146
and SR-148, it is true of `adjudicate_brief.py` at f263118, and five tests in
TC-161's evidence file pin it. The re-anchor is one separate commit, joint with
WI-601's LLR-061.

Two findings: TC-161's `method` still pins "the two unrouted briefs as
unrouted", which the blessed row and its own test contradict; and
`amendment_values` and `first_approval_values` are routed but named by no
design row. With WI-601's TC-061 finding they form the one disposition below,
filed by hand as WI-645 under the drafted title (the loop is paused, so no
merge mints it, and the mint's exact-title dedup keeps a later sweep from
minting it twice). It needs WI-642, so the TC amendments cannot ride unread
into the approval act's refresh of `test-cases.toml`.

Review: codex Sol (medium) confirmed the call, the blessing checks and the
disposition's scope and keys; its wording corrections are applied. A Fable
arbiter upheld the one-row count (WI-566's rule).

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-167 `Detail`: "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint); `compose` fills i…" -> "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint); `compose` fills i…"

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

## Dispositions

```toml
title = "Bring TC-061 and TC-161 up to their amended design rows, and name the two brief assemblers no design row names"
workstream = "requirements"
buildtier = "medium"
specref = "docs/test/test-cases.toml"
needs = ["WI-642"]
```

WI-601 and WI-603 ruled LLR-061 and LLR-167 MEANING and judged their new text
blessable, for one joint re-anchor of the design-row record. The two test cases
verifying them were not amended with them:

- `TC-161.method` still pins "the two unrouted briefs as unrouted", which the
  amended LLR-167 and `test_every_shipped_brief_is_routed_and_the_retired_one_is_gone`
  both contradict, and it does not name the consolidation arm or its refusals
  (no declared scope, no digests, a dissolved overlap). The module docstring of
  `tests/test_adjudicate_brief.py` and the section comment
  `# --- the discriminator, and the two briefs that stay unrouted` say the same
  stale thing.
- `TC-061.method` does not name the multi-row assignment block, which
  `tests/test_agent_loop_worker.py` already drives.
- `amendment_values` and `first_approval_values` are routed assemblers that no
  design row's `code_symbol` names.

IN SCOPE: re-draft `TC-161.method` and `TC-061.method` so each names what its
evidence file drives today, and correct the stale docstring and comment in
`tests/test_adjudicate_brief.py`. Put the two unnamed assemblers in a design
row's `code_symbol`, either LLR-167's or a design row that owns them, whichever
the traced text supports. Those are traced cells, so no re-attestation follows.
The two TC re-drafts are amendments to approved rows and owe an adjudication
before the next refresh of `test-cases.toml`.

NOT IN SCOPE: any change to `adjudicate_brief.py` or `agent_loop.py`
behavior. The code matches the blessed rows, and only their test-case text
lags.
