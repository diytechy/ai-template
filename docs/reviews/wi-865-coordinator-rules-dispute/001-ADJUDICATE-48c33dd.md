# WI-865 — combined adjudication at 48c33dd (amendment; first-approval)

Independent adjudicator, one sitting. I judged the amendments on the
before/after cells given in the brief, against the anchors `docs/archive/last_approved`
(system-requirements copy at c5e82208, design and test-case copies at 68b9b26b).
For first approval I read SR-234's chain, WI-865's Done-when and its specref
(the owner's 2026-10-08 ruling). To check what TC-334 can observe, I read
`kitlib/dispute.py`, the dispute arm of `adjudicate_brief.py`, the shipped
`adjudicate-dispute.template.md`, `tests/test_dispute.py`, and the dispute tests
in `tests/test_coordinator_adjudicate.py`. I did not use them to work out what
the author meant.

Runs:
- `tests/test_prompts.py -k threat_model`: `1 passed, 48 deselected`.
- The dispute tests across both modules: `33 passed, 48 deselected`.
- One probe: I weakened `_finding`'s exact-key check (`sorted(table) != sorted(_FINDING_KEYS)`) to a superset check in my working tree, and the 33 tests still passed. Restored with `git checkout`; the tree is clean.

## amendment

- [MEANING] SR-233 AcceptanceCriteria -> before: the enumerated set of finding-judging briefs, "whose only member today is the reviewer brief", each cite the definition without its examples -> after: the enumerated set each cite it, with no membership stated -> not the same: the old text fixed the set at the reviewer brief, so a build in which a second finding-judging brief (the dispute brief) did not cite §6 met it; the new text binds that brief too. BLESSED: the set is defined by its category ("delivered briefs that judge a review finding") and enumerated in `FINDING_JUDGING_BRIEFS`. The shipped dispute template cites `{process_doc} §6 "Review threat model"`, carries none of the four boundary examples, and states nothing the paragraph owns.
- [MEANING] LLR-311 Detail -> before: the reviewer brief is the set's only member and cites the bold lead -> after: every enumerated finding-judging brief cites it, membership left to the enumeration -> not the same, for the same reason: the dispute template is now bound. BLESSED: the module set it describes is accurate, and its only TestRef pins each enumerated member (below).
- [MEANING] TC-332 Expected + Method -> before: the citation is asserted for `FINDING_JUDGING_BRIEFS = (pr.REVIEWER,)` -> after: it is asserted for `(pr.REVIEWER, pr.ADJUDICATE_DISPUTE)` -> not the same: a case was added, and a dispute template lacking the citation now fails. BLESSED: the test's tuple is exactly what both cells name, the test passes, and together with the unchanged example-absence sweep over every shipped prompt it covers the widened SR-233 and LLR-311 text.

VERDICT: MEANING rows=3

## first-approval

- [APPROVE] SR-234 -> where a review finding is contested by the builder or coordinator, or recurs for a third round, the delivered adjudication content must:
  - compose a brief carrying exactly the requested findings, each finding and held position verbatim, git-derived range facts and the §6 link, and refuse malformed input with no partial sitting;
  - accept only a verdict ruling each requested finding exactly once as FIX, as DISMISS in a declared class with a reason, or as ESCALATE, each with its reason;
  - authorize no approval act with an accepted dispute verdict.

  -> UPWARD, it is honestly labelled DERIVED from SN-006 through UNATTENDED-OPS, the lens names the unbounded-review failure the owner's ruling (rule 2) describes, and the feedback to the need is stated. SIDEWAYS, it does not overlap SR-233, which owns the scope bound and the dismissal record that this row's DISMISS out-of-scope class leans on, nor SR-154, which owns review routing. DOWNWARD, every acceptance clause has a test in TC-334: the verbatim-findings composition, twelve malformed-input refusals, the well-formed parse, eleven malformed or incomplete verdicts, the empty request, `sitting.accepted` returning nothing for an accepted dispute binding, and the entry point binding the ids and refusing an empty request before launch -> ready. A closed, observable obligation, verified clause by clause.
- [RETURN] LLR-314 -> `kitlib.dispute` must:
  - accept a findings file of only a non-empty `range` and a non-empty `[[finding]]` list;
  - require each finding to carry EXACTLY id, held_by, finding and position (a unique letter-led id, held_by builder or coordinator, non-empty texts kept verbatim);
  - write and read the request line;
  - parse one RULING per requested id under the declared grammar, refusing anything missing, duplicate, unrequested, malformed or incomplete, with nothing defaulted.

  -> UPWARD and SIDEWAYS sound: it is the grammar half of SR-234, and LLR-315 is the assembly half. DOWNWARD, one clause has no verifying case. "Each finding has exactly" its four keys: weakening the check to accept extra keys leaves every TC-334 test green (observed above). A table missing a key is not driven either; without the check it would raise `KeyError` rather than refuse. Also a for-clarity point: the Detail says the texts are kept verbatim "apart from TOML delimiter newlines", but `_finding` strips every leading and trailing newline (`strip("\n")`), including the blank lines around the text, as its docstring says -> not ready, by that one clause. Returned: WI-865 spec `## Dispositions`, draft 1.
- [APPROVE] LLR-315 -> `dispute_values` must:
  - take exactly one findings-file reference and read it through `kitlib.dispute`, refusing an unreadable or malformed file;
  - accept only a hexadecimal base..head range that git resolves, and derive that range's commit and name-status facts;
  - fill the template's range, commits, request, findings and process-document values, rendering each finding and position between labelled delimiters;
  - route the class to its shipped template, so strict fill refuses a partial brief.

  -> UPWARD, it is the assembly half of SR-234. DOWNWARD, every clause has a test: zero and two references, a missing file, malformed TOML, a non-hex range, an unresolvable range, the git facts (`the lane's change`, `b.txt`), both delimiter labels with their verbatim texts, and the `BRIEF_PROMPTS` and `ROUTED` membership with its shipped template -> ready.
- [RETURN] TC-334 -> its named tests must show the four-input composition, its refusals, the verdict grammar's acceptance and refusals, no approval authorization, the routing, and the entry point's binding and pre-launch refusal, verifying SR-234, LLR-314, LLR-315 and IF-290 -> DOWNWARD, each Method step has a named test that asserts it, but the case claims to verify LLR-314 and does not drive its exact-key finding rule (see above) -> not ready until a missing-key and an extra-key finding are among its malformed-input cases. If they ride the existing parametrized test, the Method may stand as written; name them in it if it is amended. Returned: WI-865 spec `## Dispositions`, draft 1.

OUTCOME: RETURN rows=4

SITTING: JUDGED kinds=amendment;first-approval
