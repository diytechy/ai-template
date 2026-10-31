# WI-966 checkpoint sitting at d8f6fd3

## amendment

This re-sits the whole set. Since sitting 003 (`003-ADJUDICATE-48e363e.md`), three things have landed:
- dispute sitting 006 ruled both gate findings FIX;
- the fix (b724c341c) made bootstrap's in-place policy writer keep an edit only when the TOML parse confirms it;
- two reconciles moved the rows: the two misplaced privacy keys' answers are stated apart, SR-137's guarded entry points and crossing are restored, LLR-156 and TC-152 come into scope, and SN-028's migration clause is amended.

Checks I ran:
- At this tip, the writer and migration cases in `tests/test_bootstrap.py`, `tests/test_process_config.py` and `tests/test_rule_sync.py` pass (67 run).
- `trace.py --strict` exits 0.
- I re-ran my sitting-006 probe. `set_process_key` on an inline `policies` table now raises `PolicyWriteRefused`, naming the inline or dotted form and the hand-edit path, and writes nothing.
- A token check finds no new code name in any amended cell. `TOML` is a format, and `[policies]` is a table name in LLR-031's design text, which the LLR tier may name.

Nine rows changed MEANING:
- I would bless the eight on released rungs: SR-031, LLR-031, TC-031, SR-137, LLR-155, TC-150, LLR-156 and TC-152.
- SN-028 is held, so I recommend it to the owner and do not re-anchor it. No other row in this sitting shares its registry.

- [MEANING] SN-028 Acceptance, Why -> before: dials under bare `[section]` headers, one per line, the shape a checked contract pinned equal across a TOML parser and the hooks' sh parse; the legacy refusal, a migration that converts and deletes the legacy files, and bad dials refused -> after: one file, every reader taking its answer from the file's TOML parse. The migration deletes each legacy file it can confirm in the declaration, and when it cannot write one, leaves it intact with a named refusal and a hand-edit path. Bad dials are still refused, and the Why drops the sh-parse history -> not the same: the checked shape and the two-reader pin go, and the migration gains a keep-and-name outcome. The rung is held, so I stop here and recommend it to the owner:
  - The new migration clause turns sitting 006's data-loss finding into the need's own promise. A legacy declaration is never deleted on a write that did not land.
  - "So an adopter never meets that refusal unaided" still holds, because the refusal names its hand-edit path.
  - The need still carries the tag `shell`, as noted at sitting 003. It is the owner's to keep or drop.
- [MEANING+BLESS] SR-031 AcceptanceCriteria, Coincident, Rationale -> before: one parse, the hooks' and checkers' answers agreeing over the adversarial shape table, and an unreadable declaration refusing at the hooks -> after: one TOML parse, valid dotted, inline and multi-line forms read and never refused for shape. A privacy gate declaration outside the policy home's policy table reads gate on, a reviewer declaration there reads reviewer required, and an unreadable declaration still refuses -> not the same: the shape agreement goes, valid forms are accepted, and two fail-closed outcomes are stated. Ready to bless. Since 003, the two misplaced keys' outcomes are stated apart, each with its own answer, and the cell names no table header.
- [MEANING+BLESS] LLR-031 Detail, Title -> before: one first-non-comment-line reader shared by the hooks and two named Python readers -> after: every enforcer, the agent layer included, takes one parsed answer. A misplaced gate key reads gate on and a misplaced reviewer key reads reviewer required, each whatever its value or any direct or legacy declaration of its own kind. A name inside a string declares nothing, and the unreadable, opt-down and hook-answer clauses are kept -> not the same: a line reader becomes a parse, with the misplaced-key outcomes added. Ready to bless. It decomposes SR-031 arm for arm, and the arms map's five LLR-031 rows each have an existing, passing case.
- [MEANING+BLESS] TC-031 Method -> before: drive each hook over the adversarial shape table -> after: drive each hook and the checker over dotted, inline and multi-line forms against the parser; drive a misplaced gate key and a misplaced reviewer key through every reader, each to its own answer; and keep the unreadable, mixed, posture and no-text-read arms -> not the same: the verified set changes. Ready to bless. It matches LLR-031 one for one.
- [MEANING+BLESS] SR-137 Requirement, AcceptanceCriteria, Rationale, Title -> before: one home with a checked line shape, refusals at three named entry points, and shape violations refused yet reading ON -> after: one home, refusing a duplicate declaration (naming the key and both homes at every guarded entry point) and a wrong-typed or out-of-range value rather than resolving by precedence or default. The Rationale states the B-01 and B-04 crossing -> not the same: the checked shape and its refusals leave the row. Ready to bless. It keeps exactly Done-when item 4's one-home, duplicate and invalid-dial obligations. Sitting 003's note is answered: "every guarded entry point" is a closed domain again, the set TC-150's case drives. The crossing is argued in standing voice.
- [MEANING+BLESS] LLR-155 Detail, Rationale, Title -> before: named config-layer functions that parse once, read with legacy fallback, refuse sh-unfollowable shapes and return refusal strings, plus the ordinal and one comparison -> after: the configuration layer parses once, reads with legacy fallback, returns refusal text for duplicate, wrong-typed and out-of-range values, exempts valid TOML syntax, supplies the ordinal and one comparison, and refuses rather than alters a legacy dial key the migration cannot rename in place -> not the same: the shape refusal is withdrawn, and the valid-syntax exemption and the unrenameable-key refusal are new. Ready to bless. The new clause concerns the legacy fallback reading this row owns for the approval dial, it is fail-closed (the old declaration is kept), and `test_the_dial_key_rename_refuses_an_old_key_held_in_an_inline_table` holds it.

  Note, not a finding: that clause sits beside LLR-156's migration writer. The two do not overlap, because LLR-156 owns the key-setting writer and this row owns the dial-key rename. A later consolidation could still choose one home for every migration refusal.
