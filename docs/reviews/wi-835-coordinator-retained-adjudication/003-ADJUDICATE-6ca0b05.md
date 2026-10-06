# WI-835 — amendment adjudication at 6ca0b05 (meaning vs clarity)

Judged against the anchor in `docs/archive/last_approved`: SR-227 against the
2026-10-05 copy (a8458c22), LLR-270 against the 2026-10-06 copy (8c158b56).
Only the cells shown were judged.

- [MEANING] SR-227 Requirement + AcceptanceCriteria -> the loop's retained-class adjudications resume, mint, wait, drain and retire one session per route, write the store whole by one writer, and keep keep-warm to one bounded turn; at dial 0 nothing is minted, resumed, written or pinged; the drain inputs named in acceptance are the agent guides, policy file, loaded skills and the adjudication template -> the same lifecycle for adjudications the coordinator starts as well as the loop's: a second coordinator-route call resumes its first call's session; both routes compose one retention request; before retaining a family with a dedicated CLI home, a sign-in reading of signed in, missing or unknown (no home created, no model call) refuses on missing or unknown before any launch, home, lease or store write, names the setup action, and neither signs in nor falls back; no probe at dial 0; acceptance now says "governing inputs changed" without the list -> not the same: a correct loop-only implementation with no sign-in check fails the new text on the coordinator route and on the refusal. The Title and Rationale cells follow that change and add no further obligation.
- [MEANING] LLR-270 Detail -> governing_hash covers the guides, policy file and skills, plus the template (or override text) of the brief being launched -> governing_hash covers those, plus the template of every brief class `retain_for` names, each as its wired override text, else its shipped file -> not the same: under the old text, a route alternating between two retained classes drains on every switch, and editing another retained class's template never drains. Under the new text, a switch does not drain and that edit does. A correct old build fails the new one in both directions.

Re-attestation, on the RELEASED rung: I would bless both rows as amended.

- SR-227: the acceptance clause I returned in `002-ADJUDICATE-a10adc3.md`
  ("runs only from a claimed lane worktree ... verdict written by a call that
  completed within its deadline") is gone. Each remaining acceptance
  condition is now an observable check of a Requirement clause: the
  cross-route consistency, the single composition, and the
  refuse-before-retaining sign-in rule with its no-home and no-fallback
  limits. Dropping the governing-input list from acceptance moves an
  artifact list down to LLR-270, where the Detail enumerates it, which is
  the tier the spine-authoring rules put it at.
- LLR-270: a session on one route judges under every retained class, so
  hashing every retained class's template is the reading of SR-227's "the
  inputs it judges under change" that does not drain on a brief-class
  switch. `tests/test_coordinator_adjudicate.py::test_editing_another_retained_class_template_drains_the_session`
  and `::test_an_operator_override_still_drains_the_session` exercise it.

VERDICT: MEANING rows=2
