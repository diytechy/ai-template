## 2026-11-20 — WI-1010: the open-items page shows the assumptions owed, and every requirement the assumption gate asked states its argument

Deferred open items: none.

Built on the maintenance branch `maint/wi-1010`, cut from `refactor_again` at
`1cb2e8680`, outside the lane workflow at the operator's direction: no claim,
no lane review rounds, commit hooks on. The parent session reviews and merges.
The row stops before the operator's act; the flip to `assumption_gate = true`
follows the act as a one-line change, with no row filed for it.

- **The critique.** Gemini Argon's round 1 raised five findings, all adopted.
  B4: the act and the flip leave the Done-when. S1: kept whole, the page
  first, then the arguments. S4: `planmode = "single"`. S5 and S3: the spec
  names the seam (IF-075, no new one), each interface-form row's crossings
  and the IF rows that close its interface finding.
- **The page.** `trace.assumption_owing_model` is the one model of the
  assumptions and surrogates owing an acceptance; the brief's section and
  `docs/open-items.html` §2 both render it. A first-acceptance card shows its
  cells whole, a drifted one its moved cells before and after, each closed by
  the requirements relying on it (a surrogate's, the assumptions naming it).
  TC-448's three tests failed first at an assertion. `gen_open_items.py` is
  970 code lines, under the threshold; `trace.py`'s pin moves 3836 -> 3844.
- **The arguments.** Eleven waivers (SR-024, SR-129, SR-226, SR-231, SR-232,
  SR-234, SR-236, SR-238, SR-241, SR-242, SR-245), each arguing the row's own
  behaviour is the outcome and naming what it does not claim. Existing
  assumptions where one carries the argument: SR-243 on DA-016, SR-246 on
  DA-004 and DA-013, SR-247 on DA-014, SR-235 on DA-007. New, all `Drafted`:
  - DA-021 (B-09): the agent CLI keeps its hook contract (runs configured
    hooks with the documented fields, holds a denied call, exports the
    session id). SR-229, SR-230, SR-237.
  - DA-022 (B-09): its transcripts record the session as it ran, each
    response's usage once. SR-229, SR-244.
  - DA-023 (B-10, fidelity, SUR-004): the recorded and built Claude Code
    records the guard's tests use carry what the CLI writes and sends.
    SR-229, SR-230.
  - DA-024 (B-09): a coordinating session acts on the coordination
    instructions the kit publishes and injects. SR-237, SR-243, SR-244.
  - DA-025 (B-09): an agent chooses a skill by its description. SR-224.
  - DA-026 (B-02): a CLARITY ruling rules as the operator would. SR-228.
  - DA-027 (B-01, B-09): the kit runs in the normal working environment the
    review threat model names. SR-233.
  - DA-028 (B-09): judging sessions apply the written review directions.
    SR-233.
  - SUR-004: recorded coordinator session records (a real Claude Code
    2.1.289 compaction recording, built 2.1.285 transcripts, hook payloads, a
    stubbed claude), emulating EXT-005.
- **Interfaces.** IF-080 bridged also by DA-021 and DA-022; IF-275 tied to
  B-04 (a guardrail verdict during a session, as the subagent gate's
  response); IF-289 tied to B-05 (a delivered script's result contract, as
  integrate's); new IF-321 and IF-322, the two verdicts an adjudicator writes
  back, from B-10, with their contracts beside their owners' code. SR-235's
  crossing moved from B-05 to B-09. No `form` changed.
- **The four steps** (gate off): `assumption-gate` 79 -> 79 (49 + 9 + 21 ->
  68 + 11 + 0), `crossing-allocation` 9 -> 0, `interface-allocation` 6 -> 0,
  `assumption-evidence` 0 -> 0. Every line left is a `Drafted` assumption or
  surrogate, which the operator's acceptance clears.
- **For the operator:** the act over DA-001 to DA-028 and SUR-001 to SUR-004,
  and the re-accepts of the eleven waived requirements, LLR-118 and LLR-271,
  all on `docs/open-items.html` §2; then the flip.