- [MEANING+BLESS] TC-150 Method -> before: the hook's sh functions driven against the parser over adversarial shapes, with the mixed and wrong-typed refusals -> after: duplicated, wrong-typed and out-of-range declarations, valid dotted, inline and multi-line files, and an inline-held legacy rename. Duplicates are refused by key and both homes, invalid values are refused, valid forms draw no refusal, and the unreachable rename is refused with its old declaration intact -> not the same: the verified set changes. Ready to bless. It matches LLR-155 one for one.
- [MEANING+BLESS] LLR-156 Detail -> before: the writer answers three states, the write decides the delete, and `add_if_missing` makes the write total -> after: the writer keeps an in-place edit only when the TOML parse of the edited text equals the old parse with exactly that key set. Every other candidate is refused and writes nothing: an inline table, dotted keys, a key-like line inside a multi-line string, an unparseable file. A scaffold flag ends with the refusal and prints its value only when written. A refused migration keeps its legacy file, and deletes one only when the written declaration's parse holds its value. The `gate-policy` arm, the F5 duplication and the CLI are kept -> not the same: an append-to-make-total writer becomes a parse-confirmed one that refuses. Ready to bless:
  - It is sitting 006's FIX stated as a contract, closed by its equality condition.
  - It is fail-closed on every candidate it cannot confirm, and its only kept symbols are approved text.
  - The arms map's four LLR-156 rows each have existing, passing cases, the unparseable-file case included.
- [MEANING+BLESS] TC-152 Method -> before: the migration's conversion, no-op, hand-trimmed and F5-pin cases -> after: the same, plus the inline, dotted, string-decoy and unparseable refusals that leave the file unchanged; a refused migration keeping its legacy file; the ordinal migration ignoring a string decoy; an ordinary file still migrating and updating in place; and a flag reporting refusal without a value it did not write -> not the same: new arms. Ready to bless. It matches LLR-156 one for one, and the ordinary-file case guards against an over-refusal.

**Stopping boundary.** SN-028 has three chains in this round.
- **SR-031 → LLR-031 → TC-031:** one answer per dial. LLR-031 is the one shared parse that produces it. A further LLR per TOML form, per misplaced key or per reader would restate the one parse rule over different inputs, so TC-031 drives them in one Method.
- **SR-137 → LLR-155 → TC-150:** one home and its refusals. LLR-155 is the one configuration layer that returns them, and it also serves SR-139's ordinal. A split per refusal kind would divide one return path.
- **SR-138 → LLR-156 → TC-152:** the migration that keeps the one home. LLR-156 is the one writer whose parse-confirmed edit decides every write and delete. A further child per refused form would restate its one equality condition.

The three do not overlap: agreement among consumers, validity of a declaration, and the writer that changes it. The split stops at one LLR and one TC each.

- HAT SECURITY -> SR-031 and SR-137 (Hat-Refs SECURITY) -> the privacy gate fails closed on both misplaced keys and on an unreadable declaration. The writer no longer reports a requested gate on while leaving it off, and no legacy declaration is deleted on a write that did not land (sitting 006's fail-open, closed).
- HAT FIRST-RUN-ADOPTER -> no finding -> an adopter's valid TOML file is read as written. When the in-place flags or migration cannot edit that form, they refuse with a hand-edit path rather than corrupting it, and SN-028's acceptance states that path.
- HAT CROSS-PLATFORM -> no finding -> no platform text read remains, and the writer keeps its LF output. SN-028's stale `shell` tag is noted to the owner.
- HAT MAINTAINER -> no finding -> each rationale states its standing reason, and LLR-156 says why the writer confirms through the parse (no stdlib TOML writer, no return to the retired shape).
- HAT TEST-ENGINEER -> no finding -> each LLR arm has a named, existing, passing case. The ordinary-file case shows the refusal is not over-broad, and the string-decoy cases cover both the setter and the ordinal migration.
- HAT UX-DESIGNER -> no finding -> the refusal names the file, the key, the form and the fix, which is what the reader acts on.
- HAT UX-ENGINEER -> no finding -> no rendered surface changes.
- HAT ACCESSIBILITY -> no finding -> textual refusals only.
- HAT PERFORMANCE -> no finding -> one extra parse per in-place edit, at scaffold or migration time only.
- HAT CONSISTENCY -> SR-031 and SR-137 (Hat-Refs CONSISTENCY) -> the writer now reads the file the way every reader does, which closes the last disagreement between a writer and the readers that sitting 006 found.
- HAT INTEGRITY-RECOVERABILITY -> no finding -> a refused write leaves the file byte-unchanged and the legacy file in place, so every failure leaves a state the next run can name and retry.
- HAT PRODUCT-FITNESS -> no finding -> the owner's ruling 10 retires the shape rule, and the need's outcome (one home, loud on ambiguity, no silent loss) is kept and strengthened.

VERDICT: MEANING rows=9

SITTING: JUDGED kinds=amendment
