# REVIEW-A round 033 — WI-579 (the verdict carrier and the adjudication_review dial)

Reviewed `git diff contract_split...HEAD` (records/generated excluded) against
AGENTS.md, PROCESS.md, the docs/requirements registries and the spec-of-record
`docs/archive/work/complete/WI-579-the-verdict-carrier-and-the-ad.md`.

## Instruments (run here, summaries only)

- `python project-trajectory/scripts/check.py --jobs 0` — `Check summary (stage
  DevStg-LLReqs, tier all)`: PASS registry-integrity / vocabulary / need-form /
  privacy / doc-navigability / skills-index / prompt-catalog /
  staged-divergence / approval-immutable; SKIP derived-stage, approval-fresh,
  **verdict-rollup** (`work branch ... generated freshness is the trunk lane's`).
- `python project-trajectory/scripts/trace.py --strict-integrity` — final line:
  `Traceability: SN=27 SR=76 LLR=190 TC=189 orphans=2 integrity=0
  verified-mechanized=72 ... interface-findings=0 provenance-findings=1
  paraphrase-advisories=3`. The one provenance finding is LLR-197 (`WI-448`),
  a row this diff does not touch — pre-existing, out of scope.
- `python -m pytest -q tests/test_verdict_record.py` — **47 passed in 15.92 s**.
- `python -m pytest -q -m smoke --collect-only` — `1524/3380 tests collected`,
  under the re-stamped `max-tests = 1560`.

## Worst failure classes this change admits, hunted first

Silent wrong content at the merge boundary (a verdict counted that did not judge
this tree), fail-open (the gate clearing on evidence that is not evidence), and
duplicate/never-drawn rounds (the OI-76 stall the row exists to kill). The
identity and evidence pipeline holds up: driven on this repo,
`governing_rev` -> `ddd08d67`, `logged_rounds` -> the 8 real rounds, and
`round_entries` correctly returns `[]` at the current tree because the
round-030 rework moved it. The two findings below are on the WRITER and the
RESUME, not the reader.

## Done-when map

