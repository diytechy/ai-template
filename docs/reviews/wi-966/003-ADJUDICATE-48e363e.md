# WI-966 checkpoint sitting at 48e363e

## amendment

Seven approved rows moved against their copies. They carry WI-966's one change: the policy file's one-key-per-line shape rule retires, because since WI-880 every hook needs Python 3.11 or later, and since WI-962 the hooks read the policy through the one parse. The rows that stated the rule, or the two-reader agreement it existed to guard, are rewritten to the one parse.

I read them against WI-966's Done-when and scope dispositions, the code at this tip and the arms map. Checks I ran:
- `tests/test_process_config.py`, `tests/test_approval_level.py`, `tests/test_shell_portability.py` and the pre-push posture case pass (292 run).
- `trace.py --strict` exits 0. The only advisories on these rows are SR-031's and SR-137's "no Form", which nearly every SR carries.

Every row changed MEANING:
- I would bless the six on released rungs: SR-031, LLR-031, TC-031, SR-137, LLR-155 and TC-150.
- SN-028 sits on a held rung, so I recommend it to the owner and do not re-anchor it. No other row in this sitting shares its registry, so nothing else waits behind it.

- [MEANING] SN-028 Acceptance, Why -> before: every dial sits under bare `[section]` headers, one `key = value` per line. The shape is a checked contract, because a TOML parser and the hooks' plain-sh parse both read the file, and the two readings are pinned equal over adversarial files. A legacy file beside its key is a refusal, a migration converts the legacy files, and a bad dial is refused -> after: every dial sits in one file, and every reader takes its answer from the file's TOML parse. The legacy refusal, the migration and the bad-dial refusal are kept, and the Why drops the sh-parse and 3.8-floor history -> not the same: the checked line shape and the two-reader pin leave the need. The rung is held, so I stop here and recommend it to the owner:
  - The premise those clauses guarded is gone: the hooks refuse without Python 3.11 or later, and read the one parse.
  - What the owner asked for (one home, a loud refusal for a double declaration, no silent defaults) is kept whole, and a blind reader recovers it from need and acceptance alone.
  - The acceptance names a format ("TOML"), not a file or instrument.
  - One point for the owner (§1(a)): the need still carries the tag `shell`, which reached CROSS-PLATFORM for the sh parse that is now gone. Whether the tag stays is the owner's call.
- [MEANING+BLESS] SR-031 AcceptanceCriteria, Coincident, Rationale -> before: every enforcer reads one value per dial through one parse, the hooks' and checkers' answers agree over the adversarial shape table (the trailing-comment decoy included), and an unreadable declaration refuses at the hooks -> after: every enforcer reads one value per dial from one TOML parse, valid dotted, inline and multi-line forms included, and none refuses them for their shape. A privacy gate or reviewer declaration outside `[policies]` reads gate on and reviewer required for every enforcer, and an unreadable declaration still refuses at the hooks -> not the same: the shape-table agreement goes, valid forms are newly accepted, and a misplaced privacy key gains an explicit fail-closed outcome. Ready to bless:
  - The coherence property (one answer per dial) stays this row's.
  - The fail-closed direction the old decoy test protected is now stated outright for the case that still matters, a misplaced key.
  - `[policies]` is a declared vocabulary token, not a carrier.
  - The Rationale argues the partition with SR-137 in standing voice.
- [MEANING+BLESS] LLR-031 Detail, Title -> before: one first-non-comment-line reader shared by the hooks and two named Python readers, with the hooks taking IF-298's closed answer -> after: every enforcer, the agent layer included, takes its answer from one parsed representation. A privacy declaration outside `[policies]` reads gate on and reviewer required, a name inside a string declares nothing, and the unreadable-declaration, opt-down and hook-answer clauses are kept -> not the same: a line reader becomes a parse, and the misplaced-key and string clauses are new. Ready to bless. It decomposes SR-031's acceptance arm for arm, the code names the old cell carried are gone rather than swapped, and the arms map's five rows each have an existing, passing case.
- [MEANING+BLESS] TC-031 Method -> before: drive each hook over the adversarial shape table and compare it with the checker -> after: drive each hook and the checker over dotted, inline and multi-line forms against the parser's answer with no shape refusal; drive a misplaced privacy declaration through every reader; and keep the unreadable, mixed, posture and no-text-read arms -> not the same: the verified set changes with the rule. Ready to bless. It matches LLR-031 one for one.
- [MEANING+BLESS] SR-137 Requirement, AcceptanceCriteria, Rationale, Title -> before: one policy home whose line shape is a checked contract, a refusal naming the key and both files at three named entry points, shape violations refused yet reading ON, and wrong-typed or out-of-range dials refused -> after: one policy home, refusing a duplicate declaration or a wrong-typed or out-of-range value rather than resolving it by precedence or default, at the policy guard entry points -> not the same: the checked shape and its refusals leave the row. Ready to bless:
  - It keeps exactly what Done-when item 4 names (the one home, the duplicate-declaration refusal, the invalid-dial refusal) and drops the obsolete line-shape and two-reader clauses.
  - No retirement is owed, because those obligations stay here.
  - The fail-closed reading of a misplaced key moved to SR-031, where every enforcer's answer is judged, so it was relocated, not lost.

  Note, not a finding: the acceptance's "the policy guard entry points" no longer names the three the old cell listed. The set is the guarded readers TC-150's `test_every_guarded_entry_point_refuses_a_mixed_config` enumerates, which is the right tier for that list.
