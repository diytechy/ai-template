Adjudicated: bf297a4fca04023f0e783e13a28713a4ab1ace5c

## first-approval

Read at bf297a4fc. Each row was read against its parent SR-157, its approved siblings (LLR-001..LLR-274 and their TCs), the WI-994 spec's grammar, D-004, and the reader as built (`read_test_tags`, `_read_text_tags`, `_tag_line`, `tc_tag_findings`). All 22 cited evidence nodes exist (each `def` is found once in its module). `trace.py --strict-integrity` is clean at this tip. The two evidence modules are in `SLOW_MODULES`, so the six `Full` tiers agree with where their evidence runs. The severity path is one list for all four shapes, so driving one shape per severity stands for all four. The after-prose refusal runs on every read-position line, not only one-line docstrings, so the LLR does not overclaim it. The code matches what the rows say. The rows go back on their own text, not on the build.

Stopping boundary. LLR-365 is one decision: one test-file tag grammar, read by one reader, adding four values (misplaced, malformed, unknown, unreadable) to one finding domain at one severity rule. Splitting it by shape would repeat the one grammar four times, so the LLR tier stops here. The six TCs split by verification purpose, and none repeats another. TC-404 covers read positions and what declares nothing. TC-405 covers misplaced, TC-406 malformed, TC-407 unknown and TC-408 unreadable. TC-409 covers severity, vacuity, paths and the rung transition through the check. Splitting further would only copy the parametrize ids into rows.

- [RETURN] LLR-365 -> a test-file `Implements:` declaration is read only at the declared Python read positions (and at file level elsewhere); a misplaced, malformed, unknown or unreadable one is refused naming its file, line and shape; findings warn plain and error strict, gating from DevStg-Impl; an absent tests root or TC registry is vacuous -> the chain is complete and the code agrees with the text: upward, SR-157's acceptance takes in a rule added at a checker's declaration site; sideways, nothing overlaps LLR-204's code-side grammar; downward, the arms map's four gaps are closed at bf297a4 (the authority clause is gone, the repeat rule is stated, TC-406 names the wrap) -> not ready, on three counts. (1) `phase = 1`. The spine is in phase 6 (`docs/stage` `phase = 6`). Every recent child of SR-157 is stamped 6 (LLR-260, LLR-272, LLR-274), and so is the lane's neighbour LLR-364. The spec's "item 13, phase 1" is the review-churn plan's phase, not a delivery phase, and no row or decision records why this one belongs to the foundation phase. Approving it would put a false phase claim on the record. (2) "No tests root or test-case registry is vacuous." read literally says no such root or registry is vacuous, which is the opposite of what is meant. TC-409's "absent inputs are vacuous" says it correctly. (3) "names only the test cases it runs" sets a limit nothing observes. The reader checks that the list is TC ids, never that the test runs them, and a declaration naming a case its test does not run maps with no finding. This is the same reason D-004 gave for dropping "A declaration can only add a finding". Lesser notes, not grounds: "supported test-file type" and "supported workflows" leave their closed sets to the trace home.
- [RETURN] TC-404 -> drive both Python read positions, their union and a repeat, file-level reading in another supported type, the silent cases (an unsupported file, a fixture string, a backticked mention), a BOM file, and the unchanged source-side readers -> its eight nodes reach every arm it claims (arms 1-8, 21, 24), and "without a repeat finding" now has its LLR sentence -> the text is sound, but its `phase = 1` repeats LLR-365's mis-stamp, and it verifies a row going back for amendment. It returns with its parent so the two are re-stamped and re-sat together.
- [RETURN] TC-405 -> each declaration outside a read position, a pytest-fixture docstring included, is one misplaced finding naming its file, line and shape -> its two nodes drive helpers, classes, nested defs, non-test-class methods, every fixture decorator form, conftest, a non-test module, and comments above, beside and bare -> not ready: its Method says "Drive declarations in every closed Python read position". That term is defined in no row, and it names the opposite of what is driven: the drive is positions OUTSIDE a read position, in LLR-365's own words. It also carries the `phase = 1` mis-stamp.
- [RETURN] TC-406 -> each invalid declaration, a next line continuing a valid list included, is one malformed finding naming its file, line and shape; the one-line message directs the declaration to its own line; a mention does not block a valid declaration -> its nodes drive every list shape, the six wrap forms, the one-line after-prose shape with its "own line" detail, and the no-wrap boundary -> the text is sound, but `phase = 1` repeats the parent's mis-stamp. It returns with LLR-365.
- [RETURN] TC-407 -> absent, example and retired ids are unknown findings, a live id still maps, and a Drafted TC is clean -> it drives the reader and the check, with a deleted row standing for "retired" (the vocabulary has no retired status) -> the text is sound, but `phase = 1` repeats the parent's mis-stamp. It returns with LLR-365.
- [RETURN] TC-408 -> each undecodable or unparseable supported test file is one unreadable finding naming its file, line and shape -> it drives a binary `.py` and `.rs`, a broken `conftest.py` and a syntax error at its line -> the text is sound, but `phase = 1` repeats the parent's mis-stamp. It returns with LLR-365.
- [RETURN] TC-409 -> through the check, a finding warns plain and errors strict naming its repo-relative file, line and shape; an absent tests root or registry is vacuous; a bootstrapped project warns below DevStg-Impl and fails at it -> it drives plain and strict, both vacuity cases, a nested root and the scaffold's rung transition; the WARN side drives `misplaced` only, which stands for all four because the severity path is one list -> the text is sound, but `phase = 1` repeats the parent's mis-stamp. It returns with LLR-365. (IF-131 and IF-263 are unstatused and not ruled here.)

OUTCOME: RETURN rows=7

## Return answered in the lane

```toml
title = "LLR-365 and TC-404 to TC-409 return: the phase stamp, the inverted vacuity sentence, the unobserved 'it runs' limit, and TC-405's 'closed read position'"
workstream = "process"
safety_class = "spine"
buildtier = "medium"
priority = 5
specref = "docs/requirements/low-level-requirements.toml"
sr_refs = ["SR-157"]
needs = ["WI-994"]
```

VERDICT THIS CONTINUES: `docs/reviews/wi-994/005-ADJUDICATE-bf297a4.md`, `OUTCOME: RETURN rows=7` over LLR-365 and TC-404 to TC-409. The code is not in question. The verdict found it agrees with every sentence the rows keep. Scope is four cell edits and one re-sitting, nothing more:

1. `phase` on LLR-365 and on TC-404 to TC-409. Re-stamp all seven to the current delivery phase (6, as on the SR-157 children LLR-260, LLR-272 and LLR-274). The other way out is to record in LLR-365's `rationale` why this rule belongs to the foundation phase. Either way the seven cells must agree.
2. LLR-365 `detail`, the sentence "No tests root or test-case registry is vacuous." Restate it so the literal reading is the meant one, e.g. "An absent tests root, or an absent test-case registry, makes the check vacuous."
3. LLR-365 `detail`, the opening "names only the test cases it runs". Either drop the limit, or say it is the declaration's meaning and that the reader checks only that each named id is a live test case. As it stands it claims a check nothing makes, the same ground D-004 used for the clause it removed.
4. TC-405 `method`, "every closed Python read position". Replace it with LLR-365's own term, "each Python position outside a read position", listing what the evidence drives.

Out of scope: any code or test change, IF-131 and IF-263, and the arms map's "Not counted" items. If WI-994's own lane makes these edits and its next sitting approves the rows before merge, this row has nothing left to do and closes on that record.

SITTING: JUDGED kinds=first-approval