WI-558 DW1 (logged-session restriction) — covered, `test_an_implementer_authored_
file_in_the_review_path_is_not_a_round`, `test_one_session_cannot_serve_a_phase_
its_log_does_not_declare`. **WI-558 DW2 (the trailer on the round's own commit)
— UNCOVERED end-to-end; see finding 1.** DW3 — covered incl. flat scope, extra
pruning and the collision refusal; the supervisor prompt's hand-compile
instruction is retired (`skills/session-protocol/SKILL.md:160` now forbids it).
DW4 — `_legacy_rollup_refusal` + two RESYNC_PACK entries (`[since 6e19da1e]`
resolves). WI-560 DW1 — covered. WI-559 DW2 — scheduling half now driven at all
three dial values; **the resume half regresses, see finding 2.** Row Done-when 4
— dial, template row, enforcement-audit row, RESYNC entry all present. Done-when
5 — the unfiltered green is claimed at `d60af4be`, a rev this review did not
re-drive; the branch-tip green was not re-run here.

## Findings

- [BLOCKER] project-trajectory/scripts/agent_loop.py:2588 (`complete_review_round` -> `review_verdict_trailer`) -> WI-558 Done-when 2's writer has NEVER produced an artifact on the shipped path: a scan of `git log --all` for the exact `TRAILER_RE` grammar finds **0 real `Review-Verdict:` trailers in the entire repository history**, while four `telemetry: session NNN review scoreboard` commits (`d399316d`, `8a94564d`, `97d65b00`, `4af3d525`) prove `complete_review_round` ran with the trailer wired in (`grep -c 'trailer=review_verdict_trailer'` == 1 at each of those four revs) and all four carry a bare one-line message. Re-running the EXACT `kitlib/verdict.py` from `4af3d525` against rev `b30c290a` (the branch tip when round 030 completed) yields `entries=[('REVIEW-A', 30, 'CHANGES-REQUESTED')] count=1` — a derivable `Review-Verdict: CHANGES-REQUESTED rounds=1 tree=eae7c867…` that was never written. The absence is undetectable by construction: `_round_refusal` reads `stamped = attested[-1] if attested else None` and stands down when it is None, so the cross-check DW2 specifies is a permanent no-op and the gate silently reports no contradiction because it has nothing to contradict -> drive `complete_review_round` end-to-end on a repository fixture (the tests only ever call `review_verdict_trailer(root, "APPROVE", worker)` with a hand-built worker dict — tests/test_verdict_record.py:820, :1105, :1114 — so every arm between the round completing and the commit landing is untested), isolate why the live call returns None, and fix it -> @owner
- [MAJOR] project-trajectory/scripts/agent_loop.py:3456 (`resume_owed_round`) -> a surviving `out/review-owed` marker makes the resume redraw EVERY declared phase even when the committed evidence says none is owed, re-admitting the duplicate-round class WI-560 DW1 claims to make unrepresentable. The guard is an OR (`if not fields and not owed: return`), so `fields` truthy alone proceeds, and `schedule_review_round(owed)` then hits `list(phases or kverdict.declared_phases(self.rp_int))` — driven: `schedule_review_round([])` at `rp_int=2` returns `['REVIEW-A', 'REVIEW-B']`. Reachable because `clear_review_owed` fires only inside `complete_review_round` (line 2562), which runs after every reviewer session has already committed its verdict file: a run killed in that window, or a final reviewer session that commits its file and then times out, leaves marker-present + evidence-complete. This contradicts the function's own docstring ("the evidence names the phases still missing at this identity and only those are queued") and `write_review_owed`'s ("the marker is deliberately NOT the durable evidence") -> make the empty list mean empty: return when the evidence was READABLE and answers no owed phase, and drop the `phases or …` fallback so "no phases owed" and "caller specified nothing" stop sharing one falsey value — the defect is representable only because `schedule_review_round`'s optional-argument default conflates those two states, and requiring the caller to always pass an explicit list (or a distinct sentinel) deletes the fallback path rather than guarding it, per the `antidote` skill's "smallest change that makes this fix unnecessary" -> @owner
- [MINOR] project-trajectory/scripts/integrate.py:1375 -> the migration window is consulted only at `required == 1` (`if not entries and required == 1:`), so an adopter running `review-policy = 2` who holds a legacy hand-authored `docs/reviews/WI-<n>-REVIEW-A.md` gets no window at all — the gate refuses with the round-evidence message and never names the legacy path or its WARN. WI-558 Done-when 4 and the RESYNC_PACK entry both state the window unconditionally ("the gate accepts EITHER the round-file evidence or a legacy hand-authored rollup"), with no policy scoping -> either scope the window in the Done-when/RESYNC prose to policy 1, or let the legacy rollup satisfy one phase at policy 2; for clarity, the shipped narrowing and the promised behaviour should not disagree -> @owner
- [MINOR] project-trajectory/scripts/integrate.py:1416 (`_round_refusal` cross-check) -> a second honest round at one governing tree whose `commit_telemetry` is vetoed (that call is documented best-effort — "a hook veto ... never fatal") leaves the newest attestation stamped `rounds=N-1` while `round_count(entries)` reads `N`, and the gate then refuses an approved lane with "the attestation and the evidence disagree" — the OI-76 supervisor stop, re-created by the cross-check meant to prevent it, in the one case `branch_trailers`' own docstring says is normal ("a round is re-drawn without the work changing") -> treat a stamped count STRICTLY LESS THAN the evidence count as a superseded stamp rather than a contradiction (only a differing WORD, or a count above the evidence, can be forgery); this is not a new guard but a narrowing of an existing one, and the unrepresentable form is upstream — an attestation whose write can silently fail cannot be a reliable cross-check input, which is finding 1's territory -> @owner

VERDICT: CHANGES-REQUESTED findings=4