- [MEANING+BLESS] LLR-155 Detail, Rationale, Title -> before: named config-layer functions parse once, read with legacy fallback, refuse every sh-unfollowable shape and return refusal strings for duplicate, wrong-typed and out-of-range dials, plus the ordinal and one comparison -> after: the configuration layer parses once, reads with legacy fallback, returns refusal text rather than raising for those three conditions, and supplies the ordinal and one comparison. Valid TOML syntax is explicitly not a refusal condition -> not the same: the shape refusal is withdrawn and the valid-syntax exemption is new. Ready to bless. It decomposes SR-137's kept obligations in contract voice, it removes the code names rather than adding any, and its cases exist and pass.
- [MEANING+BLESS] TC-150 Method -> before: source the shipped hook's sh functions and drive them against the parser over adversarial shapes, with the mixed and wrong-typed refusals -> after: drive duplicated, wrong-typed and out-of-range declarations and valid dotted, inline and multi-line files. Each guarded entry point refuses a duplicate by key and both homes, invalid values are refused, and valid forms draw no refusal -> not the same: the sh comparison leaves, and the valid-form exemption and out-of-range arm enter. Ready to bless. It matches LLR-155 one for one.

**Stopping boundary.** The round has two chains under SN-028.
- **SR-031 → LLR-031 → TC-031:** every enforcer gives one answer per dial. LLR-031 is the one shared parse that produces that answer, and TC-031 drives every reader through it. A further LLR per TOML form or per reader would restate the same one-parse rule, because the forms differ only in input. One TC holds all the forms in a single Method.
- **SR-137 → LLR-155 → TC-150:** one home and its refusals. LLR-155 is the one configuration layer that returns them. Another LLR per refusal kind (duplicate, wrong type, out of range) would split one return path three ways. LLR-155 also serves SR-139 through its ordinal, and that is the reason it stays one row rather than two.

The two chains do not overlap: SR-031 owns agreement among consumers of a valid declaration, and SR-137 owns whether a declaration is valid. The split stops at one LLR and one TC per SR.

- HAT SECURITY -> SR-031 and SR-137 (Hat-Refs SECURITY) -> the privacy gate's fail-closed direction survives the shape rule's retirement. A misplaced privacy key reads gate on and reviewer required in every reader, an unreadable declaration refuses at the hooks, and invalid dials are refused rather than defaulted.
- HAT FIRST-RUN-ADOPTER -> no finding against these rows -> an adopter's valid TOML policy file now passes where the shape rule refused it, and the Done-when's RESYNC entry states what the file may contain.
- HAT CROSS-PLATFORM -> no finding -> the pure-sh reader this hat guarded is gone: the hooks require Python 3.11 or later and take the parse's answer, so no platform-specific text read remains. SN-028's stale `shell` tag is noted to the owner above.
- HAT MAINTAINER -> no finding -> each rationale now states its standing reason (one answer per dial; one home that refuses ambiguity), not the migration history, so a later reader can tell why each row exists.
- HAT TEST-ENGINEER -> no finding -> each LLR arm has a named, existing, passing case, and the misplaced-key arm is driven through every reader, the agent layer included.
- HAT UX-DESIGNER -> no finding -> no rendered surface. The refusal text names the key and both homes, which is what the owner acts on.
- HAT UX-ENGINEER -> no finding -> no rendered surface changes.
- HAT ACCESSIBILITY -> no finding -> textual refusals only.
- HAT PERFORMANCE -> no finding -> one parse per run replaces a parse plus a text scan, so there is no new cost.
- HAT CONSISTENCY -> SR-031 and SR-137 (Hat-Refs CONSISTENCY) -> the one parse removes the second reader whose disagreement these rows existed to catch, and the partition between them is stated in both rationales without overlap.
- HAT INTEGRITY-RECOVERABILITY -> no finding -> nothing durable is written. An unparseable file refuses rather than reading a default.
- HAT PRODUCT-FITNESS -> no finding -> the owner's ruling 10 retires the rule, and the need's outcome (one policy home, loud on ambiguity) is kept.

VERDICT: MEANING rows=7

SITTING: JUDGED kinds=amendment
