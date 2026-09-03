# WI-579 — REVIEW-A round 007 (reviewed `01fe742`, relaxed)

Scope: `git diff contract_split...HEAD` excluding session telemetry, verdict
records and generated artifacts. Requirement surface read: the archived spec
`docs/archive/work/complete/WI-579-the-verdict-carrier-and-the-ad.md`
(Done-when, including the quoted WI-558/559/560 items), `LLR-140`, `LLR-207`,
`LLR-208`, `IF-046`, `IF-047`, `IF-175`, `TC-205`, `TC-206`,
`docs/process.toml [attestation]`, `docs/stack.ini`, `RESYNC_PACK.md` and the
`session-protocol` skill.

## Instruments (run here, once each)

- `python project-trajectory/scripts/check.py --jobs 0` → `RESULT: PASS`
  (`verdict-rollup` SKIP with its siblings: "work branch
  'wi-579-the-verdict-carrier-and-the-ad' — generated freshness is the trunk
  lane's").
- `python project-trajectory/scripts/trace.py --strict-integrity` →
  `Traceability: SN=27 SR=76 LLR=190 TC=189 orphans=2 integrity=0 ... Report ->
  docs/test/report.md`.
- `python -m pytest -q -n auto -m smoke` → `1500 passed, 8 skipped in 24.27s`
  (1508 collected against the re-stamped `max-tests = 1560`; 24.4 s wall against
  the 60 s ceiling — the `docs/stack.ini` re-stamp's figures reproduce on this
  box).
- `python -m pytest -q tests/test_verdict_record.py tests/test_integrate_admission.py`
  → `78 passed in 21.19s`.
- `python project-trajectory/scripts/gen_verdict_rollup.py --check` → exit 1,
  listing 43 absent rollups (the correct answer on a work branch; the step
  stands down there and the trunk step writes them).

## What was driven, not read

The shipped `integrate._verdict_gate`, `integrate._work_tip`,
`agent_loop.review_owed_by_evidence`, `agent_loop.review_verdict_trailer` and
`kitlib.verdict.branch_trailers` were exercised on real two-branch git
fixtures built from `tests/test_verdict_record.rounds_repo`, including a
genuine `Bar-Green`-attested station refresh commit and a coordinator-stamped
double round at one governing tree. The pre-fix predicate for
`review_owed_by_evidence` (`glob("*-REVIEW-?-<head7>*.md")`) was replayed on the
regression fixture: it answers `owed=True` where the post-fix reader answers
`False`, so `test_the_review_owed_derivation_and_the_gate_share_one_definition`
does fail on the pre-fix behaviour.

## Done-when coverage

WI-558 DW1/DW2/DW3/DW4/DW5, WI-559 DW2/DW3 and the dial (`process.toml`,
template, `enforcement-audit.md`, `RESYNC_PACK.md`) are each covered by a named
test in TC-205/TC-206 and reproduce here. **WI-560 DW1 ("ONE shared definition
… used by both the merge slot and the C2 review-owed derivation") is covered
only for the record-path commit class; the refresh-commit class is UNCOVERED
and the two readers measurably disagree there** — finding 2.

## Findings

- [MAJOR] project-trajectory/scripts/kitlib/verdict.py:393 -> `branch_trailers` iterates `git log` output, which is NEWEST-FIRST, and assigns `by_tree[tree] = (word, rounds)` unconditionally, so for a tree carrying more than one coordinator attestation the OLDEST trailer is what survives; driven end-to-end, two honest rounds at one governing tree (`review_verdict_trailer` stamping `rounds=1` then `rounds=2`) make the shipped gate return `wi-401: the Review-Verdict trailer for this tree says APPROVE rounds=1 while the round files say APPROVE rounds=2 - the attestation and the evidence disagree`, i.e. a false forgery accusation that parks a legitimately-approved lane at a supervisor stop — the OI-76 failure mode, re-created by the cross-check meant to prevent it, and reachable on any re-drawn round (`latest_phase_verdicts` exists precisely because "a phase was re-run at the same commit") -> take the NEWEST attestation per tree (iterate `reversed(log.split("\x1e"))`, or guard the assignment with `if tree not in by_tree` given the newest record is emitted first) and pin it with a two-trailers-at-one-tree case in `tests/test_verdict_record.py`; the defect cannot be made unrepresentable by construction because the carrier is a git commit history whose order the module does not own — the smallest change that makes the fix unnecessary (the `antidote` skill's question) would be for `branch_trailers` to return the ordered SEQUENCE of attestations rather than a last-write-wins map, so no reader can silently receive a superseded one -> @owner
- [MAJOR] project-trajectory/scripts/agent_loop.py:3358 -> `review_owed_by_evidence` computes `want = kverdict.tree_identity(root, "HEAD")` while `integrate._verdict_gate` computes it at `_work_tip(root, branch)` — the refresh-peeled work sha — so the "ONE shared definition, two readers" the spec's Done-when 2 (WI-560 DW1) demands is only shared for commits the identity already ignores; driven on a fixture with a genuine `refresh: wi-401 onto trunk` commit carrying a verified `Bar-Green: tree=… work=…` trailer, `id(HEAD)=19f621f3…` vs `id(work_tip)=4fff62ba…`, and the loop answers `owed AFTER refresh: True` while the gate answers `None` (satisfied) at the same instant, so a resumed lane on a refreshed branch (dispatch's `_maybe_refresh`, or the hand refresh dispatch.py:210 names) draws a redundant strong-tier round whose round file the gate will not even read — the double-round class the Deliverable calls "unrepresentable, not policed" -> make the loop read the same peeled tip (call `integrate._work_tip`, or lift the peel into `kitlib.verdict` so the identity has ONE owning boundary that both readers are handed rather than each choosing its own rev) — that is the construction fix, not a guard, and no test in TC-205 places a refresh commit between a round and either reader -> @owner
- [MINOR] project-trajectory/scripts/kitlib/verdict.py:185 -> `fold_listing` matches `is_record_path` against the raw `git ls-tree` field, but git QUOTES any path holding a non-ASCII or special character (`"docs/reviews/002-REVIEW-A-abcdef\303\251.md"`), so the leading `"` defeats every `startswith(prefix)` test and the record file folds INTO the identity — driven: the same tree with and without one such round file gives `ca98f20ada1329a7` vs `06b5f2263364f628`, meaning a hand-named `docs/log.d/` fragment carrying an accent silently stales every governing verdict on the branch, the exact class `RECORD_PREFIXES` exists to prevent -> pass `-z` (or `-c core.quotePath=false`) in `tree_identity` and unquote in `fold_listing`, with a quoted-record-path case in the pure identity tests; a guard is not the shape here — the smallest change that makes the fix unnecessary (the `antidote` skill's question) is for the fold to consume an already-decoded path list, so no reader ever sees git's display encoding -> @owner
- [MINOR] project-trajectory/scripts/agent_loop.py:1453 -> the DONE banner renders `"{} review round(s) approved".format(rounds)` from `len(st.rounds)`, which `complete_review_round` appends to for EVERY completed round regardless of its merged verdict, so a lane that took a CHANGES-REQUESTED round, reworked, and then passed reports "2 review round(s) approved" when one was drawn and one approved — the same shape as the claim this very function was changed to stop making ("A banner is a claim about what happened, so it counts"); `st.rounds` is also in-process, so a resumed run that redraws nothing prints "no review round was drawn" for a lane that was reviewed in an earlier run -> say what is counted ("N review round(s) drawn this run; latest verdict APPROVE") rather than asserting an approval count the tally does not carry -> @owner

VERDICT: CHANGES-REQUESTED findings=4
