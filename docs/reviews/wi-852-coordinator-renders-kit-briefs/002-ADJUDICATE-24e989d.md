# WI-852 — combined adjudication at 24e989d (amendment; first-approval, re-sit)

Independent adjudicator, one sitting. I judged the amendments on the
before/after cells given in the brief, against the anchor `docs/archive/last_approved`
(system-requirements copy at c5e82208). For first approval I read both chains as
given, and, to check what TC-333 can observe, `review_brief.py` and
`tests/test_review_brief.py` as reworked (`a10c0472`). I did not use them to
work out what the author meant. `tests/test_review_brief.py` passes as built
(`22 passed in 10.21s`). `review_brief.py` imports no routing module and
resolves nothing from `docs/agents.toml`: the attended launcher chooses its
reviewer.

The rework answers the first sitting's test findings in full. Real-repository tests now drive `lane_commits`' three refusals with exit 2, no output file and a clean tree; exit 0 is driven for both `review` and `file`; and the empty test list, empty and missing named inputs, and the critique render's missing spec are each driven. The docstring no longer claims that the `-narrow` suffix keeps a narrow round from counting as the full-lane review. What remains is SR-154's re-amended Requirement.

## amendment

- [MEANING] SR-146 Requirement + AcceptanceCriteria -> before: every prompt the loop launches is a shipped, catalogued, strictly filled file, each session recording its template and fingerprint, and an unknown or unfilled slot is a refusal -> after: the same, also covering every review or critique brief an attended launcher renders; the session record is confined to loop sessions; and a refused attended render writes no brief -> not the same: a case was added. BLESSED, as in the first sitting (the cells are unchanged since): closed, observable, and its new clause is driven by `test_an_unfilled_slot_refuses_and_no_brief_is_written`.
- [MEANING] SR-154 Requirement + AcceptanceCriteria -> before: for unattended work reaching integration, verdicts come from a non-authoring session resolved from the registry under consent, cross-family where configured, with logging and bounded rework -> after: the trigger adds "or an attended launcher submits an independent review verdict", logging and rework are qualified "unattended", and the attended verdict is recorded in round-record form or refused without a record -> not the same: a trigger and a case were added. NOT blessed. Only logging and rework were qualified to the unattended trigger. The central clauses still apply to both triggers as written:
  - "obtain each review or critique verdict … from a session that did not author the work";
  - "resolved per in-process phase and tier from the delivered agent registry's declared … rows and only while the declared consent surface … is present";
  - "drawn from a different model family wherever one is configured".

  So the Requirement now obliges the attended path to resolve its reviewer from the registry, under consent, cross-family, and to obtain it from a non-author. The attended path does none of that, and nothing in it could verify authorship: `review_brief.py` resolves no route, and the launcher picks the reviewer. The built behaviour, which records or refuses a submitted verdict, satisfies the AC and fails the Requirement's literal text. The Requirement must state the two triggers' obligations separately: the existing routing obligation for unattended integration, and for an attended submission only the record-or-refuse obligation (or move that to SR-146, as the first sitting allowed). Returned: WI-852 spec `## Dispositions`, draft 1.

VERDICT: MEANING rows=2

## first-approval

- [RETURN] LLR-313 -> `review_brief.py` must:
  - build a Round only as a findings-free full review or a narrow review naming its findings file, with a non-empty test list;
  - strictly fill the reviewer and critique templates, refusing a missing spec, an unreadable or empty named input, or an unfilled slot before any brief is written;
  - accept only a verdict bound to the full reviewed commit, with one VERDICT line whose count matches its findings, and a changes request that names a finding;
  - file only an accepted verdict as the next ordinal round;
  - resolve both revisions on a branch, with the base an ancestor of the reviewed commit.

  -> DOWNWARD, every clause now has a test in TC-333, including the git refusals and both success codes (observed: 22 passed). SIDEWAYS, it overlaps no sibling. UPWARD, its render half answers SR-146 as blessed. Its filing half (`review_refusal`, `round_path`, `file_review`) answers only SR-154's amended text, which is not blessed (above). The SR-154 text on record makes no attended-filing requirement, so approving that half now would bless detail under an obligation the record does not yet hold -> not ready ONLY for that parent. The row's own text is blessable as written and needs no change. Returned: WI-852 spec `## Dispositions`, draft 1.
- [RETURN] TC-333 -> its fourteen named tests must show:
  - the attended briefs' content and strict fill;
  - each input, shape, slot and verdict refusal with no requested file;
  - the command line's git refusals with exit 2, a clean repository and no output;
  - successful render and filing with exit 0, writing only the brief or the next round record;
  - the filed review in the rollup.

  -> DOWNWARD, the Method and Expected now match the tests one for one, and every LLR-313, IF-288 and IF-289 clause is driven. But it claims to verify SR-154, whose amended text is not blessed, and it rides with LLR-313 -> not ready only for that reason; its own text is blessable as written. Returned: WI-852 spec `## Dispositions`, draft 1.

OUTCOME: RETURN rows=2

SITTING: JUDGED kinds=amendment;first-approval
