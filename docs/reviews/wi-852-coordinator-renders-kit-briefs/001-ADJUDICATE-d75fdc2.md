# WI-852 — combined adjudication at d75fdc2 (amendment; first-approval)

Independent adjudicator, one sitting. I judged the amendments on the
before/after cells given in the brief, against the anchor
`docs/archive/last_approved` (system-requirements copy at c5e82208). For first
approval I read the SR-146 and SR-154 chains as given, WI-852's Done-when, and,
to check what TC-333 can observe, `project-trajectory/scripts/review_brief.py`
and `tests/test_review_brief.py`. I did not use them to work out what the author
meant. `tests/test_review_brief.py` passes as built (`14 passed in 0.30s`).

## amendment

- [MEANING] SR-146 Requirement + AcceptanceCriteria -> before: every prompt the loop launches is a shipped, catalogued, strictly filled file, each session recording its template and fingerprint, and an unknown or unfilled slot is a refusal -> after: the scope widens to every brief an attended launcher renders as a review or critique brief; the per-session record narrows to loop sessions; and the AC adds that a refused attended render writes no brief -> not the same: a case was added in both cells. An attended render that wrote a partial brief before refusing would satisfy the old text and fail the new one. BLESSED: the new text is closed and observable. The reviewer and critique templates it binds are shipped and catalogued. "Each loop session" correctly confines the session record to where a session exists. The new AC clause has a verifying case: `test_an_unfilled_slot_refuses_and_no_brief_is_written` drives the command line and asserts that no `--out` file exists.
- [MEANING] SR-154 AcceptanceCriteria -> before: the unattended loop's review scheduling, routing, logging and bounded rework -> after: the same, plus a new case: an attended independent review verdict is recorded in the loop's round-record form, and a malformed or commit-unbound verdict is refused with no record -> not the same: a case was added, so any implementation of the old text is silent on attended verdicts. NOT blessed: the added clause has no home in the row's Requirement. The Requirement still opens "When unattended work reaches integration, the delivered loop content shall obtain each review or critique verdict…" and was not amended. So the acceptance now tests an obligation that a reader of the Requirement cannot derive, and an acceptance criterion must accept its own requirement. Either the Requirement states the attended recording obligation (who records, in what form, refused when), or the clause moves to a row whose requirement carries it (SR-146 was widened to attended renders in this same change set). Returned: WI-852 spec `## Dispositions`, draft 1.

VERDICT: MEANING rows=2

## first-approval

- [RETURN] LLR-313 -> review_brief.py must:
  - construct a Round only as a findings-free full-lane review or a narrow review naming its findings file, with a non-empty test list;
  - strictly fill the shipped reviewer template (spec, range, test command, scratch, optional rubric, verdict path) and the shipped critique template (spec, named rubric), refusing a missing spec, an unreadable or empty named input, or an unfilled slot before any brief is written;
  - accept a verdict only when it is bound to the full reviewed commit, has exactly one VERDICT line whose count matches its findings, and names a finding when it requests changes;
  - file only an accepted verdict, as the next ordinal round file;
  - resolve both revisions on a branch, with the base an ancestor of the reviewed commit.

  -> UPWARD, it serves SR-146's widened text (the attended render) and SR-154's amended acceptance (the round record). But SR-154's added clause is not blessed (see the amendment section), so the parent this row's filing half answers is unsettled. SIDEWAYS, it overlaps no LLR under either SR: LLR-045/048 schedule the loop's reviews, and this row only renders and files. DOWNWARD, TC-333, its only TestRef, leaves four of its clauses unverified:
  - `lane_commits` (on a branch; both revisions commits; base an ancestor) is never called. The one test that reaches the command line monkeypatches it out, and no other test names it.
  - "requires its test list" is never driven: no Round is built with empty tests.
  - "unreadable or empty named input" is driven only for a missing rubric file. An empty file and a missing findings file are not driven.
  - A missing spec is driven for the review render, not the critique render.

  -> not ready. An unsettled parent, and four obligations with no verifying case. Returned: WI-852 spec `## Dispositions`, draft 1.
- [RETURN] TC-333 -> its eight named tests must show that a complete attended brief has no unfilled slot and carries the kit clauses, lane facts or scope rubric; that invalid round shapes, named inputs, slots and verdicts refuse with no requested file; and that a filed review renders in the rollup. It claims to verify SR-146, SR-154, LLR-313, IF-288 and IF-289 -> DOWNWARD, every Method step matches a named test that asserts it, but the claim is wider than the Method:
  - IF-289's exit codes and their git refusals (not on a branch, not a commit, not an ancestor) are never driven. The only exit code observed is 2, for an unfilled slot, past a monkeypatched `lane_commits`. No test drives exit 0 for a written brief or a filed review.
  - LLR-313's `lane_commits`, empty-test-list, empty-input and critique-missing-spec clauses are unverified (see above).
  - SR-154's added clause is not blessed.

  -> not ready. It claims to verify two interfaces and an LLR whose refusal arms it never drives. Returned: WI-852 spec `## Dispositions`, draft 1.

OUTCOME: RETURN rows=2

SITTING: JUDGED kinds=amendment;first-approval
