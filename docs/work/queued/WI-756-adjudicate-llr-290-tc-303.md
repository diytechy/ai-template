+++
id = "WI-756"
title = "adjudicate: LLR-290, TC-303 - spine row(s) authored Drafted on merged trunk 183ff1c..ba0ea43 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-290", "TC-303"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-290 authored in `docs/requirements/low-level-requirements.toml`
- TC-303 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Dispositions

The adjudication is recorded at
`docs/reviews/wi-756-adjudicate-llr-290-tc-303/001-ADJUDICATE-6e89705.md`,
under the governing line `OUTCOME: RETURN rows=2`. LLR-290 and TC-303 are
RETURNED and stay `Drafted`, every cell byte-exact. This is one draft: one lane,
and one adjudication at its merge.

```toml
title = "LLR-290/TC-303 return: state that a retained session's compacted flag and source hold for its later calls, and verify that and the reported-over-inferred precedence"
workstream = "process"
safety_class = "spine"
buildtier = "quick"
priority = 3
specref = "docs/requirements/low-level-requirements.toml"
sr_refs = ["SR-227"]
bar = "DevStg-Tests"
```

IN SCOPE: exactly the text additions below, copied as written, in the two
Drafted rows, plus two tests. `Status` stays `Drafted`. Do not reword, extend or
"improve" any other part of these cells or of any other cell. No code change:
the code already behaves as the added text says (confirmed at 6e89705b).

THE DEFECT, confirmed at 6e89705b. `_observe_compaction` (`session_keep.py`)
starts each call from the record's `compaction_source` and never clears it
within a record. So once a session's compaction is inferred, every later call's
row carries `compacted: True` and `compaction-source: inferred` without new
evidence. A probe over rollouts [35911], [35911, 15717] and
[35911, 15717, 18000] printed `True inferred` on calls 2 and 3. LLR-290 does not
say this, and a per-call implementation satisfies its text equally. Separately,
LLR-290's "Reported evidence takes precedence over inferred evidence" has no
test with competing evidence.
`test_codex_reported_rollout_compaction_takes_precedence` has no prompt drop.

1. **LLR-290 (Drafted)**, `detail`: after `Reported evidence takes precedence over inferred evidence.` append ` Once recorded, compacted and its source hold for every later call of that retained session, though the call shows no new evidence; a reported entry replaces an inferred source, and an inferred drop never replaces a reported one.`
2. **TC-303 (Drafted)**, `method`: after `a legacy record with no rollout cursor learns the latest prompt and cursor before inferring.` insert ` After an inferred compaction, a later call whose new requests only rise still carries compacted with source inferred; a compacted entry arriving after an inferred source marks it reported, and a later drop leaves a reported source reported.`
3. **Tests** in `tests/test_session_keep.py`, using the existing `_codex_rollout` / `_codex_turn` helpers and the compacted-entry envelope variant from `test_codex_reported_rollout_compaction_takes_precedence`: (a) rollout [35911], then [35911, 15717], then [35911, 15717, 18000]; assert the third call's `compacted` is True with source `inferred`. (b) An inferred source followed by a call whose thread rollout also holds a compacted entry yields `reported`. A further drop after that leaves it `reported`. Nothing else in either row changes.
