+++
id = "WI-@H@"
title = "Amend LLR-140 and LLR-154 to the claim and mint as built, and move TC-144's scratchpad clause to the chain that owns it"
workstream = "requirements"
specref = "docs/requirements/low-level-requirements.toml"
sr_refs = ["SR-156", "SR-026"]
needs = ["WI-647"]
buildtier = "medium"
safety_class = "spine"
priority = 4
+++

## Context

Found while adjudicating the bookkeeping helper's amendments (WI-648), and by
the codex review of that verdict, which judged LLR-140 blessed although two
of its clauses are false:

- LLR-140's refusal ladder lists a "non-ordinary safety_class" rung that the
  claim no longer has (`integrate._claim_refusal` says the arm was deleted and
  runs SpecRef and status-prose refusals instead), and omits the rungs added
  since.
- LLR-140's "commits only the paths the claim wrote" is stronger than the
  helper: it commits every changed path inside its declared scope. WI-647
  moves the writes into a scratch worktree under a drift check, which narrows
  that window to what IF-186's contract then states; the amendment should
  say exactly that.
- LLR-154 says the mint commits "the declared generated set"; the mint
  commits through the bookkeeping helper, which stages only the step's scope.
- TC-144 (verifies SR-156, LLR-150) gained a clause about the dispatcher
  reading past a dirty owner scratchpad; that behavior belongs to LLR-143
  under SR-026, so the clause sits in the wrong chain (the test proving it is
  `tests/test_dispatch.py::test_a_dirty_owner_scratchpad_does_not_stop_the_drive`).

IN SCOPE: draft the LLR-140 and LLR-154 `detail` amendments to match the code
after WI-647 lands (read the claim and the mint as built), and move TC-144's
scratchpad clause to a test case in LLR-143's chain (amend both methods). The
amendments owe an amendment adjudication before the next refresh of the
design-row and test-case records; they can join the wave's joint adjudication.
Citing `tests/test_bookkeeping.py` from a test case is WI-647's.

## Done-when

- LLR-140's ladder and commit scope, and LLR-154's commit scope, each match
  the code at the landing commit.
- TC-144 states only SR-156/LLR-150 behavior, and the scratchpad clause is in
  a test case of LLR-143's chain.
- No approval record is refreshed by this item, and the commit bar passes.
