+++
id = "WI-645"
title = "Bring TC-061 and TC-161 up to their amended design rows, and name the two brief assemblers no design row names"
workstream = "requirements"
specref = ""
sr_refs = ["SR-026", "SR-146"]
needs = ["WI-642"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

Built by a builder session in its own worktree, reviewed, and squash-merged.
No behavior changed.

- `TC-061.method` and `TC-161.method` re-drafted to what their evidence files
  drive: each clause is held by a named test in
  `tests/test_agent_loop_worker.py` or `tests/test_adjudicate_brief.py`. Two
  corrections beyond the spec's list: a declared brief that cannot be filled
  is HELD for a human (the old "falls back to the worker assignment" is
  disproved by the tests), and the re-attestation model's seam is IF-075
  (IF-127 was merged into it).
- `TC-161.tier` moved from Smoke to Full on review: its method drives real
  git repositories, subprocesses and loop sessions, and its evidence module is
  registered slow.
- `amendment_values` and `first_approval_values` joined LLR-167's
  `code_symbol` (a traced cell), with `Implements:` back-links.
- `tests/test_adjudicate_brief.py`'s module docstring and section comments no
  longer say any shipped brief is unrouted (text only).
- The three amended cells on approved rows (TC-061 and TC-161 `method`,
  TC-161 `tier`) are left for an amendment adjudication; no approval record
  was refreshed.

Review: codex Sol (medium), NOT YET SOUND, one major (TC-161's tier), fixed.
The builder's out-of-scope findings (LLR-167 still says a refusal falls back;
LLR-167 names `dispatch.*` for the census; stale routing prose) are filed for
the follow-up amendment.

## Context

Drafted by WI-603 (its ## Dispositions section) and filed by hand with the
drafted title, since the loop is paused and no merge mints it.

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
lags. The verdicts:
`docs/reviews/wi-601-adjudicate-llr-061-approved/001-ADJUDICATE-f263118.md` and
`docs/reviews/wi-603-adjudicate-llr-167-approved/001-ADJUDICATE-f263118.md`.

## Done-when

- `TC-061.method` and `TC-161.method` each describe what their evidence file
  drives at the landing commit, and nothing their tests disprove.
- `tests/test_adjudicate_brief.py` no longer says any shipped brief is unrouted.
- `amendment_values` and `first_approval_values` are named in a design row's
  `code_symbol`, and `trace.py --strict-integrity` passes.
- The two TC amendments are left for an amendment adjudication, and no
  approval record is refreshed by this row.
