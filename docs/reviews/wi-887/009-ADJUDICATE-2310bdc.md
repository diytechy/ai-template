# WI-887 checkpoint sitting 009 — amendment

Judged at 2310bdc96. These rows answer gate 007's F3–F6 and dispute 008's DB.
Checked against the lane, not taken from either party's account:

- `applies` (session_keep.py ~831) keeps a REVIEW-A/B call only on a named route, with `review_reset_pct > 0` and a non-empty scope.
- `_OPTIONAL` declares all eleven optional occupancy, use and compaction fields. `_variant` checks them on a full record.
- `test_a_mistyped_optional_field_is_no_record_and_the_resumed_review_mints` has one case per declared field, and TC-351's Evidence names it. Its cases and those of `test_a_malformed_final_reviewer_turns_retention_off_through_the_draw` pass (15 passed).
- `trace.py --strict` no longer reports SR-239. Its one remaining finding is LLR-292's "minimal", which predates the lane (dispute 008).

## amendment

- [MEANING] SR-239 Requirement -> two sentences: retention obligations where the reviewer dial is above zero, plus a second `shall` reading a malformed setting, or persisted-while-off, as off and fresh -> one `shall` that resolves the setting first: malformed or persisted-while-off reads as off and fresh; OTHERWISE, where the dial is above zero, the same retention obligations hold -> the overlap case changed. With a positive percent and a malformed final-reviewer setting, the old text imposed both readings and the new text gives the fail-closed reading precedence. That is a resolved precedence, not a rewording. BLESS: yes. It is the response-clause shape dispute 008 allowed, it keeps the fail-closed condition reachable, and it passes the singular gate. Its unchanged AC still observes each clause.
- [MEANING] LLR-270 Detail -> `applies` described only for ADJUDICATE calls, and `_read_record` typing "all consumed fields" -> adds the REVIEW arm (a named route, `review_reset_pct` above 0, a non-empty scope, else no plan), and types each optional occupancy, use or compaction field as its writer writes it -> a new admission arm and a narrower accepted record set. BLESS: yes; it matches the code observed above. The ADJUDICATE arm's code also requires an empty scope. The cell's "only for" still states a necessary condition there, so it does not contradict the code.
- [MEANING] TC-205 Expected -> the merge is refused when FRESH full-lane claim-base evidence is absent (contradicting its own later clause that a persisted final scope can gate) -> refused when the MODE's admissible full-lane claim-base evidence is absent -> in persisted mode the acceptance condition changes. BLESS: yes; it now agrees with SR-156 and its own later clause.
- [MEANING] TC-266 Method -> verifies off and malformed percent dials, and persisted-at-zero reading fresh -> also verifies that an invalid final-reviewer word or type reads off and fresh even with a positive percent, and that the loop's review draws then retain nothing -> a new verified case. BLESS: yes; it is SR-239's fail-closed clause at its overlap case, held by the whole-file Evidence (test_a_malformed_final_reviewer_turns_retention_off_through_the_draw).
- [MEANING] TC-351 Method -> verifies writer-produced variants reload -> also verifies that a live record with a mistyped optional field reads as no record, and that the next review round mints and bookkeeps fresh instead of resuming and raising -> a new verified case (dispute 008 DA's regression). BLESS: yes; the parametrised test is named in its Evidence and covers every declared optional field.

VERDICT: MEANING rows=5

The act: `intake.py snapshot --reattests SR-239,LLR-270,TC-205,TC-266,TC-351 --verdict` this file.

SITTING: JUDGED kinds=amendment
