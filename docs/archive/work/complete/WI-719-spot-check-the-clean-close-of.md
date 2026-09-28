+++
id = "WI-719"
title = "spot-check the clean close of WI-620 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

Spot-checked by an independent Fable adjudicator, then cross-reviewed by
Codex Sol in two rounds (wave-5 ruling 57): NOT YET SOUND on the first,
SOUND on the correction
(`docs/reviews/2026-09-27-wave5/sol-wi719.md`, `sol-wi719-fix.md`).

The machine line is `OUTCOME: FOLLOW-UP drafts=0`. Of WI-620's nineteen
clauses (its own six, plus the thirteen it quotes from WI-605, WI-606 and
WI-551):
- thirteen are met;
- one is met by supersession, WI-606's "no new field mapping";
- four clause parts are not met, and are openly owed: WI-605's first
  corrected-occupancy log, WI-606's and WI-551's recorded-fixture clauses
  for codex and opencode, and WI-606's opencode pathway re-check on 1.18.29.

The close stands. The owed parts had no open home, so the coordinator
folded them into WI-541's Context and Done-when, as the verdict proposed.
WI-541's live runs on this box produce exactly that evidence. The verdict
is `docs/reviews/wi-719-spot-check-the-clean-close-of/001-SPOTCHECK-d7e1be0e.md`.
Its one observation, a stale sentence in `session_adapters.py`'s module
docstring about which module imports it, was corrected at the merge.

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-620-one-session-service-for-every.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.

## Follow-up: fold into WI-541, no row drafted

Verdict: `docs/reviews/wi-719-spot-check-the-clean-close-of/001-SPOTCHECK-d7e1be0e.md`,
governing line `OUTCOME: FOLLOW-UP drafts=0`. Nineteen clauses checked
(WI-620's six, and the quoted WI-605 three, WI-606 five, WI-551 five):
thirteen met, one met by supersession (WI-606's "no new field mapping", whose
condition — capture without S7's adapter — never existed once both landed in
one lane), four not met in whole or part and openly owed in the Deliverable,
the log and the commit body, and WI-620's roll-up clause met except in those
four parts. The owed parts: WI-606's third and WI-551's third for codex and
opencode — the clauses ask for tests over fixtures *recorded* from the CLI,
and `codex-exec-json.jsonl`, `codex-rollout.jsonl` and
`opencode-run-json.jsonl` are built from documented shapes, which is not that
however openly labelled (ruling 57; they say so on their first line, in the
test module and in TC-262/263/264/267); WI-606's last clause (the opencode
pathway checks re-run on the installed 1.18.29, `docs/agents.toml` still
reading 1.17.18); and the log-fragment half of WI-605's third (the first
session log under the corrected occupancy, which no lane can write while
`docs/work/pause` holds). The cited
modules are green on this tree (295 passed / 2 skipped). The one-path claim,
the 218/411 SLOC figures, the OTel pin, the two claude defects, the inert
dial and the keep-warm log were each driven against the code, the tests or
the diff.

The gap is a home, not a lapse: the owed items live only on closed surfaces
(the archived spec, the log). They belong on WI-541, whose live runs on this
box already produce them, so nothing is drafted here; the verdict names the
three Done-when bullets for the coordinator to fold into WI-541 (record the
codex and opencode fixtures live; re-run the opencode pathway checks and
record the version tested; name the first corrected-occupancy log).
